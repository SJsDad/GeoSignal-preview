---
layout: default
title: GeoSignal Preview
description: GeoSignal Preview 한국어 소개
permalink: /ko/
lang: ko
---

<p class="language-switch"><a href="{{ '/' | relative_url }}" lang="en">View in English</a></p>

# GeoSignal Preview

**GDS/OAS에서 폭과 간격이 좁은 후보를 추리고, 빛의 영향을 계산한 윤곽과 함께 살펴보는 공개 데모입니다.** 파일에서 검토할 위치를 찾고 주변 모양을 분석하는 과정을 한 흐름으로 연결합니다.

![자동 선택한 폭 후보와 조건별 윤곽]({{ '/assets/demo/v0.10/speed/home_aerial_overlay.png' | relative_url }})

<p class="demo-caption">마스크 위에 붉은색 계열의 빛 분포와 윤곽을 겹쳐 표시했습니다. 십자는 검토 위치, 녹색 점선은 2.56 × 2.56 µm 검토 ROI입니다. 각 변 바깥의 광학 여유 폭은 0.32 µm이며, 그림 전체 범위는 3.20 × 3.20 µm입니다. 세 윤곽은 빛을 주는 양을 기준보다 10% 줄인 경우, 기준, 10% 늘린 경우를 보여줍니다. <a href="{{ '/ko/demo/' | relative_url }}">데모에서 결과 살펴보기 →</a></p>

{% include live-demo-cta.html %}

## 현재 공개 프리뷰

폭·간격 검사로 후보를 찾은 뒤 선택한 위치의 광학 이미지와 윤곽을 계산합니다. 기준 패턴으로 비교의 출발점을 맞추며, 등록 예제 외 파일은 현재 기준 위치·방향·설계 폭 입력이 필요합니다. 처음 사용한다면 데모의 시작 안내를 확인해 주세요.

버전별 변경 사항과 검증 결과는 [v0.10 릴리즈 노트]({{ '/ko/release-notes/v0.10/' | relative_url }})에 정리했습니다.

## 1. GeoSignal Preview란?

**GeoSignal Preview**는 public GDS 또는 synthetic layout example을 기반으로, layout geometry가 simplified optical model을 거쳤을 때 어떤 optical response로 나타나는지 시각적으로 확인하기 위한 공개 데모입니다.

핵심 흐름은 다음과 같습니다.

```text
layout geometry
    -> rasterized mask
    -> simplified aerial image
    -> threshold contour
    -> hotspot-like review
```

목표는 정밀한 공정 예측이 아닙니다. 대신 다음 질문을 직관적으로 검토하는 데 초점을 둡니다.

> geometry 기준으로는 단순해 보이는 pattern이 optical response 관점에서는 어떻게 보이는가?

---

## 2. 문제의식

Minimum width, minimum space, density와 같은 geometry 기반 분석은 layout pattern을 이해하는 데 유용합니다. 하지만 geometry check만으로는 특정 pattern이 optical imaging 관점에서 어떻게 변형되어 보일지 직관적으로 파악하기 어려운 경우가 있습니다.

GeoSignal Preview는 layout polygon을 binary mask image로 변환하고, simplified optical model을 이용해 aerial image를 생성한 뒤, threshold contour를 추출하여 geometry 기반 candidate와 optical response를 ROI 단위로 비교합니다.

---

## 3. Preview 구성

| Page | 내용 |
| --- | --- |
| [Demo]({{ '/ko/demo/' | relative_url }}) | 대표 데모 이미지와 결과 해석 |
| [Method]({{ '/ko/method/' | relative_url }}) | 계산 흐름과 해석 방식 |
| [Technical Notes]({{ '/ko/notes/' | relative_url }}) | aerial image, contour, optical interpretation 배경 설명 |
| [Release Notes]({{ '/ko/release-notes/' | relative_url }}) | 버전별 구현 변경점과 평가 기록 |

