"""Slice 3 mechanical verification: battle line (S5), soldier portrait, Goliath close view.

Run from the game folder:  python3 tests/test_slice3.py
Starts its own local server on port 8767 and stops it when finished.
Morale (PRD FR5): cookfire totals 30 / 35 / 25 (listen / encourage / quiet),
then S5 stand +15, encourage +25, keep head down -10.
Portraits (PRD FR6, FR7): soldier steadied at 20 or above, weary below 20;
Goliath close in S5.
"""
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

GAME = Path(__file__).resolve().parent.parent
PORT = 8767
URL = f"http://localhost:{PORT}/"
failures = []


def check(name, condition, detail=""):
    print(("PASS " if condition else "FAIL ") + name + (f" ({detail})" if detail and not condition else ""))
    if not condition:
        failures.append(name)


def morale(page):
    return int(page.inner_text(".statusbar").rsplit(":", 1)[1])


def click_next_until_choices(page):
    while page.get_by_role("button", name="Next").count():
        page.get_by_role("button", name="Next").click()


def go_to_s5(page, cookfire_option):
    page.goto(URL)
    page.get_by_role("button", name="Start Game").click()
    page.wait_for_selector("h2.scene-title")
    click_next_until_choices(page)  # S1 has its own choice after the lines
    page.get_by_role("button", name="Move through the camp").click()
    click_next_until_choices(page)
    page.get_by_role("button", name="Head into the camp").click()
    page.wait_for_selector("h2.scene-title:has-text('Israelite Camp')")
    click_next_until_choices(page)
    page.get_by_role("button", name="Sit by the cookfire").click()
    click_next_until_choices(page)
    page.get_by_role("button", name=cookfire_option).click()
    page.wait_for_selector("h2.scene-title:has-text('A Shepherd Arrives')")
    click_next_until_choices(page)
    page.get_by_role("button", name="Come to the battle line").click()
    page.wait_for_selector("h2.scene-title:has-text('Goliath')")
    click_next_until_choices(page)


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

        cookfire = [("listen", "Listen to what the soldier", 30),
                    ("encourage", "Tell the soldier you believe", 35),
                    ("quiet", "Sit in silence", 25)]
        s5 = [("stand", "Stand your ground", 15),
              ("encourage", "Speak encouragement", 25),
              ("keep head down", "Keep your head down", -10)]

        with sync_playwright() as p:
            browser = p.chromium.launch()

            # Portrait boundary: exactly 19 is weary, exactly 20 is steadied.
            page = browser.new_page()
            page.goto(URL)
            bounds = page.evaluate(
                "import('/src/js/portraits.js').then(m => [m.soldierPortrait(19), m.soldierPortrait(20), m.soldierPortrait(-10), m.goliathPortrait('s5_the_taunt')])"
            )
            check("soldier at morale 19 is weary", bounds[0] == "weary", str(bounds))
            check("soldier at morale 20 is steadied", bounds[1] == "steadied", str(bounds))
            check("soldier at morale -10 is weary", bounds[2] == "weary", str(bounds))
            check("Goliath is close in S5", bounds[3] == "close", str(bounds))
            page.close()

            for vlabel, width in [("phone 390px", 390), ("desktop 1280px", 1280)]:
                for c_name, c_text, c_total in cookfire:
                    for s_name, s_text, s_delta in s5:
                        label = f"{vlabel} {c_name}+{s_name}"
                        page = browser.new_page(viewport={"width": width, "height": 844})
                        errors, bad = [], []
                        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                        page.on("pageerror", lambda e: errors.append(str(e)))
                        page.on("response", lambda r: bad.append(r.url) if r.status >= 400 else None)

                        go_to_s5(page, c_text)
                        check(f"[{label}] S5 reached", page.inner_text("h2.scene-title").startswith("The Battle Line"))
                        check(f"[{label}] Goliath close view shown",
                              page.get_attribute(".portrait[data-portrait='goliath']", "data-state") == "close")

                        page.get_by_role("button", name=s_text).click()
                        expected = c_total + s_delta
                        check(f"[{label}] morale is {expected}",
                              morale(page) == expected, f"got {morale(page)}")
                        # The soldier portrait on screen must match the morale shown after the choice.
                        shown = page.get_attribute(".portrait[data-portrait='soldier']", "data-state")
                        want = "steadied" if expected >= 20 else "weary"
                        check(f"[{label}] soldier portrait on screen is {want}",
                              shown == want, f"got {shown}")
                        page.wait_for_selector("h2.scene-title:has-text('After the Taunt')")
                        check(f"[{label}] S6 reached after the battle-line choice", True)

                        check(f"[{label}] no JavaScript errors", not errors, "; ".join(errors))
                        check(f"[{label}] no failed requests", not bad, ", ".join(bad))
                        page.close()

            # Layout on the battle line, phone width.
            page = browser.new_page(viewport={"width": 390, "height": 844})
            go_to_s5(page, "Listen to what the soldier")
            dialogue_px = page.eval_on_selector(".dialogue", "e => parseFloat(getComputedStyle(e).fontSize)")
            check("battle line dialogue >= 16px", dialogue_px >= 16, f"{dialogue_px}px")
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            check("battle line no horizontal scroll at 390px", overflow <= 0, f"{overflow}px")
            page.close()
            browser.close()
    finally:
        server.terminate()

    print()
    if failures:
        print(f"{len(failures)} check(s) FAILED")
        sys.exit(1)
    print("All Slice 3 checks passed")


if __name__ == "__main__":
    main()
