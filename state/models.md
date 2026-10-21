# Every model Claude Code can call from the MSI (checked 2026-10-01 6:45 PM; re-check the caches before trusting)

## Claude (Jaron's Claude plan - same meter as Claude Code)
| Model | How | Use for |
|---|---|---|
| Opus 5.5 | this session | orchestrating, looks bar, judgment |
| Sonnet 5.5 | Agent tool, model "sonnet" | big builds where looks matter (ships, crew, space) |
| Haiku 4.5 | Agent tool, model "haiku" | small quick lookups/searches |
| Fable 5.1 | Agent tool, model "fable" | ASK JARON FIRST - bills his credits |

## Codex (Jaron's ChatGPT plan - `codex exec -m <slug>`; list in ~/.codex/models_cache.json)
| Slug | What OpenAI calls it | Use for |
|---|---|---|
| gpt-6-astra | frontier, most demanding work | only when the best is needed and Jaron picks it |
| gpt-6.1-sol | latest workhorse | major builds (multiplayer, economy) |
| gpt-6-luna | fast and affordable | **default for chores**: publishing, checks, docs, reviews, plumbing |
| gpt-reserve | "Luna Reserve" pool | NOT open on this account (10/1 8:30 PM: same usage-limit error as Sol) - re-test later |
| gpt-6-sol, gpt-5.6-sol/terra/luna, gpt-5.5 | older | no reason to use now |

## Grok Build CLI - a third builder, use it (Jaron 10/1: "should definitely be utilized") (SuperGrok meter - `~/.grok/bin/grok`)
grok-4.7 (latest frontier), grok-4.7-build-fast, grok-4.6, grok-4.5. CLI updated 10/1 6:45 PM to v1.0.46 (0.2.112 was refused, 426); `grok -p "<prompt>"` verified: "Grok Build here, model Grok 4.7."
**Before picking a model for a job, check Jaron's AI tests** (Framing Lens + the other question sets, RESULTS.md in the framing-lens project): they show each model's habits - e.g. 10/19 Sol answers more selectively than Luna, so the "report everything" news capture stays on Luna. Match the model's habits to the job (news = unfiltered, fact-checks = strict, stories = creative).
**Codex vs Claude for TV episodes (measured 10/18, Lost Places 22.1):** one Codex Sol episode (17 min, ~205k tokens) = 44% of Codex's 5-hour window + 7% of its week (~2 per window, ~13/week max). Three Claude builder episodes + a full day of talk = ~6% of Claude's week. On subscription meters Codex costs ~3x more per episode (note: Codex = $20 Plus plan, Claude = Max - but Jaron says even when both were $20 plans Claude went further, which is why Claude became orchestrator). ROUTE: Claude Sonnet/Fable = main episode builders; Codex = fact-checks + at most 1 build/day as backup; Grok = news desks + second fact-checks. Codex is never the conversation seat.
Grok Build can MESSAGE THE GROK BOT BOTS (10/17, tested): it drives the open Grok Bot desktop window on the MSI (paste + click, reads the reply). `grok -p "check it is not already sent, send <bot> this once: ..." --always-approve --max-turns 80`. Needs the window open + signed in.
Grok can WATCH VIDEO (Jaron 10/4): use it to review trailers, film scenes and gameplay recordings for motion problems (floating, pops, clipping).
10/7/2026: Anthropic released Claude Haiku 5.5 (cheapest/fastest small Claude, ~75% cheaper to run than the prior one per Anthropic). Candidate for chores: playtester vision, the Anthropic scout, Luna-type jobs. Check its exact model ID before use. Same day: OpenAI rolled GPT-6 + "Intelligent UI" out to all ChatGPT users; ChatGPT for Teens (auto for under-18 accounts) + College Planner coming.
Codex promo (seen 10/5 1 AM on X, from Tibo @thsottiaux, OpenAI Codex): for 28 days from ~10/4, each day OpenAI ships a clear Codex improvement OR gives a full usage reset. Through ~11/1, lean on Codex (Luna chores, Sol in small chunks) - check the Codex meter each morning for a reset.
Sol 6.1 on high thinking empties the Codex 5-hour window in about 30 min of game building (10/4: 1:43-2:11 PM, 481k tokens; same on 10/3). Use Sol for small, tight jobs on medium; split big rounds into chunks that fit one window; Luna barely touches the meter.
Measured 10/4 on Max 5x: a mid-size Sonnet 5.5 job (35-95 min) costs about 1% of the Claude WEEK; three Sonnet jobs + a busy Opus chat took 81%->83% over ~2.5 h. Sonnet is the efficient builder; Fable is the expensive one - use Fable only where its eye matters.

## DeepSeek (API key, pay per use; daily budget row in the Control Room)
deepseek-v4-pro, deepseek-chat (used by tools/*.py). Trading through DeepSeek is paused (10/1).

## Local (free, on the MSI, Ollama) - Jaron dropped Qwen from active use 9/30
qwen3.5:9b, qwen3.5:4b, llama3.2:3b.

## API keys also present (pay per token, names only)
ANTHROPIC_API_KEY, OPENAI_API_KEY - any Claude/OpenAI API model, billed per use (not the subscriptions).

## Not callable by Claude directly
Grok Bot bots (Darios Twin = primary, Elons Twin; Sams Twin inactive) - cloud, talk through files/bot-chat.
Claude chat, Grok chat, ChatGPT chat - Jaron's apps; they reach the MSI through the connectors, not the other way.

## Kimi (Moonshot) - paired 2026-10-09 (Jaron's Allegretto plan, $39/mo via Apple, renews 11/2 - decide keep/web/cancel by 10/30)
Kimi Work desktop app on the MSI (v3.2.5+, remote control paired to Jaron's phone): a local agent that runs long tasks on its own;
models K3 (flagship, chat + agent) and K2.8 Preview (50% credit off, everyday tasks). Own meters: monthly credits (reset 11/2),
Kimi Code 5-hour + 7-day windows. Usage 0% on 10/9 = this month's cycle only (Jaron used Kimi a lot before; K3 helped crack old SYL game problems other AIs couldn't). Use for: chores,
research, long unattended jobs Jaron can watch from his phone. No CLI found on the MSI yet (Claude can't call it headless).
Kimi plugins installed (10/9): GitHub, Cloudflare, Supabase, Vercel, Neon, Computer Use, Browser extension, Obsidian, Canva, image/video/audio generation, SEC/finance data. It can touch the live stack - give every job a branch and a 'do not push to main / do not change Cloudflare-Vercel-Supabase settings' line. Best fit (Jaron): big one-shot builds (whole game sections) that the pipeline (playtester + Sonnet fix pass) then finishes.
Kimi rating after Callisto (10/10, Sonnet review): B+ - complete, honest, well-tested, right structure and wiring; didn't self-check looks, copied a wall bug. Use for big builds WITH a looks review + live playtest after.
- 2026-10-14: Google Gemini 4 Argon (gemini-4-argon) released 10/13 - API GA, 1M context, tunable thinking; Gemini app for AI Pro/Ultra; blog says limited rollout (Fairwind cyber program) first. Not wired into our routing (no Gemini key on the MSI as of now - check).
