---
layout: technical
category: foundations
title: "회절 차수와 디포커스: 경사 조명의 이미징 원리"
description: 주기적 마스크의 고차 회절항, pupil과 디포커스 위상을 통해 3-beam·2-beam 이미징과 경사 조명의 원리를 이해합니다.
permalink: /ko/notes/diffraction-defocus/
lang: ko
---

<p class="language-switch"><a href="{{ '/notes/diffraction-defocus/' | relative_url }}" lang="en">View in English</a></p>

# 회절 차수와 디포커스: 경사 조명의 이미징 원리

사각형 마스크의 모서리는 왜 영상에서 둥글어질까요? 조명을 기울이면 왜 초점 변화에 덜 민감해질 수 있을까요? 주기적인 1D line-and-space 마스크를 회절 차수의 합으로 표현하면 두 질문을 같은 pupil 그림으로 설명할 수 있습니다.

이 노트는 [Fourier Optics]({{ '/ko/notes/fourier-optics/' | relative_url }})와 [Abbe Imaging]({{ '/ko/notes/abbe-imaging/' | relative_url }})를 잇는 학습 예제입니다. 각 광원점에서는 전계를 합성하고, 서로 비간섭인 광원점 사이에서는 강도를 더합니다. 마스크는 얇은 amplitude mask, 전파는 균일 매질의 스칼라 모델로 한정합니다.

{% include diffraction-demo-cta.html %}

* 목차
{:toc}

## 1. 좌표와 단위

모든 길이는 웨이퍼 기준으로 정의하며 축소 배율은 별도로 포함하지 않습니다.

| 기호 | 의미 | 단위 |
| --- | --- | --- |
| $$x,P,w$$ | 위치, 마스크 피치, 투과 영역 폭 | µm |
| $$D=w/P$$ | 듀티 비 | 무차원 |
| $$\lambda_0$$ | 진공 파장 | µm |
| $$n_m$$ | 균일한 전파 매질의 굴절률 | 무차원 |
| $$\mathrm{NA}=n_m\sin\theta_{\max}$$ | 개구수 | 무차원 |
| $$f_0=1/P,\ f_s$$ | 기본 공간주파수, 입사 공간주파수 | cycle/µm |
| $$z$$ | 이상적 정초점에서의 signed defocus | µm |

이 노트의 회절 차수 정수는 $$j$$로 표기해 굴절률 $$n_m$$와 구분합니다. 입사각과 주파수의 관계는 $$f_s=n_m\sin\theta_s/\lambda_0$$이며, $$f_s$$ 자체가 각도는 아닙니다. pupil cutoff는 $$f_c=\mathrm{NA}/\lambda_0$$입니다.

무차원 예제에는 $$u=\lambda_0 f$$, $$\xi=x/\lambda_0$$, $$\zeta=z/\lambda_0$$를 사용합니다. 이 정의에서 cutoff는 $$\lvert u\rvert\le\mathrm{NA}$$입니다. 길이를 $$\lambda_0/\mathrm{NA}$$로 정규화하는 다른 관례와 섞어 쓰지 않습니다.

## 2. 사각형 마스크를 회절 차수로 분해하기

한 주기의 중앙에서 폭 $$w$$만 투과하는 마스크의 복소 푸리에 급수는 다음과 같습니다.

$$
m(x)=\sum_{j=-\infty}^{\infty}c_j e^{i2\pi jx/P},\qquad
c_j=\frac{1}{P}\int_{-w/2}^{w/2}e^{-i2\pi jx/P}\,dx
=D\,\operatorname{sinc}(jD).
$$

여기서 $$\operatorname{sinc}(v)=\sin(\pi v)/(\pi v)$$이며 NumPy의 `np.sinc`와 같은 정의입니다. 따라서 $$c_0=D$$, $$j\ne0$$일 때 $$c_j=\sin(\pi jD)/(\pi j)$$입니다. $$c_0$$는 평균 **진폭 투과율**이고, 0차만 통과할 때 강도는 $$D^2$$입니다. 모든 차수를 포함한 이진 마스크의 한 주기 평균 강도 $$D$$와 구분해야 합니다.

$$D=0.5$$이면 0차를 제외한 짝수 차수는 사라집니다. 고차항이 부족하다고 해서 항상 ±2차를 추가하면 해결되는 것이 아닙니다. 이 경우에는 ±3, ±5차 등의 홀수항이 모서리 재현에 기여합니다. $$D=0.3$$에서는 짝수 차수도 일반적으로 남습니다.

