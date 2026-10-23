---
layout: technical
title: Technical Notes
permalink: /ko/notes/
lang: ko
---

<p class="language-switch"><a href="{{ '/notes/' | relative_url }}">View in English</a></p>

# Technical Notes

이 섹션은 GeoSignal Preview의 Demo와 Method 페이지를 이해하기 위한 보조 설명을 정리합니다.

광학·수학적 배경을 먼저 읽고, 논문의 학습 구조와 실무 적용 가능성을 검토합니다.

## Physics & Math Foundations

* [Foundations Overview]({{ '/ko/notes/foundations/' | relative_url }})
* [Abbe Imaging]({{ '/ko/notes/abbe-imaging/' | relative_url }}) — Partial coherence · Source sampling · Pupil
* [Fourier Optics]({{ '/ko/notes/fourier-optics/' | relative_url }}) — FFT · Convolution · Sampling
* [회절 차수와 디포커스: 경사 조명의 이미징 원리]({{ '/ko/notes/diffraction-defocus/' | relative_url }}) — 고차항 · 3-beam/2-beam · 데모 안내
* [6f 광선·파동 시뮬레이터 실행]({{ '/ko/simulator/' | relative_url }}) — 브라우저에서 바로 조작
* [Hopkins / TCC / SOCS]({{ '/ko/notes/foundations/hopkins-tcc-socs/' | relative_url }}) — 한국어
* [Inverse Problem / Metrics]({{ '/ko/notes/foundations/inverse-and-metrics/' | relative_url }}) — 한국어

## Research Paper Reviews

[Overview · 비교 및 탐색]({{ '/ko/notes/research/' | relative_url }}) — 8편의 연구 분야, 입력·출력, 물리 지식의 주입 위치를 비교합니다. 접근 제한은 각 리뷰에 표시합니다.

{% include research-catalog.html %}

## 관련 페이지

* [Home]({{ '/ko/' | relative_url }})
* [Demo]({{ '/ko/demo/' | relative_url }})
* [Method]({{ '/ko/method/' | relative_url }})
* [v0.10 validation]({{ '/ko/notes/v0.10-validation/' | relative_url }}) — 기존 검증 기록
* [v0.11 sampling benchmark]({{ '/ko/release-notes/v0.11/' | relative_url }}) — Source·Raster·AI 보간 및 자원 비교
