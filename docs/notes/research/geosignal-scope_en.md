---
layout: technical
category: research
title: GeoSignal Scope and Research Connections
permalink: /notes/research/geosignal-scope/
lang: en
description: Public capabilities, research context and model limits
---

# GeoSignal Scope and Research Connections

This page separates the public preview's capabilities from the research discussed in the paper reviews.

* Contents
{:toc}

## Public capabilities

| Area | What visitors can explore |
| --- | --- |
| Layout review | Candidate locations around narrow lines and gaps in public/synthetic examples. |
| Optical views | Local light-distribution images and modeled contours. |
| Condition comparisons | Selected focus and relative-dose behavior within an idealized model. |
| Learning | The standalone 6f ray/wave demo, optical foundations and paper reviews. |

The public scope is an educational review workflow. It does not establish automatic OPC, calibrated resist chemistry, mask-3D prediction or manufacturing signoff.

## Interpreting the research reviews

The papers explore learned optical models, source conditioning, mask generation and geometry-aware correction. These are related research directions; reviewing a paper does not mean its model has been implemented in GeoSignal.

## Model limits

A representative image is not a full-layout error guarantee. Threshold contours differ from measured resist profiles, and idealized focus/dose comparisons differ from a calibrated wafer process window. See [Demo]({{ '/demo/' | relative_url }}) for the public examples and interpretation conditions.

## Public documentation scope

Public material covers features, representative results, basic principles, paper explanations, limitations and change summaries. Internal architecture, calibration/tuning procedures, optimization details and detailed benchmark/reproduction records are maintained privately.

## Related pages

* [Research Overview]({{ '/notes/research/' | relative_url }})
* [Method]({{ '/method/' | relative_url }})
* [6f simulator]({{ '/simulator/' | relative_url }})
