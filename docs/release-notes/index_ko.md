---
layout: default
title: 릴리즈 노트
description: GeoSignal Preview 버전별 변경 및 구현 기록
permalink: /ko/release-notes/
lang: ko
---

<p class="language-switch"><a href="{{ '/release-notes/' | relative_url }}" lang="en">View in English</a></p>

# 릴리즈 노트

이 섹션은 **GeoSignal Preview**의 주요 구현 변경, 평가 기록, 기술적 판단을 버전별로 정리합니다.

v0.1부터 v0.4까지는 저장소 커밋 이력을 바탕으로 복원한 과거 마일스톤입니다. 초기 버전마다 상세 benchmark artifact가 보존된 것은 아니므로, 소스 이력으로 확인할 수 있는 변경만 기록했습니다. v0.5 이후에는 개발 과정에서 작성한 보다 상세한 평가 기록을 포함합니다.

일반 방문자는 먼저 [홈]({{ '/ko/' | relative_url }}), [데모]({{ '/ko/demo/' | relative_url }}), [방법론]({{ '/ko/method/' | relative_url }})을 읽으면 됩니다. 이 노트는 preview가 버전별로 어떻게 발전했는지 확인하려는 독자를 위한 기술 기록입니다.

## 버전

| 버전 | 주요 내용 |
| --- | --- |
| [v0.1]({{ '/ko/release-notes/v0.1/' | relative_url }}) | 초기 CLI와 SVRF-like geometry rule 실험 |
| [v0.2]({{ '/ko/release-notes/v0.2/' | relative_url }}) | Flask web prototype과 layout preview |
| [v0.3]({{ '/ko/release-notes/v0.3/' | relative_url }}) | 모듈형 geometry engine, width/space 분석, density |
| [v0.4]({{ '/ko/release-notes/v0.4/' | relative_url }}) | Raster, Abbe imaging, contour, hotspot 평가 |
| [v0.5]({{ '/ko/release-notes/v0.5/' | relative_url }}) | 기존 gdstk 경로와 선택 가능한 pya backend 비교 |
| [v0.6]({{ '/ko/release-notes/v0.6/' | relative_url }}) | pya-native geometry 경로, candidate overview, printed metric 개선 |
| [v0.7]({{ '/ko/release-notes/v0.7/' | relative_url }}) | 통합 review GDS, candidate별 contour, bounded-memory imaging |
| [v0.8]({{ '/ko/release-notes/v0.8/' | relative_url }}) | Focus/dose process-window 분석, calibration, PW artifact |
| [v0.8.1]({{ '/ko/release-notes/v0.8.1/' | relative_url }}) | Backend-neutral imaging contract와 focus/dose 성능 개선 |
| [v0.9]({{ '/ko/release-notes/v0.9/' | relative_url }}) | 정확한 Hopkins/TCC/SOCS 교차검증과 bounded optical-mode cache |

v0.8.0과 v0.8.1은 application 저장소에 tag가 생성된 릴리스입니다. v0.9는
application의 v0.9 branch에서 구현과 검증을 완료한 engineering milestone을
기록합니다. 이 Pages update를 준비한 시점에는 v0.9 release tag가 아직
생성되지 않았습니다.

## 읽는 순서

공개 페이지는 핵심 내용을 짧게 전달합니다.

```text
Home / Demo / Method
    -> preview가 무엇인지
    -> 이미지가 무엇을 보여주는지
    -> 결과를 어떻게 해석하는지

Release Notes
    -> 구현 판단이 왜 바뀌었는지
    -> 무엇을 비교했는지
    -> 어떤 한계가 남아 있는지
```

아래 노트는 기술 기록이며 live demo를 이해하기 위한 필수 읽을거리는 아닙니다.

## 관련 페이지

* [홈]({{ '/ko/' | relative_url }})
* [데모]({{ '/ko/demo/' | relative_url }})
* [방법론]({{ '/ko/method/' | relative_url }})
* [기술 노트]({{ '/ko/notes/' | relative_url }})
