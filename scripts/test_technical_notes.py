"""Browser checks for the built Technical Notes.

Install the test-only dependency: pip install playwright
Install a browser: python -m playwright install chromium
Serve a build under its base URL, e.g. serve a directory containing
GeoSignal-preview/ -> the Jekyll output directory with python -m http.server.
Run: python scripts/test_technical_notes.py --url http://localhost:8000/GeoSignal-preview
Use --chromium /usr/bin/chromium to reuse an installed browser.
Screenshots and JSON are optional via --artifacts work/browser-checks.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright


PAPERS = ["optico", "hi-ilt", "lmlitho", "tokman", "resgnn-opc", "tempo", "doinn", "nitho"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Served Jekyll base URL, including baseurl")
    parser.add_argument("--chromium", help="Optional existing Chromium executable")
    parser.add_argument("--artifacts", type=Path, help="Optional screenshots and verification JSON")
    args = parser.parse_args()
    if args.artifacts:
        args.artifacts.mkdir(parents=True, exist_ok=True)
    url = args.url.rstrip("/")
    results = []
    errors = []
    with sync_playwright() as playwright:
        launch = {"headless": True}
        if args.chromium:
            launch["executable_path"] = args.chromium
        browser = playwright.chromium.launch(**launch)
        context = browser.new_context(viewport={"width": 1440, "height": 1000})
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(f"{url}/ko/notes/research/", wait_until="networkidle")
        assert page.locator("#research-catalog tbody tr:visible").count() == 8
        page.select_option("#review-year", "2026")
        assert page.locator("#research-catalog tbody tr:visible").count() == 2
        page.select_option("#review-field", "Forward Simulation")
        assert page.locator("#research-catalog tbody tr:visible").count() == 1
        page.select_option("#review-architecture", "Hierarchical VAE + ILT")
        assert page.locator("#research-catalog tbody tr:visible").count() == 0
        assert "0 / 8" in page.locator("#review-count").inner_text()
        page.click("#review-reset")
        assert page.locator("#research-catalog tbody tr:visible").count() == 8
        page.select_option("#review-field", "OPC")
        assert page.locator("#research-catalog tbody tr:visible").count() == 1
        page.click("#review-reset")
        if args.artifacts:
            page.screenshot(path=str(args.artifacts / "overview-desktop.png"))
        for width in (1440, 390, 320):
            page.set_viewport_size({"width": width, "height": 900})
            for paper in PAPERS:
                response = page.goto(f"{url}/ko/notes/research/{paper}/", wait_until="networkidle")
                assert response and response.ok, paper
                page.wait_for_function("document.querySelector('mjx-container')")
                page.locator(".study-figure img").evaluate("img => { img.loading = 'eager'; }")
                page.locator(".study-figure img").evaluate("img => img.decode()")
                data = page.evaluate("""() => ({
                    scroll: document.documentElement.scrollWidth,
                    math: document.querySelectorAll('mjx-container').length,
                    mathErrors: document.querySelectorAll('mjx-merror').length,
                    toc: document.querySelectorAll('#markdown-toc a').length,
                    brokenImages: [...document.images].filter(i => i.getAttribute('src') &&
                        (!i.complete || !i.naturalWidth)).map(i => i.src),
                    failedResources: performance.getEntriesByType('resource')
                        .filter(e => e.responseStatus >= 400).map(e => e.name)
                })""")
                assert data["scroll"] <= width + 1, (paper, width, data)
                assert data["math"] > 0 and data["mathErrors"] == 0, (paper, width, data)
                assert data["toc"] >= 9, (paper, data)
                assert not data["brokenImages"] and not data["failedResources"], (paper, data)
                results.append({"paper": paper, "viewport": width, **data})
                pagination = page.locator(".paper-pagination")
                index = PAPERS.index(paper)
                if index:
                    assert pagination.locator('[rel="prev"]').get_attribute("href").endswith(
                        f"/research/{PAPERS[index - 1]}/")
                else:
                    assert pagination.locator('[rel="prev"]').count() == 0
                if index < len(PAPERS) - 1:
                    assert pagination.locator('[rel="next"]').get_attribute("href").endswith(
                        f"/research/{PAPERS[index + 1]}/")
                else:
                    assert pagination.locator('[rel="next"]').count() == 0
                if paper == "nitho" and width == 1440:
                    page.locator("a.figure-zoom").focus()
                    page.keyboard.press("Enter")
                    assert page.locator("#figure-dialog").evaluate("d => d.open")
                    page.locator("#figure-full").evaluate("img => img.decode()")
                    page.keyboard.press("Escape")
                    assert not page.locator("#figure-dialog").evaluate("d => d.open")
                    assert page.locator("a.figure-zoom").evaluate("a => a === document.activeElement")
                    page.locator(".figure-explanation summary").first.click()
                    assert page.locator(".figure-explanation").first.evaluate("d => d.open")
                    if args.artifacts:
                        page.get_by_role("heading", name="Proposed Method / Model Architecture",
                                         exact=True).scroll_into_view_if_needed()
                        page.screenshot(path=str(args.artifacts / "nitho-architecture.png"))
                if paper == "lmlitho" and width == 390 and args.artifacts:
                    page.get_by_role("heading", name="Physics & Mathematical Foundations",
                                     exact=True).scroll_into_view_if_needed()
                    page.screenshot(path=str(args.artifacts / "lmlitho-math-mobile.png"))
        nojs = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 900})
        static = nojs.new_page()
        static.goto(f"{url}/ko/notes/research/")
        assert static.locator("#research-catalog tbody tr:visible").count() == 8
        assert not static.locator(".review-filters").is_visible()
        assert not errors, errors
        context.close()
        nojs.close()
        browser.close()
    if args.artifacts:
        (args.artifacts / "browser-results.json").write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PASS: filter combinations, zero results/reset, 24 responsive paper views, math, "
          "images, pagination, keyboard dialog/focus, figure details and no-JS catalog")


if __name__ == "__main__":
    main()
