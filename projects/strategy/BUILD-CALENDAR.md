# Build calendar (Jaron 10/27 6:43 PM) - builds that schedule themselves. Build after Wed reset.

How: a build queue (state/build-queue.json: job, domain, brief file, best model, needs GPU?, proof). A Windows task runs at
each day's slot, picks the next job for that day's domain, checks limits (route.py usage, GPU curfew 2:45-7:30 AM,
gpu.lock, temps), launches the builder (Terra/Sol via codex, Kimi, Claude -p for Anthropic, medium effort), logs to the
timeline, and posts the result to the mailbox. Jaron's live work wins: if he is actively building, scheduled jobs wait.
Nothing goes live without its checks; results come to him as one buzz.

Draft day themes (his to change):
- Mon: TV shows + Shorts batch (keeps the posting queues full)
- Tue: render engine / big build steps
- Wed: Studio + music (Claude week resets Wed 4 PM -> heaviest Claude builds Wed evening/Thu)
- Thu: worlds, games, creature
- Fri: site + control room tools + fixes from the week
- Sat: social/growth + trading prep (Polymarket back Sat)
- Sun: recap, cleanup, plan next week's queue
Daily always: news (night), posting, health checks.
