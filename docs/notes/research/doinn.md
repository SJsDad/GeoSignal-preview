---
layout: technical
category: research
paper_id: doinn
title: "DOINN — global Fourier와 local CNN을 분리하는 이유"
permalink: /ko/notes/research/doinn/
lang: ko
---

# DOINN: global Fourier와 local CNN을 분리하는 이유

* 목차
{:toc}

<div class="evidence-note">arXiv v1 PDF·HTML 본문, Figures 1–9, Tables 1–4, Appendix A.1–A.2를 확인했습니다. DOI는 arXiv DOI와 학회 DOI를 구분합니다. 이미지 재사용 license는 arXiv의 게시 허가와 별개이므로 원본 Figure를 복제하지 않습니다.</div>

## Paper Information

| 항목 | 확인 내용 |
| --- | --- |
| 정식 제목 | Generic Lithography Modeling with Dual-band Optics-Inspired Neural Networks |
| 저자 | Haoyu Yang, Zongyi Li, Kumara Sastry, Saumyadip Mukhopadhyay, Mark Kilgard, Anima Anandkumar, Brucek Khailany, Vivek Singh, Haoxing Ren |
| 소속 | NVIDIA; Zongyi Li·Anima Anandkumar는 California Institute of Technology도 병기 |
| 발표 | DAC 2022; arXiv record의 accepted at 59th DAC 확인 |
| 원문 | [arXiv](https://arxiv.org/abs/2203.08616) · [v1 PDF](https://arxiv.org/pdf/2203.08616v1) · [v1 HTML](https://arxiv.org/html/2203.08616v1) · [arXiv DOI](https://doi.org/10.48550/arXiv.2203.08616) |
| 공식 코드·weights | 원 저자 구현 공개 미확인. LithoBench DOINN 구현은 benchmark 구현이며 저자 코드와 동일하다고 주장하지 않음 |
| 데이터·분야 | ISPD 2019·ICCAD 2013·N14; forward resist/contour simulation |

## Executive Summary

**한 문장:** 저주파 global structure는 한 번의 optimized Fourier branch로, 고주파 edge detail은 CNN branch로 처리해 high-resolution contour를 재구성합니다.

Optics의 nonlocal response를 모델링하려면 멀리 있는 geometry context가 필요하지만 2000×2000 image의 여러 latent channel에 FFT를 반복하는 비용도 큽니다. DOINN은 Fourier branch를 줄이고 local branch를 보완적으로 둡니다. 핵심은 “dual-band = 광원의 파장이 두 개”가 아니라 **정보의 global/local frequency 역할 분담**입니다.

## Background & Motivation

작은 convolution kernel은 edge를 잘 표현하지만 optical influence를 넓게 보려면 깊은 network·dilation 등이 필요합니다. FNO는 global interaction을 직접 다루지만 image size와 feature channels에 FFT cost가 커집니다. coarse global path만 쓰면 edge 위치·narrow gap·via size를 복원하기 어렵습니다.

따라서 global context는 downsampled input에서 얻고, local CNN은 잃어버린 detail을 보완합니다. 이 구조가 physically exact SOCS인지 또는 optical computation과 닮은 learned approximation인지는 구분해야 합니다.

## Physics & Mathematical Foundations

### SOCS와 optimized Fourier branch

[Hopkins/TCC/SOCS]({{ '/ko/notes/foundations/hopkins-tcc-socs/' | relative_url }})에서 field synthesis는 FFT → kernel product → IFFT이고 intensity는 mode별 absolute square 합입니다. DOINN의 reduced Fourier computation은 원문 식 (11)의 개념으로

$$
V=\rho\left(\mathcal F^{-1}\left[(\mathcal F(A))_{low}\,W_P\,W_R\right]\right)
$$

라 쓸 수 있습니다. $$A$$는 single-channel input, $$W_P$$는 channel lifting, $$W_R$$은 learned complex spectral weight입니다. 이 표기에서 channel projection과 frequency interaction을 matrix product로 요약했으며 원문의 convolution 표기와 exact tensor implementation을 동일시하지 않습니다.

중요한 비용 차이는 **채널을 늘리기 전에 single-channel FFT를 한다**는 점입니다. $$B\times1\times H\times W$$에서 FFT를 한 뒤 low-mode feature를 $$C$$ channels로 lift할 수 있습니다. 일반적인 repeated FNO block의 $$C$$ FFT를 줄이는 방향입니다. output IFFT·local convolution·reconstruction 비용은 여전히 존재합니다.

### Frequency index와 physical support — 독자적 계산

Mode 간격은 $$\Delta f=1/L$$입니다. 학습 tile의 폭 $$L$$에서 lowest $$k$$ modes를 유지하면 최대 represented frequency는 대략 $$k/L$$입니다. 폭 $$4L$$의 큰 image에 같은 $$k$$를 쓰면 physical support가 약 1/4이 됩니다. nominally arbitrary input shape를 받아도 물리적으로 같은 function을 계산하는 것이 아닙니다.

이것이 DOINN이 large tile에서 tile-sized global features를 만들어 합치는 이유입니다. [FFT note]({{ '/ko/notes/fourier-optics/' | relative_url }})의 sampling·halo 설명과 연결됩니다.

## Proposed Method / Model Architecture

Section 3·Figure 4는 Global Perception(GP), Local Perception(LP), Image Reconstruction(IR)으로 나뉩니다. GP는 pooled image와 한 optimized Fourier unit, LP는 stacked VGG blocks, IR은 concatenated features를 transposed convolution과 refinement convolution으로 원래 해상도에 복원합니다.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/doinn.svg' | relative_url }}"><img src="{{ '/assets/notes/research/doinn.svg' | relative_url }}" alt="독자 제작: DOINN의 global Fourier branch, local CNN branch, contour reconstruction" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">확대 보기 ↗</span></a>
<figcaption>독자 제작 연산 흐름도. 원본 Figure 4의 복제물이 아니며 exact Appendix layer dimensions는 원문으로 연결합니다.</figcaption>
</figure>

Appendix A.1의 대표 설정은 2048×2048 grid에서 GP average pooling → 256×256×1, real FFT → 256×129×1, lifting → 16 channels, first 50×50 coefficients 유지, inverse FFT → 256×256×16입니다. LP도 4→8→16 channels와 /2·/4·/8 downsampling을 거칩니다. IR에서 GP/LP concat 32 channels를 시작으로, local bypass를 합치며 transposed convolution으로 원래 grid로 복원합니다. 본문 2000×2000 evaluation 설명과 Appendix 2048 grid의 차이는 padding policy를 재현할 때 확인해야 합니다.

Appendix A.2는 A100·PyTorch 1.9, MSE loss·Adam, 초기 learning rate 0.002, batch 16, 최대 10 epochs, 2 epochs마다 0.5 decay, weight decay 0.0001을 명시합니다. 이 설정은 후속 LithoBench 구현의 default와 구분합니다.

GP output의 표현 shape는 $$C\times H/8\times W/8$$입니다. Appendix A.1–A.2에서 stage별 Conv/GP/IR 설정을 확인할 수 있습니다. 리뷰의 diagram은 채널 수를 임의로 확정하지 않습니다.

Section 3.2·Figure 5의 large-tile flow는 training-sized clips를 half-overlap으로 만들고 valid core를 합칩니다. full-chip을 통째로 한번에 inference했다는 뜻은 아닙니다. Fourier feature의 physical support와 optical halo를 유지하려는 방식입니다.

**Physics 주입 위치:** optical FFT pipeline과 유사한 architecture prior입니다. learned features·nonlinearity·spectral truncation은 정확한 pupil·SOCS constraint가 아니며 optical PDE residual loss를 강제하지 않습니다. 본문은 supervised mask/resist pairs로 학습하고 MSE 관련 설정을 Appendix A.2에 둡니다. LithoBench의 후속 inverse variant를 원논문 forward method와 혼동하지 않습니다.

## Figures & Visual Explanation

{% include figure-coverage.html %}

Main Figures 9/9개를 연결했습니다. Appendix A.1의 layer tables와 A.2의 설정은 같은 arXiv 문서 안의 보충 설명입니다. Figure 9의 그림 label은 DOINN-FS, Table 4의 large-tile method는 DOINN-LT로 표기돼 있어 이름 차이를 그대로 기록합니다.

## Experiments & Results

Table 1과 Section 4.1은 ISPD 2019 via·ICCAD 2013 metal·N14 via를 구분합니다. L은 1000×1000, H는 2000×2000의 4 µm² tiles입니다. 같은 면적이라도 pixel 면적·공간 sampling이 다르므로 L/H 수치를 무조건 합쳐 평균내지 않습니다.

| Table 2 · mIoU [%] | UNet | DAMO-DLS | DOINN |
| --- | ---: | ---: | ---: |
| ISPD-2019 (L) | 98.03 | 98.11 | 98.27 |
| ICCAD-2013 (L) | 95.38 | 96.97 | 97.79 |
| ICCAD-2013 (H) | 93.04 | 미지원 | 97.77 |
| N14 | 91.64 | 미지원 | 96.49 |

Table 3의 ICCAD-2013(L) ablation은 GP only 96.09 → GP+IR 97.20 → GP+IR+LP 97.60 → full bypass 97.79 mIoU입니다. local branch를 추가하는 이유를 정량적으로 읽을 수 있지만 final CD/EPE가 어떤 spec을 만족하는지는 별도 평가가 필요합니다.

Table 4에서 ISPD-2019-LT의 default DOINN mIoU 92.03%, DOINN-LT 98.23%입니다. 실험은 training 4 µm² tile, test 64 µm² via tiles 10개이며 full-chip hardware capacity를 검증한 것이 아닙니다.

Figure 6의 throughput 단위는 µm²/s이며 x축은 training epochs입니다. 본문은 1.3M parameters와 DAMO-DLS 18M을 병기하면서 약 20× smaller라는 문구도 사용합니다. **독자 계산으로 18/1.3≈13.8**이므로 이 두 수치를 exact 20×로 일치시켜 쓰지 않습니다. Figure 6의 reference simulator 대비 speedup은 원문 초록에서 85×로 제시되지만 hardware·tile·accuracy 조건을 함께 확인해야 합니다.

Table 1의 train/test 수는 ICCAD 4,875/10, ISPD 10,300/11,641, N14 1,630/137입니다. 본문은 N14에서 1.6K clips 중 100 densest를 평가한다고도 설명하므로 표와 서술의 정확한 split 차이는 재현 시 확인해야 합니다. validation 분리·seed는 미확인입니다.

Source/NA/wavelength의 전체 setting, split seed·validation definition, measured peak memory와 process-window conditions는 본 리뷰에서 완전히 검증하지 못했습니다. 새 process-condition generalization의 근거로 이 표를 쓰지 않습니다.

## Critical Analysis & Limitations

Global/local 역할 분담은 계산 효율과 contour detail의 균형을 겨냥합니다. 하지만 low-frequency feature가 aerial image처럼 보인다고 hidden feature가 물리적인 coherent field라고 확정할 수 없습니다. Feature visualization은 해석의 단서이며 constraint 증명은 아닙니다.

Large tile 처리에서 halo가 충분하지 않으면 tile boundary response가 틀립니다. 또한 training data가 OPC된 masks에 집중되면 초기 uncorrected mask로 inverse loop를 시작할 때 입력 분포가 달라집니다. Figure 8은 24 OPC iterations의 perturbation response를 비교하지만 모든 optimizer trajectory를 검증하지 않습니다.

무차원 image IoU는 critical edge 또는 rare bridge를 과소평가할 수 있습니다. 상용 OPC에 쓰려면 gauge별 error tail·source/focus variation·binarization·worst-region 평가가 추가돼야 합니다.

## Practical Applications to GeoSignal / OPC

* Global/local 표현은 넓은 맥락과 모서리 세부를 함께 연구하는 관점을 제공합니다.
* 선택 예시와 처리량만으로 공정 정합성을 확정할 수는 없습니다.

현재 공개 기능은 [GeoSignal 적용 범위]({{ '/ko/notes/research/geosignal-scope/' | relative_url }})에 정리했습니다. 이 항목들은 연구 맥락이며 구현 완료를 뜻하지 않습니다.

## Key Takeaways & References

1. Dual-band는 global/local information 구분입니다.
2. FFT를 channel lifting 전에 수행하는 것이 주요 비용 절감 아이디어입니다.
3. Fourier mode index의 물리적 의미는 tile 크기에 의존합니다.
4. Arbitrary tensor size와 arbitrary physical-domain generalization은 다릅니다.
5. Feature visualization은 물리 정합성 증명이 아닙니다.
6. Parameters·model bytes·throughput는 단위가 다른 지표입니다.

[Fourier Optics]({{ '/ko/notes/fourier-optics/' | relative_url }}) · [Nitho]({{ '/ko/notes/research/nitho/' | relative_url }}) · [LMLitho]({{ '/ko/notes/research/lmlitho/' | relative_url }}) · [LithoBench](https://github.com/shelljane/lithobench)
