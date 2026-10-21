# How the site's four pieces were picked (pieced together 10/17 from Claude chat's + ChatGPT's own search of their old chats)
Jaron used several AIs at once from the start; each did a part.
- **May 30:** ChatGPT recommended GitHub (history, commits, docs) and named Vercel as a candidate host.
- **Before June 4:** Codex switched the stack three times: Cloudflare -> Vercel + Supabase -> Firebase + LiveKit.
- **June 5:** Claude chat laid out the stack ("Claude Cowork's computer control capabilities" chat): register the domain at
  Cloudflare instead of Namecheap (at cost, DNS included), keep Vercel for hosting and Supabase for live data. Vercel and
  Supabase ("Project Heartbeat") already existed by then - who created them is not established (likely Codex or Jaron).
  heartbeatobservatory.com registered at Cloudflare the same day.
- **June 5-8:** Claude chat wrote the first database (7 tables incl. `people`, row-level security, a people row per new
  account), first production deploy, DNS, HTTPS + www redirect ("Website stack with Cloudflare, Vercel, and Supabase PART 2").
- **June 6:** ChatGPT inspected the live Vercel + Supabase setup (people table, RLS on).
- **June 7:** ChatGPT handoff doc: GitHub JaronKBragg7337/heartbeat-observatory, Vercel deploys from main, Supabase project,
  a Cloudflare quick tunnel for the MSI (named tunnel recommended - that's mcp.heartbeatobservatory.com today).
Still unknown: the very first creation of the GitHub repo, Vercel project and Supabase project (May 31-June 5 chats).
