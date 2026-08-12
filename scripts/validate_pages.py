from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PERMALINK_PATTERN = re.compile(r"^permalink:\s*(\S+)\s*$", re.MULTILINE)
RELATIVE_URL_PATTERN = re.compile(
    r"{{\s*'(/[^']+)'\s*\|\s*relative_url\s*}}"
)


def main() -> int:
    errors: list[str] = []
    documents: dict[Path, str] = {}
    permalinks: dict[str, Path] = {}

    for path in sorted(DOCS.rglob("*.md")):
        try:
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

    print(f"Markdown files: {len(documents)}")
    print(f"Unique permalinks: {len(permalinks)}")
    print(f"Validation errors: {len(errors)}")
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
