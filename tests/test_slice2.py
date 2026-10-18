"""Slice 2 mechanical verification: camp hotspots, cookfire morale, S4 reached.

Run from the game folder:  python3 tests/test_slice2.py
Starts its own local server on port 8766 and stops it when finished.
Morale rule (PRD FR5): choosing the cookfire hotspot adds +10; then listen +20,
encourage +25, quiet +15. Supply tent and brook add 0.
"""
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

GAME = Path(__file__).resolve().parent.parent
PORT = 8766
URL = f"http://localhost:{PORT}/"
failures = []


def check(name, condition, detail=""):
    print(("PASS " if condition else "FAIL ") + name + (f" ({detail})" if detail and not condition else ""))
    if not condition:
        failures.append(name)


def morale(page):
    text = page.inner_text(".statusbar")
    return int(text.rsplit(":", 1)[1])


def go_to_s3(page):
    page.goto(URL)
    page.get_by_role("button", name="Start Game").click()
    page.wait_for_selector("h2.scene-title")
    for _ in range(2):
        page.get_by_role("button", name="Next").click()
    page.get_by_role("button", name="Move through the camp").click()
    page.get_by_role("button", name="Next").click()
    page.get_by_role("button", name="Head into the camp").click()
    page.wait_for_selector("h2.scene-title:has-text('Israelite Camp')")
    while page.get_by_role("button", name="Next").count():
        page.get_by_role("button", name="Next").click()


def run_path(page, label, hotspot_button, hotspot_title, option_button, expected_morale):
    go_to_s3(page)
    page.get_by_role("button", name=hotspot_button).click()
    page.wait_for_selector(f"h2.scene-title:has-text('{hotspot_title}')")
    if option_button is not None:
        check(f"[{label}] hotspot shows after S3 choice", True)
        # Cookfire opens with two lines; the others have a line or two. Advance to the choices.
        while page.get_by_role("button", name="Next").count():
            page.get_by_role("button", name="Next").click()
        check(f"[{label}] morale after choosing the hotspot", morale(page) == expected_morale["hotspot"],
              f"got {morale(page)}, expected {expected_morale['hotspot']}")
        page.get_by_role("button", name=option_button).click()
    else:
        while page.get_by_role("button", name="Next").count():
            page.get_by_role("button", name="Next").click()
        page.get_by_role("button", name=expected_morale["return_text"]).click()

    page.wait_for_selector("h2.scene-title:has-text('A Shepherd Arrives')")
    check(f"[{label}] S4 reached", True)
    total = morale(page)
    check(f"[{label}] morale at S4 is {expected_morale['total']}",
          total == expected_morale["total"], f"got {total}")


def main():
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
        cwd=GAME, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(URL, timeout=1)
                break
            except Exception:
                time.sleep(0.1)

        with sync_playwright() as p:
            browser = p.chromium.launch()
            for width, vlabel in [(390, "phone 390px"), (1280, "desktop 1280px")]:
                page = browser.new_page(viewport={"width": width, "height": 844})
                errors, bad = [], []
                page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("response", lambda r: bad.append(r.url) if r.status >= 400 else None)

                cookfire_cases = [
                    ("listen", "Listen to what the soldier", 20),
                    ("encourage", "Tell the soldier you believe", 25),
                    ("quiet", "Sit in silence", 15),
                ]
                for name, option, value in cookfire_cases:
                    run_path(page, f"{vlabel} cookfire-{name}", "Sit by the cookfire", "The Cookfire",
                             option, {"hotspot": 10, "total": 10 + value, "return_text": ""})

                run_path(page, f"{vlabel} supply", "Head to the supply tent", "The Supply Tent",
                         "Explain that you've brought", {"hotspot": 0, "total": 0, "return_text": ""})
                run_path(page, f"{vlabel} brook", "Slip away to the quiet brook", "The Brook",
                         None, {"total": 0, "return_text": "Return to the camp with renewed"})

                # Readability and layout on the S4 screen.
                dialogue_px = page.eval_on_selector(".dialogue", "e => parseFloat(getComputedStyle(e).fontSize)")
                check(f"[{vlabel}] dialogue text >= 16px", dialogue_px >= 16, f"{dialogue_px}px")
                status_px = page.eval_on_selector(".statusbar", "e => parseFloat(getComputedStyle(e).fontSize)")
                check(f"[{vlabel}] status bar text >= 16px", status_px >= 16, f"{status_px}px")
                overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                check(f"[{vlabel}] no horizontal scroll", overflow <= 0, f"{overflow}px")
                check(f"[{vlabel}] no JavaScript errors", not errors, "; ".join(errors))
                check(f"[{vlabel}] no failed requests", not bad, ", ".join(bad))
                page.close()
            browser.close()
    finally:
        server.terminate()

    print()
    if failures:
        print(f"{len(failures)} check(s) FAILED")
        sys.exit(1)
    print("All Slice 2 checks passed")


if __name__ == "__main__":
    main()
