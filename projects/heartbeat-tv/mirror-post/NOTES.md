# Mirror post video: notes (Fable 5.2, 12 Nov 2026)

## What is here

| File | What it is |
| --- | --- |
| `mirror-post-vertical.mp4` | 1080x1920, 30 fps, 47 s, sound |
| `mirror-post-wide.mp4` | 1920x1080, 30 fps, 47 s, same cut, laid out for wide |
| `contact-sheet.png` | 6 frames pulled from the finished vertical file |
| `build/` | everything needed to rebuild it (scripts, the person file, the render passes) |

Nothing was posted anywhere.

## The cut (same in both versions)

| Time | What happens |
| --- | --- |
| 0:00 to 0:03 | His line from the post: "People say we might only have so many years before AI turns on us." A heartbeat trace starts along the bottom. |
| 0:03 to 0:14 | Four quote cards, one at a time, each landing on a heartbeat: Hinton, Amodei, Musk, Bengio. Name, role, the number in gold, their words, the source in small print. |
| 0:14 to 0:22 | The numbers come faster: 32 arrivals in 8.6 s. The first five land where each can be read, then they collide and pile up. The heartbeat climbs from about 75 to about 200 beats a minute with a rising low tone. |
| 0:22 to 0:23 | Hard cut to black and silence. |
| 0:23 to 0:32 | His line fades in, one phrase at a time, "in your own image," in gold. Slow heartbeat. |
| 0:32 to 0:47 | The mirror. A person looks into a brass-framed mirror. Gold lines spread out from between the reflection's eyes, the skin gives way to dark metal, and the reflection is the same face as a machine. Then "Become what you want your AI to become." and, small, Heartbeat Observatory. |

It reads with the sound off (every word is on screen), which matters because X autoplays muted.

## How it was made

