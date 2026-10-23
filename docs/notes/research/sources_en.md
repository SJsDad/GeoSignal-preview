---
layout: technical
category: research
title: "Source Access · Figure Coverage · Reuse Conditions"
permalink: /notes/research/sources/
lang: en
---

# Source Access · Figure Coverage · Reuse Conditions

* Contents
{:toc}

## Rules for interpreting evidence

**Full text reviewed** means the actual PDF or HTML was read. **Partial indexed text reviewed** means official-PDF indexed passages supported method/caption/table checks without access to the full document or visuals. **Abstract/table reviewed** means only the publisher's public content was available. Search indexing alone is not full-paper access.

Reviews distinguish source-supported equations, notation-only rewrites and independent general theory. Unknown dimensions, NA, source conditions, runtime units and licenses are not guessed. Recalculated quantities are labeled independent calculations.

## Access status by paper

| Paper | Material actually checked | Limits / remaining checks |
| --- | --- | --- |
| [OptiCo]({{ '/notes/research/optico/' | relative_url }}) | CVF metadata, partial official-PDF index, equations (6)–(15), Tables 1–5 and references to Figures 1–6 | Direct PDF 403; complete figures/subfigures, appendices, license and official code unverified |
| [Hi-ILT]({{ '/notes/research/hi-ilt/' | relative_url }}) | ScienceDirect metadata, abstract, Highlights and author listings | Full text 403/purchase notice; VAE internals, tables, figure count, affiliations and supplement unknown |
| [LMLitho]({{ '/notes/research/lmlitho/' | relative_url }}) | Full nine-page author PDF, Tables I–IV, Algorithm 1, official data README | Separate supplement, complete calibrated optical setup and model code/weights unverified |
| [TokMan]({{ '/notes/research/tokman/' | relative_url }}) | NeurIPS metadata/abstract, partial official index, Sections 4–5, Table 1 and Figures 1–6 | Approximately 15.5 MB PDF size limit, OpenReview browser challenge, unparsed ZIP; full visuals/inventory/appendix unknown |
| [ResGNN-OPC]({{ '/notes/research/resgnn-opc/' | relative_url }}) | Optica metadata, affiliations, abstract, Table 1, Data Availability and ten-figure count | Subscription required; full text, seven equations, captions/images and optics unknown |
| [TEMPO]({{ '/notes/research/tempo/' | relative_url }}) | Full eight-page author GitHub PDF, Figures 1–5, Tables 1–5 | ACM DOI page 403; obsolete homepage PDF 404 replaced by actual author file; supplement/model availability unknown |
| [DOINN]({{ '/notes/research/doinn/' | relative_url }}) | Full arXiv v1 PDF/HTML, Figures 1–9, Tables 1–4, Appendix A.1/A.2 | Camera-ready differences, complete optics and author code/weights unknown |
| [Nitho]({{ '/notes/research/nitho/' | relative_url }}) | Full arXiv v4 PDF/HTML, Figures 1–6, Tables I–V, Algorithm 1 | Camera-ready differences, separate supplement and author code/weights unknown |

Limited access does not mean source links are absent. Official URLs and failure reasons are retained. Access controls and tool limits were not bypassed, and not every external URL is claimed to have returned HTTP 200 in this environment.

## Figure coverage totals

| Paper | Known main figure numbers | Text/caption-based readings | Source links only | Complete inventory? |
| --- | --- | ---: | ---: | --- |
| OptiCo | 1–6 | 6 · Partial index | 0 | Unconfirmed minimum |
| Hi-ILT | Unknown | 0 | Official article entry | Unconfirmed |
| LMLitho | 1–13 | 13 | 0 | Main paper confirmed |
| TokMan | 1–6 | 6 · Partial index | 0 | Unconfirmed minimum |
| ResGNN-OPC | 1–10 | 0 | 10 | Publisher count confirmed; captions unknown |
| TEMPO | 1–5 | 5 | 0 | Main paper confirmed |
| DOINN | 1–9 | 9 | 0 | Main paper confirmed |
| Nitho | 1–6 | 6 | 0 | Main paper confirmed |

The registry contains **55 numbered entries** and **45 text/caption-based readings**: 33 from four fully read papers and 12 from partial official indexes. Ten are limited ResGNN links. No total-coverage percentage assumes unavailable papers/supplements have zero figures.

The site redistributes **zero original paper figure files** and contains **eight independently drawn SVG diagrams**. Zoom and original-SVG links are separate from paper-figure coverage. Experimental numbers appear in rewritten data tables.

## Copyright and reuse decisions

| Source | Checked conditions | Treatment here |
| --- | --- | --- |
| CVF OptiCo | Open-access availability; individual figure-reuse license unknown | Links and independent diagrams; access is not assumed permission |
| Elsevier Hi-ILT | Purchase/access notice; figure license unknown | No original reproduction |
| Author LMLitho PDF | Author-hosted copy; figure permission unknown | Repository MIT license is not assumed to cover PDF figures |
| NeurIPS TokMan | Official paper/supplement entries; file licenses incompletely verified | Access distinguished from reuse; no reproduction |
| Optica ResGNN | All rights reserved; subscription figures | No reproduction |
| Author ACM TEMPO PDF | Author copy available; redistribution permission unknown | Public access does not establish figure permission |
| arXiv DOINN | Perpetual nonexclusive posting license | Not interpreted as third-party reuse permission |
| arXiv Nitho v4 | CC BY-NC-ND 4.0 | Linked while applicability of noncommercial/no-derivatives terms remains unconfirmed |
| Original explanatory SVGs | Newly drawn for these learning notes | Captions/alt text distinguish them from paper figures |
| MathJax 3.2.2 | Apache 2.0, vendored LICENSE | Source, fonts and license supplied separately from paper figures |

Summaries and source locations replace wholesale caption reproduction. Originals, reconstructions, new explanations and experimental data remain distinguishable. Additional original images require checking actual reuse terms and third-party notices first.

## Remaining scholarly verification

1. Obtain full OptiCo/TokMan papers and supplements; verify all figures/subfigures and axes/legends.
2. Check Hi-ILT VAE/BSTE/SepAvgPool details, experiment baselines, units and tables/figures.
3. Read ResGNN full text, graph construction, losses, optical conditions and ten captions.
4. Distinguish official code, weights and datasets; align protocols and versions.
5. Further check LMLitho/DOINN/Nitho optics, split definitions and parameter/model-byte discrepancies.
6. Update the zoom UI and coverage registry if additional image permissions are verified.

## Related pages

[Research Overview]({{ '/notes/research/' | relative_url }}) · [GeoSignal scope]({{ '/notes/research/geosignal-scope/' | relative_url }}) · [Foundations]({{ '/notes/foundations/' | relative_url }})
