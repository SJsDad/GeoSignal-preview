"""Compare the archived Demo with a separately built original Git revision."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright


def canonical(html):
    html = html.replace("/assets/demo/original-v0.11/assets/", "/assets/")
    html = html.replace("/demo-legacy/", "/demo/")
    return re.sub(r' hreflang="(?:en|ko)"', "", html)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--reference-url", required=True)
    parser.add_argument("--chromium")
    parser.add_argument("--artifacts", type=Path)
    args = parser.parse_args()
    if args.artifacts:
        args.artifacts.mkdir(parents=True, exist_ok=True)
    url, reference = args.url.rstrip("/"), args.reference_url.rstrip("/")
    origins = {urlsplit(url).netloc, urlsplit(reference).netloc}
    errors, failures, requests, results = [], [], [], []
    with sync_playwright() as playwright:
        launch = {"headless": True}
        if args.chromium:
            launch["executable_path"] = args.chromium
        browser = playwright.chromium.launch(**launch)
        context = browser.new_context(viewport={"width": 1440, "height": 1100})
        context.route("**/*", lambda route: route.continue_()
                      if urlsplit(route.request.url).netloc in origins else route.abort())
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("response", lambda response: failures.append(response.url) if response.status >= 400 else None)
        page.on("request", lambda request: requests.append((request.method, request.url)))
        for language, prefix in (("en", ""), ("ko", "/ko")):
            page.goto(f"{reference}{prefix}/demo/", wait_until="networkidle")
            expected = canonical(page.locator("html").evaluate("e=>e.outerHTML"))
            page.goto(f"{url}{prefix}/demo-legacy/", wait_until="networkidle")
            actual = canonical(page.locator("html").evaluate("e=>e.outerHTML"))
            assert actual == expected, f"The {language} original Demo DOM was changed"
            assert page.locator("html").get_attribute("lang") == language
            assert page.locator(".page-content h2").count() >= 5
            assert page.locator(".page-content img").count() == 11
            iframe = page.locator("iframe")
            assert iframe.get_attribute("height") == "850"
            iframe.scroll_into_view_if_needed()
            frame = page.frames[1]
            frame.wait_for_selector("#cards .card")
            assert frame.locator("#cards .card").count() == 6
            assert frame.locator("#analysis-form").is_visible()
            assert frame.locator(".result-panel").is_visible()
            assert frame.locator('input[type="file"]').is_disabled()
            frame.select_option("#candidate-count", "4")
            assert frame.locator("#cards .card").count() == 4
            frame.select_option("#candidate-count", "8")
            assert frame.locator("#cards .card").count() == 6
            assert "8 requested" in frame.locator("#count-label").inner_text()
            frame.locator('#cards [data-index="1"]').click()
            assert "WIDTH_0002" in frame.locator("#selected-title").inner_text()
            frame.locator("#pw summary").click()
            assert "Not calculated" in frame.locator("#pw-content").inner_text()
            frame.locator("#space-tab").click()
            assert "SPACE_0001" in frame.locator("#selected-title").inner_text()
            frame.locator("#pw-content img").evaluate("i=>i.decode()")
            assert frame.locator("#pw-content circle").count() == 9
            for width in (1440, 390, 320):
                page.set_viewport_size({"width": width, "height": 1100})
                frame.evaluate("scrollTo(0,0)")
                iframe.scroll_into_view_if_needed()
                data = page.evaluate("() => ({width:innerWidth,scroll:document.documentElement.scrollWidth})")
                data["frame_scrolls"] = frame.evaluate("document.documentElement.scrollHeight>innerHeight")
                assert data["frame_scrolls"]
                results.append({"language": language, **data})
                if args.artifacts and width in (1440, 390):
                    page.screenshot(path=str(args.artifacts / f"original-{language}-{width}.png"))
            page.set_viewport_size({"width": 1440, "height": 1100})
            # The original page's static galleries and both optional comparisons load too.
            page.locator(".page-content details summary").evaluate_all("nodes=>nodes.forEach(n=>n.click())")
            page.locator(".page-content img").evaluate_all(
                "images=>Promise.all(images.map(i=>{i.loading='eager';return i.decode();}))")
        assert not errors, errors
        assert not failures, failures
        assert all(method == "GET" and urlsplit(target).netloc in origins
                   and "/api/" not in target for method, target in requests)
        browser.close()
    if args.artifacts:
        (args.artifacts / "original-demo-results.json").write_text(json.dumps({
            "views": results, "errors": errors, "failures": failures,
            "original_dom_matches": ["en", "ko"]
        }, indent=2))
    print("PASS: complete EN/KO DOM equals the original Git build after URL normalization; "
          "original iframe controls, scrolling, images, nine-condition results and no API requests")


if __name__ == "__main__":
    main()
