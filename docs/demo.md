---
layout: default
title: Demo
description: GeoSignal relative exposure study and validation
permalink: /demo/
---

<p class="language-switch"><a href="{{ '/ko/demo/' | relative_url }}" lang="ko">한국어로 보기</a></p>

# Demo — v0.10

> This is a locally validated v0.10 snapshot. The live Render deployment may differ.

The nominal model CD is fitted to a design anchor. This is not measured-wafer fitting or scanner/resist process calibration. Polygon transmission is 1 and the contour describes the high-intensity region. Development and final conductor transfer are not modeled.

KrF 248 nm · NA 0.68 · sigma 0.60 · ROI 2.56 µm · pixel 10 nm · ambit 0.32 µm · internal DBU 0.1 nm

Input: public TT04 PWM, SKY130 li1 67/20. The reference is a 170 nm dense line at (147.770, 108.460) µm measured on a fixed vertical gauge. Two ranked geometry candidates and one separate reference were evaluated. The reference does not replace severity ranking.

`Tnorm = T0 / D0`, `T_eff = Tnorm / d`.

| Preset | Relative dose | T0 | D0 | T_eff | CD (nm) |
|---|---:|---:|---:|---:|---:|
| speed | 0.90 | 0.30 | 0.82421875 | 0.404423 | 152.019 |
| speed | 1.00 | 0.30 | 0.82421875 | 0.363981 | 170.018 |
| speed | 1.10 | 0.30 | 0.82421875 | 0.330892 | 184.658 |
| internal | 0.90 | 0.30 | 0.84765625 | 0.393241 | 152.296 |
| internal | 1.00 | 0.30 | 0.84765625 | 0.353917 | 169.979 |
| internal | 1.10 | 0.30 | 0.84765625 | 0.321743 | 184.384 |

## speed

![speed reference gauge and relative dose contours]({{ '/assets/demo/v0.10/speed/reference_anchor.png' | relative_url }})

- [Dose / CD CSV]({{ '/assets/demo/v0.10/speed/reference_dose.csv' | relative_url }})
- [Model and reference JSON]({{ '/assets/demo/v0.10/speed/relative_dose_model.json' | relative_url }})
- [Focus / dose CSV]({{ '/assets/demo/v0.10/speed/focus_dose_measurements.csv' | relative_url }})
- [Region hotspot checks]({{ '/assets/demo/v0.10/speed/contour_hotspots.json' | relative_url }})
- [Review GDS]({{ '/assets/demo/v0.10/speed/pya_native_combined_review.gds' | relative_url }})

## internal

![internal reference gauge and relative dose contours]({{ '/assets/demo/v0.10/internal/reference_anchor.png' | relative_url }})

- [Dose / CD CSV]({{ '/assets/demo/v0.10/internal/reference_dose.csv' | relative_url }})
- [Model and reference JSON]({{ '/assets/demo/v0.10/internal/relative_dose_model.json' | relative_url }})
- [Focus / dose CSV]({{ '/assets/demo/v0.10/internal/focus_dose_measurements.csv' | relative_url }})
- [Region hotspot checks]({{ '/assets/demo/v0.10/internal/contour_hotspots.json' | relative_url }})
- [Review GDS]({{ '/assets/demo/v0.10/internal/pya_native_combined_review.gds' | relative_url }})

PW validation uses focus −0.40…+0.40 µm in 0.05 µm steps and dose 0.80…1.20 in 0.02 steps: 357 conditions × 3 locations = 1,071 rows per preset. Common nominal-dose DoF is zero for this example; fitting the reference does not ensure other weak candidates pass. Timing and memory are local measurements, not Render guarantees.

[Method]({{ '/method/' | relative_url }}) · [Validation notes]({{ '/notes/v0.10-validation/' | relative_url }}) · [Legacy Demo]({{ '/demo-legacy/' | relative_url }})
