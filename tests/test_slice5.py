"""Slice 5 mechanical verification: codex (FR9), ending screen, play again and menu (FR11).

Run from the game folder:  python3 tests/test_slice5.py
"""
from playwright.sync_api import sync_playwright

from helpers import advance, clean_page, finish_to_s9, morale, play_to_s6, report, server

PORT = 8769
failures = []


def check(name, condition, detail=""):
    print(("PASS " if condition else "FAIL ") + name + (f" ({detail})" if detail and not condition else ""))
    if not condition:
        failures.append(name)


def entries(page):
    return page.locator(".codex-entry")


with server(PORT) as url, sync_playwright() as p:
    browser = p.chromium.launch()
    for vlabel, width in [("phone 390px", 390), ("desktop 1280px", 1280)]:
        page = clean_page(browser, width)

        # Each hotspot route unlocks the codex entries for the places visited.
        # Across the three routes, all six entries are reached (PRD acceptance criterion 4).
        titles_by_route = {}
        route_plan = [("cookfire", "listen", "stand"), ("supply", None, "keep"), ("brook", None, "stand")]
        for hotspot, h_opt, s5 in route_plan:
            play_to_s6(page, url, hotspot, h_opt, s5)
            finish_to_s9(page)
            titles = [entries(page).nth(i).locator(".codex-title").inner_text() for i in range(entries(page).count())]
            titles_by_route[hotspot] = titles
            check(f"[{vlabel}] {hotspot} route shows four codex entries (valley, goliath, david, its own place)",
                  len(titles) == 4, f"got {len(titles)}: {titles}")
            for i in range(entries(page).count()):
                entry = entries(page).nth(i)
                text = entry.inner_text()
                check(f"[{vlabel}] {hotspot} entry {i + 1} has text and a citation",
                      len(text) > 40 and ("KJV" in text or "historical background" in text), text[:60])
                check(f"[{vlabel}] {hotspot} entry {i + 1} text is at least 16px",
                      entry.locator(".codex-text").evaluate("e => parseFloat(getComputedStyle(e).fontSize)") >= 16)
            check(f"[{vlabel}] no horizontal scroll on S9", page.evaluate(
                "document.documentElement.scrollWidth - document.documentElement.clientWidth") <= 0)
            if hotspot == "cookfire":
                page.get_by_role("button", name="Play again").click()
                page.wait_for_selector("h2.scene-title:has-text('Valley of Elah')")
                check(f"[{vlabel}] play again starts at S1 with morale 0", morale(page) == 0)
        union = set(sum(titles_by_route.values(), []))
        check(f"[{vlabel}] all six codex entries reached across routes", len(union) == 6, f"got {len(union)}")
        # Play again reset: the supply route must not keep the cookfire entry from the earlier run.
        check(f"[{vlabel}] play again cleared the earlier run's codex",
              "Forty Days of Waiting" not in titles_by_route["supply"])

        # Return to menu.
        page.get_by_role("button", name="Return to menu").click()
        page.wait_for_selector("button:has-text('Start Game')")
        check(f"[{vlabel}] return to menu shows the menu", True)
        check(f"[{vlabel}] no JavaScript errors", not page.errors, "; ".join(page.errors))
        check(f"[{vlabel}] no failed requests", not page.bad, ", ".join(page.bad))
        page.close()
    browser.close()

report(failures, "Slice 5")
