---
layout: technical
category: foundations
title: Inverse Problem · Gradient · Metrics
permalink: /ko/notes/foundations/inverse-and-metrics/
lang: ko
---

# Inverse Problem · Gradient · Metrics

* 목차
{:toc}

## Forward와 inverse의 구분

Forward는 mask $$M$$·광학 조건 $$p$$를 주고 $$I$$ 또는 resist/contour $$R$$을 구합니다. Inverse는 target $$T$$를 잘 인쇄할 $$M$$을 찾습니다. 빠른 forward simulator가 좋은 inverse optimizer가 되려면 예측값뿐 아니라 mask에 대한 gradient도 유용해야 합니다.

$$
\min_{M\in\mathcal C}\mathcal L(g(M;p),T)+\beta\Omega(M).
$$

$$g$$는 simulator, $$\mathcal C$$는 binary·Manhattan·mask rule 같은 feasible set, $$\Omega$$는 정규화, $$\beta$$는 weight입니다. CNN·VAE·diffusion은 inverse 초기 mask를 제안할 수 있고, GNN은 edge displacement를 직접 예측할 수 있습니다. 목적과 제약이 다르면 동일한 성능 표로 묶지 않습니다.

## Differentiable simulation과 gradient

$$
M_{t+1}=\Pi_{\mathcal C}\left(M_t-\eta\left[\left(\frac{\partial g}{\partial M}\right)^\top\frac{\partial\mathcal L}{\partial g}+\beta\nabla_M\Omega\right]\right).
$$

$$\eta$$는 step size, $$\Pi$$는 projection입니다. Binary projection은 불연속이므로 실제 학습은 sigmoid relaxation·straight-through estimator·geometry parameterization 등을 사용할 수 있습니다. hard threshold의 도함수를 자동미분할 수 있다는 것과 의미 있는 gradient가 나온다는 것은 다릅니다.

SOCS field $$E_j=H_jM$$에 대해 $$\delta I=2\operatorname{Re}\sum_jE_j^*H_j\delta M$$입니다. 실제 구현은 FFT의 adjoint·complex conjugate·normalization을 맞춰야 합니다. surrogate에 low pixel error가 있어도 $$\partial g/\partial M$$가 틀리면 optimizer가 surrogate의 오류를 악용할 수 있습니다. 최종 mask는 별도 reference engine으로 재평가합니다.

## 이미지 지표와 단위

$$
\mathrm{MSE}=\frac1N\sum_p(\widehat I_p-I_p)^2,\qquad
L_{2,\mathrm{sum}}=\sum_p(R_p-T_p)^2.
$$

MSE는 intensity 단위의 제곱, 정규화 intensity라면 무차원입니다. binary $$R,T$$에서 $$L_{2,\mathrm{sum}}$$은 XOR pixel count와 같습니다. pixel 면적 $$a_{px}$$를 곱해야 면적 [nm²]이 됩니다. 논문이 합을 MSE나 L2로 표기하기도 하므로 이름보다 normalization을 먼저 확인합니다.

$$
\operatorname{IoU}=\frac{|R\cap T|}{|R\cup T|}.
$$

IoU는 무차원입니다. foreground IoU, foreground/background class mean, image mean은 서로 다릅니다. mPA도 논문에 따라 전체 pixel accuracy 또는 class recall mean을 의미합니다. background가 많은 layout에서는 pixel accuracy가 높아도 중요한 edge가 틀릴 수 있습니다.

## EPE와 CD

Target edge의 merit point $$x_i$$와 normal $$n_i$$를 정하고 printed contour 교차점을 $$y_i$$라 하면 signed EPE 예시는 $$e_i=(y_i-x_i)\cdot n_i$$ [nm]입니다. 평균 절댓값 EPE는 $$N^{-1}\sum_i|e_i|$$, violation count는 $$\sum_i\mathbf1_{|e_i|>\tau}$$입니다. count와 nm 수치를 같은 열에서 비교하지 않습니다.

교차 contour가 없는 point, 여러 교차가 있는 point, corner normal은 지표 구현에서 정의해야 합니다. CD는 같은 transect의 두 contour intersection 사이 거리입니다. 양쪽 edge error가 같은 방향이면 CD는 맞아도 pattern이 이동할 수 있으므로 CD와 EPE는 보완적입니다.

## Process Variation Band와 process window

$$
\mathrm{PVB}_{area}=a_{px}\sum_p\left[\max_{c\in\mathcal P}R_c(p)-\min_{c\in\mathcal P}R_c(p)\right].
$$

$$c$$는 focus/dose condition, $$\mathcal P$$는 평가 corner 집합입니다. binary contour들의 union과 intersection 사이 면적입니다. 두 ordered corner일 때 XOR band와 대응할 수 있지만 여러 condition 또는 topology 변화에서는 극값 정의를 명시해야 합니다. soft-image MSE 기반 PVB loss와 최종 binary PVB 면적은 같지 않습니다.

DoF는 특정 CD/EPE spec과 dose 조건에서 허용되는 focus 범위입니다. Bossung curve는 focus에 따른 CD를 dose별로 보여줍니다. process window는 spec을 만족하는 focus/dose 영역입니다. PVB가 작아도 모든 contour가 target에서 함께 벗어나면 좋은 공정 창이라고 할 수 없습니다.

## Runtime·shot·일반화 비교

Runtime은 inference, ILT refinement, source/TCC setup, CPU↔GPU transfer, I/O, 학습 비용을 나눠 봅니다. mask shot count는 지정된 fracturing algorithm의 rectangle 수이며 실제 multi-beam write-time과 일대일 대응하지 않습니다.

OOD shape test와 새 공정으로의 transfer는 구분합니다. 동일 NA·source에서 via→metal을 잘 예측한다고 새 scanner·resist·focus/dose를 검증한 것은 아닙니다. 새로운 공정 데이터로 fine-tune한 결과는 zero-shot generalization으로 표기하지 않습니다.

## 관련 자료

* [Research Overview]({{ '/ko/notes/research/' | relative_url }})
* [LithoBench 공식 코드](https://github.com/shelljane/lithobench)
* [LithoSim 공식 프로젝트](https://dw-hongquan.github.io/LithoSim/)
