# Studio team round 1 (2026-10-24, Jaron: "let the team take a look - add more things, improve it, find what's wrong or missing")

The Studio is live at https://www.heartbeatobservatory.com/studio/ - a free music studio in the browser for artists on their PHONES:
pick or make a beat, record vocals over it, stack ad-libs, punch in fixes, save the song. Files (site repo):
- studio/index.html - the studio: beat list, recorder (Web Audio + ScriptProcessor mic), layers, timeline (overview + 30 s close-up),
  punch-in, undo, trim, headphone sync (latency), save WAV, beat requests (Supabase beat_requests, insert-only).
- studio/beatlab.js - Beat Lab: our OWN rule-based beat engine (music theory rules + seeded randomness, no AI model makes audio).
  Styles trap / boom bap / R&B, parts drums/bass/chords/melody, drum grid, sound chips, render offline, Use / Save WAV / Save parts.
- studio/beats/*.mp3 - ready-made beats.

Who it is for: Jaron ran a small street label years ago; artists couldn't afford beats and didn't know their rights. Goal: everything an
independent artist needs from step 1 to a finished song, free, on a phone, and they understand every step.

## Rules for every builder
- Work ONLY in your own worktree/branch (below). Commit there. Never push, never touch main, never change Vercel/Supabase/Cloudflare settings.
- Phone first: iPhone Safari is the real target (390 px wide, touch, iOS audio quirks). Everything must work at 390 px with no sideways scroll.
- No new paid services, no API keys, no trackers, no external audio/AI generation. Plain HTML/CSS/JS, no build step. CC0.
- Beats stay rule-based (our engine). Don't claim anything about streaming/distribution eligibility (we asked TuneCore; no answer yet).
- User-facing words: plain, short, no jargon, no em dashes.
- Keep every existing feature working. If you find a bug outside your files, write it in your report instead of editing.
- Finish with a report: C:\Users\lilli\AI-Shared\projects\music\studio-team\<your-name>.md = what you found wrong/missing (whole Studio),
  what you changed (file + why), what you tested and how, what is NOT tested (e.g. real iPhone mic). Keep it short.

## Lanes (each edits only its own files)
- Fable (ho-studio-fable, branch studio-fable): studio/beatlab.js. Make beats sound more like real records and more musical:
  mix, drum sounds, 808, arrangement, more styles if worth it (drill, lo-fi, afrobeats...), the Lab's looks and ease of use.
- Codex (ho-studio-codex, branch studio-codex): studio/index.html. The recording studio itself: bugs, iPhone Safari issues,
  timing, punch-in, timeline, mixing, saving/export, vocal sound (simple EQ/compression/reverb chain), anything missing for recording a real song.
- Kimi (ho-studio-kimi, branch studio-kimi): NEW files only under studio/learn/ and studio/lyrics/ (do not edit studio/index.html;
  Claude adds the links). (1) "Know the steps" guide for artists: copyright basics, owning your masters, split sheets, PROs/publishing,
  distribution, Content ID - researched from the official sources (US Copyright Office, distributors' own help pages), each with a
  dated link, plain words. (2) A lyric pad: write by bars, bar/syllable counter, simple rhyme helper that runs in the page, saves on the
  phone (localStorage), export as text. Match the Studio's look (copy its CSS variables).
