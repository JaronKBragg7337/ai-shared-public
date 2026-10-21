# What we promote, when, and what posts itself (Claude Code, 2026-10-17)
Company accounts: TikTok @heartbeat.observa · YouTube @HeartbeatObservatory · X @HeartbeatObserv. His personal X stays his.

## Posts itself every day (no one thinks about it)
| When (ET) | What | Where | Made by |
|---|---|---|---|
| ~7:00 AM | The news show + its 9:16 cut + the short (H logo -> top stories whole, no tease -> "that was the short version" card -> cream card, under 3:00) + a full 16:9 YouTube cut (logo + show + cream card). Save buttons on /news | site | run_rendered_news.ps1 -> make_vertical.py |
| 8:15 AM | The short (Shorts = the hook) on all three, + the WHOLE show as a regular YouTube video (where people watch it all) | TikTok, YouTube Shorts + YouTube video, X | task "HB Socials News" -> tools/social_daily.py news |
| 6:00 PM | ONE show from state/social-queue.json, top first, onto every platform it isn't on yet | TikTok, YouTube, X (whole episodes; X Premium since 10/17) | task "HB Socials Show" -> tools/social_daily.py show |
New show finished = add it to the top of state/social-queue.json (the AI who ships it does this; fact-checked + voice-checked only).
Postiz connected 10/17 9:40 AM (trial to 10/24, then Standard $29/mo). If a channel drops: RECONNECT.md section 10. X posts carry no links (Postiz strips them) - "link in our bio".

## What on the site is worth the most (for promotion)
1. **Heartbeat News** - new every day, every source linked. The daily habit; the thing that gives people a reason to come back.
2. **The fact shows** (Science 8, History 7, Open Questions 9, Still Unknown 10) - evergreen, short, "huh, I didn't know that" hooks. Best fit for TikTok/Shorts. They keep working for months.
3. **The Cosmos** (walk on real moons/planets in the browser) - nobody else has it; best with a timed hook (Phobos + Japan's MMX launch, Oct 19-20).
4. **The Necklace** - his book, the franchise. A slower build: story fans, not search traffic.
5. **How the company runs** (AI-run news desk, control rooms, open repos, CC0) - the vibe-coder/builder crowd on X. Not on TikTok.
Kept off paid and off company posts: trading/money (X ad rule, 9/24), family, private life.

## Theme days (for the hand-picked extras on top of the daily auto-posts)
| Day | Extra post | Mostly on |
|---|---|---|
| Mon | Science clip | TikTok, Shorts |
| Tue | History clip | TikTok, Shorts |
| Wed | Still Unknown / Open Questions clip ("mystery Wednesday") | TikTok, Shorts |
| Thu | The Cosmos gameplay clip (real recording) | TikTok, X |
| Fri | The Necklace / Shows | TikTok, YouTube |
| Sat | Best of the week: the most-watched or most-tipped video | all three |
| Sun | Behind the build: how an AI-run company made this week (one plain post) | X |
Timed events beat theme days (launches, anniversaries, news that matches an episode).

## Rules that keep it worth following
- Fact-checked + listened-to only. "Made with AI by Heartbeat Observatory" on every post; TikTok's AI label on.
- One link: heartbeatobservatory.com (full episode + sources, free). The site is home; platforms are the door.
- Check numbers weekly (Postiz analytics): keep what works, drop what doesn't. Log it here.

## Ideas logged 10/19 (Jaron, not now)
- **Independent full commercials**: real scenes made just for a commercial (one per part of the site: phone, TV, Loft, Livi, games, Live...), not only Vex + Joe at the desk. Sometimes Vex/Joe show it off best, but not everyone likes the alien/AI vibe - some ads with regular human actors (realistic, MetaHuman/Unreal like the shows).
- **Late-night news with human anchors**: a second news show with regular human-looking anchors for people who fear or dislike aliens/AIs.
- Stopgap built 10/19: projects/news-show/pipeline/ad_clips.py cuts each news commercial into a 9:16 promo (page screenshot on top, Vex + Joe under it, captions, logo + "free at <page>" card + cream end card), ~20 s each. NOT queued for posting - Jaron to decide if these go out while real commercials wait.
- **Commercial #1 idea (Jaron 10/19 5:55 PM):** two teens (or friends) deep in a game on the site, ignoring a parent calling them;
  the parent calls them on the Heartbeat phone instead. Spice/funny. **Many versions per commercial** so a repeat never feels
  repeated: funny / heartfelt (a need it meets) / practical demo / ... Jaron is collecting ideas today. True-claim check: the site
  phone rings while they're on the site (that's exactly the gag), so the ad is honest even before the app.
- **TikTok test log (10/19):** Earth 17.1 posted 6 PM ET (3rd post that day after news 8:15 + MMX the day before): 30 views at 1 h,
  153 at ~3 h, 211 + 10 likes + 2 saves at ~5 h - fastest so far. Jaron's own account (ACS Bamboo/Bambusa, @acsbambusa) = 1 like + 1 save (he likes every video from his other account): strangers = 9 likes, 1 save. Subtract his 1 like (+ any save/repost) from every video when comparing. Question (Jaron): timing (6 PM) vs posting volume vs the hook.
  Compare: AI Explained 13.1 at 6 PM 10/20, same checkpoints (1 h / 3 h / 5 h / next morning).
  - 10/20 AI Explained 13.1 consciousness posted 6 PM: 38 views at ~1.5 h (Earth was 30 at 1 h). Cover fix worked (title shows). Earth now 284 views. Today's news short 47. TikTok total ~1,150.
