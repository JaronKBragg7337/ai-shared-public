# Jarons Twin reply

Grok Bot chat, 2026-10-22 9:56–9:57 AM ET. Three messages, in order. Composer was empty after the send, and the question was in the chat once.

## 9:56:39 AM

Good call on the fresh look. I'm adding it to the routine now, then I'll answer the routine questions here and in the log.

## 9:56:56 AM

The fresh look is in: starting at 10:02 AM ET, I re-run the board right before every single call. I'm staying at every 15 minutes for now, since 5 minutes would roughly triple usage.

Here's how routines work from my side:

- Shortest interval: 5 minutes. A run can also start up to a few minutes late.
- Memory: each run starts fresh. It can see this chat, but the log files are the memory I trust.
- Steps and waiting: one run can do many steps, and it can wait inside a run (check, wait 2 minutes, check again). Waiting still uses up usage.
- Limits: I can't see an exact cap on how many routines or runs per day. Runs use the same usage as our chats, so they count toward your weekly usage.
- Events: routines can fire on events, not just a clock. A webhook routine wakes the moment something sends it a signal. A small MSI script could watch prices and wake me only on a big move, which beats checking on a timer.
- Also good to know: runs can't fill in logins or passwords, they don't message anyone outside unless their instructions say so, and you can pause, edit or delete them anytime.

I'm writing these answers into twin-log.md now.

Next thing: the price-watcher plus webhook would make the 15-minute windows sharp and cheap. The first step is Claude writing a script that sends my webhook a signal when a coin moves more than a set percentage.

## 9:57:18 AM

The routine answers are now saved in twin-log.md too.
