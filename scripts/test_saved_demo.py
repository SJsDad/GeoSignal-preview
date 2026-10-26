"""Check the bilingual saved-results viewer against a served Jekyll build.

Uses the same test-only Playwright dependency as test_technical_notes.py.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--chromium")
    parser.add_argument("--artifacts", type=Path)
    args = parser.parse_args()
    if args.artifacts:
        args.artifacts.mkdir(parents=True, exist_ok=True)
    base = args.url.rstrip("/")
    origin = urlsplit(base).netloc
    errors, requests, views = [], [], []
    with sync_playwright() as playwright:
        launch = {"headless": True}
        if args.chromium:
            launch["executable_path"] = args.chromium
        browser = playwright.chromium.launch(**launch)
        context = browser.new_context(viewport={"width": 1440, "height": 1000})
        context.route("**/*", lambda route: route.continue_()
                      if urlsplit(route.request.url).netloc == origin else route.abort())
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda request: requests.append((request.method, request.url)))

        def field(name):
            return page.locator(f"[data-demo-viewer] [data-{name}]")

        def decoded():
            page.locator("[data-demo-viewer] img[src]").evaluate_all(
                "images => Promise.all(images.map(i => {i.loading='eager'; return i.decode();}))")

        for language, prefix in (("en", ""), ("ko", "/ko")):
            page.goto(f"{base}{prefix}/demo/", wait_until="networkidle")
            page.wait_for_selector('[data-demo-viewer][data-state="ready"]')
            root = page.locator("[data-demo-viewer]")
            assert page.locator("html").get_attribute("lang") == language
            assert field("cards").locator("button").count() == 6
            assert field("geometry").inner_text() == "170 nm"
            assert field("measured").inner_text() == "166.34 nm"
            nominal = field("selected-image").get_attribute("src")
            page.locator('[data-candidate="width-2"]').click()
            assert field("selected-image").get_attribute("src") != nominal
            assert page.locator('[data-candidate="width-2"]').evaluate("e=>e===document.activeElement")
            field("comparison").locator("summary").first.click()
            assert field("no-comparison").is_visible()
            assert field("comparison-content").is_hidden()
            page.locator('[data-candidate="width-6"]').click()
            field("count").select_option("4")
            assert root.get_attribute("data-selected") == "width-1"
            assert field("cards").locator("button").count() == 4
            assert field("measurements").locator("tr").count() == 9
            assert field("bossung").locator("circle").count() == 9
            assert field("selected-image").get_attribute("src").endswith("67-width-1-f1-d1.png")
            page.locator(".saved-grid summary").click()
            page.locator('[data-sample="0.2,1.1"]').click()
            assert field("focus").input_value() == "0.2"
            assert field("dose").input_value() == "1.1"
            assert field("selected-image").get_attribute("src").endswith("67-width-1-f2-d2.png")
            assert page.locator('[data-sample="0.2,1.1"]').evaluate("e=>e===document.activeElement")
            field("layer").select_option("68")
            assert field("cards").locator("button").count() == 1
            assert field("count").input_value() == "1"
            assert field("count").locator('option[value="4"]').evaluate("option=>option.disabled")
            field("focus").select_option("-0.2")
            field("dose").select_option("0.9")
            assert field("measured").inner_text() == ("측정 불가" if language == "ko" else "Not measurable")
            assert field("bossung").locator("circle").count() == 7
            assert field("measurements").locator("tr").count() == 9
            assert field("measurements").text_content().count("—") == 2
            page.locator('[data-kind="space"]').click()
            assert field("bossung").locator("circle").count() == 9
            field("layer").select_option("67")
            field("focus").select_option("0")
            field("dose").select_option("1")
            assert field("measured").inner_text() == "199.44 nm"
            page.locator(".saved-table summary").click()
            decoded()
            if language == "en":
                assert not re.search("[가-힣]", root.inner_text())
            for width in (1440, 1024, 768, 390, 320):
                page.set_viewport_size({"width": width, "height": 1000})
                page.evaluate("() => new Promise(requestAnimationFrame)")
                view = page.evaluate("""() => ({width:innerWidth,
                    scroll:document.documentElement.scrollWidth,
                    chart:document.querySelector('[data-bossung] svg').getBoundingClientRect().width})""")
                assert view["scroll"] <= width + 1, (language, view)
                assert view["chart"] > 100
                views.append({"language": language, **view})
                if args.artifacts and width in (1440, 390):
                    field("selected-title").scroll_into_view_if_needed()
                    page.screenshot(path=str(args.artifacts / f"viewer-{language}-{width}.png"))
                    field("bossung").scroll_into_view_if_needed()
                    page.screenshot(path=str(args.artifacts / f"comparison-{language}-{width}.png"))
            page.set_viewport_size({"width": 1440, "height": 1000})
            # Restored explanations and both language routes remain available.
            for route, minimum_headings in (("/", 10), ("/method/", 9)):
                page.goto(f"{base}{prefix}{route}", wait_until="networkidle")
                assert page.locator(".page-content h2").count() >= minimum_headings
                assert page.locator('a[href$="/demo/#saved-results"]').count() > 0
                assert page.locator(".language-switch a").get_attribute("href") == (
                    urlsplit(base).path + ("/ko" if language == "en" else "") + route)

        # Readable representative figures survive absent JS or a failed data request.
        nojs = browser.new_context(java_script_enabled=False)
        static = nojs.new_page()
        static.goto(f"{base}/ko/demo/", wait_until="networkidle")
        static.locator(".saved-fallback summary").click()
        assert static.locator(".saved-fallback img:visible").count() == 2
        static.locator(".saved-fallback img").evaluate_all(
            "images=>Promise.all(images.map(i=>i.decode()))")
        assert static.locator("noscript").is_visible()
        page.route("**/viewer-data.json", lambda route: route.fulfill(status=503, body="Unavailable"))
        page.goto(f"{base}/demo/", wait_until="networkidle")
        page.wait_for_selector('[data-demo-viewer][data-state="error"]')
        assert field("viewer-content").is_hidden()
        page.locator(".saved-fallback summary").click()
        assert page.locator(".saved-fallback img:visible").count() == 2
        assert not errors, errors
        assert all(method == "GET" and urlsplit(url).netloc == origin and "/api/" not in url
                   for method, url in requests), requests
        browser.close()
    if args.artifacts:
        (args.artifacts / "saved-demo-results.json").write_text(json.dumps({
            "views": views, "requests": requests, "errors": errors
        }, indent=2))
    print("PASS: bilingual candidate selection, enlarged images, focus/dose records, missing values, "
          "charts, keyboard focus, responsive views, restored pages, fallbacks and no API requests")


if __name__ == "__main__":
    main()
