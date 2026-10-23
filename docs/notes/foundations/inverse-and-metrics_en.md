---
layout: technical
category: foundations
title: "Inverse Problem · Gradient · Metrics"
permalink: /notes/foundations/inverse-and-metrics/
lang: en
---

# Inverse Problem · Gradient · Metrics

* Contents
{:toc}

## Forward versus inverse problems

A forward problem maps mask $$M$$ and optical conditions $$p$$ to intensity $$I$$ or resist/contour $$R$$. An inverse problem seeks a mask that prints target $$T$$. A fast forward surrogate needs useful mask gradients as well as accurate predictions to support inverse optimization.

$$
\min_{M\in\mathcal C}\mathcal L(g(M;p),T)+\beta\Omega(M).
$$

Here $$g$$ is the simulator, $$\mathcal C$$ the feasible set (binary, Manhattan or mask rules), $$\Omega$$ a regularizer and $$\beta$$ its weight. CNNs, VAEs and diffusion models can propose initial masks; GNNs can directly predict edge displacements. Different objectives and constraints should not be merged into one performance ranking.

## Differentiable simulation and gradients

$$
M_{t+1}=\Pi_{\mathcal C}\left(M_t-\eta\left[\left(\frac{\partial g}{\partial M}\right)^\top\frac{\partial\mathcal L}{\partial g}+\beta\nabla_M\Omega\right]\right).
$$

$$\eta$$ is a step size and $$\Pi$$ a projection. Binary projection is discontinuous; practical training may use sigmoid relaxation, a straight-through estimator or geometry parameterization. Being able to invoke automatic differentiation on a hard threshold does not imply a meaningful gradient.

For SOCS fields $$E_j=H_jM$$, $$\delta I=2\operatorname{Re}\sum_jE_j^*H_j\delta M$$. Match FFT adjoints, conjugation and normalization in code. A surrogate with low pixel error can still have incorrect $$\partial g/\partial M$$, allowing the optimizer to exploit its errors. Reevaluate the final mask with an independent reference engine.

## Image metrics and units

$$
\mathrm{MSE}=\frac1N\sum_p(\widehat I_p-I_p)^2,\qquad
L_{2,\mathrm{sum}}=\sum_p(R_p-T_p)^2.
$$

MSE has squared intensity units, or is dimensionless for normalized intensity. For binary $$R,T$$, $$L_{2,\mathrm{sum}}$$ equals the XOR pixel count. Multiply by pixel area $$a_{px}$$ to obtain nm². Papers sometimes label sums as MSE or L2, so inspect normalization before the metric name.

$$
\operatorname{IoU}=\frac{|R\cap T|}{|R\cup T|}.
$$

IoU is dimensionless. Foreground IoU, foreground/background class means and image means differ. Depending on the paper, mPA may mean overall pixel accuracy or mean class recall. Background-heavy layouts can score high pixel accuracy while missing critical edges.

## EPE and CD

For target-edge merit point $$x_i$$ with normal $$n_i$$ and printed-contour intersection $$y_i$$, one signed EPE definition is $$e_i=(y_i-x_i)\cdot n_i$$ [nm]. Mean absolute EPE is $$N^{-1}\sum_i|e_i|$$; violation count is $$\sum_i\mathbf1_{|e_i|>\tau}$$. Do not compare counts and nm values in one column.

Define missing intersections, multiple intersections and corner normals explicitly. CD measures the distance between two intersections on the same transect. Equal-direction errors on both edges can shift a pattern without changing CD; CD and EPE therefore complement one another.

## Process variation band and process window

$$
\mathrm{PVB}_{area}=a_{px}\sum_p\left[\max_{c\in\mathcal P}R_c(p)-\min_{c\in\mathcal P}R_c(p)\right].
$$

Here $$c$$ is a focus/dose condition and $$\mathcal P$$ the evaluated corner set. The expression measures the area between the union and intersection of binary contours. It can correspond to an XOR band for two ordered corners, but multiple conditions or topology changes require an explicit extremum definition. A soft-image MSE-based PVB loss differs from final binary PVB area.

DOF is the accepted focus interval under stated CD/EPE specifications and dose conditions. Bossung curves show CD versus focus at specified doses; a process window is the focus/dose region passing the specifications. A small PVB alone is insufficient if all contours miss the target together.

## Comparing runtime, shots and generalization

Separate inference, ILT refinement, source/TCC setup, CPU–GPU transfers, I/O and training cost. Mask shot count is the rectangle count from a specified fracturing algorithm; it is not equivalent to actual multibeam write time.

Distinguish OOD shape tests from transfer to a new process. Predicting metal after training on vias under the same NA/source does not validate a new scanner, resist or focus/dose range. Fine-tuning on new-process data is not zero-shot generalization.

## Related resources

* [Research Overview]({{ '/notes/research/' | relative_url }})
* [Official LithoBench code](https://github.com/shelljane/lithobench)
* [Official LithoSim project](https://dw-hongquan.github.io/LithoSim/)
