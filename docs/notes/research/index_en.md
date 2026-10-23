---
layout: technical
category: research
title: "OPC ML/DL Research Paper Reviews"
permalink: /notes/research/
lang: en
---

# OPC ML/DL Research Paper Reviews

* Contents
{:toc}

## Learning goals and reading order

These notes compare **which physical information enters which learned representation**, rather than ranking papers. Read the five recent studies first, then revisit their foundations through TEMPO, DOINN and Nitho. Each review identifies abstract-only or partial-text access. Having every review page does not mean every source and supplement has been fully verified.

Start with [Physics & Math Foundations]({{ '/notes/foundations/' | relative_url }}) for Abbe, FFT, TCC/SOCS, inverse gradients and metrics. Relate implementation ideas to [GeoSignal's current scope]({{ '/notes/research/geosignal-scope/' | relative_url }}), and check unfinished verification in [Source Access, Figure Coverage and Reuse]({{ '/notes/research/sources/' | relative_url }}).

## Browse papers

Combine year, field and architecture filters. Without JavaScript, the complete table and all links remain available.

{% include research-catalog.html %}

## Development of OPC ML/DL research

| Research direction | Examples here | Changing question |
| --- | --- | --- |
| 2020 · Conditional image modeling | TEMPO | Can geometry and film heights share one generator? |
| 2022 · Global/local frequency modeling | DOINN | Can broad optical context and fine edges be represented efficiently together? |
| 2023 · Separating physical computation from learning | Nitho | Can known mask operations remain fixed while only optical kernels are identified? |
| 2025 · Expanded input/output representations | LMLitho, TokMan, ResGNN-OPC | Which fits the task: source-conditioned resist, geometry tokens or edge-graph updates? |
| 2026 · Optical priors and hybrid refinement | OptiCo, Hi-ILT | How can phase priors and learned initializers guide physical optimization? |

CNN→FNO→physics-informed→Transformer/generative describes some design axes, not a single lineage replacing all predecessors. Nitho's small MLP and LMLitho's large Transformer do not solve an identical problem under identical conditions. Transformers, GANs, VAEs and diffusion can have different representations and supervision.

## Forward Modeling and Inverse Optimization

Forward modeling predicts intensity $$I$$ or resist/contour $$R$$ from mask $$M$$ and optical/process conditions $$p$$. Inverse optimization finds a mask printing target $$T$$:

$$
\text{Forward: }\widehat R=f_\theta(M,p),\qquad
\text{Inverse: }M^*=\arg\min_{M\in\mathcal C}\mathcal L(g(M,p),T).
$$

Low prediction error can help inverse optimization, but incorrect surrogate gradients can steer masks incorrectly. Verify final masks with an independent reference. [Inverse Problem · Metrics]({{ '/notes/foundations/inverse-and-metrics/' | relative_url }}) explains the chain rule and EPE definitions.

## Inputs, outputs and architectures

| Paper | Main input | Main output | Representation | Physics entry point |
| --- | --- | --- | --- | --- |
| OptiCo | Target; mask for separate forward tasks | Optimized mask; aerial/resist | Complex convolution + OP kernel | Layer phase priors/residual branches; TV is separate manufacturing regularization |
| Hi-ILT | Target | Initial → ILT-refined mask | Lightweight hierarchical VAE/CNN + ILT | Subsequent physical optimization; VAE internals unverified |
| LMLitho | Source map + mask | Resist image | ViT, source/cross-attention, decoder | Input conditioning, learned interaction and commercial labels |
| TokMan | Segmented Manhattan points | Axis corrections/rendered mask | Point/polygon tokens + diffusion Transformer | Geometry priors, differentiable simulation loss and post-ILT |
| ResGNN-OPC | Mask-related geometry graph | OPC correction | Residual graph convolution | Iteration-inspired topology; exact physical features/loss unknown |
| TEMPO | Mask; thin aerial in Scheme 2; film height | Thick-mask aerial slice | Height-conditioned cGAN | Conditions, physical intermediate inputs and rigorous labels |
| DOINN | Mask | Resist/contour | Fourier GP + CNN LP + reconstruction | Optical-FFT-like architecture prior |
| Nitho | Training: kernel coordinates plus mask/aerial pairs; inference: mask | Kernels, aerial, threshold resist | Complex neural field + fixed SOCS | Mask-independent kernels and fixed synthesis |

**The label “physics-informed” is insufficient.** Physical input features, constrained layers, PDE-residual losses and simulator-guided optimization are distinct approaches. These eight papers do not all use PDE-residual PINNs.

## Metrics and benchmark comparisons

| Study | Reference/dataset | Metrics to inspect | Why direct cross-paper ranking fails |
| --- | --- | --- | --- |
| OptiCo | LithoBench MetalSet/ViaSet, StdMetal/StdContact | Inverse MSE/PVB/EPE violations; forward MSE/IoU | Forward/inverse scales differ; EPE is a count |
| Hi-ILT | Public ICCAD 2013 32 nm and 45 nm LithoBench claims | Maximum L2/PVB/EPE/TAT improvements | Individual baselines, tables and process settings unknown |
| LMLitho | Commercial labels, 28/20 nm, BenchOPC | mIoU/mPA, mean EPE [nm], mask L2/PVB | Source conditions, fine-tuning and CPU/GPU differences |
| TokMan | ICCAD13-S/L | Mean EPE, shots, TAT | Mean distance rather than violations; refinement included |
| ResGNN-OPC | Private numerical data | Correction error, EPE [nm], runtime | Unknown optics, dataset and cost boundaries |
| TEMPO | DUV contacts, 13 film heights, Sentaurus | RMSE/NRMSE, central-contact CD | Topography task, 7.5 nm XY pitch, not inverse design |
| DOINN | ISPD vias, ICCAD metal, N14 | mIoU/mPA, throughput | L/H sampling and large-tile conditions differ |
| Nitho | ICCAD Lithosim, ISPD Calibre | Aerial MSE/PSNR, mIoU, shape OOD | Reference systems, retrained baselines and kernel caching |

Even identical benchmark names can hide different versions, splits, mask stages, optical models, pixel spacing, thresholds and metric implementations. Explain within-paper comparisons without inventing an absolute cross-paper SOTA ranking.

### Reading representative numbers correctly

* OptiCo Table 1 has low OOD EPE, but higher mean PVB than DOINN.
* LMLitho Table IV's advanced-node results follow fine-tuning.
* TokMan's TAT advantage differs between small and large cases.
* ResGNN prediction is fast, but final EPE exceeds conventional MBOPC.
* TEMPO's schemes have different accuracy/speed tradeoffs.
* DOINN's large-tile strategy addresses physical frequency/grid changes beyond training tiles.
* Nitho's roughly 69× MSE ratio is a table-average ratio; via-only gains are smaller.

Numbers and conditions are linked to each review's experiments and original table/figure numbers, rather than compressed into one score.

## Using public benchmarks

[Official LithoBench](https://github.com/shelljane/lithobench) provides forward/ILT interfaces, datasets, baselines and shot counting. Fix repository versions and source settings when reproducing results. Benchmark distribution links do not establish original-author code availability.

The checked [evaluation snapshot](https://github.com/shelljane/lithobench/blob/9c74e82218e377eaf6d02d113fc1ce6e36c92aa6/pyilt/evaluation.py) uses binary-output `mse_loss(..., reduction="sum")` and pixel PVB counts. Check normalization even when a paper calls the value MSE. This snapshot is not necessarily every paper's exact experimental version.

[Official LithoSim](https://dw-hongquan.github.io/LithoSim/) describes source, dose, defocus and sub-28 nm simulation benchmarks. LMLitho's partial public dataset is not automatically the full LithoSim benchmark. Apache 2.0 code and CC BY-NC 4.0 data have separate terms. GeoSignal's simplified source and relative focus/dose references are not calibrated commercial resist ground truth; separate scalar-reference matching from commercial-resist surrogate learning.

## Model-Based OPC and ML-Based OPC

| Aspect | Model-based OPC | ML-assisted OPC |
| --- | --- | --- |
| Iterations | Repeated explicit models track objectives/conditions | Training moves some repeated cost offline |
| Flexibility | Change modeled source/focus/dose inputs | Revalidate outside conditioning/training coverage |
| Corrections | Solver-dependent edge/pixel/level-set variables | Image, graph, token or latent representations |
| Accuracy | Calibration, numerical approximation, convergence | Reference fidelity, distribution shift, gradients, uncertainty |
| Cost | Source/TCC setup and iterations | Labels, training, memory, inference and refinement |
| Final verification | Process models, MRC and verification gates | The same gates remain necessary, preferably independently |

Hybrid initialization/prediction plus model-based refinement can be practical, depending on layout scale, hardware, process stability and data availability.

## Future research and GeoSignal connections

**Ideas applicable now:** sample schemas with physical units, normalization and source/focus/dose metadata; layout-level splits; separate image, contour and gradient evaluations.

**Further research / Hypothesis:** test fixed-condition learned kernels, coarse-to-fine optimization, geometry-preserving updates and source-conditioned surrogates on small public ROIs. Evaluate EPE tails, CD, PVB and reference runtime beyond nominal MSE.

**Long term / Hypothesis:** vector/3D masks, calibrated resist/etch coupling, process-window conditioning, uncertainty/active learning and mask-rule-aware generation. These papers' numerical results are not established production flows.

## Essential terminology

| Term | Meaning here |
| --- | --- |
| OP kernel | A convolutional prior shaped by optical propagation phase |
| Neural operator / FNO | Function/grid mappings with learned Fourier-mode interactions |
| Neural field | Coordinate-to-function-value implicit representation |
| VAE | Variational generative model learning a latent distribution and decoder |
| DiT | Transformer-based conditional sequence/image diffusion updates |
| GNN / residual | Neighbor aggregation and learned increments added to existing features |
| Differentiable rasterizer | Rendering gradients from point/polygon changes to pixels |
| SRAF | A nonprinting assist improving main-pattern response, subject to checks |
| SOCS | Coherent-mode intensity synthesis from a positive-semidefinite TCC |
| EPE / PVB | Edge distance or violations / printed-region band across process corners |
| OOD / transfer | Evaluation beyond training distribution / adaptation with new-condition data |

## References and completion scope

Each review's Paper Information links official papers, DOIs and verified code/data. [Source & Figure Coverage]({{ '/notes/research/sources/' | relative_url }}) keeps access limitations visible. All eight reviews, overview, foundations and navigation exist in both languages; source/supplement verification remains incomplete where stated.
