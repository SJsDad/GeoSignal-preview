# GeoSignal Preview

> 한국어 버전은 하단에 있습니다.  
> Korean version is provided below.

---

# English

## 1. What is GeoSignal Preview?

**GeoSignal Preview** is a documentation-focused public preview repository for organizing a **lithography-aware visualization workflow** that connects layout geometry with a simplified optical model using open-source Python-based tools.

This repository does not expose the core implementation code.  
Instead, it focuses on the following materials:

- problem definition
- workflow overview
- demo images
- method explanation
- technical notes
- early feedback collection

The basic workflow is:

```text
layout geometry
    → rasterized mask
    → simplified aerial image
    → threshold contour
    → hotspot candidate visualization
```

The goal is not to provide a high-precision lithography simulator calibrated to real process conditions.

Instead, this preview focuses on visualizing the relationship between layout geometry and optical response, and on lightly exploring the gap between intended layout patterns and expected optical behavior.

---

## 2. Motivation

Geometry-based analysis such as minimum width, minimum space, and density checks is very useful for understanding layout patterns.

However, geometry checks alone do not always make it easy to intuitively understand how a pattern may appear from an optical imaging perspective, or which regions may be relatively lithography-sensitive.

GeoSignal Preview explores the following approach to reduce this gap:

- convert layout polygons into a rasterized mask
- generate an aerial image using a simplified optical model
- visualize printed-shape-like response using threshold contours
- compare geometry-based candidates with optical response
- organize candidate risk regions at the ROI level

The main purpose is to experiment with a workflow that helps users understand layout risk more intuitively using public examples and open-source-based tools, without assuming access to expensive commercial simulation environments.

This preview is especially intended for:

- researchers or students studying computational lithography
- users who want to quickly understand the relationship between layout geometry and optical response
- users who want to run lightweight experiments with public GDS or synthetic patterns
- users who want to review early-stage lithography-aware visualization ideas

---

## 3. Current Scope

This public repository is focused on documentation and preview materials.

### Included

- problem definition
- workflow overview
- demo result pages
- simplified method explanation
- technical notes
- public or synthetic examples
- preview images
- feedback points for future feature expansion

### Not Included

- private core implementation code
- internal experiment notes
- non-public layout data

In other words, this repository is not a full software package release.  
It is closer to a preview space for sharing ideas, results, and early feedback.

---

## 4. Preview Pages

The GitHub Pages site will be organized around the following pages.

| Page | Description |
|---|---|
| `docs/index.md` | Landing page and overall project story |
| `docs/demo.md` | Demo images and result interpretation |
| `docs/method.md` | Simplified method and workflow explanation |
| `docs/notes/` | Optional technical notes |

Rather than explaining the full repository structure in detail, the goal is to help visitors quickly understand the problem definition, demo results, and methodology through GitHub Pages.

---

## 5. Demo Concept

The initial demo will focus on public GDS or synthetic layout examples.

Planned visual materials include:

- workflow overview
- mask image
- aerial image
- mask + aerial image + contour overlay
- threshold comparison: 0.2 / 0.3 / 0.4
- hotspot candidate ROI visualization

The purpose of the demo is not to claim production-level accuracy.  
Instead, it is to show intuitively how layout patterns may appear differently after passing through a simplified optical model.

Through this demo, users can review questions such as:

- How does a pattern that looks simple in geometry appear in optical response?
- Do edge rounding, line-end pullback, necking, or bridge-like responses appear in threshold contours?
- How similar or different are geometry-based candidates and optical-response-based candidates?
- What type of visualization is most helpful for understanding layout risk?

---

## 6. Method Overview

GeoSignal Preview is based on a simplified lithography-aware visualization flow.

1. Extract a region of interest from layout geometry.
2. Rasterize polygons into a binary mask image.
3. Generate an aerial image using a simplified Abbe-style imaging model.
4. Extract threshold contours from the aerial image.
5. Compare contour behavior with the original mask geometry.
6. Visualize candidate risk regions.

The current prototype is based on a simplified Abbe-style imaging model with configurable optical parameters such as wavelength, NA, source shape, source sampling, and threshold level.

The illumination condition is calculated by sampling multiple source points.  
For the current preview, the condition is selected by considering the balance between intuitive visual output and computational cost.

The initial examples assume conditions closer to a general optical lithography study setting rather than a model calibrated to a specific production process.

