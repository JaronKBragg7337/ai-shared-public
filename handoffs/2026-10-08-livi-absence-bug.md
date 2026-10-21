# LIVI false-absence bug (0.6.1) - 2026-10-08

Repo: C:\Users\lilli\Projects\livi-organism. Commit 4bf1d9f on main (pushed). Live: https://livi-organism.vercel.app (auto-deploys from main; confirmed the 0.6.1 bundle is live).

## What went wrong
Jaron's mom's Livi (~1800 cells) was tended daily but got "ABSENCE - waiting through 8 quiet days" on Oct 7 and fell to 47 cells.
The app turns elapsed time into starvation. Several restore paths used the wrong clock:
1. Cloud sync restore (app/LiviCompanion.tsx, initializeCloudContinuity): absence = now - the time the cloud head revision was WRITTEN. A stale head (8 days) means 8 days of simulated starvation, even if she fed it that morning. This only fires when the device has no local save (or local is byte-identical to the head). Triggers: local storage lost/blocked, a new origin or browser, or an account switch. It cannot fire on a normal used device, because every tick changes the local checksum.
2. Restore-history ("Restore" button) and file import used normalizeSavedOrganism, which also ages the body by the revision's age. So restoring the 1800-cell revision in 0.6.0 would have re-killed it. This was an important find.
3. Start-up: localStorage was aged forward before IndexedDB was consulted. If the localStorage copy was stale, the aged copy (lastSeen = now) beat the fresh IndexedDB copy, which was then ignored. Also hadLocalSaveRef ignored IndexedDB.
4. Cloud restore overwrote motes, bond and trust with the cloud value (a rollback to the stale value).
I could not tell from code which one hit her. Her device state is needed for that, and I did not touch it. Reproduced the damage in a test: the old path takes a 1800-cell body to under half and writes the false memory. 5-minute periodic pushes do happen while signed in, but they stop entirely while sync status is "conflict", and silently on errors.

## Stage changes
Not involved. Stage is only a label from age (Hatchling/Young/Mature/Elder); nothing at a stage change touches cells. The only age-based loss is the elder drain above 78% of life, which "Mature" is not in. The 8-day jump also aged it 8 days; that is not repaired.

## Invisible Livi
Rendering is by cell count and spacing (max about 10px per cell). 47 scattered, low-health cells are a small, dim blob, so the render is working as designed. I did not change rendering.

## Fix (0.6.1)
- New resolveRestoreLastSeen/applyRestoredLife: absence starts from the newest trustworthy sign of presence (local last-seen, this device's last sync, the copy's own last-seen), never from when a backup was written. With no local evidence at all the absence is capped at 12 hours (below the 24 hours that writes a long-absence memory).
- Restore-history restore: no gap simulation (she is present). Import: same capped rule.
- Start-up: reads IndexedDB first (1.2s race) and picks the save with the newer own lastSeen BEFORE aging; a save in IndexedDB counts as a local save.
- Cloud restore no longer lowers motes, bond or trust and keeps owned items (max/union).
- tests/restore-absence.test.mjs (6 tests); version 0.6.1; CHANGELOG and in-app History entry; updated the stale 0.5.1 version assertion in rendered-html test.
- Not repaired: an already-written false "long-absence" memory stays in her permanent memory (it cannot be told apart from a real one by code).

## Verified
- Local: npm test = 42 unit tests + 2 render tests pass (also tsc clean; lint has the same 5 problems as before my change).
- Local browser: seeded a stale (8 day) localStorage save plus a fresh IndexedDB save, reloaded: 1793 cells kept, 0 absence memories, age unchanged.
- Live: 0.6.1 bundle served; page loads at 375px wide, no horizontal scroll, clean-storage start works.
- Not verified: the cloud-restore branch end to end (needs a signed-in Supabase account; covered by unit tests only); iPhone Safari specifically (checked Chromium at phone width); which of the 4 causes hit her.

## How she can get the ~1800-cell Livi back (her choice; nothing was done to her data)
Cloud history is append-only (no pruning), and every restore is saved as a NEW revision, so nothing is overwritten and today's Livi stays in history too.
1. Open LIVI (updated to 0.6.1; reload the page once), open the Life Hub, then the Commons tab, signed in with her recovery account (unlock with her password if asked).
2. Find "RESTORE HISTORY". Each row shows life phase, cell count, and time. Tap "Load older protected revisions" until you reach Oct 6-7.
3. Pick the newest row BEFORE the one saved as a "long absence" milestone that still shows about 1800 cells. Tap its "Restore". The row says cells and time so she can check.
4. The app keeps a local restore point first, and the restore becomes the latest save. In 0.6.1 it does not apply any time away. The false memory entry will remain in her Memory tab (history is merged forward).
Today's 1412-cell Livi is replaced as the active body but stays in the timeline (restore it the same way if she changes her mind). If she never signed in on that device, there is no cloud history; then only an exported recovery file could restore it.

## Still open
- Which trigger hit her (ask: is she signed in to the Commons recovery account? any "cloud paused" or "conflict" message?).
- Optional: let the owner delete a clearly false long-absence memory.
- Optional: show a visible "sync is stuck" notice when status is conflict/error for hours.
