---
layout: default
title: Pre-v0.12 Demo Comparison
description: Compare the earlier scrollable application screen with the current demo
permalink: /demo-legacy/
lang: en
---

# Pre-v0.12 Demo Comparison

This comparison restores the screen layout used before v0.12: an input panel on the left, saved results on the right, and scrolling inside an 850 px frame. The current Demo remains available while you compare the two presentations.

[Current Demo]({{ '/demo/' | relative_url }}) · [Open the earlier screen at full width ↗]({{ '/demo-legacy/screen/' | relative_url }})

## 1. Earlier application screen

<iframe id="legacy-demo-frame" src="{{ '/demo-legacy/screen/' | relative_url }}" title="Earlier GeoSignal application screen with internal scrolling" width="100%" height="850" loading="lazy" style="border:1px solid #dce3ec;border-radius:10px" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>

Scroll **inside the screen** to explore the saved results. Select Width or Space, choose 4 / 6 / 8 candidates, and click a card to move to its large image. There are six saved examples per type; choosing 8 does not create additional results.

## 2. What to compare

| Earlier presentation | What to try |
| --- | --- |
| Complete application layout | View the input controls and result panel together. |
| Internal scrolling | Browse long results while keeping this page compact. |
| Candidate-led review | Start with the layout overview, then select a candidate and inspect its large image. |
| Optional focus/dose comparison | Use the checkbox or detail heading. Candidate 1 in each type has nine saved conditions and a Bossung curve. |

This is a reconstruction of the earlier presentation using reviewed saved images and display values. Internal calibration information, raw downloads and calculation settings are excluded; some input fields therefore show placeholders. Uploads and new analysis remain disabled, as in the original saved-data preview. Figures and measurements are model results, not wafer validation.

{% include live-demo-cta.html %}