Therefore, this workflow is more suitable for the following purposes than for quantitative CD prediction:

- checking optical response trends
- relative comparison between patterns
- layout risk visualization
- computational lithography study
- early-stage technical review for research and learning

If more complex partial coherence calculation or computational efficiency becomes necessary in the future, Hopkins / TCC-related approaches may be reviewed separately.

---

## 7. Current Assumptions and Limitations

This preview is based on a simplified optical model and public or synthetic layout examples.

Current assumptions and limitations are:

- wafer-data-based calibration is not included
- resist / etch models are not included in the current preview scope
- threshold contours are used for qualitative visualization and relative comparison
- optical parameters are simplified for public demo and learning purposes
- results should be interpreted as early-stage qualitative indicators, not production specifications
- current evaluation focuses on small ROI or small public GDS examples

Therefore, GeoSignal Preview results should be interpreted as **visual analysis aids** for exploring the relationship between layout geometry and optical response, rather than as definitive answers.

---

## 8. Intended Use

This repository is suitable for:

- computational lithography study
- layout risk visualization experiments
- public or synthetic pattern-based demos
- reviewing the connection between geometry checks and optical models
- technical portfolio documentation
- early feedback collection
- discussion on future feature expansion

This preview is not a finished product.  
It is a public technical preview for studying computational lithography and reviewing layout risk visualization ideas.

Based on user feedback, the following directions may be considered:

- adding more diverse layout examples
- improving hotspot candidate visualization
- adding contour-based metrics
- improving comparison between geometry features and optical response
- organizing Abbe model parameters
- reviewing Hopkins / TCC-related approaches if needed
- collecting feedback through a feedback form

---

## 9. Feedback

Feedback is welcome.

The purpose of this preview is to collect early reactions and improve the direction of the project.

The following types of feedback are especially helpful:

- which demo images are easiest to understand
- what layout examples would be useful to add
- whether mask / aerial image / contour overlay visualization is intuitive enough
- whether threshold comparison helps understand layout risk
- what technical notes would be useful to add
- what future analysis features would be valuable

A Google Form may be added later for anonymous feedback.

GitHub Issues may be used selectively as a secondary channel for documentation fixes, example suggestions, or technical questions.

---

## 10. Current Status

| Area | Status |
|---|---|
| Public preview repository | Preparing for public operation |
| Core implementation | Private |
| Imaging model | Simplified Abbe-style model |
| Layout examples | Public or synthetic examples |
| Current evaluation scale | Small ROI / small public GDS examples |
| Demo materials | In preparation |
| GitHub Pages | Planned |
| Feedback channel | Mainly considering Google Form |
| Future direction | More examples, improved scoring, optional Hopkins / TCC review |

At the current stage, the priority is not to expose every complex feature, but to organize a minimal set of visible results and collect external feedback.

---

## 11. License

No open-source license has been selected yet.

This repository is currently shared as a public documentation preview for feedback and discussion.

If the public scope of the code or documentation expands later, an appropriate license will be reviewed separately.

---

# 한국어

## 1. GeoSignal Preview란?

**GeoSignal Preview**는 오픈소스 Python 기반 도구를 활용해 **layout geometry와 simplified optical model을 연결하는 lithography-aware visualization workflow**를 공개적으로 정리하기 위한 문서 중심 preview repository입니다.

이 저장소는 핵심 구현 코드를 공개하는 것이 아니라, 다음 내용을 중심으로 구성됩니다.

- 문제 정의
- workflow 개요
- demo image
- 방법론 설명
- technical note
- 초기 feedback 수집

기본 workflow는 다음과 같습니다.

```text
layout geometry
    → rasterized mask
    → simplified aerial image
    → threshold contour
    → hotspot candidate visualization
```

목표는 실제 공정 조건에 맞게 보정된 고정밀 lithography simulator를 제공하는 것이 아닙니다.

대신 layout geometry와 optical response 사이의 관계를 직관적으로 시각화하고, 패턴 의도와 예상 optical behavior 사이의 차이를 가볍게 탐색할 수 있는 preview를 제공하는 데 초점을 둡니다.

---

## 2. 배경

minimum width, minimum space, density check와 같은 geometry 기반 분석은 layout pattern을 이해하는 데 매우 유용합니다.

다만 geometry check만으로는 특정 pattern이 optical imaging 관점에서 어떻게 보일지, 또는 어떤 영역이 상대적으로 lithography-sensitive할 수 있는지를 직관적으로 확인하기 어려운 경우가 있습니다.

