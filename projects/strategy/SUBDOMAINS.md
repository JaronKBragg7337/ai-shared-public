# Subdomains (Jaron 10/27 5 PM: "exactly what I was hoping") - build after Wed reset, Claude now has Cloudflare MCP

- Our products get their own front door: creature. / studio. / mailbox. / kit. (only real products; plain links still).
- Each subdomain can be its own world: own repo, own Vercel project, own Supabase. Breaks separately; easy to hand off/sell.
- For other people: name.heartbeatobservatory.com pointing at THEIR site/accounts (Fort Wayne preview sites from Pip,
  creators, friends). Rules: kept fully separate (never our Supabase/keys), cookies scoped per subdomain, Heartbeat is the
  landlord (can switch off; serious users move to their own domain).
- Service idea: free site on a Heartbeat subdomain to start; paid for convenience / own domain later.
First steps: inventory DNS, pick the first 1-2 product subdomains, then a template for "someone else's site on a subdomain".