<figure class="study-figure">
  <a class="figure-zoom" href="{{ '/assets/notes/diffraction-defocus/fourier-orders.png' | relative_url }}"><img src="{{ '/assets/notes/diffraction-defocus/fourier-orders.png' | relative_url }}" alt="듀티 비 0.5와 0.3의 부호 있는 푸리에 계수 비교. 듀티 비 0.5에서는 0차를 제외한 짝수항이 사라지고 일부 홀수항은 음수이다." loading="lazy"></a>
  <figcaption>그림 1. 막대의 부호는 복소 진폭의 위상과 연결됩니다. 음수인 계수를 절댓값으로 바꾼 뒤 전계를 합성하면 다른 영상이 됩니다.</figcaption>
</figure>

유한한 차수로 불연속 마스크를 복원하면 모서리 주변에 Gibbs 진동이 남을 수 있습니다. 고차항 추가는 정확한 사각형으로 단조롭게 수렴하는 강도 곡선을 보장하지 않습니다.

## 3. 조명 방향과 pupil을 함께 보기

입사 carrier를 포함한 각 차수의 pupil 주파수를 다음 부호 규약으로 정의합니다.

$$
f_j=f_s+\frac{j}{P},\qquad
A_j(z)=c_j\,\mathbf 1_{|f_j|\le f_c}\,e^{i\phi(f_j,z)},\qquad
I(x,z)=\left|\sum_j A_j(z)e^{i2\pi jx/P}\right|^2.
$$

전계에 공통으로 곱해지는 $$e^{i2\pi f_sx}$$는 강도를 바꾸지 않으므로 마지막 식에서 생략했습니다. GeoSignal의 기존 shifted-pupil API는 $$j/P-s_x$$ 규약을 쓰므로 이 노트의 조명과 비교할 때 $$s_x=-f_s$$로 대응합니다. 부호 규약을 바꿀 때는 비대칭 조명과 정초점 밖의 영상도 함께 검증해야 합니다.

<figure class="study-figure">
  <a class="figure-zoom" href="{{ '/assets/notes/diffraction-defocus/pupil-comparison.png' | relative_url }}"><img src="{{ '/assets/notes/diffraction-defocus/pupil-comparison.png' | relative_url }}" alt="동일한 pupil에서 수직 조명은 −1·0·+1차를, 대칭 경사 조명은 0·+1차만 통과시키는 비교. pupil 좌표는 파장 곱하기 공간주파수이다." loading="lazy"></a>
  <figcaption>그림 2. λ₀=248 nm, P=620 nm, D=0.5, NA=0.50, 공기 매질. 경사 조명의 0·+1차는 u=−0.20,+0.20에 대칭으로 위치합니다. 막대 높이는 |cⱼ|이고 회색은 차단된 차수입니다.</figcaption>
</figure>

최대 차수를 $$N$$으로 정했다면 합은 $$-N\le j\le N$$으로 제한됩니다. 실제 pupil에 들어오는 정수 구간은 다음과 같으므로, 임의의 ±5차 고정이 모든 설정에 충분하지는 않습니다.

$$
\left\lceil P(-f_c-f_s)\right\rceil\le j\le
\left\lfloor P(f_c-f_s)\right\rfloor.
$$

의도적으로 차수를 잘라 비교할 때는 물리적인 pupil 차단과 사용자가 설정한 차수 절단을 따로 표시해야 합니다.

## 4. 디포커스의 2차 위상은 어디에서 오는가

시간 의존성을 $$e^{-i\omega t}$$로 두면 균일 매질에서

$$
k_z=\frac{2\pi}{\lambda_0}\sqrt{n_m^2-(\lambda_0 f)^2}.
$$

강도에 영향을 주지 않는 piston을 제거한 스칼라 전파 위상은

$$
\phi_{\mathrm{AS}}(f,z)=\frac{2\pi z}{\lambda_0}
\left[\sqrt{n_m^2-(\lambda_0 f)^2}-n_m\right].
$$

$$\lvert\lambda_0f\rvert\ll n_m$$인 근축 범위에서 제곱근을 전개하면

$$
\phi_{\mathrm{paraxial}}(f,z)=-\pi\frac{\lambda_0}{n_m}zf^2,\qquad
P_z(f)=\mathbf 1_{|f|\le f_c}\,e^{i\phi(f,z)}.
$$

