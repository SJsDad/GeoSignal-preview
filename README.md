# GeoSignal Preview

**GeoSignal Preview** is a documentation-focused public preview of a lightweight, lithography-aware layout visualization workflow.

It connects geometry-based candidate selection with rasterized mask generation, simplified aerial-image calculation, and relative-dose contour visualization using public GDS or synthetic layout examples.

> This repository presents documentation, demo results, and method explanations.
> The private core implementation code is not included.

## Live Preview

* [GeoSignal Preview Home](https://sjsdad.github.io/GeoSignal-preview/)
* [Demo](https://sjsdad.github.io/GeoSignal-preview/demo/)
* [Method](https://sjsdad.github.io/GeoSignal-preview/method/)
* [Technical Notes](https://sjsdad.github.io/GeoSignal-preview/notes/)
* [Share Feedback](https://docs.google.com/forms/d/e/1FAIpQLSerlp3xN8b82NyXBjl5tSNPCoS9N5MUqnE8r3c93cfR5n1U7w/viewform)

---

## 1. Overview

GeoSignal Preview explores the following workflow:

```text
Layout geometry
    → Geometry-based candidate filtering
    → ROI selection
    → Rasterized mask
    → Simplified aerial image
    → Relative-dose contour
    → Hotspot-like shape review
```

The project focuses on one main question:

> Can potentially sensitive locations first be identified from layout geometry and then reviewed from an optical-response and contour-behavior viewpoint?

The goal is not to provide a production-level lithography simulator or a process-calibrated wafer prediction model.

Instead, GeoSignal Preview is intended to provide a visual analysis workflow for qualitatively reviewing the relationship between layout geometry and simplified optical response.

---

## 2. Motivation

Minimum-width, minimum-space, and density checks are useful for understanding layout geometry.

However, geometry checks alone do not always make it easy to understand how a pattern may appear from an optical-imaging perspective.

GeoSignal Preview explores this gap by:

* identifying candidate regions from layout geometry
* converting layout polygons into rasterized binary masks
* generating aerial images with a simplified Abbe-based model
* extracting contours at multiple threshold levels
* comparing mask geometry with contour behavior
* visualizing hotspot-like shapes at selected ROIs

This workflow is intended as a lightweight preview for research, learning, technical discussion, and early feedback.

---

## 3. What the Demo Shows

The current demo uses public or synthetic layout examples and includes:

* geometry-based width and space candidates
* selected regions of interest
* rasterized binary masks
* simplified aerial-image intensity maps
* relative-dose contours at d = 0.90, 1.00, and 1.10, labeled with effective threshold
* approximate nominal-dose printed width and space on raw clear-field-relative intensity
* fixed-reference calibration and fixed-transect CD, with separate pya Region hotspot screening
* ROI markers
* hotspot-like shape annotations

The results can be reviewed for qualitative behavior such as:

* edge blur
* corner-rounding-like response
* line-end-pullback-like response
* necking- or pinch-like response
* bridge-like response
* threshold-dependent contour movement
* mismatch between mask geometry and contour behavior

These observations should be treated as review signals rather than confirmed process failures.

---

## 4. Method Summary

The current preview builds on the v0.6 pya-native geometry engine and the v0.7
bounded-memory review workflow. v0.8 adds idealized relative focus/dose process-window
analysis, and v0.8.1 makes the imaging integration backend-neutral while
improving repeated focus/dose execution. The v0.9.0 release adds an exact
full-rank Hopkins/TCC/SOCS cross-validation path and a bounded optical-mode
cache. Abbe remains the public service default; no approximate SOCS truncation
policy is enabled by default.

### Stage 1: Geometry-based candidate filtering

Candidate regions are first identified using layout-level width and space criteria.

The current demo uses a temporary criterion of:

```text
width or space < 0.200 µm
```

This value is a preview-stage heuristic, not a process rule or calibrated hotspot threshold.
The comparison is intentionally strict, so geometry measured exactly at `0.200 µm`
is not included. Candidates are primarily prioritized by measured minimum width/space severity.
Component geometry is a secondary heuristic: smaller area for width and larger
area for space, followed by deterministic bounding-box ordering. Missing measured
distances are ordered last.

### Stage 2: Optical-response review

Selected ROIs are rasterized and processed using a simplified Abbe-based imaging workflow.

The conceptual calculation flow is:

```text
Rasterized mask
    → Mask spectrum
    → Source-point sampling
    → Shifted pupil filtering
    → Coherent image contribution
    → Partially coherent aerial image
    → Relative-dose contours
```

The resulting contours are used as printed-shape-like visual indicators. They are not calibrated resist or wafer contours.

More details are available on the [Method page](https://sjsdad.github.io/GeoSignal-preview/method/).

---

## 5. Current Scope

### Included

* project overview and motivation
* public GitHub Pages site
* representative demo images
* method and workflow explanation
* source-sampling comparison images
* simplified Abbe-imaging debug images
* technical-note structure
* public or synthetic layout examples
* anonymous feedback form

### Not Included

* private core implementation code
* internal experiment notes
* non-public layout or process data
* wafer-data-based calibration
* resist or etch models
* production verification specifications

This repository is therefore a public technical preview, not a complete software-package release.

---

## 6. Assumptions and Limitations

The current preview has the following limitations:

* candidate selection is not an optimized hotspot-ranking method
* the `0.200 µm` criterion is an arbitrary preview criterion
* the mask is treated as a binary mask
* PSM-aware mask representation is not included
* the imaging model is a simplified Abbe-based model
* source sampling is selected by balancing visual stability and runtime
* wafer-data-based calibration is not included
* resist and etch models are not included
* threshold contours are qualitative visual indicators
* evaluation is mainly performed at the ROI level
* the live upload workflow must be used only with public, non-confidential GDS/OAS files
* results should not be used for production CD prediction

GeoSignal Preview should be interpreted as:

```text
layout-to-optical-response visualization
```

rather than:

```text
production lithography verification
```

---

## 7. Intended Use

GeoSignal Preview may be useful for:

* computational lithography study
* understanding the relationship between layout geometry and optical response
* public or synthetic pattern-based experiments
* qualitative layout-risk visualization
* early technical review
* student or academic projects
* discussion of hotspot-review workflows
* technical portfolio documentation
* collecting feedback on future development directions

The project is intended to complement geometry-based review with optical-response visualization, not replace calibrated commercial verification tools.

---

## 8. Repository Structure

```text
GeoSignal-preview/
├─ docs/
│  ├─ _config.yml
│  ├─ _includes/
│  │  └─ sidebar.html
│  ├─ _layouts/
│  │  └─ default.html
│  ├─ assets/
│  │  ├─ css/
│  │  ├─ demo/
│  │  ├─ index/
│  │  └─ method/
│  ├─ notes/
│  │  ├─ index.md
│  │  ├─ abbe-imaging.md
│  │  └─ fourier-optics.md
│  ├─ index.md
│  ├─ demo.md
│  └─ method.md
└─ README.md
```

The main public content is organized through GitHub Pages rather than through the repository file browser alone.

---

## 9. Current Status

| Area                      | Status                                     |
| ------------------------- | ------------------------------------------ |
| Public preview repository | Available                                  |
| GitHub Pages              | Published                                  |
| Home page                 | Available                                  |
| Demo page                 | Available                                  |
| Method page               | Available                                  |
| Technical Notes index     | Available                                  |
| Detailed technical notes  | Reserved for future expansion              |
| Representative images     | Available                                  |
| Core implementation       | Private                                    |
| Layout examples           | Public or synthetic                        |
| Feedback form             | Active                                     |
| Current evaluation scale  | Selected ROI and small public GDS examples |

---

## 10. Future Directions

Possible future improvements include:

* more diverse layout examples
* improved candidate-selection and ranking logic
* contour-sensitivity metrics
* mask-to-contour mismatch metrics
* local image-contrast evaluation
* denser or refined source modeling
* runtime improvement
* representative layout-derived Hopkins/SOCS evaluation
* alternative approximation strategies with explicit aerial/CD error gates
* phase- or attenuation-aware mask representation
* contact, via, or adjacent-layer-aware review
* simple mask-correction experiments
* expanded technical notes

Development priorities will be reviewed based on technical results and external feedback.

---

## 11. Feedback

Feedback on the clarity, usefulness, and possible next direction of GeoSignal Preview is welcome.

Useful feedback includes:

* whether the workflow is easy to understand
* whether the demo images are useful
* whether relative-dose contours help explain pattern sensitivity
* whether geometry and optical-response comparisons are meaningful
* which technical topics need more explanation
* which layout examples should be added
* which future improvement would be most valuable

The feedback form does not require a name or email address.

[Share feedback through the GeoSignal Preview form](https://docs.google.com/forms/d/e/1FAIpQLSerlp3xN8b82NyXBjl5tSNPCoS9N5MUqnE8r3c93cfR5n1U7w/viewform)

Please do not submit confidential, proprietary, company-related, or other non-public information.

---

## 12. License

No open-source license has been selected for this repository.

The repository is currently shared as a public documentation and result preview for technical discussion and feedback. The absence of a license does not grant permission to reuse, modify, or redistribute the repository contents.

An appropriate license may be reviewed later if the public scope of the code or documentation expands.


## Prepared v0.10 validation snapshot

Home and Demo show regenerated relative-dose results with Speed dense7, Internal dense11, a separate 170 nm reference and 0.1 nm DBU. Speed detailed Region checks are optional; Internal checks all three preview doses. Both export all three filled contours. This prepared snapshot does not claim the live Render deployment or a release tag was updated.
