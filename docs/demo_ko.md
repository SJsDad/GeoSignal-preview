---
layout: default
title: Demo
description: GeoSignal Preview 데모 한국어 설명
permalink: /ko/demo/
lang: ko
---

<p class="language-switch"><a href="{{ '/demo/' | relative_url }}" lang="en">View in English</a></p>

# Demo

## 1. Demo Overview

이 페이지는 **GeoSignal Preview**의 대표 데모 결과를 정리한 페이지입니다.

{% include live-demo-cta.html %}

GeoSignal Preview는 layout geometry에서 후보 ROI를 선택하고, 해당 영역에 대해 rasterized mask, simplified Abbe-based aerial image, relative-dose contour를 생성한 뒤 hotspot-like 형상을 시각적으로 확인하는 workflow입니다.

정확한 공정 예측이나 최적화된 hotspot 검출기가 목표는 아닙니다. 이 데모는 geometry-only review를 optical-response 및 contour-behavior visualization으로 확장하는 흐름을 보여줍니다.

기본 데모 흐름은 다음과 같습니다.

```text
Layout Geometry
    -> Geometry-based Candidate Filtering
    -> ROI Selection
    -> Rasterized Mask
    -> Abbe-based Aerial Image
    -> Relative-dose Contour
    -> Hotspot-like Shape Review
```

전체 workflow는 다음 두 부분으로 이해할 수 있습니다.

```text
Layout Geometry
    -> Width / Space screening
    -> Candidate ROI selection

Candidate ROI
    -> Rasterized Mask
    -> Aerial Image
    -> Relative-dose Contour
    -> Hotspot-like Shape Review
```

이 demo는 모든 layout 영역에서 optical simulation을 실행하지 않습니다. Geometry 관점에서 검토 가치가 있는 영역을 먼저 좁힌 다음, 제한된 수의 ROI에 optical-model 기반 contour review를 적용합니다.

이 workflow의 상세 구현 변경점은 [릴리즈 노트]({{ '/ko/release-notes/' | relative_url }})에 정리했습니다.

---

## 2. Candidate Selection in This Demo

현재 서비스는 폭·간격이 좁은 후보를 찾아 기본적으로 5개 위치를 검토합니다. 아래에는 상위 폭 후보 6개와 간격 후보 6개를 표시했습니다. 다운로드 자료는 폭·간격 후보 각 한 곳과 별도의 기준 패턴 한 곳을 포함합니다. ROI는 선택한 위치 주변의 작은 검토 영역입니다.

선택된 후보는 최종 hotspot 판정이 아니라 representative review example입니다. 구체적인 screening rule과 ordering 방식은 데모를 구체화하고 계산량을 관리하기 위한 preview-stage heuristic입니다.

중요한 것은 다음 구조입니다.

```text
geometry 기준으로 취약 가능성이 높은 위치를 먼저 찾고
    -> 해당 위치에서 optical response를 계산하고
    -> threshold contour를 통해 형상 변화를 확인한다
```

현재 예제는 공개 TT04 PWM layout의 67/20 레이어를 Speed 설정으로 계산했습니다. 더 좁은 폭·간격을 우선하고, 같은 값이면 병합된 후보 영역이 큰 곳을 먼저 봅니다. 짧은 구간을 일괄 제외하지 않으며, 선 끝만을 따로 찾는 규칙은 아닙니다.

| 예제 항목 | 내용 |
| --- | --- |
| 입력 | 공개 TT04 PWM GDS |
| 대상 레이어 | 67/20 |
| 검사 기준 | 폭 또는 간격이 0.200 µm보다 좁은 곳 |
| 표시한 결과 | 상위 폭 후보 6개와 간격 후보 6개 |
| 비교 조건 | 빛의 양 −10% / 기준 / +10% |

광학 설정, 측정 기준과 평가 결과는 [v0.10 릴리즈 노트]({{ '/ko/release-notes/v0.10/' | relative_url }})에서 확인할 수 있습니다.

