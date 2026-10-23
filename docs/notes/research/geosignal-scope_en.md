---
layout: technical
category: research
title: "GeoSignal Scope and Research Connections"
permalink: /notes/research/geosignal-scope/
lang: en
---

# GeoSignal Scope and Research Connections

* Contents
{:toc}

## Current state checked in source code

GeoSignal-preview contains Jekyll documentation, public results and the browser-only educational simulator. These paper reviews do not add ML models to the core simulator. GeoSignal-lab source in the working environment was inspected to verify existing functions, listed below; the private core is not included in the public Preview repository.

| Checked location | Verified behavior | Interpretation |
| --- | --- | --- |
| `src/litho/abbe.py` · `prepare_abbe_context`, `compute_abbe_image_from_context` | FFT reuse, coherent fields per source and intensity accumulation | Scalar binary-mask aerial calculation |
| `src/litho/pupil.py`, `config.py` | Shifted circular pupil, wavelength/NA/source settings and focus phase | Idealized optical settings |
| `src/litho/tcc.py`, `socs.py`, `imaging_backend.py` | Source factor, exact full-rank SOCS, backend dispatch and mode cache | Cross-validation against Abbe, not proof of commercial process fidelity |
| `src/litho/truncation.py` | Separate SOCS truncation evaluation | Approximate truncation is not implied to be the service default |
| `src/service.py` · `_calibrate_dose_to_size`, `_run_focus_dose_sweep` | Reference patterns, relative-dose thresholds and focus/dose sweeps | Idealized analysis at fixed references/transects |
| Preview [v0.10 validation]({{ '/notes/v0.10-validation/' | relative_url }}) | Public validation snapshot and conditions | Does not establish live deployment updates or wafer validation |

## Connections to practical interests

| Goal | Verified GeoSignal capability | Idea from the reviews | Additional validation |
| --- | --- | --- | --- |
| Aerial Image Prediction | Scalar Abbe and exact SOCS paths | Nitho kernel identification, DOINN dual branches, LMLitho source conditioning | Reference intensity normalization, boundaries, gradients |
| Resist / Contour Prediction | Intensity-threshold contours | LMLitho resist surrogate | Separate chemistry/wafer calibration |
| OPC Edge Movement | No automatic correction solver | ResGNN residual edge updates | Segmentation, graphs, MBOPC labels, mask rules |
| EPE / CD Prediction | Fixed-transect CD and contour review; no identical paper EPE benchmark | Edge-centered error gates | Gauges, normals, missing contours |
| SRAF Optimization | No learned/automatic SRAF optimizer | OptiCo and Hi-ILT inverse generation/refinement | Nonprinting SRAFs and mask rules |
| DOF / Bossung Curve | Idealized focus/dose sweeps and CD plotting | Condition-specific surrogate error | Scanner/resist response and acceptance specs |
| Focus / Dose Variation | Relative dose and focus simulation | Process conditioning or per-condition kernels | Extrapolation beyond tested conditions |
| Process Window | Idealized specification-based evaluation | Reference reevaluation after a coarse surrogate | Distinguish from calibrated wafer windows |
| Patterning Margin Analysis | Geometry candidates and optical contour review | Uncertainty-aware prioritization | No certified commercial margin claim |
| Optical Simulation Acceleration | FFT/context/mode cache reuse | Learned kernels and source-encoder caches | End-to-end setup, transfers, memory and runtime |

## Ideas applicable now

Align exported results and dataset schemas before importing paper metrics. Record ROI width, pixel spacing, halo, mask polarity, NA, wavelength, source sampling, focus, dose and normalization per sample. Store separate Abbe/SOCS references under identical scalar conditions and split train/test at layout level. These are workflow proposals, not new core features implemented by this documentation change.

## Ideas requiring further research

**Future Application / Hypothesis.** Identifying fixed-condition kernels in the style of Nitho, gated on aerial/CD errors, is close to the existing computation path. Before inverse optimization, compare surrogate directional derivatives against a reference. ResGNN/TokMan also need data structures preserving polygon or edge topology beyond a raster-only flow.

## Longer-term directions

**Future Application / Hypothesis.** Investigate calibrated resist, mask-3D effects, vector imaging, process-conditioned neural operators and uncertainty. TEMPO's height inside resist and GeoSignal's focus coordinate have different physical roles and are not interchangeable inputs. Reading these eight papers does not establish support for stochastic EUV defects or manufacturing-yield prediction.

## Related pages

* [Research Overview]({{ '/notes/research/' | relative_url }})
* [Method]({{ '/method/' | relative_url }})
* [Abbe Imaging]({{ '/notes/abbe-imaging/' | relative_url }})
