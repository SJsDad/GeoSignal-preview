---
layout: technical
category: foundations
title: "Diffraction Orders and Defocus: Off-Axis Imaging"
description: Higher diffraction orders, pupil filtering and defocus phase explain three-beam and symmetric two-beam imaging.
permalink: /notes/diffraction-defocus/
lang: en
---

# Diffraction Orders and Defocus: Off-Axis Imaging

Start by following rays from source to wafer through the 6f system. Synthesizing the pupil spectrum, complex field and intensity from the same orders explains both rounded square-mask edges and the focus sensitivity of tilted illumination.

This learning example connects [Fourier Optics]({{ '/notes/fourier-optics/' | relative_url }}) and [Abbe Imaging]({{ '/notes/abbe-imaging/' | relative_url }}). Fields add within each source point; intensities add across mutually incoherent source points. The model uses a thin amplitude mask and scalar propagation in a uniform medium.

{% include diffraction-demo-cta.html %}

* Contents
{:toc}

## 1. Reading the rays in a 6f optical system

Ideal thin lenses with equal focal length $$F$$ give this sequence: source at 0f, condenser at 1f, mask at 2f, objective at 3f, pupil at 4f, imaging lens at 5f and wafer at 6f. The first 2f implements Köhler illumination; the remaining 4f forms the image. Lens focal length $$F$$ is distinct from spatial frequency $$f_j$$.

For paraxial height and slope $$(h,\theta)$$, free propagation and a thin lens obey

$$
\begin{bmatrix}h'\\\theta'\end{bmatrix}
=\begin{bmatrix}1&d\\0&1\end{bmatrix}
\begin{bmatrix}h\\\theta\end{bmatrix},\qquad
\begin{bmatrix}h'\\\theta'\end{bmatrix}
=\begin{bmatrix}1&0\\-1/F&1\end{bmatrix}
\begin{bmatrix}h\\\theta\end{bmatrix}.
$$

Define $$u_s=\lambda_0f_s$$ and $$u_j=u_s+j\lambda_0/P$$, using $$u_j$$ as the paraxial slope. Source height $$-Fu_s$$ gives a collimated slope $$u_s$$ after the condenser. Rays of the same order leaving different mask positions **meet at one pupil height $$Fu_j$$**. Only orders with $$\lvert u_j\rvert\le\mathrm{NA}$$ pass. At the wafer they form the inverted image $$h_i=-h_m$$.

<figure class="study-figure">
  <a class="figure-zoom" href="{{ '/assets/notes/diffraction-defocus/ray-6f.png' | relative_url }}"><img src="{{ '/assets/notes/diffraction-defocus/ray-6f.png' | relative_url }}" alt="6f rays through the source, condenser, mask, objective, pupil, imaging lens and wafer. Under tilted illumination, order minus one stops at the pupil." loading="lazy"></a>
  <figcaption>Figure 1. Normal three-beam and symmetric tilted two-beam ray paths. Gold: order 0; red: +1; green: −1. λ₀=248 nm, P=620 nm, D=0.5, NA=0.50, using the same transmission conditions as the wave examples.</figcaption>
</figure>

Vertical height in the ray drawing becomes horizontal position in the wafer wave plot. Away from best focus, paraxial rays follow $$h_i(z)=-h_m-zu_j$$. The demo magnifies only this small focus-plane displacement by 2000 for visibility; wave phase uses the actual focus in µm. The ray model is paraxial, while the angular-spectrum wave option is a separate scalar propagation model.

## 2. Coordinates and units

All lengths are wafer-side; reduction magnification is not included separately.

| Symbol | Meaning | Unit |
| --- | --- | --- |
| $$x,P,w$$ | Position, mask pitch, opening width | µm |
| $$D=w/P$$ | Duty ratio | Dimensionless |
| $$\lambda_0$$ | Vacuum wavelength | µm |
| $$n_m$$ | Refractive index of the uniform medium | Dimensionless |
| $$\mathrm{NA}=n_m\sin\theta_{\max}$$ | Numerical aperture | Dimensionless |
| $$f_0=1/P,\ f_s$$ | Fundamental and illumination spatial frequencies | cycles/µm |
| $$z$$ | Signed defocus from ideal best focus | µm |

