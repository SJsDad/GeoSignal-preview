---
layout: technical
category: research
paper_id: tokman
title: "TokMan — Manhattan 형상을 유지하는 token 기반 inverse 설계"
permalink: /ko/notes/research/tokman/
lang: ko
---

# TokMan: Manhattan 형상을 유지하는 token 기반 inverse 설계

* 목차
{:toc}

<div class="evidence-note">부분 리뷰. NeurIPS 공식 서지·초록과 공식 PDF 색인 본문의 Sections 4–5, Table 1, Figures 1–6 관련 설명을 확인했습니다. 직접 PDF는 약 15.5 MB로 열람 도구의 크기 제한에 걸렸고 Supplemental ZIP은 파싱하지 못했습니다. 전체 Figure·subfigure·시각적 세부·Appendix는 완전 검증 전입니다.</div>

## Paper Information

| 항목 | 확인 내용 |
| --- | --- |
| 정식 제목 | TokMan:Tokenize Manhattan Mask Optimization for Inverse Lithography |
| 저자 | Yiwen Wu, Yuyang Chen, Ye Xia, Yao Zhao, Jingya Wang, Xuming He, Hao Geng, Jingyi Yu |
| 소속 | ShanghaiTech University 관련 저자 발표목록과 PDF 첫 페이지 일부 확인; 전체 소속 매핑은 미확인 |
| 발표 | Advances in Neural Information Processing Systems 38, NeurIPS 2025 |
| 원문 | [공식 페이지](https://proceedings.nips.cc/paper_files/paper/2025/hash/4e127d4fb92a3145ecb60f6aa0b16eef-Abstract-Conference.html) · [DOI](https://doi.org/10.52202/085713-1807) · [PDF](https://proceedings.nips.cc/paper_files/paper/2025/file/4e127d4fb92a3145ecb60f6aa0b16eef-Paper-Conference.pdf) |
| 보충자료 | [Supplemental ZIP](https://proceedings.nips.cc/paper_files/paper/2025/file/4e127d4fb92a3145ecb60f6aa0b16eef-Supplemental-Conference.zip), 내용 미확인 |
| 코드·데이터·weights | 공식 공개 저장소·checkpoint 미확인; layout 기반 self-supervised dataset 구성은 Section 5.1에서 확인 |
| 분야 | Manhattan-constrained ILT / mask generation |

## Executive Summary

**한 문장:** mask 픽셀 대신 axis-aligned boundary point와 correction sequence를 모델링하고, differentiable lithographic feedback으로 Transformer를 학습합니다.

Pixel-space ILT의 좋은 relaxed 해는 binarization 이후 shape가 깨질 수 있습니다. TokMan은 표현 공간을 Manhattan geometry에 맞춰 설계합니다. 학습할 변수는 image의 모든 픽셀보다 edge correction 쪽에 가깝습니다. diffusion은 이 correction sequence의 생성 과정에 사용합니다.

실무적 가치는 contour fidelity와 mask representation을 함께 다루는 데 있습니다. 다만 Manhattan compliance만으로 minimum width·space·notch·shot policy 등 전체 manufacturing rule이 충족된다고 결론내리지 않습니다.

## Background & Motivation

Continuous intensity loss만 최소화하면 curvilinear island나 작은 artifact가 생길 수 있습니다. target의 optical fidelity를 높이는 것과 write-friendly binary mask를 만드는 것은 다른 목적입니다. polygon/edge parameterization은 처음부터 horizontal/vertical 구조를 유지할 수 있지만, 표현이 허용하지 않는 topology나 신규 assist feature의 생성을 제한할 수 있습니다.

CNN은 raster pattern 생성에 자연스럽고 FNO는 frequency relation에 유리합니다. Transformer는 point/polygon sequence 사이의 문맥을 다루기 편합니다. 이는 서로를 대체하는 단일 세대 발전이 아니라 output representation의 차이에 맞춘 설계입니다.

## Physics & Mathematical Foundations

### Point displacement에서 mask까지 — 독자적 연산 설명

입력 point 좌표를 $$X\in\mathbb R^{N\times2}$$, scalar correction을 $$\delta\in\mathbb R^N$$로 둡니다. 각 point의 허용 이동 방향 $$n_i$$에 대해

$$
x'_i=x_i+\delta_i n_i,\qquad M=\mathcal R(X'),\qquad R=g(M).
$$

$$x_i,\delta_i$$는 pixel index 또는 nm로 정의할 수 있으며 두 단위를 혼용하지 않습니다. $$n_i$$는 무차원 axis direction, $$\mathcal R$$는 rasterizer입니다. 원문의 scalar axis correction을 이해하기 위한 일반 표현으로, point별 normal sign·constraint handling은 본문 전체가 없어 확정하지 않습니다.

$$
\frac{\partial\mathcal L}{\partial\delta}=\left(\frac{\partial X'}{\partial\delta}\right)^T
\left(\frac{\partial M}{\partial X'}\right)^T
\left(\frac{\partial g}{\partial M}\right)^T\frac{\partial\mathcal L}{\partial R}.
$$

gradient는 simulator뿐 아니라 rasterizer를 지나야 합니다. 이 chain이 없으면 image-space loss가 geometry correction을 학습시키기 어렵습니다. Section 4/Figure 2는 nvdiffrast를 사용한 렌더링·simulation feedback을 설명합니다. Anti-aliasing·binary projection의 정확한 처리는 미확인입니다.

### Diffusion Transformer — 일반 개념과 주의점

표준 Gaussian diffusion의 예시식은 $$z_t=\sqrt{\bar\alpha_t}z_0+\sqrt{1-\bar\alpha_t}\epsilon$$입니다. $$t$$는 물리적 노광 시간이 아니라 noise level이며 Transformer는 조건부 token sequence에서 denoising update를 예측합니다.

**이 표준식은 TokMan의 확인된 forward process가 아닙니다.** lithographic distortion을 구조적 noise에 비유했다고 해서 광학 전파가 Gaussian Markov process라고 가정할 수 없습니다. 정확한 noise schedule·prediction target·sampling step 수는 원문 전체 확인 전까지 보류합니다.

Point-wise position은 같은 polygon 내 순서를, polygon-wise position은 형상 간 context를 제공합니다. 두 embedding을 모두 사용하면 같은 좌표 근처의 서로 다른 polygon을 구별할 수 있지만 permutation·rotation·reflection robustness는 별도 평가가 필요합니다.

## Proposed Method / Model Architecture

Section 4.1은 corner split, 인접 parallel edge의 spatial alignment, 긴 segment의 partition을 설명합니다. Section 4.2·Figure 3은 point/polygon positional embedding과 denoising Transformer로 scalar correction을 예측하는 구조입니다. Section 4.3은 후속 ILT refinement로 local fidelity를 높입니다.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/tokman.svg' | relative_url }}"><img src="{{ '/assets/notes/research/tokman.svg' | relative_url }}" alt="독자 제작: TokMan의 segmentation, point correction, rasterization, lithography feedback" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">확대 보기 ↗</span></a>
<figcaption>독자 제작 데이터 흐름도. 원본 Figure 2·3의 복제물이 아닙니다. geometry token과 image pixel을 분리해 표시합니다.</figcaption>
</figure>

색인 Section 5.1은 6 Transformer blocks, embedding dimension 512, attention heads 16을 명시합니다. **Physics-Guided 위치:** geometry segmentation의 lithographic influence prior, differentiable simulation을 통한 self-supervised loss, inference 후 ILT refinement입니다. Transformer 내부가 exact diffraction operator인 것은 아닙니다.

Ground-truth corrected mask 없이 target layout과 simulated wafer mismatch로 학습할 수 있다는 점이 핵심입니다. 하지만 정확한 전체 loss weight와 diffusion supervision 구성이 확인되지 않아 일반 DDPM noise loss를 논문의 식처럼 제시하지 않습니다.

## Figures & Visual Explanation

{% include figure-coverage.html %}

색인으로 확인된 최소 6개 Figure를 기록했습니다. 그림 원본·전체 Supplementary를 검토하지 못했으므로 색상·subfigure 누락 가능성을 남깁니다. Figure 6의 axis는 feature dimension·head 수·decoder layer 수이며 숫자와 confidence interval을 직접 추출하지 않습니다.

## Experiments & Results

색인 Section 5.1: 89,697 training layouts, ICCAD13-S/L 평가, 1 nm/pixel, wavelength 193 nm, defocus ±30 nm, dose ±3%, threshold 0.225, sigmoid steepness 50. 학습 platform은 32 H20, test는 1 A100이며 batch 40에서 약 80 GB memory를 언급합니다. 이는 card별/전체 memory의 명확한 구분을 직접 확인하지 못했으므로 단정하지 않습니다. NA·validation 분리·sampling schedule은 미확인입니다.

| Table 1 · 조건 | Method | Mean EPE | Mean shots | TAT 표기값 |
| --- | --- | ---: | ---: | ---: |
| ICCAD13-S | IL-ILT | 2.70 | 4948.4 | 2.87 |
| ICCAD13-S | TokMan | 2.16 | 287.6 | 0.89 |
| ICCAD13-L | IL-ILT | 1.80 | 7916.4 | 2.92 |
| ICCAD13-L | TokMan | 1.38 | 642.3 | 1.57 |

Section 5의 EPE는 boundary merit-point distance의 평균이며 violation count가 아닙니다. 1 nm/pixel 설정이지만 원문 표 caption의 단위 표시·TAT 시간 단위를 PDF 시각 확인하지 못해 위 열은 원문 표기값으로 유지합니다. TAT 정의는 TokMan inference+postprocessing, baseline은 method별 fixed iteration 또는 inference이며 I/O를 제외합니다. 서로 다른 benchmark 조건의 OptiCo EPE와 직접 순위를 비교할 수 없습니다.

ICCAD13-L에서는 Multi-ILT TAT 표기값 1.33이 TokMan 1.57보다 작습니다. **모든 조건에서 최단 runtime이라고 쓰지 않습니다.** 실제 mask write time은 shots라는 간접 지표와 달라 별도 mask writer/fracturing 조건이 필요합니다.

## Critical Analysis & Limitations

**사실:** 제조 친화적 표현 공간·self-supervised simulation·post-ILT를 조합합니다. **저자 주장:** strict Manhattan mask를 통해 manufacturability를 개선합니다. **독자적 분석:** Manhattan과 full MRC는 같은 제약 집합이 아닙니다.

Point 수가 늘면 attention matrix 규모가 증가합니다. 균일한 segmentation은 계산을 불필요하게 키울 수 있고 너무 거친 segmentation은 corner correction을 놓칠 수 있습니다. influence-zone 선택과 최소 segment 길이의 민감도를 확인해야 합니다.

여러 polygon의 상대 위치를 변경하면 self-intersection·overlap·minimum space·topology 변화가 생길 수 있습니다. axis alignment만 유지하는 update로 이러한 제약이 모두 해결되는지는 별도 검증 문제입니다. optional refinement 포함 여부와 비용도 정확하게 나눠야 합니다.

Diffusion이 단일 deterministic regressor보다 필요한 이유는 multi-modal inverse solution·robust training·constraint representation 등으로 설명할 수 있지만, 실제 기여는 동일 representation에서 diffusion 제거 ablation을 읽어야 판단할 수 있습니다. 미확인 ablation 결과를 만들어 설명하지 않습니다.

## Practical Applications to GeoSignal / OPC

* 형상을 유지하는 출력은 학습 예측과 모서리 기반 업무를 연결할 수 있습니다.
* Manhattan 정렬만으로 전체 마스크 규칙을 보장하지는 않습니다.

현재 공개 기능은 [GeoSignal 적용 범위]({{ '/ko/notes/research/geosignal-scope/' | relative_url }})에 정리했습니다. 이 항목들은 연구 맥락이며 구현 완료를 뜻하지 않습니다.

## Key Takeaways & References

1. Token은 word가 아니라 layout geometry 표현입니다.
2. Point/polygon context와 image resolution을 구분합니다.
3. Rasterization gradient가 inverse 학습의 중요한 연결부입니다.
4. Diffusion time과 lithographic exposure time은 다릅니다.
5. Mean EPE와 violation count는 다릅니다.
6. Manhattan constraint가 전체 제조 적합성을 보장하지 않습니다.

[Inverse Problem · Metrics]({{ '/ko/notes/foundations/inverse-and-metrics/' | relative_url }}) · [Hi-ILT]({{ '/ko/notes/research/hi-ilt/' | relative_url }}) · [ResGNN-OPC]({{ '/ko/notes/research/resgnn-opc/' | relative_url }})
