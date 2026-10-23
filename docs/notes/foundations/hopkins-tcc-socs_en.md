---
layout: technical
category: foundations
title: "Hopkins · TCC · SOCS"
permalink: /notes/foundations/hopkins-tcc-socs/
lang: en
---

# Hopkins · TCC · SOCS

* Contents
{:toc}

## Intuition: compute the optics first, then change the mask

[Abbe imaging]({{ '/notes/abbe-imaging/' | relative_url }}) sums fields for each source point. Hopkins expands that expression and collects source and pupil information into the transmission cross-coefficient, TCC. This makes optical information reusable across many masks under fixed process conditions.

## From Abbe to TCC

Let $$S(\mathbf s)$$ be the normalized weight density of a continuous source. Writing the field in Fourier form gives

$$
I(\mathbf x)=\int S(\mathbf s)\left|\int\widehat m(\mathbf f)P(\mathbf f-\mathbf s)e^{i2\pi\mathbf f\cdot\mathbf x}d\mathbf f\right|^2d\mathbf s.
$$

Expand the squared magnitude as the product of an integral and its complex conjugate, then change the order of integration:

$$
T(\mathbf f,\mathbf g)=\int S(\mathbf s)P(\mathbf f-\mathbf s)P^*(\mathbf g-\mathbf s)d\mathbf s,
$$

$$
I(\mathbf x)=\iint T(\mathbf f,\mathbf g)\widehat m(\mathbf f)\widehat m^*(\mathbf g)e^{i2\pi(\mathbf f-\mathbf g)\cdot\mathbf x}d\mathbf f d\mathbf g.
$$

$$T$$ is mask-independent but depends on source, pupil and focus. Frequencies $$\mathbf f,\mathbf g,\mathbf s$$ are in µm⁻¹; normalize $$S$$ to integrate to 1. Under this normalization $$T$$ is dimensionless, with intensity normalization following the Fourier convention. Separate mask-3D scattering requires reassessing this factorization's scope.

## Why the TCC is Hermitian and positive semidefinite

For discrete sources define $$A_{k,f}=\sqrt{w_k}P_k^*(f)$$. Then $$T=A^\dagger A$$, so $$T_{g,f}=T_{f,g}^*$$ and $$u^\dagger Tu=\|Au\|^2\ge0$$. All eigenvalues are nonnegative, but some can be zero: the general statement is positive **semidefinite**.

## Deriving SOCS and its computation

$$
T=\sum_j\lambda_j q_jq_j^\dagger,\qquad
I(\mathbf x)=\sum_j\lambda_j\left|\mathcal F^{-1}[q_j\widehat m](\mathbf x)\right|^2.
$$

The orthonormal modes $$q_j$$ have weights $$\lambda_j\ge0$$. Absorbing the eigenvalue into $$K_j=\sqrt{\lambda_j}q_j$$ gives $$I=\sum_j|\mathcal F^{-1}[K_j\widehat m]|^2$$. In Nitho, the absence of an explicit eigenvalue does not mean intensity weights are absent. SOCS coherent eigenmodes need not correspond one-to-one to physical illumination points.

For $$F$$ frequency pixels, dense TCC storage requires an $$F\times F$$ complex matrix. At large ROI sizes it can be preferable to apply SVD to a source-pupil factor. GeoSignal's exact path also uses this factor; full-rank cross-validation and truncated-mode experiments are separate.

## What truncation error tells us

If $$\lambda_1\ge\lambda_2\ge\cdots$$ and only the first $$r$$ modes remain, omitted terms are nonnegative within this scalar model, so $$I_r\le I_{full}$$. Small average intensity error does not guarantee small EPE. Near a threshold with a shallow intensity slope,

$$
\delta x\simeq -\frac{\delta I}{\partial I/\partial n}.
$$

The numerator is dimensionless intensity error and the denominator intensity/µm, giving $$\delta x$$ in µm. This local linearization can fail where bridging or pinching changes contour topology. Gate rank selection on CD, EPE and process-window error as well as retained optical energy.

## Using learned kernels

Learning kernels under fixed optical conditions seeks to identify the optical system rather than a mask distribution. However, multiplying kernels by global phases or mixing modes unitarily leaves intensity unchanged. Account for this nonuniqueness and validate aerial-image and contour predictions. Claims about new sources or focus conditions require conditioning on those inputs or retraining the kernels.

## Related reviews and references

* [Nitho]({{ '/notes/research/nitho/' | relative_url }})
* [DOINN]({{ '/notes/research/doinn/' | relative_url }})
* [Nitho paper, Section II](https://arxiv.org/html/2303.08435v4)
* [DOINN paper, Section 2](https://arxiv.org/html/2203.08616v1)
