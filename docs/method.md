---
layout: default
title: Method
description: Method and workflow explanation for GeoSignal Preview
permalink: /method/
---

[English]({{ site.baseurl }}/method/) | [한국어]({{ site.baseurl }}/ko/method/)

# Method

## 1. Method Overview

This page explains the calculation concept and interpretation flow used in **GeoSignal Preview**.

GeoSignal Preview is not intended to be a production-level lithography simulator or a calibrated wafer prediction model. Instead, it is a preview workflow that first identifies candidate regions from layout geometry, then reviews selected ROIs using a simplified optical model and multi-threshold contour visualization.

The core structure is:

```text
Step 1: Geometry-based candidate filtering
Step 2: Optical-response and contour-behavior review for selected ROIs
```

The key question is:

> Can we first identify suspicious locations from layout geometry and then quickly review those locations from an optical contour viewpoint?

The basic method flow is:

```text
Layout Geometry
    → Geometry-based Candidate Filtering
    → ROI Selection
    → ROI Rasterization
    → Abbe-based Aerial Image Calculation
    → Multi-threshold Contour Extraction
    → Hotspot-like Shape Review
```

This method does not run optical simulation on every layout location. Instead, it first narrows down potentially weak regions using layout-level width / space criteria, then calculates optical-model-based contours only for selected ROIs.

This public preview repository does not include the private core implementation code. This page is intended to explain the workflow structure, calculation concept, and interpretation logic behind the preview results.

---

## 2. Candidate ROI Selection

The first step is to select candidate ROIs from layout geometry.

In the current demo, candidate regions are first identified from a minimum width / space viewpoint. Regions where width or space is below a given criterion are extracted as first-stage candidates, and a limited number of ROIs are then selected for optical contour review.

The current preview demo uses the following temporary criterion:

```text
width or space ≤ 0.200 µm
```

The `0.200 µm` criterion is not a process rule or a calibrated hotspot threshold. It is a preview criterion used under the assumption that a minimum width / space reference is already known and that regions near this reference may be worth reviewing first.

The current candidate selection method is also not an optimized hotspot-ranking logic. Selecting two width candidates and two space candidates was a pragmatic choice for showing the overall workflow while keeping computation manageable.

Therefore, this step should be understood as:

```text
Final hotspot decision
    X

First-stage geometry-based filtering for optical contour review
    O
```

The important point is not that the current candidate-selection rule is optimal. The important point is the structure:

```text
Find potentially weak locations from layout geometry
→ Calculate optical response at those locations
→ Review shape behavior through threshold contours
```

Future candidate selection can be improved by considering:

* local pattern context beyond simple width / space
* line-end, corner, jog, and neighboring features
* local density or pattern interaction
* overlay relationship with adjacent layers
* contour sensitivity or mask-contour mismatch based ranking

---

## 3. ROI Rasterization

After a candidate ROI is selected, layout polygons inside the ROI are converted into a rasterized mask image.

In the rasterized mask:

```text
inside polygon  → 1
outside polygon → 0
```

This means that layout geometry is represented as a binary mask on a regular pixel grid.

```text
Layout polygons in ROI
    → Pixel grid
    → Binary mask image
```

The rasterized mask becomes the input for the optical imaging calculation.

In the current preview, the mask is treated as a binary mask rather than a PSM-aware mask model. This choice is made for simplicity, runtime control, and preview-stage clarity. In other words, phase-shift mask effects, attenuated mask transmission, or more detailed mask stack effects are not included in the current public preview workflow.

If needed, future versions can extend this step toward phase / attenuation-aware mask representation or PSM-aware modeling.

Pixel size controls the trade-off between resolution and computation. A smaller pixel size can represent layout details more accurately, but it increases image-array size and FFT-based calculation cost. A larger pixel size reduces runtime but may lose small geometry details.

The ROI may include a margin around the candidate location. This is useful because optical response is influenced not only by the candidate polygon itself, but also by neighboring layout structures.

Therefore, rasterization is not merely an image conversion step. It defines the reference mask used to interpret the later aerial image and contour results.

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
    → Mask spectrum
    → Source point sampling
    → Shifted pupil filtering
    → Coherent image per source point
    → Partially coherent aerial image
```

More specifically:

1. Transform the rasterized mask into the frequency domain.
2. Shift the pupil position according to each source point.
3. Filter the mask spectrum using the shifted pupil.
4. Transform the filtered spectrum back to the image domain.
5. Calculate a coherent intensity image for each source point.
6. Accumulate the coherent intensity images to form the final aerial image.

The following image shows a debug example of the Abbe-style aerial image calculation flow using a 9-point source condition.

![Abbe debug example with 9-point source](assets/method/abbe_debug_9.png)

The following image shows the same calculation flow under a denser source-sampling condition.

![Abbe debug example with dense source](assets/method/abbe_debug_dense.png)

The aerial image can qualitatively show effects such as:

* edge blur
* corner rounding-like response
* line-end pullback-like response
* intensity degradation around narrow regions
* optical interaction between neighboring patterns
* response difference between dense and isolated structures

At the current preview stage, the simplified Abbe-based calculation is used because it provides a practical balance between physical interpretability, implementation complexity, and runtime.

---

## 5. Source Sampling and Pupil Filtering

The illumination source is approximated by sampling multiple source points.

Each source point represents one illumination direction. For each source point, the pupil is shifted in the frequency domain, and only spatial frequency components passing through the shifted pupil are used to reconstruct the image contribution.

Conceptually:

```text
Source point
    → Shifted pupil
    → Filtered mask spectrum
    → Coherent image contribution
