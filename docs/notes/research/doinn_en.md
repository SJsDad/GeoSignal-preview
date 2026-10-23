---
layout: technical
category: research
paper_id: doinn
title: "DOINN — Why Separate Global Fourier and Local CNN Branches?"
permalink: /notes/research/doinn/
lang: en
---

# DOINN: Why Separate Global Fourier and Local CNN Branches?

* Contents
{:toc}

<div class="evidence-note">Reviewed the arXiv v1 PDF/HTML, Figures 1–9, Tables 1–4 and Appendix A.1–A.2. The arXiv DOI and conference DOI are distinct. Permission to post on arXiv does not establish an image-reuse license, so original figures are linked rather than reproduced.</div>

## Paper Information

| Item | Verified information |
| --- | --- |
| Title | Generic Lithography Modeling with Dual-band Optics-Inspired Neural Networks |
| Authors | Haoyu Yang, Zongyi Li, Kumara Sastry, Saumyadip Mukhopadhyay, Mark Kilgard, Anima Anandkumar, Brucek Khailany, Vivek Singh, Haoxing Ren |
| Affiliations | NVIDIA; Zongyi Li and Anima Anandkumar also list California Institute of Technology |
| Publication | DAC 2022; the arXiv record confirms acceptance at the 59th DAC |
| Sources | [arXiv](https://arxiv.org/abs/2203.08616) · [v1 PDF](https://arxiv.org/pdf/2203.08616v1) · [v1 HTML](https://arxiv.org/html/2203.08616v1) · [arXiv DOI](https://doi.org/10.48550/arXiv.2203.08616) |
| Official code/weights | An original-author implementation was not verified. LithoBench's implementation is a benchmark implementation, not established as identical to the authors' code |
| Data/task | ISPD 2019, ICCAD 2013, N14; forward resist/contour simulation |

## Executive Summary

**One sentence:** one optimized Fourier branch handles low-frequency global structure, while a CNN handles high-frequency edge details to reconstruct high-resolution contours.

Nonlocal optical response needs distant geometry context, but repeated FFTs across many latent channels of a 2000×2000 image are expensive. DOINN reduces Fourier work and adds a complementary local branch. “Dual-band” refers to **global/local information roles**, not two illumination wavelengths.

## Background & Motivation

Small convolution kernels represent edges well but need depth or dilation to cover broad optical influence. FNOs handle global interactions directly, with FFT costs growing with image size and feature channels. A coarse global path alone struggles to recover edge positions, narrow gaps and via sizes.

The global path therefore uses downsampled inputs, while the CNN restores lost details. Distinguish this learned approximation from physically exact SOCS.

## Physics & Mathematical Foundations

### SOCS and the optimized Fourier branch

In [Hopkins/TCC/SOCS]({{ '/notes/foundations/hopkins-tcc-socs/' | relative_url }}), fields follow FFT → kernel product → IFFT, and intensity sums squared mode magnitudes. A conceptual form of DOINN's reduced Fourier computation, following equation (11), is

$$
V=\rho\left(\mathcal F^{-1}\left[(\mathcal F(A))_{low}\,W_P\,W_R\right]\right).
$$

$$A$$ is a single-channel input, $$W_P$$ channel lifting, and $$W_R$$ learned complex spectral weights. This matrix-product shorthand does not assert an exact tensor implementation identical to the paper's convolution notation.

The main saving is an **FFT before channel lifting**: transform $$B\times1\times H\times W$$, then lift retained modes to $$C$$ channels, reducing the channel-wise FFTs of repeated FNO blocks. Output IFFT, local convolutions and reconstruction still cost time.

### Frequency indices and physical support — independent calculation

Mode spacing is $$\Delta f=1/L$$. Retaining the lowest $$k$$ modes on width $$L$$ represents frequencies up to roughly $$k/L$$; keeping the same $$k$$ on width $$4L$$ reduces physical support to about one quarter. Accepting arbitrary tensor shapes does not guarantee the same physical function.

This motivates constructing and combining training-tile-sized global features for larger tiles. See the sampling and halo discussion in the [FFT note]({{ '/notes/fourier-optics/' | relative_url }}).

## Proposed Method / Model Architecture

Section 3 and Figure 4 divide the model into Global Perception (GP), Local Perception (LP) and Image Reconstruction (IR). GP uses a pooled input and one optimized Fourier unit; LP uses stacked VGG blocks. IR concatenates features and restores resolution with transposed and refinement convolutions.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/doinn.svg' | relative_url }}"><img src="{{ '/assets/notes/research/doinn.svg' | relative_url }}" alt="Original explanatory diagram: global Fourier branch, local CNN branch and contour reconstruction in DOINN" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">Enlarge ↗</span></a>
<figcaption>An independently drawn computation diagram, not a reproduction of Figure 4. Exact Appendix layer dimensions remain in the source.</figcaption>
</figure>

Appendix A.1 gives a representative 2048×2048 configuration: GP average pooling to 256×256×1, real FFT to 256×129×1, lifting to 16 channels, retaining the first 50×50 coefficients, and inverse FFT to 256×256×16. LP uses 4→8→16 channels and /2, /4, /8 downsampling. IR starts with 32 concatenated GP/LP channels and combines local bypasses while upsampling. Check padding when reproducing the difference between the main text's 2000×2000 evaluation and the Appendix's 2048 grid.

Appendix A.2 specifies A100, PyTorch 1.9, MSE/Adam, initial learning rate 0.002, batch 16, up to 10 epochs, decay by 0.5 every two epochs, and weight decay 0.0001. These are distinct from later LithoBench defaults.

GP output has shape $$C\times H/8\times W/8$$. Appendix A.1–A.2 records stage-level Conv/GP/IR settings; the diagram does not invent additional channel counts. Section 3.2/Figure 5 uses half-overlapping training-sized clips and combines valid cores, rather than full-chip inference in one pass. This preserves physical Fourier support and optical halo.

**Physics entry point:** an architecture prior resembling an optical FFT pipeline. Learned features, nonlinearities and spectral truncation do not enforce an exact pupil/SOCS constraint or optical PDE residual. Training uses supervised mask/resist pairs; MSE settings appear in Appendix A.2. Later LithoBench inverse variants are distinct from the original forward method.

## Figures & Visual Explanation

{% include figure-coverage.html %}

All 9/9 main figures are linked. Appendix A.1 layer tables and A.2 settings are supplementary explanations within the same arXiv document. Figure 9 uses the label DOINN-FS, while Table 4 calls the large-tile method DOINN-LT; this naming difference is retained.

## Experiments & Results

Table 1/Section 4.1 separate ISPD 2019 vias, ICCAD 2013 metal and N14 vias. L and H are 1000×1000 and 2000×2000 grids covering 4 µm² tiles. Their pixel areas and sampling differ, so do not pool the metrics indiscriminately.

| Table 2 · mIoU [%] | UNet | DAMO-DLS | DOINN |
| --- | ---: | ---: | ---: |
| ISPD-2019 (L) | 98.03 | 98.11 | 98.27 |
| ICCAD-2013 (L) | 95.38 | 96.97 | 97.79 |
| ICCAD-2013 (H) | 93.04 | Unsupported | 97.77 |
| N14 | 91.64 | Unsupported | 96.49 |

Table 3's ICCAD-2013(L) ablation is GP only 96.09 → GP+IR 97.20 → GP+IR+LP 97.60 → full bypass 97.79 mIoU. It supports the local branch's benefit, while CD/EPE specifications require separate evaluation. Table 4 reports ISPD-2019-LT mIoU of 92.03% for default DOINN and 98.23% for DOINN-LT, using 4 µm² training tiles and ten 64 µm² via test tiles, not full-chip hardware validation.

Figure 6 plots throughput in µm²/s against training epochs. The paper lists 1.3M parameters versus DAMO-DLS's 18M while also saying approximately 20× smaller. **Independent calculation gives 18/1.3≈13.8**, so these values should not be forced into exact agreement. The abstract reports 85× speedup over the reference simulator; hardware, tile and accuracy conditions still matter.

Table 1 lists train/test counts ICCAD 4,875/10, ISPD 10,300/11,641 and N14 1,630/137. The text also describes evaluating the 100 densest of approximately 1.6K N14 clips; check the exact split discrepancy when reproducing. Validation split and seed were not verified. Complete source/NA/wavelength settings, peak memory and process-window conditions were not fully verified either; these tables do not establish transfer to new process conditions.

## Critical Analysis & Limitations

Global/local separation balances computation and contour detail. A low-frequency feature resembling an aerial image is not proof that the hidden feature is a coherent field; visualization suggests an interpretation without proving constraints.

Insufficient halo can corrupt large-tile boundaries. Training mainly on OPC-corrected masks also shifts the input distribution when an inverse loop starts from an uncorrected mask. Figure 8 compares responses over 24 OPC iterations, not all optimizer trajectories. Image IoU can underweight critical edges or rare bridges. Commercial OPC requires gauge error tails, source/focus variation, binarization and worst-region checks.

## Practical Applications to GeoSignal / OPC

* **Available idea:** record ROI halo, valid core and frequency grids in dataset metadata; this also helps validate cached optical pipelines.
* **Further research / Hypothesis:** compare a GP/LP ROI surrogate against Abbe/SOCS for raw intensity, CD, boundary error and mask gradients.
* **Long term / Hypothesis:** add source/focus/dose conditioning; do not claim that the original paper already supports all those inputs.

## Key Takeaways & References

1. Dual-band separates global and local information.
2. FFT before channel lifting is the main saving.
3. Physical meaning of mode indices depends on tile size.
4. Arbitrary tensor size is distinct from physical-domain generalization.
5. Feature visualization does not prove physical consistency.
6. Parameter counts, model bytes and throughput have different units.

[Fourier Optics]({{ '/notes/fourier-optics/' | relative_url }}) · [Nitho]({{ '/notes/research/nitho/' | relative_url }}) · [LMLitho]({{ '/notes/research/lmlitho/' | relative_url }}) · [LithoBench](https://github.com/shelljane/lithobench)
