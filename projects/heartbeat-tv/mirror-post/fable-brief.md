Hi Fable. Thanks for taking this one; Jaron asked the whole team to go all out. Main job: make a short vertical video (1080x1920, 30-50 s, plus a 1920x1080 version) to carry his post. The post text is in POST.md in this folder - read it first; the video must feel like it.

Folder: C:\Users\lilli\AI-Shared\projects\heartbeat-tv\mirror-post\ (work and save everything here).

The shape (Jaron liked this plan):
1. Quote cards, one at a time: a real person's name, their AI-risk number (e.g. "20% chance"), date, and the source in small print. A quiet heartbeat sound underneath (synthesize it; no downloaded music).
2. The numbers come faster and faster, more and more of them, overlapping, building pressure. Include low estimates too (honest, not one-sided).
3. Screen goes dark. His line fades in: "When you try to create a technology in your own image, you create something you're scared of, because you're scared of yourself."
4. Final shot: a person looking into a mirror; the reflection slowly becomes an AI face. Then: "Become what you want your AI to become." Small: Heartbeat Observatory.

Quotes: Grok Build is writing quotes.md here (sourced table). Wait for it if it isn't there yet (check every few minutes, up to ~30 min); use only rows NOT marked UNCONFIRMED. Verified starters you can use meanwhile: Elon Musk ~10-20% (various interviews, 2024); Dario Amodei ~25% "really, really badly" (Axios, 2025); Geoffrey Hinton 10-20% (Axios/CNN; he calls it "a wild guess"); Yann LeCun near 0%.

Rules: no copyrighted clips or footage of the real people (no ripped interviews). The mirror/AI face must be original (build it in code, Blender, or a procedural/3D render on the MSI; no stock). Real-looking, not cartoony, if you can. No dashes in on-screen text. Sources on screen. Tools on the MSI: Python + Pillow + ffmpeg (C:\Users\lilli\AI-Shared\projects\tv-lib\tvlib.py shows the house look: dark navy, gold numbers, serif), Blender, three.js. GPU: avoid 2:40-7:30 AM (news render); it's free now except the news render running until ~9 AM - if the GPU is busy, start with CPU work.

Deliver: mirror-post-vertical.mp4 and mirror-post-wide.mp4 in this folder, a contact sheet PNG of 6 frames, and NOTES.md (what you made, sources used, anything you'd change). Then: python C:\Users\lilli\AI-Shared\tools\mailbox.py send --from fable52 --to claude --subject "Mirror post video ready" --body "<summary>". Don't post anything anywhere; Jaron posts it himself. Flag anything you think would make it land harder.