```

The final aerial image is obtained by accumulating image contributions from all sampled source points.

Using more source points can make the illumination approximation smoother, but it also increases calculation time. Using fewer source points reduces runtime, but the result may depend more strongly on the sampling condition.

The following image compares source sampling conditions.

![Source sampling comparison](assets/method/source_sampling_comparison.png)

The following image compares how aerial image and contour behavior may change depending on source sampling conditions.

![Source result comparison](assets/method/source_result_comparison.png)

In the current preview, the source sampling condition is selected by considering both visual stability and computational cost.

Future work may include source-model refinement, use of more source points, and TCC-based computation for improved efficiency.

The current result should be interpreted as qualitative optical-response visualization, not as a scanner-calibrated lithography model.

---

## 6. Multi-threshold Contour Extraction

After the aerial image is calculated, threshold contours are extracted from the intensity image.

A threshold contour is the curve where aerial image intensity crosses a selected threshold level.

```text
Aerial image
    → Intensity threshold
    → Threshold contour
```

In GeoSignal Preview, the threshold contour is used as a printed-shape-like visual indicator. It is not a calibrated resist contour.

The current demo commonly compares the following threshold levels:

```text
0.20 / 0.30 / 0.40
```

These threshold values are used for qualitative comparison only. They should not be interpreted as process-calibrated thresholds or wafer CD references.

Multi-threshold contour comparison helps visualize how the aerial image appears as contour behavior under different threshold levels.

This is useful for reviewing:

* threshold-dependent contour shift
* weak image-contrast regions
* necking-like behavior
* bridge-like behavior
* line-end pullback-like behavior
* corner rounding-like behavior
* locations with large contour movement

If a contour moves significantly across threshold levels, the region may have relatively weak or unstable optical response. If a contour remains relatively stable, the region may be more robust from a contour-behavior viewpoint.

---

## 7. Hotspot-like Shape Review

The final step is hotspot-like shape review.

This step combines geometry-based candidate selection with contour-based optical-response review.

The reviewed signals include:

* narrow width or narrow space detected by geometry screening
* visible mismatch between mask and contour
* large contour movement across threshold levels
* bridge-like response around narrow gaps
* necking or pinch-like response around narrow lines
* line-end pullback-like response
* corner rounding-like response

The output of this step is not a final pass/fail result. It is a visual guide for quickly identifying locations that may deserve additional review.

```text
Geometry candidate
    + Aerial image behavior
    + Threshold contour behavior
    → Lithography-aware review point
```

At the current preview stage, hotspot-like shapes should be interpreted as review candidates, not confirmed lithography failures.

The philosophy of GeoSignal Preview is:

```text
Extract geometry-based candidates
    → Review optical response
    → Review contour behavior
    → Prioritize locations with possible process risk
    → Connect to mask correction or additional simulation if needed
```

In other words, this method is not intended to make a final hotspot judgment. It is intended to help reviewers quickly narrow down locations that deserve attention.

---

## 8. Current Scope and Limitations

GeoSignal Preview is currently a qualitative visualization workflow for public preview.

It has the following assumptions and limitations.

* The public preview repository does not include the core implementation code.
* The candidate selection logic is not an optimized hotspot-ranking method.
* The current `0.200 µm` criterion is an arbitrary preview criterion.
* The mask is treated as a binary mask; PSM-aware mask modeling is not included.
* The imaging model is a simplified Abbe-based model.
* Wafer-data-based calibration is not included.
* Resist and etch models are not included.
* Threshold contours are qualitative visual indicators.
* The current result should not be used for production CD prediction.
* Optical parameters are simplified for preview and learning purposes.
* Public or synthetic layout examples are used.
* Optical analysis is mainly performed at the ROI level.
* Source sampling is selected by considering runtime and implementation complexity.

Therefore, the current method should be understood as:

```text
layout-to-optical-response visualization
```

rather than:

```text
production lithography verification
```

The main goal is to help users understand how geometry-based candidates may appear from optical-response and contour-behavior viewpoints.

---

## 9. Relation to Demo Page

The Demo page shows visual outputs generated through this method.

The Method page explains how those outputs are generated and how they should be interpreted.

| Demo Output              | Method Step                         |
| ------------------------ | ----------------------------------- |
| Geometry-based candidate | Candidate ROI Selection             |
| Rasterized mask          | ROI Rasterization                   |
| Aerial image             | Abbe-based Aerial Image Calculation |
| Multi-threshold contour  | Multi-threshold Contour Extraction  |
| Hotspot-like annotation  | Hotspot-like Shape Review           |

Recommended reading order:

1. Review the Demo page to understand the visual flow.
2. Read the Method page to understand the calculation flow.
3. Check Technical Notes if additional optical background is needed.

---

## 10. Future Work

Future improvements may include the following directions.

| Item                           | Direction                                                                                                 |
| ------------------------------ | --------------------------------------------------------------------------------------------------------- |
| Candidate selection            | Consider pattern context, line-end, corner, density, and neighboring features beyond simple width / space |
| Ranking logic                  | Use contour sensitivity, mask-contour mismatch, and local contrast instead of simple area-based ordering  |
| Runtime improvement            | Improve computation efficiency for wider layout regions                                                   |
| Accuracy / imaging improvement | Refine source modeling, use more source points, and review TCC-based computation for efficiency           |
| Mask representation            | Review phase / attenuation-aware or PSM-aware mask representation if needed                               |
| Mask optimization              | Review simple mask correction or rule-based adjustment based on contour results                           |
| Layer-aware review             | Consider overlay relationship with adjacent layers                                                        |
| Additional examples            | Add dense line-space, isolated line-end, narrow gap, and corner pattern cases                             |
| Technical notes                | Add explanations for Fourier optics, Abbe imaging, and contour interpretation                             |

The current priority is to keep the public preview understandable, visually useful, technically honest, and easy to respond to.

GeoSignal Preview will be improved step by step based on demo results, technical review, and external feedback.

