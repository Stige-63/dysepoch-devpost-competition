# DysEpoch: David & Goliath

A short, choice-driven story set in the Valley of Elah. The player experiences the moment before David meets Goliath, makes choices that change the soldier's morale, and reads codex entries with Scripture and historical context.

## Run it locally

1. Open a terminal in this folder.
2. Run `python3 -m http.server 8000`.
3. Open `http://localhost:8000` in a browser.

Opening `index.html` by double-clicking does not work: the story loads from a file, and browsers block that without a server.

## Check it

From this folder, with Python and Playwright installed: `python3 tests/test_slice1.py`.

## Status

The complete story (scenes S1 to S9), the codex, and the automated checks in `tests/`. Run `tests/matrix.py` for the full check.

## License

Code and documentation: Apache License 2.0 (see `LICENSE`). Artwork is excluded from that licence and is documented in `THIRD_PARTY_NOTICES.md`. Copyright: Sheron Burton (see `NOTICE`).

## Artwork status

This build uses placeholder panels where the character portraits and scene backgrounds will appear. The Cinematic Realism artwork from the approved prototype is not included in this repository. Its permitted use has not been verified (see THIRD_PARTY_NOTICES.md), so it is not published here.

## Scripture

The S6 quotation is "for the battle is the LORD's, and he will give you into our hands." (1 Samuel 17:47, King James Version), taken from the approved correction in commit 445b182 of the prototype repository.
