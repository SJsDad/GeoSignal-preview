---
layout: default
title: Demo
description: Demo results and interpretation for GeoSignal Preview
permalink: /demo/
---

<p class="language-switch"><a href="{{ '/ko/demo/' | relative_url }}" lang="ko">한국어로 보기</a></p>

# Demo

Upload a layout, find narrow features, and inspect the patterns that deserve a closer look.

{% include live-demo-cta.html %}

**Start with locations and patterns.** GeoSignal screens the selected GDS layer for narrow widths and gaps, then calculates optical images for a limited set of candidates. Focus / Dose comparison is an optional next step.

## 1. Screen guide

The proposed screen below starts with a layout overview and **six candidates per type by default**. Choose 4, 6 or 8, switch between Width and Space, and click a pattern to see it at full width below. Candidate count controls detailed review; it does not limit geometry detection.

This is an interactive, saved-data preview, not a live analysis session. Six examples per type are available. Actual PW data is available for Width #1 and Space #1; the other cards show an uncalculated state. Choosing 8 does not invent additional examples. The deployed app may still show the previous interface.

<iframe src="{{ '/assets/demo/ui-guide/reference-draft.html' | relative_url }}" title="Candidate review UI draft" width="100%" height="850" loading="lazy" style="border:1px solid #dce3ec;border-radius:10px" sandbox="allow-scripts allow-downloads allow-popups"></iframe>

[Open the interactive screen ↗]({{ '/assets/demo/ui-guide/reference-draft.html' | relative_url }})

| No. | Item | How to use it |
| --- | --- | --- |
| ① | File | Choose a public, non-confidential GDS/OAS file. |
| ② | Layer / Datatype | Select the target layer. TT04 PWM 68/20 can also be reviewed. |
| ③ | Width / Space limit | Geometry screening limits, not printed-CD tolerances. |
| ④ | ROI / Pixel size | Review area and pixel spacing. Illumination stays at dense7. |
| ⑤ | Focus / Dose | Enter symmetric ranges. Compare shapes and CD changes at nine combinations. |
| ⑥ | Override reference | Usually leave blank. To fit another design reference, enter its center X/Y, design width and measurement direction. |
| ⑦ | Candidate locations | Locate candidate regions across the GDS. |
| ⑧ | Main candidates | Default: 6 per type; choose 4 / 6 / 8. Click a card for a full-width detail image. |
| ⑨ | Optional comparison | Expand the selected candidate’s 3×3 images and Bossung curve. No pass/fail grading. |

<h3 id="getting-started">Using the live demo</h3>

The screen above previews the updated workflow. In the currently deployed app, files outside the registered examples may still require an explicit reference location, direction and design width. Follow the reference fields shown in that app.

Usually, leave **Override reference** blank. These examples share the TT04 PWM 67/20 anchor at **(147.770, 108.460) µm**, fitted to its **170 nm design width**. This is a common comparison baseline, not calibration to measured wafers. Other patterns are not individually fitted.

## 2. Find the main candidates

The overview locates candidates across TT04 PWM 67/20. Markers identify places to inspect, not confirmed manufacturing defects.

![TT04 67/20 candidate locations]({{ '/assets/demo/v0.10/speed/geometry_candidate_overview.png' | relative_url }})

Narrower geometry comes first; ties prefer larger candidate regions. The galleries below show six Width and six Space examples. Warm colors show light intensity; cyan, white and lime contours represent dose −10%, nominal and +10%.

### Width · top 6

![Six Width candidates]({{ '/assets/release-notes/v0.10/width_area_desc_review/top6.png' | relative_url }})

### Space · top 6

![Six Space candidates]({{ '/assets/release-notes/v0.10/width_area_desc_review/space_top6.png' | relative_url }})

## 3. Actual examples: 67/20 and 68/20

These are actual local calculations on the public TT04 PWM GDS, using the same 67/20 reference. Each example keeps its candidate and measurement location fixed. They are not Render runtime tests or a ranking of entire layers.

Start with the nominal pattern pair. Open the optional comparison to see nine conditions and the corresponding Bossung curves.

### TT04 PWM 67/20

![TT04 67/20 nominal Width and Space]({{ '/assets/demo/tt04-comparison/layer67_nominal.png' | relative_url }})

The geometry and model measurements differ because the common reference is not fitted separately to these candidates.

<details markdown="1">
<summary>Optional: Focus / Dose images and Bossung curves</summary>

![TT04 67/20 width comparison]({{ '/assets/demo/tt04-comparison/layer67_width.png' | relative_url }})

![TT04 67/20 space comparison]({{ '/assets/demo/tt04-comparison/layer67_space.png' | relative_url }})

![TT04 67/20 bossung comparison]({{ '/assets/demo/tt04-comparison/layer67_bossung.png' | relative_url }})

Focus: −0.20 / 0 / +0.20 µm. Relative dose: 0.90 / 1.00 / 1.10. Bossung plots show measured size against focus, one line per dose. Missing measurements are not connected; three sampled points show a trend, not a precise DoF estimate. No CD pass/fail specification is applied.

</details>

### TT04 PWM 68/20

![TT04 68/20 nominal Width and Space]({{ '/assets/demo/tt04-comparison/layer68_nominal.png' | relative_url }})

The selected width candidate has a narrow neck. Its nominal model width is about 88 nm versus 140 nm in the geometry. At dose 0.90 and focus ±0.20 µm, the fixed-gauge measurement reports a missing feature. This is a local model response, not a wafer-defect claim.

<details markdown="1">
<summary>Optional: Focus / Dose images and Bossung curves</summary>

![TT04 68/20 width comparison]({{ '/assets/demo/tt04-comparison/layer68_width.png' | relative_url }})

![TT04 68/20 space comparison]({{ '/assets/demo/tt04-comparison/layer68_space.png' | relative_url }})

![TT04 68/20 bossung comparison]({{ '/assets/demo/tt04-comparison/layer68_bossung.png' | relative_url }})

Focus: −0.20 / 0 / +0.20 µm. Relative dose: 0.90 / 1.00 / 1.10. Bossung plots show measured size against focus, one line per dose. Missing measurements are not connected; three sampled points show a trend, not a precise DoF estimate. No CD pass/fail specification is applied.

</details>

## 4. Read the results

Look for a narrowing neck, a closing gap, rounded corners or a line end pulling back. The orange cross marks the measurement location. In the 3×3 images, cyan marks the calculated contour and Δ shows the change from that candidate’s nominal result. Brightness is held consistent within each comparison.

The model treats polygons as illuminated regions. These contours do not determine which material remains after resist development or etch. They are relative model results for study, not calibrated process predictions.

## 5. Data and details

- [Measurements CSV]({{ '/assets/demo/tt04-comparison/measurements.csv' | relative_url }})
- [Reference and conditions]({{ '/assets/demo/tt04-comparison/conditions.json' | relative_url }})
- [67/20 review GDS]({{ '/assets/demo/v0.10/speed/pya_native_combined_review.gds' | relative_url }})
- [v0.10 evaluation and technical details]({{ '/release-notes/v0.10/' | relative_url }})

The review GDS is the saved 67/20 example; it does not include the 68/20 comparison. Upload only public, non-confidential layouts.
