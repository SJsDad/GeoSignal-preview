---
layout: technical
category: research
paper_id: nitho
title: "Nitho — mask가 아니라 optical kernel을 학습하기"
permalink: /ko/notes/research/nitho/
lang: ko
---

# Nitho: mask가 아니라 optical kernel을 학습하기

* 목차
{:toc}

<div class="evidence-note">arXiv v4 본문·6페이지 PDF·Main Figures 1–6·Tables I–V·Algorithm 1을 확인했습니다. license 표기는 CC BY-NC-ND 4.0입니다. 이 사이트의 이미지 재배포는 보류하고 독자 도식과 공식 링크를 사용합니다. 별도 supplementary 공개는 확인하지 못했습니다.</div>

## Paper Information

| 항목 | 확인 내용 |
| --- | --- |
| 정식 제목 | Physics-Informed Optical Kernel Regression Using Complex-valued Neural Fields |
| 저자 | Guojin Chen, Zehua Pei, Haoyu Yang, Yuzhe Ma, Bei Yu, Martin D. F. Wong |
| 소속 | The Chinese University of Hong Kong; Haoyu Yang: NVIDIA; Yuzhe Ma: HKUST(GZ) |
| 발표 | DAC 2023; arXiv record에서 Accepted by DAC23 확인 |
| 원문 | [arXiv](https://arxiv.org/abs/2303.08435) · [v4 PDF](https://arxiv.org/pdf/2303.08435v4) · [v4 HTML](https://arxiv.org/html/2303.08435v4) · [arXiv DOI](https://doi.org/10.48550/arXiv.2303.08435) |
| 코드·dataset·weights | 원 저자 공식 구현·학습 kernel 공개 미확인. ICCAD/ISPD layouts는 reference imaging labels와 별개 |
| 분야 | Forward optical simulation / complex kernel identification |

## Executive Summary

**한 문장:** 고정 optical condition에서 mask-independent complex kernels를 neural field로 식별하고, 새로운 mask는 고정 FFT/SOCS 연산으로 처리합니다.

Mask마다 neural network가 이미지를 직접 생성하는 방법과 달리, Nitho는 mask의 알려진 linear operation을 그대로 둡니다. 학습 대상은 source/pupil 정보를 요약하는 kernel입니다. 학습이 끝나면 kernels를 저장할 수 있어 매 mask마다 MLP inference가 필요하지 않습니다.

실무적으로 가장 중요한 차이는 **offline system identification과 online image synthesis의 분리**입니다. 다만 kernel은 공정 조건에 묶이므로 새로운 optics·resist가 주어졌을 때 저절로 일반화한다고 주장할 수 없습니다.

## Background & Motivation

Image-to-image predictor는 geometry distribution과 imaging system을 동시에 학습합니다. 새로운 mask morphology에 대한 generalization이 어려울 수 있습니다. [Hopkins/TCC/SOCS]({{ '/ko/notes/foundations/hopkins-tcc-socs/' | relative_url }})는 mask와 optics를 수학적으로 분리할 수 있으므로 이 구조를 학습에도 반영합니다.

Neural field는 좌표를 입력으로 받아 그 위치의 function value를 반환하는 MLP입니다. Nitho에서 좌표는 physical scene의 3D position이 아니라 optical kernel grid의 coordinate입니다. NeRF-inspired라고 해서 volumetric scene rendering이나 view direction input이 있다는 뜻은 아닙니다.

## Physics & Mathematical Foundations

### Kernel 합성과 mask 분리

원문 식 (9)의 형태는

$$
I(M)=\sum_{j=1}^{r}\left|\mathcal F^{-1}\left[K_j\odot\mathcal F(M)\right]\right|^2.
$$

$$M$$은 binary mask, $$K_j$$는 complex optical mode kernel, $$r$$은 retained modes입니다. eigenvalue scaling은 kernel에 흡수할 수 있습니다. $$K_j$$는 실제 source point와 일대일 대응하는 것이 아니라 effective coherent mode로 읽는 것이 정확합니다.

MLP는 mask가 아니라 coordinate $$v$$에서 $$K(v)$$를 출력합니다. mask FFT·kernel multiplication·IFFT·absolute square sum은 fixed operation입니다. **Physics-Informed 위치는 이 고정 합성식과 학습 target의 분리**입니다. 단순히 complex weight를 썼다는 사실보다 더 강한 구조적 제약입니다.

### Complex neural field와 positional encoding

원문은 complex linear layers와 실수/허수별 ReLU를 사용하고, Gaussian random Fourier features(RFF)를 좌표 encoding으로 사용합니다. 일반적인 real RFF 예시는

$$
\gamma(v)=[\cos(2\pi Bv),\sin(2\pi Bv)],\quad B_{ab}\sim\mathcal N(0,\sigma^2).
$$

$$v\in[0,1]^2$$는 정규화된 무차원 coordinate, $$B$$는 feature-frequency matrix입니다. Nitho 원문 식 (15)는 이 feature를 $$(1+i)$$로 complex domain에 올립니다. embedding frequency는 optical spatial frequency와 같은 단위가 아닙니다.

Low-dimensional MLP는 smooth low-frequency function부터 학습하는 경향이 있어 rapidly varying complex kernel을 표현하기 어렵습니다. RFF는 다양한 방향·빈도의 basis를 제공해 학습을 쉽게 할 수 있습니다. Gaussian scale을 키우면 빠른 variation을 표현하지만 noise fitting·optimization cost도 변할 수 있습니다. CReLU는 일반적으로 holomorphic하지 않으며, 실수·허수 parameter에 대한 differentiation과 complex analyticity는 구분해야 합니다.

### Kernel support 설계의 단위 — 독자적 확인

ROI 물리 폭을 $$L_x$$ [nm]라 하면 원문 식 (10)의 dimension heuristic은 대략 $$m\simeq4\mathrm{NA}L_x/\lambda+1$$ 꼴입니다. 원문은 1 nm/pixel을 가정해 image width를 physical width와 대응시킵니다. pixel pitch가 달라지면 $$L_x=W\Delta x$$를 넣어야 합니다.

이 식은 resolution-based design heuristic입니다. 실제 shifted pupil/source support, FFT grid, crop·zero-padding, learned rank를 맞춰야 합니다. 임의 NA나 arbitrary source에 universal bandwidth cutoff로 그대로 이식하지 않습니다.

## Proposed Method / Model Architecture

Figure 3(a)·Algorithm 1: normalized coordinates → RFF → complex MLP → kernels. 별도의 mask FFT를 central crop하고 kernels와 곱해 aerial image를 합성하며 supervised aerial MSE로 parameters를 갱신합니다. binary resist는 constant threshold로 얻습니다.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/nitho.svg' | relative_url }}"><img src="{{ '/assets/notes/research/nitho.svg' | relative_url }}" alt="독자 제작: Nitho의 offline kernel 학습과 online mask FFT 합성 경로" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">확대 보기 ↗</span></a>
<figcaption>독자 제작 설명도. 원본 Figure 3을 복제하지 않았으며 training-time neural field와 inference-time cached kernel을 분리합니다.</figcaption>
</figure>

Kernel tensor는 $$r\times n\times m$$ complex array, input coordinate는 $$nm\times2$$입니다. batch mask $$B\times1\times H\times W$$의 spectrum은 retained support에 맞춥니다. crop한 spectrum을 IFFT할 때 output resolution을 유지하려면 zero-padding/FFT normalization이 맞아야 하며, 작은 crop array를 바로 IFFT해 원본 grid intensity로 간주하면 안 됩니다. 이 부분은 재현 구현에서 반드시 확인할 항목입니다.

학습 후 kernels를 cache하면 new mask의 online path는 FFT·mode별 multiplication/IFFT·intensity sum뿐입니다. kernel precomputation 비용과 mode count에 따른 inference 비용을 따로 기록해야 합니다. trained network bytes와 exported kernel bytes도 다릅니다.

## Figures & Visual Explanation

{% include figure-coverage.html %}

Main Figures 6/6개를 연결했습니다. Table V는 positional encoding ablation, Figure 6은 dataset ratio와 kernel dimension ablation이므로 서로 같은 실험으로 합치지 않습니다. 별도 Supplementary는 확인되지 않았습니다.

## Experiments & Results

Table II: ICCAD B1은 4,875 training·10 test, B1opc는 10 OOD tests, ISPD metal B2m은 1,000/300, via B2v는 10,000/10,000입니다. 4 µm² tiles를 2000×2000으로 표현합니다. ISPD reference는 Calibre·193 nm·NA 1.35이며 ICCAD reference는 contest Lithosim입니다. source·focus/dose variation·wafer resist calibration을 통일한 전체 protocol은 아닙니다.

| Table III · aerial MSE ×10⁻⁵ | DOINN 재학습 | Nitho |
| --- | ---: | ---: |
| B1 | 5.55 | 1.32 |
| B2m | 1202.39 | 25.48 |
| B2v | 2.26 | 2.01 |
| B2m+B2v | 3114.24 | 33.13 |
| 표의 평균 | 1081.11 | 15.49 |

약 69× MSE 차이는 표 평균의 ratio이며 모든 row가 69×라는 뜻은 아닙니다. B2v 차이는 작고 B2m/mixed 차이가 큽니다. 이 표의 DOINN은 Nitho protocol에서 다시 학습한 모델로, DOINN 원논문의 Table 2와 직접 비교하지 않습니다.

Table IV의 B2m→B2v mIoU는 DOINN 78.31%, Nitho 97.33%입니다. shape OOD의 장점을 보여주지만 같은 imaging reference 아래의 실험이며 새 scanner process generalization은 아닙니다. Table V에서 B1 PSNR은 PE 없음 25.33 dB, NeRF PE 48.83 dB, RFF 50.75 dB입니다. PSNR은 로그 척도이므로 50.75/25.33을 “정확도 2배”라고 계산하지 않습니다.

Table I는 모델 크기를 0.41 MB와 DOINN 약 1.3 MB로 표기하며 parameter-count 단위와 혼용 가능성을 남깁니다. DOINN 본문은 1.3M parameters로 표기합니다. 이 discrepancy를 임의로 정정해 동일 weight-storage 조건의 memory ranking으로 만들지 않습니다. Figure 5는 throughput 약 1.3× improvement와 reference 대비 약 90× speedup을 설명하지만 inference cache·GPU·simulator 비용 범위를 함께 확인해야 합니다.

## Critical Analysis & Limitations

**구조적 이점:** learned model이 mask morphology를 직접 생성하지 않아 고정 optical model에서 shape OOD에 유리할 수 있습니다. **한계:** shift invariance·fixed process·finite kernel support·rank truncation 가정입니다. 실제 mask 3D scattering처럼 geometry-dependent optics가 큰 경우 동일 mask-independent kernel로 충분한지는 별도 문제입니다.

Intensity supervision만으로 coherent modes는 유일하지 않습니다. 모든 $$K_j$$에 unitary mixing을 적용해도 sum of squared fields는 같을 수 있습니다. 따라서 recovered kernel이 실제 eigenmode와 동일하다는 검증을 추가하지 않으면 kernel visualization을 physical identification의 유일한 증거로 삼지 않습니다.

학습 후 exported kernel을 쓰는 inference는 conventional SOCS와 가까워집니다. 속도 이득을 neural field 자체의 online 연산으로만 설명하면 핵심을 놓칩니다. exact reference kernels가 이미 cache돼 있을 때와 비교한 이득도 필요합니다.

Constant threshold resist는 chemistry가 아닙니다. source/focus/dose를 입력으로 condition한 neural field 또는 condition별 kernels가 없으면 DoF·Bossung generalization을 검증했다고 할 수 없습니다.

## Practical Applications to GeoSignal / OPC

* **당장 적용 가능한 아이디어:** existing SOCS/Abbe reference에 대해 kernel support·normalization·exported cache size를 명확히 기록합니다. [현재 scope]({{ '/ko/notes/research/geosignal-scope/' | relative_url }})의 exact cross-validation 경로와 연결되는 연구 설계입니다.
* **추가 연구 / Hypothesis:** fixed optical condition의 learned kernels를 식별한 뒤 aerial/CD·directional gradient·mode-rank error를 평가합니다. exact kernels가 있는 경우 학습이 필요한 이유도 baseline으로 검토합니다.
* **장기 / Hypothesis:** source·focus·aberration 조건의 kernel neural field, uncertainty-aware rank selection, calibrated resist coupling을 연구합니다. 현재 지원 기능으로 표시하지 않습니다.

## Key Takeaways & References

1. 학습 입력은 kernel coordinate이며 mask image가 아닙니다.
2. Online inference에는 cached kernels만 사용할 수 있습니다.
3. Physics-Informed의 핵심은 고정 synthesis와 learned kernel의 분리입니다.
4. SOCS mode와 physical source point는 일대일 대응하지 않을 수 있습니다.
5. Kernel dimension heuristic은 pixel pitch와 단위를 확인해야 합니다.
6. Shape OOD와 process OOD는 다릅니다.
7. PSNR·model bytes·parameter count의 단위를 구분합니다.

[Hopkins/TCC/SOCS]({{ '/ko/notes/foundations/hopkins-tcc-socs/' | relative_url }}) · [Fourier Optics]({{ '/ko/notes/fourier-optics/' | relative_url }}) · [DOINN]({{ '/ko/notes/research/doinn/' | relative_url }}) · [TEMPO]({{ '/ko/notes/research/tempo/' | relative_url }})
