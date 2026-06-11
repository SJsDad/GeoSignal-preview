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

GeoSignal Preview는 layout geometry에서 먼저 검토 후보 영역을 찾고, 해당 영역에 대해 rasterized mask, simplified Abbe-based aerial image, multi-threshold contour를 생성한 뒤, hotspot-like 형상을 시각적으로 확인하는 workflow입니다.

이 데모의 목적은 정확한 공정 예측이나 최적화된 hotspot 검출기를 제시하는 것이 아닙니다.

대신 다음 흐름을 보여주는 데 초점을 둡니다.

```text
1차: geometry 기반 후보 영역 필터링
2차: 선택된 후보 영역에 대한 optical response 및 contour behavior 검토
```

즉, 이 demo는 다음 질문을 다룹니다.

> minimum width / space 관점에서 먼저 의심되는 영역을 찾은 뒤, 해당 영역이 optical response와 threshold contour 관점에서도 추가 검토할 가치가 있는지 확인할 수 있는가?

GeoSignal Preview의 기본 데모 흐름은 다음과 같습니다.

```text
Layout Geometry
    → Geometry-based Candidate Filtering
    → ROI Selection
    → Rasterized Mask
    → Abbe-based Aerial Image
    → Multi-threshold Contour
    → Hotspot-like Shape Review
```

![GeoSignal demo pipeline](assets/demo/demo_pipeline_overview.png)

전체 workflow는 크게 두 단계로 나눌 수 있습니다.

첫 번째는 **geometry 기반 1차 후보 필터링**입니다.

```text
Layout Geometry
    → Width / Space screening
    → Candidate ROI selection
```

두 번째는 **선택된 ROI에 대한 optical contour review**입니다.

```text
Candidate ROI
    → Rasterized Mask
    → Aerial Image
    → Multi-threshold Contour
    → Hotspot-like Shape Review
```

이 demo는 모든 layout 영역에 대해 optical simulation을 수행하는 방식이 아닙니다.
먼저 geometry 기준으로 검토 우선순위가 높은 영역을 좁힌 뒤, 제한된 ROI에 대해 optical model 기반 contour를 확인하는 방식입니다.

이 접근은 계산량을 줄이면서도, 사람이 우선적으로 확인해야 할 lithography-aware review point를 빠르게 살펴보기 위한 preview workflow입니다.

---

## 2. Candidate Selection Policy in This Demo

현재 demo에서는 minimum width / space 관점에서 후보 영역을 먼저 찾은 뒤, 그중 일부 ROI를 선택하여 aerial image와 contour를 생성했습니다.

구체적으로는 다음과 같은 방식으로 대표 후보를 구성했습니다.

```text
1. width 또는 space가 0.200 µm 이하인 영역을 1차 후보로 추출
2. width-related candidate와 space-related candidate를 구분
3. 계산량을 고려하여 width 후보 2개, space 후보 2개를 선택
4. 선택된 4개 ROI에 대해 aerial image와 multi-threshold contour를 생성
```

여기서 `0.200 µm` 기준은 공정 rule이나 calibrated hotspot threshold가 아닙니다.
현재 demo에서는 minimum width / space 기준을 알고 있다고 가정하고, 해당 기준 주변의 취약 후보 영역을 먼저 찾아본다는 의미로 사용한 임의의 preview 기준입니다.

또한 후보를 선택하는 방식 역시 현재 단계에서는 최적화된 ranking logic이 아닙니다.
면적이 큰 후보 영역을 우선적으로 선택한 것은 demo 구성을 위한 pragmatic choice이며, 실제 hotspot 우선순위 판단 기준으로 확정된 것은 아닙니다.

현재 candidate selection은 다음과 같이 이해하는 것이 적절합니다.

```text
최종 hotspot 판정 로직
    X

preview 목적의 1차 geometry-based filtering
    O
```

즉, 이 demo에서 중요한 것은 `0.200 µm` 기준 자체나 후보 ranking 방식이 아니라, 다음 workflow입니다.

```text
geometry 기준으로 취약 가능성이 높은 위치를 먼저 찾고
→ 해당 위치에서 optical response를 계산하고
→ threshold contour를 통해 추가 검토가 필요한 형상 변화를 확인한다
```

