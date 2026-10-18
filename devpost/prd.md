---
doc: prd
status: approved
---

# Product Requirements: DysEpoch: David & Goliath (Prototype #1)

**Companion documents:** scope.md (what is in and out, approved), spec.md (to be written in Step 4).
**Basis:** the approved prototype PRD (latest approved GitHub main), carried forward as decided by the learner on October 17, 2026.

## Decisions Recorded (learner, October 17, 2026)
- The approved prototype PRD is the base. The player journey, FR1–FR11, NFR1–NFR6, acceptance criteria, and approved scope are preserved.
- The Cinematic Realism look is kept. Approved character portraits, backgrounds, and cinematic visual design are retained. No redesign.
- Text-size exception resolved (Option A): mobile choice buttons, secondary buttons, status-bar text, and footer text are raised to at least 16px. The layout must not overflow, clip, or break on desktop or mobile.

## 1. Problem
Historical and biblical learning is often delivered as text or quizzes. Students and young adults disengage. DysEpoch tests whether a short, choice-driven story can make the player feel present in a historical moment, with the facts and Scripture revealed through that experience.

## 2. Target player
- Adults and older teens who like short narrative games.
- Readers interested in the David and Goliath account, including people who have not studied it closely.
- Judges of the Build With AI: Basics competition, who need to see a working experience quickly.

## 3. Player experience
The target reaction is "I experienced this," not "I studied this."
Core loop: enter the era → receive the mission → explore the camp → make choices → experience consequences → witness the event → reflect → complete.

## 4. Scene flow
| Scene | Title (short) | Player action |
|---|---|---|
| S1 | Valley of Elah — The Standoff | Make the one choice to continue |
| S2 | The Camp — Saul's Orders | Make the one choice to continue |
| S3 | The Israelite Camp — Exploration | Choose a hotspot: cookfire, supply tent, or brook |
| S3.1 | The Cookfire | Choose: listen, encourage, or sit in silence |
| S3.2 | The Supply Tent | Make the one choice to return to the camp |
| S3.3 | The Brook | Make the one choice to return to the camp |
| S4 | The Camp — A Shepherd Arrives | Make the one choice to continue (David arrives with provisions) |
| S5 | The Battle Line — Goliath's Challenge | Choose: stand, encourage, or keep your head down |
| S6 | After the Taunt — A Young Shepherd's Faith | Make the one choice to continue |
| S7 | The Valley — David Meets Goliath | Make the one choice to continue (witness the encounter) |
| S8 | Reflection | Write a reflection, then continue |
| S9 | Aftermath — The Codex & Your Journey | Review codex entries; play again or return to menu |

## 5. Functional requirements
- **FR1** The player starts from a menu and begins at S1.
- **FR2** Each scene shows its title, description, scripted dialogue, and the portraits of the characters present.
- **FR3** Dialogue advances with a Next/Continue control.
- **FR4** Each choice applies its declared consequence, then moves to its next scene.
- **FR5** Soldier morale starts at 0 and changes by the declared amount for each choice:
  - Choosing the S3 cookfire hotspot adds +10.
  - S3 cookfire: listen +20, encourage +25, quiet +15.
  - S5: stand +15, encourage +25, keep head down −10.
- **FR6** The soldier portrait is the weary version below morale 20, and the steadied version at 20 or above.
- **FR7** The Goliath portrait is the close version in S5, and the distant version in S7.
- **FR8** The player portrait appears in every scene.
- **FR9** Six codex entries unlock during play and are shown in S9. Scripture quotations are verbatim KJV.
- **FR10** S8 shows a reflection prompt. The player may enter text and continue.
- **FR11** S9 offers "play again" and "menu."

## 6. Non-functional requirements
- **NFR1 Readability.** Narrative, codex, reflection, objective, choice, secondary-button, status-bar, and footer text is at least 16px (12pt) on desktop and mobile. This replaces the earlier open exceptions (15.2px and 14px).
- **NFR2 Layout.** No horizontal page scroll on a 390px-wide phone or a 1280px-wide desktop. No text overflow or clipping after the NFR1 size change.
- **NFR3 Reliability.** No JavaScript errors and no failed asset requests in any of the nine S3/S5 combinations.
- **NFR4 Offline behavior.** The game requires an HTTP server to load its local files but does not require external APIs, cloud services, or an internet connection when served locally. All gameplay dialogue is scripted.
- **NFR5 Duration.** A complete playthrough takes about 5–10 minutes.
- **NFR6 Compatibility.** Current desktop and mobile browsers, served over HTTP.

## 7. Acceptance criteria
1. All nine S3/S5 combinations reach S9 on desktop and on mobile.
2. Morale totals match FR5 in every combination.
3. All 19 choices lead to their declared next scene.
4. All six codex entries can be reached and read on desktop and mobile.
5. No overflow, clipping, or layout break in S1, S8, or S9 on either viewport, with all text at the NFR1 size.

## 8. Out of scope for this release
As decided in scope.md, "Explicitly Cut" and "Later": other mission sets or episodes, progress saving, and any change to the biblical outcome.

## 9. Open questions
- **Artwork reuse (OPEN).** The Cinematic Realism look depends on reusing the approved portraits and backgrounds. Their rights and the image tool's terms are not yet independently verified (see THIRD_PARTY_NOTICES.md, section 8). Reuse is permitted for the prototype build only after those are confirmed.
- **Devpost Skill Pack usage** is recorded in the learner profile and build log as it occurs, not assumed here.
- **Licence** for the new work is to be confirmed at the ship step.
