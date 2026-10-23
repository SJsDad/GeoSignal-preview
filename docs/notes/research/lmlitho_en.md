---
layout: technical
category: research
paper_id: lmlitho
title: "LMLitho — A Large Forward Model for Source–Mask Relationships"
permalink: /notes/research/lmlitho/
lang: en
---

# LMLitho: A Large Forward Model for Source–Mask Relationships

* Contents
{:toc}

<div class="evidence-note">Reviewed the authors' nine-page PDF, Figures 1–13, Tables I–IV and Algorithm 1. Original images are not redistributed; a separate supplement was not verified. Attention, gradient and practical interpretations below distinguish learned resemblance from physical laws.</div>

## Paper Information

| Item | Verified information |
| --- | --- |
| Title | LMLitho: A Large Vision Model-Driven Lithography Simulation Framework |
| Authors | Zhen Wang, Hongquan He, Tao Wu, Xuming He, Qi Sun, Cheng Zhuo, Bei Yu, Jingyi Yu, Hao Geng |
| Affiliations | ShanghaiTech University; Qi Sun/Cheng Zhuo: Zhejiang University; Bei Yu: The Chinese University of Hong Kong |
| Publication | ICCAD 2025 |
| Sources | [DOI](https://doi.org/10.1109/ICCAD66269.2025.11240940) · [Author PDF](https://www.cse.cuhk.edu.hk/~byu/papers/C286-ICCAD2025-LMLitho.pdf) |
| Official repository | [LMLitho/LMLitho](https://github.com/LMLitho/LMLitho): README and some data archives checked; model implementation/checkpoints not verified |
| Task | Source-conditioned forward resist simulation; mask-generator training with a frozen simulator |

## Executive Summary

**One sentence:** separate mask and illumination encoders are joined by cross-attention to predict resist images with a large vision model.

Unlike fixed-source mask-to-resist models, it explicitly represents how changing illumination changes the print from the same mask. Large simulated datasets train source–mask–resist relationships, followed by fine-tuning for new nodes. Useful ideas are preserving full source maps instead of one sigma value and using a frozen surrogate for inverse training. Cross-attention is not an exact interference equation.

## Background & Motivation

In [Abbe imaging]({{ '/notes/abbe-imaging/' | relative_url }}), source positions and weights change the mask-spectrum combinations admitted by the pupil. Annular, quasar and multipole illumination can give different responses to one layout. Mask-only models learn mappings tied to their training source.

Small convolutional receptive fields limit distant context. ViT attention directly connects patches across an image, but global receptive field is not identical to optical support and raises computation/data requirements.

## Physics & Mathematical Foundations

### Cross-attention through coordinates and shapes

For $$N$$ mask patches, $$N_s$$ source tokens and head dimension $$d$$,

$$
\begin{aligned}
Q&\in\mathbb R^{N\times d},\\
K&\in\mathbb R^{N_s\times d},\quad V\in\mathbb R^{N_s\times d_v},\\
A&=\operatorname{softmax}\left(\frac{QK^T}{\sqrt d}\right),\\
Y&=AV.
\end{aligned}
$$

$$A$$ has shape $$N\times N_s$$ and $$Y$$ is $$N\times d_v$$. Each mask query learns source-token relevance. Scaling by $$\sqrt d$$ limits growth of dot-product variance with dimension. Latent weights/embeddings are dimensionless, not directly optical quantities. Equation (5) uses mask queries and source keys/values; standard per-head projections make dimensions compatible without requiring equal raw embedding dimensions.

### Attention and optics: connection and distinction — independent analysis

Abbe source weights are incident intensities independent of the mask. Learned attention weights depend on mask queries and source keys, are positive and row-normalized, and do not explicitly carry complex interference phase. Attention is an architectural analogy, not an identical Abbe source sum.

### Resist supervision and inverse gradients

For predictions $$P_p\in[0,1]$$ and labels $$G_p\in\{0,1\}$$, BCE measures foreground/background mismatch, Dice overlap and SSIM local structure. Equation (6) combines $$\alpha L_{dice}+\beta L_{BCE}+\gamma L_{SSIM}$$, not an optical PDE residual. Overlap loss helps sparse targets but cannot replace EPE for missing small vias or shifted edges.

## Proposed Method / Model Architecture

Section III/Figure 5 follows Mask Encoder → Exposure Attention with Source Encoder → Resist Decoder. The mask path uses nonoverlapping patches, positional embeddings, ViT and local residual refinement. The source path uses residual blocks, self-attention and downsampling; the decoder combines edge refinement with global attention.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/lmlitho.svg' | relative_url }}"><img src="{{ '/assets/notes/research/lmlitho.svg' | relative_url }}" alt="Independent data-flow diagram joining mask queries with source keys and values in LMLitho" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">Enlarge ↗</span></a>
<figcaption>An original attention-flow illustration, separate from Figure 5; patch and channel dimensions are symbolic.</figcaption>
</figure>

Dividing $$M\in\mathbb R^{H\times W}$$ into $$P\times P$$ patches gives $$N=(H/P)(W/P)$$ and embeddings $$N\times D_m$$. Source and mask images occupy different coordinate spaces; their pixel spacings and patch indices are not necessarily aligned.

Algorithm 1/Figure 7 freezes the Source Encoder after pretraining and fine-tunes the remaining modules. Section IV specifies four heads, mask depth four, source/decoder depth two, approximately 0.3B parameters and four H100 GPUs. Exact patch size, batch schedule and peak memory were not verified.

**Physics-informed/guided assessment:** source-preserving architecture and commercial-simulator supervision. Figure 11 trains a mask generator through a frozen LMLitho gradient. It does not impose Maxwell or resist-reaction equations as exact constraints.

## Figures & Visual Explanation

The inventory links **13/13 main figures**, using summaries and source locations rather than redistributed images. Red/gray meanings differ between Figures 8 and 9; follow each caption/text.

{% include figure-coverage.html %}

## Experiments & Results

Table I lists 101,650 flexible-source pretraining samples, with CPU/metal/via test counts 150/750/300. Fixed-source training uses 3,435 samples and tests 25/90/50. Source maps are padded from 201×201 to 256×256. Mask/resist sampling is 1 nm²/pixel over 4 µm²/image, equivalent to 1 nm square-pixel pitch. Partial repository data differ from the paper's full dataset.

| Matched evaluation | Baseline mIoU [%] | LMLitho mIoU [%] | Source |
| --- | ---: | ---: | --- |
| 28nm-S-CPU · Flexible source | Abbe 86.17 / Torch Litho 84.18 | 97.78 | Table II(a) |
| 28nm-CPU · Fixed annular source | DOINN 97.14 / DLS 96.46 | 98.12 | Table II(b) |
| 20nm-CPU · New-node training/fine-tuning | DOINN 96.10 / DLS 92.51 | 97.62 | Table IV |

Table III's five-epoch ablation reports mIoU 94.62% for CNN+attention, 94.74% for ViT without source/decoder attention, 92.73% with both removed, and 96.32% for the full model. Check modified modules and training budgets rather than inferring contributions from one receptive-field visualization.

The baseline optical/resist models differ in scope from commercial labels; Table II(a) does not prove AI universally more accurate than physics. Table IV includes 20 nm fine-tuning after source-encoder freezing, so it is not zero-shot transfer.

Section IV-A compares approximately 0.12 s GPU inference with 15 s CPU commercial simulation after optical-model setup. A roughly 40-minute source setup is separate. Do not reinterpret the 120× claim as same-hardware algorithmic speedup or training-amortized end-to-end acceleration.

BenchOPC uses 3,000 training layouts and 25 tests, with final masks reevaluated commercially. Figure 12 PVB uses dose ±3% and defocus ±40 nm. Figure 10's 28 nm mean forward EPE is 0.42 nm for LMLitho, 0.67 for DOINN and 0.84 for DLS. This compares **predicted and golden forward contours**, not optimized masks against inverse targets. Complete calibrated NA/wavelength settings and split leakage could not be fully reproduced from public evidence.

## Critical Analysis & Limitations

**Facts:** separate source input, large simulated data, cross-node fine-tuning and frozen-engine inverse tests. **Author claim:** source-aware large vision models can lead toward lithography foundation models. **Independent interpretation:** source interpolation within training and extrapolation to a new optical process are different problems.

**Independent calculation:** 0.3B float32 weights alone need about 1.2 GB; this is not measured GPU memory. Optimizer states, activations and attention add training memory. Whether small ROIs beat cached Abbe depends on batching, source reuse and GPU access.

Freezing the source encoder may depend on limited optical changes. Similar source shape does not guarantee the same encoding remains appropriate after NA, aberration or resist changes. Matching commercial-simulator labels is distinct from wafer-metrology validation. Independent reevaluation of inverse masks is valuable, but average fidelity does not guarantee gradient accuracy, worst EPE or complete MRC.

## Practical Applications to GeoSignal / OPC

* Source-conditioned prediction is a research direction beyond fixed-illumination examples.
* Source interpolation, process transfer and calibrated resist prediction are distinct goals.

See [GeoSignal scope]({{ '/notes/research/geosignal-scope/' | relative_url }}) for public capabilities. These are research connections, not claims of implemented features.

## Key Takeaways & References

1. Explicit source input is a defining feature.
2. Attention weights differ from physical source intensities.
3. Forward and inverse EPE use different references.
4. The 20 nm results follow fine-tuning.
5. Separate CPU/GPU, setup and training costs in runtime claims.
6. Frozen parameters can still pass input gradients.

[Abbe Imaging]({{ '/notes/abbe-imaging/' | relative_url }}) · [Metrics]({{ '/notes/foundations/inverse-and-metrics/' | relative_url }}) · [Official LMLitho data](https://github.com/LMLitho/LMLitho) · [LithoSim](https://dw-hongquan.github.io/LithoSim/)
