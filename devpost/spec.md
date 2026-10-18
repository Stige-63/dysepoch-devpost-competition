---
doc: spec
status: approved
---

# DysEpoch: David & Goliath (Prototype #1): Technical Spec

**Companion documents:** scope.md (approved), prd.md (approved, with the NFR4 clarification).
**Reference only:** the completed prototype (latest approved GitHub main). This build is a new implementation that follows the same product decisions; the prototype's code is read for reference, not copied wholesale.

## How This Works, In Plain Language
- **The page is the game.** One web page (`index.html`) loads a stylesheet for the look and a script for the game. The browser runs it. There is no install and no framework.
- **The story is data.** All dialogue, choices, morale changes, and codex entries live in one data file (`src/data/story.json`). The script reads it, so the story can be changed without changing the game logic.
- **The game is a state machine.** The game remembers which scene it's on and the soldier's morale. Each choice names its next scene and its morale change. Choosing a button applies the change and moves to the named scene. That is how choices control progression.
- **The local server is a delivery truck.** Browsers won't load the story data straight from the disk, so a tiny web server on your machine hands the files to the browser. It does nothing else. Opening `index.html` by double-clicking won't work for this reason.
- **Testing is an automated player.** A script opens the game in a real browser, clicks through every path, and checks each requirement in the PRD's acceptance criteria. If a check fails, the build is not done.
- **Public hosting is the same delivery truck on the internet.** Anyone can reach the files, so only the game files may be published. Private planning notes, learner profiles, and internal checklists stay out of any published folder.

Why this shape: the PRD needs one short, offline-capable, scripted experience. Plain files plus one data file is the smallest design that meets it and is easy to check.

## The Core Journey Through the System
1. The player opens the page → `index.html` loads → the script reads `story.json`.
2. The menu appears → Start Game sets the scene to S1 and morale to 0 (PRD FR1).
3. Each scene shows its title, description, dialogue, and portraits (FR2). Next advances dialogue (FR3).
4. A choice applies its morale change, then moves to its next scene (FR4, FR5).
5. The soldier portrait switches between weary and steadied at morale 20 (FR6). Goliath and player portraits follow the scene rules (FR7, FR8).
6. Codex entries unlock as scenes are reached and appear in S9 (FR9).
7. S8 takes a reflection entry and continues (FR10). S9 offers play again or menu (FR11).

PRD ref: `prd.md > 3. Player experience`, `prd.md > 4. Scene flow`, `prd.md > 5. Functional requirements`.

## Stack
- **HTML5, CSS3, and plain JavaScript (ES2020).** No framework, no build step, no package installs. Learner agreed (Question 1).
  - Docs: https://developer.mozilla.org/en-US/docs/Web/HTML, https://developer.mozilla.org/en-US/docs/Web/CSS, https://developer.mozilla.org/en-US/docs/Web/JavaScript
  - Rationale: the PRD needs one short scripted experience. Fewer moving parts means fewer things to break before the deadline. Accepted tradeoff: no component library; layout is written by hand.
- **Local HTTP server:** Python's built-in `python3 -m http.server`. Docs: https://docs.python.org/3/library/http.server.html
- **Automated testing:** Playwright for Python, driving Chromium. Docs: https://playwright.dev/python/docs/intro
  - Note: the test tool is needed only to verify the build. It is not part of the game.
- **Hosting (optional, Question 2 answer B):** static file hosting of a published copy of the game folder only. Platform to be chosen at the ship step (GitHub Pages is one option). Docs: https://docs.github.com/en/pages
  - Hosting does not require accounts, payment, or installation for players.

## Where It Runs and How Someone Tries It
- **Runtime:** any current desktop or mobile browser, served over HTTP. No internet connection is needed once served locally (PRD NFR4).
- **Local start:** from the game folder, run `python3 -m http.server 8000`, then open `http://localhost:8000`.
- **Recording for the video:** the same local start, then record the browser window.
- **Public link (after approval):** a published copy of the game folder at a public address. Only these may be published: `index.html`, `src/`, `assets/`, `LICENSE`, `NOTICE`, `README.md`, and `THIRD_PARTY_NOTICES.md`.
- **Submission requirements:** a short demo video and a public GitHub repository. Hosting is additional evidence and does not replace either.
- **Blocked until approved:** publishing the repository, publishing the artwork, and hosting any artwork. See Decisions and Open Issues.

