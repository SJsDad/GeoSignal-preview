---
layout: technical
category: foundations
title: "Abbe Imaging"
permalink: /notes/abbe-imaging/
lang: en
---

# Abbe Imaging

Abbe imaging explains how mask diffraction, pupil filtering and illumination combine to form an aerial image.

---

## Related pages

* [Back to Technical Notes]({{ '/notes/' | relative_url }})
* [Method]({{ '/method/' | relative_url }})
* [Demo]({{ '/demo/' | relative_url }})

## Distinguishing fields from intensity

For one source point, the spatial-frequency components diffracted by the mask interfere. Sum the fields $$E$$ first, then calculate $$|E|^2$$. Contributions from mutually incoherent source points add as intensities. Changing this order changes the physical model.

* Contents
{:toc}

## Pupil and source sampling

Use wafer coordinates $$\mathbf{x}=(x,y)$$ [µm] and spatial frequencies $$\mathbf{f}=(f_x,f_y)$$ [µm⁻¹]. The dimensionless complex amplitude transmittance $$m(\mathbf{x})$$ is 0 or 1 for a binary mask. $$P$$ is the pupil, $$s_k$$ the source-frequency coordinate, and $$w_k\ge0$$ the source intensity weight.

$$
E_k(\mathbf{x};z)=\mathcal{F}^{-1}\{\widehat m(\mathbf f)P_z(\mathbf f-\mathbf s_k)\},\qquad
I(\mathbf{x};z)=\frac{\sum_k w_k|E_k(\mathbf{x};z)|^2}{\sum_k w_k}.
$$

Factoring the illumination carrier out of the field gives the shifted-pupil form. Its sign depends on the Fourier-transform and source-direction conventions and must match the code. GeoSignal's `abbe.py` reuses one mask FFT, applies a shifted pupil for each source, then accumulates weighted squared IFFT magnitudes. Avoid ROI peak normalization when preserving clear-field-relative intensity.

The ideal circular pupil is

$$
P_0(\mathbf f)=\mathbf 1_{\|\mathbf f\|\le f_c},\qquad f_c=\frac{\mathrm{NA}}{\lambda}.
$$

NA is dimensionless and $$\lambda$$ is in µm, so $$f_c$$ is in µm⁻¹. A conventional source has radius $$\sigma f_c$$ with dimensionless $$\sigma$$. A linewidth is not a frequency cutoff. The pupil acts on the field; intensity is quadratic in the field.

## Deriving partial coherence

For $$E=\sum_k a_kE_k$$, the squared magnitude contains cross terms $$a_ka_l^*E_kE_l^*$$. Time averaging independent sources gives $$\langle a_ka_l^*\rangle=0$$ for $$k\ne l$$ and $$\langle |a_k|^2\rangle=w_k$$, producing the weighted intensity sum above. This does not make the mask diffraction orders within one source incoherent.

Two coherent fields of 1 and −1 produce zero intensity when added. Two equally weighted, mutually incoherent sources of those fields have mean intensity 1. An ML architecture that discards phase and uses only amplitude magnitudes cannot readily preserve this distinction.

## Defocus and contours

With time dependence $$e^{-i\omega t}$$, paraxial propagation after removing a global phase can be written as

$$
P_z(\mathbf f)=P_0(\mathbf f)\exp[-i\pi\lambda z\|\mathbf f\|^2].
$$

Here $$z$$ is in µm and the exponent is dimensionless. This homogeneous-medium paraxial example does not replace a high-NA, immersion or vector defocus model. Follow the code's pupil convention for the focus sign.

When relative dose $$d$$ multiplies raw intensity, the contour at fixed threshold $$T_0$$ satisfies $$dI\ge T_0$$, or $$I\ge T_0/d$$. Peak-normalizing each dose changes the dose-to-size relationship. A threshold contour does not replace resist chemistry or etch modeling.

## Connections for computation and validation

Check convergence while considering source count, ROI halo, pixel size and FFT padding together. More source points alone do not guarantee contour accuracy. Evaluate fixed-transect CD and edge displacement as well as intensity error. [Hopkins/TCC/SOCS]({{ '/notes/foundations/hopkins-tcc-socs/' | relative_url }}) expresses the same physics using mask-independent modes.

LMLitho conditions on the illumination source; Nitho learns mask-independent kernels; OptiCo inserts propagation phase as a convolutional inductive bias. Their inputs and physical constraints differ.

## Further reading

* [Diffraction Orders and Defocus: Off-Axis Imaging]({{ '/notes/diffraction-defocus/' | relative_url }}) — Compare three-beam and symmetric two-beam examples.
* [Fourier Optics]({{ '/notes/fourier-optics/' | relative_url }})
* [Nitho paper, Section II](https://arxiv.org/html/2303.08435v4)
* [LMLitho review]({{ '/notes/research/lmlitho/' | relative_url }})
