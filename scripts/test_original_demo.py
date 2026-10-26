"""Compare restored Home, Demo and Method with the separately built Git original."""
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
    errors, failures, requests, results, matched = [], [], [], [], []
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
            for route in ("/", "/demo/", "/method/", "/demo-legacy/"):
                reference_route = route.replace("demo-legacy", "demo")
                page.goto(f"{reference}{prefix}{reference_route}", wait_until="networkidle")
                expected = canonical(page.locator("html").evaluate("e=>e.outerHTML"))
                page.goto(f"{url}{prefix}{route}", wait_until="networkidle")
                notice = page.locator("#home-6f-simulator")
                assert notice.count() == (1 if route == "/" else 0)
                if route == "/":
                    assert notice.locator("a").get_attribute("href") == f"/GeoSignal-preview{prefix}/simulator/"
                    if language == "ko":
                        assert notice.locator("h2").inner_text() == "6f 광선·파동 시뮬레이터"
                        assert notice.locator("p").inner_text() == (
                            "시뮬레이터 실행에서 광원→웨이퍼의 6f 광선 경로와 같은 회절 차수의 pupil·파동 결과를 함께 조작할 수 있습니다. "
                            "Pages에서 직접 실행되며 Render 서버 기동을 기다리지 않습니다. (v0.12 추가)")
                    else:
                        assert "Added in v0.12" in notice.inner_text()
                actual = canonical(page.locator("html").evaluate("""e=>{
                    const copy=e.cloneNode(true);copy.querySelector('#home-6f-simulator')?.remove();
                    return copy.outerHTML;
                }"""))
                assert actual == expected, f"Original page DOM was changed beyond the Home notice: {prefix}{route}"
                matched.append(prefix + route)
                page.locator(".page-content img").evaluate_all(
                    "images=>Promise.all(images.map(i=>{i.loading='eager';return i.decode();}))")
                if args.artifacts and route in ("/", "/method/"):
                    if route == "/":
                        notice.scroll_into_view_if_needed()
                    page.screenshot(path=str(args.artifacts / f"{language}-{'home' if route=='/' else 'method'}.png"))
            page.goto(f"{url}{prefix}/demo/", wait_until="networkidle")
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
            "original_dom_matches": matched
        }, indent=2))
    print("PASS: restored EN/KO Home, Demo and Method match the original Git build with only the "
          "requested Home notice; original iframe controls, scrolling, images and no API requests")


if __name__ == "__main__":
    main()