공기 모델 $$n_m=1$$에서 익숙한 $$-\pi\lambda_0zf^2$$가 됩니다. 무차원 좌표로는 $$\phi=-\pi\zeta u^2/n_m$$입니다. 높은 NA에서는 근축 근사와 angular-spectrum 위상을 구분해야 합니다. angular-spectrum도 여기서는 스칼라 전파식이며 벡터·편광·mask-3D·실제 렌즈 수차까지 정확히 푼다는 의미는 아닙니다.

## 5. 3-beam과 2-beam의 초점 민감도

### 수직 조명: DC와 ±1차의 위상이 달라진다

0·±1차만 통과하고 마스크 계수가 실수일 때

$$
E(x,z)=c_0+2c_1e^{i\delta(z)}\cos(2\pi x/P),\qquad
\delta(z)=\phi(1/P,z)-\phi(0,z).
$$

따라서

$$
I=c_0^2+4c_1^2\cos^2(2\pi x/P)
+4c_0c_1\cos(2\pi x/P)\cos\delta.
$$

전계는 DC+cos 형태지만, **강도는 단순한 사인파 하나가 아닙니다.** $$\cos^2$$ 때문에 $$2/P$$ 성분도 생깁니다. 디포커스로 $$\cos\delta$$의 크기와 부호가 바뀌면 기본 피치 성분이 약해지거나 반전될 수 있습니다. 기본 성분이 0이 되어도 고조파 강도 변조가 남을 수 있습니다.

### 대칭 경사 조명: 두 차수가 같은 위상을 얻는다

$$f_s=-1/(2P)$$이면 0차와 +1차는 $$-1/(2P),+1/(2P)$$를 통과합니다. 두 주파수의 절댓값이 같으므로 근축 위상과 위의 angular-spectrum 위상 모두 동일합니다. **두 차수만 남는 경우** 디포커스가 공통 위상이 되어 강도에서 사라집니다.

두 빔만 통과하는 기하학적 조건은

$$
\frac{1}{2P}\le\frac{\mathrm{NA}}{\lambda_0}<\frac{3}{2P}.
$$

이는 이상적인 두 평면파 간섭의 초점 불변성입니다. 유한한 광원 폭, 다른 회절항, 비대칭 배치와 수차 등이 추가되면 일반적으로 유지되지 않습니다. 대칭이고 진폭이 같은 두 광원점의 이상적 조명과 실제 폭을 가진 dipole source도 구분해야 합니다.

두 차수의 진폭도 같을 필요가 없습니다. $$D=0.5$$이면 $$c_0=0.5$$, $$c_1=1/\pi$$이므로 Michelson contrast는 약 90.6%이며 100%가 아닙니다.

<figure class="study-figure">
  <a class="figure-zoom" href="{{ '/assets/notes/diffraction-defocus/through-focus.png' | relative_url }}"><img src="{{ '/assets/notes/diffraction-defocus/through-focus.png' | relative_url }}" alt="수직 3-beam과 대칭 경사 2-beam의 근축 through-focus 강도 비교. 수직 조명은 초점에 따라 프로파일이 변하고 이상적인 2-beam은 같은 프로파일을 유지한다." loading="lazy"></a>
  <figcaption>그림 3. 그림 2와 같은 조건의 근축 계산. 위치는 x/P, 디포커스는 실제 µm입니다. 두 맵은 동일한 raw-intensity 색 범위를 사용하고 행별 peak normalization을 하지 않았습니다. 이 그림은 CD/Bossung 곡선이나 측정된 공정 DOF가 아닙니다.</figcaption>
</figure>

## 6. 데모에서 비교할 실험 조건

아래 $$u_s=\lambda_0f_s$$, $$u_0=\lambda_0/P$$는 무차원 값입니다. 파장이 248 nm일 때 $$u_0=0.40$$은 피치 620 nm에 해당합니다.

| 실험 | $$u_s$$ | $$u_0$$ | NA | D | 확인할 점 |
| --- | --- | --- | --- | --- | --- |
| 수직 3-beam | 0 | 0.40 | 0.50 | 0.50 | 0·±1차가 서로 다른 디포커스 위상을 얻음 |
| 대칭 2-beam | −0.20 | 0.40 | 0.50 | 0.50 | 0·+1차의 위상이 같음 |
| 짝수 차수 확인 | 0 | 0.20 | 0.70 | 0.30 | ±2차를 포함한 여러 차수가 통과함 |