향후에는 candidate selection logic을 개선하여 단순 width / space 기준뿐 아니라, contour mismatch, local pattern context, line-end, corner, neighboring density, contact / via overlay 관점 등을 함께 고려하는 방향으로 확장할 수 있습니다.

---

## 3. What This Demo Shows

이 demo에서 확인하는 핵심 항목은 다음과 같습니다.

| 항목                        | 설명                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------ |
| Geometry-based Candidate  | layout 상의 minimum width / space 기준으로 먼저 선별한 후보 영역                                    |
| ROI Selection             | 계산 가능한 범위에서 우선 검토할 후보 영역 선택                                                          |
| Rasterized Mask           | layout polygon을 pixel grid 위의 binary mask로 변환한 결과                                    |
| Aerial Image              | simplified Abbe-based imaging으로 계산한 optical intensity map                            |
| Multi-threshold Contour   | threshold 0.20 / 0.30 / 0.40 기준으로 추출한 contour                                        |
| Hotspot-like Shape Review | necking, pinch, corner rounding, line-end pullback, bridge-like behavior 등을 시각적으로 검토 |

핵심 비교 대상은 다음입니다.

```text
geometry-based candidate
    vs
aerial-image-based optical response
    vs
threshold-contour-based printed-shape-like behavior
```

현재 demo에서 사용하는 threshold contour는 calibrated resist contour가 아닙니다.
대신 aerial image가 threshold level에 따라 어떤 contour behavior로 나타나는지 확인하기 위한 정성적 시각화 기준입니다.

---

## 4. Representative Candidate Results

현재 demo는 4개의 대표 candidate ROI를 보여줍니다.

```text
WIDTH_0001
WIDTH_0002
SPACE_0001
SPACE_0002
```

이 4개 후보는 width / space 기준으로 추출된 후보 중 일부를 계산량을 고려하여 선택한 preview example입니다.
각 후보는 개별적으로 다른 해석을 하기보다는, 동일한 관점에서 aerial image와 multi-threshold contour behavior를 확인하기 위한 예시로 보는 것이 적절합니다.

각 이미지는 다음 정보를 함께 보여줍니다.

```text
aerial image
+ multi-threshold contours
+ ROI marker
+ hotspot-like shape annotation
```

아래 이미지는 특정 후보가 실제 공정에서 반드시 fail이 된다는 의미가 아닙니다.
대신 layout 상의 width / space 기준으로 먼저 선택된 후보 영역에서, optical response와 contour behavior가 어떻게 나타나는지 확인하기 위한 preview result입니다.

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

4개의 후보 이미지는 각각 다른 ROI를 보여주지만, 해석 관점은 동일합니다.

각 이미지에서 주로 확인하는 내용은 다음과 같습니다.

* aerial image에서 edge blur 또는 intensity spreading이 나타나는지
* line-end 주변에서 pullback-like behavior가 보이는지
* corner 주변에서 rounding-like behavior가 나타나는지
* narrow width 주변에서 necking 또는 pinch-like behavior가 나타나는지
* narrow space 주변에서 bridge-like behavior 가능성이 보이는지
* threshold 0.20 / 0.30 / 0.40 contour가 얼마나 이동하는지
* contour movement가 큰 위치가 geometry-based candidate와 잘 연결되는지
* contact / via overlay 또는 다른 layer와의 관계를 고려했을 때 공정 이슈로 이어질 수 있는 위치가 있는지
* 향후 mask correction 또는 mask optimization 검토 대상으로 볼 만한 위치가 있는지

이 demo의 철학은 hotspot을 최종 판정하는 것이 아니라, 사람이 먼저 봐야 할 위치를 빠르게 좁혀주는 것입니다.

즉, GeoSignal Preview는 다음과 같은 lightweight review tool을 지향합니다.

```text
geometry 기준 후보 추출
    → optical response 확인
    → contour behavior 확인
    → 공정 이슈 가능성이 있는 위치를 우선 검토
    → 필요 시 mask correction 또는 추가 simulation으로 연결
```

---

## 6. 결과를 읽는 순서

Demo 결과는 다음 순서로 보는 것을 권장합니다.

