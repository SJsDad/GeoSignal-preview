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

![Six steps from TT04 PWM 67/20 layout to pattern review]({{ '/assets/demo/tt04-comparison/method_flow_67_roi.png' | relative_url }})

The same 67/20 width candidate is followed from layout selection to mask, light distribution and relative-dose outlines. The marked region is a candidate for review, not a confirmed defect. Focus / Dose comparison is an optional next step; see the [Demo examples]({{ '/demo/' | relative_url }}).

The dashed box marks the inner review ROI; the surrounding margin supplies optical context. Contours compare relative doses 0.90, 1.00 and 1.10.

[Open full-size diagram]({{ '/assets/demo/tt04-comparison/method_flow_67_roi.png' | relative_url }})

This method does not run optical simulation on every layout location. It narrows down potentially useful review regions first, then calculates optical-response visualizations only for selected ROIs.

Version-specific implementation details are separated into [Release Notes]({{ '/release-notes/' | relative_url }}) so this page can stay focused on the method concept.

The current calculation uses the Abbe optical model. Version-specific cross-validation and backend details are in [v0.10 Release Notes]({{ '/release-notes/v0.10/' | relative_url }}).

---

## 2. Candidate ROI Selection

ROI means a small review area around a selected location. Width is the line thickness; space is the gap between shapes.

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

Candidates are ordered by smaller measured width/gap, then larger merged candidate area when measurements are equal. Rule settings and evaluation results are in [v0.10 Release Notes]({{ '/release-notes/v0.10/' | relative_url }}).

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

In the current preview, the source-sampling condition is selected by considering both visual stability and computational cost. The detailed rationale for recent default choices is recorded in the release notes.

The current result should be interpreted as qualitative optical-response visualization, not as a scanner-calibrated lithography model.

---

## 6. Relative-dose Contour Extraction

The aerial image is the calculated light distribution. A contour outlines the region above a selected level. Overlaying it on the original drawing makes shape changes easier to see.

```text
Calculated light distribution
    -> Set a baseline with a reference pattern
    -> Compare outlines as the amount of light changes
```

The model is fitted to the design width of a reference pattern, then compared at 10% less light, baseline and 10% more light. Changing the light amount does not change the model's material threshold itself. This is not a process model fitted to measured wafers.

Look for:

* line widening or narrowing
* changes in gaps
* line ends that appear shorter
* rounded corners
* boundaries that move substantially across conditions

Large movement can identify a location worth inspecting. Small movement alone does not establish manufacturing safety. The dose–threshold relationship, fitting procedure and validation results are documented in detail in [v0.10 Release Notes]({{ '/release-notes/v0.10/' | relative_url }}).

---

## 7. Hotspot-like Shape Review

The final step is hotspot-like shape review.

This step combines geometry-based candidate selection with contour-based optical-response review.

The reviewed signals include:

* narrow width or narrow space detected by geometry screening
* visible mismatch between mask and contour
* large contour movement across relative-dose conditions
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