GeoSignal Preview는 이 간극을 줄이기 위해 다음과 같은 접근을 탐색합니다.

- layout polygon을 rasterized mask로 변환
- simplified optical model을 이용해 aerial image 생성
- threshold contour를 통해 printed-shape-like response 시각화
- geometry 기준 후보와 optical response를 함께 비교
- candidate risk region을 ROI 단위로 정리

핵심 목적은 **고가의 상용 simulation 환경을 전제로 하지 않고도**, 공개 가능한 예제와 오픈소스 기반 도구를 활용해 layout risk를 보다 직관적으로 이해할 수 있는 workflow를 실험하는 것입니다.

이 preview는 특히 다음과 같은 상황을 염두에 둡니다.

- computational lithography를 학습하는 연구자 또는 학생
- layout geometry와 optical response의 관계를 빠르게 이해하고 싶은 사용자
- public GDS 또는 synthetic pattern으로 가벼운 실험을 해보고 싶은 사용자
- 초기 단계의 lithography-aware visualization 아이디어를 검토하고 싶은 사용자

---

## 3. 현재 공개 범위

이 public repository는 문서와 preview 자료 중심으로 구성됩니다.

### 포함되는 내용

- 문제 정의
- workflow 개요
- demo result page
- simplified method 설명
- technical note
- public 또는 synthetic example
- preview image
- 향후 기능 확장을 위한 feedback point

### 포함하지 않는 내용

- 비공개 핵심 구현 코드
- 내부 실험 노트
- 공개되지 않은 layout data

즉, 이 저장소는 전체 software package 공개가 아니라, **아이디어와 결과를 공유하고 피드백을 받기 위한 preview space**에 가깝습니다.

---

## 4. Preview 페이지 구성

GitHub Pages는 다음 페이지 중심으로 구성할 예정입니다.

| Page | 설명 |
|---|---|
| `docs/index.md` | 전체 landing page 및 프로젝트 스토리 |
| `docs/demo.md` | 데모 이미지와 결과 해석 |
| `docs/method.md` | 단순화된 방법론과 workflow 설명 |
| `docs/notes/` | 선택적 technical note |

저장소 전체 구조를 자세히 설명하기보다는, 방문자가 GitHub Pages를 통해 문제 정의, 데모, 방법론을 빠르게 이해할 수 있도록 구성하는 것을 목표로 합니다.

---

## 5. 데모 컨셉

초기 데모는 public GDS 또는 synthetic layout example 중심으로 구성합니다.

예정된 시각 자료는 다음과 같습니다.

- workflow overview
- mask image
- aerial image
- mask + aerial image + contour overlay
- threshold 0.2 / 0.3 / 0.4 비교
- hotspot candidate ROI visualization

데모의 핵심은 production-level accuracy를 주장하는 것이 아니라, **layout pattern이 simplified optical model을 거쳤을 때 어떻게 다르게 보일 수 있는지**를 직관적으로 보여주는 것입니다.

이를 통해 사용자는 다음 질문을 검토할 수 있습니다.

- geometry 기준으로는 단순해 보이는 pattern이 optical response에서는 어떻게 보이는가?
- threshold contour 기준으로 edge rounding, line-end pullback, necking, bridge-like response가 나타나는가?
- geometry 기반 candidate와 optical response 기반 candidate는 얼마나 유사하거나 다른가?
- 어떤 형태의 visualization이 layout risk를 이해하는 데 가장 도움이 되는가?

---

## 6. 방법론 개요

GeoSignal Preview는 단순화된 lithography-aware visualization flow를 기반으로 합니다.

1. layout geometry에서 region of interest를 추출합니다.
2. polygon을 binary mask image로 rasterize합니다.
3. 단순화된 Abbe-style imaging model을 이용해 aerial image를 생성합니다.
4. aerial image에서 threshold contour를 추출합니다.
5. contour behavior를 원본 mask geometry와 비교합니다.
6. candidate risk region을 시각화합니다.

현재 prototype은 wavelength, NA, source shape, source sampling, threshold level 등의 optical parameter를 조정할 수 있는 simplified Abbe-style imaging model을 기반으로 합니다.

조명계는 여러 개의 source point를 샘플링해 계산하며, 현재 preview에서는 결과의 직관성과 계산량 사이의 균형을 고려한 조건을 사용합니다.

