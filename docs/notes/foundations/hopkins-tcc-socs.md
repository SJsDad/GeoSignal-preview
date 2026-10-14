---
layout: technical
category: foundations
title: Hopkins · TCC · SOCS
permalink: /ko/notes/foundations/hopkins-tcc-socs/
lang: ko
---

# Hopkins · TCC · SOCS

* 목차
{:toc}

## 직관: 광학계를 먼저 계산하고 mask를 바꾸기

[Abbe]({{ '/ko/notes/abbe-imaging/' | relative_url }})에서는 source point별 전계를 합성합니다. Hopkins는 이 식을 전개해 source와 pupil의 정보를 TCC(Transmission Cross-Coefficient)에 모읍니다. 동일한 공정 조건에서 많은 mask를 계산할 때 광학 정보를 재사용하기 유리합니다.

## Abbe에서 TCC로

연속 source의 정규화 weight density를 $$S(\mathbf s)$$로 두고 전계를 Fourier 형태로 쓰면

$$
I(\mathbf x)=\int S(\mathbf s)\left|\int\widehat m(\mathbf f)P(\mathbf f-\mathbf s)e^{i2\pi\mathbf f\cdot\mathbf x}d\mathbf f\right|^2d\mathbf s.
$$

절댓값 제곱을 원래 적분과 complex conjugate 적분의 곱으로 펼칩니다. 적분 순서를 바꾸면

$$
T(\mathbf f,\mathbf g)=\int S(\mathbf s)P(\mathbf f-\mathbf s)P^*(\mathbf g-\mathbf s)d\mathbf s,
$$

$$
I(\mathbf x)=\iint T(\mathbf f,\mathbf g)\widehat m(\mathbf f)\widehat m^*(\mathbf g)e^{i2\pi(\mathbf f-\mathbf g)\cdot\mathbf x}d\mathbf f d\mathbf g.
$$

$$T$$는 mask와 무관하지만 source·pupil·focus에 의존합니다. $$\mathbf f,\mathbf g,\mathbf s$$ 단위는 µm⁻¹, $$S$$는 적분해서 1이 되도록 정규화합니다. $$T$$는 이 정규화에서 무차원이고 intensity의 normalization은 Fourier convention을 따릅니다. 별도 mask 3D scattering이 있으면 이 단순 분리는 적용 범위를 다시 확인해야 합니다.

## Hermitian·positive semidefinite인 이유

source를 이산화하고 $$A_{k,f}=\sqrt{w_k}P_k^*(f)$$로 정의하면 $$T=A^\dagger A$$입니다. 따라서 $$T_{g,f}=T_{f,g}^*$$, $$u^\dagger Tu=\|Au\|^2\ge0$$입니다. 모든 eigenvalue가 음이 아니지만 zero eigenvalue가 있을 수 있으므로 일반적으로 positive **semidefinite**라고 표현합니다.

## SOCS의 유도와 계산 흐름

$$
T=\sum_j\lambda_j q_jq_j^\dagger,\qquad
I(\mathbf x)=\sum_j\lambda_j\left|\mathcal F^{-1}[q_j\widehat m](\mathbf x)\right|^2.
$$

$$\lambda_j\ge0$$, $$q_j$$는 orthonormal mode입니다. $$K_j=\sqrt{\lambda_j}q_j$$로 eigenvalue를 kernel에 흡수하면 $$I=\sum_j|\mathcal F^{-1}[K_j\widehat m]|^2$$입니다. Nitho를 읽을 때 eigenvalue가 수식에서 사라졌다고 intensity weight가 없다고 해석하면 안 됩니다. SOCS mode는 source의 coherent eigenmode이며 실제 illumination source point와 일대일 대응하지 않을 수 있습니다.

소규모 grid의 dense TCC는 frequency pixel 수를 $$F$$라 하면 $$F\times F$$ 복소 matrix입니다. 큰 ROI에서 이를 직접 저장하기보다 source-pupil factor에 SVD를 적용하는 경로가 유리할 수 있습니다. GeoSignal의 exact 경로도 source factor를 활용하며 full-rank cross-validation과 truncation 실험을 구분합니다.

## Truncation error가 말해주는 것

$$\lambda_1\ge\lambda_2\ge\cdots$$에서 첫 $$r$$개만 남기면 scalar model 내부에서는 누락한 항이 nonnegative이므로 $$I_r\le I_{full}$$입니다. 하지만 작은 평균 intensity 오차가 작은 EPE를 보장하지 않습니다. threshold 부근 intensity slope가 작으면

$$
\delta x\simeq -\frac{\delta I}{\partial I/\partial n}.
$$

분자는 무차원 intensity 오차, 분모는 intensity/µm, 따라서 $$\delta x$$는 µm입니다. 이는 local linearization이며 bridging·pinching으로 contour topology가 바뀌는 곳에서는 적용하기 어렵습니다. optical energy retention만으로 rank를 선택하기보다 CD·EPE·process-window 오차를 함께 제한해야 합니다.

## 학습 kernel을 사용할 때

고정 optical condition에서 kernel을 학습한다는 것은 mask distribution보다 광학계를 식별하려는 접근입니다. 그러나 intensity만 보면 $$K_j$$에 global phase를 곱하거나 mode를 unitary mixing해도 같은 intensity가 나옵니다. kernel의 비유일성을 고려하고 aerial·contour prediction을 검증해야 합니다. 새로운 source나 focus에 대한 보장은 해당 조건을 입력하거나 다시 kernel을 학습한 경우에만 주장할 수 있습니다.

## 관련 리뷰와 참고자료

* [Nitho]({{ '/ko/notes/research/nitho/' | relative_url }})
* [DOINN]({{ '/ko/notes/research/doinn/' | relative_url }})
* [Nitho 원문, Section II](https://arxiv.org/html/2303.08435v4)
* [DOINN 원문, Section 2](https://arxiv.org/html/2203.08616v1)
