# Phone-only company test, built as a game (Jaron 11/16 3:58 PM, with ChatGPT). PLANNED, not started
Comes after the company-organization work.

**Idea (Jaron):** test a phone-only company by having the AIs make something real together: a new game. ChatGPT is the main conductor, as it would be for a phone-only owner. It runs a Claude cloud session, which is a conductor too and hands work to Grok, Kimi, and back to ChatGPT. Jaron only drops in to send messages and get updates, while living his normal phone life (scroll, video, back to the chat). That's his natural flow, so the test fits it.

**What it tests (ChatGPT's list):**
1. Phone interruptions: Wi-Fi <-> cellular, app in the background, the app reopening, a reply erroring and then finishing without a retry (happened to Jaron before). Change one thing at a time first, then mix them to reproduce the old error.
2. How long one ChatGPT turn lasts: is the limit time, number of tool calls, context, or something else? (Today: 12 rounds, 11m 13s, about 31s per round trip.)
3. Two levels of conductor: ChatGPT -> cloud Claude -> Grok/Kimi/others -> results back.
4. Shared pictures and files: ChatGPT makes an image, puts it in shared storage, Claude picks it up and uses it (then the other way). Later: videos and game environments (links to his game ideas).
5. A playable game as the proof, with a visual that grows at every milestone, so the owner sees progress at a glance.
Every test event logs: task id, agent, start, last successful step, connection state, error, how it recovered, result.
Limit to test: once a ChatGPT turn ends, it can't restart its own tool calls. Something has to wake it (a schedule, a cloud worker, or a new message from the owner).

**Why:** phone-only owners need to know what to log and what they'll run into.

**Parked (Jaron, "not right now"):** have ChatGPT and Claude each give different analogies for "a correction narrows, never widens", then compare. He learns by seeing one idea from many angles.

Pictures: research/relay-test-2026-11-16/chatgpt-side-stress/ (15).
