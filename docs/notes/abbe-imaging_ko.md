---
layout: technical
category: foundations
title: Abbe Imaging
description: GeoSignal Preview의 Abbe imaging 기술 노트
permalink: /ko/notes/abbe-imaging/
lang: ko
---

<p class="language-switch"><a href="{{ '/notes/abbe-imaging/' | relative_url }}" lang="en">View in English</a></p>

# Abbe Imaging

이 기술 노트는 향후 필요할 때 내용을 추가하기 위해 마련해 둔 페이지입니다.

---

## 관련 페이지

* [기술 노트로 돌아가기]({{ '/ko/notes/' | relative_url }})
* [방법론]({{ '/ko/method/' | relative_url }})
* [데모]({{ '/ko/demo/' | relative_url }})


## 학습 확장: 전계와 intensity를 구분하기

한 source point의 빛은 mask에서 회절한 서로 다른 주파수 성분끼리 간섭합니다. 따라서 전계 $$E$$를 먼저 합성하고, 그 다음 $$|E|^2$$를 계산합니다. 서로 비간섭인 source point끼리는 intensity를 더합니다. 이 순서를 바꾸면 다른 물리 모델이 됩니다.

* 목차
{:toc}

## Pupil과 source sampling

Wafer 기준 좌표를 $$\mathbf{x}=(x,y)$$ [µm], 공간 주파수를 $$\mathbf{f}=(f_x,f_y)$$ [µm⁻¹]로 둡니다. $$m(\mathbf{x})$$는 무차원 복소 amplitude transmittance이며 binary mask에서는 0 또는 1입니다. $$P$$는 pupil, $$s_k$$는 source 주파수 좌표, $$w_k\ge0$$는 source intensity weight입니다.

$$
E_k(\mathbf{x};z)=\mathcal{F}^{-1}\{\widehat m(\mathbf f)P_z(\mathbf f-\mathbf s_k)\},\qquad
I(\mathbf{x};z)=\frac{\sum_k w_k|E_k(\mathbf{x};z)|^2}{\sum_k w_k}.
$$

입사 기울기에 따른 carrier를 전계에서 분리하면 shifted pupil 형태로 쓸 수 있습니다. 부호는 Fourier transform과 source 방향 정의에 따라 달라질 수 있으므로 실제 코드와 맞춰야 합니다. GeoSignal `abbe.py`는 한 번 계산한 mask FFT에 source별 shifted pupil을 곱하고 IFFT·절댓값 제곱·weight 누적을 수행합니다. clear-field-relative intensity를 유지하려면 ROI별 peak normalization을 추가하지 않습니다.

이상적인 circular pupil은 다음과 같습니다.

$$
P_0(\mathbf f)=\mathbf 1_{\|\mathbf f\|\le f_c},\qquad f_c=\frac{\mathrm{NA}}{\lambda}.
$$

NA는 무차원, $$\lambda$$는 µm이며 따라서 $$f_c$$ 단위는 µm⁻¹입니다. conventional source 반경은 $$\sigma f_c$$이고 $$\sigma$$도 무차원입니다. 선폭 자체를 frequency cutoff와 혼동하면 안 됩니다. pupil은 전계에 적용되고 intensity는 전계의 이차식입니다.

## Partial coherence의 유도

$$E=\sum_k a_kE_k$$일 때 $$|E|^2$$에는 교차항 $$a_ka_l^*E_kE_l^*$$가 있습니다. 서로 독립인 source의 시간 평균에서 $$\langle a_ka_l^*\rangle=0$$ ($$k\ne l$$), $$\langle |a_k|^2\rangle=w_k$$이므로 위 weighted intensity sum이 나옵니다. 이는 한 source에서 mask 회절 성분이 비간섭이라는 뜻이 아닙니다.

예를 들어 두 coherent field가 각각 1과 −1이면 전계 합의 intensity는 0입니다. 두 source가 mutually incoherent하고 같은 weight이면 intensity 평균은 1입니다. ML 모델이 위상을 버리고 amplitude magnitude만 입력하면 이 차이를 학습 구조에서 보존하기 어렵습니다.

## Defocus와 contour

시간 의존성을 $$e^{-i\omega t}$$로 잡은 paraxial propagation에서는 global phase를 제외하고 다음 위상으로 표현할 수 있습니다.

$$
P_z(\mathbf f)=P_0(\mathbf f)\exp[-i\pi\lambda z\|\mathbf f\|^2].
$$

$$z$$는 µm, 지수는 무차원입니다. 이는 homogeneous-medium paraxial 예시이며 실제 고 NA·immersion·vector model의 정확한 defocus 식을 대신하지 않습니다. focus sign convention은 코드의 pupil 정의를 따릅니다.

상대 dose $$d$$가 raw intensity에 곱해질 때 고정 threshold $$T_0$$의 contour는 $$dI\ge T_0$$, 즉 $$I\ge T_0/d$$입니다. dose마다 peak normalize하면 dose-to-size 관계가 바뀝니다. threshold contour는 resist 화학·etch 모델의 대체물이 아닙니다.

## 계산·검증에서 중요한 연결점

source sampling 개수·ROI halo·pixel size·FFT padding을 함께 바꿔 convergence를 확인합니다. source 개수 증가가 항상 contour 정확도를 보장하지는 않습니다. intensity 차이뿐 아니라 fixed transect CD와 edge displacement도 봐야 합니다. [Hopkins/TCC/SOCS]({{ '/ko/notes/foundations/hopkins-tcc-socs/' | relative_url }})는 동일한 물리를 mask-independent 모드로 다시 표현합니다.

LMLitho의 source conditioning은 이러한 광원 의존성을 학습 입력으로 다룹니다. Nitho는 mask-independent kernels를 학습합니다. OptiCo는 전파 위상을 convolution의 inductive bias로 넣습니다. 각 방법의 입력과 물리 제약은 같지 않습니다.

## 추가 참고자료

* [회절 차수와 디포커스: 경사 조명의 이미징 원리]({{ '/ko/notes/diffraction-defocus/' | relative_url }}) — 3-beam과 대칭 2-beam 예제를 비교합니다.
* [Fourier Optics]({{ '/ko/notes/fourier-optics/' | relative_url }})
* [Nitho 원문, Section II](https://arxiv.org/html/2303.08435v4)
* [LMLitho 리뷰]({{ '/ko/notes/research/lmlitho/' | relative_url }})
