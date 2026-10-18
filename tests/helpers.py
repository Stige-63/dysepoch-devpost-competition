"""Shared helpers for the automated checks. Used by test_slice2.py onward."""
import subprocess
import sys
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path

GAME = Path(__file__).resolve().parent.parent

COOKFIRE = {"listen": "Listen to what the soldier", "encourage": "Tell the soldier you believe", "quiet": "Sit in silence"}
S5 = {"stand": "Stand your ground", "encourage": "Speak encouragement", "keep": "Keep your head down"}


@contextmanager
def server(port):
    """Serve the game folder on localhost:port for the length of a with-block."""
    proc = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
                            cwd=GAME, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"http://localhost:{port}/"
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(url, timeout=1)
                break
            except Exception:
                time.sleep(0.1)
        yield url
    finally:
        proc.terminate()


def morale(page):
    return int(page.inner_text(".statusbar").rsplit(":", 1)[1])


def advance(page):
    """Click Next until the choices appear."""
    while page.get_by_role("button", name="Next").count():
        page.get_by_role("button", name="Next").click()


def collect_lines(page):
    """Read every dialogue line of the current scene, in order, by pressing Next."""
    lines = []
    while True:
        lines.append(page.inner_text(".dialogue"))
        if page.get_by_role("button", name="Next").count() == 0:
            return lines
        page.get_by_role("button", name="Next").click()


def start(page, url):
    page.goto(url)
    page.get_by_role("button", name="Start Game").click()
    page.wait_for_selector("h2.scene-title")


def play_to_s6(page, url, hotspot, hotspot_option, s5_option):
    """From the menu, reach S6 by way of the chosen hotspot and battle-line choice."""
    start(page, url)
    advance(page)                                  # S1 lines
    page.get_by_role("button", name="Move through the camp").click()
    advance(page)                                  # S2 lines
    page.get_by_role("button", name="Head into the camp").click()
    page.wait_for_selector("h2.scene-title:has-text('Israelite Camp')")
    advance(page)                                  # S3 lines
    if hotspot == "cookfire":
        page.get_by_role("button", name="Sit by the cookfire").click()
        advance(page)                              # cookfire lines
        page.get_by_role("button", name=COOKFIRE[hotspot_option]).click()
    elif hotspot == "brook":
        page.get_by_role("button", name="Slip away to the quiet brook").click()
        advance(page)                              # brook lines
        page.get_by_role("button", name="Return to the camp with renewed").click()
    else:
        page.get_by_role("button", name="Head to the supply tent").click()
        advance(page)                              # supply tent lines
        page.get_by_role("button", name="Explain that you've brought").click()
    page.wait_for_selector("h2.scene-title:has-text('A Shepherd Arrives')")
    advance(page)                                  # S4 lines
    page.get_by_role("button", name="Come to the battle line").click()
    page.wait_for_selector("h2.scene-title:has-text('Goliath')")
    advance(page)                                  # S5 lines
    page.get_by_role("button", name=S5[s5_option]).click()
    page.wait_for_selector("h2.scene-title:has-text('After the Taunt')")


def finish_to_s9(page):
    """From S6, walk the rest of the story to the ending screen."""
    advance(page)
    page.get_by_role("button", name="Witness David's courage").click()
    page.wait_for_selector("h2.scene-title:has-text('David Meets Goliath')")
    advance(page)
    page.get_by_role("button", name="Take a moment to let this settle").click()
    page.wait_for_selector("h2.scene-title:has-text('Reflection')")
    advance(page)
    page.locator("textarea").fill("I learned that courage acts despite fear.")
    page.get_by_role("button", name="Write a reflection").click()
    page.wait_for_selector("h2.scene-title:has-text('Aftermath')")
    advance(page)


def clean_page(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 844})
    page.errors = []
    page.bad = []
    page.on("console", lambda m: page.errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: page.errors.append(str(e)))
    page.on("response", lambda r: page.bad.append(r.url) if r.status >= 400 else None)
    return page


def overflow(page):
    return page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")


def report(failures, label=""):
    print()
    if failures:
        print(f"{len(failures)} check(s) FAILED")
        sys.exit(1)
    print(f"All {label} checks passed")