PRD ref: `prd.md > 6. Non-functional requirements` (NFR4, NFR6).

## Look and Feel
- Cinematic Realism: the approved character portraits and scene backgrounds, displayed as they are. No redesign.
- Typography: a serif for narrative and headings (Georgia, with fallbacks) and a sans-serif for buttons and status text (Segoe UI, with fallbacks). System fonts only; no font files bundled.
- Palette: warm paper background, dark brown accent, cream cards. Colours follow the prototype's approved palette.
- Text: at least 16px for all narrative, codex, reflection, objective, choice, secondary-button, status-bar, and footer text on desktop and mobile (PRD NFR1).
- Constraint: the static stack can honour all of this with CSS. No animation library.

PRD ref: `prd.md > Decisions Recorded`, NFR1.

## Components

### Story data (`src/data/story.json`)
Scenes, dialogue lines, choices (each with its next scene and morale change), portrait rules, and codex entries. Every Scripture quotation is marked and checked against the King James Version.
PRD ref: `prd.md > 4. Scene flow`, FR4, FR5, FR9.

### Game state (`src/js/state.js`)
Holds the current scene, morale (starts at 0), codex entries unlocked, and reflection text. Provides a reset for play again.
PRD ref: FR1, FR5, FR9, FR11.

### Scene engine (`src/js/engine.js`)
Renders a scene's title, description, dialogue (with Next), portraits, and choices. Applies a chosen morale change and moves to the next scene. Handles the S3 hotspot return and the S8 reflection step.
PRD ref: FR2, FR3, FR4, FR8, FR10.

### Portrait rules (`src/js/portraits.js`)
Returns the weary or steadied soldier portrait by morale, and the close or distant Goliath portrait by scene.
PRD ref: FR6, FR7.

### Codex (`src/js/codex.js`)
Unlocks entries when their scene is reached and renders them in S9 with their citations.
PRD ref: FR9.

### Layout and styles (`src/css/main.css`)
Responsive layout for 390px phone and 1280px desktop. Minimum 16px text. No horizontal scroll.
PRD ref: NFR1, NFR2.

### Automated checks (`tests/`)
Plays the nine S3/S5 combinations on desktop and mobile, checks morale totals, all 19 choices, codex reachability, text size, and overflow. Writes a pass or fail report.
PRD ref: acceptance criteria 1–5, NFR3.

## Data Model
- **Story data:** read-only at runtime, loaded once on start.
- **Game state:** held in memory only. Refreshing the page returns to the menu. Progress is not saved (scope Explicitly Cut). For each piece: current scene (reset on play again), morale (reset to 0), codex unlocked (reset), reflection text (kept only for the current run).

## File Structure
```
dysepoch-david-goliath/              (new implementation folder)
├── index.html                       entry page
├── README.md                        how to run locally; what is in the repo
├── LICENSE                          Apache-2.0 (code and documentation)
├── NOTICE                           copyright and artwork exclusion
├── THIRD_PARTY_NOTICES.md           third-party and artwork status
├── src/
│   ├── css/main.css                 layout and styles
│   ├── data/story.json              dialogue, choices, codex
│   └── js/
│       ├── state.js                 game state
│       ├── engine.js                scene engine
│       ├── portraits.js             portrait rules
│       └── codex.js                 codex unlock and display
├── assets/                          approved portraits and backgrounds (reuse after rights check)
├── tests/                           automated player checks
├── devpost/                         learning workspace (NOT published)
└── .gitignore                       keeps devpost/learner-profile.md and secrets out of commits
```

## External Services and Dependencies
- None at runtime. No API keys, no external scripts, no fonts downloaded (PRD NFR4).
- Test tooling only: Playwright (Python) and Chromium. Not included in the published game.
- Optional hosting platform (to be chosen at ship). Keys: none.

