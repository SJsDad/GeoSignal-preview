---
layout: default
title: Demo
description: Representative public-layout review figures, conditions and interpretation
permalink: /demo/
demo_viewer: true
---

# Demo

Upload a layout, find narrow regions and inspect the patterns that matter. On this page you can also explore saved results immediately, without starting the analysis service.

{% include live-demo-cta.html %}

**Start with locations and patterns.** Geometry screening highlights candidate regions; optical views help you compare their local shapes. Focus/dose comparisons are an optional next step, not a requirement for the first review.

[Jump to the interactive results](#saved-results) · [Read the method]({{ '/method/' | relative_url }}) · [Compare the pre-v0.12 screen]({{ '/demo-legacy/' | relative_url }})

## 1. Screen and usage guide

The live analysis service accepts new public GDS/OAS files. The viewer below uses saved TT04 PWM examples and responds immediately to selections; it does not upload files or run a new layout calculation.

| Item | How to use it |
| --- | --- |
| File | Choose a public, non-confidential layout for Live Demo. |
| Layer / Datatype | Select the geometry you want to review. Saved examples here cover 67/20 and 68/20. |
| Width / Space limit | A geometry-screening criterion, distinct from a printed-CD acceptance specification. |
| ROI / Pixel size | The local review region and image spacing. Display zoom and calculation extent are different. |
| Candidate cards | Switch between Width and Space, choose how many saved examples to show, and select a card for a larger image. |
| Focus / Relative dose | For a recorded candidate, inspect the sampled conditions and modeled dimensions together. |
| Reference input | Follow the live application's guidance. Files outside registered examples may require a reference location, measurement direction and design width. |
| Result interpretation | Candidate locations and modeled contours guide further review; they do not certify defects or manufacturing safety. |

### Getting started with the live application

Begin with a registered public example. Inspect the candidate locations before comparing local contours. Supply custom reference information only when the application asks for it, using a meaningful design feature in your input. The example baseline is a design comparison, not a fit to measured wafer data.

The saved viewer and the live application's arrangement can differ. Use Live Demo for new calculations; use the viewer here to learn how to read the results.

## 2. Find and select a candidate

The overview shows saved example locations on TT04 PWM 67/20. W and S labels identify width and gap examples. A marker means “inspect this location,” not “confirmed defect.”

![Saved Width and Space example locations on public TT04 PWM 67/20]({{ '/assets/demo/public/candidate-locations.png' | relative_url }})

Layer 67/20 has six saved candidates per type. Layer 68/20 has one per type. Focus/dose records are available for candidate 1 of each type in both layers. Other cards retain their default images and explicitly show that comparison records are unavailable.

{% include saved-demo-viewer.html %}

## 3. Compare actual examples

### TT04 PWM 67/20

Select layer 67/20 and compare Width 1 with Space 1. Both design dimensions are 170 nm, while the nominal modeled dimensions are approximately 166.34 nm and 199.44 nm. Geometry dimensions and modeled contours are different quantities; each candidate has not been independently fitted to reproduce its design dimension.

Use the six cards to compare a straight narrow line, nearby line ends and different local gap shapes. Selecting a card changes the large image. Opening the optional comparison switches recorded candidates to a specific focus/dose condition.

### TT04 PWM 68/20

Select layer 68/20, Width 1 for a necked pattern. Its design width is 140 nm and the nominal modeled width is approximately 87.88 nm. At relative dose 0.90 and focus ±0.20 µm, the feature is not measurable at the fixed review location in this model. The viewer shows “Not measurable,” rather than zero, and leaves those gaps in the Bossung curves.

These are local responses under one shared example baseline, not a ranking of whole layers or a wafer-defect assessment.

## 4. Read the image and comparison

| What you see | Interpretation |
| --- | --- |
| Gray geometry | The input mask shapes near the review point. |
| Warm light distribution | A modeled aerial image, not a measured resist profile. |
| Cross | The local review point; coordinates are relative to it. |
| Default contours | Relative doses 0.90, 1.00 and 1.10 at best focus. |
| Blue comparison contour | The focus/dose condition selected in the optional comparison. |
| Geometry versus modeled dimension | A design quantity compared with a contour measurement at the recorded location. |
| Bossung curves | Modeled dimension versus focus for each dose; only three focus samples are present. |

You can expand the nine-image comparison or measurement table. Displayed measurements are rounded to two decimals; that formatting does not imply equivalent physical accuracy. Missing measurements are not replaced with zero or interpolated through.

## 5. Conditions and limits

| Item | Saved example conditions |
| --- | --- |
| Input | Public TT04 PWM, layers/datatypes 67/20 and 68/20 |
| Optical model | Scalar thin binary mask; 248 nm wavelength, NA 0.68, conventional illumination σ=0.60 |
| Focus | −0.20, 0.00 and +0.20 µm |
| Relative dose | 0.90, 1.00 and 1.10; dimensionless, not mJ/cm² |
| Local display | 1.28 × 1.28 µm close-ups; x/y relative to the review point |
| Comparison | Fixed example locations and one shared design baseline; consistent intensity scale across focus within a candidate |

The three focus points show a trend, not a precise DOF estimate. No CD pass/fail specification is applied. Threshold contours do not model resist chemistry or etch. A selected example does not establish whole-layout accuracy, process-window validity or hosted-service runtime.

## 6. Continue learning

* [Method]({{ '/method/' | relative_url }}) — Geometry, sampling, optical images and contour interpretation.
* [6f simulator]({{ '/simulator/' | relative_url }}) — Live ray and wave controls for a periodic educational model.
* [Technical Notes]({{ '/notes/' | relative_url }}) — Optical foundations and research reviews.
* [Release Notes]({{ '/release-notes/' | relative_url }}) — Feature changes and validation summaries.
