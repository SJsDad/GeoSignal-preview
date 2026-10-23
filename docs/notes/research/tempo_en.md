---
layout: technical
category: research
paper_id: tempo
title: "TEMPO — A Shared Height-Conditioned Thick-Mask Aerial Model"
permalink: /notes/research/tempo/
lang: en
---

# TEMPO: A Shared Height-Conditioned Thick-Mask Aerial Model

* Contents
{:toc}

<div class="evidence-note">Reviewed the authors' eight-page GitHub-hosted PDF, Figures 1–5 and Tables 1–5. Separate supplements, model weights and the complete training dataset were not verified. Original-figure reuse permission was not established, so this site links sources and uses independent diagrams.</div>

## Paper Information

| Item | Verified information |
| --- | --- |
| Title | TEMPO: Fast Mask Topography Effect Modeling with Deep Learning |
| Authors/affiliations | Wei Ye, Mohamed Baker Alawieh, David Z. Pan: UT Austin; Yuki Watanabe, Shigeki Nojima: Kioxia Corporation; Yibo Lin: Peking University |
| Publication | ISPD 2020, pp. 127–134 |
| Sources | [DOI](https://doi.org/10.1145/3372780.3375565) · [Author PDF](https://github.com/ywwwer/ywwwer.github.io/blob/master/files/papers/DFM_ISPD2020_Ye.pdf) |
| Code/data/weights | Official training implementation, dataset and checkpoint unverified. The author's website repository hosts paper material, not established model code |
| Task | Mask topography / height-conditioned 3D aerial slices |

## Executive Summary

**One sentence:** one conditional GAN predicts aerial images at multiple resist-film heights to reduce rigorous thick-mask simulation costs.

Scheme 1 uses mask geometry; Scheme 2 adds a thin-mask aerial image, producing different accuracy/speed tradeoffs. A shared encoder and height-conditioned decoder replace separate networks at each height. **Film height is not scanner defocus.** Despite EUV background motivation, Section 4 evaluates 193 nm DUV at NA 1.2, not 13.5 nm EUV.

## Background & Motivation

Thin masks place transmittance on an infinitesimal plane. Thick-mask edges, sidewalls and materials scatter fields, modifying amplitude, phase and polarization and raising electromagnetic simulation costs. Fixed thin-image biases can miss geometry-dependent phase changes. Independent networks at each height also relearn shared geometry.

[Abbe imaging]({{ '/notes/abbe-imaging/' | relative_url }}) explains projection but cannot recover topography from binary thin-mask inputs alone. TEMPO learns differences using rigorous thick-mask references.

## Physics & Mathematical Foundations

### Near fields and aerial slices — independent explanation

For complex mask near field $$E_{near}(x,y)$$ and an operator $$\mathcal H_h$$ including projection and film propagation, a coherent example is

$$
I_h(x,y)=|\mathcal H_h[E_{near}](x,y)|^2.
$$

Height $$h$$ is in nm inside the film and $$I_h$$ is normalized intensity. Partial coherence/polarization require separate source/vector sums. This formula does not assert that TEMPO outputs electromagnetic fields; it predicts intensity. Heights share a mask and stack, motivating shared latents and height-conditioned decoding, without guaranteeing continuous interpolation between sampled heights.

### Conditional GAN loss

A paired cGAN trains discriminator $$D$$ to distinguish reference/generated pairs and generator $$G$$ to resemble references:

$$
\min_G\max_D\ \mathbb E[\log D(x,y,h)]+\mathbb E[\log(1-D(x,G(x,h),h))]
+\lambda\mathbb E\|y-G(x,h)\|_1.
$$

$$x$$ is a mask or mask+thin image, $$y$$ a thick aerial reference and $$h$$ the condition. This notation summarizes the cGAN/paired-fidelity idea; it does not assert an identical reduction convention to equation (4). Adversarial loss alone need not preserve absolute intensity, making paired fidelity important.

### Height encoding

The generator bottleneck receives a one-hot height label. The discriminator uses the ordinal height channel of equation (5):

$$
p_k=p_{min}+\frac{p_{max}-p_{min}}{m-1}k,\quad k\in\{0,\ldots,m-1\}.
$$

$$p_k$$ is an encoding value, not optical intensity. For $$m=13$$ domains, map label indices separately to nm. Ordered discriminator labels do not establish continuous-height extrapolation by the one-hot generator.

## Proposed Method / Model Architecture

Section 3/Figure 4/Table 1 uses eight encoder convolution layers, eight decoder deconvolution layers and skips. Inputs are 200×200, with one channel for Scheme 1 and two for Scheme 2. Height joins the 512-feature bottleneck. Four discriminator convolutions plus FC classification inspect pairs and heights.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/tempo.svg' | relative_url }}"><img src="{{ '/assets/notes/research/tempo.svg' | relative_url }}" alt="Independent diagram of TEMPO input schemes, shared encoder and height-conditioned decoder" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">Enlarge ↗</span></a>
<figcaption>An original explanation, not a reproduction of Figures 3–4, summarizing the roles of input channels and film height.</figcaption>
</figure>

Section 4 lists 1.03×10⁸ shared TEMPO parameters versus 1.17×10⁹ across 13 independent models. Measured peak memory was not verified; parameter reductions do not directly give GPU-memory reductions. Scheme 2 inputs already encode some source/pupil response but require a thin-mask simulation before inference. Network-only Scheme 1 and end-to-end Scheme 2 costs are different scopes.

**Physics entry points:** height conditioning, simulator-derived Scheme 2 inputs and rigorous labels. The GAN does not enforce Maxwell equations as a PINN. Training uses TensorFlow, batch four, up to 70 epochs and paired-loss weight 1000, compared with 13 separate-height models.

## Figures & Visual Explanation

{% include figure-coverage.html %}

All 5/5 main figures are linked. Table 3 also shows aerial slices and difference maps, interpreted below. A separate supplement was not verified.

## Experiments & Results

The dataset contains 966 contact clips, 60×60 nm contacts, 128 nm pitch and original 2×2 µm layouts. Calibre adds SRAFs/OPC; Sentaurus Lithography generates references. Conditions are quasar illumination, 193 nm, NA 1.2 and central nonperiodic 1.5×1.5 µm windows. XY pitch is 7.5 nm, height pitch 10 nm over 0–120 nm (13 slices). Train/test is 75%/25%; runtime evaluates 242 clips on Intel i9 3.3 GHz/TITAN Xp. A separate validation split was not explicitly verified.

| Mean on the same test set | Scheme 1 | Scheme 2 | Source |
| --- | ---: | ---: | --- |
| TEMPO NRMSE [%] | 4.23 | 1.79 | Table 2 |
| 13 independent models NRMSE [%] | 4.63 | 2.27 | Table 2 |
| Central-contact X CD error [nm] | 0.72 | 0.38 | Table 4 |
| Central-contact Y CD error [nm] | 0.67 | 0.45 | Table 4 |
| All 242 clips runtime | 1.1 min | 46.4 min | Table 5 |

Table 5's rigorous simulation takes 20.5 h. Scheme 2 is 45.3 min thin-mask simulation plus 1.1 min GAN, with reported ratio 26.51. The abstract's up-to-1170× claim belongs to faster Scheme 1, not Scheme 2. Rounded 1.1 min cannot reproduce an exact speed ratio.

Table 3 compares reference, schemes and differences at 0/60/120 nm for one contact. Intensity and error use different scales, approximately 0.02–0.12 and 0.002–0.008 respectively; matching colors do not imply the same quantity. CD evaluates the central contact using an aerial image averaged over 13 slices, not complete resist chemistry, worst CD across all contacts or wafer measurements.

## Critical Analysis & Limitations

Shared height conditioning is useful, but 966 contact clips and a fixed optical stack limit claims about lines/spaces, new sources, materials or absorber geometry. CD from averaged slices differs from film-profile reconstruction. Replacing a 3D resist model requires matching absorption, standing waves and chemistry. Scheme 2 gains from added physical information as well as architecture. Plausible smooth GAN images can miss rare high-error contacts; inspect maximum CD and error tails, starting with Figure 5's histogram.

## Practical Applications to GeoSignal / OPC

* Topography-aware learning requires suitable physical references and data.
* Film-height slices and scanner-focus comparisons must remain distinct.

See [GeoSignal scope]({{ '/notes/research/geosignal-scope/' | relative_url }}) for public capabilities. These are research connections, not claims of implemented features.

## Key Takeaways & References

1. Experiments use 193 nm DUV, not EUV.
2. Film height is not scanner defocus.
3. Scheme 2 includes both information and cost from thin-mask inputs.
4. Shared modeling across heights is central.
5. CD refers to the central contact and averaged slices.
6. 1170× and 26.51× describe different schemes.

[Abbe Imaging]({{ '/notes/abbe-imaging/' | relative_url }}) · [Nitho]({{ '/notes/research/nitho/' | relative_url }}) · [GeoSignal scope]({{ '/notes/research/geosignal-scope/' | relative_url }})
