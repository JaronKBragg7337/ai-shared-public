# ChatGPT <-> Claude relay test, Fri 11/13/2026 (Jaron's idea)

What happened, in order (screenshots in screens/, numbered):
- 01-05 (9:17): ChatGPT (phone chat, Desktop Commander on the MSI) explores AI-Shared read-only, finds the mailbox and the two listeners, proposes a one-message test.
- 06-15 (9:27-9:28): one-message test. ChatGPT -> ai_mailbox -> Claude's long-running session -> ntfy buzz on Jaron's phone, end to end. Jaron watched ChatGPT's reply arrive while Claude's buzz landed over it.
- 16-21 (9:47-9:52): relay test (agents/chatgpt-chat/RELAY-TEST.md). One ChatGPT turn: 8 of 8 rounds, 4m 18s, average reply 15.3 s. Ended by the planned 8-round cap, not a limit; the true ceiling is unknown.
- 22-29 (9:55-9:56): the same rounds seen from Claude's side (Remote Control on his phone).

Results: agents/chatgpt-chat/relay-results-2026-11-13.md (ChatGPT's log) and state/timeline.md 11/13 09:27 + 09:46.
Made possible by: tools/mailbox_wait.py --to <ai> --minutes N (added 11/13).

The rounds designed a compaction-memory test (to run later):
- Three versions: handoff only / handoff + words of the conversation / handoff + words + the screenshots that matter.
- Questions written and sealed before any search. A blind third AI scores; Jaron rates "feels like the same Claude" blind, as its own outcome.
- Measures: tokens, accuracy, recovered relationships, order of discoveries, false associations.
- Worst failure: a confidently invented connection. "Missing a detail is cheaper than inventing one."
- Label evidence, hypotheses and uncertain links separately.

Next: run the memory test; find the real round ceiling (no cap, or a high one).
