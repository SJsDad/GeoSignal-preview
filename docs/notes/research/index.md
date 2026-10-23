---
layout: technical
category: research
title: OPC ML/DL Research Paper Reviews
permalink: /ko/notes/research/
lang: ko
---

# OPC ML/DL Research Paper Reviews

* 목차
{:toc}

## 학습 목적과 읽는 순서

이 자료는 논문의 성능 순위를 매기는 대신 **어떤 물리 정보를 어떤 학습 표현에 넣는가**를 비교합니다. 최신 5편을 먼저 읽고, TEMPO·DOINN·Nitho에서 background와 architecture의 연결을 되짚을 수 있습니다. 초록·부분 본문만 확보된 논문은 그 제한을 문서 첫머리에 표시합니다. 모든 페이지가 존재한다는 것과 모든 원문·보충자료가 완전히 검증됐다는 것은 구분합니다.

먼저 [Physics & Math Foundations]({{ '/ko/notes/foundations/' | relative_url }})에서 Abbe·FFT·TCC/SOCS·inverse gradient와 지표를 확인합니다. 구현 아이디어는 [GeoSignal 현재 범위]({{ '/ko/notes/research/geosignal-scope/' | relative_url }})와 연결해 읽습니다. [원문 접근·Figure coverage·라이선스 기록]({{ '/ko/notes/research/sources/' | relative_url }})에서 미완료 항목을 확인할 수 있습니다.

## 논문 탐색

연도·분야·architecture 필터를 함께 사용할 수 있습니다. JavaScript가 없어도 전체 표와 모든 문서 링크는 보입니다.

{% include research-catalog.html %}

## OPC ML/DL 연구 발전 과정

| 연구 단계 | 여기서 읽는 대표 연구 | 바뀌는 질문 |
| --- | --- | --- |
| 2020 · conditional image modeling | TEMPO | geometry·film height를 shared generator로 처리할 수 있는가? |
| 2022 · global/local frequency modeling | DOINN | 넓은 optical context와 좁은 edge detail을 효율적으로 함께 표현할 수 있는가? |
| 2023 · 물리 연산과 학습 대상의 분리 | Nitho | mask의 알려진 연산을 고정하고 optical kernel만 식별할 수 있는가? |
| 2025 · 입력·출력 표현 확장 | LMLitho, TokMan, ResGNN-OPC | source-conditioned resist, constrained geometry tokens, edge graph update 중 어디가 업무에 맞는가? |
| 2026 · 광학 prior와 hybrid 정제 | OptiCo, Hi-ILT | complex phase prior와 learned initializer를 physics optimization에 어떻게 연결하는가? |

CNN→FNO→Physics-Informed→Transformer/Generative의 흐름은 일부 설계 축을 보여줍니다. 모든 연구가 이전 모델을 대체하는 단일 계보는 아닙니다. Nitho의 작은 MLP와 LMLitho의 대형 Transformer는 같은 문제를 같은 조건에서 겨루는 모델이 아닙니다. Transformer·GAN·VAE·diffusion은 서로 다른 representation과 supervision 목표를 가질 수 있습니다.

## Forward Modeling과 Inverse Optimization

Forward model은 $$g(M,p)\to I$$ 또는 $$R$$을 예측합니다. inverse는 $$g(M,p)$$를 target $$T$$에 가깝게 만들 $$M$$을 찾습니다. 여기서 $$p$$는 광학·공정 조건이며 $$I$$는 intensity, $$R$$은 resist/contour입니다.

$$
\text{Forward: }\widehat R=f_\theta(M,p),\qquad
\text{Inverse: }M^*=\arg\min_{M\in\mathcal C}\mathcal L(g(M,p),T).
$$

Forward error가 작으면 inverse에서 유리할 수 있지만, surrogate gradient가 틀리면 optimizer가 잘못된 mask로 이동할 수 있습니다. 최종 mask를 independent reference engine으로 검증하는 과정이 필요합니다. [Inverse Problem · Metrics]({{ '/ko/notes/foundations/inverse-and-metrics/' | relative_url }})에서 chain rule과 EPE 정의를 설명합니다.

## 입력·출력·아키텍처 비교

