from __future__ import annotations

import re
import argparse
import hashlib
import json
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PERMALINK_PATTERN = re.compile(r"^permalink:\s*(\S+)\s*$", re.MULTILINE)
RELATIVE_URL_PATTERN = re.compile(
    r"{{\s*'(/[^']+)'\s*\|\s*relative_url\s*}}"
)
PUBLIC_DEMO_IMAGES = {
    "assets/demo/public/overview.png",
    "assets/demo/public/narrow-line.png",
    "assets/demo/public/narrow-gap.png",
}


def validate_public_assets(root, errors):
    """Check files themselves, including assets with no visible download link."""
    restricted = (".csv", ".csv.gz", ".gds", ".gds.gz", ".oas", ".oas.gz",
                  ".npy", ".npz", ".parquet", ".zip", ".tar", ".tar.gz")
    for path in (root / "assets").rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if path.name.lower().endswith(restricted):
            errors.append(f"engineering data outside public scope: {relative}")
        if path.suffix == ".json" and not relative.startswith(
                ("assets/simulator/", "assets/notes/diffraction-defocus/")):
            errors.append(f"unreviewed data/configuration asset: {relative}")
        if relative.startswith("assets/demo/") and relative not in PUBLIC_DEMO_IMAGES:
            errors.append(f"unreviewed layout-demo asset: {relative}")
        if relative.startswith(("assets/release-notes/", "assets/method/")):
            errors.append(f"detailed engineering artifact outside public scope: {relative}")


def validate_implementation_references(documents, errors):
    # The public optical tutorials and paper citations stay available. References
    # to private source trees or reproduction commands belong in private records.
    implementation = re.compile(
        r"\bsrc[/\\][\w./\\-]+\.py\b|"
        r"\bpython(?:3)?\s+(?:-m\s+)?(?:src\.|experiments[/\\])"
    )
    for path, text in documents.items():
        without_urls = re.sub(r"https?://[^\s)<>]+", "", text)
        if implementation.search(without_urls):
            errors.append(f"private implementation reference outside public scope: {path.name}")


