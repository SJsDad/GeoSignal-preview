---
layout: default
title: GeoSignal Preview
description: GeoSignal relative exposure study and validation
permalink: /ko/
lang: ko
---

<p class="language-switch"><a href="{{ '/' | relative_url }}" lang="en">View in English</a></p>

# GeoSignal Preview

> 이 v0.10 검증 snapshot은 모델과 preset을 설명합니다. 기재한 benchmark는 로컬 측정이며 실제 서버 성능은 다를 수 있습니다.

Layout geometry에서 후보를 고른 뒤 광학 contour와 국소 형상을 검토하는 스터디 도구입니다.

설계 anchor의 nominal CD를 맞춘 상대 노광 모델입니다. 실제 wafer CD fitting이나 scanner/resist 공정 calibration이 아닙니다. Polygon 투과율은 1이며 contour는 고강도 영역입니다. PTD/NTD 현상 또는 최종 배선 전사는 모델링하지 않습니다.

KrF 248 nm · NA 0.68 · sigma 0.60 · ROI 2.56 µm · pixel 10 nm · ambit 0.32 µm · internal DBU 0.1 nm

![Fixed reference and relative-dose contours]({{ '/assets/demo/v0.10/speed/reference_anchor.png' | relative_url }})

Speed는 dense7과 선택적인 nominal-dose Region 검사를, Internal은 dense11과 세 dose Region 검사를 사용합니다. Speed의 상세 Region 검사는 기본적으로 꺼져 있습니다. 두 preset 모두 세 dose contour를 제공합니다. 서로 다른 수치 근사이므로 각자 nominal 보정하며 결과를 동등하게 취급하지 않습니다. 후보는 measured width/space를 우선하고 area는 secondary heuristic으로 사용합니다.

[Demo]({{ '/ko/demo/' | relative_url }}) · [Method]({{ '/ko/method/' | relative_url }}) · [Technical Notes]({{ '/ko/notes/' | relative_url }}) · [v0.10]({{ '/ko/release-notes/v0.10/' | relative_url }})

{% include live-demo-cta.html %}
