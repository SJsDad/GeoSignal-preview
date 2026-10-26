---
layout: default
title: v0.12 이전 데모 비교
description: 내부 스크롤이 있는 이전 앱 화면과 현재 데모 비교
permalink: /ko/demo-legacy/
lang: ko
---

# v0.12 이전 데모 비교

v0.12 이전의 **왼쪽 입력 패널 + 오른쪽 결과 패널 + 850px 높이 화면 내부 스크롤** 구성을 다시 볼 수 있습니다. 비교 후 선택할 수 있도록 현재 데모는 유지했습니다.

[현재 데모]({{ '/ko/demo/' | relative_url }}) · [이전 화면을 전체 너비로 열기 ↗]({{ '/ko/demo-legacy/screen/' | relative_url }})

## 1. 이전 앱 화면

<iframe id="legacy-demo-frame" src="{{ '/ko/demo-legacy/screen/' | relative_url }}" title="내부 스크롤이 있는 이전 GeoSignal 앱 화면" width="100%" height="850" loading="lazy" style="border:1px solid #dce3ec;border-radius:10px" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>

**화면 안에서 스크롤**해 저장된 결과를 살펴보세요. Width / Space와 표시 개수 4·6·8을 선택하고, 카드를 누르면 아래의 큰 이미지로 이동합니다. 유형별 저장 예시는 6개이며, 8개를 선택해도 없는 결과를 만들지 않습니다.

## 2. 비교할 부분

| 이전 구성 | 확인해 볼 점 |
| --- | --- |
| 앱 전체 화면 | 입력 항목과 결과 패널을 함께 볼 수 있습니다. |
| 내부 스크롤 | 페이지를 짧게 유지하면서 긴 결과를 탐색합니다. |
| 후보 중심 흐름 | 전체 위치를 보고, 후보를 고르고, 큰 이미지로 이동합니다. |
| 선택적인 초점·도즈 비교 | 체크박스 또는 상세 보기를 펼칩니다. 각 유형의 1번 후보에는 9개 저장 조건과 Bossung 곡선이 있습니다. |

이전 화면 구성을 검토된 저장 이미지와 표시값으로 재현했습니다. 내부 보정정보·원자료 다운로드·계산 설정은 제외해 일부 입력란은 예시 표시로 남겼습니다. 업로드와 새 분석은 원래의 저장 데이터 미리보기처럼 비활성화되어 있습니다. 그림과 측정값은 모델 결과이며 웨이퍼 실측 검증이 아닙니다.

{% include live-demo-cta.html %}