---

## 3. What This Demo Shows

| 항목 | 설명 |
| --- | --- |
| Geometry-based Candidate | layout 상의 minimum width / space 기준으로 먼저 선별한 후보 영역 |
| ROI Selection | 계산 가능한 범위에서 우선 검토할 후보 영역 선택 |
| Rasterized Mask | layout polygon을 pixel grid 위의 binary mask로 변환한 결과 |
| Aerial Image | simplified Abbe-based imaging으로 계산한 optical intensity map |
| Relative-dose Contour | 빛의 양을 기준 대비 −10% / 기준 / +10%로 바꾸어 계산한 경계선 |
| Hotspot-like Shape Review | necking, pinch, corner rounding, line-end pullback, bridge-like behavior 등을 시각적으로 검토 |

핵심 비교 구조는 다음과 같습니다.

```text
geometry-based candidate
    vs
aerial-image-based optical response
    vs
threshold-contour-based printed-shape-like behavior
```

윤곽은 기준 패턴의 설계 폭에 맞춘 상대 비교 모델의 결과입니다. 빛의 양을 바꿀 때 모양이 어떻게 달라지는지 살펴볼 수 있지만, 실제 웨이퍼 측정값에 맞춘 공정 예측은 아닙니다.

---

## 4. Representative Candidate Results

아래 그림은 현재 코드의 분석 경로로 로컬에서 생성한 공개 예제입니다. 먼저 전체 후보 분포를 보고, 선택한 위치의 원래 도형과 계산한 윤곽을 비교합니다.

### Analysis Summary

폭 후보와 간격 후보는 검토할 위치를 뜻합니다. 별도의 기준 패턴은 비교 출발점을 맞추기 위한 것이며 추가로 발견한 hotspot이 아닙니다. 넓게 표시된 후보 영역에는 여러 작은 검사 결과가 병합되어 있을 수 있습니다.

### Geometry Candidate Overview

![전체 폭·간격 후보 분포]({{ '/assets/demo/v0.10/speed/geometry_candidate_overview.png' | relative_url }})

분포도는 전체 도면에서 폭·간격이 좁은 곳과 선택한 위치를 보여줍니다. 표시가 조밀한 부분부터 살펴볼 수 있지만, 표시 개수를 실제 불량 개수로 해석하지는 않습니다.

### 상위 Width 후보 6개

![에어리얼 이미지와 도즈별 윤곽선을 표시한 상위 폭 후보 6개]({{ '/assets/release-notes/v0.10/width_area_desc_review/top6.png' | relative_url }})

같은 조건에서 선택한 폭 후보 6개를 나란히 비교합니다. 마스크 위의 붉은색 계열은 계산한 빛의 분포이며, 밝을수록 빛의 세기가 큽니다. 하늘색·흰색·연두색 선은 각각 기준보다 빛을 10% 적게, 기준만큼, 10% 많이 주었을 때의 윤곽입니다. 주황색 십자는 검토 위치입니다.

그림의 CD는 원래 도형에서 측정한 폭입니다. 후보의 순서는 이 폭을 먼저 비교하고, 같으면 후보 영역의 면적이 큰 쪽을 우선합니다. 빛을 계산한 뒤의 윤곽이나 실제 공정의 위험도 순위와는 구분해야 합니다. 아래 링크에서 큰 크기로 볼 수 있습니다.

[6개 후보 이미지 크게 보기]({{ '/assets/release-notes/v0.10/width_area_desc_review/top6.png' | relative_url }}) · [조건과 자세한 평가]({{ '/ko/release-notes/v0.10/' | relative_url }})

### 상위 Space 후보 6개

![상위 Space 후보 6개]({{ '/assets/release-notes/v0.10/width_area_desc_review/space_top6.png' | relative_url }})

Width와 같은 조건·색상으로 상위 간격 후보 6개를 비교합니다. 간격이 좁은 순서로, 같으면 병합된 후보 영역이 큰 순서로 선택했습니다. 첫 세 후보가 비슷하게 보이는 것은 서로 다른 좌표에 반복된 패턴이 있기 때문입니다.