## Important Failure Modes
- **Dialogue file does not load** (opened without a server) → the page shows a short message telling the player to start a local server, instead of a blank screen.
- **Portrait file missing** → a labelled placeholder with the character name, and the test run fails so it is caught before recording.
- **Text overflows on a small phone** → the layout wraps and scrolls inside the card, never horizontally on the page; the overflow check catches regressions.

## What Was Simplified and Why
- **No progress saving** instead of saved games — a single run is enough for the demonstration and matches the approved scope.
- **Static files and one data file** instead of a database or server logic — nothing in the PRD needs either, and it removes the most common ways a hackathon build breaks.
- **Scripted dialogue only** instead of AI-generated text — the PRD requires scripted dialogue and offline play (NFR4).

## Decisions and Open Issues
**Learner decisions (October 17, 2026):**
- Same technology as the approved prototype: plain HTML, CSS, and JavaScript; one data file for scripted dialogue; simple HTTP server.
- Reuse the approved Cinematic Realism portraits and backgrounds once their rights and permitted uses are verified.
- Hosting: also hosted online, so judges can click and play. No accounts, payment, or installation for players. The repository and video remain as submission evidence.

**Derived implementation decisions (for agreement):**
- The new build is a new implementation. The completed prototype is used as reference. Assets are copied only after the rights check.
- Tests are automated browser checks written in Python with Playwright.

**Learner uncertainty (Question 3), with what clarified it:**
- How approved requirements become code: explained above (requirement → scene data → engine → automated check).
- How dialogue and choices control progression: explained above (choices name the next scene and morale change; the engine follows them).
- How testing verifies requirements: explained above (automated player against the acceptance criteria).
- Local server vs public hosting: explained above (same files; local is only on your machine, hosting makes them public).
- Secure deployment: only the listed game files are published. The `devpost/` folder, learner profile, and internal notes are never copied to a published folder. Before any push, check that git history contains no private material.

**Open items (block publication, not the build):**
- **Artwork rights and tool terms (OPEN).** Reuse and hosting of the artwork must wait for verification (THIRD_PARTY_NOTICES.md section 8).
- **Public repository and hosting (OPEN).** Requires the rights checks and your explicit approval (Sheron).
- **S6 Scripture text.** The new build must use the verbatim KJV line (Sage's correction) and be checked against a KJV text.
- **Devpost Skill Pack usage.** Recorded as it actually occurs in each step.

## Publication Policy (decision, Step 4 correction)
- **Published with the repository:** the game files (`index.html`, `src/`, `assets/`, `tests/`), `README.md`, `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md`, and the non-sensitive Skill Pack evidence and planning documents required by the competition: `devpost/scope.md`, `devpost/prd.md`, `devpost/spec.md`, and their HTML review companions, plus `devpost/checklist.md` when it exists.
- **Never published:** `devpost/learner-profile.md` (personal learning context), any credentials or `.env` files, internal notes, and the prototype's private planning or Phase records.
- **Gated (not published yet):** the artwork in `assets/` and any online hosting of it. Both wait until the rights and tool-terms checks are resolved and approved.
- **Before any push:** check that the file list and git history contain nothing from the "never published" list.

## Reuse Register (decision, Step 4 correction)
| Component | Status | Source | Notes |
|---|---|---|---|
| Story content (nine scenes, 19 choices, morale values, codex text) | Reused, rechecked | Approved prototype data | Text as approved; S6 Scripture correction from GitHub main is preserved |
| Scene engine, state, portrait rules, codex display | Newly implemented | Written in this workspace | Prototype logic read for reference |
| Stylesheet | Newly implemented | Written in this workspace | Cinematic Realism look and 16px minimum text kept |
| Portraits and backgrounds | Reused, gated | Approved Muse artwork | Used only after rights and tool-terms checks |
| Automated tests | Newly implemented | Written in this workspace | Covers the PRD acceptance criteria |
| Documentation (scope, PRD, spec, README, notices) | Approved, carried forward | Prototype and Skill Pack steps | Skill Pack step records added as each step completes |
