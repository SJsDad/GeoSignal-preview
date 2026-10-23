---
layout: default
title: GeoSignal Preview
description: 공개 레이아웃 검토 예시와 브라우저 기반 6f 광학 학습 데모
permalink: /ko/
lang: ko
---

# GeoSignal Preview

**레이아웃에서 폭과 간격이 좁은 후보를 찾고, 선택한 영역을 단순화된 광학 모델로 살펴봅니다.** 공개 프리뷰는 형상 검토를 aerial image·상대 도즈 윤곽과 연결합니다.

![레이아웃에서 후보와 광학 결과를 살펴보는 흐름]({{ '/assets/demo/public/overview.png' | relative_url }})

공개 TT04 PWM 레이아웃의 한 영역을 마스크·빛 분포·윤곽으로 이어서 보여줍니다. 웨이퍼 실측이 아닌 모델 예시입니다.

{% include live-demo-cta.html %}

## GDS/OAS 레이아웃 검토

레이아웃 분석 데모는 후보 위치를 표시하고 주변의 광학 반응을 비교합니다. [데모]({{ '/ko/demo/' | relative_url }})에서 예시 조건과 그림 해석을, [방법론]({{ '/ko/method/' | relative_url }})에서 개념적인 흐름을 확인할 수 있습니다.

## 6f 교육용 시뮬레이터

[6f 시뮬레이터 실행]({{ '/ko/simulator/' | relative_url }})에서 광원부터 웨이퍼까지 광선을 따라가며 같은 차수의 pupil·파동 결과를 조작할 수 있습니다. 한글·영문 화면이 Pages에서 직접 실행되어 Render 기동 대기가 없습니다. [광학 원리]({{ '/ko/notes/diffraction-defocus/' | relative_url }})를 함께 읽어보세요.

## 페이지 안내

| 페이지 | 내용 |
| --- | --- |
| [데모]({{ '/ko/demo/' | relative_url }}) | 대표 결과와 해석 |
| [방법론]({{ '/ko/method/' | relative_url }}) | 개념적인 흐름과 모델 범위 |
| [기술 노트]({{ '/ko/notes/' | relative_url }}) | 광학 기초와 논문 해설 |
| [릴리즈 노트]({{ '/ko/release-notes/' | relative_url }}) | 사용자에게 달라진 동작과 검증 요약 |

[v0.12 노트]({{ '/ko/release-notes/v0.12/' | relative_url }})에 한영 시뮬레이터와 공개 문서 변경을 정리했습니다. v0.11의 수치 연구는 현재 레이아웃 분석 데모에 새 옵션을 추가하는 변경이 아닙니다.

## 범위와 의견

공개·합성 레이아웃의 선택 영역을 살펴보는 교육용 도구이며, 정합된 공정 검증 서비스는 아닙니다. 라이브 데모에는 공개된 비기밀 파일만 사용해 주세요. 사이트 메뉴에서 의견을 보낼 수 있습니다.