1. 먼저 전체 pipeline image에서 workflow를 확인합니다.
2. layout 상의 width / space 기준으로 후보 ROI를 먼저 선별한다는 점을 이해합니다.
3. 현재 demo의 `0.200 µm` 기준과 후보 선택 방식은 preview용 heuristic임을 전제로 봅니다.
4. 선택된 ROI에서 aerial image가 어떻게 형성되는지 확인합니다.
5. threshold 0.20 / 0.30 / 0.40 contour가 어떻게 이동하는지 확인합니다.
6. necking, pinch, corner rounding, line-end pullback, bridge-like behavior가 나타나는 위치를 확인합니다.
7. 해당 위치가 향후 mask optimization 또는 추가 lithography-aware review 대상으로 적절한지 판단합니다.

핵심 질문은 다음입니다.

```text
Geometry 기준으로 먼저 의심되는 위치는 어디인가?
그 위치가 optical response에서도 약하거나 불안정하게 보이는가?
Threshold contour 관점에서 movement가 큰 위치는 어디인가?
이 위치가 contact / via overlay 또는 다른 layer 조건과 결합될 때 공정 risk로 이어질 수 있는가?
추후 mask correction 또는 추가 simulation 대상으로 볼 가치가 있는가?
```

---

## 7. Current Scope and Limitations

현재 demo는 public preview 목적의 정성적 시각화 결과입니다.

다음과 같은 한계를 가집니다.

* `0.200 µm` width / space 기준은 demo용 임의 기준입니다.
* 후보 선택 방식은 최적화된 hotspot ranking logic이 아닙니다.
* width 후보 2개와 space 후보 2개만 사용한 것은 계산량을 고려한 preview 구성입니다.
* Abbe 기반 simplified imaging model을 사용합니다.
* wafer data 기반 calibration은 포함하지 않습니다.
* resist model과 etch model은 포함하지 않습니다.
* threshold contour는 정성적 비교와 시각화를 위한 기준입니다.
* CD prediction accuracy를 목표로 하지 않습니다.
* public 또는 synthetic example 중심으로 구성됩니다.
* core implementation code는 public preview repository에 포함하지 않습니다.

따라서 현재 결과는 다음과 같이 해석하는 것이 적절합니다.

```text
qualitative visual indicator
```

다음과 같이 해석하면 안 됩니다.

```text
production specification
```

즉, 이 demo는 정확한 공정 결과 예측보다는 **geometry-only review에서 optical contour-based lithography-aware review로 확장할 수 있음을 보여주는 preview**입니다.

---

## 8. Future Work

향후에는 다음 방향으로 개선할 수 있습니다.

| 항목                             | 방향                                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------- |
| Candidate selection            | 단순 width / space 기준을 넘어 pattern context, line-end, corner, density, neighboring feature를 고려 |
| Ranking logic                  | 면적 기준이 아닌 contour sensitivity, mask-contour mismatch, local contrast 등을 반영                  |
| Runtime improvement            | 더 넓은 layout 영역을 다루기 위한 계산 최적화                                                               |
| Accuracy / imaging improvement | source 고도화, 더 많은 source point 사용, 계산 효율화를 위한 TCC 적용 검토 등                                    |
| Mask optimization              | contour 결과를 바탕으로 간단한 mask correction 또는 rule-based adjustment 검토                            |
| Layer-aware review             | contact / via overlay, metal / gate relation 등 다른 layer와의 관계 검토                             |
| Additional examples            | dense line-space, isolated line-end, narrow gap, corner pattern 등 case 확장                   |

현재 demo는 이 중 첫 단계에 해당합니다.

즉, 우선은 다음 질문에 답하는 데 집중합니다.

> geometry 기반으로 먼저 의심되는 위치를 찾고, 그 위치를 optical contour 관점에서 빠르게 확인할 수 있는가?

---

## 9. 받고 싶은 피드백

이 demo에서 받고 싶은 피드백은 다음과 같습니다.

* multi-threshold contour가 contour sensitivity를 이해하는 데 도움이 되는지
* hotspot-like 형상 확인이 직관적인지
* necking, corner rounding, line-end pullback, bridge-like behavior 관찰이 유용한지
* 향후 mask correction 또는 mask optimization으로 연결되는 방향이 필요한지
* runtime과 accuracy 개선 관점에서 어떤 방향이 더 중요해 보이는지
* 어떤 pattern case가 추가되면 preview가 더 명확해질지

짧은 의견, 질문, 첫인상 수준의 코멘트도 모두 유용합니다.

---

## 10. Related Pages

* [Home](./)
* [Method](method.md)
* [Technical Notes](notes/)
