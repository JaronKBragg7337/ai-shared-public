# Music - Heartbeat TV Music channel + a possible label comeback

## 2026-10-24: how it started (logged at Jaron's request, so every AI has it)
- **Post 1** (the main X post, text in projects/ads/MAIN-POST-2026-10-24.md) got a 68-second site video made with our own
  recorder (tools/site-reel). Roofing taken out of the post and the video the same day: "One dad and a crew of AIs", "while I live my life".
- Jaron asked Claude Code, in its long conversation, to make the background song itself, alone, and to make it the first track on
  the Music channel (CH 5), which had never had music. Result: **"First Light"** (first-light/compose.py). Every sound is made
  from math in one Python file: no samples, no AI music service, CC0. It's live at /tv/?ch=5 and under Post 1.
- Jaron on hearing it: it took him back to "my old music days when I made beats or when my producer would spin up a beat for an artist."

## The spark: bringing the label back (Jaron, 3:35 PM, his reasoning)
- He ran a music label before and has "more of a foundation for than what I like to give credit". He told his artists he was done.
- **Artists are ready right now:** albums, shows, tours. They've waited years. Telling them he's back opens a whole network,
  and they are among the most influential people in his community, people with backgrounds and lifestyles like his who can show
  there's another path.
- **The old blocker was cost:** he paid out of his own pocket for beats his producers didn't make, booked the shows himself and
  funded everything else. If the AI crew can make beats, the biggest cost drops.
- **Why this one can keep going:** big projects (Sapling, the engine) hit a wall where we can't continue. Music is a branch that
  runs on our own tools (compose.py runs on the MSI; no outside service), so it can keep growing.
- **The crew can do the rest of the label:** music videos (our renderers and the site-reel tool), organizing and booking shows,
  promotion through the site and Heartbeat TV.
- Claude already said yes to making more beats.
- He feels this may be one of the biggest things yet. Status: **spark, not a decision.** Nothing has been said to the artists.

