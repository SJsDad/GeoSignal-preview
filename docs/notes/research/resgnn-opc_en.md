---
layout: technical
category: research
paper_id: resgnn-opc
title: "ResGNN-OPC — Residual Graph Updates for OPC"
permalink: /notes/research/resgnn-opc/
lang: en
---

# ResGNN-OPC: Residual Graph Updates for OPC

* Contents
{:toc}

<div class="evidence-note">Access-limited review. Verified official Optica authors, affiliations, abstract, Data Availability, Table 1 and the total of ten figures. Subscription limits prevented reading the full text, seven equations and figure images/captions. GNN equations below are explanatory examples, not the paper's verified equations.</div>

## Paper Information

| Item | Verified information |
| --- | --- |
| Title | ResGNN-OPC: a fast optical proximity correction approach based on an interpretable residual graph neural network |
| Authors/affiliations | Jingqing Liu, Xu Ma; School of Optics and Photonics, Beijing Institute of Technology; Key Laboratory of Photoelectronic Imaging Technology and System |
| Publication | Applied Optics 64(15), 4227–4234, 2025 |
| Sources | [DOI](https://doi.org/10.1364/AO.561432) · [Official article](https://opg.optica.org/ao/abstract.cfm?uri=ao-64-15-4227) · [PDF entry](https://opg.optica.org/ao/viewmedia.cfm?uri=ao-64-15-4227&seq=0) |
| Data | Official Data Availability says data are not public and may be obtained from the authors upon reasonable request |
| Code/weights | No official public repository or pretrained weights verified |
| Task | OPC correction prediction using a residual graph neural network |

## Executive Summary

**One sentence:** residual updates in graph convolutions create a correction predictor whose stages resemble iterative MBOPC updates.

Predicting movements on existing edges/control points can fit naturally into OPC workflows. Residual connections carry features forward while adding learned increments. The interpretability claim starts from this structural resemblance. However, resemblance to OPC iterations does not prove physically equivalent updates; full graph features, supervision and losses were unavailable.

## Background & Motivation

MBOPC repeatedly calculates contours and updates edge displacements. Segment-specific geometry dependencies motivate a graph rather than a flat image. A sparse graph can represent neighboring-edge relationships directly.

GNN layers update features through neighbor aggregation. Greater depth spreads information but can introduce oversmoothing and training difficulty. Residual paths may preserve features and gradients; whether they represent the correct optical interaction range depends on graph construction.

## Physics & Mathematical Foundations

### MBOPC updates and residual GNNs — independent example

A generic update for edge position $$u^{(t)}$$ [nm] and contour mismatch $$e^{(t)}$$ [nm] is

$$
u^{(t+1)}=u^{(t)}+\Delta u^{(t)},\qquad \Delta u^{(t)}=F(e^{(t)},\text{local geometry},p).
$$

An illustrative residual GNN is

$$
h_i^{(\ell+1)}=h_i^{(\ell)}+\psi_\ell\left(h_i^{(\ell)},\operatorname{AGG}_{j\in\mathcal N(i)}\phi_\ell(h_i^{(\ell)},h_j^{(\ell)},a_{ij})\right).
$$

$$h_i$$ is a node embedding, $$a_{ij}$$ an edge feature and $$\mathcal N(i)$$ the neighbors. AGG is a permutation-invariant sum/mean or similar operation. Embeddings are generally dimensionless; a final projection supplies movement units. These $$\phi,\psi$$, aggregation and feature definitions are explanatory, not verified ResGNN-OPC details.

For $$N$$ nodes and $$C$$ features, a conceptual shape is $$H\in\mathbb R^{N\times C}$$ with sparse adjacency. The encoding of segment position, length, normals and proximity remains unverified.

### Optical interaction range and graph depth

$$L$$ layers reach an $$L$$-hop neighborhood, but the graph policy sets each hop's physical distance. Check whether edges encode spatial distance, optical interaction or polygon relationships. Depth alone does not establish coherent diffraction support.

When relating graph neighborhoods to nonlocal [Abbe imaging]({{ '/notes/abbe-imaging/' | relative_url }}), distinguish explicit wave calculations from learned geometry correlations. The public abstract supports iteration-inspired residual structure, not an exact optical kernel embedded in each GNN layer.

## Proposed Method / Model Architecture

The abstract describes residual structure in graph-convolution layers to improve depth and correction fitting, aiming to reduce subsequent MBOPC iterations.

<figure class="study-figure">
<a class="figure-zoom" href="{{ '/assets/notes/research/resgnn-opc.svg' | relative_url }}"><img src="{{ '/assets/notes/research/resgnn-opc.svg' | relative_url }}" alt="Independent explanation of neighbor aggregation and residual increments in a generic GNN" width="1100" height="520" loading="lazy"><span class="figure-zoom-label">Enlarge ↗</span></a>
<figcaption>A generic residual GNN diagram, not a reconstruction of the paper's unverified graph definition, module arrangement or figures.</figcaption>
</figure>

Layer count, feature dimensions, activation, loss, correction-label generation, graph normalization, splits and hardware were not verified. Neither end-to-end differentiable optical loss nor a PINN residual was confirmed.

**Physics-informed/guided assessment:** public evidence establishes iteration-inspired topology. The exact placement of enforced physical equations in inputs, layers, losses or optimization is unknown. “Interpretable” does not mean “physics-enforced.”

## Figures & Visual Explanation

{% include figure-coverage.html %}

Official figure links cover Fig. 1–10. Captions, axes, colors, subfigures and loss curves were unavailable, so no detailed explanations are invented: **0/10 detailed figure readings are complete**. Official Table 1 is publicly readable and interpreted below.

## Experiments & Results

Official Table 1 reports averages over test layouts. Wavelength, NA, source, layout count and hardware were not verified on the public page.

| Method | Correction prediction error [nm] | Runtime [s] | Initial EPE [nm] | Corrected EPE [nm] |
| --- | ---: | ---: | ---: | ---: |
| Conventional MBOPC | — | 17.6299 | 7.21 | 2.43 |
| RGCN-OPC | 2.17 | 0.0022 | 7.21 | 4.33 |
| ResGNN-OPC | 1.27 | 0.0029 | 7.21 | 3.02 |

**Independent calculation:** $$(2.17-1.27)/2.17\approx41.5\%$$ less prediction error and runtime ratio $$17.6299/0.0029\approx6079$$. The table alone does not establish whether refinement, training or graph construction is included.

Read accuracy and speed together: ResGNN improves correction prediction relative to RGCN with slightly more runtime, but final EPE 3.02 nm remains above MBOPC's 2.43 nm. It is incorrect to claim 6000× speedup with identical final EPE. The abstract mentions fewer subsequent iterations; condition-specific counts need full-text verification.

Correction error and printed-contour EPE assess different targets. Optical nonlinearity prevents matching movement labels from guaranteeing matching contour error. See [Metrics]({{ '/notes/foundations/inverse-and-metrics/' | relative_url }}).

## Critical Analysis & Limitations

**Contribution:** residual updates offer an interpretable interface for vector/edge OPC workflows. **Verified limits:** private data, unknown optical conditions, and unavailable graph features, loss and figures.

Graphs may depend strongly on polygon segmentation, segment length and control-point placement. Different segmentations of one shape can change node counts and aggregation weights; check segmentation invariance or robustness. Residual architecture does not guarantee convergence or monotonically lower EPE. Updates can accumulate errors or violate mask rules, so optical verification, movement bounds and MRC remain necessary. Numerical results are not wafer experiments.

## Practical Applications to GeoSignal / OPC

* **Available idea:** link geometry candidates and contour gauges to persistent edge identities. GeoSignal currently has no automatic edge correction.
* **Further research / Hypothesis:** first build a solver producing MBOPC labels for public synthetic layouts; compare initial predictions and post-refinement EPE/runtime separately.
* **Long term / Hypothesis:** add optical sensitivities and process-window constraints to graph updates, rechecking stability when combining a correction predictor with differentiable imaging.

## Key Takeaways & References

1. GNNs express geometry dependencies as nodes and edges.
2. Equivalence to actual MBOPC updates needs independent validation.
3. Read Table 1 runtime ratios together with final EPE.
4. Correction prediction error and EPE are different metrics.
5. Private-data results do not establish public-benchmark rankings.

[GeoSignal scope]({{ '/notes/research/geosignal-scope/' | relative_url }}) · [TokMan]({{ '/notes/research/tokman/' | relative_url }}) · [Inverse Problem]({{ '/notes/foundations/inverse-and-metrics/' | relative_url }})
