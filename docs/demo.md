---
layout: default
title: Demo
description: Representative public-layout review figures, conditions and interpretation
permalink: /demo/
---

# Demo

This page shows representative geometry and optical-review results from a public TT04 PWM layout. Start with the pattern and review point, then compare how its modeled contours change.

{% include live-demo-cta.html %}

## 1. What the preview shows

* Candidate regions around narrow lines and gaps.
* Local mask geometry and a modeled light-intensity distribution.
* Contours at several relative doses, with optional focus comparisons in the live workflow.

![Layout, local mask and optical review]({{ '/assets/demo/public/overview.png' | relative_url }})

The panels follow the same region from layout selection to optical review. A candidate marker identifies a location worth inspecting; it does not establish a manufacturing defect.

## 2. Example conditions

| Item | Conditions for the figures below |
| --- | --- |
| Input | Public TT04 PWM layout, layer/datatype 67/20 |
| Optical model | Scalar, thin binary mask; 248 nm wavelength, NA 0.68, conventional illumination σ=0.60 |
| Comparison | Nominal focus; relative doses 0.90, 1.00 and 1.10 |
| Display | Coordinates in µm relative to the review point; contours use one comparison baseline |
| Interpretation | Selected local model results; no calibrated wafer-accuracy or whole-layout performance claim |

Relative dose is dimensionless. It is not an absolute exposure in mJ/cm². These figures illustrate shape changes rather than establish a universal process window.

## 3. Representative patterns

### Narrow line

![Narrow-line optical review at three relative doses]({{ '/assets/demo/public/narrow-line.png' | relative_url }})

Compare the two long edges near the cross. The background shows modeled light distribution; colored contours compare 10% less light, the baseline and 10% more light.

### Narrow gap

![Narrow-gap optical review at three relative doses]({{ '/assets/demo/public/narrow-gap.png' | relative_url }})

Inspect the separation between adjacent shapes and the rounded line ends. An apparent connection or separation depends on the chosen model and contour criterion.

## 4. Reading limits

Geometry width and modeled contour width are different quantities. A contour is not a chemical-resist or etch prediction. Selected examples do not validate every pattern, source condition or wafer process. Runtime also depends on the layout, analysis scope and hosting state.

## 5. Related learning pages

* [Method]({{ '/method/' | relative_url }}) — Conceptual workflow and scope.
* [6f simulator]({{ '/simulator/' | relative_url }}) — Interactive ray and wave learning.
* [Technical Notes]({{ '/notes/' | relative_url }}) — Foundations and research reviews.
* [Release Notes]({{ '/release-notes/' | relative_url }}) — Changes and validation summaries.