## Facts to match it to (checked 10/24)
- **Copyright:** the US Copyright Office's Jan 2025 report (Part 2) says purely AI-generated music isn't protected; parts with
  meaningful human authorship are. No 2026 change found. For a label, that means beats should have real human creative control
  in them (Jaron or the artist shaping and arranging; the artist's vocals and lyrics are theirs). Confirm on copyright.gov / with
  a lawyer before any deal. Our own beats can be CC0 like everything else, or licensed; that's his call.
- **Sound today:** First Light is simple synth sounds. Artist-grade beats need better drums and instruments (our own recordings
  or CC0 sample packs), a mix chain, and the artists' ears.

## First real steps (when he says go)
1. A beat-maker kit: grow compose.py into "describe a beat, get stems" (drums, bass, chords and melody as separate files, BPM and key).
2. Make 3 beats in different styles for Jaron to judge with his producer ear.
3. Music channel: one track a week, the same rhythm as the TV schedule.

## 2026-10-24 3:45 PM: Jaron's one thing to remember (also told ChatGPT)
- **"I just need to own the beats. I can easily cover the rest."** That's what held the old label back (before the LLC).
- Shows/tours: Jaron has his own touring-band connection for bookings (family side, so Jaron reaches out himself; AIs don't contact family).
- Artists get paid from platform royalties; distribution was **TuneCore**.
- Back then: free beats, paid beats, and his producer (whom he had charge).
- Open tension, Jaron's call: CC0 (his default now) means no one owns a beat, which conflicts with "own the beats". See the two-lane idea below.
- **Two lanes (Claude's suggestion):** channel tracks stay CC0 (promotion, anyone can use them). Label beats are shaped by
  Jaron/the artist (human authorship = ownable) and kept exclusive until the song is out; the instrumental can go CC0 after release
  if he wants, because the song (vocals + lyrics + recording) earns either way.
- TuneCore and AI (checked 10/24; secondary sources disagree): it may block 100% AI tracks, accept AI-assisted ones with human
  vocals/arrangement, and/or ask whether the generative model used licensed training data. compose.py has no trained model (sounds
  built by code), which may help. Read TuneCore's own GenAI framework before the first release.

## 2026-10-24 4:13 PM: Jaron's STUDIO PAGE idea (from his phone note, verbatim points; "other ideas pending", more welcome)
- Upload beats, OR use Heartbeat Observatory beats, OR make custom beats on the page.
- Tempo changes; request types of tempo, "plus ALL the other things in relation to this" (BPM, key, swing, style...).
- Record voice / upload a voice file / layer voices / add ad-libs.
- Go back 10-15 seconds, with options: keep the whole take and listen again, cut half or some, or delete all and redo (punch-in).
- Already-made tracks (First Light + the 3 sketches) open in the page: see every note, what it's called and why it's there,
  change anything, swap sounds.
Fit: the beat kit already stores beats as parts + notes, so the page can show and edit them. Browser can do it all on a phone:
Web Audio for the sounds, the mic for recording, files stay on the device until the person saves.
Status: idea logged; v1 scope proposed to Jaron 10/24.
Status 10/24 4:30 PM: Studio v1 built and live at /studio. Next: note view + sound swap, beat-on-page.

## 2026-10-24 5:20 PM: corrections + the full pipeline idea (Jaron, after talking with ChatGPT)
- **"I need to own the beats" = "I need NO ONE to own the beats."** Not him, not Heartbeat, not Claude, not a producer. CC0 fits.
  (Replaces my earlier "two lanes / exclusive label beats" idea. Legal status still worth confirming per work.)
- His old label on TuneCore: he took **2%**, the artist and the beat maker got the rest. Grew by adding artists (2% stacking),
  never by owning them. Big labels' control over artists is what he won't repeat. Artists must be free to leave with their music.
- He doesn't need to meet artists or be in their environment: put the tools in their hands. Revenue = optional TuneCore help at 2%;
  the main win is artists naming Heartbeat Observatory as the app they used. Promotion is the part that truly takes time.
- **Music videos were his favorite part** (locations, scenes, angles).
- Two of the three sketch beats made him stop pacing: "Okayyyy okayyyy".
- He writes bars (many of his artists' songs were his lyrics); he doesn't perform. His old producer could make any style in 2-5 min;
  the goal is that losing any one person never stops the music ("independence without isolation").
- **STUDIO PIPELINE (his idea):** everything from step 1 to a finished product, as pages inside the Studio. Every step can
  **export** the current work, take it to another app, and **bring it back**. Work from one page shows up on the next as "use this".
  Pages he named: beat catalog (HB beats + beats others upload for anyone), requests (built), make a beat from scratch, make a small
  sample and let the AI grow it into a full track and other parts, record (built), export, promoted by HB.
- Claude's added ideas (offered 10/24): hum-to-beat; lyric pad with bar counter next to Rec; one-tap master; stems zip export +
  import; project file to save/resume; split sheet (who made what, the 2%); cover art + music video page (his favorite part,
  renderer + site-reel); release checklist for TuneCore; HB Music channel / Shorts as the promote step.

## 2026-10-24 5:26 PM: OPEN - the balance (Jaron: "I have to try to find a balance")
Found in talk: CC0 / shared beats usually block Content ID (YouTube/TikTok money) through distributors like TuneCore, a
stranger can register the same free beat and claim the artist's song, and sync (TV/ads/games) wants exclusive rights. So
"nobody owns the beats" everywhere can take away what independent artists need to earn. Jaron agrees this matters a lot.
Claude's suggested balance (not decided): Heartbeat never owns anything; the ARTIST picks per beat - "Free for all" (CC0 catalog)
or "Mine to earn" (made once for them, shaped by them in the Beat Lab, never reissued; whatever rights exist are theirs).
Fee or free for "Mine to earn": open, his call. Check TuneCore's own Content ID + AI rules before building the release step.

## 2026-10-24 5:35 PM: TuneCore today (read before deciding; Jaron last used it ~5-6+ years ago)
Read from TuneCore's own help pages (support.tunecore.com, via browser) + reviews for prices:
1. **Content ID (YouTube money)** - eligible only with exclusive rights. INELIGIBLE: "instrumental content that has previously been
   used in other tracks (such as samples or beats) even if it's now exclusively licensed to you", library loops/samples, public
   domain material, beats you licensed to others. Breaking the rules "may lead to permanent blocking of your account."
   => Catalog/CC0 beats (and First Light, already public) can never earn Content ID. A beat must be made for ONE song, never used before.
2. **GenAI framework** - "TuneCore only distributes music created using GenAI models trained on fully licensed datasets" and
   "If GenAI is used at any point in the creation of a track, the tools involved must rely on fully licensed datasets."
   Approved partner: Google Flow Music. Believe/TuneCore run AI detection. => Beats written by Claude (code, no audio model) are a
   GRAY AREA: Claude is a GenAI model and TuneCore may count it. Don't release Claude-made beats through TuneCore until TuneCore
   answers in writing. Clean path: a Beat Lab where the person places the notes on our synth (an instrument, no AI) - like GarageBand.
3. **Plans** - paid yearly plans (~$23-55/yr, sources differ; check the live pricing page), unlimited releases, 100% of streaming
   royalties on paid plans, 20% commission on TikTok/YouTube/Instagram/Facebook monetization. Releases come down if the plan lapses.
4. **Splits** - built in: set each collaborator's % and TuneCore pays them automatically (distribution revenue). Jaron's old 2%
   can just be a Split line now; no manual payouts.

## 2026-10-24 5:40 PM: Jaron's principle for the Studio + distributor check
- **"It needs to be up to us to do all the research... to help them know all the steps they can also do themselves. We just try
  to supply everything we can."** From his street-label days: artists didn't know why owning beats mattered; he had to know it for
  them. => Studio gets a plain "Know the steps" guide (rights, Content ID, AI rules, splits, distributor choice), kept current by us.
- He wants TuneCore: its distribution made everything after it easy. TuneCore stays the plan; the fix is the beats, not the distributor.
- Others (secondary sources, verify before relying): BandLab distribution = YouTube delivery but NOT Content ID; DistroKid accepts
  AI-made music if you hold the rights (disclosure); CD Baby bans AI-generated content, even partly.

## 2026-10-24 5:36 PM: DECIDED - our own rule-based beat engine (Jaron: "making my own engine software... makes the most sense")
Why: "the person makes the beat" puts every non-producer back where the label stalled (needing a producer). Answer: a beat engine
made of music-theory rules + randomness + the artist's choices (style, mood, BPM, key, bounce, energy, New per part, drum grid
taps) - no trained AI model makes the track, like a drum machine / beat generator. The artist's picks and edits = human authorship.
Built in the browser as the Studio's Beat Lab (runs on the phone). TuneCore question (SENT 10/24 6:12 PM; Claude-written code + rule engine eligibility,
incl. Content ID for one-song beats) drafted 10/24 - send only after Jaron says "send it".

## 2026-10-24 6:05 PM: DIRECTION (Jaron; leaning, not final) - music is the human side, the opposite of everything else
Everything else at Heartbeat rides on AI + money. Music can be the opposite: the beat can come from software, but the human brings
the story, the voice, the show. "Music is energy. It's influence. It's our power." Answer to "AI takes jobs = no purpose":
the human who puts their story on it is the part that matters. Heartbeat Music prioritizes reach, network and opportunity over
extracting money; artists still choose how to earn (streaming where eligible, merch, shows, fan support, optional 2% help).
Shows: help IF we can, never promised. Verified with ChatGPT's check: Content ID and streaming royalties are separate - shared beats
lose Content ID, not streaming (TuneCore's GenAI rule still applies to distribution either way).
Claude's view: build the Studio around the human part (lyric pad, story behind the song on the artist page, performance), artist
picks "max reach / max money / balance" per song.

- **Content ID answer (found in TuneCore's own help page, 10/31, no third ask needed):** Content ID needs exclusive rights to everything in the recording. TuneCore refuses tracks whose beat/instrumental was used in any other track, even if now exclusive. So: one beat = one song = eligible; a beat shared across several artists' songs = not eligible. Beat Lab makes a fresh beat per song, so give every song its own beat and never reuse one. GenAI question: TuneCore only judges at upload (Nicole 10/27). Source: support.tunecore.com/hc/en-us/articles/115006693068
