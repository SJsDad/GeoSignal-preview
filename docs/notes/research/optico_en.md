---
layout: technical
category: research
paper_id: optico
title: "OptiCo — Why Put Diffraction Phase into Convolution?"
permalink: /notes/research/optico/
lang: en
---

# OptiCo: Why Put Diffraction Phase into Convolution?

* Contents
{:toc}

<div class="evidence-note">Partial review. Verified CVF metadata and indexed official-PDF passages covering equations (6)–(15), Tables 1–5 and references to Figures 1–6. Direct PDF access returned 403; the supplement, full figure inventory and visual details remain unverified. Derivations and critical interpretations below are independent explanations.</div>

## Paper Information

| Item | Verified information |
| --- | --- |
| Title | Optical Diffraction-based Convolution for Semiconductor Lithography |
| Authors/affiliations | Young-Han Son, Dong-Hee Shin, Deok-Joong Lee, Hyun Jung Lee, Tae-Eui Kam; Korea University, with Dong-Hee Shin at Yonsei University, according to indexed first-page text |
| Publication | CVPR 2026, pp. 12458–12468 |
| Sources | [Official CVF page](https://openaccess.thecvf.com/content/CVPR2026/html/Son_Optical_Diffraction-based_Convolution_for_Semiconductor_Lithography_CVPR_2026_paper.html) · [Official PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Son_Optical_Diffraction-based_Convolution_for_Semiconductor_Lithography_CVPR_2026_paper.pdf) |
| DOI/code/weights | Not verified. Unrelated repositories named OptiCo are not presented as official code |
| Data/tasks | LithoBench; ILT mask optimization and forward aerial/resist simulation |

## Executive Summary

**One sentence:** couple complex diffraction-phase structure to learned convolutions as an inductive bias for generating masks from targets.

The model embeds a computation in which spatial contributions can reinforce or cancel by phase, rather than memorizing only corner/assist patterns. The key question is **which physical forms the learned kernel is encouraged to prefer**, beyond whether it uses FFTs. This can improve CNN optical-interaction representations without guaranteeing a scanner model or manufacturable SRAFs. Read MSE/EPE and PVB gains separately.

## Background & Motivation

CNNs learn local correlations without explicit field phase. FNOs support global frequency interactions but do not automatically constrain learned weights to pupils or propagation. An Optical Phase (OP) kernel addresses that distinction. Small mask changes can affect distant edges, making a physical prior useful for OOD via arrays; learned propagation scale is still not a calibrated lens distance or wafer focus.

## Physics & Mathematical Foundations

### Why Fresnel phase is quadratic — independent derivation

For transverse distance $$r_\perp$$ small relative to propagation distance $$z$$,

$$
R=\sqrt{z^2+r_\perp^2}\simeq z+\frac{r_\perp^2}{2z}.
$$

Substitution in $$e^{ikR}$$ separates global phase $$e^{ikz}$$ from quadratic phase $$e^{ik r_\perp^2/(2z)}$$. A homogeneous scalar paraxial example is

$$
h_z(x,y)=\frac{e^{ikz}}{i\lambda z}\exp\!\left[\frac{ik}{2z}(x^2+y^2)\right],\qquad E_z=h_z*E_0.
$$

$$k=2\pi/\lambda$$ is in µm⁻¹ and lengths in µm, making the exponent dimensionless. Kernel units µm⁻² preserve amplitude units after area integration. This background formula does not model all high-NA, finite-pupil, partial-coherence and mask-3D scanner effects. Read [Fourier convolution]({{ '/notes/fourier-optics/' | relative_url }}) with [Abbe source sums]({{ '/notes/abbe-imaging/' | relative_url }}) to distinguish a **single complex propagation prior** from a **complete partially coherent system**.

### The role of complex convolution

For $$U=U_r+iU_i$$ and $$W=W_r+iW_i$$, real/imaginary cross terms follow the [complex-layer calculation]({{ '/notes/fourier-optics/' | relative_url }}). Magnitudes alone lose destructive-interference information. Calling complex features electric fields additionally requires matching normalization, boundaries and source summation.

## Proposed Method / Model Architecture

Indexed equations (6)–(12) combine OP kernel $$Q$$ with learned weights, complex convolution and residual backbone fusion:

$$
W_{eff}=Q\odot W\quad\text{or}\quad W_{eff}=\lambda_\alpha Q.
$$

The first permits location-specific freedom; the second restricts kernel shape through scalar scaling. Free complex $$W$$ can even cancel $$Q$$'s phase prior. A useful learning bias therefore differs from a strict propagation constraint.

Inverse flow maps target → mask; forward tasks map mask → aerial/resist. MetaNeXt features, an OP complex branch and per-pixel complex channel projection are combined. A conceptual latent shape is $$B\times C\times H\times W$$; stage channels, depths and strides remain unverified without the supplement.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/optico.svg' | relative_url }}"><img src="{{ '/assets/notes/research/optico.svg' | relative_url }}" alt="Independent explanation of the optical-phase branch and residual feature fusion in OptiCo" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">Enlarge ↗</span></a>
<figcaption>An original explanation, not a reproduction of Figure 2; exact layers and channel counts are omitted. Click to enlarge.</figcaption>
</figure>

Equations (13)–(15) add TV regularization to squared simulated-resist/target discrepancy. A generic TV form is

$$
\Omega_{TV}(M)=\sum_{p,q}\left(|M_{p+1,q}-M_{p,q}|+|M_{p,q+1}-M_{p,q}|\right).
$$

TV suppresses grainy differences but does not exactly encode minimum width/space, fracturing or nonprinting SRAFs. A high TV weight can remove useful small assists. **Physics entry point:** complex-kernel parameterization and phase modulation in layers. TV is manufacturing regularization, not an optical governing-equation residual. Schedule, optimizer, wavefront scales and inference runtime remain unverified pending Appendix E.2 access.

## Figures & Visual Explanation

Read full captions/images at the official PDF. Summaries below paraphrase available descriptions while leaving unseen axes, colors and subfigures unverified. This is a **verified minimum inventory**, not complete coverage.

{% include figure-coverage.html %}

## Experiments & Results

Indexed Section 4/Table 1 covers LithoBench MetalSet/ViaSet and StdMetal/StdContact OOD tasks at 2048×2048 with 1 nm² pixels. These are **values within Table 1's protocol**:

| Evaluation/metric | ILILT | OptiCo | Interpretation |
| --- | ---: | ---: | --- |
| StdContact OOD · Reported MSE | 38,957 | 18,474 | Not on the normalized forward-MSE scale |
| StdContact OOD · Mean EPE violations | 7.1 | 0.1 | Counts, not EPE distance in nm |
| StdContact OOD · Reported PVB | 43,869 | 39,181 | Requires corner and pixel-scaling checks |
| Four-subtask mean · Reported MSE | 22,143 | 14,535 | Aggregated within the same table |
| Four-subtask mean · Reported PVB | 31,064 | 29,373 | Does not beat every baseline |

DOINN's mean PVB is 23,370, below OptiCo. **OptiCo is not best on every metric.** Table 2 forward StdContact aerial MSE is DOINN 2.72×10⁻⁵ versus OptiCo 1.01×10⁻⁵, with IoU 0.89/0.90. These normalized forward values differ from the large inverse-table MSE values.

Tables 3–5 ablate diffraction formulations, strict kernels and OP/MC/CC components. Follow actual variant definitions; kernel modifications do not alone validate high-NA scanner fidelity. Complete NA, wavelength, process corners, splits, parameters, memory and runtime remain unverified. Apply the [metric normalization checks]({{ '/notes/foundations/inverse-and-metrics/' | relative_url }}).

## Critical Analysis & Limitations

**Verified:** explicit optical phase in convolutions and OOD mask evaluation. **Author claim:** diffraction priors help generalization. **Independent interpretation:** helpful priors do not guarantee overall physical consistency.

Paraxial assumptions, finite support, feature-space scale, binarization and source variation introduce distinct errors. Larger kernels broaden context but can undersample rapidly oscillating quadratic phase or destabilize learning. Separate propagation error from training instability. Visible mask rings do not establish manufacturability: check SRAF printability, MRC and focus/dose reference reevaluation. Partial evidence does not justify stronger industrial validation claims.

## Practical Applications to GeoSignal / OPC

* **Available idea:** evaluate corner/SRAF error maps alongside Abbe outputs, following [verified scope]({{ '/notes/research/geosignal-scope/' | relative_url }}).
* **Further research / Hypothesis:** compare real, complex and OP-constrained branches on one backbone; separate aerial and contour errors and investigate conditioning on high NA/source variation.
* **Long term / Hypothesis:** combine geometry rules and process-conditioned optical priors. This is not a currently implemented automatic OPC/SRAF feature.

## Key Takeaways & References

1. Complex arithmetic, FFTs and optical priors are distinct choices.
2. OP kernels with free weights differ from strict physical propagation.
3. TV does not replace mask rules.
4. EPE violation counts differ from EPE in nm.
5. Shape OOD is not new-process generalization.
6. Key formulas concern phase, effective kernels, complex products and TV.

[Foundations]({{ '/notes/foundations/' | relative_url }}) · [Nitho]({{ '/notes/research/nitho/' | relative_url }}) · [DOINN]({{ '/notes/research/doinn/' | relative_url }}) · [LithoBench](https://github.com/shelljane/lithobench)
