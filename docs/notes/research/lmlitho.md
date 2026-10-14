---
layout: technical
category: research
paper_id: lmlitho
title: "LMLitho — source–mask 관계를 학습하는 대형 forward model"
permalink: /ko/notes/research/lmlitho/
lang: ko
---

# LMLitho: source–mask 관계를 학습하는 대형 forward model

* 목차
{:toc}

<div class="evidence-note">저자 제공 9페이지 PDF의 본문·Figures 1–13·Tables I–IV·Algorithm 1을 확인했습니다. 원본 이미지는 재배포하지 않습니다. 별도 supplementary는 확인하지 못했습니다. 이 페이지의 attention·gradient·실무 분석은 독자적 설명이며 물리 법칙과 학습적 유사성을 구분합니다.</div>

## Paper Information

| 항목 | 확인 내용 |
| --- | --- |
| 정식 제목 | LMLitho: A Large Vision Model-Driven Lithography Simulation Framework |
| 저자 | Zhen Wang, Hongquan He, Tao Wu, Xuming He, Qi Sun, Cheng Zhuo, Bei Yu, Jingyi Yu, Hao Geng |
| 소속 | ShanghaiTech University; Qi Sun·Cheng Zhuo: Zhejiang University; Bei Yu: The Chinese University of Hong Kong |
| 발표 | ICCAD 2025 |
| 원문 | [DOI](https://doi.org/10.1109/ICCAD66269.2025.11240940) · [저자 제공 PDF](https://www.cse.cuhk.edu.hk/~byu/papers/C286-ICCAD2025-LMLitho.pdf) |
| 공식 repository | [LMLitho/LMLitho](https://github.com/LMLitho/LMLitho). README와 일부 데이터 archive 확인; 모델 구현·pretrained checkpoint는 확인하지 못함 |
| 분야 | source-conditioned forward resist simulation; frozen simulator를 이용한 mask generator 학습 |

## Executive Summary

**한 문장:** mask와 illumination source를 별도 encoder로 표현하고 cross-attention으로 결합해 resist image를 예측하는 대형 vision model입니다.

많은 mask-to-resist 모델은 고정 광원을 가정합니다. 광원을 바꿨을 때 같은 mask가 다르게 인쇄되는 관계를 입력으로 표현하는 것이 이 연구의 핵심입니다. 대규모 simulation pair로 복잡한 source–mask–resist 관계를 학습하고, 신규 node에는 fine-tune합니다.

실무적으로는 source map을 scalar sigma 하나로 축약하지 않고 조건 입력으로 유지하는 데이터 설계, 그리고 학습 simulator를 frozen forward engine으로 inverse 학습에 연결하는 방법을 배울 수 있습니다. cross-attention을 interference의 정확한 해석식이라고 부르는 것은 과장입니다.

## Background & Motivation

[Abbe Imaging]({{ '/ko/notes/abbe-imaging/' | relative_url }})에서 source의 위치·weight가 달라지면 pupil이 통과시키는 mask spectrum의 조합이 바뀝니다. 같은 layout이라도 annular·quasar·multi-pole 아래의 aerial response가 다를 수 있습니다. mask만 보는 모델은 training source에 묶인 mapping을 학습하게 됩니다.

좁은 convolution receptive field는 멀리 있는 feature의 context를 다루기 어렵습니다. ViT는 patch 전체에 attention을 계산할 수 있어 long-range context를 직접 연결합니다. 그러나 global receptive field가 실제 optical support와 같지는 않으며, 더 넓은 context는 계산량·데이터 요구량을 함께 늘립니다.

## Physics & Mathematical Foundations

### Cross-attention을 좌표와 shape로 이해하기

Mask patch 수를 $$N$$, source token 수를 $$N_s$$, head dimension을 $$d$$라 두면

$$
\begin{aligned}
Q&\in\mathbb R^{N\times d},\\
K&\in\mathbb R^{N_s\times d},\quad V\in\mathbb R^{N_s\times d_v},\\
A&=\operatorname{softmax}\left(\frac{QK^T}{\sqrt d}\right),\\
Y&=AV.
\end{aligned}
$$

$$A$$ shape는 $$N\times N_s$$, $$Y$$는 $$N\times d_v$$입니다. 각 mask query가 source token에 대한 learned relevance를 계산합니다. dot product의 분산이 dimension과 함께 커지는 것을 완화하려고 $$\sqrt d$$로 나눕니다. latent weight·embedding은 무차원이며 직접적인 광학 단위는 없습니다.

원문 식 (5)는 mask embedding을 Q, source embedding을 K/V로 사용합니다. head별 projection은 compatible dimension을 만들기 위한 일반적인 attention 연산입니다. raw mask/source embedding dimension이 같다고 임의로 가정하지 않습니다.

### Attention과 광학의 연결·차이 — 독자적 분석

Abbe source weight는 입사 광원 intensity에 의해 정해지고 mask와 무관합니다. Attention weight는 Q/K에서 학습되므로 mask에 따라 달라집니다. 또한 softmax weight는 양수·row-normalized이고 complex phase interference는 직접 포함하지 않습니다. 따라서 attention의 weighted sum을 Abbe source summation과 완전히 동일하게 해석하면 안 됩니다. 물리적 관계를 표현하기 위한 학습 구조의 유사성입니다.

### Resist supervision과 inverse gradient

픽셀 예측 $$P_p\in[0,1]$$, label $$G_p\in\{0,1\}$$에서 BCE는 foreground/background mismatch를, Dice는 overlap을, SSIM은 local structure를 다룹니다. 원문 식 (6)의 조합은 $$\alpha L_{dice}+\beta L_{BCE}+\gamma L_{SSIM}$$입니다. 광학 PDE residual loss는 아닙니다.

Binary target이 sparse할 때 전체 accuracy만 최적화하면 background 예측이 쉬운 해가 될 수 있습니다. overlap loss는 이 불균형을 완화하지만 작은 via가 없어지거나 edge가 약간 이동하는 현상을 EPE 없이 모두 잡는 것은 아닙니다.

## Proposed Method / Model Architecture

Section III·Figure 5의 흐름은 Mask Encoder → Source Encoder와의 Exposure Attention → Resist Decoder입니다. mask는 non-overlapping patch·position embedding·ViT·local residual refinement를 거칩니다. source branch는 residual·self-attention·downsampling을 사용하고 decoder는 local edge refinement와 global attention을 결합합니다.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/lmlitho.svg' | relative_url }}"><img src="{{ '/assets/notes/research/lmlitho.svg' | relative_url }}" alt="독자 제작: LMLitho의 mask query와 source key/value를 결합하는 데이터 흐름" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">확대 보기 ↗</span></a>
<figcaption>독자 제작 attention 데이터 흐름도. 원본 Figure 5와 구분하며 channel·patch dimension은 기호로 표시합니다.</figcaption>
</figure>

원문의 $$M\in\mathbb R^{H\times W}$$를 $$P\times P$$ patch로 나누면 $$N=(H/P)(W/P)$$이고 embedding은 $$N\times D_m$$입니다. source image와 mask image는 서로 다른 좌표 공간이므로 같은 pixel 간격 또는 aligned patch index라고 해석하지 않습니다.

Algorithm 1·Figure 7은 대규모 pre-training 후 Source Encoder를 freeze하고 나머지 모듈을 fine-tune합니다. Section IV는 4 attention heads, mask depth 4, source/decoder depth 2, 약 0.3B parameters와 4 H100을 명시합니다. 정확한 patch size·batch schedule·peak memory는 이 리뷰에서 검증하지 못했습니다.

**Physics-Informed/Guided 판별:** source를 입력으로 보존하고 interaction을 attention으로 표현하는 architecture prior, commercial-simulator labels에 의한 supervision입니다. Figure 11의 inverse 학습에서는 frozen LMLitho의 gradient가 mask generator를 guide합니다. 이는 Maxwell equation이나 resist reaction equation을 exact constraint로 강제하는 구조는 아닙니다.

## Figures & Visual Explanation

아래는 **Main Paper 13/13개**를 번호별로 연결한 목록입니다. caption은 요지와 원문 위치를 제공하고 원본 파일을 재배포하지 않습니다. Figure 8과 9의 red/gray 정의가 서로 바뀌므로 해당 그림의 caption·본문을 따라 읽습니다.

{% include figure-coverage.html %}

## Experiments & Results

Table I의 flexible-source pre-training 합계는 101,650 samples이며 tests는 CPU 150, metal 750, via 300입니다. fixed-source training은 3,435, tests는 25/90/50입니다. source map은 201×201을 256×256으로 pad합니다. mask/resist는 1 nm²/pixel, 4 µm²/image입니다. 이산 square pixel 기준 1 nm pixel pitch와 일치합니다. README의 partial data 공개와 paper의 전체 dataset 규모는 구분합니다.

| 같은 평가 조건 | Baseline mIoU [%] | LMLitho mIoU [%] | 원문 |
| --- | ---: | ---: | --- |
| 28nm-S-CPU · flexible source | Abbe 86.17 / Torch Litho 84.18 | 97.78 | Table II(a) |
| 28nm-CPU · fixed annular source | DOINN 97.14 / DLS 96.46 | 98.12 | Table II(b) |
| 20nm-CPU · 새 node 학습·fine-tuning | DOINN 96.10 / DLS 92.51 | 97.62 | Table IV |

Table III의 5-epoch ablation에서 CNN+attention mIoU는 94.62%, ViT without source/decoder attention은 94.74%, 둘 다 제거하면 92.73%, full model은 96.32%입니다. 비교마다 수정한 module과 training budget을 확인하며, 한 예시의 receptive-field visualization만으로 기여를 판단하지 않습니다.

baseline optical/resist의 모델링 수준이 commercial labels와 다르므로 Table II(a)는 “물리 모델보다 AI가 정확하다”라는 보편적 결론의 근거가 아닙니다. source encoder freeze 후 20 nm data로 fine-tune했으므로 Table IV는 zero-shot transfer도 아닙니다.

Section IV-A는 GPU 모델 inference 약 0.12 s와 optical model이 이미 구성된 CPU commercial simulation 약 15 s를 비교합니다. source model setup 약 40 min은 별도 경우입니다. 120× 주장을 end-to-end training amortization 또는 같은 hardware algorithm speedup으로 바꾸지 않습니다.

BenchOPC는 3,000 training layouts·25 tests이고 final mask를 commercial tool에서 재평가합니다. Figure 12의 PVB 조건은 dose ±3%, defocus ±40 nm입니다. Figure 10의 28 nm forward mean EPE는 LMLitho 0.42 nm, DOINN 0.67 nm, DLS 0.84 nm입니다. 이는 **forward predicted contour 대 golden contour**이며 mask optimization의 target 대비 EPE와 다릅니다. optical NA·wavelength의 전체 calibrated configuration과 split leakage 검증은 공개 자료만으로 충분히 재현하지 못했습니다.

## Critical Analysis & Limitations

**사실:** 별도 source input, 큰 simulation dataset, cross-node fine-tuning, frozen-engine inverse test가 있습니다. **저자 주장:** large vision model의 범용성과 source-aware 표현이 lithography foundation model로 이어질 수 있습니다. **독자적 분석:** training distribution 내 source interpolation과 새로운 optical process extrapolation은 다른 문제입니다.

0.3B weight를 float32로만 저장하면 단순 계산상 약 1.2 GB입니다. 이 값은 **독자 계산**이며 논문의 measured GPU memory가 아닙니다. optimizer state·activation·batch attention이 더해지면 학습 memory는 크게 늘어납니다. LMLitho가 small ROI를 처리할 때 기존 Abbe cache보다 유리할지는 batch·source reuse·GPU availability에 따라 달라집니다.

Source Encoder를 freeze하는 정책은 새 공정의 optics 변화가 작다는 가정에 의존할 수 있습니다. source shape는 비슷해도 NA·aberration·resist가 바뀌면 같은 encoder 표현이 적절한지 재검증해야 합니다. 상용 simulator ground truth를 잘 재현한 것은 wafer metrology로 검증한 것과 다릅니다.

최종 inverse mask를 별도 engine에서 평가한 점은 중요합니다. 그러나 reference 재평가의 평균 image fidelity가 gradient 정확도·worst EPE·complete MRC를 자동으로 보증하지 않습니다.

## Practical Applications to GeoSignal / OPC

* **당장 적용 가능한 아이디어:** source map과 mask ROI를 별도 sample field로 보존합니다. [현재 코드 범위]({{ '/ko/notes/research/geosignal-scope/' | relative_url }})에는 scalar optical calculation만 있습니다.
* **추가 연구 / Hypothesis:** fixed-condition aerial surrogate에서 source-conditioned model로 확장하고, source family별 held-out split을 설계합니다. source encoder cache와 end-to-end runtime을 비교합니다.
* **장기 / Hypothesis:** calibrated resist data가 확보됐을 때 contour·CD·process-window prediction으로 확장합니다. 현재 threshold contour를 학습했다고 chemical resist physics를 학습했다고 부르지 않습니다.

## Key Takeaways & References

1. Source input이 이 논문의 중요한 차별점입니다.
2. Attention weight는 physical source intensity weight가 아닙니다.
3. Forward EPE와 inverse EPE의 reference가 다릅니다.
4. 20 nm 결과는 fine-tuning 후 결과입니다.
5. CPU–GPU·setup 비용·training 비용을 구분해 runtime을 읽습니다.
6. Frozen forward model은 parameter를 고정해도 input gradient를 전달할 수 있습니다.

[Abbe Imaging]({{ '/ko/notes/abbe-imaging/' | relative_url }}) · [Metrics]({{ '/ko/notes/foundations/inverse-and-metrics/' | relative_url }}) · [LMLitho 공식 데이터 repository](https://github.com/LMLitho/LMLitho) · [LithoSim](https://dw-hongquan.github.io/LithoSim/)
