"""Restore the pre-v0.12 Home, Demo and Method, plus the requested Home notice.

Build docs from SOURCE_COMMIT with Jekyll first, then pass --source-site.
Images, the iframe application and its inline data are copied byte for byte.
The current pages and private layout engine are not inputs to this export.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "7bb4ea485bd30fb5337e8f6c141d11d871eba234"
BASE = "/GeoSignal-preview"
PREFIX = "assets/demo/original-v0.11"
ASSETS = (
    "assets/css/style.css",
    "assets/demo/ui-guide/reference-draft.html",
    "assets/demo/ui-guide/style.css",
    "assets/demo/v0.10/speed/geometry_candidate_overview.png",
    "assets/demo/v0.10/speed/pya_native_combined_review.gds",
    "assets/release-notes/v0.10/width_area_desc_review/top6.png",
    "assets/release-notes/v0.10/width_area_desc_review/space_top6.png",
    "assets/demo/tt04-comparison/conditions.json",
    "assets/demo/tt04-comparison/measurements.csv",
    "assets/demo/v0.10/speed/home_aerial_overlay.png",
    "assets/demo/tt04-comparison/method_flow_67_roi.png",
    "assets/method/abbe_debug_9.png",
    "assets/method/abbe_debug_dense.png",
    "assets/method/source_sampling_comparison.png",
    *(f"assets/demo/tt04-comparison/layer{layer}_{kind}.png"
      for layer in (67, 68) for kind in ("nominal", "width", "space", "bossung")),
)
HOME_NOTICE = {
    "ko": ('<section id="home-6f-simulator"><h2>6f 광선·파동 시뮬레이터</h2>'
           f'<p><a href="{BASE}/ko/simulator/">시뮬레이터 실행</a>에서 광원→웨이퍼의 6f 광선 경로와 '
           '같은 회절 차수의 pupil·파동 결과를 함께 조작할 수 있습니다. Pages에서 직접 실행되며 '
           'Render 서버 기동을 기다리지 않습니다. (v0.12 추가)</p></section>'),
    "en": ('<section id="home-6f-simulator"><h2>6f Ray and Wave Simulator</h2>'
           f'<p>In <a href="{BASE}/simulator/">Run simulator</a>, interactively explore the 6f ray paths '
           'from source → wafer alongside the pupil and wave results for the same diffraction orders. '
           'Runs directly on Pages without waiting for the Render server to start. '
           '(Added in v0.12)</p></section>'),
}


def digest(value):
    return hashlib.sha256(value).hexdigest()


def git_file(path):
    return subprocess.run(["git", "show", f"{SOURCE_COMMIT}:docs/{path}"], cwd=ROOT,
                          check=True, capture_output=True).stdout


def routed_html(original, legacy=False):
    html = original.replace(f'"{BASE}/assets/', f'"{BASE}/{PREFIX}/assets/')
    if legacy:
        for route_prefix in ("", "/ko"):
            html = html.replace(f'"{BASE}{route_prefix}/demo/"', f'"{BASE}{route_prefix}/demo-legacy/"')
    return re.sub(r'(<p class="language-switch"><a [^>]*lang="(en|ko)")>',
                  lambda m: f'{m[1]} hreflang="{m[2]}">', html)


def add_page(files, manifest, source_site, language, source, route, output, *, legacy=False, home=False):
    source_route = route.replace("demo-legacy", "demo") if legacy else route
    original = (source_site / source_route.lstrip("/") / "index.html").read_text()
    html = routed_html(original, legacy)
    if home:
        html, count = re.subn(r'(<section class="live-demo-callout"[\s\S]*?</section>)',
                             lambda m: m[0] + HOME_NOTICE[language], html, count=1)
        assert count == 1, "Original Home callout not found"
    front = (f"---\nlayout: null\ntitle: Original v0.11 {source.split('.')[0]}\n"
             f"permalink: {route}\nlang: {language}\n---\n")
    files[output] = (front + html).encode()
    manifest["pages"][output] = {
        "route": route, "source_path": source,
        "source_sha256": digest(git_file(source)),
        "original_html_sha256": digest(original.strip().encode()),
        "published_html_sha256": digest(html.strip().encode()),
    }


def export(source_site):
    files = {}
    manifest = {"source_commit": SOURCE_COMMIT, "home_addition": "6f simulator notice only",
                "assets": {}, "pages": {}}
    for relative in ASSETS:
        original = git_file(relative)
        assert (source_site / relative).read_bytes() == original, f"Historical asset changed: {relative}"
        files[f"{PREFIX}/{relative}"] = original
        manifest["assets"][relative] = digest(original)
    for language, prefix, suffix in (("en", "", ""), ("ko", "/ko", "_ko")):
        add_page(files, manifest, source_site, language, f"demo{suffix}.md",
                 f"{prefix}/demo-legacy/", f"demo_legacy{suffix}.html", legacy=True)
        for name, path in (("index", "/"), ("demo", "/demo/"), ("method", "/method/")):
            add_page(files, manifest, source_site, language, f"{name}{suffix}.md",
                     f"{prefix}{path}", f"{name}{suffix}.html", home=name == "index")
    files[f"{PREFIX}/manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-site", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for relative, content in export(args.source_site).items():
        destination = ROOT / "docs" / relative
        if args.check:
            assert destination.read_bytes() == content, f"Original Demo export changed: {relative}"
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
    for name in ("index", "demo", "method"):
        for suffix in ("", "_ko"):
            obsolete = ROOT / "docs" / f"{name}{suffix}.md"
            if args.check:
                assert not obsolete.exists(), f"Duplicate restored route: {obsolete}"
            elif obsolete.exists():
                obsolete.unlink()
    print("Original v0.11 pages verified." if args.check else "Restored original v0.11 pages with only the requested Home notice.")


if __name__ == "__main__":
    main()