The integer order index $$j$$ is distinct from refractive index $$n_m$$. Illumination obeys $$f_s=n_m\sin\theta_s/\lambda_0$$; $$f_s$$ is not itself an angle. The pupil cutoff is $$f_c=\mathrm{NA}/\lambda_0$$.

Dimensionless examples use $$u=\lambda_0 f$$, $$\xi=x/\lambda_0$$ and $$\zeta=z/\lambda_0$$, giving cutoff $$\lvert u\rvert\le\mathrm{NA}$$. Do not mix this convention with lengths normalized by $$\lambda_0/\mathrm{NA}$$.

## 3. Decomposing a square mask into diffraction orders

A periodic mask transmitting a centered opening of width $$w$$ has complex Fourier series

$$
m(x)=\sum_{j=-\infty}^{\infty}c_j e^{i2\pi jx/P},\qquad
c_j=\frac{1}{P}\int_{-w/2}^{w/2}e^{-i2\pi jx/P}\,dx
=D\,\operatorname{sinc}(jD).
$$

Here $$\operatorname{sinc}(v)=\sin(\pi v)/(\pi v)$$ matches NumPy's `np.sinc`. Thus $$c_0=D$$ and, for $$j\ne0$$, $$c_j=\sin(\pi jD)/(\pi j)$$. The DC coefficient is mean **amplitude transmittance**: passing only DC gives intensity $$D^2$$. This differs from the full binary mask's mean intensity $$D$$ over one period.

At $$D=0.5$$ all nonzero even orders vanish, so adding ±2 does not recover missing edges. Odd orders ±3, ±5 and beyond contribute instead. At $$D=0.3$$ even orders generally remain.

<figure class="study-figure">
  <a class="figure-zoom" href="{{ '/assets/notes/diffraction-defocus/fourier-orders.png' | relative_url }}"><img src="{{ '/assets/notes/diffraction-defocus/fourier-orders.png' | relative_url }}" alt="Signed Fourier coefficients for duty ratios 0.5 and 0.3. Nonzero even orders vanish at 0.5, and some odd-order coefficients are negative." loading="lazy"></a>
  <figcaption>Figure 2. Coefficient signs encode complex-amplitude phase. Replacing negative coefficients with their magnitudes before field synthesis changes the image.</figcaption>
</figure>

A finite-order reconstruction of a discontinuous mask can retain Gibbs oscillations near edges. Adding orders does not guarantee monotonic convergence of the intensity curve to a perfect square.

## 4. Reading illumination direction and pupil together

Including the illumination carrier, define the pupil frequencies and amplitudes by

$$
f_j=f_s+\frac{j}{P},\qquad
A_j(z)=c_j\,\mathbf 1_{|f_j|\le f_c}\,e^{i\phi(f_j,z)},\qquad
I(x_i,z)=\left|\sum_j A_j(z)e^{-i2\pi jx_i/P}\right|^2.
$$

$$x_i$$ is the actual wafer coordinate. Equal-focal-length 4f imaging gives $$x_i=-x$$ relative to the corresponding mask coordinate, hence the negative exponent. The omitted common carrier $$e^{-i2\pi f_sx_i}$$ does not affect intensity. When comparing independent formulations, align the source-sign convention and image inversion. Asymmetric illumination away from best focus is useful for checking these signs.

<figure class="study-figure">
  <a class="figure-zoom" href="{{ '/assets/notes/diffraction-defocus/pupil-comparison.png' | relative_url }}"><img src="{{ '/assets/notes/diffraction-defocus/pupil-comparison.png' | relative_url }}" alt="One pupil passing orders minus one, zero and plus one under normal illumination, versus only zero and plus one under symmetric tilted illumination. The pupil coordinate is wavelength times spatial frequency." loading="lazy"></a>
  <figcaption>Figure 3. λ₀=248 nm, P=620 nm, D=0.5, NA=0.50, in air. Tilted orders 0 and +1 are symmetric at u=−0.20,+0.20. Stem height is |cⱼ|; gray indicates blocked orders.</figcaption>
