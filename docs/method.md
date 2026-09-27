---
layout: default
title: Method
description: Method and workflow explanation for GeoSignal Preview
permalink: /method/
---

<p class="language-switch"><a href="{{ '/ko/method/' | relative_url }}" lang="ko">한국어로 보기</a></p>

# Method

## 1. Method Overview

This page explains the calculation concept and interpretation flow used in **GeoSignal Preview**.

GeoSignal Preview is not intended to be a production-level lithography simulator or a calibrated wafer prediction model. Instead, it is a preview workflow that first identifies candidate regions from layout geometry, then reviews selected ROIs using a simplified optical model and relative-dose contour visualization.

The basic method flow is:

```text
Layout Geometry
    -> Geometry-based Candidate Filtering
    -> ROI Selection
    -> ROI Rasterization
    -> Abbe-based Aerial Image Calculation
    -> Relative-dose Contour Extraction
    -> Hotspot-like Shape Review
```

This method does not run optical simulation on every layout location. It narrows down potentially useful review regions first, then calculates optical-response visualizations only for selected ROIs.

Version-specific implementation details are separated into [Release Notes]({{ '/release-notes/' | relative_url }}) so this page can stay focused on the method concept.

The public service currently uses Abbe as its validated default. v0.9 also
implements an exact full-rank Hopkins/TCC/SOCS formulation for cross-validation,
but no approximate SOCS truncation policy is enabled by default. See the
[v0.9 milestone notes]({{ '/release-notes/v0.9/' | relative_url }}) for the
equivalence gates and measured tradeoffs.

---

## 2. Candidate ROI Selection

The first step is to select candidate ROIs from layout geometry.

In the current demo, candidate regions are first identified from a minimum width / space viewpoint. A limited number of ROIs are then selected for optical contour review.

This step should be understood as:

```text
Final hotspot decision
    X

First-stage geometry-based filtering for optical contour review
    O
```

The important point is not that the current candidate-selection rule is optimal. The important point is the structure:

```text
Find potentially weak locations from layout geometry
    -> Calculate optical response at those locations
    -> Review shape behavior through threshold contours
```

Specific rule thresholds, ordering heuristics, backend changes, and benchmark results are documented in [v0.5]({{ '/release-notes/v0.5/' | relative_url }}) and [v0.6]({{ '/release-notes/v0.6/' | relative_url }}) release notes.

Candidates are ranked by measured minimum width/space first, then smaller width-component area or larger space-component area; deterministic ties and missing-distance fallback follow.

---

## 3. ROI Rasterization

After a candidate ROI is selected, layout polygons inside the ROI are converted into a rasterized mask image.

In the rasterized mask:

```text
inside polygon  -> 1
outside polygon -> 0
```

This means that layout geometry is represented as a binary mask on a regular pixel grid.

```text
Layout polygons in ROI
    -> Pixel grid
    -> Binary mask image
```

The rasterized mask becomes the input for the optical imaging calculation.

In the current preview, the mask is treated as a binary mask rather than a PSM-aware mask model. Phase-shift mask effects, attenuated mask transmission, and detailed mask-stack effects are not included in the current public preview workflow.

Pixel size controls the trade-off between resolution and computation. A smaller pixel size can represent layout details more accurately, but it increases image-array size and FFT-based calculation cost. A larger pixel size reduces runtime but may lose small geometry details.

The ROI may include a margin around the candidate location because optical response is influenced not only by the candidate polygon itself, but also by neighboring layout structures.

---

## 4. Abbe-based Aerial Image Calculation

GeoSignal Preview currently uses a simplified Abbe-based imaging approach.

The aerial image is an optical intensity map calculated by applying a simplified optical imaging model to the rasterized mask.

It should be interpreted as:

```text
optical response image
```

not as:

```text
final wafer contour
calibrated resist contour
production CD prediction
```

The conceptual calculation flow is:

```text
Rasterized mask
    -> Mask spectrum
    -> Source point sampling
    -> Shifted pupil filtering
    -> Coherent image per source point
    -> Partially coherent aerial image
```

