---
layout: technical
category: foundations
title: Fourier Optics
description: GeoSignal Preview의 Fourier optics 기술 노트
permalink: /ko/notes/fourier-optics/
lang: ko
---

# Fourier Optics

Fourier optics는 마스크 형상, 공간주파수 필터링과 영상 형성을 연결합니다. FFT는 샘플링된 격자에서 이 계산을 효율적으로 수행하는 알고리즘입니다.

---

## 관련 페이지

* [기술 노트로 돌아가기]({{ '/ko/notes/' | relative_url }})
* [방법론]({{ '/ko/method/' | relative_url }})
* [데모]({{ '/ko/demo/' | relative_url }})


## 학습 확장: Fourier Optics에서 FFT까지

FFT는 물리 법칙이 아니라 Fourier transform을 효율적으로 계산하는 알고리즘입니다. ML에서 FFT layer를 썼다는 사실만으로 광학적 정합성이 확보되는 것은 아닙니다.

* 목차
{:toc}

## 공간 주파수와 convolution theorem

다음 transform convention을 사용합니다.

$$
\widehat m(\mathbf f)=\int m(\mathbf x)e^{-i2\pi\mathbf f\cdot\mathbf x}\,d\mathbf x,\qquad
m(\mathbf x)=\int\widehat m(\mathbf f)e^{i2\pi\mathbf f\cdot\mathbf x}\,d\mathbf f.
$$

$$x,y$$는 µm, $$f_x,f_y$$는 µm⁻¹입니다. 연속 2D transform의 $$\widehat m$$에는 µm²의 적분 차원이 있으나 discrete FFT array는 선택한 normalization에 따라 다릅니다. 연속·이산 수식 간 면적 factor를 생략한 값을 임의로 혼용하지 않습니다.

Shift-invariant coherent imaging에서 amplitude impulse response를 $$h$$라 하면

$$
E(\mathbf x)=(h*m)(\mathbf x)=\int h(\mathbf x-\boldsymbol\xi)m(\boldsymbol\xi)d\boldsymbol\xi,
\qquad \widehat E=\widehat h\widehat m=P\widehat m.
$$

두 번째 등식은 첫 적분을 Fourier transform하고 $$\mathbf u=\mathbf x-\boldsymbol\xi$$로 치환하면 유도됩니다. $$m(\boldsymbol\xi)$$의 transform과 $$h(\mathbf u)$$의 transform이 곱으로 분리되기 때문입니다. 연속에서 $$h$$ 단위는 µm⁻²로 잡아 $$E$$를 정규화된 무차원 amplitude로 둘 수 있습니다.

## FFT의 격자와 aliasing

$$N_x\times N_y$$ grid에서 pixel 간격이 $$\Delta x,\Delta y$$ [µm]일 때

$$
\Delta f_x=\frac{1}{N_x\Delta x},\qquad f_{\mathrm{Nyquist},x}=\frac{1}{2\Delta x}.
$$

예를 들어 1 nm pixel·2000 pixel 폭이면 ROI 폭은 2 µm, 주파수 간격은 0.5 µm⁻¹입니다. 같은 pixel 크기에서 ROI 폭을 늘리면 주파수 간격이 좁아집니다. 따라서 FNO에서 같은 index의 mode를 재사용해도 같은 물리 주파수라는 보장이 없습니다. DOINN의 large-tile 전략을 이해하는 핵심입니다.

`fft2`는 주기 경계를 가정합니다. `fftshift`는 DC를 중앙으로 옮기는 index permutation이며 광학적 연산이 아닙니다. 배열이 shifted인지 아닌지 kernel과 mask spectrum을 함께 맞춰야 합니다. zero padding은 wrap-around를 완화할 수 있지만 누락된 ROI 외부 geometry를 복원하지는 못합니다. 주변 pattern을 포함한 halo와 최종 core crop이 필요합니다.

## Pupil cutoff와 intensity bandwidth

Coherent field의 support가 pupil cutoff $$f_c$$로 제한되더라도 $$I=EE^*$$는 frequency-domain autocorrelation이므로 intensity bandwidth는 단순히 field cutoff와 같지 않습니다. 서로 다른 주파수 $$f_1,f_2$$의 차이 $$f_1-f_2$$가 intensity에 나타납니다. 이 이유로 kernel dimension 설계에서는 field와 intensity grid의 support를 구분해야 합니다.

## FNO와 물리 convolution의 차이

일반적인 Fourier layer의 학습 weight $$R$$은 frequency별로 채널을 혼합합니다.

$$
v_{\ell+1}=\rho\{W_\ell v_\ell+\mathcal F^{-1}[R_\ell(\mathbf f)\mathcal F(v_\ell)]\}.
$$

$$v$$는 latent feature, $$W,R$$은 학습 weight, $$\rho$$는 activation입니다. 이는 optical kernel과 비슷한 계산 패턴이지만 kernel support·Hermitian symmetry·nonnegative intensity·source incoherence가 자동으로 보장되지는 않습니다. DOINN은 global Fourier branch와 local CNN branch를 조합하고, Nitho는 물리 합성식을 고정한 채 kernel만 학습합니다.

## 복소수 layer의 직접 계산

$$
(a+ib)*(c+id)=(a*c-b*d)+i(a*d+b*c).
$$

실수 convolution 네 개로 구현할 수 있습니다. 예를 들어 $$(1+i)(1-i)=2$$이며 imaginary 부분은 상쇄됩니다. 실수·허수의 두 channel에 별도 비선형을 적용하면 일반적으로 complex analytic function은 아닙니다. 실수 파라미터에 대한 자동미분이 가능하다는 것과 Cauchy–Riemann 조건을 만족한다는 것은 구분합니다.

## 참고자료와 다음 단계

* [회절 차수와 디포커스: 경사 조명의 이미징 원리]({{ '/ko/notes/diffraction-defocus/' | relative_url }}) — 주기적 마스크로 pupil·위상·영상의 관계를 확인합니다.
* [Abbe Imaging]({{ '/ko/notes/abbe-imaging/' | relative_url }})
* [Hopkins/TCC/SOCS]({{ '/ko/notes/foundations/hopkins-tcc-socs/' | relative_url }})
* [DOINN 원문, Section 3](https://arxiv.org/html/2203.08616v1)
* [Nitho 원문, Section III](https://arxiv.org/html/2303.08435v4)
