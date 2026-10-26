"""Export the actual pre-v0.12 Demo, changing routing only.

Build docs from SOURCE_COMMIT with Jekyll first, then pass --source-site.
Images, the iframe application and its inline data are copied byte for byte.
The current demo and private layout engine are not inputs to this export.
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
    *(f"assets/demo/tt04-comparison/layer{layer}_{kind}.png"
      for layer in (67, 68) for kind in ("nominal", "width", "space", "bossung")),
)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def git_file(path):
    return subprocess.run(["git", "show", f"{SOURCE_COMMIT}:docs/{path}"], cwd=ROOT,
                          check=True, capture_output=True).stdout


def export(source_site):
    files = {}
    manifest = {"source_commit": SOURCE_COMMIT, "routing_only": True, "assets": {}, "pages": {}}
    for relative in ASSETS:
        original = git_file(relative)
        assert (source_site / relative).read_bytes() == original, f"Historical asset changed: {relative}"
        files[f"{PREFIX}/{relative}"] = original
        manifest["assets"][relative] = digest(original)
    for language, prefix, suffix in (("en", "", ""), ("ko", "/ko", "_ko")):
        source_path = f"demo{suffix}.md"
        original = (source_site / prefix.lstrip("/") / "demo/index.html").read_text()
        html = original.replace(f'"{BASE}/assets/', f'"{BASE}/{PREFIX}/assets/')
        for route_prefix in ("", "/ko"):
            html = html.replace(f'"{BASE}{route_prefix}/demo/"', f'"{BASE}{route_prefix}/demo-legacy/"')
        # The old inline language switch predates hreflang. Add the attribute
        # without changing its text, position or styling.
        html = re.sub(r'(<p class="language-switch"><a [^>]*lang="(en|ko)")>',
                      lambda m: f'{m[1]} hreflang="{m[2]}">', html)
        route = f"{prefix}/demo-legacy/"
        page_path = f"demo_legacy{suffix}.html"
        front = (f"---\nlayout: null\ntitle: Original v0.11 Demo\n"
                 f"permalink: {route}\nlang: {language}\n---\n")
        files[page_path] = (front + html).encode()
        manifest["pages"][page_path] = {
            "route": route, "source_path": source_path,
            "source_sha256": digest(git_file(source_path)),
            "original_html_sha256": digest(original.strip().encode()),
            "published_html_sha256": digest(html.strip().encode()),
        }
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
    print("Original v0.11 Demo verified." if args.check else "Exported original v0.11 Demo with routing-only changes.")


if __name__ == "__main__":
    main()
