---
layout: technical
category: research
paper_id: tokman
title: "TokMan — Token-Based Inverse Design with Manhattan Geometry"
permalink: /notes/research/tokman/
lang: en
---

# TokMan: Token-Based Inverse Design with Manhattan Geometry

* Contents
{:toc}

<div class="evidence-note">Partial review. Verified NeurIPS metadata/abstract and indexed official-PDF passages for Sections 4–5, Table 1 and Figures 1–6. The approximately 15.5 MB PDF exceeded the reading tool's size limit; the supplemental ZIP was not parsed. Complete figures, subfigures, visual details and appendices remain unverified.</div>

## Paper Information

| Item | Verified information |
| --- | --- |
| Title | TokMan:Tokenize Manhattan Mask Optimization for Inverse Lithography |
| Authors | Yiwen Wu, Yuyang Chen, Ye Xia, Yao Zhao, Jingya Wang, Xuming He, Hao Geng, Jingyi Yu |
| Affiliations | ShanghaiTech-related author listings and partial first-page text checked; complete mapping unverified |
| Publication | Advances in Neural Information Processing Systems 38, NeurIPS 2025 |
| Sources | [Official page](https://proceedings.nips.cc/paper_files/paper/2025/hash/4e127d4fb92a3145ecb60f6aa0b16eef-Abstract-Conference.html) · [DOI](https://doi.org/10.52202/085713-1807) · [PDF](https://proceedings.nips.cc/paper_files/paper/2025/file/4e127d4fb92a3145ecb60f6aa0b16eef-Paper-Conference.pdf) |
| Supplement | [ZIP](https://proceedings.nips.cc/paper_files/paper/2025/file/4e127d4fb92a3145ecb60f6aa0b16eef-Supplemental-Conference.zip), contents unverified |
| Code/data/weights | No official repository/checkpoint verified; layout-based self-supervised dataset construction checked in Section 5.1 |
| Task | Manhattan-constrained ILT / mask generation |

## Executive Summary

**One sentence:** model axis-aligned boundary points and correction sequences rather than mask pixels, training a Transformer with differentiable lithographic feedback.

A good relaxed pixel solution can break after binarization. TokMan aligns its representation with Manhattan geometry and uses diffusion to generate correction sequences. This joins contour fidelity with mask representation, but axis alignment does not guarantee width, spacing, notch or shot-policy compliance.

## Background & Motivation

Continuous image losses can create curvilinear islands and artifacts. Optical fidelity and write-friendly masks are different objectives. Edge/polygon parameterization preserves horizontal/vertical structure but can restrict topology changes and new assists. CNNs, FNOs and Transformers favor different output representations; they are not one successive replacement chain.

## Physics & Mathematical Foundations

### From point displacement to masks — independent explanation

For points $$X\in\mathbb R^{N\times2}$$ and scalar corrections $$\delta\in\mathbb R^N$$ along allowed directions $$n_i$$,

$$
x'_i=x_i+\delta_i n_i,\qquad M=\mathcal R(X'),\qquad R=g(M).
$$

Use either pixel coordinates or nm consistently for $$x_i,\delta_i$$. Directions $$n_i$$ are dimensionless and $$\mathcal R$$ is a rasterizer. This generic expression explains scalar axis corrections; point-normal signs and constraint handling remain unverified.

$$
\frac{\partial\mathcal L}{\partial\delta}=\left(\frac{\partial X'}{\partial\delta}\right)^T
\left(\frac{\partial M}{\partial X'}\right)^T
\left(\frac{\partial g}{\partial M}\right)^T\frac{\partial\mathcal L}{\partial R}.
$$

The gradient must pass through both simulation and rasterization. Section 4/Figure 2 describes nvdiffrast rendering and simulation feedback. Exact antialiasing and binary projection were not verified.

### Diffusion Transformers — general concept and limits

A standard Gaussian diffusion example is $$z_t=\sqrt{\bar\alpha_t}z_0+\sqrt{1-\bar\alpha_t}\epsilon$$. Here $$t$$ is a noise level, not exposure time; a Transformer predicts conditional token denoising updates.

**This is not TokMan's verified forward process.** A noise analogy for lithographic distortion does not make optical propagation a Gaussian Markov process. Exact schedules, prediction targets and sampling steps require the full text. Point positions encode within-polygon order; polygon positions encode shape context. Their combination does not automatically establish permutation, rotation or reflection robustness.

## Proposed Method / Model Architecture

Section 4.1 describes corner splitting, spatial alignment of parallel edges and partitioning long segments. Section 4.2/Figure 3 predicts scalar corrections with point/polygon embeddings and a denoising Transformer. Section 4.3 adds local ILT refinement.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/tokman.svg' | relative_url }}"><img src="{{ '/assets/notes/research/tokman.svg' | relative_url }}" alt="Independent flow: segmentation, point corrections, rasterization and lithographic feedback in TokMan" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">Enlarge ↗</span></a>
<figcaption>An original data-flow explanation, separate from Figures 2–3, distinguishing geometry tokens from image pixels.</figcaption>
</figure>

Indexed Section 5.1 specifies six Transformer blocks, embedding size 512 and 16 heads. **Physics-guided locations:** lithographic-influence priors in segmentation, self-supervised differentiable simulation and post-inference ILT. The Transformer itself is not an exact diffraction operator.

Target layouts and simulated wafer mismatch can supply training without corrected-mask labels. Full loss weights and diffusion supervision remain unverified, so a generic DDPM loss is not presented as the paper's equation.

## Figures & Visual Explanation

{% include figure-coverage.html %}

The minimum indexed inventory contains six figures. Unseen originals/supplement can contain additional subfigures or colors. Figure 6 varies feature dimensions, head count and decoder layers; no unverified numeric/confidence-interval extraction is claimed.

## Experiments & Results

Indexed Section 5.1 lists 89,697 training layouts, ICCAD13-S/L, 1 nm/pixel, 193 nm wavelength, defocus ±30 nm, dose ±3%, threshold 0.225 and sigmoid steepness 50. Training uses 32 H20s and testing one A100; approximately 80 GB memory is mentioned at batch 40, without verified per-card/total distinction. NA, validation split and sampling schedules remain unverified.

| Table 1 · Condition | Method | Mean EPE | Mean shots | Reported TAT |
| --- | --- | ---: | ---: | ---: |
| ICCAD13-S | IL-ILT | 2.70 | 4948.4 | 2.87 |
| ICCAD13-S | TokMan | 2.16 | 287.6 | 0.89 |
| ICCAD13-L | IL-ILT | 1.80 | 7916.4 | 2.92 |
| ICCAD13-L | TokMan | 1.38 | 642.3 | 1.57 |

EPE is mean boundary-merit-point distance, not violation count. Although sampling is 1 nm/pixel, table-caption EPE/TAT units were not visually verified, so values retain the source labels. TAT includes TokMan inference/postprocessing; baseline scopes differ between fixed iterations and inference, excluding I/O. Do not directly rank against OptiCo's differently defined EPE.

On ICCAD13-L, Multi-ILT's reported TAT 1.33 is below TokMan's 1.57: **TokMan is not fastest in every setting**. Shots are an indirect measure; real write time requires specified fracturing/writer conditions.

## Critical Analysis & Limitations

**Verified:** geometry-aware representation, self-supervised simulation and post-ILT. **Author claim:** strict Manhattan geometry improves manufacturability. **Independent interpretation:** Manhattan compliance is a smaller constraint set than full MRC.

More points grow attention cost; uniform segmentation can waste work, while coarse segmentation can miss corners. Check influence-zone and minimum-segment sensitivity. Moving polygons can cause overlap, self-intersection, spacing violations or topology changes even with axis-aligned edges. Separate optional-refinement cost and benefit. Whether diffusion improves over a deterministic regressor requires same-representation ablations; unverified results are not invented.

## Practical Applications to GeoSignal / OPC

* **Available idea:** preserve edge/point correspondence and gauges before GDS rasterization.
* **Further research / Hypothesis:** test axis-constrained optimization and differentiable rasterization, with final masks checked by Abbe/SOCS. This optimizer is not in the current core.
* **Long term / Hypothesis:** include multiple conditions, SRAF topology and full MRC in token representations. See [current scope]({{ '/notes/research/geosignal-scope/' | relative_url }}).

## Key Takeaways & References

1. Tokens represent layout geometry, not words.
2. Point/polygon context differs from image resolution.
3. Rasterization gradients are a key inverse-learning connection.
4. Diffusion time is not exposure time.
5. Mean EPE differs from violation counts.
6. Manhattan constraints do not guarantee all manufacturing rules.

[Inverse Problem · Metrics]({{ '/notes/foundations/inverse-and-metrics/' | relative_url }}) · [Hi-ILT]({{ '/notes/research/hi-ilt/' | relative_url }}) · [ResGNN-OPC]({{ '/notes/research/resgnn-opc/' | relative_url }})
