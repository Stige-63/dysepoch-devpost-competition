"""Slice 4 mechanical verification: S6 Scripture and soldier reaction, S7 distant Goliath,
S8 reflection, player portrait in every scene.

Run from the game folder:  python3 tests/test_slice4.py
"""
from playwright.sync_api import sync_playwright

from helpers import clean_page, collect_lines, morale, overflow, play_to_s6, report, server

PORT = 8768
KJV_VERSE = "for the battle is the LORD's, and he will give you into our hands."
failures = []


def check(name, condition, detail=""):
    print(("PASS " if condition else "FAIL ") + name + (f" ({detail})" if detail and not condition else ""))
    if not condition:
        failures.append(name)


CASES = [
    # (hotspot, hotspot option, S5 option, expected morale, expected reaction text, label)
    ("cookfire", "listen", "stand", 45, "Did you hear? The battle is the Lord's", "steadied"),
    ("supply", None, "keep", -10, "Even the boy sees what we cannot", "discouraged"),
    ("cookfire", "quiet", "keep", 15, "A young shepherd. Either the bravest", "neutral"),
]

with server(PORT) as url, sync_playwright() as p:
    browser = p.chromium.launch()
    for vlabel, width in [("phone 390px", 390), ("desktop 1280px", 1280)]:
        for hotspot, h_opt, s5, expected_morale, reaction, tier in CASES:
            label = f"{vlabel} {hotspot}{'-' + h_opt if h_opt else ''}+{s5} ({tier})"
            page = clean_page(browser, width)
            play_to_s6(page, url, hotspot, h_opt, s5)
            check(f"[{label}] morale {expected_morale} at S6", morale(page) == expected_morale, f"got {morale(page)}")

            lines = collect_lines(page)
            check(f"[{label}] David's Scripture line is the KJV verse",
                  any(KJV_VERSE in line for line in lines))
            check(f"[{label}] the {tier} soldier line is shown",
                  any(reaction in line for line in lines))
            others = [r for r in ["Did you hear? The battle is the Lord's",
                                  "A young shepherd. Either the bravest",
                                  "Even the boy sees what we cannot"] if r != reaction]
            check(f"[{label}] other soldier lines are hidden",
                  not any(o in line for line in lines for o in others))
            check(f"[{label}] player portrait shown in S6",
                  page.get_attribute(".portrait[data-portrait='player']", "data-state") == "default")
            check(f"[{label}] soldier portrait shown in S6",
                  page.get_attribute(".portrait[data-portrait='soldier']", "data-state") == ("steadied" if expected_morale >= 20 else "weary"))

            # S6 -> S7: Goliath is distant.
            page.get_by_role("button", name="Witness David's courage").click()
            page.wait_for_selector("h2.scene-title:has-text('David Meets Goliath')")
            check(f"[{label}] S7 reached", True)
            check(f"[{label}] Goliath distant in S7",
                  page.get_attribute(".portrait[data-portrait='goliath']", "data-state") == "distant")
            check(f"[{label}] player portrait shown in S7",
                  page.get_attribute(".portrait[data-portrait='player']", "data-state") == "default")

            # S7 -> S8: reflection box keeps what is typed.
            lines = collect_lines(page)
            page.get_by_role("button", name="Take a moment to let this settle").click()
            page.wait_for_selector("h2.scene-title:has-text('Reflection')")
            collect_lines(page)
            check(f"[{label}] S8 reflection box shown", page.locator("textarea").count() == 1)
            page.locator("textarea").fill("Courage acts despite fear.")
            check(f"[{label}] reflection text kept while typing",
                  page.locator("textarea").input_value() == "Courage acts despite fear.")
            check(f"[{label}] player portrait shown in S8",
                  page.get_attribute(".portrait[data-portrait='player']", "data-state") == "default")

            # S8 -> S9
            page.get_by_role("button", name="Write a reflection").click()
            page.wait_for_selector("h2.scene-title:has-text('Aftermath')")
            check(f"[{label}] S9 reached", True)
            check(f"[{label}] no JavaScript errors", not page.errors, "; ".join(page.errors))
            check(f"[{label}] no failed requests", not page.bad, ", ".join(page.bad))
            check(f"[{label}] no horizontal scroll", overflow(page) <= 0)
            page.close()
    browser.close()

report(failures, "Slice 4")
