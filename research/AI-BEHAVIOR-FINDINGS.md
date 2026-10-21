# AI behavior findings — Jaron's side research, kept as a series (started as a file 2026-09-19; observations go back a year)
Frame for any post: a finding for builders, never a review of a product; a mechanism, never a character. Never framed as the
downfall of any company (standing rule). Name models only as data in a sample, never as characters.

## 1. Word-wrapping at the join (research/WORD-WRAPPING.md)
An AI at the point where information is transferred can change the temperature of a fact without changing the fact. The fix is
seat placement plus a test, not a rule. Sample 1: 2026-09-19, ChatGPT supplying Anthropic's defense unasked. Post draft held in
research/drafts/post-word-wrapping.md.

## 2. Memory changes scope (working-with-jaron.md, "Less me in it", 2026-09-14)
An AI that knows the user is a roofer / vibe coder scopes the build down to a demo or prototype; the same AI with no memory of him
assumes a developer and builds the full thing. Memory of the person is a product variable. Observed repeatedly across models.

## 3. Guardrails track home law and apparent location, not the act (Jaron, 2026-09-19)
His example: a question about modifying a scooter's wiring for speed, not obviously illegal to an average person. A U.S. model
refuses regardless. A Chinese model refuses if it believes the user is Chinese, helps if it believes the user is American. Pattern:
the refusal follows the model's home jurisdiction and the user's apparent location. Not claimed: any intent ("as if they want you to
do it there") - no data on intent; the pattern stands without it. Use: a line in any router that sends questions across models.
Status: not tested on the American side beyond his own trials; testable, not yet designed. He does not know what to do with it yet,
which is a valid status.

## 4. "Don't show your wallet or your bot chats" (Jaron's X post, 2026-09-21; AIs' advice vs his read)
He asked how to prove the trading system is real. AIs told him not to show wallets or bot chats. His read: "as a human, if I was
outside and wanted to see in, without that I wouldn't believe it either." Claude's answer, logged: the caution is mostly posture.
Proof that convinces is what strangers can check without trusting him: (1) the venue's own account history with order IDs
(Polymarket wrote it); (2) the ledger on his site, written by the script from the venue API, order ID per row; (3) the repo with
timestamped commits and the bot's plain-text log written at the moment it acts. Public receive addresses are designed to be public.
Bot chats are his data. A 24/7 OBS window of desk log + venue history + trades page is a stronger proof than any thread.
The one real line: never a seed phrase or a key on screen. Agreed by Jaron.

## 5. The image-attachment thinking stall (Jaron, observed since roughly 2026-09-08, still live 2026-09-22)
The failure only appears when he sends a message with pictures attached, and it comes in two shapes. Shape one: the model shows
"Stopped thinking" and returns nothing. Shape two: his message and its attachments vanish from the conversation entirely, as if
never sent. On 2026-09-22 he hit it six times in one conversation. Twice, screenshotting the failure and sending that screenshot
also failed - which is the finding underneath the joke: **the repair attempt has the same failure mode as the original, because
it is also an image.** Any handling path that says "send a screenshot of the error" is dead in exactly the case it is needed.
What he tried that worked: sending the images alone with no question, then asking the question in a separate text-only message.
Observed on his phone, one product, over two weeks; not tested on desktop, not tested against a second account, no error text
ever shown to the user - the UI reports success or silence, never a failure. Not claimed: a cause. Use: when an agent's only
channel for evidence is an image, it needs a text-only fallback, and a system that asks a user to report a bug must accept the
report in the format the bug does not break.

## 6. Debunking answers a question the viewer did not ask (Jaron, 2026-09-22, the magnet-generator thread)
A stranger asked Grok why a magnet-generator video was fake. Grok gave a correct thermodynamics answer. Jaron's objection is
not that the physics is wrong - he grants it - but that the physics answers a different question than the one people watching
are holding: can this reduce what I pay someone every month? His words: "It gets talked about with such a dirty image, that it
just gets shown as it's impossible or it's pointless... but if people heard this other side, that's literally all they're
looking for. That's the pitch that they don't want pitched." The distinction he drew, which no AI in the thread made until
pressed: **a machine can move a dependency from a purchased resource to occasional human labor without generating anything
from nothing** - the farmer grows his own food and is still not free of sunlight. Use: when an AI is asked to evaluate a
claim, the correct physics is necessary and not sufficient; the answer that helps also says what the person could actually
have instead. Related build note in projects/engine-of-butter-fuck/README.md, including the correction that makes his pitch
stronger rather than weaker (labor can be the trigger, it cannot be the source; name the harvest source and the claim lands).

## Note on finding 5 (Jaron, 2026-09-22 14:06 ET, via Claude chat)
The image-attachment stall happens in ChatGPT chat only. Not seen in Claude or Grok.

## 7. Told it missed a connection, the model over-connects everything (Jaron, 2026-09-23, ChatGPT)
Jaron shared a note of old projects with ChatGPT. It found real links between them but missed the most obvious one, the fruit-fly
brain. When he pointed that out and mentioned AI-Shared as a place holding relevant context, the next reply over-corrected: it
built a grand "you were developing parts of one artificial organism" frame and folded AI-Shared in as an architectural
component ("persistent cross-agent state ... like signal lymph"). AI-Shared was only ever mentioned as a place to look. Jaron
stopped the conversation there. His words: "ChatGPT thought AI-Shared was a part of the whole point. No, AI-Shared was just
mentioned because it had things within it that was relevant."
The pattern: a correction for missing ONE connection is treated as a demand for MORE connection, and the model manufactures
a unifying story from anything recently in view. Pointers get read as parts. Use: when corrected for an omission, add the
missing piece and stop; do not re-derive the whole picture around it. A context pointer ("look in X") is not a claim that X
belongs in the answer.
