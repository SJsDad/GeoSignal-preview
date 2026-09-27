from __future__ import annotations

import re
import argparse
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


class BuiltPage(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "name" in attrs:
            self.ids.add(attrs["name"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


def validate_built(site, permalinks, errors):
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, help="Also validate actual Jekyll output routes, links, assets and fragments")
    args = parser.parse_args()
    errors: list[str] = []
    documents: dict[Path, str] = {}
    permalinks: dict[str, Path] = {}

    for path in sorted(DOCS.rglob("*.md")):
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

    print(f"Markdown files: {len(documents)}")
    print(f"Unique permalinks: {len(permalinks)}")
    print(f"Validation errors: {len(errors)}")
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
