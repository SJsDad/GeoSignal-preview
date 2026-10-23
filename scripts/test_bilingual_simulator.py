"""Browser checks for language routing and the statically hosted 6f simulator.

Uses the same test-only Playwright dependency as test_technical_notes.py.
Example: python scripts/test_bilingual_simulator.py --url http://localhost:8000/GeoSignal-preview --chromium /usr/bin/chromium
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
        workers = []
        page.on("worker", lambda worker: workers.append(worker.url))

        def ready():
            page.wait_for_function("document.getElementById('results').getAttribute('aria-busy') === 'false'")

        def set_value(name, value):
            page.locator("#" + name).evaluate(
                '(e,v)=>{e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}));}', str(value))
            page.evaluate("() => new Promise(requestAnimationFrame)")

        for language, prefix in (("ko", "/ko"), ("en", "")):
            page.goto(f"{base}{prefix}/notes/diffraction-defocus/", wait_until="networkidle")
            assert page.locator(".study-figure").count() == 4
            assert page.locator("#interactive-demo .live-demo-button").get_attribute("href") == (
                urlsplit(base).path + prefix + "/simulator/")
            page.goto(f"{base}{prefix}/simulator/", wait_until="networkidle")
            ready()
            assert page.locator("html").get_attribute("lang") == language
            labels = page.locator("#simulator-strings").evaluate("e=>JSON.parse(e.textContent)")
            assert page.locator("h1").inner_text() == labels["title"]
            assert page.locator("#active-orders").inner_text() == "-1, 0, +1"
            assert page.locator("#ray-chart").get_attribute("data-geometry") == "thin-lens-6f"
            set_value("source_u", .3)
            assert page.locator("#ray-chart").get_attribute("data-transmitted") == "-1,0"
            assert page.locator("#ray-chart").get_attribute("data-blocked") == "1"
            page.locator('[data-preset="two"]').click()
            set_value("focus_um", .63)
            assert page.locator("#active-orders").inner_text() == "0, +1"
            assert page.locator("#contrast").inner_text() == "90.6%"
            assert "×2000" in page.locator("#defocus-description").inner_text()
            page.locator("#focus-detail summary").click()
            page.wait_for_function("document.getElementById('map-status').textContent === JSON.parse(document.getElementById('simulator-strings').textContent).mapReady")
            page.locator('[data-preset="even"]').click()
            page.locator("#advanced-controls summary").click()
            set_value("max_order", 0)
            assert page.locator("#truncation-warning").is_visible()
            assert page.locator("#contrast").inner_text() == "0.0%"
            set_value("max_order", 32)
            page.locator("#spectrum-detail summary").click()
            page.wait_for_function("document.querySelectorAll('#spectrum-body tr').length === 65")
            page.select_option("#phase_model", "angular")
            set_value("focus_um", .37)
            page.locator("#pitch_nm").fill("50")
            page.evaluate("() => new Promise(requestAnimationFrame)")
            assert page.locator("#error-message").inner_text() == labels["inputError"]
            page.locator('[data-preset="two"]').click()
            set_value("focus_um", .37)
            assert page.locator("#error-message").is_hidden()
            snapshot = page.locator("#simulator-controls").evaluate("f=>Object.fromEntries([...f.elements].filter(e=>e.name).map(e=>[e.name,e.value]))")
            contrast = page.locator("#contrast").inner_text()
            page.locator("#language-switch").click()
            ready()
            assert page.locator("html").get_attribute("lang") != language
            restored = page.locator("#simulator-controls").evaluate("f=>Object.fromEntries([...f.elements].filter(e=>e.name).map(e=>[e.name,e.value]))")
            assert restored == snapshot, (snapshot, restored)
            assert page.locator("#contrast").inner_text() == contrast
            page.locator("#language-switch").click()
            ready()
            assert page.locator("html").get_attribute("lang") == language
            for width in (1440, 768, 390, 320):
                page.set_viewport_size({"width": width, "height": 1000})
                page.evaluate("() => new Promise(requestAnimationFrame)")
                view = page.evaluate("""() => ({width: innerWidth, scroll: document.documentElement.scrollWidth,
                    ray: document.getElementById('ray-chart').getBoundingClientRect().top,
                    wave: document.getElementById('pupil-chart').getBoundingClientRect().top})""")
                assert view["scroll"] <= width + 1 and view["ray"] < view["wave"], view
                views.append({"language": language, **view})
                if args.artifacts and width in (1440, 390):
                    page.screenshot(path=str(args.artifacts / f"simulator-{language}-{width}.png"), full_page=True)
            # The current image/rays continue to update without server access.
            context.set_offline(True)
            set_value("source_u", .25)
            assert page.locator("#calculation-status").inner_text() == labels["liveStatus"]
            context.set_offline(False)
            page.set_viewport_size({"width": 1440, "height": 1000})
            page.goto(f"{base}{prefix}/release-notes/", wait_until="networkidle")
            assert page.locator('table a').filter(has_text="v0.11").count() == 1
            assert page.locator('table a').filter(has_text="v0.12").count() == 1
            page.goto(f"{base}{prefix}/release-notes/v0.12/", wait_until="networkidle")
            assert page.locator(".language-switch a").count() == 1

        # Invalid fragments are ignored instead of breaking startup.
        page.goto(f"{base}/simulator/#max_order=999&focus_um=NaN&phase_model=unknown&pitch_nm=0", wait_until="networkidle")
        ready()
        assert page.locator("#max_order").input_value() == "1"
        assert page.locator("#focus_um").input_value() == "0"
        assert page.locator("#error-message").is_hidden()

        # Full derivations must typeset in both languages, not just link correctly.
        for prefix in ("/ko", ""):
            for topic in ("abbe-imaging", "fourier-optics", "diffraction-defocus",
                          "foundations/hopkins-tcc-socs", "foundations/inverse-and-metrics"):
                page.goto(f"{base}{prefix}/notes/{topic}/", wait_until="networkidle")
                page.wait_for_function("document.querySelector('mjx-container')")
                page.evaluate("() => MathJax.startup.promise.then(() => true)")
                assert page.locator("mjx-merror").count() == 0, (prefix, topic)
                if not prefix:
                    assert not re.search("[가-힣]", page.locator(".technical-content").inner_text()), topic
        assert workers
        assert not errors, errors
        assert all(method == "GET" and urlsplit(url).netloc == origin
                   and "/api/" not in url for method, url in requests), requests
        browser.close()
    if args.artifacts:
        (args.artifacts / "bilingual-results.json").write_text(json.dumps({
            "views": views, "requests": requests, "workers": workers, "errors": errors
        }, indent=2))
    print("PASS: both simulator languages, matching note/demo links, presets, blocked rays, Worker maps, "
          "validation, preserved settings, mobile layouts, release links and no Render/API requests")


if __name__ == "__main__":
    main()
