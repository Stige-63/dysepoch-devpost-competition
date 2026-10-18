"""Slice 1 mechanical verification: menu, S1, S2, Next, choices, file-open message.

Run from the game folder:  python3 tests/test_slice1.py
It starts its own local server on port 8765 and stops it when finished.
"""
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

GAME = Path(__file__).resolve().parent.parent
PORT = 8765
URL = f"http://localhost:{PORT}/"
failures = []


def check(name, condition, detail=""):
    print(("PASS " if condition else "FAIL ") + name + (f" ({detail})" if detail and not condition else ""))
    if not condition:
        failures.append(name)


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
            for width, label in [(390, "phone 390px"), (1280, "desktop 1280px")]:
                page = browser.new_page(viewport={"width": width, "height": 844})
                errors, bad_requests = [], []
                page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("response", lambda r: bad_requests.append(r.url) if r.status >= 400 else None)

                page.goto(URL)
                page.get_by_role("button", name="Start Game").wait_for()
                check(f"[{label}] menu shows Start Game", True)

                page.get_by_role("button", name="Start Game").click()
                page.wait_for_selector("h2.scene-title")
                check(f"[{label}] S1 title shown",
                      page.inner_text("h2.scene-title") == "Valley of Elah - The Standoff")
                check(f"[{label}] morale starts at 0",
                      "Soldier morale: 0" in page.inner_text(".statusbar"))

                # Three dialogue lines in S1: Next twice, then choices appear.
                for _ in range(2):
                    page.get_by_role("button", name="Next").click()
                check(f"[{label}] S1 last dialogue line reached with no Next",
                      page.get_by_role("button", name="Next").count() == 0)
                page.get_by_role("button", name="Move through the camp").click()

                page.wait_for_selector("h2.scene-title:has-text('Saul')")
                check(f"[{label}] S2 reached from S1 choice", True)
                for _ in range(1):
                    page.get_by_role("button", name="Next").click()
                page.get_by_role("button", name="Head into the camp").click()
                page.wait_for_selector("h2.scene-title:has-text('Israelite Camp')")
                check(f"[{label}] S3 reached from S2 choice", True)

                # Readability: dialogue and choice text at least 16px.
                dialogue_px = page.eval_on_selector(".dialogue", "e => parseFloat(getComputedStyle(e).fontSize)")
                check(f"[{label}] dialogue text >= 16px", dialogue_px >= 16, f"{dialogue_px}px")
                choice_px = page.eval_on_selector(".choice", "e => parseFloat(getComputedStyle(e).fontSize)")
                check(f"[{label}] choice text >= 16px", choice_px >= 16, f"{choice_px}px")

                # Layout: no horizontal page scroll.
                overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                check(f"[{label}] no horizontal scroll", overflow <= 0, f"{overflow}px overflow")

                check(f"[{label}] no JavaScript errors", not errors, "; ".join(errors))
                check(f"[{label}] no failed requests", not bad_requests, ", ".join(bad_requests))
                page.close()

            # Opening the file directly must show the server message, not a blank page.
            page = browser.new_page()
            page.goto((GAME / "index.html").as_uri())
            text = page.inner_text("#app")
            check("file:// opening shows the local-server notice", "python3 -m http.server 8000" in text)
            page.close()
            browser.close()
    finally:
        server.terminate()

    print()
    if failures:
        print(f"{len(failures)} check(s) FAILED")
        sys.exit(1)
    print("All Slice 1 checks passed")


if __name__ == "__main__":
    main()