- **Cards, numbers, text:** Python + Pillow, drawn at double size and scaled down, in the house look from `tv-lib` (dark navy, gold numbers, Georgia serif). `build/mirror_video.py`.
- **Sound:** all synthesized in the same script with numpy. Heartbeat, a tick per arriving number, the rising tone, a soft chord that goes from minor to major on the closing words. No downloaded music or samples. The heartbeat has a mid-range knock added so it is still heard on a phone speaker (about half its energy is above 200 Hz).
- **Mirror shot:** Blender 5.1, Cycles, on the MSI's GPU. `build/make_person.py` and `build/scene.py`.
  - The person is generated, not stock and not a real individual: the MakeHuman generator (MPFB 2.0.18 add-on) with its CC0 asset pack, an even mix of its three ancestry sliders, short hair grown as real strands on the scalp. Its output is CC0, which fits public by default.
  - The mirror is built the way a flat mirror really works: an opening onto a mirrored copy of the room, the person and the lights. That lets the reflection change while the person in front stays human.
  - The AI face is the same head, same pose, same eyes on the camera: dark brushed metal with fine gold contour lines (a machine's depth map of the face) and lit irises. It is original; there is no logo, robot or character from anywhere else in it.
  - The change is four still renders per version (human, AI, glow only, and a map of when each point changes) blended frame by frame in `mirror_video.py`, with a slow push in and film grain.

**New on the MSI:** the MPFB add-on and its CC0 assets are now installed in Blender 5.1. Any AI can script a realistic person from it (`build/make_person.py` is a working example, about 20 s to build).

## Sources used (all from Grok Build's `quotes.md`, confirmed rows only)

Slow cards:

| On screen | Their words or what it measures | Source |
| --- | --- | --- |
| Geoffrey Hinton, 10% to 20% | "Not really, 10% to 20%." (asked if he had changed his one in ten estimate of AI wiping out humanity within 30 years) | BBC Radio 4 Today, 27 Dec 2024, as printed by The Guardian: https://www.theguardian.com/technology/2024/dec/27/godfather-of-ai-raises-odds-of-the-technology-wiping-out-humanity-over-next-30-years |
| Dario Amodei, 25% | "I think there's a 25% chance that things go really, really badly." | Axios AI+ DC Summit, 17 Sep 2025, as printed by TechRadar: https://www.techradar.com/ai-platforms-assistants/claude/anthropics-ceo-gives-a-25-percent-chance-things-go-really-really-badly-with-ai |
| Elon Musk, 10 to 20% | "some chance, which could be, 10 to 20 per cent, that it goes bad" | Future Investment Initiative, Riyadh, 29 Oct 2024, as printed by The National: https://www.thenationalnews.com/future/technology/2024/10/29/ai-to-outthink-humans-in-matter-of-years-tesla-and-softbank-ceos-say-at-fii/ |
| Yoshua Bengio, 20% | "around, like, 20 per cent probability that it turns out catastrophic" | ABC News Australia, 15 Jul 2023: https://www.abc.net.au/news/2023-07-15/whats-your-pdoom-ai-researchers-worry-catastrophe/102591340 |

Fast section (gold = odds it goes badly, teal = doubters and good odds, blue = how soon; the legend is on screen):

| On screen | Colour | Source |
| --- | --- | --- |
| Emad Mostaque, 50%: "My P(doom) is 50%." | gold | https://x.com/EMostaque/status/1864266899170767105 |
| Paul Christiano, 46% (irreversibly messed up future), 22% (AI takeover), 20% (most humans die within 10 years of powerful AI) | gold | https://www.lesswrong.com/posts/xWMqsvHapP3nwdSW8/my-views-on-doom |
| Survey of 2,778 AI researchers, 5% median odds of extinction or similar (2,778 answered the survey; 1,321 of them answered this question) | teal | https://arxiv.org/abs/2401.02843 |
| Same survey, 50% by 2047 (machines outperform humans at every task) | blue | https://arxiv.org/abs/2401.02843 |
| Dan Hendrycks, over 80%: "my p(doom) > 80%" | gold | https://x.com/hendrycks/status/1642394635657162753 |
| Yann LeCun, "essentially zero" | teal | https://x.com/ylecun/status/2043673634363851250 |
| Yann LeCun, "P(doom) is BS." | teal | https://x.com/ylecun/status/1755362942491439265 |
| Vitalik Buterin, 10%: "My p(doom) is around 0.1." | gold | https://x.com/VitalikButerin/status/1729251822391447904 |
| Sam Altman, "a few thousand days" (superintelligence, "it is possible") | blue | https://ia.samaltman.com/ |
| Roman Yampolskiy, 99.999999% | gold | https://x.com/romanyam/status/1767575356155027503 |
| Elon Musk, 80%: "The probability of a good outcome is like 80%." | teal | Joe Rogan Experience, Feb 2025, via https://www.businessinsider.com/elon-musk-only-chance-of-annihilation-with-ai-2025-2 |
| Demis Hassabis, 50% in 5 to 10 years (chance of AGI) | blue | https://www.wired.com/video/watch/big-interview-demis-hassabis-on-the-future-of-work-in-the-age-of-ai |
| Geoffrey Hinton, 10% ("My current estimate is 0.1", extinction in 30 years if AI is not strongly regulated) | gold | https://x.com/geoffreyhinton/status/1719447980753719543 |
| Geoffrey Hinton, next 20 years (AIs "smarter than people", what he says most experts think) | blue | The Guardian link above |
| Eliezer Yudkowsky, "Yes" (ruin, if superintelligence is built like current systems) | gold | https://x.com/ESYudkowsky/status/2101804209528271092 |
| Dario Amodei, as early as 2026 (powerful AI) | blue | https://darioamodei.com/essay/machines-of-loving-grace |
| Masayoshi Son, 2035 (superintelligence) | blue | The National link above |

Left out on purpose: both rows Grok marked UNCONFIRMED (Yudkowsky "95%", Andreessen "0"), Jensen Huang (Grok could not load the Reuters page), and Musk's "20% chance of annihilation" (Business Insider attributes it; the 80% sentence is the one it quotes).

## Honesty checks someone should know about

- **These numbers do not measure the same thing.** The video says so on screen under every slow card ("They are not all answering the same question") and colours the fast section by kind. A viewer still walks away with "lots of experts gave scary numbers", which is the feeling the post wants, but nobody is misquoted.
- **Hinton's slow card is the one place the label is not his sentence.** The number is his ("10% to 20%"); the line under it describes the question he was answering, in The Guardian's framing. It is shown without quote marks for that reason.
- **Three sources are "as printed by"** (Hinton via The Guardian, Amodei via TechRadar, Musk via The National and Business Insider). Grok did not play the original audio or video. The small print says "as printed by" or "via".
- **Repeats in the pile.** After all 19 fast entries have appeared once, the last 13 arrivals are repeats of the same entries. Small repeats show the number only; their source was on screen the first time.
- **I did not re-open the links myself.** I worked from Grok's table and its Check column.

## What I checked, and what I did not

- Checked on the finished files: both play to the end at the right size and frame rate with an audio track (ffprobe), frames pulled from each file at eight points look right (the contact sheet is from the vertical file, not from the renderer), no dash characters in any on-screen text (the script refuses to run if one appears), loudness -16.2 LUFS with a true peak of -0.7 dB.
- **Not checked: nobody has listened to it.** I can measure the sound but I cannot hear it. The heartbeat level, the rising tone and the chord are worth one listen on a phone before it goes out.
- Not checked: playback inside the X app, and how X's recompression treats the film grain in the mirror shot.

- Not built: the optional v2 card Claude added to POST.md at 9:14 (the 1960 Science paper that set doomsday for 13 Nov 2026). It would slot in as one more card after the closing words; say the word and I will add it.

## What I would change with more time

1. **The human face is the weakest part.** It reads as a real person at phone size and in motion, but paused and zoomed it is clearly a good CG head (skin a little smooth, shirt with no folds). An hour more on skin and cloth would help. He does not blink or breathe, because the shot is blended from stills.
2. **The pile is dense by design.** In the last three seconds the captions cannot be read. That is the pressure the plan asked for; the first five are readable.

## Things that could make it land harder (for Jaron to pick)

1. **His own voice on the dark section.** Him saying the line, recorded on his phone, over the slow heartbeat. That would hit harder than text alone, and I can lay it in within minutes of getting the file.
2. **Many faces, not one.** The post says it has to be the masses. The reflection could pass through four or five different people (ages, women and men, skin tones) before it becomes the machine, or the final shot could be a row of mirrors. The generator makes each person in about 20 s, so this is roughly 30 to 40 minutes of work.
3. **A harder first two seconds.** It opens on his line. Opening cold on "99.999999%" for one beat, then his line, would stop more thumbs. It trades calm for hook.
4. **Use the half-changed face as the cover frame** (0:36 to 0:37). It is the strongest single image.
5. **A 30 s cut** is easy if he wants it shorter: three slow cards in place of four and a shorter hold on the mirror.