[6개 간격 후보 이미지 크게 보기]({{ '/assets/release-notes/v0.10/width_area_desc_review/space_top6.png' | relative_url }})

### Download and Continue

[검토용 GDS]({{ '/assets/demo/v0.10/speed/pya_native_combined_review.gds' | relative_url }})를 내려받아 다른 레이아웃 뷰어에서도 원래 도형, 검토 영역과 윤곽을 함께 볼 수 있습니다. 측정 수치, 보정 조건과 추가 그래프는 [v0.10 릴리즈 노트]({{ '/ko/release-notes/v0.10/' | relative_url }})에 있습니다.

<h3 id="getting-started">직접 예제를 사용하려면</h3>

공개 가능한 GDS/OAS와 레이어를 선택하고 Speed 설정으로 시작합니다. 등록된 TT04 예제에는 기준 패턴이 준비되어 있습니다. 다른 파일은 현재 기준 위치·방향·설계 폭을 입력해야 합니다. 결과에서는 측정 불가나 검사 생략 상태도 함께 확인해 주세요.

---

## 5. Common Interpretation Points

Summary, 선택 overlay, measurement 확대 결과, geometry overview를 함께 검토해야 합니다.

주요 확인 포인트는 다음과 같습니다.

* aerial image에서 edge blur 또는 intensity spreading이 보이는가?
* line-end pullback-like behavior가 나타나는가?
* corner rounding-like behavior가 나타나는가?
* narrow-width 주변에서 necking 또는 pinch-like behavior가 보이는가?
* narrow-space 주변에서 bridge-like behavior가 보이는가?
* 상대 노광량별 윤곽가 얼마나 이동하는가?
* 큰 contour movement가 geometry-based candidate 위치와 맞물리는가?

이 demo의 목적은 최종 hotspot 판정이 아니라, 추가 검토할 위치를 빠르게 좁히는 것입니다.

---

## 6. Current Scope and Limitations

현재 demo는 public preview를 위한 정성적 시각화 결과입니다.

다음과 같은 한계가 있습니다.

* width / space screening criterion은 preview heuristic이며 calibrated process rule이 아닙니다.
* candidate selection은 optimized hotspot-ranking logic이 아닙니다.
* 계산량을 고려해 소수의 대표 ROI만 보여줍니다.
* simplified Abbe-based imaging model을 사용합니다.
* Wafer-data-based calibration은 포함하지 않습니다.
* Resist 및 etch model은 포함하지 않습니다.
* threshold contour는 qualitative visualization 기준입니다.
* CD prediction accuracy가 목표가 아닙니다.
* Public 또는 synthetic example을 사용합니다.
* live demo에는 public, non-confidential GDS/OAS file만 사용해야 합니다.
* Public preview repository에는 core implementation code를 포함하지 않습니다.

따라서 현재 결과는 다음과 같은 의미로 해석해야 합니다.

```text
qualitative visual indicators
```

다음과 같은 의미는 아닙니다.

```text
production specifications
```

---

## 7. Feedback Points

다음 항목에 대한 feedback이 특히 도움이 됩니다.

* relative-dose contour가 contour sensitivity를 이해하는 데 도움이 되는지
* hotspot-like shape 관찰이 직관적인지
* necking, corner rounding, line-end pullback, bridge-like behavior 관찰이 유용한지
* 어떤 pattern case를 추가하면 preview가 더 명확해지는지

<a href="{{ site.feedback_url }}" target="_blank" rel="noopener noreferrer">GeoSignal Preview form으로 feedback 남기기</a>

---

## 8. Related Pages

* [Home]({{ '/ko/' | relative_url }})
* [Method]({{ '/ko/method/' | relative_url }})
* [Technical Notes]({{ '/ko/notes/' | relative_url }})
* [Release Notes]({{ '/ko/release-notes/' | relative_url }})
