---
layout: default
title: GeoSignal Preview
description: Public layout-review examples and a browser-based 6f optical learning
  demo
permalink: /
---

# GeoSignal Preview

**Find narrow lines and gaps in a layout, then inspect selected regions through a simplified optical model.** This public preview connects geometry review with aerial images and relative-dose contours.

![From layout to candidate and optical review]({{ '/assets/demo/public/overview.png' | relative_url }})

The example uses a public TT04 PWM layout. The panels follow one region from layout to mask, light distribution and contours. These are model illustrations, not wafer measurements.

{% include live-demo-cta.html %}

## GDS/OAS layout review

The layout-analysis demo highlights candidate regions and lets you compare their local optical response. [Demo]({{ '/demo/' | relative_url }}) explains the example conditions and how to read the figures; [Method]({{ '/method/' | relative_url }}) gives the conceptual workflow.

## 6f educational simulator

[Open the 6f simulator]({{ '/simulator/' | relative_url }}) to follow rays from source to wafer and explore the same orders in pupil and wave plots. It runs directly on Pages in English or Korean, with no Render startup wait. Read the [optical principles]({{ '/notes/diffraction-defocus/' | relative_url }}) alongside it.

## Explore the site

| Page | Purpose |
| --- | --- |
| [Demo]({{ '/demo/' | relative_url }}) | Representative results and interpretation |
| [Method]({{ '/method/' | relative_url }}) | Conceptual workflow and model scope |
| [Technical Notes]({{ '/notes/' | relative_url }}) | Optical foundations and research-paper explanations |
| [Release Notes]({{ '/release-notes/' | relative_url }}) | User-visible changes and validation summaries |

The [v0.12 notes]({{ '/release-notes/v0.12/' | relative_url }}) cover the bilingual simulator and public documentation. The numerical studies in v0.11 did not introduce new layout-analysis options into the live demo.

## Scope and feedback

The preview supports selected regions in public or synthetic layouts. It is an educational review aid, not a calibrated process-verification service. Use only public, non-confidential files in the live demo. Share feedback through the site navigation.
