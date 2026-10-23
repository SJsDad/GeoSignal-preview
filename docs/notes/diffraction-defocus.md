---
layout: technical
category: foundations
title: "Diffraction Orders and Defocus: Off-Axis Imaging"
description: Higher diffraction orders, pupil filtering and defocus explain the differences between three-beam and symmetric two-beam imaging.
permalink: /notes/diffraction-defocus/
lang: en
---

<p class="language-switch"><a href="{{ '/ko/notes/diffraction-defocus/' | relative_url }}" lang="ko">한국어로 보기 · 전체 유도와 실험 조건</a></p>

# Diffraction Orders and Defocus: Off-Axis Imaging

Why do square mask edges become rounded in the aerial image? Why can tilted illumination reduce sensitivity to focus? This note connects [Fourier Optics]({{ '/notes/fourier-optics/' | relative_url }}) and [Abbe Imaging]({{ '/notes/abbe-imaging/' | relative_url }}) through a periodic, one-dimensional binary amplitude mask. The full derivations and worked conditions are in the [Korean learning note]({{ '/ko/notes/diffraction-defocus/' | relative_url }}).

{% include diffraction-demo-cta.html %}

* Contents
{:toc}

## Diffraction orders and the pupil

The demo starts with the 6f ray layout: source at 0f, condenser at 1f, mask at 2f, objective at 3f, pupil at 4f, imaging lens at 5f and wafer at 6f. Equal-focal-length thin lenses collimate the illumination, focus each order to one pupil height, stop blocked rays at that plane, and form an inverted image. The wave graphs use the same transmitted orders and the actual inverted wafer coordinate. Defocus displacement in the ray sketch is magnified for visibility; its wave phase uses the physical focus in µm.

<figure class="study-figure">
  <a class="figure-zoom" href="{{ '/assets/notes/diffraction-defocus/ray-6f.png' | relative_url }}"><img src="{{ '/assets/notes/diffraction-defocus/ray-6f.png' | relative_url }}" alt="6f thin-lens ray paths for normal three-beam and tilted two-beam illumination. The blocked minus-first order ends at the pupil." loading="lazy"></a>
  <figcaption>Follow the rays first, then compare their pupil spectrum and wave intensity. Heights are normalized by focal length.</figcaption>
</figure>

A centered opening with pitch $$P$$, width $$w$$ and duty ratio $$D=w/P$$ has coefficients

$$
c_j=D\operatorname{sinc}(jD),\qquad f_j=f_s+j/P.
$$

The normalized sinc is $$\sin(\pi v)/(\pi v)$$. At $$D=0.5$$, nonzero even orders vanish. Coefficient signs carry phase information and must be preserved when summing fields.

## Defocus and two-beam imaging

With vacuum wavelength $$\lambda_0$$, medium index $$n_m$$ and lengths in µm, the cutoff is $$\mathrm{NA}/\lambda_0$$ and the paraxial defocus phase is

$$
\phi(f,z)=-\pi\frac{\lambda_0}{n_m}zf^2.
$$

At $$f_s=-1/(2P)$$, orders 0 and +1 lie symmetrically about the pupil center. Their defocus phases match, including in the piston-removed scalar angular-spectrum model. If only those orders pass, the ideal intensity is focus-invariant. This does not imply infinite measured process DOF for finite sources, additional orders or aberrated optics.

For $$\lambda_0=0.248$$ µm, $$P=0.620$$ µm, $$D=0.5$$ and NA=0.50, normal illumination passes orders −1, 0 and +1; tilted illumination with $$\lambda_0f_s=-0.20$$ passes only 0 and +1.

<figure class="study-figure">
  <a class="figure-zoom" href="{{ '/assets/notes/diffraction-defocus/through-focus.png' | relative_url }}"><img src="{{ '/assets/notes/diffraction-defocus/through-focus.png' | relative_url }}" alt="Paraxial three-beam and symmetric two-beam intensity profiles and through-focus maps using a shared raw-intensity color scale." loading="lazy"></a>
  <figcaption>Normal and symmetric tilted illumination at the same pitch and NA. The latter is an ideal two-plane-wave example. No per-row peak normalization is used.</figcaption>
</figure>

## Interpretation and further reading

A three-beam field containing DC and a cosine produces intensity harmonics at both $$1/P$$ and $$2/P$$. A through-focus intensity map is not a Bossung plot: the latter measures CD versus focus under specified dose and threshold conditions. In partial coherence, add fields within each source point, then average intensities across mutually incoherent source points.

The [Korean note]({{ '/ko/notes/diffraction-defocus/' | relative_url }}) includes signed coefficients, pupil diagrams, corrected two-beam presets, physical units and implementation checks. The demo starts with 0/±1 rays and paraxial wave phase. Higher orders and scalar angular-spectrum wave phase are available in the expanded settings. Slider interactions run locally in the browser; the optional through-focus map runs in a separate Worker.
