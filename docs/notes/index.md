---
layout: technical
title: Technical Notes
permalink: /notes/
---

<p class="language-switch"><a href="{{ '/ko/notes/' | relative_url }}">한국어로 보기</a></p>

# Technical Notes

This section provides supporting notes for understanding the demo and method pages of GeoSignal Preview.

These notes provide background concepts related to the simplified optical-imaging and contour-visualization workflow used in GeoSignal Preview.

Study the optical and mathematical foundations, then examine research architectures and practical OPC implications. Research reviews are written in Korean.

## Physics & Math Foundations

* [Foundations Overview]({{ '/notes/foundations/' | relative_url }})
* [Abbe Imaging]({{ '/notes/abbe-imaging/' | relative_url }}) — Partial coherence · Source sampling · Pupil
* [Fourier Optics]({{ '/notes/fourier-optics/' | relative_url }}) — FFT · Convolution · Sampling
* [Diffraction Orders and Defocus]({{ '/notes/diffraction-defocus/' | relative_url }}) — Higher orders · 3-beam/2-beam · Demo guide
* [Hopkins / TCC / SOCS]({{ '/ko/notes/foundations/hopkins-tcc-socs/' | relative_url }}) — 한국어
* [Inverse Problem / Metrics]({{ '/ko/notes/foundations/inverse-and-metrics/' | relative_url }}) — 한국어

## Research Paper Reviews

[Overview · 비교 및 탐색]({{ '/ko/notes/research/' | relative_url }}) — 8편의 연구 분야, 입력·출력, 물리 지식의 주입 위치를 비교합니다. 접근 제한은 각 리뷰에 표시합니다.

{% include research-catalog.html %}

## Related Pages

* [Home]({{ '/' | relative_url }})
* [Demo]({{ '/demo/' | relative_url }})
* [Method]({{ '/method/' | relative_url }})
* [v0.10 validation]({{ '/notes/v0.10-validation/' | relative_url }}) — 기존 검증 기록
* [v0.11 sampling benchmark]({{ '/release-notes/v0.11/' | relative_url }}) — Source·Raster·AI 보간 및 자원 비교
