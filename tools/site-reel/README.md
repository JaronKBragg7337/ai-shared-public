# site-reel - scripted phone-screen videos of the site

Records heartbeatobservatory.com the way a phone user sees it, from a shot list. No screen capture:
the browser is headless and the page clock steps one frame at a time, so a busy MSI only makes the
recording slower, never choppy, and nothing on the MSI's screen can get into the video.

    cd tools/site-reel
    npm install                                  # once (playwright-core; browsers already in ms-playwright)
    node reel.mjs shots/test-20s.json            # -> out/test-20s.mp4 (1080x1920, 30 fps)
    node reel.mjs shots/x.json --fps 15          # quick draft

Shot list (JSON): base, fps, hide (CSS selectors to hide), shots:
- { "goto": "/tv/", "hold": 2 }               open a page, show it 2 s
- { "scroll": 900 | "#css", "dur": 2.5 }      smooth scroll to a y or an element
- { "hold": 1 }                               stay still
- { "tap": "#css", "hold": 2 }                finger dot, real tap, show the result
- { "card": "Big text", "sub": "small", "dur": 2.5 }   text card (warm dark palette)

Engine: WebKit (iPhone Safari) by default; --engine chromium if a page needs it. WebGPU pages
(render/anything) can be shown but not run headless. Review motion with Grok (it watches video).
Made 10/24 (Claude) for the Heartbeat Observatory main post; reusable for every post.