| 논문 | 주 입력 | 주 출력 | 핵심 표현 | 물리 지식의 주입 위치 |
| --- | --- | --- | --- | --- |
| OptiCo | target; 별도 forward task의 mask | optimized mask; aerial/resist | complex convolution + OP kernel | layer의 phase prior·residual branch; TV는 별도 제조 정규화 |
| Hi-ILT | target | 초기 mask → ILT-refined mask | lightweight hierarchical VAE/CNN + ILT | 후속 physics-guided optimization; VAE 내부 세부는 미확인 |
| LMLitho | source map + mask | resist image | ViT·source attention·cross-attention·decoder | 입력 조건화·학습 interaction 구조·commercial labels |
| TokMan | segmented Manhattan layout points | axis corrections·rendered mask | polygon/point tokens + diffusion Transformer | geometry prior·differentiable lithographic loss·후속 ILT |
| ResGNN-OPC | geometry graph로 표현한 mask 관련 정보 | OPC correction | residual graph convolution | iteration-inspired 구조; 정확한 physical feature/loss는 미확인 |
| TEMPO | mask; Scheme 2는 thin aerial 추가; film height | thick-mask aerial slice | height-conditioned cGAN | condition·physical intermediate input·rigorous labels |
| DOINN | mask | resist/contour | one Fourier GP + CNN LP + reconstruction | optical FFT pipeline과 유사한 architecture prior |
| Nitho | 학습: kernel coordinates + mask/aerial pairs; 추론: mask | kernels·aerial·threshold resist | complex neural field + fixed SOCS | mask-independent kernel learning, fixed optical synthesis |

**Physics-Informed라는 이름만으로 수준을 판단하지 않습니다.** input feature를 물리적으로 구성하는 것, layer를 물리 형태로 제한하는 것, PDE residual을 loss에 넣는 것, physical simulator가 optimization을 guide하는 것은 다른 방법입니다. 이 8편이 모두 PDE-residual PINN을 사용한다는 설명은 틀립니다.

## 성능 지표와 Benchmark 비교

| 연구 | evaluation reference·dataset | 읽어야 하는 지표 | 직접 교차 순위를 매기기 어려운 이유 |
| --- | --- | --- | --- |
| OptiCo | LithoBench MetalSet/ViaSet·StdMetal/StdContact | inverse MSE 표기값·PVB·EPE violations, forward MSE/IoU | inverse와 forward scale이 다르고 EPE는 count |
| Hi-ILT | 공개 초록의 ICCAD 2013 32 nm·45 nm LithoBench | 최대 개선율 L2/PVB/EPE/TAT | 개별 baseline·표·공정 조건 미확인 |
| LMLitho | commercial labels·28 nm/20 nm·BenchOPC | mIoU/mPA·mean EPE [nm]·mask L2/PVB | source 조건·fine-tuning·CPU/GPU 차이 |
| TokMan | ICCAD13-S/L | mean EPE·shots·TAT | violation count 대신 mean distance; refinement 포함 |
| ResGNN-OPC | private numerical dataset | correction error·EPE [nm]·runtime | optical conditions·dataset·cost boundary 미확인 |
| TEMPO | DUV contact·13 film heights·Sentaurus reference | RMSE/NRMSE·central-contact CD | 3D mask-effect task; xy pitch 7.5 nm; inverse task가 아님 |
| DOINN | ISPD via·ICCAD metal·N14 | mIoU/mPA·throughput | L/H image sampling과 large-tile conditions 차이 |
| Nitho | ICCAD Lithosim·ISPD Calibre | aerial MSE/PSNR·mIoU·shape OOD | reference system·retrained baselines·kernel cache |

동일한 benchmark 이름도 dataset version·split·mask stage·optical model·pixel pitch·threshold·evaluation implementation이 다를 수 있습니다. 원문별 표 안의 비교는 유효하게 설명하되 논문 간의 절대 SOTA 순위는 만들지 않습니다.

### 대표 수치의 올바른 읽기

* OptiCo Table 1에서 OOD EPE가 낮지만, 평균 PVB는 DOINN보다 높습니다.
* LMLitho Table IV의 advanced-node 성능은 fine-tuning 후 결과입니다.
* TokMan Table 1에서 simple/large case의 TAT 우위가 같지 않습니다.
* ResGNN Table 1에서 predictor는 빠르지만 final EPE는 conventional MBOPC보다 높습니다.
* TEMPO Scheme 1과 Scheme 2는 speedup·accuracy가 다릅니다.
* DOINN large-tile scheme은 training tile을 넘어서는 frequency/grid 문제를 다룹니다.
* Nitho의 약 69× MSE 개선은 해당 표 평균 ratio이며 via-only row의 차이는 작습니다.

모든 숫자와 비교 조건은 각 리뷰의 Experiments 절과 원문 Figure/Table 번호에 연결돼 있습니다. 하나의 공통 성능 숫자로 압축하지 않습니다.

## 공개 Benchmark를 활용하는 방법

