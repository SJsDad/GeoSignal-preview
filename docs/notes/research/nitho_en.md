---
layout: technical
category: research
paper_id: nitho
title: "Nitho — Learning Optical Kernels Instead of Masks"
permalink: /notes/research/nitho/
lang: en
---

# Nitho: Learning Optical Kernels Instead of Masks

* Contents
{:toc}

<div class="evidence-note">Reviewed the arXiv v4 text/six-page PDF, Figures 1–6, Tables I–V and Algorithm 1. The stated license is CC BY-NC-ND 4.0. This site uses original explanatory diagrams and source links rather than redistributing figures. A separate supplement was not verified.</div>

## Paper Information

| Item | Verified information |
| --- | --- |
| Title | Physics-Informed Optical Kernel Regression Using Complex-valued Neural Fields |
| Authors | Guojin Chen, Zehua Pei, Haoyu Yang, Yuzhe Ma, Bei Yu, Martin D. F. Wong |
| Affiliations | The Chinese University of Hong Kong; Haoyu Yang: NVIDIA; Yuzhe Ma: HKUST(GZ) |
| Publication | DAC 2023; arXiv confirms acceptance by DAC23 |
| Sources | [arXiv](https://arxiv.org/abs/2303.08435) · [v4 PDF](https://arxiv.org/pdf/2303.08435v4) · [v4 HTML](https://arxiv.org/html/2303.08435v4) · [arXiv DOI](https://doi.org/10.48550/arXiv.2303.08435) |
| Code/data/weights | Original-author implementation and trained kernels not verified. ICCAD/ISPD layouts are separate from reference imaging labels |
| Task | Forward optical simulation / complex kernel identification |

## Executive Summary

**One sentence:** identify mask-independent complex kernels with neural fields under fixed optics, then process new masks with fixed FFT/SOCS operations.

Rather than generating images with a network for every mask, Nitho preserves known mask-linear operations and learns the kernels summarizing source/pupil information. After training, kernels can be stored without running the MLP per mask. The key separation is **offline system identification versus online synthesis**. Fixed-condition kernels do not automatically generalize to new optics or resist.

## Background & Motivation

Image-to-image predictors jointly learn geometry distributions and imaging systems, which can limit morphology generalization. [Hopkins/TCC/SOCS]({{ '/notes/foundations/hopkins-tcc-socs/' | relative_url }}) separates optics from masks mathematically; Nitho carries this separation into learning. Its neural-field coordinates describe a kernel grid, not 3D scene positions. NeRF inspiration does not imply volumetric rendering or view-direction inputs.

## Physics & Mathematical Foundations

### Kernel synthesis and mask separation

Equation (9) takes the form

$$
I(M)=\sum_{j=1}^{r}\left|\mathcal F^{-1}\left[K_j\odot\mathcal F(M)\right]\right|^2.
$$

$$M$$ is a binary mask, $$K_j$$ a complex optical-mode kernel and $$r$$ the retained mode count. Eigenvalue scaling can be absorbed into kernels. Effective coherent modes need not correspond to individual source points.

The MLP maps coordinate $$v$$ to $$K(v)$$, not a mask to an image. FFT, kernel multiplication, IFFT and squared-magnitude summation remain fixed. **The physics-informed structure is this fixed synthesis plus a separately learned kernel**, a stronger constraint than complex weights alone.

### Complex neural fields and positional encoding

The paper uses complex linear layers, separate real/imaginary ReLUs and Gaussian random Fourier features (RFF). A generic real encoding is

$$
\gamma(v)=[\cos(2\pi Bv),\sin(2\pi Bv)],\quad B_{ab}\sim\mathcal N(0,\sigma^2).
$$

$$v\in[0,1]^2$$ is a normalized dimensionless coordinate; $$B$$ sets feature frequencies. Equation (15) lifts these features into the complex domain using $$(1+i)$$. Encoding frequency is not in optical spatial-frequency units.

MLPs tend to learn smooth low-frequency functions first, making rapidly varying complex kernels harder. RFF supplies directional/frequency bases; higher Gaussian scale can also change noise fitting and optimization cost. CReLU generally is not holomorphic: differentiation in real/imaginary parameters differs from complex analyticity.

### Kernel support units — independent check

For physical ROI width $$L_x$$ [nm], equation (10)'s dimension heuristic is roughly $$m\simeq4\mathrm{NA}L_x/\lambda+1$$. The paper assumes 1 nm/pixel; with other spacing use $$L_x=W\Delta x$$. This is a resolution heuristic, not a universal support formula for arbitrary NA/source. Align shifted pupils, FFT grids, cropping, padding and learned rank.

## Proposed Method / Model Architecture

Figure 3(a)/Algorithm 1 follows normalized coordinates → RFF → complex MLP → kernels. A separate mask FFT is centrally cropped, multiplied by kernels and used to synthesize aerial intensity; supervised aerial MSE updates parameters. Constant thresholding produces binary resist.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/nitho.svg' | relative_url }}"><img src="{{ '/assets/notes/research/nitho.svg' | relative_url }}" alt="Independent diagram separating offline neural-field kernel learning from online mask FFT synthesis" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">Enlarge ↗</span></a>
<figcaption>An original explanation, separate from Figure 3, distinguishing training-time neural fields from cached inference kernels.</figcaption>
</figure>

Kernel tensors are complex $$r\times n\times m$$ arrays; input coordinates have shape $$nm\times2$$. Batch spectra of $$B\times1\times H\times W$$ masks are aligned to retained support. Maintaining output resolution after spectral cropping requires correct zero padding and FFT normalization; directly IFFTing a small crop does not yield the original-grid intensity. This needs explicit reproduction checks.

With cached trained kernels, the online path is FFT, mode products/IFFTs and intensity summation. Record precomputation separately from mode-dependent inference, and distinguish trained-network bytes from exported-kernel bytes.

## Figures & Visual Explanation

{% include figure-coverage.html %}

All 6/6 main figures are linked. Table V studies positional encoding; Figure 6 studies dataset ratio/kernel dimensions. They are not one experiment. A separate supplement was not verified.

## Experiments & Results

Table II lists ICCAD B1 4,875 train/10 test, B1opc ten OOD tests, ISPD metal B2m 1,000/300 and via B2v 10,000/10,000. Tiles cover 4 µm² with 2000×2000 pixels. ISPD references use Calibre, 193 nm and NA 1.35; ICCAD uses contest Lithosim. This is not a unified source/focus/dose/wafer-resist protocol.

| Table III · Aerial MSE ×10⁻⁵ | Retrained DOINN | Nitho |
| --- | ---: | ---: |
| B1 | 5.55 | 1.32 |
| B2m | 1202.39 | 25.48 |
| B2v | 2.26 | 2.01 |
| B2m+B2v | 3114.24 | 33.13 |
| Reported average | 1081.11 | 15.49 |

The approximately 69× difference is a ratio of table averages, not every row: B2v differs little, while metal/mixed differences are large. DOINN was retrained under Nitho's protocol, so these numbers are not directly comparable with DOINN's original Table 2.

Table IV's B2m→B2v mIoU is 78.31% for DOINN and 97.33% for Nitho. This supports shape OOD under the same imaging reference, not new-scanner transfer. Table V reports B1 PSNR 25.33 dB without PE, 48.83 with NeRF PE and 50.75 with RFF. PSNR is logarithmic; dividing 50.75 by 25.33 does not mean twice the accuracy.

Table I lists 0.41 MB for Nitho and roughly 1.3 MB for DOINN, with possible parameter-count/unit ambiguity; DOINN's own paper lists 1.3M parameters. Do not silently correct this into an equal-storage memory ranking. Figure 5 discusses about 1.3× throughput improvement and about 90× reference speedup; account for cached inference, GPU and simulator cost boundaries.

## Critical Analysis & Limitations

**Structural advantage:** not directly generating morphology can help shape OOD under fixed optics. **Limits:** shift invariance, fixed processes, finite support and mode truncation. Geometry-dependent mask-3D scattering may require more than one mask-independent kernel set.

Intensity supervision does not uniquely identify modes: unitary mixing of $$K_j$$ can preserve summed squared fields. Kernel visualization alone does not prove recovery of actual eigenmodes. Cached inference resembles conventional SOCS, so speed claims should include a baseline with exact kernels already cached, rather than attributing all online savings to neural fields.

Constant-threshold resist is not chemistry. Without condition-dependent fields or per-condition kernels, source/focus/dose, DOF and Bossung generalization are not established.

## Practical Applications to GeoSignal / OPC

* Fixed-condition kernel identification is a research direction distinct from mask generation.
* Shape generalization and transfer to new optical conditions need separate evidence.

See [GeoSignal scope]({{ '/notes/research/geosignal-scope/' | relative_url }}) for public capabilities. These are research connections, not claims of implemented features.

## Key Takeaways & References

1. The learned input is kernel position, not a mask image.
2. Online inference can use only cached kernels.
3. Fixed synthesis plus learned kernels supplies the physical structure.
4. SOCS modes need not map one-to-one to source points.
5. Kernel heuristics require correct pixel pitch and units.
6. Shape OOD differs from process OOD.
7. Distinguish PSNR, model bytes and parameter counts.

[Hopkins/TCC/SOCS]({{ '/notes/foundations/hopkins-tcc-socs/' | relative_url }}) · [Fourier Optics]({{ '/notes/fourier-optics/' | relative_url }}) · [DOINN]({{ '/notes/research/doinn/' | relative_url }}) · [TEMPO]({{ '/notes/research/tempo/' | relative_url }})
