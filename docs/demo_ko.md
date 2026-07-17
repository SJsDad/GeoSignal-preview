---
layout: default
title: Demo
description: GeoSignal Preview 데모 한국어 설명
permalink: /ko/demo/
---

[English]({{ site.baseurl }}/demo/) | [한국어]({{ site.baseurl }}/ko/demo/)

# Demo

## 1. Demo Overview

이 페이지는 **GeoSignal Preview**의 대표 데모 결과를 정리한 페이지입니다.

GeoSignal Preview는 layout geometry에서 후보 ROI를 선택하고, 해당 영역에 대해 rasterized mask, simplified Abbe-based aerial image, multi-threshold contour를 생성한 뒤 hotspot-like 형상을 시각적으로 확인하는 workflow입니다.

정확한 공정 예측이나 최적화된 hotspot 검출기가 목표는 아닙니다. 이 데모는 geometry-only review를 optical-response 및 contour-behavior visualization으로 확장하는 흐름을 보여줍니다.

기본 데모 흐름은 다음과 같습니다.

```text
Layout Geometry
    -> Geometry-based Candidate Filtering
    -> ROI Selection
    -> Rasterized Mask
    -> Abbe-based Aerial Image
    -> Multi-threshold Contour
    -> Hotspot-like Shape Review
```

![GeoSignal demo pipeline](assets/demo/demo_pipeline_overview.png)

전체 workflow는 다음 두 부분으로 이해할 수 있습니다.

```text
Layout Geometry
    -> Width / Space screening
    -> Candidate ROI selection

Candidate ROI
    -> Rasterized Mask
    -> Aerial Image
    -> Multi-threshold Contour
    -> Hotspot-like Shape Review
```

최근 구현 변경점, pya-native 적용, candidate overview 변경, benchmark 내용은 [Release Notes]({{ '/release-notes/' | relative_url }})로 분리했습니다.

---

## 2. Candidate Selection in This Demo

현재 demo에서는 minimum width / space 관점에서 후보 영역을 먼저 찾은 뒤, 그중 일부 ROI를 선택하여 aerial image와 contour를 생성합니다.

선택된 후보는 최종 hotspot 판정이 아니라 representative review example입니다. 구체적인 screening rule과 ordering 방식은 데모를 구체화하고 계산량을 관리하기 위한 preview-stage heuristic입니다.

중요한 것은 다음 구조입니다.

```text
geometry 기준으로 취약 가능성이 높은 위치를 먼저 찾고
    -> 해당 위치에서 optical response를 계산하고
    -> threshold contour를 통해 형상 변화를 확인한다
```

v0.6의 pya-native geometry handling과 candidate ordering은 [v0.6 Release Notes]({{ '/release-notes/v0.6/' | relative_url }})에 정리했습니다. 통합 review GDS, candidate별 contour datatype, 서비스 메모리 변경은 [v0.7 Release Notes]({{ '/release-notes/v0.7/' | relative_url }})에 정리했습니다.

---

## 3. What This Demo Shows

| 항목 | 설명 |
| --- | --- |
| Geometry-based Candidate | layout 상의 minimum width / space 기준으로 먼저 선별한 후보 영역 |
| ROI Selection | 계산 가능한 범위에서 우선 검토할 후보 영역 선택 |
| Rasterized Mask | layout polygon을 pixel grid 위의 binary mask로 변환한 결과 |
| Aerial Image | simplified Abbe-based imaging으로 계산한 optical intensity map |
| Multi-threshold Contour | threshold 0.20 / 0.30 / 0.40 기준으로 추출한 contour |
| Hotspot-like Shape Review | necking, pinch, corner rounding, line-end pullback, bridge-like behavior 등을 시각적으로 검토 |

Threshold contour는 calibrated resist contour가 아닙니다. Aerial image가 threshold level에 따라 어떤 contour behavior로 나타나는지 확인하기 위한 정성적 시각화 기준입니다.

---

## 4. Representative Candidate Results

현재 demo는 네 개의 대표 candidate ROI를 보여줍니다.

```text
WIDTH_0001
WIDTH_0002
SPACE_0001
SPACE_0002
```

각 이미지는 aerial image, multi-threshold contours, ROI marker, hotspot-like shape annotation을 함께 보여줍니다.

### Width Candidate 0001

![Width candidate 0001](assets/demo/demo_width_0001_threshold_overlay.png)

### Width Candidate 0002

![Width candidate 0002](assets/demo/demo_width_0002_threshold_overlay.png)

### Space Candidate 0001

![Space candidate 0001](assets/demo/demo_space_0001_threshold_overlay.png)

### Space Candidate 0002

![Space candidate 0002](assets/demo/demo_space_0002_threshold_overlay.png)

---

## 5. Common Interpretation Points

주요 확인 포인트는 다음과 같습니다.

* aerial image에서 edge blur 또는 intensity spreading이 보이는가?
* line-end pullback-like behavior가 나타나는가?
* corner rounding-like behavior가 나타나는가?
* narrow-width 주변에서 necking 또는 pinch-like behavior가 보이는가?
* narrow-space 주변에서 bridge-like behavior가 보이는가?
* 0.20 / 0.30 / 0.40 threshold contour가 얼마나 이동하는가?
* 큰 contour movement가 geometry-based candidate 위치와 맞물리는가?

이 demo의 목적은 최종 hotspot 판정이 아니라, 추가 검토할 위치를 빠르게 좁히는 것입니다.

---

## 6. Current Scope and Limitations

* width / space screening criterion은 preview heuristic이며 calibrated process rule이 아닙니다.
* candidate selection은 optimized hotspot-ranking logic이 아닙니다.
* 계산량을 고려해 소수의 대표 ROI만 보여줍니다.
* simplified Abbe-based imaging model을 사용합니다.
* wafer-data calibration, resist model, etch model은 포함하지 않습니다.
* threshold contour는 qualitative visualization 기준입니다.
* CD prediction accuracy가 목표가 아닙니다.
* live demo에는 public, non-confidential GDS/OAS file만 사용해야 합니다.

---

## 7. Related Pages

* [Home]({{ '/ko/' | relative_url }})
* [Method]({{ '/ko/method/' | relative_url }})
* [Technical Notes]({{ '/notes/' | relative_url }})
* [Release Notes]({{ '/release-notes/' | relative_url }})