초기 예제는 특정 양산 공정에 보정된 model이라기보다, 일반적인 optical lithography study에 가까운 조건을 가정합니다.

따라서 이 workflow는 정량적 CD 예측보다는 다음 목적에 더 적합합니다.

- optical response 경향 확인
- pattern별 상대 비교
- layout risk visualization
- computational lithography 학습
- 초기 연구·학습 단계의 기술 검토

향후 더 복잡한 partial coherence 계산이나 계산 효율화가 필요할 경우 Hopkins / TCC 계열 접근도 별도로 검토할 수 있습니다.

---

## 7. 현재 가정과 한계

이 preview는 단순화된 optical model과 public 또는 synthetic layout example을 기반으로 합니다.

현재 가정과 한계는 다음과 같습니다.

- wafer data 기반 calibration은 포함하지 않습니다.
- resist / etch model은 현재 preview 범위에 포함하지 않습니다.
- threshold contour는 정성적 시각화와 상대 비교 목적으로 사용합니다.
- optical parameter는 공개 데모와 학습 목적에 맞게 단순화합니다.
- 결과는 production specification이 아니라 초기 단계의 qualitative indicator로 해석하는 것이 적절합니다.
- 현재 평가는 small ROI 또는 small public GDS example 중심으로 진행합니다.

따라서 GeoSignal Preview의 결과는 “정답”이라기보다, layout geometry와 optical response 사이의 관계를 탐색하기 위한 **시각적 분석 보조 자료**로 보는 것이 적절합니다.

---

## 8. 의도한 사용 목적

이 repository는 다음 목적에 적합합니다.

- computational lithography 학습
- layout risk visualization 실험
- public 또는 synthetic pattern 기반 demo
- geometry check와 optical model의 연결 구조 검토
- technical portfolio 정리
- 초기 feedback 수집
- 향후 기능 확장 방향 논의

이 preview는 완성된 제품이라기보다, computational lithography 학습과 layout risk visualization 아이디어 검토를 위한 공개 기술 preview입니다.

사용자의 피드백을 바탕으로 다음과 같은 방향을 검토할 수 있습니다.

- 더 다양한 layout example 추가
- hotspot candidate visualization 개선
- contour 기반 metric 추가
- geometry feature와 optical response의 비교 방식 개선
- Abbe model parameter 정리
- 필요 시 Hopkins / TCC 계열 접근 검토
- feedback form 기반 의견 수집

---

## 9. 피드백

피드백을 환영합니다.

이 preview의 목적은 초기 반응을 수집하고 프로젝트 방향을 개선하는 것입니다.

특히 다음과 같은 의견이 도움이 됩니다.

- 어떤 demo image가 가장 이해하기 쉬운지
- 어떤 layout example이 추가되면 좋을지
- mask / aerial image / contour overlay 표현이 충분히 직관적인지
- threshold 비교가 layout risk 이해에 도움이 되는지
- 어떤 technical note가 추가되면 좋을지
- 향후 기능으로 어떤 분석이 유용할지

추후 익명 의견 수집을 위한 Google Form을 추가할 수 있습니다.

GitHub Issues는 필요 시 문서 오류, 예제 제안, 기술적 질문을 위한 보조 채널로 제한적으로 운영할 수 있습니다.

---

## 10. 현재 상태

| 항목 | 상태 |
|---|---|
| Public preview repository | 운영 준비 중 |
| Core implementation | 비공개 |
| Imaging model | simplified Abbe-style model |
| Layout example | public 또는 synthetic example 중심 |
| 현재 평가 규모 | small ROI / small public GDS 중심 |
| Demo material | 준비 중 |
| GitHub Pages | 구성 예정 |
| Feedback channel | Google Form 중심 검토 |
| 향후 방향 | 예제 확장, scoring 개선, 필요 시 Hopkins / TCC 검토 |

현재 단계에서는 복잡한 기능을 모두 공개하기보다, **보여줄 수 있는 최소 결과를 정리하고 외부 반응을 확인하는 것**을 우선합니다.

---

## 11. 라이선스

아직 별도의 오픈소스 라이선스는 선택하지 않았습니다.

현재 이 repository는 피드백과 논의를 위한 public documentation preview로 공유됩니다.

추후 코드 또는 문서의 공개 범위가 확장될 경우, 적절한 license를 별도로 검토할 예정입니다.

