# Control Room kit (Jaron 10/27 10:45 AM) - the phone control room as a product

Modules (all exist except the last):
1. Key Drop - phone encrypts, only the home computer can unlock, tests + buzzes. (Jaron's favorite)
2. Video Drop - phone video/photos to the home computer (memories, movies, content creation).
3. AI talk panel - pluggable: Sapling today; any AI tomorrow (a CLI agent like Claude Code/Codex in a terminal, a local model).
4. Machine health - temperature, memory, disk, what's running, buzz on trouble.
5. NEW: Remote screen + controls - see the computer's screen on the phone, an on-screen analog stick moves the mouse, taps click,
   a keyboard types. Built ourselves (Jaron rejects using an existing app): screen streamed over WebRTC from the home computer,
   input sent back and injected (Windows SendInput), signaling through Supabase Realtime, admin-only, every session logged.

Smallest version for others (no Vercel/Cloudflare needed):
- A static page (GitHub Pages works) + ONE relay both phone and computer can reach (Supabase free tier), + a small agent
  script on the home computer. Or no cloud at all: a private network (Tailscale, free) and the computer serves the page itself.
- A GitHub page alone can't do it: static pages can't receive uploads or pass messages without a relay.
Two markets: free CC0 kit you set up yourself; hosted version that just works. Build after the Wed reset.

## The story (10/27, for the ad / trailer / "why did you make it")
Day off, Jaron out walking across town (21+ min drive from the MSI, no one home). In one morning, all from his phone:
- 10:33 AM: new Anthropic API key made on the sidewalk, dropped via Key Drop, MSI tested it, buzzed "test: works".
- 11:05: Terra built a remote-screen tool; 11:51 he controlled the MSI from his phone (stick, clicks, typing).
- 12:10: "I can't see the mouse" -> MSI now draws a gold pointer on every frame.
- 1:09: it failed on 5G -> diagnosed: cell networks need a TURN relay.
- 1:30: installed Cloudflare's agent plugin to make that relay; its sign-in seemed to need him AT the MSI...
- 1:38 his idea: drop a Cloudflare token via Key Drop -> AI builds the relay -> remote screen works on 5G -> he uses
  the remote screen to finish the Cloudflare sign-in himself. The tool unlocks its own setup, from across town.
Why it helps: you never have to be at the computer. What it does: keys, videos, AI talk, health, and full screen control
from a phone. How: phone page + one relay + a small agent on the home computer.

## Demo mode for recording (Jaron 10/28 9:12 AM)
He wants to screen-record the whole flow (remote, sign-in, Key Drop) for the product but can't show real passwords. Plan: a **demo mode** with
a fake "Example AI" sign-in page, fake keys (sk-demo-...), a fake email code and fake machine stats, all running the real
Control Room flow. It must use made-up branding only, never a copy of a real company's login page. Recordings from it can be shared publicly.

## Guided setup for people who aren't comfortable with tech (Jaron 11/25/2026 9:53 AM)
From the YouTube sign-in he did on his phone: "These are also the things that when we set systems up for other people with the kit, things like that could be useful for people that aren't comfortable or understand things."
What worked, to build into the kit's setup:
- Exact-page links with the account pre-picked (Google `authuser=`, project in the URL) - no "go find the setting".
- One step per message, a screenshot back after each, the AI reads the screenshot and says the next tap.
- A short list of all steps with checkmarks, so the person sees how close the end is.
- Keys go through a Key Drop page on the phone, never pasted into a chat; the machine tests them and buzzes "you are done".
- Warn ahead about scary-but-normal screens ("Google hasn't verified this app" for your own app) and about traps (e.g. a logo upload that forces a weeks-long review).
- Never "sign out" or "delete" anything without saying plainly that nothing is lost; people fear losing accounts.
- Missing pieces get made for them on the spot (here: a privacy policy + Terms of Service page the provider required).
