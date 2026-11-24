# Kimi lane report

## Found wrong or missing
- Artists needed the business steps after recording: song vs master rights, beat and sample permission, split sheets, PRO/MLC/SoundExchange registration, distribution checks, and Content ID limits.
- Reused beats need special care: commercial use does not prove the exclusive rights required for Content ID.
- Outside my lane: Studio takes are lost when leaving the page, with no project-file save. Its mic uses `ScriptProcessorNode`, which is deprecated and can be less reliable than newer audio worklets. I did not change these; Codex owns `studio/index.html`.
- Guide and lyric-pad links still need to be added to Studio by Claude.

## Changed
- `studio/learn/index.html`: new phone-first "Know the steps" guide, printable release checklist, and 13 official source links checked 24 Oct 2026. Sources include the U.S. Copyright Office, ASCAP, BMI, The MLC, SoundExchange, TuneCore, and CD Baby.
- `studio/lyrics/index.html`: new lyric pad matching Studio's colors and type.
- `studio/lyrics/lyrics.js`: one-line-per-bar counts, estimated syllables, offline near-rhyme suggestions and insertion, bar navigation, localStorage autosave, two-tap clear, and real `.txt` export.

## Tested
- `node --check studio/lyrics/lyrics.js` passed.
- Served the real pages locally and drove headless Chrome through Chrome DevTools Protocol at a true 390 x 844 mobile viewport.
- Passed: no sideways scroll on either page; 3-bar/13-syllable fixture; current-bar count; save and reload; bar-click selection; rhyme search and insertion at the cursor; fresh downloaded text file contents; two-tap clear; all 8 guide sections and 13 dated source links; no browser JavaScript exceptions.
- Visually checked 390 px screenshots of both pages. Checked the lane for em dashes; none found.

## Not tested
- Real iPhone Safari, including its Files/download interface and private-browsing storage behavior.
- Studio mic recording or the other builders' lanes. Nothing was pushed or tested live.
