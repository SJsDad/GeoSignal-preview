---
layout: technical
category: research
title: 원문 접근 · Figure Coverage · 재사용 조건
permalink: /ko/notes/research/sources/
lang: ko
---

# 원문 접근 · Figure Coverage · 재사용 조건

* 목차
{:toc}

## 근거를 읽는 규칙

**원문 확인**은 실제 PDF 또는 HTML 본문을 읽은 경우입니다. **색인 본문 일부 확인**은 공식 PDF가 검색 색인에서 제공한 구간으로 method·caption·table을 확인했지만 원본 전체와 시각 자료를 열람하지 못한 경우입니다. **초록/표 확인**은 publisher가 공개한 부분만 읽은 경우입니다. 검색 결과에 나타났다는 이유로 full paper를 확보했다고 표시하지 않습니다.

각 문서의 수식은 원문 근거가 있는 식, 표기만 정리한 식, 독자적 일반 이론 설명을 구분합니다. 확인하지 못한 layer dimension·NA·source condition·runtime unit·license는 추정해 넣지 않습니다. 데이터 수치의 재계산은 독자 계산으로 표시합니다.

## 논문별 접근 상태

| 논문 | 실제 확인한 자료 | 제한·남은 검증 |
| --- | --- | --- |
| [OptiCo]({{ '/ko/notes/research/optico/' | relative_url }}) | CVF 서지·공식 PDF 색인 일부, 식 (6)–(15), Tables 1–5·Figures 1–6 참조 | PDF 직접 요청 403; 전체 figure/subfigure·Appendix·license·공식 코드 미확인 |
| [Hi-ILT]({{ '/ko/notes/research/hi-ilt/' | relative_url }}) | ScienceDirect 공식 서지·초록·Highlights, 저자 발표목록 | publisher 본문 403/구매 안내; VAE 내부·experiment tables·Fig 총수·affiliation·supplement 미확인 |
| [LMLitho]({{ '/ko/notes/research/lmlitho/' | relative_url }}) | 저자 9-page PDF 전문·Tables I–IV·Algorithm 1·공식 data README | 별도 supplement·full calibrated optical configuration·모델 코드/weights 미확인 |
| [TokMan]({{ '/ko/notes/research/tokman/' | relative_url }}) | NeurIPS 서지·초록·공식 PDF 색인 일부, Sections 4–5·Table 1·Figures 1–6 | PDF 약 15.5 MB 크기 제한; OpenReview browser challenge; ZIP 미파싱; 전체 inventory·시각 자료·Appendix 미확인 |
| [ResGNN-OPC]({{ '/ko/notes/research/resgnn-opc/' | relative_url }}) | Optica 서지·소속·초록·Table 1·Data Availability·10 figures 총수 | subscription 필요; 전체 본문·7 equations·Fig 1–10 captions/images·process conditions 미확인 |
| [TEMPO]({{ '/ko/notes/research/tempo/' | relative_url }}) | 저자의 GitHub PDF 8페이지 전문·Figures 1–5·Tables 1–5 | ACM DOI page 403; 이전 홈페이지 PDF 경로는 404라서 실제 저자 repo 파일로 대체; supplement·model 공개 미확인 |
| [DOINN]({{ '/ko/notes/research/doinn/' | relative_url }}) | arXiv v1 PDF/HTML 전문·Figures 1–9·Tables 1–4·Appendix A.1/A.2 | 학회 camera-ready와 preprint 차이·전체 optical settings·원 저자 code/weights 미확인 |
| [Nitho]({{ '/ko/notes/research/nitho/' | relative_url }}) | arXiv v4 PDF/HTML 전문·Figures 1–6·Tables I–V·Algorithm 1 | camera-ready와 preprint 차이·별도 supplement·원 저자 code/weights 미확인 |

접근 제한은 링크 자체의 부재를 뜻하지 않습니다. 공식 출처 URL을 유지하고 실패 사유를 구분했습니다. 접근 권한이나 도구 크기 제한을 우회해 파일을 얻지는 않았습니다. 모든 외부 링크가 이 실행 환경에서 HTTP 200으로 검증됐다고 주장하지 않습니다.

## Figure Coverage 집계