</figure>

A chosen maximum order $$N$$ limits the sum to $$-N\le j\le N$$. The actual integer interval admitted by the pupil is

$$
\left\lceil P(-f_c-f_s)\right\rceil\le j\le
\left\lfloor P(f_c-f_s)\right\rfloor.
$$

A fixed ±5 limit therefore need not suffice for every setting. Distinguish physical pupil blocking from deliberate user-selected order truncation.

## 5. Where quadratic defocus phase comes from

With time dependence $$e^{-i\omega t}$$ in a uniform medium,

$$
k_z=\frac{2\pi}{\lambda_0}\sqrt{n_m^2-(\lambda_0 f)^2}.
$$

Removing the intensity-invariant piston gives scalar angular-spectrum phase

$$
\phi_{\mathrm{AS}}(f,z)=\frac{2\pi z}{\lambda_0}
\left[\sqrt{n_m^2-(\lambda_0 f)^2}-n_m\right].
$$

Expanding the square root for $$\lvert\lambda_0f\rvert\ll n_m$$ gives

$$
\phi_{\mathrm{paraxial}}(f,z)=-\pi\frac{\lambda_0}{n_m}zf^2,\qquad
P_z(f)=\mathbf 1_{|f|\le f_c}\,e^{i\phi(f,z)}.
$$

In air, $$n_m=1$$ yields the familiar $$-\pi\lambda_0zf^2$$. Dimensionless phase is $$\phi=-\pi\zeta u^2/n_m$$. At high NA, distinguish paraxial and angular-spectrum phases. The latter remains scalar here; it does not solve vector, polarization, mask-3D or real-lens aberration effects.

## 6. Focus sensitivity of three-beam and two-beam imaging

### Normal illumination: DC and first orders gain different phases

When only 0 and ±1 pass and mask coefficients are real,

$$
E(x,z)=c_0+2c_1e^{i\delta(z)}\cos(2\pi x/P),\qquad
\delta(z)=\phi(1/P,z)-\phi(0,z).
$$

Therefore

$$
I=c_0^2+4c_1^2\cos^2(2\pi x/P)
+4c_0c_1\cos(2\pi x/P)\cos\delta.
$$

Although the field is DC plus a cosine, **intensity is not a single sinusoid**. The squared cosine also produces a $$2/P$$ harmonic. Defocus changes the magnitude and sign of $$\cos\delta$$, weakening or reversing the fundamental pitch component. Higher-harmonic intensity modulation can remain when the fundamental vanishes.

### Symmetric tilted illumination: two orders gain the same phase

For $$f_s=-1/(2P)$$, orders 0 and +1 pass at $$-1/(2P),+1/(2P)$$. Equal frequency magnitudes give equal paraxial and angular-spectrum phases. **If only these two orders remain**, defocus is a common phase and cancels from intensity.

The geometrical condition for only two transmitted orders is

$$
\frac{1}{2P}\le\frac{\mathrm{NA}}{\lambda_0}<\frac{3}{2P}.
$$

This is focus invariance of ideal two-plane-wave interference. Finite source width, other orders, asymmetry or aberrations generally break it. A symmetric pair of ideal equal-strength source points also differs from a real dipole source of finite width.

The two order amplitudes need not be equal. For $$D=0.5$$, $$c_0=0.5$$ and $$c_1=1/\pi$$ give about 90.6% Michelson contrast, rather than 100%.

<figure class="study-figure">
  <a class="figure-zoom" href="{{ '/assets/notes/diffraction-defocus/through-focus.png' | relative_url }}"><img src="{{ '/assets/notes/diffraction-defocus/through-focus.png' | relative_url }}" alt="Paraxial through-focus intensity maps for normal three-beam and symmetric tilted two-beam imaging. The former changes with focus; the ideal two-beam profile remains invariant." loading="lazy"></a>
  <figcaption>Figure 4. Same conditions as Figure 3, with position x/P and physical defocus in µm. Both maps share a raw-intensity scale with no per-row peak normalization. This is not a CD/Bossung curve or measured process DOF.</figcaption>
