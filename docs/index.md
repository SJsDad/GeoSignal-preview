---
layout: default
title: GeoSignal Preview
description: Find weak layout candidates and review their optical contours from GDS/OAS
permalink: /
---

<p class="language-switch"><a href="{{ '/ko/' | relative_url }}" lang="ko">한국어로 보기</a></p>

# GeoSignal Preview

## Find where to look in your layout.

**Turn a GDS/OAS layout into a shortlist of weak geometry candidates, then inspect how their shapes respond to a simplified optical model.** GeoSignal helps you move from a layout file to locations worth a closer look, without assembling a separate analysis pipeline.

{% include live-demo-cta.html %}

![A width candidate and its relative-dose contours]({{ '/assets/demo/v0.10/speed/width_candidate.png' | relative_url }})

<p class="demo-caption">An automatically selected width candidate in a public layout. The cross marks the review location; the three outlines show relative dose −10%, nominal and +10%. <a href="{{ '/demo/' | relative_url }}">Explore the results →</a></p>

## From a layout file to a focused review

1. **Choose a layout and layer.** Start with a public GDS/OAS example and the default Speed preset.
2. **Find candidate locations.** Width and space screening narrows the layout down to regions that deserve attention.
3. **Inspect the local shape.** View the geometry, optical intensity and dose-dependent contours together, then download a review GDS or result tables.

The live preview is still developing. Registered examples use a built-in reference; other layouts currently need a reference-pattern input. See the [getting-started notes on Demo]({{ '/demo/' | relative_url }}#getting-started) before uploading your own example.

## Why look beyond geometry?

A narrow neck, a tight gap or a line end can look acceptable in the original drawing yet respond differently under optical imaging. GeoSignal brings the candidate location and its local contours into the same view so you can inspect rounding, narrowing, spacing and shape sensitivity.

It helps answer **“Which locations should I investigate next?”** The results are approximate review aids, not confirmed manufacturing defects.

## What you get

| Result | How it helps |
| --- | --- |
| Candidate overview | Locate narrow-width and narrow-space regions across the layout |
| Local contour overlays | See shape changes around selected candidates |
| Measurements and status | Review available width/space measurements and recognize unavailable results |
| Review GDS and tables | Continue the inspection in a layout viewer or compare results |

## Built for exploration

GeoSignal is intended for students, researchers and engineers exploring the relationship between layout geometry and optical response using public examples. It offers an accessible starting point for layout review and computational lithography study.

The model is simplified and is not fitted to wafer measurements. Results are not process signoff. Upload only public, non-confidential layouts.

[See the Demo]({{ '/demo/' | relative_url }}) · [How it works]({{ '/method/' | relative_url }}) · [Technical validation]({{ '/notes/v0.10-validation/' | relative_url }})

## Help shape the preview

Which candidate views are useful? What makes a result difficult to interpret? <a href="{{ site.feedback_url }}" target="_blank" rel="noopener noreferrer">Share your feedback</a>.
