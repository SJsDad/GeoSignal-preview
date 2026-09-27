---
layout: default
title: Demo
description: GeoSignal relative exposure study and validation
permalink: /ko/demo/
lang: ko
---

<p class="language-switch"><a href="{{ '/demo/' | relative_url }}" lang="en">View in English</a></p>

# Demo — v0.10

> 이 페이지는 로컬 검증을 완료한 v0.10 snapshot입니다. Live Render 배포 상태와는 별개입니다.

설계 anchor의 nominal CD를 맞춘 상대 노광 모델입니다. 실제 wafer CD fitting이나 scanner/resist 공정 calibration이 아닙니다. Polygon 투과율은 1이며 contour는 고강도 영역입니다. PTD/NTD 현상 또는 최종 배선 전사는 모델링하지 않습니다.

KrF 248 nm · NA 0.68 · sigma 0.60 · ROI 2.56 µm · pixel 10 nm · ambit 0.32 µm · internal DBU 0.1 nm

입력: 공개 TT04 PWM, SKY130 li1 67/20. Reference는 (147.770, 108.460) µm의 170 nm dense line이며 수직 고정 단면으로 측정합니다. Geometry 후보 2개와 별도 reference 1개를 평가했습니다. Reference는 severity ranking을 대체하지 않습니다.

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

PW 검증은 focus −0.40…+0.40 µm, step 0.05 µm와 dose 0.80…1.20, step 0.02를 사용합니다. 각 preset은 357조건 × 3개 위치 = 1,071행입니다. 이 예제의 common nominal-dose DoF는 0입니다. Anchor fitting이 다른 취약 후보의 PASS를 보장하지 않습니다. 시간과 메모리는 로컬 측정이며 Render 성능 보장이 아닙니다.

[Method]({{ '/ko/method/' | relative_url }}) · [Validation notes]({{ '/ko/notes/v0.10-validation/' | relative_url }}) · [Legacy Demo]({{ '/ko/demo-legacy/' | relative_url }})
