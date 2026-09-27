---
layout: default
title: Demo
description: GDS/OAS에서 취약 후보를 찾고 광학 윤곽을 살펴보는 레이아웃 분석 도구
permalink: /ko/demo/
lang: ko
---

<p class="language-switch"><a href="{{ '/demo/' | relative_url }}" lang="en">View in English</a></p>

# Demo

## 레이아웃에서 검토할 위치를 찾고, 결과를 읽어 봅니다

**후보 찾기 → 주변 윤곽 살펴보기 → 레이아웃 뷰어에서 추가 검토하기** 순서로 결과를 보여드립니다. 공개 TT04 PWM 레이아웃을 Speed 설정으로 분석한 예입니다.

{% include live-demo-cta.html %}

## 1. 후보가 어디에 모여 있는지 봅니다

분포도는 폭이 좁거나 간격이 좁은 영역을 표시합니다. 개별 위치를 확대하기 전에 후보가 모여 있는 곳을 파악할 수 있습니다. 표시는 형상 검사로 찾은 후보이며, 확정된 불량 개수가 아닙니다.

![공개 TT04 PWM 레이아웃의 폭·간격 후보 분포도]({{ '/assets/demo/v0.10/speed/geometry_candidate_overview.png' | relative_url }})

이 예시는 우선순위로 고른 후보 2개와 별도 기준 패턴을 검토합니다. Live Demo의 기본값은 후보 5개와 기준 패턴입니다. 기준 패턴은 비교 기준을 맞추기 위한 것이며, 추가로 검출한 hotspot이 아닙니다.

## 2. 폭이 좁은 후보를 살펴봅니다

![폭 후보 주변의 형상, 광학 강도와 상대 dose별 윤곽]({{ '/assets/demo/v0.10/speed/width_candidate.png' | relative_url }})

십자 표시와 주변 윤곽을 함께 보세요. 원래 형상에서는 폭 후보로 선택됐지만 nominal 광학 윤곽에서는 측정 중심에 해당 형상이 유지되지 않습니다. 따라서 폭을 0이나 PASS로 표시하지 않고 **측정 불가(`missing_feature`)**로 기록합니다. 추가로 살펴볼 모델의 반응이지, 실제 wafer 불량이 확인됐다는 뜻은 아닙니다.

## 3. 간격이 좁은 후보와 비교합니다

![간격 후보 주변의 형상, 광학 강도와 상대 dose별 윤곽]({{ '/assets/demo/v0.10/speed/space_candidate.png' | relative_url }})

이 후보는 선택한 단면에서 간격을 측정할 수 있습니다. 원래 형상의 후보 간격은 **0.170 µm**, nominal dose의 모델 간격은 약 **0.199 µm**입니다. 세 윤곽이 어디서 벌어지는지, 주변 선 끝과 모서리가 어떻게 달라지는지 살펴보세요.

빨강·어두운색·파랑 윤곽은 각각 상대 dose **−10%, nominal, +10%**입니다. 범례에는 대응하는 effective threshold도 함께 표시합니다. 윤곽 이동이 큰 곳은 민감도를 더 검토할 후보이며, 그 자체로 불량 판정은 아닙니다.

## 4. 결과를 가져가 추가로 검토합니다

[통합 검토 GDS]({{ '/assets/demo/v0.10/speed/pya_native_combined_review.gds' | relative_url }})를 내려받아 레이아웃 뷰어에서 원본 형상, 선택 영역과 윤곽을 함께 확인할 수 있습니다. 측정값이나 모델 조건이 궁금하면 [결과 데이터와 기준 패턴 검증]({{ '/ko/notes/v0.10-validation/' | relative_url }})을 참고하세요.

그림은 저장된 동일 후보 위치에 검증된 상대 dose 계산을 적용한 것입니다. Speed 예시의 상세 contour Region 검사는 꺼져 있으므로, 상세 검사 표시가 없다고 PASS를 뜻하지 않습니다.

<h2 id="getting-started">자신의 공개 예제로 시작하려면</h2>

- 공개 GDS/OAS 파일, 대상 레이어와 Speed 설정을 선택합니다.
- 등록된 TT04 예제에는 기준 패턴이 준비되어 있습니다. 다른 파일은 아직 기준 위치·방향·설계 폭 입력이 필요하며, 이 부분은 현재 preview의 사용성 제약입니다.
- 먼저 후보 분포를 보고, 국소 윤곽과 측정 상태를 확인합니다. 계산 과정이 궁금할 때 Method를 읽으면 됩니다.
- 서버 분석은 시간이 걸릴 수 있습니다. 공개 샘플의 한 실행은 약 109초였으며, 일정한 응답 시간을 보장하는 값은 아닙니다.

비기밀 레이아웃만 업로드해 주세요. 이 단순화한 모델은 학습과 상대 비교용이며 제조 signoff를 위한 결과가 아닙니다.

[계산 방법]({{ '/ko/method/' | relative_url }}) · [기술 검증·다운로드]({{ '/ko/notes/v0.10-validation/' | relative_url }}) · [이전 Demo]({{ '/ko/demo-legacy/' | relative_url }})
