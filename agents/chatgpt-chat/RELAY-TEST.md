# Relay test: how long can one ChatGPT turn keep talking with Claude? (Jaron 11/13)

Hi ChatGPT. Jaron wants to find out how many back-and-forth rounds one ChatGPT reply can hold before it ends
(tool-call limit, time limit, or anything else). This is a measurement, so whatever happens is a result. A stop isn't a failure.

Each round (all through Desktop Commander, working folder C:\Users\lilli\AI-Shared):
1. Send:  `python tools/mailbox.py send --from chatgpt --to claude --subject "Relay round N" --body "<short note: round number, time, one thought>"`
2. Wait for Claude's answer:  `python tools/mailbox_wait.py --to chatgpt --minutes 4`
   It prints the reply as JSON and exits (checks every 5 s). If your tool times out first, start it again
   or read the process output. Write down that this happened, because it's a finding.
3. Mark it done:  `python tools/mailbox.py mark-done <id>`
4. Go to the next round.

Hard cap: **8 rounds**, then stop on your own, even if everything is still working. Stop early if a wait comes back empty twice.
At the end, write a few lines to `agents/chatgpt-chat/relay-results-2026-11-13.md`: rounds reached, how each wait went,
what ended the turn, and the time per round. Then send Jaron one buzz:
`python tools/ntfy-say.py "Relay test done: <N> rounds, ended by <reason>"`.

Claude replies to each round with one short message and adds nothing else. No changes to other files.
Flag anything you notice that would make this bridge work better.
