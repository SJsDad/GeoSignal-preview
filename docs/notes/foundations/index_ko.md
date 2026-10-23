---
layout: technical
category: foundations
title: Physics & Math Foundations
permalink: /ko/notes/foundations/
lang: ko
---

# Physics & Math Foundations

* 목차
{:toc}

이 영역은 원문 리뷰의 공통 언어를 정리합니다. 기존 Abbe/Fourier 문서의 경로를 유지하고, 새 설명과 학습 경로를 연결했습니다. 설명의 적용 범위는 scalar, thin-mask, shift-invariant 근사이며 벡터 광학이나 3D mask 전자기 해석은 별도 모델이 필요합니다.

## 권장 학습 순서

1. [Fourier Optics · FFT]({{ '/ko/notes/fourier-optics/' | relative_url }}) — 공간 주파수·convolution·sampling을 확인합니다.
2. [Abbe Imaging · Pupil · Partial Coherence]({{ '/ko/notes/abbe-imaging/' | relative_url }}) — source마다 전계를 계산한 뒤 intensity를 더하는 이유를 이해합니다.
3. [회절 차수와 디포커스: 경사 조명의 이미징 원리]({{ '/ko/notes/diffraction-defocus/' | relative_url }}) — 주기적 마스크의 고차항과 3-beam/2-beam의 초점 민감도를 비교합니다.
4. [Hopkins · TCC · SOCS]({{ '/ko/notes/foundations/hopkins-tcc-socs/' | relative_url }}) — mask와 광학계를 분리해 kernel을 재사용하는 과정을 유도합니다.
5. [Inverse Problem · Gradient · Metrics]({{ '/ko/notes/foundations/inverse-and-metrics/' | relative_url }}) — differentiable imaging이 mask update로 연결되는 과정과 지표 단위를 확인합니다.
6. [Research Paper Reviews]({{ '/ko/notes/research/' | relative_url }}) — 물리 지식을 네트워크의 어느 위치에 넣는지 비교합니다.

## 기존 노트 설명

| 주제 | 내용 |
| --- | --- |
| [Abbe Imaging]({{ '/ko/notes/abbe-imaging/' | relative_url }}) | Preview workflow에서 사용하는 simplified Abbe-style imaging 개념 설명 |
| [Fourier Optics]({{ '/ko/notes/fourier-optics/' | relative_url }}) | Aerial image 형성과 관련된 Fourier optics 배경 설명 |
| [회절 차수와 디포커스]({{ '/ko/notes/diffraction-defocus/' | relative_url }}) | 고차 회절항, pupil과 경사 조명의 through-focus 비교 |

## 기존 문서와 구현 범위

[v0.10 검토 요약]({{ '/ko/notes/v0.10-validation/' | relative_url }})에서 해당 단계의 검토 범위를 확인할 수 있습니다. [Method]({{ '/ko/method/' | relative_url }})와 [Demo]({{ '/ko/demo/' | relative_url }})는 기존 workflow와 결과를 보여줍니다. 새 논문 리뷰는 현재 GeoSignal에 학습 모델이 도입됐다는 뜻이 아닙니다.

공개 기능과 연구 맥락은 [GeoSignal 적용 범위]({{ '/ko/notes/research/geosignal-scope/' | relative_url }})에 정리했습니다.
