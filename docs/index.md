---
layout: default
title: GeoSignal Preview
description: GeoSignal relative exposure study and validation
permalink: /
---

<p class="language-switch"><a href="{{ '/ko/' | relative_url }}" lang="ko">한국어로 보기</a></p>

# GeoSignal Preview

> This is a locally validated v0.10 snapshot. The live Render deployment may differ.

A study tool for screening layout geometry and reviewing local optical contours.

The nominal model CD is fitted to a design anchor. This is not measured-wafer fitting or scanner/resist process calibration. Polygon transmission is 1 and the contour describes the high-intensity region. Development and final conductor transfer are not modeled.

KrF 248 nm · NA 0.68 · sigma 0.60 · ROI 2.56 µm · pixel 10 nm · ambit 0.32 µm · internal DBU 0.1 nm

![Fixed reference and relative-dose contours]({{ '/assets/demo/v0.10/speed/reference_anchor.png' | relative_url }})

Speed uses dense7 with optional nominal-dose Region screening (off by default); Internal uses dense11 with screening at all three preview doses. Both provide all three contours. Each is fitted independently and their responses are not interchangeable. Candidate ordering prioritizes measured width/space, with area as a secondary heuristic.

[Demo]({{ '/demo/' | relative_url }}) · [Method]({{ '/method/' | relative_url }}) · [Technical Notes]({{ '/notes/' | relative_url }}) · [v0.10]({{ '/release-notes/v0.10/' | relative_url }})

{% include live-demo-cta.html %}
