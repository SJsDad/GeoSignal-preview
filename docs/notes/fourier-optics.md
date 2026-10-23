---
layout: technical
category: foundations
title: "Fourier Optics"
permalink: /notes/fourier-optics/
lang: en
---

# Fourier Optics

Fourier optics connects mask geometry, spatial-frequency filtering and image formation. FFTs make these calculations practical on a sampled grid.

---

## Related pages

* [Back to Technical Notes]({{ '/notes/' | relative_url }})
* [Method]({{ '/method/' | relative_url }})
* [Demo]({{ '/demo/' | relative_url }})

## From Fourier optics to the FFT

The FFT efficiently computes a Fourier transform; it is not a physical law. Using an FFT layer in an ML model does not by itself ensure optical consistency.

* Contents
{:toc}

## Spatial frequency and the convolution theorem

We use the transform convention

$$
\widehat m(\mathbf f)=\int m(\mathbf x)e^{-i2\pi\mathbf f\cdot\mathbf x}\,d\mathbf x,\qquad
m(\mathbf x)=\int\widehat m(\mathbf f)e^{i2\pi\mathbf f\cdot\mathbf x}\,d\mathbf f.
$$

Coordinates $$x,y$$ are in µm and frequencies $$f_x,f_y$$ in µm⁻¹. The continuous 2D transform $$\widehat m$$ has an integration dimension of µm²; a discrete FFT array depends on the chosen normalization. Do not mix continuous and discrete values while silently dropping area factors.

For shift-invariant coherent imaging with amplitude impulse response $$h$$,

$$
E(\mathbf x)=(h*m)(\mathbf x)=\int h(\mathbf x-\boldsymbol\xi)m(\boldsymbol\xi)d\boldsymbol\xi,
\qquad \widehat E=\widehat h\widehat m=P\widehat m.
$$

Fourier-transforming the integral and substituting $$\mathbf u=\mathbf x-\boldsymbol\xi$$ separates the transforms of $$m(\boldsymbol\xi)$$ and $$h(\mathbf u)$$ into a product. In the continuous formulation, choosing units µm⁻² for $$h$$ makes $$E$$ a normalized dimensionless amplitude.

## FFT grids and aliasing

For an $$N_x\times N_y$$ grid with spacing $$\Delta x,\Delta y$$ [µm],

$$
\Delta f_x=\frac{1}{N_x\Delta x},\qquad f_{\mathrm{Nyquist},x}=\frac{1}{2\Delta x}.
$$

A 2000-pixel-wide ROI with 1 nm pixels spans 2 µm and has frequency spacing 0.5 µm⁻¹. Increasing the ROI width at fixed pixel spacing narrows the frequency interval. Reusing the same mode index in an FNO therefore does not guarantee the same physical frequency. This matters for DOINN's large-tile strategy.

`fft2` assumes periodic boundaries. `fftshift` is an index permutation that centers DC, not an optical operation. Keep the mask spectrum and kernel in the same shifted or unshifted convention. Zero padding can reduce wrap-around but cannot reconstruct missing geometry outside the ROI. Include surrounding patterns in a halo and crop the valid core.

## Pupil cutoff and intensity bandwidth

Even when the coherent field is limited by pupil cutoff $$f_c$$, $$I=EE^*$$ involves a frequency-domain autocorrelation. Its bandwidth differs from the field cutoff: differences $$f_1-f_2$$ between field frequencies appear in intensity. Distinguish field and intensity support when designing kernel dimensions and sampling grids.

## FNO layers versus physical convolution

A typical Fourier layer mixes channels with learned frequency-dependent weights $$R$$:

$$
v_{\ell+1}=\rho\{W_\ell v_\ell+\mathcal F^{-1}[R_\ell(\mathbf f)\mathcal F(v_\ell)]\}.
$$

Here $$v$$ is a latent feature, $$W,R$$ are learned weights and $$\rho$$ an activation. This resembles an optical computation but does not automatically enforce kernel support, Hermitian symmetry, nonnegative intensity or source incoherence. DOINN combines a global Fourier branch with a local CNN; Nitho fixes the physical synthesis formula and learns the kernels.

## Computing complex layers

$$
(a+ib)*(c+id)=(a*c-b*d)+i(a*d+b*c).
$$

Four real convolutions implement this expression. For example, $$(1+i)(1-i)=2$$ because the imaginary parts cancel. Applying separate nonlinearities to real and imaginary channels generally does not define a complex analytic function. Automatic differentiation with respect to real parameters is distinct from satisfying the Cauchy–Riemann conditions.

## References and next steps

* [Diffraction Orders and Defocus: Off-Axis Imaging]({{ '/notes/diffraction-defocus/' | relative_url }}) — Explore pupil, phase and image formation with a periodic mask.
* [Abbe Imaging]({{ '/notes/abbe-imaging/' | relative_url }})
* [Hopkins/TCC/SOCS]({{ '/notes/foundations/hopkins-tcc-socs/' | relative_url }})
* [DOINN paper, Section 3](https://arxiv.org/html/2203.08616v1)
* [Nitho paper, Section III](https://arxiv.org/html/2303.08435v4)