More specifically:

1. Transform the rasterized mask into the frequency domain.
2. Shift the pupil position according to each source point.
3. Filter the mask spectrum using the shifted pupil.
4. Transform the filtered spectrum back to the image domain.
5. Calculate a coherent intensity image for each source point.
6. Accumulate the coherent intensity images to form the final aerial image.

The following image shows a debug example of the Abbe-style aerial-image calculation flow using a 9-point source condition.

![Abbe debug example with 9-point source]({{ '/assets/method/abbe_debug_9.png' | relative_url }})

The following image shows the same calculation flow under a denser source-sampling condition.

![Abbe debug example with dense source]({{ '/assets/method/abbe_debug_dense.png' | relative_url }})

These images are kept as visual references for understanding the method. They are not intended as calibrated scanner-model validation.

The aerial image can qualitatively show effects such as:

* edge blur
* corner-rounding-like response
* line-end-pullback-like response
* intensity degradation around narrow regions
* optical interaction between neighboring patterns
* response differences between dense and isolated structures

---

## 5. Source Sampling and Pupil Filtering

The illumination source is approximated by sampling multiple source points.

Each source point represents one illumination direction. For each source point, the pupil is shifted in the frequency domain, and only spatial-frequency components passing through the shifted pupil are used to reconstruct the image contribution.

Conceptually:

```text
Source point
    -> Shifted pupil
    -> Filtered mask spectrum
    -> Coherent image contribution
```

The final aerial image is obtained by accumulating image contributions from all sampled source points.

Using more source points can make the illumination approximation smoother, but it also increases calculation time. Using fewer source points reduces runtime, but the result may depend more strongly on the sampling condition.

The following image compares source-sampling conditions.

![Source sampling comparison]({{ '/assets/method/source_sampling_comparison.png' | relative_url }})

The following image compares how aerial-image and contour behavior may change depending on source-sampling conditions.

![Source result comparison]({{ '/assets/method/source_result_comparison.png' | relative_url }})

Legacy fixed-threshold comparison image; visualization only, not a dose-aware result.


In the current preview, the source-sampling condition is selected by considering both visual stability and computational cost. The detailed rationale for default choices is recorded in the release notes.

The current result should be interpreted as qualitative optical-response visualization, not as a scanner-calibrated lithography model.

---

## 6. Relative Dose and Effective Threshold

The model resist threshold T0 is fixed; it is not a measured material parameter. The relative exposure model is
`D0 * d * I(x,y,z) >= T0`, equivalently `I >= T_eff = T0 / (D0 * d)`.
I is raw clear-field-relative intensity per unit dose. Best-focus dose-to-size
calibration supplies D0 using the same convention as Process Window.
The preview compares d = 0.90, 1.00, 1.10 and displays both relative dose and
T_eff; increasing dose lowers T_eff, not the physical resist threshold T0.

Contour extraction, CD/space measurements and PW use raw intensity without
per-ROI peak or min/max normalization. Normalized backgrounds may be used for
display only. Failed or out-of-tolerance calibration makes quantitative preview
unavailable rather than substituting an arbitrary threshold.

This is an idealized relative exposure model, not scanner/resist calibrated
signoff and not exposure in mJ/cm². The current Demo uses relative-dose results. Legacy fixed-threshold images are isolated in Legacy Demo and are not convergence evidence.