### Demo

Demo 페이지는 예제 조건, 분석 결과, 선택한 폭·간격 후보의 확대 그림과 전체 후보 분포도를 보여줍니다. 각 그림에서 무엇을 살펴볼지 함께 안내합니다.

### Method

Method 페이지는 candidate ROI 선택, rasterized mask 생성, simplified Abbe-style aerial imaging, source sampling, threshold contour 추출, visual review의 계산 개념을 설명합니다.

### Technical Notes

Technical Notes는 aerial image, threshold contour, source sampling, Fourier optics, Abbe imaging의 추가 배경을 제공합니다.

### Release Notes

Release Notes에는 버전별 구현 세부 사항, benchmark, backend 변경, metric 개선을 정리합니다. Preview의 변화 과정을 확인하려는 독자를 위한 기록이며, demo를 처음 이해할 때 반드시 읽을 필요는 없습니다.

---

## 4. Demo에서 확인할 수 있는 것

Demo에서는 다음 질문을 검토할 수 있습니다.

* geometry 기준으로 단순해 보이는 pattern이 optical response에서는 민감하게 보이는가?
* threshold contour에서 edge rounding, necking, bridge-like response가 관찰되는가?
* geometry-based candidate와 optical-response behavior가 같은 위치를 가리키는가?
* 빛의 양에 따른 윤곽 비교가 contour sensitivity를 이해하는 데 도움이 되는가?

이 데모는 calibrated lithography prediction이 아니라 qualitative review workflow로 이해해야 합니다.

---

## 5. 해석 범위와 한계

GeoSignal Preview 결과는 정성적 시각화와 상대 비교를 위한 것입니다.

현재 가정과 한계는 다음과 같습니다.

* public 또는 synthetic layout example을 사용합니다.
* live demo에는 public, non-confidential layout file만 사용해야 합니다.
* simplified optical model을 사용합니다.
* wafer-data-based calibration은 포함하지 않습니다.
* resist / etch model은 포함하지 않습니다.
* 조건별 윤곽은 단순화한 모델 안에서 비교하는 결과입니다.
* 결과는 quantitative CD prediction이 아니라 qualitative indicator로 해석해야 합니다.
* public preview repository에는 core implementation code가 포함되어 있지 않습니다.

---

## 6. 활용 목적

GeoSignal Preview는 고비용 상용 simulation 환경에 직접 의존하지 않고 초기 학습, 연구, 정성적 비교를 수행하려는 대학 연구실, 학생 프로젝트, 교육 연구자, 소규모 기술 팀에 유용할 수 있습니다.

주요 활용 목적은 다음과 같습니다.

* computational lithography 학습
* layout geometry와 optical response의 관계 이해
* public 또는 synthetic pattern 기반 demo 검토
* aerial-image 및 threshold-contour 시각화 검토
* geometry check와 optical-model 직관의 연결

---

## 7. Feedback

GeoSignal Preview는 초기 public preview입니다.

의견, 질문, 제안이 있다면 feedback form으로 남겨주세요.

<a href="{{ site.feedback_url }}" target="_blank" rel="noopener noreferrer">GeoSignal Preview form으로 feedback 남기기</a>

Demo가 이해하기 쉬운지, contour 비교가 유용한지, 어떤 pattern 예제가 더 있으면 좋은지에 대한 의견이 특히 도움이 됩니다.

---

## 8. 데이터 및 예제 정책

GeoSignal Preview는 public dataset, synthetic pattern, open-source layout example을 기반으로 합니다.

분석 workflow는 공개적으로 공유 가능한 example과 결과 해석을 중심으로 구성합니다. Public preview repository에는 core implementation code를 포함하지 않습니다.

---

## Keywords

`Lithography` · `Layout Analysis` · `GDS/OAS` · `Aerial Image` · `Threshold Contour` · `Hotspot Candidate` · `Python` · `Computational Lithography`
