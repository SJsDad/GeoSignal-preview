---
layout: default
title: GeoSignal Preview
description: Lithography-aware layout visualization workflow
permalink: /
---

# GeoSignal Preview

*Representative preview showing aerial-image intensity, multi-threshold contours, ROI marker, and hotspot-like interpretation on a public GDS layout.*

![GeoSignal Preview]({{ '/assets/index/index_geosignal_preview.png' | relative_url }})

{% include live-demo-cta.html %}

## 1. What is GeoSignal Preview?

**GeoSignal Preview** is a lightweight public demo for reviewing how layout geometry may appear from an optical-response viewpoint. It uses public GDS or synthetic layout examples to connect geometry, rasterized mask images, simplified aerial-image intensity, and threshold-contour visualization.

The basic workflow is:

```text
layout geometry
    -> rasterized mask
    -> simplified aerial image
    -> threshold contour
    -> hotspot-like review
```

The goal is not precise process prediction. GeoSignal Preview focuses on one central question:

> How does a pattern that looks simple from a geometry viewpoint appear from an optical-response viewpoint?

The preview is intended as a visual analysis aid, not a calibrated lithography verification tool.

---

## 2. Motivation

Geometry-based analysis, such as minimum width, minimum space, and density review, is useful for understanding layout patterns. However, geometry checks alone do not always make it easy to intuit how a pattern may behave after optical imaging.

GeoSignal Preview explores this gap by turning layout polygons into a binary mask image, generating a simplified aerial image, extracting threshold contours, and comparing geometry-based review points with optical-response behavior at the ROI level.

---

## 3. Preview Structure

GeoSignal Preview is organized around the following pages.

{% assign demo_url = '/demo/' | relative_url %}
{% assign method_url = '/method/' | relative_url %}
{% assign notes_url = '/notes/' | relative_url %}
{% assign release_url = '/release-notes/' | relative_url %}

| Page | Description |
| --- | --- |
| [Demo]({{ demo_url }}) | Representative images and result interpretation |
| [Method]({{ method_url }}) | Simplified calculation flow and interpretation logic |
| [Technical Notes]({{ notes_url }}) | Background notes for aerial image, contour, and optical interpretation |
| [Release Notes]({{ release_url }}) | Version-level implementation changes and evaluation notes |

### Demo

The Demo page shows representative ROI results, including aerial images, multi-threshold contours, and hotspot-like shape interpretation.

### Method

The Method page explains the calculation concept behind the preview: candidate ROI selection, rasterized mask generation, simplified Abbe-style aerial imaging, source sampling, threshold contour extraction, and visual review.

### Technical Notes

Technical Notes provide supporting background for readers who want more context on aerial images, threshold contours, source sampling, Fourier optics, and Abbe imaging.

### Release Notes

Release Notes collect version-specific implementation details, benchmark notes, backend changes, and metric updates. These notes are useful for readers who want to understand how the preview evolved, but they are not required for a first reading of the demo.

---

## 4. What You Can Review in the Demo

The demo helps review questions such as:

* Does a simple-looking geometry pattern become more sensitive in optical response?
* Can edge rounding, necking, bridge-like behavior, or line-end pullback-like behavior be observed in threshold contours?
* Do geometry-based candidates and optical-response behavior point to the same locations?
* Does threshold comparison help reveal contour sensitivity?

The demo should be understood as a qualitative review workflow rather than a calibrated lithography prediction result.

---

## 5. Interpretation and Limitations

The results of GeoSignal Preview are intended for qualitative visualization and relative comparison.

Current assumptions and limitations are:

* public or synthetic layout examples are used
* only public, non-confidential layout files should be used with the live demo
* a simplified optical model is used
* wafer-data-based calibration is not included
* resist and etch models are not included
* threshold contours are used for qualitative visualization
* results should be interpreted as qualitative indicators, not quantitative CD prediction
* core implementation code is not included in this public preview repository

---

## 6. Intended Use

GeoSignal Preview may be useful for university labs, student projects, educational researchers, or small technical teams that want to perform early learning, research, or qualitative comparison without directly relying on high-cost commercial simulation environments.

Main intended uses include:

* computational lithography study
* understanding the relationship between layout geometry and optical response
* reviewing public or synthetic pattern-based demos
* reviewing aerial-image and threshold-contour visualization
* connecting geometry checks with optical-model intuition

---

## 7. Feedback

GeoSignal Preview is currently an early public preview.

If you have feedback, questions, or suggestions, please feel free to leave a comment through the feedback form.

<a href="{{ site.feedback_url }}" target="_blank" rel="noopener noreferrer">Share feedback through the GeoSignal Preview form</a>

Useful feedback includes whether the demo is easy to understand, whether the contour comparison is useful, and what additional pattern examples would make the preview clearer.

---

## 8. Data and Example Policy

GeoSignal Preview is based on public datasets, synthetic patterns, and open-source layout examples.

The analysis workflow is organized around publicly shareable examples and result interpretation. Core implementation code is not included in this public preview repository.

---

## Keywords

`Lithography` · `Layout Analysis` · `GDS/OAS` · `Aerial Image` · `Threshold Contour` · `Hotspot Candidate` · `Python` · `Computational Lithography`
