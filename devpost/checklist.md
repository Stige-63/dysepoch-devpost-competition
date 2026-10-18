---
doc: checklist
status: approved
---

# Build Checklist

Build mode: fast (chosen by the learner, October 17, 2026; checkpoints and verification as planned)

Repository status:
- Competition workspace (this folder, `main`): local only, no remote configured. Holds the Skill Pack work, the `devpost/` planning documents, and the new build. Latest commit 103cc7e.
- Prototype (`Stige-63/dysepoch-david-goliath-prototype`, `main`): live main is 445b182 per Sage. The local prototype copy is at 54c94cd and is not the same history. Its commits are not pushed from this session.
- S6 correction: the new build's S6 text must be copied from the approved correction on live main 445b182, then checked word for word against the KJV. The local prototype copy is not used as the source for S6.

Game folder: `dysepoch-david-goliath/` (inside this repository, per `spec.md > File Structure`). Run commands from that folder.

## Baseline and New Work

Reference only: the completed prototype (latest approved GitHub main, commit 445b182 per Sage's check). It is read for reference and is not copied wholesale.

**Already completed in the prototype (reused, not rebuilt in Step 5):**
- Story content: nine scenes, 19 choices, morale values, six codex entries, scripted dialogue. The S6 Scripture correction is preserved.
- Gameplay capture and the approved demonstration video. These are not changed or re-recorded.
- Planning documents (scope, PRD, spec) and the Apache-2.0 licence, NOTICE, README, and THIRD_PARTY_NOTICES, with the corrected legal disclosures.

**Genuinely new in Step 5 (the Skill Pack build):**
- The Skill Pack build of the game in `dysepoch-david-goliath/`: state, engine, portraits, codex, and story data written in this repository.
- The 16px readability correction (NFR1) and the no-overflow layout check (NFR2), verified by tests.
- Automated browser testing of the nine S3/S5 combinations on two viewports (`tests/`).
- Deployment preparation for Step 6: a published-files list and a privacy check of the history before any push.

**Not in Step 5, and gated:**
- Artwork reuse and any hosting of artwork: wait for the rights and tool-terms checks.
- Public repository and Devpost submission: wait for the CEO's declarations and approval.

## Slices

- [x] **1. The menu starts Scene 1 and the player can advance dialogue**
  Becomes usable: Opening the page shows a menu. Start Game shows S1 with its title, dialogue, Next, and one choice that continues into S2.
  Why now: Proves the full path (page, data file, state, render) with the smallest real story, so the scene engine exists before any content depends on it.
  PRD ref: `prd.md > 5. Functional requirements` (FR1–FR4)
  Spec ref: `spec.md > Components`, `spec.md > File Structure`, `spec.md > Look and Feel`
  Build: Create the folder structure from the spec. Write `index.html`, `src/js/state.js`, `src/js/engine.js`, `src/css/main.css`, and `src/data/story.json` (S1–S2 only). If `story.json` fails to load, show the "start a local server" message from the failure modes. Portraits use a labelled placeholder until the rights check clears; no artwork is copied yet.
  Verify (mechanical): From the game folder, run `python3 -m http.server 8000`. A Playwright script opens the page, clicks Start, advances the dialogue, and continues to S2 with zero console errors and zero failed requests. Opening `index.html` directly shows the server message, not a blank screen.
  Learner check: Start the game, read S1 and S2, and say whether the dialogue flow feels right.
  Commit: `Add menu, scene engine, and first two scenes`

- [x] **2. Camp hotspots and cookfire morale**
  Becomes usable: The player explores S3 (cookfire, supply tent, brook), cookfire choices change morale, and every hotspot returns to camp. S4 is reached.
  Why now: Morale runs through the whole story. Adding it now lets later scenes check it instead of being retrofitted.
  PRD ref: `prd.md > 4. Scene flow` (S3–S4), FR4, FR5 (cookfire +10; listen +20, encourage +25, quiet +15)
  Spec ref: `spec.md > Components > Game state`, `spec.md > Components > Scene engine`
  Build: Add S3, S3.1–S3.3, and S4 to `story.json` with their declared morale values. Add hotspot return logic to `engine.js`. Start morale at 0 in `state.js`. Show morale in the status bar at 16px or larger.
  Verify (mechanical): Playwright enters the cookfire, picks each of listen, encourage, and quiet, and confirms morale equals 10 plus the choice value in each case. Confirm the supply tent and brook return to camp with morale unchanged.
  Learner check: Visit all three hotspots, watch the morale number, and say whether the cookfire choices feel like they matter.
  Commit: `Add camp hotspots and morale tracking`

- [x] **3. Battle line choices, soldier portrait, and Goliath close view (the kernel)**
  Becomes usable: S5 offers stand, encourage, or keep your head down. Each changes morale. The soldier portrait switches to steadied at 20 or above. Goliath appears close.
  Why now: This scene carries the unique kernel, choosing to act faithfully despite fear. Building it early lets the learner judge it before the rest of the story exists.
  PRD ref: `prd.md > 3. Player experience`, FR5 (S5: stand +15, encourage +25, keep head down −10), FR6, FR7 (close Goliath in S5)
  Spec ref: `spec.md > Components > Portrait rules`, `spec.md > How This Works, In Plain Language`
  Build: Add S5 to `story.json`. Write `src/js/portraits.js` with the soldier rule (weary below 20, steadied at 20 or above) and the Goliath close rule. Apply the S5 morale values.
  Verify (mechanical): Playwright reaches S5 from each of the three cookfire outcomes, tries all three S5 choices, and confirms morale totals. It also checks the portrait at morale 19 (weary) and 20 (steadied) at the boundary.
  Learner check: Play to S5 with different choices, then say whether the soldier's change reads clearly.
  Commit: `Add battle line choices, morale portraits, and Goliath close view`

- [x] **4. The encounter, the Scripture scene, and reflection**
  Becomes usable: S6 (Scripture scene), S7 (Goliath distant), and S8 (reflection) all work. The player portrait appears in every scene.
  PRD ref: FR7 (distant Goliath in S7), FR8, FR10, `prd.md > 4. Scene flow` (S6–S8)
  Spec ref: `spec.md > Components > Story data`, `spec.md > Components > Scene engine`
  Build: Add S6–S8 to `story.json`. Every S6 quotation must match the approved wording from GitHub main (Sage's S6 correction, verbatim KJV). Check it word for word against a KJV text before committing. Add the S8 reflection input, kept in memory only. Show the player portrait in every scene.
  Verify (mechanical): Playwright reaches S8, enters a reflection, and continues. The test compares the S6 quotation with the KJV string it stores. It confirms the distant Goliath in S7.
  Learner check: Read S6 and S8 and say whether the reflection step feels natural.
  Commit: `Add encounter, Scripture scene, and reflection`

- [x] **5. Codex and the ending**
  Becomes usable: Six codex entries unlock as their scenes are reached. S9 shows them, with "play again" and "menu" buttons.
  PRD ref: FR9 (six entries, verbatim KJV, narrative marked [Story]), FR11, `prd.md > 3. Player experience`
  Spec ref: `spec.md > Components > Codex`, `spec.md > Components > Game state`
  Build: Add six codex entries to `story.json`. Write `src/js/codex.js` to unlock and render them. Build S9. "Play again" resets state (morale 0, no codex). "Menu" returns to the menu.
  Verify (mechanical): Playwright reaches S9 and confirms six entries show. "Play again" returns to S1 with morale 0 and an empty codex. "Menu" returns to the menu. Every codex entry is read back and checked for text.
  Learner check: Finish a run, read the codex on S9, press play again, and say whether the ending feels earned.
  Commit: `Add codex entries and ending screen`

- [x] **6. Readable layout and the full automated check**
  Becomes usable: At 390px (phone) and 1280px (desktop), text is at least 16px, nothing overflows or scrolls sideways, and all nine S3/S5 combinations pass the automated checks.
  PRD ref: NFR1, NFR2, NFR3, acceptance criteria 1–5
  Spec ref: `spec.md > Components > Layout and styles`, `spec.md > Components > Automated checks`, `spec.md > Look and Feel`
  Build: Apply the Cinematic Realism styling in `main.css` (serif for narrative, sans-serif for controls, 16px minimum for every listed element). Write `tests/matrix.py` to run the nine combinations on both viewports and check the acceptance criteria. Save a pass/fail report.
  Verify (mechanical): Run `python3 tests/matrix.py`. Every check passes with zero JavaScript errors and zero failed requests. The report is saved.
  Learner check: Open the game in a phone-sized window and on desktop. Say whether the text is easy to read and nothing is cut off.
  Commit: `Add responsive styling and automated matrix tests`

- [ ] **7. Approved artwork (gated)**
  Becomes usable: Approved portraits and backgrounds replace the placeholders.
  Why now: Last, because it waits on the rights checks. The game is complete without it.
  PRD ref: `prd.md > 9. Open questions` (artwork reuse, OPEN)
  Spec ref: `spec.md > Publication Policy`, `spec.md > Reuse Register`
  Build: Copy assets into `assets/` only after the rights and tool-terms checks are approved in writing. Record the source of each file.
  Verify (mechanical): The matrix still passes. No failed asset requests. Every asset appears in the reuse register.
  Learner check: Play one run and say whether the artwork appears where expected.
  Commit: `Add approved portraits and backgrounds after rights check`

## Hands-on Checkpoints

- [ ] Early usable behavior explored: after slice 3, the kernel scene, shared with the learner for feedback
- [ ] Final kick-the-tires exploration and feedback completed

## Final Review

- [ ] Final review complete: feedback resolved and learner confirms ready to ship

## Code Tour and App Map

- [ ] Learning activity complete: guided route, focused alternative, prior practice connected, or brief recap
- [ ] Optional edit and transfer reflection addressed: offered, declined, already covered, or not applicable
- [ ] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: not started
Route and stops: not started
Edit outcome: not started
Reflection: not started
Activity mode: not started

## Revisions

