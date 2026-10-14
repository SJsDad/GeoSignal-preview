---
layout: technical
category: research
paper_id: resgnn-opc
title: "ResGNN-OPC — OPC 반복 갱신을 residual graph로 해석하기"
permalink: /ko/notes/research/resgnn-opc/
lang: ko
---

# ResGNN-OPC: OPC 반복 갱신을 residual graph로 해석하기

* 목차
{:toc}

<div class="evidence-note">접근 제한 리뷰. Optica 공식 페이지의 저자·소속·초록·Data Availability·Table 1·Figure 총수 10을 확인했습니다. 본문, 7개 equations, Figure 이미지·caption은 구독 제한으로 열람하지 못했습니다. 아래 GNN 수식은 일반적인 설명 모델이며 논문의 실제 식으로 제시하지 않습니다.</div>

## Paper Information

| 항목 | 확인 내용 |
| --- | --- |
| 정식 제목 | ResGNN-OPC: a fast optical proximity correction approach based on an interpretable residual graph neural network |
| 저자·소속 | Jingqing Liu, Xu Ma. School of Optics and Photonics, Beijing Institute of Technology; Key Laboratory of Photoelectronic Imaging Technology and System |
| 발표 | Applied Optics 64(15), 4227–4234, 2025 |
| 원문 | [DOI](https://doi.org/10.1364/AO.561432) · [공식 article](https://opg.optica.org/ao/abstract.cfm?uri=ao-64-15-4227) · [PDF entry](https://opg.optica.org/ao/viewmedia.cfm?uri=ao-64-15-4227&seq=0) |
| 데이터 | 공식 Data Availability: 비공개이며 합리적인 요청으로 저자에게 얻을 수 있음 |
| 코드·weights | 공식 공개 repository·pretrained weights 미확인 |
| 분야 | OPC correction prediction, residual graph neural network |

## Executive Summary

**한 문장:** graph convolution에 residual update를 넣어 MBOPC의 반복 보정과 비슷한 단계별 구조를 갖춘 correction predictor입니다.

Raster mask 전체를 생성하는 것보다 기존 edge/control-point 구조에 보정량을 주는 모델이 OPC flow에 자연스럽게 연결될 수 있습니다. residual connection은 초기 feature를 다음 layer까지 전달하면서 learned increment를 더합니다. 논문의 interpretability는 이러한 구조적 유사성에서 출발합니다.

하지만 “layer가 OPC iteration과 닮았다”는 것과 “각 layer가 물리적으로 같은 update를 한다”는 것은 다릅니다. 본문을 확보하지 못해 graph feature·supervision·정확한 loss를 확인하지 못했습니다.

## Background & Motivation

MBOPC는 contour를 계산하고 edge displacement를 갱신하는 과정을 반복합니다. mask segment마다 주변 geometry의 영향이 다르므로 flat image와 다른 graph representation이 유용할 수 있습니다. 이웃 edge 사이의 dependency를 sparse graph로 표현하면 전체 pixel image보다 구조를 직접 학습할 여지가 있습니다.

일반적인 GNN은 node feature를 이웃 aggregation으로 갱신합니다. layer 수를 늘리면 더 먼 node의 정보가 전달되지만 over-smoothing·training difficulty가 생길 수 있습니다. residual update는 깊은 layer에서 feature와 gradient를 보존하는 데 도움을 줄 수 있습니다. 이 장점이 실제 optical range를 올바르게 표현하는지는 graph construction에 달려 있습니다.

## Physics & Mathematical Foundations

### MBOPC update와 residual GNN의 연결 — 독자적 예시

Edge position $$u^{(t)}$$ [nm], contour mismatch $$e^{(t)}$$ [nm]를 사용한 일반 update는

$$
u^{(t+1)}=u^{(t)}+\Delta u^{(t)},\qquad \Delta u^{(t)}=F(e^{(t)},\text{local geometry},p).
$$

GNN의 설명용 residual 식은

$$
h_i^{(\ell+1)}=h_i^{(\ell)}+\psi_\ell\left(h_i^{(\ell)},\operatorname{AGG}_{j\in\mathcal N(i)}\phi_\ell(h_i^{(\ell)},h_j^{(\ell)},a_{ij})\right).
$$

$$h_i$$는 node embedding, $$a_{ij}$$는 edge feature, $$\mathcal N(i)$$는 graph neighbors, AGG는 sum/mean 등 permutation-invariant aggregation입니다. embedding은 일반적으로 무차원이며 final output projection이 movement 단위로 변환합니다. 위 $$φ,ψ$$·AGG·edge feature는 설명용 변수이며 ResGNN-OPC의 검증된 구현 정의가 아닙니다.

개념적 shape는 node 수 $$N$$, feature 수 $$C$$일 때 $$H\in\mathbb R^{N\times C}$$, graph connectivity는 sparse adjacency입니다. segment 위치·길이·normal·proximity가 어떤 방식으로 feature에 들어가는지는 본문 확인 전까지 미확인입니다.

### Optical interaction range와 graph depth

$$L$$ layers는 $$L$$-hop neighborhood를 볼 수 있습니다. 그러나 한 hop의 물리 거리는 graph 생성 정책에 의해 결정됩니다. 연결이 layout distance에 기반하는지 optical interaction 또는 polygon 관계에 기반하는지 확인해야 합니다. graph depth 숫자만으로 coherent diffraction support를 추정할 수 없습니다.

[Abbe]({{ '/ko/notes/abbe-imaging/' | relative_url }})의 nonlocal imaging과 graph neighborhood를 연결할 때, 직접 파동 연산을 수행하는지 geometry correlation을 학습하는지 구분합니다. 현재 공개 초록은 residual 구조의 MBOPC iteration 유사성을 설명하며 exact optical kernel을 GNN layer에 넣었다는 근거는 제공하지 않습니다.

## Proposed Method / Model Architecture

공식 초록은 residual structure를 graph convolution layer에 통합해 network depth와 correction fitting을 개선한다고 설명합니다. 최종 correction을 출력한 뒤 후속 MBOPC iteration을 줄이는 목적입니다.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/resgnn-opc.svg' | relative_url }}"><img src="{{ '/assets/notes/research/resgnn-opc.svg' | relative_url }}" alt="독자 제작: graph 이웃 aggregation과 residual increment의 일반 개념" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">확대 보기 ↗</span></a>
<figcaption>일반 residual GNN의 설명용 도식. 논문의 graph 정의·실제 module 배치·Figure를 재구성했다고 주장하지 않습니다.</figcaption>
</figure>

Layer 수, feature count, activation, loss, target correction label의 생성법, graph normalization, training split, hardware를 확인하지 못했습니다. “end-to-end differentiable optical simulation을 loss에 사용한다” 또는 “PINN residual이 있다”는 설명도 확인되지 않았습니다.

**Physics-Informed/Guided 판별:** 공개 범위에서 확인 가능한 것은 iteration-inspired network topology입니다. physical equations가 입력·layer·loss·optimizer에 강제되는 정확한 위치는 미확인입니다. interpretable이라는 제목을 physics-enforced라는 뜻으로 바꾸지 않습니다.

## Figures & Visual Explanation

{% include figure-coverage.html %}

공식 Figures 탭의 총수 10에 맞춰 Fig. 1–10 원문 접근 링크를 기록했습니다. caption·subfigure·axis·color·loss curve 여부는 열람하지 못했으므로 별도 그림 설명을 지어 넣지 않습니다. 본문 접근 확보 전에는 **0/10개 상세 그림 해설 완료**입니다. Table 1은 공식 페이지에서 숫자를 확인할 수 있어 아래에서 해석합니다.

## Experiments & Results

아래 표는 공식 Table 1, 전체 test layout의 average입니다. wavelength·NA·source·layout 수·hardware는 공개 페이지에서 확인하지 못했습니다.

| Method | Correction prediction error [nm] | Runtime [s] | Initial EPE [nm] | Corrected EPE [nm] |
| --- | ---: | ---: | ---: | ---: |
| Conventional MBOPC | — | 17.6299 | 7.21 | 2.43 |
| RGCN-OPC | 2.17 | 0.0022 | 7.21 | 4.33 |
| ResGNN-OPC | 1.27 | 0.0029 | 7.21 | 3.02 |

**독자 계산:** $$(2.17-1.27)/2.17\approx41.5\%$$ prediction-error 감소, $$17.6299/0.0029\approx6079$$ runtime ratio입니다. 후속 refinement 포함 여부·학습 비용·graph construction 비용은 표만으로 확정할 수 없습니다.

중요한 해석은 accuracy–runtime trade-off입니다. ResGNN은 RGCN보다 correction을 정확히 예측하지만 runtime은 약간 더 큽니다. 최종 EPE 3.02 nm는 MBOPC 2.43 nm보다 높습니다. 따라서 “6000× 빠르면서 모든 최종 EPE가 동일하다”는 서술은 맞지 않습니다. 후속 iteration 감소 주장은 초록에서 확인되지만 조건별 iteration count는 본문에서 확인해야 합니다.

Correction prediction error와 printed-contour EPE는 서로 다른 target을 평가합니다. movement label과 가까워도 optical response의 비선형성 때문에 같은 contour error를 보장하지 않습니다. [Metrics]({{ '/ko/notes/foundations/inverse-and-metrics/' | relative_url }}) 참조.

## Critical Analysis & Limitations

**기술적 기여의 해석:** vector/edge workflow에 익숙한 OPC engineer에게 residual update는 해석 가능한 interface를 제공합니다. **현재 확인한 한계:** 데이터 비공개, 공정 조건 미확인, full graph feature·loss·Figure 미확인입니다.

Graph representation은 polygon 수·segment 길이·control-point placement에 민감할 수 있습니다. 같은 physical shape를 다르게 분할하면 node 수가 달라지고 aggregation weight가 바뀔 수 있습니다. segmentation-invariance 또는 재분할 robustness를 확인해야 합니다.

Residual architecture를 썼다고 convergence·monotonic EPE improvement가 보장되지는 않습니다. 잘못된 correction이 누적될 수 있고 node 간 update가 mask rule violation을 만들 수도 있습니다. final optical verification과 movement bound·MRC가 필요합니다. 저자 numerical experiment를 wafer 실험으로 확대 해석하지 않습니다.

## Practical Applications to GeoSignal / OPC

* **당장 적용 가능한 아이디어:** geometry candidates와 contour gauges를 edge identity에 연결하는 데이터 설계를 검토합니다. 현재 GeoSignal은 자동 edge correction을 지원하지 않습니다.
* **추가 연구 / Hypothesis:** 공개 synthetic layout에서 MBOPC label을 생성할 solver를 먼저 구성하고, initial prediction 및 refinement 후 EPE·total runtime을 별도로 비교합니다.
* **장기 / Hypothesis:** graph update에 optical sensitivities와 process-window constraints를 포함합니다. exact gradient가 없는 correction predictor와 differentiable imaging을 조합할 때 stability를 재검증합니다.

## Key Takeaways & References

1. GNN은 geometry dependency를 node/edge로 표현합니다.
2. Residual increment와 실제 MBOPC update의 동등성은 별도 검증 문제입니다.
3. Table 1의 runtime ratio와 최종 contour EPE를 함께 읽습니다.
4. Correction error와 EPE는 같은 지표가 아닙니다.
5. 비공개 데이터에서의 결과를 공개 benchmark 순위로 바꾸지 않습니다.

[GeoSignal 적용 범위]({{ '/ko/notes/research/geosignal-scope/' | relative_url }}) · [TokMan]({{ '/ko/notes/research/tokman/' | relative_url }}) · [Inverse Problem]({{ '/ko/notes/foundations/inverse-and-metrics/' | relative_url }})
