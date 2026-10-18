---
doc: build-log
status: working
---

# Build Log (public: non-sensitive build record)

This log records each Step 5 build slice: what was built, how it was verified, and what came from the approved prototype.

## Slice 1: menu, scene engine, first two scenes (verified)

- **Built:** `dysepoch-david-goliath/` with `index.html`, `src/js/engine.js`, `src/js/state.js`, `src/css/main.css`, `src/data/story.json` (S1–S2), `tests/test_slice1.py`, and `README.md`.
- **New in this build:** the scene engine, state handling, stylesheet (16px minimum text), and the test.
- **Reused from the approved prototype:** the S1 and S2 scene text (`src/dialogue-tree.json`, prototype commit 54c94cd), used as approved. No Scripture is in these two scenes.
- **Placeholder:** the soldier portrait is a labelled placeholder. No artwork is copied (artwork is gated on rights checks).
- **Mechanical verification:** `python3 tests/test_slice1.py` passed all 23 checks on phone (390px) and desktop (1280px) widths: menu, S1 and S2 reached, Next and choices, morale at 0, dialogue and choice text at least 16px, no horizontal scroll, no JavaScript errors, no failed requests, and the local-server notice on direct file opening.
- **Known limit (by design, resolved in Slice 2):** the S2 choice led to a placeholder message until S3 was built.
- **Learner checkpoint:** none for Slice 1 (fast mode checkpoints are after Slice 3 and at final review).

## Slice 2: camp hotspots, cookfire morale, S4 reached (verified)

- **Built:** S3 (camp), S3.1 cookfire, S3.2 supply tent, S3.3 brook, and S4 in `src/data/story.json`. Test: `tests/test_slice2.py`.
- **Reused from the approved prototype:** the S3 and S4 scene text and the cookfire choice values. The morale values follow PRD FR5 (cookfire +10, then listen +20, encourage +25, quiet +15).
- **Mechanical verification:** `python3 tests/test_slice2.py` passed all checks at phone and desktop widths. Morale at S4 is 30, 35, or 25 for the three cookfire paths, and 0 for the supply and brook paths. Also checked: text at least 16px, no horizontal scroll, no JavaScript errors, no failed requests.
- **Regression:** `tests/test_slice1.py` still passes, with S2 now leading to S3.
- **Known limit (by design):** the S4 choice leads to S5, which is built in Slice 3.

## Slice 3: battle line, soldier portrait, Goliath close view (the kernel; verified)

- **Built:** S5 (the taunt) with stand, encourage, and keep-head-down choices; `src/js/portraits.js` (soldier steadied at 20 or above, weary below 20; Goliath close in S5); the engine now applies a morale change before checking the next scene, and re-renders the scene so the portrait shows the new morale. Test: `tests/test_slice3.py`.
- **Reused from the approved prototype:** the S5 text and choice values (FR5: stand +15, encourage +25, keep head down −10).
- **Mechanical verification:** `python3 tests/test_slice3.py` passed all checks at phone and desktop widths: all nine cookfire-by-S5 combinations (morale checked on screen, for example 45 for listen plus stand and 60 for encourage plus encourage), the soldier portrait state on screen after each choice, the boundary at 19 (weary) and 20 (steadied), Goliath close in S5, text at least 16px, no horizontal scroll, no JavaScript errors, no failed requests.
- **Regression:** `tests/test_slice1.py` and `tests/test_slice2.py` still pass.
- **Learner checkpoint:** an early feedback session on the kernel scene is planned here (fast mode). Results to be recorded when the learner reports.
- **Known limit (by design):** S5 choices lead to S6, built in Slice 4.

## Slice 4: encounter, Scripture scene, reflection (verified)

- **Built:** S6 (David's challenge with the Scripture verse, and the soldier's reaction by morale), S7 (David meets Goliath, Goliath distant), S8 (reflection box), the player portrait in every scene. Test: `tests/test_slice4.py`.
- **Scripture (S6):** the approved correction from commit 445b182 (confirmed by Sage): "for the battle is the LORD's, and he will give you into our hands." (1 Samuel 17:47, KJV). The text is used exactly as approved. The prototype's earlier paraphrase is not used. Note: the King James text prints LORD in small capitals; the approved text uses "LORD's" in ordinary type.
- **Known discrepancy:** the approved Muse video (45.6 seconds, captured from the prototype) shows the earlier paraphrase, "The battle is the LORD's, and he will give you into our hands." on the S6 screen. The video therefore does not show the approved S6 wording. Decision pending (see the Devpost technical facts file).
- **Reused from the approved prototype:** S6 to S9 scene text, soldier reaction lines by morale (steadied at 20 or above, neutral from −5 to 19, discouraged at −10 or below), the codex entries.
- **Verified:** 6 cases at phone and desktop: the morale range picks the correct soldier line, other lines stay hidden, Goliath distant in S7, reflection text kept while typing, no JavaScript errors, no failed requests, no horizontal scroll.

## Slice 5: codex and ending (verified)

- **Built:** codex unlocking as scenes are reached, the codex list on S9, "Play again" (resets morale and codex), "Return to menu". Test: `tests/test_slice5.py`.
- **Routing (decision, from the approved prototype):** each hotspot leads straight to S4, as in the prototype. A single run shows the codex entries for the places visited (4 per run). Across the three hotspot routes all six entries are reached (PRD acceptance criterion 4).
- **Verified:** the codex text and citations are readable at 16px or more, play again resets morale and the earlier run's codex, the menu returns, no errors.

## Slice 6: readable layout and full automated check (verified)

- **Built:** `tests/matrix.py`: all nine cookfire-by-battle-line combinations at phone and desktop widths, morale totals (PRD FR5), all 19 choices (data check), all six codex entries reached and readable, no overflow on S1, S8, and S9, text at least 16px, no JavaScript errors, no failed requests.
- **Result:** 133 of 133 checks passed. Report: `tests/matrix-report.txt`.

## Known gaps (documented, not in this build)

- The prototype's "after choice" soldier lines for the cookfire (S3.1) and battle line (S5) are not included in this build. The PRD functional requirements do not require them, and the morale rules and portraits are complete. They can be added in a later build if the CEO asks for them.
- Artwork is still placeholders. Slice 7 remains gated on the rights checks.


## Skill Pack usage record (factual, as of this build)

- Official Skill Pack installed from challengepost/learn-ai-basics (workspace commit 56d3c35).
- Planning steps run in the workspace and approved: 1-start (learner profile, kept private), 2-scope (45fb332), 3-prd (f20feb4), 4-spec (f47a060).
- 5-build: checklist drafted and approved (6847d0d, eb2d476); build mode fast; Slices 1 to 6 built and verified (ebda417, aa0f011, 5bd5b9f, ed64884); licence and notices added (8174555). The Final Review and the Code Tour and App Map are the learner's steps and are still open.
- 6-ship: not yet run; it waits for the 5-build wrap-up.
- The completed prototype (commit 445b182 on the existing repository) was built before the Skill Pack and is not claimed as Skill Pack work.
- Slice 7 (artwork) is not started; it is gated on rights checks.