[LithoBench 공식 repository](https://github.com/shelljane/lithobench)는 forward와 ILT model interfaces, datasets, baseline evaluation과 shot counting을 제공합니다. 원문 benchmark 수치를 재현할 때 repository version과 source configuration을 고정해야 합니다. README의 data/weights 배포 링크와 모델 원 저자의 코드 공개 여부는 구분합니다.

실제로 확인한 [LithoBench evaluation code](https://github.com/shelljane/lithobench/blob/9c74e82218e377eaf6d02d113fc1ce6e36c92aa6/pyilt/evaluation.py)는 binary output의 `mse_loss(..., reduction="sum")`와 pixel PVB count를 사용합니다. 따라서 논문에 MSE로 표시된 값도 normalization을 확인해야 합니다. 이 repository snapshot이 모든 논문의 exact experimental version이라는 뜻은 아닙니다.

[LithoSim 공식 프로젝트](https://dw-hongquan.github.io/LithoSim/)는 source·dose·defocus와 sub-28 nm 조건을 다루는 simulation benchmark 방향을 소개합니다. LMLitho의 일부 공개 dataset과 LithoSim 전체 benchmark를 같은 dataset이라고 가정하지 않습니다. 코드 Apache 2.0과 data CC BY-NC 4.0 조건도 별개입니다.

GeoSignal의 simplified source sampling·idealized relative focus/dose 결과를 이 benchmark의 calibrated resist labels와 같은 ground truth라고 사용하면 안 됩니다. 학습 목적에 따라 scalar reference matching과 commercial resist surrogate matching을 분리해야 합니다.

## Model-Based OPC와 ML-Based OPC

| 관점 | Model-Based OPC | ML-assisted OPC |
| --- | --- | --- |
| 반복 계산 | explicit model을 반복 호출해 process 조건·objective를 추적 | 학습이 일부 반복 비용을 사전 계산으로 이전 |
| 유연성 | 모델에 정의된 source·focus·dose 조건을 입력으로 변경 | conditioning과 training coverage 밖에서는 재검증 필요 |
| 보정 표현 | solver에 따라 edge/pixel/level set 등 | image, graph, token, latent 등 representation에 의존 |
| 정확도 관리 | calibration·numerical approximation·convergence 검증 | reference fidelity·distribution shift·gradient error·uncertainty 검증 |
| 계산 비용 | source/TCC setup·iteration cost | labels·training·deployment memory·inference·refinement cost |
| 최종 검증 | 공정 모델·MRC·verification gates | 같은 gates가 여전히 필요하며 independent reference가 중요 |

Hybrid는 learned initializer/predictor로 시간을 줄이고 model-based verification 또는 refinement를 유지하는 실용적인 방향일 수 있습니다. 다만 어떤 업무에서 유리한지는 layout scale·compute hardware·process stability·data availability에 따라 달라집니다.

## 향후 연구와 GeoSignal 연결

**당장 검토할 수 있는 아이디어:** physical units·normalization·source/focus/dose metadata를 갖춘 sample schema, layout-level split, image/contour/gradient 평가를 분리하는 benchmark 설계입니다.

**추가 연구 / Hypothesis:** fixed-condition learned optical kernel, coarse-to-fine optimization, geometry-preserving edge updates, source-conditioned forward surrogate를 작은 공개 ROI에서 검증합니다. nominal MSE뿐 아니라 EPE tail·CD·PVB·reference runtime을 확인합니다.

**장기 / Hypothesis:** vector/3D mask physics, calibrated resist·etch coupling, process-window-conditioned model, uncertainty/active learning, mask-rule-aware generation을 연구합니다. 이 8편의 numerical results를 산업에서 검증된 production flow로 소개하지 않습니다.

## 필수 용어 정리

| 용어 | 이 자료에서의 의미 |
| --- | --- |
| OP kernel | optical propagation phase를 convolution의 prior로 넣는 kernel |
| Neural operator / FNO | function/grid mapping을 학습하고 Fourier mode별 interaction을 처리하는 모델 계열 |
| Neural field | 좌표에서 function value를 출력하는 implicit representation |
| VAE | latent distribution과 decoder를 함께 학습하는 variational generative model |
| DiT | diffusion update의 조건부 sequence/image model에 Transformer를 사용하는 구조 |
| GNN / residual | graph neighbors의 aggregation 및 이전 feature에 learned increment를 더하는 구조 |
| Differentiable rasterizer | polygon/point 변화에서 pixel mask 변화로 gradient를 전달하는 렌더링 연산 |
| SRAF | main pattern response를 돕는 비인쇄 assist feature; 제약 확인 필요 |
| SOCS | positive semidefinite TCC를 coherent modes로 분해한 intensity 합성 |
| EPE / PVB | edge displacement 또는 violation count / process corners의 printed-region band |
| OOD / transfer | training distribution 밖 평가 / 신규 조건 데이터로 적응하는 학습 |

## References와 완성 범위

각 리뷰의 Paper Information에 공식 원문·DOI·확인된 코드/데이터를 연결했습니다. [Source & Figure Coverage]({{ '/ko/notes/research/sources/' | relative_url }})의 기록을 유지해 접근 제한을 full-review 완료로 숨기지 않습니다. 8개 리뷰·개요·기초 노트·탐색 UI는 한글·영문으로 제공하지만 미확보 본문·supplement 검증은 남아 있습니다.
