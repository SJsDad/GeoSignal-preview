# GeoSignal Preview

A public introduction to layout-review examples and optical learning.

## Explore

* [Home](https://sjsdad.github.io/GeoSignal-preview/) · [한국어](https://sjsdad.github.io/GeoSignal-preview/ko/)
* [Layout examples](https://sjsdad.github.io/GeoSignal-preview/demo/)
* Original v0.11 Demo for comparison: [English](https://sjsdad.github.io/GeoSignal-preview/demo-legacy/) · [한국어](https://sjsdad.github.io/GeoSignal-preview/ko/demo-legacy/)
* [Method and scope](https://sjsdad.github.io/GeoSignal-preview/method/)
* [Technical Notes](https://sjsdad.github.io/GeoSignal-preview/notes/)
* 6f educational simulator: [English](https://sjsdad.github.io/GeoSignal-preview/simulator/) · [한국어](https://sjsdad.github.io/GeoSignal-preview/ko/simulator/)
* [Release summaries](https://sjsdad.github.io/GeoSignal-preview/release-notes/)

The layout demo connects candidate regions with local optical images and
relative-dose contours. Representative figures use public or synthetic layouts;
conditions and interpretation limits are stated on the Demo page. GDS/OAS
analysis is served separately; use only non-confidential input in the public demo.

The bilingual Home, Demo and Method pages use the original v0.11 content and
presentation. The Demo includes its original scrollable iframe, candidate
selection, enlarged images and saved focus/dose comparisons. Home adds only a
link and short introduction to the v0.12 6f simulator. New input files are
analyzed through the separate live service.

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

The restored pages preserve their previously published diagrams, example values
and downloads from commit `7bb4ea4`. This is an explicit exception to the reduced
public scope, not a reconstruction. Apart from Home's requested 6f notice, only
asset URLs and language-link attributes change. The 22 original assets and eight
rendered pages (six primary pages and two earlier Demo links) are checked against
a pinned SHA-256 manifest. No additional private engine files are published.

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

Optional browser checks in `scripts/test_bilingual_simulator.py` and `scripts/test_technical_notes.py`
use Playwright against a served build.
`scripts/test_original_demo.py` compares the restored pages' complete DOM against
a separately served build of their original Git revision, allowing only routing,
language-link changes and the requested 6f Home notice. `scripts/restore_original_demo.py --check` verifies
the export against that historical build.
The simulator files share a maintained educational implementation; its public
manifest records exported hashes.

## Feedback and reuse

Use the site's feedback link for public examples, interpretation and usability
feedback. Do not submit confidential or proprietary layout/process information.

The repository is shared for technical discussion and feedback. The absence of
a license does not grant permission to reuse, modify or redistribute its contents.