The nominal CD fit matches the model to a designed reference/anchor CD, not to measured printed CD. Actual process-model calibration generally uses measured CDs across multiple patterns and focus/exposure conditions; see [Mack et al., Improved Methods for Lithography Model Calibration](https://www.lithoguru.com/scientist/litho_papers/2007_156_Improved%20Methods%20for%20Lithography%20Model%20Calibration.pdf). The fitted value is specific to the reference geometry, optical conditions and numerical settings. It is not a measured resist property. With `Tnorm = T0 / D0`, the contour threshold is `T_eff = Tnorm / d`; T0 and D0 are not independently identified physical parameters in this fit.

The current binary-mask convention is polygon transmission = 1 and background = 0. The reported high-intensity region (`I >= T_eff`) must not be interpreted as remaining positive-tone resist. A positive-tone remaining-pattern study requires an explicit mask-polarity convention and low-intensity-region measurement, followed by a new nominal fit. Complementing a mask requires recomputing the optical image, not replacing intensity with `1 - I`.

For positive-tone development, the high-intensity contour can describe an idealized resist opening. Whether that opening corresponds to the final conductor depends on the subsequent pattern-transfer process; the GDS layer name alone does not establish this correspondence.

---

## 7. Hotspot-like Shape Review

The final step is hotspot-like shape review.

This step combines geometry-based candidate selection with contour-based optical-response review.

The reviewed signals include:

* narrow width or narrow space detected by geometry screening
* visible mismatch between mask and contour
* large contour movement across threshold levels
* bridge-like response around narrow gaps
* necking- or pinch-like response around narrow lines
* line-end-pullback-like response
* corner-rounding-like response

The output of this step is not a final pass/fail result. It is a visual guide for quickly identifying locations that may deserve additional review.

```text
Geometry candidate
    + Aerial image behavior
    + Threshold contour behavior
    -> Lithography-aware review point
```

---

## 8. Current Scope and Limitations

GeoSignal Preview is currently a qualitative visualization workflow for public preview.

It has the following assumptions and limitations.

* The public preview repository does not include the core implementation code.
* The candidate-selection logic is not an optimized hotspot-ranking method.
* The mask is treated as a binary mask; PSM-aware mask modeling is not included.
* The imaging model is a simplified Abbe-based model.
* Wafer-data-based calibration is not included.
* Resist and etch models are not included.
* Threshold contours are qualitative visual indicators.
* The current result should not be used for production CD prediction.
* Optical parameters are simplified for preview and learning purposes.
* Public or synthetic layout examples are used.
* Optical analysis is mainly performed at the ROI level.

Therefore, the current method should be understood as:

```text
layout-to-optical-response visualization
```

rather than:

```text
production lithography verification
```

---

## 9. Relation to Demo Page

The [Demo]({{ '/demo/' | relative_url }}) page shows visual outputs generated through this method.

| Demo Output | Method Step |
| --- | --- |
| Geometry-based candidate | Candidate ROI Selection |
| Rasterized mask | ROI Rasterization |
| Aerial image | Abbe-based Aerial Image Calculation |
| Relative-dose contour | Relative-dose Contour Extraction |
| Hotspot-like annotation | Hotspot-like Shape Review |

Recommended reading order:

1. Review the [Demo]({{ '/demo/' | relative_url }}) page to understand the visual flow.
2. Read the Method page to understand the calculation flow.
3. Check [Technical Notes]({{ '/notes/' | relative_url }}) if additional optical background is needed.
4. Check [Release Notes]({{ '/release-notes/' | relative_url }}) if implementation history is needed.

---

## 10. Related Pages

* [Home]({{ '/' | relative_url }})
* [Demo]({{ '/demo/' | relative_url }})
* [Technical Notes]({{ '/notes/' | relative_url }})
* [Release Notes]({{ '/release-notes/' | relative_url }})

## v0.10 geometry and measurement path

Input geometry is rescaled to 0.1 nm DBU without changing physical size. Float intensity produces filled contours with outer/hole associations, then pya Regions. Open contours follow the sampled-domain boundary instead of arbitrary closing chords. Width/space screening checks the full sampled domain and clips paired edges to the inner ROI/domain guard. Curved edges use Euclidean metrics, a 90-degree ignore-angle and shielding. These markers are distinct from fixed-gauge CD or physical hotspot classification.

Registered references are identified by file hash and layer. Other inputs require a gauge center, direction and design CD, checked against geometry. Results record source, pixel, ROI, ambit, optics, DBU, reference and Tnorm.