</figure>

## 7. Experimental conditions to compare in the demo

Here $$u_s=\lambda_0f_s$$ and $$u_0=\lambda_0/P$$ are dimensionless. At 248 nm wavelength, $$u_0=0.40$$ corresponds to pitch 620 nm.

| Experiment | $$u_s$$ | $$u_0$$ | NA | D | What to check |
| --- | --- | --- | --- | --- | --- |
| Normal 3-beam | 0 | 0.40 | 0.50 | 0.50 | Orders 0 and ±1 acquire different defocus phases |
| Symmetric 2-beam | −0.20 | 0.40 | 0.50 | 0.50 | Orders 0 and +1 acquire equal phases |
| Even-order example | 0 | 0.20 | 0.70 | 0.30 | Several orders, including ±2, pass |

A counterexample is $$u_s=-0.22$$, $$u_0=0.45$$, $$\mathrm{NA}=0.70$$, $$D=0.50$$: order −1 at $$u=-0.67$$ still passes, so this is not two-beam imaging. Changing only illumination to −0.225 does not block it. To keep $$u_0=0.45$$, use, for example, $$u_s=-0.225$$ and adjust the pupil to $$\mathrm{NA}=0.60$$.

## 8. Partial coherence, DOF and Bossung curves

For mutually incoherent source points $$s$$ with weights $$w_s$$,

$$
I(x_i,z)=\frac{\sum_s w_s\left|\sum_j A_{s,j}(z)e^{-i2\pi jx_i/P}\right|^2}{\sum_s w_s}.
$$

Add **fields** within one source, but **intensities** across sources. A single $$f_s$$ slider does not implement partial coherence from a finite source distribution.

A through-focus map displays $$I(z,x)$$. Reporting DOF requires an acceptance criterion—contrast, CD error at fixed threshold, or another specification—and the passing focus interval containing best focus. A Bossung curve is CD versus focus, usually compared across doses; it is a different quantity.

Compute contrast over a full period and preserve raw intensity. Normalizing each focus row independently can change brightness, dose and threshold relationships. Threshold contours do not replace resist response or wafer measurements.

## 9. Computation and validation

Reuse coefficients, order frequencies, aperture and spatial-phase matrices for fixed mask/optical conditions. Changing only current focus requires updating the 1D image and map marker, not recalculating the entire sweep. Check for missing admitted orders and sample the intensity sufficiently to resolve order-difference frequencies.

Useful checks include even-order zeros at D=0.5, $$I=D^2$$ with DC only, symmetric two-beam focus invariance, agreement between a single focus and the corresponding sweep row, and source signs under asymmetric illumination. Separate computation time from web latency; fixed 1 ms or 60 fps performance is not a property guaranteed by the model.

The figures above are static examples generated by reproducible NumPy calculations. Open the interactive display through the [button above](#interactive-demo) or the [simulator link]({{ '/simulator/' | relative_url }}). It runs directly on GitHub Pages without a Render cold start. The default shows 0/±1 rays and paraxial waves; higher orders and angular-spectrum phase are in the expanded settings. Sliders calculate and draw locally in the browser; the expanded through-focus map uses a separate Worker. Wavelength and pitch use nm, defocus uses µm, and illumination is a dimensionless spatial frequency.

## Related notes and references

* [Fourier Optics · FFT]({{ '/notes/fourier-optics/' | relative_url }}) — Spatial frequency, sampling and intensity bandwidth
* [Abbe Imaging]({{ '/notes/abbe-imaging/' | relative_url }}) — Source-specific fields and partial-coherence intensity sums
* [Hopkins · TCC · SOCS]({{ '/notes/foundations/hopkins-tcc-socs/' | relative_url }}) — Alternative computation of the same imaging physics
* [v0.11 sampling benchmark]({{ '/release-notes/v0.11/' | relative_url }}) — Periodic references and separate source/raster errors
* [NumPy `sinc` definition](https://numpy.org/doc/stable/reference/generated/numpy.sinc.html)
* J. W. Goodman, *Introduction to Fourier Optics* — Standard reference for coherent imaging and spatial-frequency filtering
