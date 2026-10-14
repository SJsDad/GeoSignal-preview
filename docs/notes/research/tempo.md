---
layout: technical
category: research
paper_id: tempo
title: "TEMPO — height 조건으로 공유하는 thick-mask aerial model"
permalink: /ko/notes/research/tempo/
lang: ko
---

# TEMPO: height 조건으로 공유하는 thick-mask aerial model

* 목차
{:toc}

<div class="evidence-note">저자 GitHub repository의 8페이지 PDF 전문을 읽었습니다. Main Figures 1–5와 Tables 1–5를 확인했습니다. 별도 supplementary·공식 모델 weights·전체 학습 dataset 공개는 확인하지 못했습니다. 원본 Figure 재사용 권한이 확인되지 않아 원문 링크와 독자 도식을 제공합니다.</div>

## Paper Information

| 항목 | 확인 내용 |
| --- | --- |
| 정식 제목 | TEMPO: Fast Mask Topography Effect Modeling with Deep Learning |
| 저자·소속 | Wei Ye, Mohamed Baker Alawieh, David Z. Pan: UT Austin; Yuki Watanabe, Shigeki Nojima: Kioxia Corporation; Yibo Lin: Peking University |
| 발표 | ISPD 2020, pp. 127–134 |
| 원문 | [DOI](https://doi.org/10.1145/3372780.3375565) · [저자 PDF 파일](https://github.com/ywwwer/ywwwer.github.io/blob/master/files/papers/DFM_ISPD2020_Ye.pdf) |
| 코드·데이터·weights | 공식 학습 구현·dataset·checkpoint 미확인. 저자 홈페이지 repository는 논문 자료이며 모델 코드라고 소개하지 않음 |
| 분야 | Mask Topography / height-conditioned 3D aerial slices |

## Executive Summary

**한 문장:** resist film 내부 여러 height의 aerial image를 하나의 conditional GAN으로 예측해 thick-mask reference simulation의 계산 비용을 줄입니다.

Mask geometry만 넣는 Scheme 1과 mask + thin-mask aerial image를 넣는 Scheme 2가 서로 다른 speed–accuracy 지점을 만듭니다. 여러 height마다 별도 네트워크를 학습하는 대신 shared encoder와 height-conditioned decoder를 사용합니다. **TEMPO의 height는 film 내부 z 위치이며 scanner defocus sweep과 같은 변수가 아닙니다.**

초록에서 EUV mask 문제를 일반 배경으로 읽을 수 있어도 실험을 EUV 13.5 nm 조건으로 소개하면 틀립니다. 실제 Section 4의 실험은 193 nm DUV·NA 1.2입니다.

## Background & Motivation

Thin mask는 transmittance가 무한히 얇은 평면에 놓였다고 근사합니다. thick mask는 edge·sidewall·재료 내부에서 scattering을 일으켜 transmitted field의 amplitude·phase·polarization을 바꿀 수 있습니다. 전자기 near-field를 정확히 계산하는 비용이 큰 이유입니다.

Thin-mask image를 단순히 fixed bias로 수정하면 pattern-dependent phase 변화를 놓칠 수 있습니다. 또한 film 안에서 height가 달라지면 diffraction field가 달라집니다. 이 변화를 height별 independent mapping으로 나누면 공통 geometry 정보를 다시 학습해야 합니다.

[Abbe Imaging]({{ '/ko/notes/abbe-imaging/' | relative_url }})은 projection imaging을 설명하지만 binary thin-mask input만으로 실제 mask topography를 복구할 수는 없습니다. TEMPO의 surrogate는 reference thick-mask simulation을 통해 그 차이를 데이터로 학습합니다.

## Physics & Mathematical Foundations

### Near-field와 aerial slice — 독자적 물리 설명

Mask 뒤의 복소 near-field를 $$E_{near}(x,y)$$라 두면 projection 및 film propagation을 포함하는 operator $$\mathcal H_h$$를 거쳐

$$
I_h(x,y)=|\mathcal H_h[E_{near}](x,y)|^2
$$

라는 coherent 예시로 표현할 수 있습니다. $$h$$는 film 내부 height [nm]이고 $$I_h$$는 정규화된 intensity입니다. partial coherence·polarization이 있으면 source·vector 성분별 합을 별도로 포함해야 합니다. 이 설명식은 TEMPO가 전자기 field를 직접 출력한다는 뜻이 아닙니다. output은 intensity image입니다.

높이별 image가 독립이 아닌 이유는 같은 mask와 optical stack이 만드는 field를 다른 plane에서 평가하기 때문입니다. 공유 latent representation은 geometry를 재사용하고 decoder에 height 조건을 넣을 수 있습니다. 하지만 sampled height 사이의 연속 interpolation이 자동으로 정확하다는 보장은 없습니다.

### Conditional GAN loss

일반적인 paired cGAN의 adversarial objective는 $$D$$가 reference와 generated pair를 구별하고 $$G$$가 reference와 유사한 image를 생성하도록 학습합니다.

$$
\min_G\max_D\ \mathbb E[\log D(x,y,h)]+\mathbb E[\log(1-D(x,G(x,h),h))]
+\lambda\mathbb E\|y-G(x,h)\|_1.
$$

$$x$$는 mask 또는 mask+thin image, $$y$$는 thick aerial reference, $$h$$는 condition입니다. 위 식은 원문의 CGAN+paired fidelity 개념을 condition notation으로 정리한 설명입니다. 원문의 식 (4) 표기와 objective 구현을 하나의 동일한 reduction convention이라고 가정하지 않습니다. adversarial loss만으로 pixel intensity의 absolute calibration이 유지된다고 볼 수 없어 paired fidelity가 중요합니다.

### Height encoding

Generator bottleneck에는 one-hot height label을 결합합니다. Discriminator에는 원문 식 (5)처럼 ordinal height channel을 줍니다.

$$
p_k=p_{min}+\frac{p_{max}-p_{min}}{m-1}k,\quad k\in\{0,\ldots,m-1\}.
$$

$$p_k$$는 encoding 값으로 optical intensity가 아닙니다. $$m=13$$ height domains에서 one-hot의 index와 실제 nm 값은 별도 mapping입니다. ordinal representation은 height 순서를 보존하지만 one-hot generator가 continuous height extrapolation을 검증했다는 뜻은 아닙니다.

## Proposed Method / Model Architecture

Section 3·Figure 4·Table 1의 encoder는 8 convolution layers, decoder는 8 deconvolution layers와 skip connections입니다. 입력은 200×200, Scheme 1은 1 channel, Scheme 2는 2 channels이며 bottleneck 512 feature에 height label을 결합합니다. discriminator는 convolution 4개와 FC classification으로 pair·height 조건을 검토합니다.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/tempo.svg' | relative_url }}"><img src="{{ '/assets/notes/research/tempo.svg' | relative_url }}" alt="독자 제작: TEMPO의 두 입력 scheme과 공유 encoder, height-conditioned decoder" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">확대 보기 ↗</span></a>
<figcaption>독자 제작 설명도. 원본 Figure 3·4의 복제물이 아니며 generator에 전달되는 height와 input channel의 역할을 요약합니다.</figcaption>
</figure>

Section 4는 shared TEMPO의 trainable parameters를 1.03×10⁸, 13개 individual models의 합을 1.17×10⁹으로 제시합니다. measured peak memory는 확인하지 못했습니다. parameter 수 감소와 실제 inference GPU memory를 같은 수치로 취급하지 않습니다.

Scheme 2의 thin-mask aerial input은 이미 source·pupil의 일부 response를 포함합니다. 따라서 network가 geometry부터 전체 response를 다시 알아낼 필요를 줄일 수 있습니다. 그 대신 thin-mask simulation 비용이 inference 앞에 추가됩니다. Scheme 1 network 호출과 Scheme 2 end-to-end runtime은 같은 단계의 비용이 아닙니다.

**Physics 주입 위치:** height conditioning, Scheme 2의 물리 simulator-derived input, rigorous simulator labels입니다. GAN 자체에 Maxwell equation을 exact constraint로 넣는 PINN 구조는 아닙니다. 학습은 TensorFlow, batch 4, 최대 70 epochs, paired-loss weight 1000이며 13개 individual-model baseline과 비교합니다.

## Figures & Visual Explanation

{% include figure-coverage.html %}

Main Figure 5/5개를 연결했습니다. Table 3도 여러 height의 aerial image와 difference map을 보여주는 visual result로 아래에서 별도 설명합니다. Supplementary 유무는 확인하지 못했습니다.

## Experiments & Results

966 contact clips, contact 60×60 nm, pitch 128 nm, 원래 layout clip 2×2 µm입니다. Calibre로 SRAF·OPC 후 Sentaurus Lithography로 reference를 생성합니다. source는 quasar, wavelength 193 nm, NA 1.2, nonperiodic simulation window는 중심 1.5×1.5 µm입니다. xy pitch 7.5 nm·height pitch 10 nm, 0–120 nm의 13 slices입니다. train/test 75%/25%, runtime test clips 242개, Intel i9 3.3 GHz·TITAN Xp 조건입니다. 별도 validation split은 명시적으로 확인하지 못했습니다.

| 같은 test set · 평균 | Scheme 1 | Scheme 2 | 원문 |
| --- | ---: | ---: | --- |
| NRMSE [%] · TEMPO | 4.23 | 1.79 | Table 2 |
| NRMSE [%] · 13 individual models | 4.63 | 2.27 | Table 2 |
| 중앙 contact CD error X [nm] | 0.72 | 0.38 | Table 4 |
| 중앙 contact CD error Y [nm] | 0.67 | 0.45 | Table 4 |
| 전체 242 clips runtime | 1.1 min | 46.4 min | Table 5 |

Table 5의 rigorous simulation은 20.5 h이고 Scheme 2는 thin-mask simulation 45.3 min + GAN 1.1 min입니다. 표의 Scheme 2 speed ratio는 26.51입니다. abstract의 최대 1170× speedup은 빠른 Scheme 1의 맥락이며 Scheme 2에 붙이면 안 됩니다. 반올림한 1.1 min으로 exact ratio를 복원하지 않습니다.

Table 3의 0/60/120 nm slices는 같은 contact에 대해 reference·두 scheme·difference image를 나란히 배치합니다. intensity 색 막대와 error 색 막대는 다릅니다. 원문은 intensity 약 0.02–0.12, difference 약 0.002–0.008 범례를 사용하므로 두 colormap을 같은 물리량으로 읽지 않습니다. 색상이 비슷해도 equal intensity scale인지 먼저 확인해야 합니다.

CD는 13 slices의 평균 aerial image로 평가한 중앙 contact 지표입니다. full resist chemical profile·모든 contact worst-CD·wafer measurement에 대한 검증으로 확대 해석하지 않습니다.

## Critical Analysis & Limitations

Thickness-aware 조건 모델이라는 장점은 분명하지만 966 contact clips·고정 optical stack이라는 제약을 함께 봐야 합니다. line/space·다른 source·다른 mask material·다른 absorber geometry에 대한 일반화는 별도 문제입니다.

평균 slice image를 통한 CD와 film 내부 profile reconstruction은 다릅니다. threshold-based contour가 실제 3D resist profile을 대신하려면 optical absorption·standing wave·chemistry까지 조건이 맞아야 합니다. Scheme 2가 좋아지는 이유에는 learned architecture뿐 아니라 추가 physical input의 정보량이 있습니다.

GAN이 평활하고 그럴듯한 image를 내더라도 rare high-error contact를 놓칠 수 있습니다. maximum CD·tail distribution을 함께 평가해야 합니다. Figure 5 histogram은 이를 읽는 출발점입니다.

## Practical Applications to GeoSignal / OPC

* **당장 적용 가능한 아이디어:** cheap physical output을 surrogate input으로 보존하고 학습·추론 비용을 분리하는 비교 설계를 사용합니다.
* **추가 연구 / Hypothesis:** Abbe reference와 별도 thick-mask reference의 차이를 학습하는 correction model을 탐색할 수 있습니다. 현재 GeoSignal에는 mask topography reference·film 내부 propagation이 없습니다.
* **장기 / Hypothesis:** mask-stack·source·film height 조건 모델을 확장하고 vector/3D physics에 맞는 dataset을 구축합니다. focus sweep과 height slice를 구분합니다.

## Key Takeaways & References

1. 실험은 193 nm DUV이며 EUV 실험이라고 쓰지 않습니다.
2. Film height는 scanner defocus가 아닙니다.
3. Scheme 2는 thin-mask input의 정보와 비용을 모두 포함합니다.
4. One model이 height마다 공유하는 것이 핵심입니다.
5. CD는 중앙 contact와 평균 slice 기준입니다.
6. 1170×와 26.51×는 서로 다른 scheme의 비교입니다.

[Abbe Imaging]({{ '/ko/notes/abbe-imaging/' | relative_url }}) · [Nitho]({{ '/ko/notes/research/nitho/' | relative_url }}) · [GeoSignal 범위]({{ '/ko/notes/research/geosignal-scope/' | relative_url }})
