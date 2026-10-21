# Brief: full audit of everything that makes up heartbeatobservatory.com

For: Codex on GPT-6 Luna (max effort). Written 2026-09-23 by Claude Code with Jaron. READ-ONLY. Change nothing, deploy nothing,
merge nothing, delete nothing. Never print a secret value; names only.

## Why this exists

Jaron has built far more than anyone has a map of: pages, worlds, games, AIs, live feeds, NPCs, multiplayer. Some are live,
some are unreachable, some have several versions, and some quietly run on their own - writing to the database or spending API
credits - without anyone watching. Today (9/23) the Supabase database came back after filling up, and the real cause turned out
to be something nobody knew was running (the Polymarket connector logging every call, not Qwen). Jaron's hunch is that there is
more like that. Find it.

**Folder names are not to be trusted.** Identify things by what they are - project names in package.json / README / page
titles / deployed URLs / repo names - not by what a folder happens to be called. G:\ copies are usually stale; GitHub main and
what is actually deployed are the truth. See projects/games/INVENTORY-2026-09-22.md for how that played out with the games.

## Where to look (all of it)

1. **GitHub** - every repo under JaronKBragg7337: what it is, last commit, whether it deploys somewhere, where.
2. **Vercel** - every project, its domains, latest production deployment, serverless / API routes, cron jobs, and env var
   NAMES (not values). A VERCEL_TOKEN exists on the MSI (AI-Shared secrets, name only). If you cannot reach it, say so.
3. **Cloudflare** - DNS for heartbeatobservatory.com, any Workers, Pages, R2 or caching rules. If there is no access from the
   MSI, say exactly what you could not see.
4. **Supabase** - Claude Code already pulled the database side; it is below. Match code to it.
5. **The MSI** - Windows scheduled tasks, running processes, and the project folders under C:\Users\lilli (AI-Shared,
   Projects, source, runtime) and G:\My Drive\Codex Active\projects. Name things by what they are, not the folder.

## Jaron's leads (things he knows exist; find them and everything like them)

- **Social page** gets live news from the **Perplexity API**. Who calls it, how often, what it costs, where the key lives (name).
- **Movie theater** plays live video. Several versions exist; one lets him upload his own videos. A theater *building* was made
  for it but never placed in any world; it had its own test page. Find every version and which is best.
- **Games** - many were meant to be multiplayer: see each other second-for-second, keep inventory, characters, a phone they
  carry. Which games have multiplayer code, what backend each uses, whether it works now.
- **3D worlds** (not games; walk around). Objects in them open games, the theater, social, and library pages. Worlds have
  characters, users, their own apartments with pages, phones, account info. One world has **Claude and Perplexity roaming as
  NPCs using API credits**; Claude helps players with information about the site and world. **Characters persist as ghosts**
  after the player leaves. Find which world, what calls the APIs, how often, and what it costs when nobody is playing.
- **AIs he tried to make**: **PAM** (own repo, "updates every" - find out how often and what it does), **Keava AI** on the social
  page (he thinks it is not plugged in - confirm).
- **NPC towns with scripts** - a world like the others with NPCs that have jobs and roles.
- "Many, many other things like this too." Treat the list as a starting point, not the boundary.

## What the database already shows (Claude Code, 9/23 ~6:35 PM)

- 75 tables in `public`. Biggest: qwen_events 1,492 MB (the connector log above, now capped), fly_school 136 MB, fly_ground 7.7 MB;
  everything else under 1 MB.
- **Tables broadcast live by Supabase Realtime** (each insert/update is pushed to listeners, which costs CPU): qwen_events,
  qwen_state, qwen_messages, qwen_runtime_control, pam_events, pam_devices, pam_messages, world_characters, world_props,
  world_spaces, placements, apartments, messages, agent_state, agent_events, rustfall_rooms, rustfall_player_sessions,
  rustfall_commands, rustfall_events. For each: which page listens, and is anything still writing to it.
- **Scheduled jobs inside Supabase (pg_cron):** `the-current-tick` every 10 minutes (HTTP post to an edge function) and
  `habitat-world-heartbeat` every minute (`select public.habitat_world_heartbeat()`). What do they do, what do they write, are they
  still wanted.
- **Edge functions:** `the-current-tick` (v7) and `world3-tick` (v3, no JWT check - anyone can call it; note it, do not change it).
- Table families that hint at projects: the_current_* (a world / "era" simulation), habitat_* (bodies, actors, memories, objects,
  model generations), world3_*, rustfall_*, parkworks_saves, pam_*, qwen_*, desk_*, paper_* (paper trader), posts / follows /
  likes / reposts / bookmarks (social), library_books, people, surfaces, items, observable_sources, ask_log.

## What to produce

One file: `C:\Users\lilli\AI-Shared\projects\site-audit\INVENTORY.md`, plain words, phone-readable, with these sections:
1. **Every page** - public URL, what it is in one line, source repo, deployed yes/no, reachable from the site's own links yes/no
   (and from where), and duplicates / older versions of the same thing.
2. **Everything that runs on its own** - scheduled jobs anywhere (Supabase cron, edge functions, Vercel cron, Windows tasks,
   always-on processes, NPC loops, ghosts): where, how often, what it touches.
3. **Everything that spends money or API credits** - Perplexity, Claude/Anthropic, OpenAI, DeepSeek, xAI, anything else:
   what calls it, how often, estimated cost per day even when no human is on the site.
4. **Every database dependency** - page or job -> table -> read/write/realtime.
5. **Orphans** - built and working but unreachable; and **ghosts** - running but not needed by anything live.
6. **Top five findings** Jaron should know first, in plain words.

End with the three lines from WORKSPACE_RULES: verified locally, verified remotely, still unverified.