class BuiltPage(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.language = None
        self.language_links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "a" and attrs.get("hreflang"):
            self.language_links.append((attrs["hreflang"], attrs.get("href")))
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "name" in attrs:
            self.ids.add(attrs["name"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


def validate_built(site, permalinks, errors):
    validate_public_assets(site, errors)
    base = "/GeoSignal-preview"
    pages = {}
    for route in permalinks:
        destination = site / route.lstrip("/")
        if route.endswith("/"):
            destination /= "index.html"
        if not destination.is_file():
            errors.append(f"missing built route: {route}")
    for path in site.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if "{{" in text or "{%" in text:
            errors.append(f"unrendered Liquid in {path.relative_to(site)}")
        pages[path.resolve()] = BuiltPage(text)
    for route in permalinks:
        destination = site / route.lstrip("/")
        if route.endswith("/"):
            destination /= "index.html"
        page = pages.get(destination.resolve())
        if page is None:
            continue
        korean = route.startswith("/ko/")
        counterpart = route.removeprefix("/ko") if korean else "/ko" + route
        expected = ("en" if korean else "ko", base + counterpart)
        if page.language != ("ko" if korean else "en"):
            errors.append(f"incorrect HTML language: {route}")
        if page.language_links != [expected]:
            errors.append(f"incorrect language switch: {route}: {page.language_links}")
    for path, page in pages.items():
        origin = base + "/" + path.relative_to(site.resolve()).as_posix()
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = urlsplit(urljoin(origin, link))
            if not target.path.startswith(base + "/"):
                errors.append(f"link outside baseurl: {path.name}: {link}")
                continue
            local = site / unquote(target.path[len(base) + 1:])
            if local.is_dir():
                local /= "index.html"
            if not local.is_file():
                errors.append(f"missing built link: {path.relative_to(site.resolve())}: {link}")
            elif target.fragment and local.resolve() in pages and unquote(target.fragment) not in pages[local.resolve()].ids:
                errors.append(f"missing fragment: {path.relative_to(site.resolve())}: {link}")
    print(f"Built HTML files: {len(pages)}")


def validate_language_pairs(documents, permalinks, errors):
    """Catch missing counterparts and dropped teaching material during edits."""
    signatures = {
        "headings": r"^#{1,4} ",
        "display-math delimiters": r"^\$\$\s*$",
        "images": r"<img\s|!\[",
    }
    for route, path in permalinks.items():
        counterpart = route.removeprefix("/ko") if route.startswith("/ko/") else "/ko" + route
        if counterpart not in permalinks:
            errors.append(f"missing language counterpart: {route} -> {counterpart}")
        elif not route.startswith("/ko/"):
            for label, pattern in signatures.items():
                count = len(re.findall(pattern, documents[path], re.MULTILINE))
                other = len(re.findall(pattern, documents[permalinks[counterpart]], re.MULTILINE))
                if count != other:
                    errors.append(f"language pair differs in {label}: {route}: en={count}, ko={other}")

    # Translation can change descriptions, but not the evidence source inventory.
    original = (DOCS / "_data/figure_coverage.yml").read_text(encoding="utf-8")
    translated = (DOCS / "_data/figure_coverage_en.yml").read_text(encoding="utf-8")
    for label, pattern in {
        "figure sources": r"^\s*url:\s*(\S+)",
        "figure numbers": r"^\s*- number:\s*(\S+)",
        "inventory status": r"^\s*inventory_complete:\s*(\S+)",
    }.items():
        if re.findall(pattern, original, re.MULTILINE) != re.findall(pattern, translated, re.MULTILINE):
            errors.append(f"translated {label} differ from Korean evidence")

    manifest_path = DOCS / "assets/simulator/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for relative, expected in manifest["sha256"].items():
        path = ROOT / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f"stale simulator export: {relative}; regenerate from GeoSignal-lab")
    strings = json.loads((DOCS / "assets/simulator/simulator-i18n.json").read_text(encoding="utf-8"))
    if strings["en"].keys() != strings["ko"].keys():
        errors.append("simulator translation keys differ")
    else:
        for key, english in strings["en"].items():
            korean = strings["ko"][key]
            if isinstance(english, str) and re.findall(r"\{\w+\}", english) != re.findall(r"\{\w+\}", korean):
                errors.append(f"simulator placeholders differ: {key}")
    print(f"Bilingual route pairs: {len(permalinks) // 2}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, help="Also validate actual Jekyll output routes, links, assets and fragments")
    args = parser.parse_args()
    errors: list[str] = []
    documents: dict[Path, str] = {}
    permalinks: dict[str, Path] = {}

    # Standalone interactive HTML pages also have Jekyll front matter/routes.
    sources = [*DOCS.rglob("*.md"), *DOCS.rglob("*.html")]
    for path in sorted(sources):
        if path.suffix == ".html":
            if path.relative_to(DOCS).parts[0] in {"_includes", "_layouts"}:
                continue
            if not path.read_bytes().removeprefix(b"\xef\xbb\xbf").startswith(b"---\n"):
                continue  # Copied static HTML without front matter is not a Jekyll page.
        try:
            if path.read_bytes().startswith(b"\xef\xbb\xbf"):
                errors.append(f"UTF-8 BOM hides Jekyll front matter: {path.relative_to(ROOT)}")
            text = path.read_text(encoding="utf-8-sig", errors="strict")
        except UnicodeDecodeError as exc:
            errors.append(f"invalid UTF-8: {path.relative_to(ROOT)}: {exc}")
            continue

        documents[path] = text
        if not text.startswith("---\n"):
            errors.append(f"missing front matter: {path.relative_to(ROOT)}")
            continue

        match = PERMALINK_PATTERN.search(text)
        if match is None:
            errors.append(f"missing permalink: {path.relative_to(ROOT)}")
            continue

        route = match.group(1)
        previous = permalinks.get(route)
        if previous is not None:
            errors.append(
                "duplicate permalink "
                f"{route}: {previous.relative_to(ROOT)} and {path.relative_to(ROOT)}"
            )
        else:
            permalinks[route] = path

    for path, text in documents.items():
        for route in RELATIVE_URL_PATTERN.findall(text):
            if route.startswith("/assets/"):
                asset = DOCS / route.lstrip("/")
                if not asset.is_file():
                    errors.append(
                        f"missing asset from {path.relative_to(ROOT)}: {route}"
                    )
            elif route not in permalinks:
                errors.append(
                    f"missing route from {path.relative_to(ROOT)}: {route}"
                )

    validate_language_pairs(documents, permalinks, errors)
    validate_public_assets(DOCS, errors)
    validate_implementation_references(
        {**documents, ROOT / "README.md": (ROOT / "README.md").read_text(encoding="utf-8")}, errors
    )

    # Public presentation must not expose personal development dates/schedules.
    chronology = re.compile(
        r"\b20\d{2}-\d{2}-\d{2}\b|20\d{2}년\s*\d{1,2}월|"
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Aug)\s+\d{1,2}(?:,|\s)|"
        r"\b(?:released on|release date|official release|updated on|last updated|development date|development schedule|milestone date|planned for|completed on)\b",
        re.IGNORECASE,
    )
    public_text = [ROOT / "README.md", *DOCS.rglob("*.md"),
                   *DOCS.rglob("*.html"), *DOCS.rglob("*.yml")]
    for path in public_text:
        for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            if chronology.search(line):
                errors.append(f"public chronology: {path.relative_to(ROOT)}:{number}")

    if args.site is not None:
        validate_built(args.site.resolve(), permalinks, errors)

    print(f"Jekyll source pages: {len(documents)}")
    print(f"Unique permalinks: {len(permalinks)}")
    print(f"Validation errors: {len(errors)}")
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
