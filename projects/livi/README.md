# LIVI - the pet organism (coming back)

Repo: github.com/JaronKBragg7337/livi-organism (Next.js, last commit 2026-07-29, v0.5 "living continuity"). Live at
livi-organism.vercel.app. Logged 2026-09-25 from Jaron's bedtime notes.

## Why it is coming back (Jaron)
His mom feeds her Livi three times a day, plays with it, and is attached to it. His other projects are cool to her; this one
she opens every day. Originally made for his kids (not shown to them yet). Plan was an iOS + Android app at $0.99-1.99, free with
a code for family, friends and people who follow him; people who find it cold on the store pay. The pay side is still an open talk.

## The hard constraint: his mom keeps her exact pet
Checked 2026-09-25: Livi saves the pet in the phone's browser storage (`localStorage` key `livi-organism-v1`) at
**livi-organism.vercel.app**, plus an optional encrypted cloud backup through Supabase (app/cloud.ts, NEXT_PUBLIC_SUPABASE_URL).
Browser storage belongs to the web address. So:
- **Moving Livi to a different address (e.g. heartbeatobservatory.com/livi) would show her an empty pet.** An iframe does not
  fix it either - iPhone Safari partitions storage inside frames.
- Safe path: keep livi-organism.vercel.app as Livi's home, ship every update there, and give Heartbeat Observatory a Livi
  page/tile that opens that address. Her pet stays where it is.
- Before any bigger move (app store, new domain), get her pet into the cloud backup first and verify it restores on a second
  device. Only then move.

## Supabase question (Jaron: "more than one project on it now?")
Yes - the Pro org can hold more projects, but each extra project adds its own compute bill (~$10/month for the smallest). Cheaper:
Livi's cloud tables live inside the existing project (ygjpnvrwhkrowkrskftk) - no extra cost. Which Supabase Livi's cloud backup
points at today is not yet checked (Vercel env on the livi project).

## Next (pending, Claude Code on the MSI)
Audit the build (does it still run, what's broken), list improvements/new features, add the tile on the site, keep the address.

## 0.6.0 shipped 2026-09-25 ~8:10 PM (Claude Code) - commit 2a3f30d on main, live on livi-organism.vercel.app
From Jaron + his mom's texts: her LIVI stuck at ~883 cells, 1,840 Motes with nothing to buy, plays only with Pip, Moss sometimes,
never Oona, "Pip should dance when he visits". Shipped: grid 35 -> 51 (old saves migrate, every cell kept - tests/save-compat),
auto zoom-out + Wide Meadow room (free at 600 cells), friends drawn as living cell lattices grown from visits + bond, Pip dances,
new items (Bubble Wand 90, Dance Drum 140, Star Lamp 220, Crystal Cave 320, Sunset Reef 450). Friends only ever visit when she
invites them, so Oona never shows up unless invited. She made a backup download before the update.
Not done: no remote way to see her pet's state; perf measured equal to 0.5.1 in headless tests, not on her phone.

## Mom's feedback, 2026-09-26 morning (via Jaron)
"She absolutely loves it! She didn't know how we could get it to work but she's glad we did." Great job on the work. "Her Livi
loves it." More details will come as she uses it.
