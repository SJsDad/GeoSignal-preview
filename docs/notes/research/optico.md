---
layout: technical
category: research
paper_id: optico
title: "OptiCo — 회절 위상을 convolution에 넣는 이유"
permalink: /ko/notes/research/optico/
lang: ko
---

# OptiCo: 회절 위상을 convolution에 넣는 이유

* 목차
{:toc}

<div class="evidence-note">부분 리뷰. CVF의 공식 서지정보와 공식 PDF의 색인 본문에서 식 (6)–(15), Tables 1–5, Figures 1–6 관련 내용을 확인했습니다. PDF 직접 열람은 403 응답으로 제한됐고 보충자료·전체 Figure 목록·시각적 세부사항은 검증하지 못했습니다. 아래 이론 유도와 비판적 해석은 독자적 설명입니다.</div>

## Paper Information

| 항목 | 확인 내용 |
| --- | --- |
| 정식 제목 | Optical Diffraction-based Convolution for Semiconductor Lithography |
| 저자·소속 | Young-Han Son, Dong-Hee Shin, Deok-Joong Lee, Hyun Jung Lee, Tae-Eui Kam. Korea University; Dong-Hee Shin은 Yonsei University. 공식 PDF 첫 페이지 색인 기준 |
| 발표 | CVPR 2026, pp. 12458–12468 |
| 원문 | [CVF 공식 페이지](https://openaccess.thecvf.com/content/CVPR2026/html/Son_Optical_Diffraction-based_Convolution_for_Semiconductor_Lithography_CVPR_2026_paper.html) · [공식 PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Son_Optical_Diffraction-based_Convolution_for_Semiconductor_Lithography_CVPR_2026_paper.pdf) |
| DOI·공식 코드·학습 weights | 확인하지 못함. 이름이 같은 다른 분야의 OptiCo 저장소를 공식 코드로 연결하지 않음 |
| 데이터·분야 | LithoBench 사용; ILT mask optimization과 forward aerial/resist simulation |

## Executive Summary

**한 문장:** 회절 전파의 복소 위상 구조를 학습 convolution에 결합해, target에서 mask를 생성할 때 활용하는 inductive bias를 만드는 연구입니다.

어떤 corner나 assist feature를 고칠지 데이터만으로 외우는 대신, 서로 다른 위치의 기여가 위상에 따라 강화·상쇄될 수 있다는 연산 구조를 feature 내부에 넣습니다. 핵심 질문은 FFT 사용 여부보다 **학습 kernel이 어떤 물리 형태를 선호하도록 설계됐는가**입니다.

실무적으로는 기존 CNN의 optical interaction 표현을 개선하는 방법을 배울 수 있습니다. 실제 scanner model 또는 제조 가능한 SRAF를 자동으로 보장하는 알고리즘으로 해석할 근거는 부족합니다. 성능표에서 MSE·EPE 개선과 PVB 개선은 별도로 읽어야 합니다.

## Background & Motivation

일반 CNN은 local correlation을 학습하지만 전계 phase를 명시적으로 다루지 않습니다. FNO는 global frequency interaction을 다룰 수 있으나 learned spectral weight가 실제 pupil 또는 diffraction propagation에 해당한다는 제약은 별개입니다. OP(Optical Phase) kernel은 이 차이를 줄이려는 구조적 선택입니다.

Inverse mask 설계에서는 작은 픽셀 변화가 멀리 떨어진 edge의 intensity에 영향을 줄 수 있습니다. 학습 분포 밖의 via 배열에 대해 단순한 local pattern memorization이 실패한다면 물리적인 연산 prior가 도움이 될 수 있습니다. 그렇더라도 학습 전파 scale을 실제 lens 거리나 wafer focus 값이라고 읽으면 안 됩니다.

## Physics & Mathematical Foundations

### Fresnel phase가 quadratic인 이유 — 독자적 유도

두 점의 횡방향 거리 $$r_\perp$$가 propagation distance $$z$$보다 작으면 경로 길이는

$$
R=\sqrt{z^2+r_\perp^2}\simeq z+\frac{r_\perp^2}{2z}.
$$

$$e^{ikR}$$에 대입하면 global phase $$e^{ikz}$$와 quadratic phase $$e^{ik r_\perp^2/(2z)}$$가 분리됩니다. 균질 매질의 scalar paraxial 예시는

$$
h_z(x,y)=\frac{e^{ikz}}{i\lambda z}\exp\!\left[\frac{ik}{2z}(x^2+y^2)\right],\qquad E_z=h_z*E_0.
$$

$$k=2\pi/\lambda$$ [µm⁻¹], $$x,y,z,\lambda$$ [µm]이며 지수는 무차원입니다. $$h_z$$는 µm⁻² 차원을 가지므로 면적 적분 뒤 $$E_0$$와 같은 amplitude 차원을 얻습니다. 이는 이론 설명용 식입니다. 고 NA imaging·finite pupil·partial coherence·mask 3D 효과를 모두 포함한 정확한 scanner 모델은 아닙니다.

[Fourier Optics]({{ '/ko/notes/fourier-optics/' | relative_url }})의 convolution theorem과 [Abbe]({{ '/ko/notes/abbe-imaging/' | relative_url }})의 source별 intensity sum을 함께 읽으면, **single complex propagation prior**와 **전체 partially coherent imaging system**을 구분할 수 있습니다.

### Complex convolution의 역할

$$U=U_r+iU_i$$, $$W=W_r+iW_i$$일 때 실수·허수 cross term은 [복소수 layer 계산]({{ '/ko/notes/fourier-optics/' | relative_url }})과 같습니다. amplitude magnitude만 처리하면 destructive interference의 정보가 손실됩니다. 다만 complex feature가 실제 electric field라고 주장하려면 normalization·boundary condition·source summation도 맞아야 합니다.

## Proposed Method / Model Architecture

공식 색인 본문의 식 (6)–(12)는 OP kernel $$Q$$와 학습 weight의 결합, complex convolution, backbone feature와의 residual fusion을 명시합니다.

$$
W_{eff}=Q\odot W\quad\text{또는}\quad W_{eff}=\lambda_\alpha Q.
$$

첫 형태는 위치별 자유도를 많이 허용하고, 두 번째는 kernel 형태를 scalar scaling으로 더 강하게 제한합니다. 따라서 “물리를 넣었다”는 말의 강도도 다릅니다. 자유로운 complex $$W$$는 $$Q$$의 phase prior를 상쇄할 수도 있습니다. 학습에 유용한 inductive bias와 strict physical constraint는 분리해서 평가해야 합니다.

데이터 흐름은 target → mask network이며, forward task에서는 mask → aerial/resist output입니다. MetaNeXt backbone·OP complex branch·per-pixel complex channel projection을 조합합니다. 복소 latent tensor의 개념적 shape를 $$B\times C\times H\times W$$로 쓸 수 있지만, stage별 channel·depth·stride는 보충자료를 확인하지 못해 확정하지 않습니다.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/optico.svg' | relative_url }}"><img src="{{ '/assets/notes/research/optico.svg' | relative_url }}" alt="독자 제작: OptiCo의 optical phase branch와 residual feature fusion" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">확대 보기 ↗</span></a>
<figcaption>독자 제작 설명도. 원본 Figure 2의 복제물이 아니며 정확한 layer 배치·channel dimension은 생략했습니다. 클릭해 확대합니다.</figcaption>
</figure>

식 (13)–(15)는 simulated resist와 target 사이의 squared discrepancy에 TV regularization을 더합니다. TV의 일반적인 형태는

$$
\Omega_{TV}(M)=\sum_{p,q}\left(|M_{p+1,q}-M_{p,q}|+|M_{p,q+1}-M_{p,q}|\right).
$$

TV는 픽셀 방향 차이를 줄여 grainy artifact를 억제합니다. 하지만 minimum width·space·shot fracturing·SRAF 비인쇄 제약을 정확히 표현하는 loss는 아닙니다. TV weight를 키우면 작은 유용한 assist feature가 사라질 수 있습니다.

**Physics-Informed 위치:** layer의 complex kernel parameterization과 phase modulation입니다. Loss의 TV는 제조 정규화이며 optical governing-equation residual은 아닙니다. 학습 schedule·optimizer·wavefront scale 수치·추론 runtime은 Appendix E.2 직접 열람 전까지 미확인입니다.

## Figures & Visual Explanation

원문 caption 전문과 그림은 공식 PDF 링크에서 확인합니다. 아래 caption 요지는 원문 설명을 간단히 바꾸어 적었으며, 직접 볼 수 없었던 axis·색상·subfigure 세부는 미확인으로 남깁니다. 현재 Figure 목록은 **확인된 최소 목록**으로, full coverage 완료를 뜻하지 않습니다.

{% include figure-coverage.html %}

## Experiments & Results

공식 PDF 색인 Section 4·Table 1에서 LithoBench의 MetalSet/ViaSet 및 StdMetal/StdContact OOD 평가를 확인했습니다. 원문의 해상도는 2048×2048, pixel 면적은 1 nm²입니다. 다음은 **Table 1의 같은 protocol 안의 수치**입니다.

| 평가·지표 | ILILT | OptiCo | 해석 |
| --- | ---: | ---: | --- |
| StdContact OOD · MSE 표기값 | 38,957 | 18,474 | normalized forward MSE와 같은 scale로 비교하지 않음 |
| StdContact OOD · EPE violation 평균 count | 7.1 | 0.1 | EPE distance [nm]가 아님 |
| StdContact OOD · PVB 표기값 | 43,869 | 39,181 | 공정 조건·pixel scaling을 함께 확인해야 함 |
| 4개 subtask 평균 · MSE 표기값 | 22,143 | 14,535 | 같은 표의 집계 |
| 4개 subtask 평균 · PVB 표기값 | 31,064 | 29,373 | 모든 baseline보다 낮다는 뜻은 아님 |

Table 1에서 DOINN 평균 PVB는 23,370으로 OptiCo보다 낮습니다. **OptiCo가 모든 지표에서 최상이라고 쓰지 않습니다.** Table 2의 forward StdContact aerial MSE는 DOINN 2.72×10⁻⁵, OptiCo 1.01×10⁻⁵이고 IoU는 0.89/0.90입니다. inverse 표의 큰 MSE 값과 forward normalized MSE 값을 같은 scale로 보지 않습니다.

Tables 3–5는 diffraction formulation·strict kernel·OP/MC/CC 요소를 제거하는 ablation입니다. 정확한 비교를 위해 원문 표의 variant 정의를 따라야 하며, kernel 수식을 바꿨다는 사실만으로 실제 high-NA scanner 조건의 보존을 검증했다고 결론내리지 않습니다.

NA·wavelength·process corner·train/validation/test split·parameter count·memory·runtime의 완전한 설정은 미확인입니다. [지표 문서]({{ '/ko/notes/foundations/inverse-and-metrics/' | relative_url }})의 normalization 확인 규칙을 적용해야 합니다.

## Critical Analysis & Limitations

**확인 사실:** 광학 phase를 convolution에 명시적으로 결합하고 OOD mask task를 평가합니다. **저자 주장:** explicit diffraction prior가 generalization에 도움이 됩니다. **독자적 분석:** kernel prior가 유용해도 physical consistency 전체를 보장하는 것은 아닙니다.

Fresnel의 paraxial 조건, finite-support kernel, feature-space scale, mask binarization, source variation은 각기 다른 오차 요인입니다. kernel 규모를 크게 하면 receptive field는 넓어지지만 quadratic phase sampling이 빠르게 진동해 optimization이 어려워질 수 있습니다. 이것이 actual field propagation error인지 neural training instability인지 분리하는 검증이 필요합니다.

실무 mask는 “ring이 뚜렷하다”는 시각적 특징으로 승인할 수 없습니다. simulated SRAF printability와 MRC를 검사하고 dose/focus 조건별 reference 재평가를 해야 합니다. 부분 본문 확인 상태에서 산업 적용의 검증 수준을 높여 주장하지 않습니다.

## Practical Applications to GeoSignal / OPC

* **당장 적용 가능한 아이디어:** 기존 Abbe output으로 corner/SRAF 주변의 error map을 함께 보는 평가 schema를 설계합니다. 구현 범위는 [GeoSignal 코드 확인]({{ '/ko/notes/research/geosignal-scope/' | relative_url }})을 따릅니다.
* **추가 연구 / Hypothesis:** 동일 backbone에서 real·complex·OP-constrained branch를 비교하고 aerial error와 contour error를 나눠 측정합니다. 고 NA 또는 source variation을 실제 input으로 조건화할지 별도 검토합니다.
* **장기 / Hypothesis:** 제조 rule을 포함한 geometry parameterization과 process-conditioned optical prior를 결합합니다. 현재 GeoSignal의 자동 OPC·SRAF 기능으로 소개하지 않습니다.

## Key Takeaways & References

1. Complex arithmetic, FFT, optical prior는 각각 다른 설계 요소입니다.
2. OP kernel과 자유로운 weight의 결합은 strict physical propagation과 다릅니다.
3. TV는 mask rules를 대신하지 않습니다.
4. EPE violation count와 EPE [nm]는 비교할 수 없습니다.
5. OOD mask shape 성능을 새 공정 generalization으로 확대 해석하지 않습니다.
6. 주요 식은 diffraction phase·effective kernel·complex product·TV입니다.

[Foundations Overview]({{ '/ko/notes/foundations/' | relative_url }}) · [Nitho 비교]({{ '/ko/notes/research/nitho/' | relative_url }}) · [DOINN 비교]({{ '/ko/notes/research/doinn/' | relative_url }}) · [LithoBench](https://github.com/shelljane/lithobench)