주의할 반례는 $$u_s=-0.22$$, $$u_0=0.45$$, $$\mathrm{NA}=0.70$$, $$D=0.50$$인 설정입니다. −1차가 $$u=-0.67$$에 있어 통과하므로 2-beam 예제가 아닙니다. 입사 좌표만 −0.225로 맞춰도 −1차는 여전히 통과합니다. $$u_0=0.45$$를 유지하려면 예를 들어 $$u_s=-0.225$$, $$\mathrm{NA}=0.60$$으로 pupil도 조정해야 합니다.

## 7. 부분결맞음, DOF와 Bossung의 구분

서로 비간섭인 광원점 $$s$$의 가중치 $$w_s$$를 사용하면

$$
I(x,z)=\frac{\sum_s w_s\left|\sum_j A_{s,j}(z)e^{i2\pi jx/P}\right|^2}{\sum_s w_s}.
$$

한 광원점의 회절항은 **전계**로 더하고, 다른 광원점의 기여는 **강도**로 더합니다. 단일 $$f_s$$ 슬라이더만으로는 유한한 source 분포의 부분결맞음이 구현되지 않습니다.

Through-focus intensity map은 $$I(z,x)$$를 보여줍니다. 실제로 DOF를 보고하려면 contrast, 고정 threshold에서의 CD 오차, 또는 다른 허용 기준을 먼저 정하고 정초점을 포함하는 통과 구간을 측정해야 합니다. Bossung은 CD 대 focus 곡선이며 보통 dose 조건별로 비교합니다. intensity map에 붙이는 이름과 같지 않습니다.

전체 한 주기를 샘플링해 contrast를 계산하고, raw intensity를 유지해야 합니다. 각 초점 행을 따로 정규화하면 밝기·dose·threshold 관계를 바꿀 수 있습니다. threshold 기반 contour도 resist 반응이나 웨이퍼 계측을 대체하지 않습니다.

## 8. 계산 구조와 검증 포인트

푸리에 계수, 차수 주파수, aperture와 공간 위상 행렬은 동일한 마스크·광학 조건에서 재사용할 수 있습니다. 현재 초점만 바뀌면 1D 영상과 맵 위의 현재 위치만 갱신하면 되고, 전체 focus sweep을 다시 계산할 이유는 없습니다. pupil에 실제로 들어오는 차수가 빠졌는지, 강도 샘플링이 차수 간 차 주파수까지 표현하는지도 확인합니다.

검증 기준으로는 D=0.5의 짝수항 소멸, 0차만 남을 때 $$I=D^2$$, 대칭 2-beam의 초점 불변성, 단일 초점과 sweep의 같은 행 일치, 비대칭 조명의 source 부호를 사용할 수 있습니다. 계산 시간과 웹 응답 시간은 구분해야 하며, 고정된 1 ms나 60 fps를 모델의 성질로 보장할 수는 없습니다.

현재 페이지의 그림은 재현 가능한 NumPy 계산으로 생성한 정적 예제입니다. 인터랙티브 화면은 [페이지 위쪽의 실행 버튼](#interactive-demo)에서 열 수 있습니다. 데모 기본값은 스칼라 angular-spectrum 위상이며, 이 노트의 정적 그림과 비교하려면 **근축 근사 · 2차 위상**을 선택하세요. 파장·피치는 nm, 디포커스는 µm로 입력하고 조명 위치는 무차원 $$u_s=\lambda_0f_s$$로 조절합니다.

## 관련 노트와 참고자료

* [Fourier Optics · FFT]({{ '/ko/notes/fourier-optics/' | relative_url }}) — 공간주파수, sampling과 intensity bandwidth
* [Abbe Imaging]({{ '/ko/notes/abbe-imaging/' | relative_url }}) — source별 전계와 부분결맞음 강도 합
* [Hopkins · TCC · SOCS]({{ '/ko/notes/foundations/hopkins-tcc-socs/' | relative_url }}) — 동일한 이미징의 다른 계산 구조
* [v0.11 sampling benchmark]({{ '/ko/release-notes/v0.11/' | relative_url }}) — 주기적 패턴 기준과 source·raster 오차의 구분
* [NumPy `sinc` 정의](https://numpy.org/doc/stable/reference/generated/numpy.sinc.html)
* J. W. Goodman, *Introduction to Fourier Optics* — coherent imaging과 공간주파수 필터링의 표준 참고서
