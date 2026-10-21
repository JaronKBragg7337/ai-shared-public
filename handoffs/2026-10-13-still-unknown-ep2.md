# Still Unknown (CH 10) ep.2 "Coral Castle: one man, 1,100 tons" - 2026-10-13 (Claude Sonnet 5.5)

LIVE: heartbeatobservatory.com/tv/?ch=10 -> 10.2 (345 s = 5 min 45 s; vertical 9:16 same length, clears 61 s). Commit b02fe9a on main (pull --rebase clean).
tv_items row 656a8124-7644-471b-a93f-7d9dda772a5f (channel stillunknown, approved, sort 1, reviewed_by "house show").
CPU only (Pillow + numpy + ffmpeg libx264, Kokoro CPU). No GPU touched. Every image is drawn; no photographs.

## What shipped
Folder projects/still-unknown/ep2-coral-castle/: script.json (from mkscript.py), ep.py (= ep_head.py + ep_body.py, own renderer, same look as ep1: violet-black, cyan/rose/mint, Segoe Light, square tags), music.py, build.sh, SOURCES.md, FACTCHECK-codex-r1.md + FACTCHECK-codex.md (second pass), stills/.
Site: tv/stillunknown/stillunknown-ep2-coral-castle.mp4, -vertical.mp4, .jpg (poster).
Scenes: man, Agnes (as told, name disputed), 1923 site, the move, weights, the 1,100 total, the gate, our arithmetic check, tools, block and tackle worked example, lever, affidavits, his words, popular theories, ledger, "Not established. Not ruled out.", end card with sources.

## Findings worth knowing (all on screen + SOURCES.md)
- Primary source: 1984 National Register nomination form (scanned PDF; I OCR'd it). It gives NO total tonnage, lists pieces up to 30 tons, says Bob Biggers' truck, worked alone at night.
- The "9-ton" gate (81 x 92 x 21 in = 90.6 ft3) cannot weigh 9 tons even if solid aragonite (8.3 t); porous oolite ~5.4-5.8 t. Labelled OUR ARITHMETIC / NOT SETTLED. An engineer's 1950s book (C. A. Lake) gives different gate dimensions.
- 1,100 tons: castle website + Wikipedia (unattributed). Earliest number found: Lake, "over 1000 tons" (his own sums ~1,050 for walls + tower, plus furniture). First use of exactly 1,100 not found.
- Move date conflict: form 1937 vs obelisk "Moved in 1939" vs castle chronology (land clearing May 1939). Biggers hauled on a trailer; Ed loaded/unloaded (accounts).
- Brief said "one grainy photo of his tripod": not what I found - several photographs of tripods/hoists exist (Rock Gate Park, Florida Memory 328424); none shown here (rights unchecked).

## Codex fact-check
r1 (84 KB): said needs revision. Fixed: move chronology, Biggers' role, gate repair relabelled REPORTED (dropped July 23 date and 2005), "one finger" past tense, aragonite wording + metric aside removed, 180 ft rope claim (now 36 ft tackle rope / ~180 ft winch-handle travel), rockgatepark.com is independent (not the castle), sound levitation is not in the form, pamphlets do not state a weight-cancelling method, ledger "documented" narrowed, weights = form's published estimates.
r2: "Revised claims pass." Two UNSURE left: ledger "alone" (screen now says working alone is claimed; narration still says "alone") and s15 parity tone. Kept the required ending "Not established. Not ruled out." per channel rule.

## Verified / not verified
- Verified locally: both mp4s probe clean (h264/aac, 345.4 s), contact sheets of all 18 scenes in both orientations, frames pulled from the final mp4s.
- Verified live: both mp4s + poster return 206 on the live host; /tv/?ch=10 at 375 px: guide lists 10.1 and 10.2, 10.2 loads and plays (readyState 4, no error, 345 s), scrollWidth 375 (no sideways scroll).
- Not verified: watched end to end with sound; phone-speaker level; the exact 1,100 origin; Florida Memory c.1936 photo date (page 403); Live Science / Mental Floss only seen as snippets; the repair details (1984 vs 1986, crane size) are conflicting accounts, shown as such. Not posted to TikTok/YouTube/X.

## r3 (2026-10-13, coordinator request) - ledger re-voiced
Narration s16 now ends: "Unknown: exactly how the largest blocks were raised and set. That he worked alone is claimed." (matches screen). All voice lines re-generated (Kokoro), both cuts re-rendered CPU-only, same filenames. Now 347.2 s (5:47), h264/aac, 1920x1080 and 1080x1920. Commit 5a5352a on main; live Content-Length matches local (23,717,256 landscape / 23,594,519 vertical). Added to heartbeat-tv/POSTING-QUEUE.md as ready.

## Next thing (done in r3: the ledger fix)
Narration says "how he raised the largest blocks, alone" in the ledger; if re-voicing for TikTok/YouTube, change to "exactly how ... (working alone is claimed)" to match the screen. Then post the vertical cut.
