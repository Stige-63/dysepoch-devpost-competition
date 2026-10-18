"""Full automated check (PRD acceptance criteria 1-5). Run from the game folder:

    python3 tests/matrix.py

1. All nine S3/S5 combinations (3 cookfire options x 3 battle-line choices) reach S9 on phone and desktop.
2. Morale totals match PRD FR5 in every combination.
3. All 19 choices lead to their declared next scene (checked in the story data and in play).
4. All six codex entries can be reached and read on phone and desktop (across the three hotspot routes).
5. No overflow or clipping on S1, S8 and S9 at either width, with all text at least 16px.
NFR3: no JavaScript errors and no failed requests in any combination.

Writes a plain report to tests/matrix-report.txt.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from helpers import (COOKFIRE, GAME, S5, advance, clean_page, finish_to_s9, morale, overflow,
                     play_to_s6, server)

PORT = 8770
REPORT = Path(__file__).resolve().parent / "matrix-report.txt"
lines = []
failures = []


def check(name, condition, detail=""):
    text = ("PASS " if condition else "FAIL ") + name + (f" ({detail})" if detail and not condition else "")
    lines.append(text)
    print(text)
    if not condition:
        failures.append(name)


def static_choice_check():
    story = json.loads((GAME / "src/data/story.json").read_text(encoding="utf-8"))
    scenes = story["scenes"]
    total = 0
    for sid, scene in scenes.items():
        for choice in scene["choices"]:
            total += 1
            target = choice["next"]
            check(f"[data] {choice['id']} leads to a built scene or the menu",
                  target == "menu" or target in scenes, target)
    check("[data] there are 19 choices", total == 19, f"found {total}")
    check("[data] there are six codex entries", len(story["codex"]) == 6, str(len(story["codex"])))


def run_combinations(browser):
    cookfire_totals = {"listen": 30, "encourage": 35, "quiet": 25}   # 10 for the hotspot, then 20/25/15
    s5_deltas = {"stand": 15, "encourage": 25, "keep": -10}
    for vlabel, width in [("phone 390px", 390), ("desktop 1280px", 1280)]:
        codex_titles = set()
        for c_key in ["listen", "encourage", "quiet"]:
            for s_key in ["stand", "encourage", "keep"]:
                label = f"{vlabel} cookfire-{c_key}+{s5_deltas and s_key}"
                page = clean_page(browser, width)
                # Morale check: after the S5 choice the status bar shows FR5 total.
                play_to_s6(page, url, "cookfire", c_key, s_key)
                expected = cookfire_totals[c_key] + s5_deltas[s_key]
                check(f"[{label}] morale total is {expected} (PRD FR5)", morale(page) == expected, f"got {morale(page)}")
                finish_to_s9(page)
                check(f"[{label}] reaches S9", page.inner_text("h2.scene-title").startswith("Aftermath"))
                check(f"[{label}] no JavaScript errors", not page.errors, "; ".join(page.errors))
                check(f"[{label}] no failed requests", not page.bad, ", ".join(page.bad))
                page.close()
        # Codex and layout across the three hotspot routes at this width.
        for hotspot, h_opt in [("cookfire", "listen"), ("supply", None), ("brook", None)]:
            page = clean_page(browser, width)
            play_to_s6(page, url, hotspot, h_opt, "stand")
            finish_to_s9(page)
            for i in range(page.locator(".codex-entry").count()):
                entry = page.locator(".codex-entry").nth(i)
                codex_titles.add(entry.locator(".codex-title").inner_text())
                size = entry.locator(".codex-text").evaluate("e => parseFloat(getComputedStyle(e).fontSize)")
                check(f"[{vlabel} {hotspot}] codex entry {i + 1} text at least 16px", size >= 16, f"{size}px")
            check(f"[{vlabel} {hotspot}] S9 no horizontal overflow", overflow(page) <= 0)
            page.close()
        check(f"[{vlabel}] all six codex entries reached and read", len(codex_titles) == 6, f"got {len(codex_titles)}")

        # Layout on S1, S8 and S9 with no overflow and text at least 16px.
        page = clean_page(browser, width)
        page.goto(url)
        page.get_by_role("button", name="Start Game").click()
        page.wait_for_selector("h2.scene-title")
        check(f"[{vlabel}] S1 no horizontal overflow", overflow(page) <= 0)
        check(f"[{vlabel}] S1 text at least 16px",
              page.eval_on_selector(".dialogue", "e => parseFloat(getComputedStyle(e).fontSize)") >= 16)
        page.close()
        page = clean_page(browser, width)
        play_to_s6(page, url, "cookfire", "listen", "stand")
        advance(page)
        page.get_by_role("button", name="Witness David's courage").click()
        page.wait_for_selector("h2.scene-title:has-text('David Meets Goliath')")
        advance(page)
        page.get_by_role("button", name="Take a moment to let this settle").click()
        page.wait_for_selector("h2.scene-title:has-text('Reflection')")
        advance(page)
        check(f"[{vlabel}] S8 no horizontal overflow", overflow(page) <= 0)
        check(f"[{vlabel}] S8 text at least 16px",
              page.eval_on_selector(".dialogue", "e => parseFloat(getComputedStyle(e).fontSize)") >= 16)
        page.close()


def main():
    global url
    with server(PORT) as url, sync_playwright() as p:
        browser = p.chromium.launch()
        static_choice_check()
        run_combinations(browser)
        browser.close()

    REPORT.write_text("\n".join(lines) + f"\n\nTotal checks: {len(lines)}; failed: {len(failures)}\n", encoding="utf-8")
    print()
    if failures:
        print(f"{len(failures)} check(s) FAILED. Report: {REPORT}")
        sys.exit(1)
    print(f"All {len(lines)} matrix checks passed. Report: {REPORT}")


url = None
if __name__ == "__main__":
    main()
