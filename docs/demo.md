---
layout: default
title: Demo
description: Find weak layout candidates and review their optical contours from GDS/OAS
permalink: /demo/
---

<p class="language-switch"><a href="{{ '/ko/demo/' | relative_url }}" lang="ko">한국어로 보기</a></p>

# Demo

## From layout geometry to locations worth reviewing

This example follows the result workflow: **find candidates → inspect local contours → take the results back to a layout viewer.** It uses the public TT04 PWM layout and the Speed preset.

{% include live-demo-cta.html %}

## 1. Find the candidate locations

The overview highlights narrow-width and narrow-space regions. It helps you see where candidates are concentrated before inspecting individual locations. Markers are screening results, not a count of confirmed defects.

![Width and space candidate overview for the public TT04 PWM layout]({{ '/assets/demo/v0.10/speed/geometry_candidate_overview.png' | relative_url }})

This illustrated snapshot reviews two ranked candidates and a separate model reference. The live default reviews five ranked candidates plus that reference. The reference sets the comparison baseline; it is not an extra detected hotspot.

## 2. Inspect a narrow-width candidate

![Width candidate with geometry, optical intensity and relative-dose contours]({{ '/assets/demo/v0.10/speed/width_candidate.png' | relative_url }})

Look at the cross and the nearby contours. The original geometry selects this location for review, but the nominal optical contour does not retain the feature at its measurement center. The width measurement is therefore unavailable (`missing_feature`), rather than reported as zero or a pass. This is a model observation to investigate, not proof of a wafer defect.

## 3. Compare a narrow-space candidate

![Space candidate with geometry, optical intensity and relative-dose contours]({{ '/assets/demo/v0.10/speed/space_candidate.png' | relative_url }})

Here the gap remains measurable on the selected cross-section: approximately **0.199 µm** at nominal dose, compared with the geometry candidate's **0.170 µm** gap. Check where the three contours separate, and how the nearby line ends and corners change shape.

The red, dark and blue outlines represent relative dose **−10%, nominal and +10%**. The legend also reports their effective thresholds. Large movement suggests sensitivity worth reviewing; it does not by itself establish a defect.

## 4. Continue the review

Download the [combined review GDS]({{ '/assets/demo/v0.10/speed/pya_native_combined_review.gds' | relative_url }}) to inspect the original geometry, selected ROIs and contours in a layout viewer. The [result data and reference checks]({{ '/notes/v0.10-validation/' | relative_url }}) are available for readers who want the measurements and model details.

These figures use the validated relative-dose calculation for the same saved candidate locations. Detailed contour Region screening is off in the Speed snapshot: absent detailed markers do not mean a pass.

<h2 id="getting-started">Try your own public example</h2>

- Choose a public GDS/OAS file, target layer and the Speed preset.
- The registered TT04 example has a built-in reference. Other files currently require a reference location, direction and design width; this remains a setup limitation of the preview.
- Start with the candidate overview, then inspect the local contours and measurement status. Use Method only when you want the calculation details.
- Hosted processing can take time. A completed public-sample request took about 109 seconds; this is one observation, not a response-time guarantee.

Only upload non-confidential layouts. This simplified model is for relative comparison and learning, not manufacturing signoff.

[How it works]({{ '/method/' | relative_url }}) · [Technical validation and downloads]({{ '/notes/v0.10-validation/' | relative_url }}) · [Earlier Demo]({{ '/demo-legacy/' | relative_url }})
