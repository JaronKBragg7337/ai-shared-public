# Cloudflare inventory — 2026-10-28, Terra

Report only: nothing was deleted or changed. This is **partial**, not a complete account inventory. Read-only Cloudflare API calls used the requested CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID from the MSI. The ledger says this token was created with Realtime Read + Admin permissions (`state/build-ledger/2026-10-21.md`, 10/27 entry), which explains the visibility gap. No credential values are included here.

## API visibility

| Resource | API result | Interpretation and advice |
|---|---|---|
| Workers scripts | HTTP 200, empty result | No scripts visible to this token; **not proof the account has none**. The three named below are recorded elsewhere but their actual presence, routes, bindings, traffic and purpose could not be checked. Keep until inspected with an account-wide Workers read credential or Claude's Cloudflare connector. |
| Cloudflare tunnels | HTTP 200, empty result | No tunnels visible to this token; **not proof there are none**. A working connector is documented below. Keep. |
| Zones | HTTP 200, empty result | No zones visible to this token; not proof of absence. Public DNS delegates the domain to Cloudflare. Keep DNS. |
| Pages | HTTP 403 authentication error | Unknown; list and check deployments/domains before any removal. |
| KV, D1 | HTTP 401 authentication error | Unknown; inventory bindings and callers before any removal. |
| R2, Queues, Workers subdomain, Durable Objects, Hyperdrive, Vectorize | HTTP 403 authentication error | Unknown; inventory and check dependencies before any removal. |

## Named resources and evidence

| Name or resource | What it is / use evidence | Advice |
|---|---|---|
| `codex-observer-relay` | Named as a Worker in `state/open-list.md:52`; exact-name search across AI-Shared and the site checkout found no other match. Contents, routes, bindings and live traffic unverified. | Keep pending inspection; absence of a repo reference does not establish it is unused. |
| `royal-river-797b` | Named as a Worker in the same open-list entry; no other exact-name match in the two repositories. Purpose and use unknown. | Keep pending inspection of script, routes, bindings and traffic. |
| `cold-morning-fd03` | Named as a Worker in the same open-list entry; no other exact-name match in the two repositories. Purpose and use unknown. | Keep pending inspection of script, routes, bindings and traffic. |
| MSI connector tunnel, Cloudflare name unknown | `runtime/grok-machine-mcp/README.md` and `projects/live-systems-for-everyone/README.md` describe the public MCP hostname forwarding to the MSI; `tools/connector-watch.py` checks it. Live unauthenticated MCP endpoint returned HTTP 401, consistent with a reachable protected endpoint. The API could not identify the tunnel or establish its account. | Keep: used by connector. Do not infer a tunnel is removable from the empty scoped API response. |
| `heartbeatobservatory.com` DNS zone | Public NS lookup returned `raquel.ns.cloudflare.com` and `wesley.ns.cloudflare.com`; site audit records apex and www pointing to Vercel. Zone settings and individual records were not visible to this token. | Keep: domain DNS is in use. |
| `hb-remote-screen` Realtime TURN key | Ledger records its creation; `tools/remote_agent.py` requests relay credentials using the named TURN environment variables for remote-screen connectivity. Current key status and usage were not independently listed. | Keep: code uses it for cellular remote screen. |
| Pages projects and other storage/compute | No list available under this token. Site checkout `README.md` and public DNS identify the primary site as Vercel-hosted, but that does not establish whether any Cloudflare Pages projects or other resources serve other work. | Keep until inventory and callers can be checked. |

## Scope and next inspection

Searched exact Worker names across AI-Shared and `C:\Users\lilli\Projects\heartbeat-observatory`, excluding generated logs, HTML, JSONL and locks; searched Cloudflare, tunnel and TURN references in the code and operational notes. Search cannot prove absence of outside callers, secrets-held URLs, scheduled tasks, routes, bindings or use under another name. Claude's authenticated Cloudflare MCP, or a token with account-wide read permissions for Workers, tunnels, Pages, zones and storage, is needed to finish this report. For each discovered item, inspect routes, bindings, deployment history and recent traffic, then search exact names and URLs again. No remove recommendation is safe on current evidence.

## Full read by Claude via the Cloudflare MCP (10/28 8:05 PM, read-only)
- Workers (4): codex-observer-relay (Jun 3 2026), divine-water-e893, cold-morning-fd03, royal-river-797b (all Dec 18 2025, untouched since). No code in AI-Shared or the site repo calls any of them.
- Tunnel (1): Grok-Machine, HEALTHY. KEEP: it's the MSI connector door (Grok Machine / Heartbeat MAI / msi-heartbeat).
- Pages, KV, D1: none. R2: not enabled. Zone: heartbeatobservatory.com (active).
- Advice: the 4 Workers look like leftovers (3 from Dec 2025 experiments, 1 from the June Codex observer). Remove ONLY with Jaron's yes, since deletes can't be undone.