| 논문 | 확인된 Main Figure 번호 | 본문/caption 기반 해설 | 원문 링크만 | 전체 inventory 확정 |
| --- | --- | ---: | ---: | --- |
| OptiCo | 1–6 | 6 · 색인 일부 | 0 | 미확정, 최소 목록 |
| Hi-ILT | 미확인 | 0 | 공식 article entry | 미확정 |
| LMLitho | 1–13 | 13 | 0 | Main Paper 확정 |
| TokMan | 1–6 | 6 · 색인 일부 | 0 | 미확정, 최소 목록 |
| ResGNN-OPC | 1–10 | 0 | 10 | publisher 총수 확인; caption 미확인 |
| TEMPO | 1–5 | 5 | 0 | Main Paper 확정 |
| DOINN | 1–9 | 9 | 0 | Main Paper 확정 |
| Nitho | 1–6 | 6 | 0 | Main Paper 확정 |

확인한 번호의 registry는 **55개**, 본문/caption 기반 설명은 **45개**입니다. 이 중 33개는 전문을 읽은 4편의 Figure, 12개는 공식 색인 일부입니다. 10개는 ResGNN의 제한된 원문 링크입니다. 미확보 논문·supplement의 Figure 수를 0으로 추정한 전체 coverage percentage를 만들지 않습니다.

사이트에 포함한 **원본 논문 Figure 파일은 0개**, **독자 제작 SVG 도식은 8개**입니다. 도식은 확대 보기·원본 SVG 열기를 지원하며, original paper coverage count와 분리합니다. 숫자를 포함한 실험표는 재작성한 data table로 제시합니다.

## Copyright와 재사용 판단

| 출처 | 확인한 조건 | 이 작업의 처리 |
| --- | --- | --- |
| CVF OptiCo | open-access availability 확인; 개별 figure reproduction license 미확인 | Open Access를 재배포 허가로 가정하지 않고 링크/독자 도식 |
| Elsevier Hi-ILT | publisher purchase/access 안내; figure license 미확인 | 원본 복제 없음 |
| LMLitho 저자 PDF | author-hosted copy; figure reproduction permission 미확인 | official repository MIT와 PDF 그림의 권리를 동일시하지 않음 |
| NeurIPS TokMan | official paper/supplement entries 확인; 개별 파일 license 검증 미완료 | paper access와 image reuse를 구분, 원본 복제 없음 |
| Optica ResGNN | all rights reserved·figure subscription 제한 | 원본 복제 없음 |
| ACM TEMPO 저자 PDF | 저자 copy 확보; 원본 재배포 permission 미확인 | 공개 파일에 접근할 수 있어도 그림 재배포는 보류 |
| arXiv DOINN | perpetual non-exclusive arXiv posting license | 제3자 재사용 허가로 해석하지 않음 |
| arXiv Nitho v4 | CC BY-NC-ND 4.0 | 비상업·무변경 조건의 사이트 적용을 확정하지 않아 링크로 제공 |
| 독자 제작 SVG | 이번 학습 해설을 위해 직접 작성한 새로운 도식 | 원문 Figure와 구분하는 caption·alt text |
| MathJax 3.2.2 | Apache 2.0, vendored package LICENSE 포함 | source·font·license를 함께 제공; paper figure와 별개 |

Caption 전문을 페이지 전체에 복제하는 대신 요지와 원문 위치를 제공했습니다. 원본/재구성/새 설명도/실험 데이터의 출처를 구분합니다. 추가 원본 이미지를 넣으려면 해당 논문의 실제 reuse terms와 third-party content notice를 먼저 확인해야 합니다.

## 남은 학술 검증

1. OptiCo/TokMan 전체 PDF와 보충자료, Figure·subfigure 전체 inventory 및 정확한 axis/legend를 확보합니다.
2. Hi-ILT hierarchical VAE·BSTE·SepAvgPool 세부, 실험별 baseline·단위·Table/Figure를 확인합니다.
3. ResGNN full text·graph construction·loss·optical conditions·10개 caption을 확인합니다.
4. 저자 공식 코드·weights·dataset artifacts를 구분하고 논문 protocol과 구현 version을 대조합니다.
5. LMLitho·DOINN·Nitho의 optical conditions, split definitions, parameter/model-byte 표기 차이를 추가 검증합니다.
6. 새로운 image permission이 확인되면 확대 UI에 원본을 연결하고 coverage registry를 갱신합니다.

## 연결 문서

[Research Overview]({{ '/ko/notes/research/' | relative_url }}) · [GeoSignal 범위]({{ '/ko/notes/research/geosignal-scope/' | relative_url }}) · [Foundations]({{ '/ko/notes/foundations/' | relative_url }})
