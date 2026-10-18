# Third-Party Notices and Asset Ownership — DysEpoch: David & Goliath

**Status:** Artwork ownership statement received October 17, 2026. Licence approved: Apache License 2.0 for code and documentation; artwork excluded. Items marked **OPEN** are still to be resolved before publication.

## 1. Project code and text

- Game code (`index.html`, `src/`), the dialogue text, and the codex commentary were written for this project.
- **Licence:** Apache License 2.0 (see `LICENSE`), covering the game code and documentation. Copyright 2026 Sheron Burton.
- **Copyright holder:** Sheron Burton.

## 2. Scripture

- Quotations are from the **King James Version** (1611), which is in the public domain.
- Quotations in the codex and in the S6 challenge are meant to be verbatim KJV text from 1 Samuel 17. OPEN — these must be re-checked against a KJV text before publication.
- Narrative text that paraphrases or expands the account is tagged **[Story]** and is not presented as Scripture.

## 3. Fonts

- The build uses system fonts only (Georgia, Segoe UI, and common fallbacks). No font files are bundled, and no external font service is loaded.

## 4. Software dependencies

- None. The game has no npm packages, build tools, or external scripts.
- The optional AI module (`src/js/ai-npc.js`) calls the Anthropic API only if it is enabled. It is not called in this build, and no API key is included.

## 5. Artwork

### 5.1 Covered files

- Character portraits: `assets/portraits/` — C1_player_soldier, C2_david, C3_goliath_close, C3_goliath_distant, C4_soldier_weary, C4_soldier_steadied, C5_eliab (7 PNG files, 400×600).
- Scene backgrounds: `assets/scenes/` — A1_vista_valley_afternoon, A2_camp_overview, A3_cookfire_vignette, A4_supply_tent_muster, A5_brook_quiet, A6_battleline_ravine, A7_completion_backdrop (7 PNG files).
- Icons: `favicon.ico`, `apple-touch-icon.png`.

### 5.2 Creation method

- All 14 game artworks (7 backgrounds and 7 portraits) were produced with Meta AI image generation, working from the project's approved P0 visual specifications and the Cinematic Realism style. They were not drawn by hand.
- Pixel-level corrections were made to the generated files with Python/PIL. These were the Phase 11 flame correction and the Phase 12 fog-band alpha corrections on the C4 soldier portraits.
- `favicon.ico` and `apple-touch-icon.png` were derived from the project's own approved artwork (the helmet mark).
- No stock imagery, third-party textures, photos, fonts, icons, or brushes are present in the artwork.

### 5.3 Originality and likeness

- The artwork is original to the DysEpoch project, created to its specifications. It does not copy any existing artwork or game asset.
- All portraits depict fictional characters (Israelite soldier, David, Goliath, and Eliab), created without reference to any real person, living or dead.

### 5.4 Tool terms

- Muse reports that it is not aware of any term of the image-generation tool that restricts the project owner's commercial use, public distribution, or competition entry use of these works.
- This is Muse's report. The project has not independently verified the tool's terms of service. OPEN — see §8.

### 5.5 Ownership and permitted uses

- Muse's written statement of October 17, 2026 records that all rights in the artwork listed in §5.1 are assigned to the project owner, Sheron Burton, for this competition and for public display in the competition repository, including the Devpost submission, demo video, and screenshots. See §7.
- Permitted uses stated in Muse's statement: competition submission, demo video, screenshots, and public display in this repository.
- The legal effect of that statement has not been reviewed. See §8.

### 5.6 Licence status of the artwork

- The artwork is **excluded from the Apache License 2.0** that covers the game code and documentation.
- Nothing in the LICENSE or NOTICE files grants any licence to the artwork.
- Ownership and permitted uses are as stated in §5.5 and §7, subject to the open items in §8.

### 5.7 Known artwork notes

- The steadied soldier portrait (C4_soldier_steadied) has a faint base fade on light backgrounds. Muse accepts this as the artwork's intended natural vignette fade and considers it final.
- The corrected C4 portrait files (fog-band alpha correction applied) were supplied on October 17, 2026. The integrated copies in this build were verified byte-identical in RGB to the corrected files.
- In-game visual confirmation of the fade on light backgrounds is **pending** the final build's visual inspection.

## 6. Competition use summary

- The artwork may be used in the Devpost submission, the demo video, the screenshots, and the public repository, subject to the open items in §8.

## 7. Artwork ownership statement

- **Artist/creator for the artwork:** Muse (Meta AI), creating at the direction of Sheron Burton, project owner.
- **Creation method and tools:** Meta AI image generation per project specifications; pixel-level corrections with Python/PIL; favicon derived from project artwork. No stock or third-party sources.
- **Tool or stock terms that permit commercial use and public display:** No stock content involved. Muse reports no known restriction on the project owner's commercial use, public distribution, or competition entry. Not independently verified (see §8).
- **Rights assigned or licensed to the project owner, for this competition and public display in this repository:** Muse's statement records an assignment of all rights to the project owner (see §5.5). Its legal effect is open (see §8).
- **Date of Muse's statement:** October 17, 2026. Recorded as received from Muse; it has not been reviewed as a legal instrument.

## 8. Open items before publication

- **OPEN — Legal effect of the assignment statement.** Muse's statement records an assignment of rights. Its legal effect has not been reviewed, and the statement is not treated as a verified legal instrument.
- **OPEN — Copyrightability of AI-generated artwork.** Whether the artwork can be owned or protected as copyright, and what that means for an "all rights" statement, needs legal review.
- **OPEN — Tool terms.** The image-generation tool's terms of service have not been independently verified for commercial use, public display, and competition entry.
- **OPEN — Competition rules.** Devpost's rules on third-party materials and repository licences have not been verified.
- **OPEN — In-game fade check.** Visual confirmation of the C4 base fade on light backgrounds in the final build.
- **OPEN — Scripture check.** KJV quotations are to be re-checked against a KJV text (§2).
- **OPEN — Devpost Skill Pack usage** (see scope.md, §7).
