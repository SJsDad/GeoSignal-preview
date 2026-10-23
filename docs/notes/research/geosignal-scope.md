---
layout: technical
category: research
title: GeoSignal 적용 범위와 연구 연결점
permalink: /ko/notes/research/geosignal-scope/
lang: ko
---

# GeoSignal 적용 범위와 연구 연결점

* 목차
{:toc}

## 코드로 확인한 현재 상태

GeoSignal-preview는 Jekyll 문서·공개 결과와 브라우저 기반 학습 시뮬레이터를 제공합니다. 논문을 설명하는 이번 변경은 core simulator에 ML 모델을 추가하지 않습니다. 작업 환경의 GeoSignal-lab source도 읽어 기능의 존재 여부를 확인했습니다. 확인한 코드 파일과 함수는 아래와 같습니다. core source가 공개 Preview 저장소에 포함돼 있다는 뜻은 아닙니다.

| 확인 위치 | 확인 내용 | 해석 범위 |
| --- | --- | --- |
| `src/litho/abbe.py` · `prepare_abbe_context`, `compute_abbe_image_from_context` | FFT 재사용, source별 coherent field, intensity 누적 | scalar binary-mask aerial 계산 |
| `src/litho/pupil.py`, `config.py` | shifted circular pupil, wavelength/NA/source 설정, focus phase | 이상화된 광학 설정 |
| `src/litho/tcc.py`, `socs.py`, `imaging_backend.py` | source factor, exact full-rank SOCS, backend dispatch, mode cache | Abbe와 교차검증 경로; 상용 공정 정합성의 증거는 아님 |
| `src/litho/truncation.py` | 별도 SOCS truncation 평가 | approximate truncation이 기본 서비스라는 뜻은 아님 |
| `src/service.py` · `_calibrate_dose_to_size`, `_run_focus_dose_sweep` | 기준 pattern, relative-dose threshold, focus/dose sweep | fixed reference·transect 기반 idealized 분석 |
| Preview [v0.10 validation]({{ '/ko/notes/v0.10-validation/' | relative_url }}) | 공개 검증 snapshot과 조건 | live deployment 갱신·wafer 검증을 뜻하지 않음 |

## 실무 관심 항목별 연결

| 목적 | 현재 GeoSignal에서 확인한 것 | 리뷰에서 얻을 아이디어 | 추가 검증 |
| --- | --- | --- | --- |
| Aerial Image Prediction | scalar Abbe, exact SOCS 경로 | Nitho kernel 식별, DOINN dual branch, LMLitho source 조건화 | reference intensity normalization·경계·gradient |
| Resist / Contour Prediction | intensity threshold contour | LMLitho resist surrogate | 화학 resist·wafer 데이터와 별도 calibration 필요 |
| OPC Edge Movement | 자동 보정 solver 미구현 | ResGNN residual edge update | segmentation, graph 구성, MBOPC label, mask rules |
| EPE / CD Prediction | fixed-transect CD와 contour review; 논문과 동일한 EPE benchmark 미구현 | edge 중심 error gate | gauge·normal·missing contour 정의 |
| SRAF Optimization | 학습/자동 SRAF optimizer 미구현 | OptiCo, Hi-ILT의 inverse 생성·정제 | SRAF 비인쇄 조건과 mask manufacturing rules |
| DoF / Bossung Curve | idealized focus/dose sweep·CD plotting 경로 | 조건별 surrogate 오차 평가 | 실제 scanner·resist focus response와 spec |
| Focus / Dose Variation | 상대 dose 및 focus simulation | process-condition 입력 또는 condition별 kernel | 조건 밖 extrapolation 검증 |
| Process Window | idealized spec 기반 평가 | coarse surrogate 이후 reference 재평가 | calibrated wafer process window와 구분 |
| Patterning Margin Analysis | geometry candidate·optical contour 검토 | uncertainty를 포함한 후보 우선순위 | 상용 margin certification 미검증 |
| Optical Simulation Acceleration | FFT/context/mode cache 재사용 | 학습 kernel·source encoder cache | end-to-end runtime, setup·transfer·memory 포함 |

## 당장 적용 가능한 아이디어

원문 수치를 이식하는 대신 기존 결과 export와 학습 데이터 schema를 맞추는 것이 먼저입니다. ROI width·pixel size·halo·mask polarity·NA·wavelength·source sampling·focus·dose·normalization을 각 sample에 기록할 수 있습니다. 동일 scalar 조건에서 Abbe/SOCS reference를 분리해 저장하고, train/test를 layout 단위로 분리합니다. 이 항목들은 workflow 설계 제안이며 이번 문서 작업에서 core에 새로 구현한 기능은 아닙니다.

## 추가 연구가 필요한 아이디어

**Future Application / Hypothesis.** Nitho 방식으로 고정 optical condition의 kernel을 식별하고 aerial/CD 오차를 gate로 삼는 연구가 현재 계산 경로와 가장 가까운 출발점입니다. learned forward model을 inverse optimization에 쓰기 전에는 mask perturbation에 대한 directional derivative를 reference와 비교해야 합니다. ResGNN/TokMan은 raster-only flow보다 polygon·edge topology를 보존하는 데이터 구조가 추가로 필요합니다.

## 장기 연구 방향

**Future Application / Hypothesis.** calibrated resist·mask 3D effect·vector imaging·process-conditioned neural operator·uncertainty model을 검토할 수 있습니다. TEMPO의 resist 내 height와 GeoSignal의 focus 좌표는 물리적 역할이 다르므로 이름이 비슷하다는 이유로 같은 input으로 취급하면 안 됩니다. stochastic EUV defect나 제조 수율 예측은 이 8편을 읽었다는 이유로 지원 또는 검증됐다고 주장할 수 없습니다.

## 연결 문서

* [Research Overview]({{ '/ko/notes/research/' | relative_url }})
* [Method]({{ '/ko/method/' | relative_url }})
* [Abbe Imaging]({{ '/ko/notes/abbe-imaging/' | relative_url }})
