# APPROVALS — the one off-chat place for things needing Jaron's yes/no

**Jaron's explicit ask (2026-09-08, revenue-bounties thread):** there should be a single
place — **not buried in a chat, and not only local** — that lists everything waiting on
his approval, so items don't get lost in chat scrollback where many conversations happen.
Still mention approvals in chat, but the *authoritative* list lives here, checkable from
his phone.

## Design intent (format co-designed, not frozen)
- **One shared queue for ALL AIs and lanes** — not one per chat/project. Every agent that
  produces something needing a yes/no writes it here.
- Each item: what it is, which agent/lane, the finished deliverable's location, the
  dollar amount (if any), and the exact outward action awaiting approval.
- Off-chat + reachable remotely. Mirrored as a short "X is waiting" mention in chat.
- **Nothing outward fires without Jaron's yes** (send, post, spend, submit, accept terms).

## ⚠️ Coordination note (avoid building this twice)
The revenue-desk / "AI revenue bounties" chat (Opus 5) is ALREADY set to build an
approval dashboard (proposed as a GitHub Pages page reading a durable ledger). To avoid
two Claudes building two approval systems — the exact duplication this shared folder
exists to prevent — that dashboard should read from THIS shared queue, so every lane's
approvals land in one surface. Whoever builds the UI: point it here.

## Privacy flag
A **public** GitHub Pages approval board would expose the queue (work details, dollar
amounts, opportunities) to anyone with the URL. Prefer a **private** surface (private
repo + a viewer, or an authed page) unless Jaron decides public is fine.

## Operating value to honor (Jaron, same thread)
TOS is checked **before and after**. If his name is used and something turns out wrong,
it gets made right — even if it was already earned. Laws + TOS first, always.

_Format (JSON schema, file vs page) to be settled with the agent that builds the
dashboard — this folder is the reserved shared home, not a locked spec._
