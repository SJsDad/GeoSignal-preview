# GeoSignal Preview

A public introduction to layout-review examples and optical learning.

## Explore

* [Home](https://sjsdad.github.io/GeoSignal-preview/) · [한국어](https://sjsdad.github.io/GeoSignal-preview/ko/)
* [Layout examples](https://sjsdad.github.io/GeoSignal-preview/demo/)
* Earlier application layout for comparison: [English](https://sjsdad.github.io/GeoSignal-preview/demo-legacy/) · [한국어](https://sjsdad.github.io/GeoSignal-preview/ko/demo-legacy/)
* [Method and scope](https://sjsdad.github.io/GeoSignal-preview/method/)
* [Technical Notes](https://sjsdad.github.io/GeoSignal-preview/notes/)
* 6f educational simulator: [English](https://sjsdad.github.io/GeoSignal-preview/simulator/) · [한국어](https://sjsdad.github.io/GeoSignal-preview/ko/simulator/)
* [Release summaries](https://sjsdad.github.io/GeoSignal-preview/release-notes/)

The layout demo connects candidate regions with local optical images and
relative-dose contours. Representative figures use public or synthetic layouts;
conditions and interpretation limits are stated on the Demo page. GDS/OAS
analysis is served separately; use only non-confidential input in the public demo.

The bilingual Demo also provides an interactive saved-results viewer: candidate
selection, enlarged images, sampled focus/dose comparisons and modeled-dimension
curves. Its reviewed display data contains only the conditions and rounded results
shown to visitors. Private calibration, tuning records and the layout engine are
not included. New input files are analyzed through the separate live service.

The 6f simulator runs directly in the browser on Pages. Its inspectable
JavaScript implementation and optical explanations remain public educational
material. It is separate from the private layout-analysis engine.

## Public scope

This repository presents features, representative results, basic optical
principles, paper explanations, limitations and user-visible change summaries.
Layout-engine architecture, calibration/tuning, optimization details, detailed
benchmark artifacts and reproduction procedures are maintained privately.
Public summaries do not establish calibrated wafer accuracy, universal numerical
settings or guaranteed service performance.

English and Korean pages share navigation and corresponding routes. Paper
reviews identify source-access limits; original explanatory diagrams are
separate from links to published paper figures.

## Website maintenance

Jekyll builds the site from `docs`. The checks below validate routes, language
links, assets, math/image structure and the public asset policy:

```bash
python scripts/validate_pages.py
python scripts/validate_pages.py --site _site
```

Optional browser checks in `scripts/test_saved_demo.py`,
`scripts/test_bilingual_simulator.py` and `scripts/test_technical_notes.py`
use Playwright against a served build.
The simulator files share a maintained educational implementation; its public
manifest records exported hashes.

## Feedback and reuse

Use the site's feedback link for public examples, interpretation and usability
feedback. Do not submit confidential or proprietary layout/process information.

The repository is shared for technical discussion and feedback. The absence of
a license does not grant permission to reuse, modify or redistribute its contents.
