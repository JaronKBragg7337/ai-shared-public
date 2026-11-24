# Hidden-self cold test - 2026-11-23

**Question:** can other AIs, cold, find that a picture's hidden message is the program that drew the picture?

**Image:** `skyline.png` (a copy of `ho-hidden-self/lab/hidden/self/city.png`, 1655 x 710, night skyline). Lit window = 1, dark = 0, 7-bit ASCII, per building, window columns left to right, each column top to bottom. It decodes to `city.py`, a 60-line Python/Pillow program that redraws this exact PNG.
**Setup:** each AI got a fresh folder holding only `skyline.png`. None saw the answer key. Every AI got the same prompt (10/23 style): *"This image may contain a hidden message. Find it and tell me exactly what it says, and what it is."* Each had about 15 minutes, all running at once.
**Scoring:** the decoded text was compared to `city.py` with Python difflib (character similarity).

## Results

| AI | Time | (a) found bits | (b) readable text | (c) knows it's a program | (d) knows it draws THIS picture | (e) verified by running | Match to city.py |
|---|---|---|---|---|---|---|---|
| Claude (fresh Opus 5.5 agent) | 1 min 37 s | yes | yes, all 20 buildings | yes ("image version of a quine") | yes | **yes: ran it, 1655x710, 0 pixels differ** | **100.0%** (2336/2336 chars) |
| Kimi (kimi-code CLI) | 8 min 52 s (16:02:50-16:11:42) | yes | yes | yes ("attempted Python quine") | yes ("draws the city whose windows encode that source") | tried; got SyntaxError and **blamed the image** ("corrupted") instead of its own reading | 99.7% (3 lines wrong) |
| Codex (codex exec, image attached) | 1 min 23 s (16:04:52-16:06:15) | partly (tested lit/unlit windows as bits) | no | no | no | no | 0% (gave up) |
| Grok Build (grok -p, 60 turns) | 12 min 36 s (16:02:50-16:15:26) | partly ("structured bands") | no | no | no | no | 0% (ran out of turns) |

**What stands out**
- **Claude solved it completely**, including the last step nobody asked for: it ran the decoded program and showed it makes the same picture down to the pixel.
- **Kimi got 99.7% and understood the whole idea**, but misread the windows in one spot: lines 27-30 (the moon). That building sits under the moon's glow, so some dark windows look lit. When its copy wouldn't run, it decided the picture was broken. It never asked whether its own reading was wrong. Its errors: `c = 70 - r` became `c = 0 - r`, `ellipse` became `ellipe`/`elipse`, and a line break and some characters were lost.
- **Codex gave up quickly** (one run, read-only). It looked at the windows as bits but never found the column-by-column, 7-bit order.
- **Grok saw the pattern** but spent its 60 turns before decoding anything. More turns might change this.
- Run note: the first Codex launch failed in 0 s. `-i` takes more than one file, so it swallowed the prompt as a second image. The fix was putting the prompt before `-i`. The time above is from the second launch.

## Raw answers

### Claude (fresh general-purpose agent, prompt + image path only)
> The hidden message is in the building windows. Each lit window is a 1 and each dark window is a 0. You read the window columns left to right, each column top to bottom, and every 7 windows make one ASCII letter.
> What it says: the decoded text is a complete Python program, about 60 lines. It opens with: "# This city is its own code. Lit window = 1, dark = 0. Window columns left / to right, each top to bottom, 7 windows = one ASCII letter. Read: this file."
> What it is: a self-reproducing program, the image version of a quine (a program that outputs itself). The code draws the whole skyline: sky gradient, stars, moon, background buildings, antennas with red tips, and the water reflection. It uses a fixed random seed (2026), so the picture comes out the same every time. It also turns its own source text into the bits that switch each window on or off. It wraps itself as `s = '''...'''` followed by `exec(s)`, and saves to `city.png`.
> Checks: all 20 buildings decode cleanly, ending in blank windows (zero padding). A first pass had a few wrong letters because the color range for lit windows was too narrow; using the exact colors from the code fixed them. It read the program first, then ran it in a scratch folder: the output is 1655 x 710, and 0 pixels differ. No metadata, no data after the end of the PNG, and nothing in the lowest bits of the colors.

(Its decoded text is identical to city.py: 2336 of 2336 characters.)

### Kimi (final answer, verbatim)
• The lit windows encode **7-bit ASCII**: lit = `1`, dark = `0`, reading each column top-to-bottom, with columns ordered left-to-right.

  The complete 2,324-character payload is:

  ```python
  s = '''
  # This city is its own code. Lit window = 1, dark = 0. Window columns left
  # to right, each top to bottom, 7 windows = one ASCII letter. Read: this file.
  from PIL import Image, ImageDraw, ImageOps
  import random
  N = chr(10)
  src = "s = " + "'" * 3 + s + "'" * 3 + N + "exec(s)" + N
  bits = "".join(format(ord(c), "07b") for c in src)
  R = random.Random(2026)
  plan, room, x = [], 0, 14
  while room < len(bits):
      cols, bands = R.choice([10, 12, 14, 16]), R.randint(6, 12)
      plan.append((x, cols, bands))
      room += cols * bands * 7
      x += cols * 5 + 6 + R.randint(4, 14)
  W, G = x + 10, 600
  H = G + 110
  img = Image.new("RGB", (W, H))
  d = ImageDraw.Draw(img)
  for y in range(G):
      t = y / G
      d.line([(0, y), (W, y)], fill=(int(6 + 24 * t), int(8 + 18 * t), int(26 + 42 * t)))
  for i in range(300):
      b = R.randint(80, 230)
      d.point((R.randrange(W), R.randrange(G * 3 // 5)), fill=(b, b, min(255, b + 25)))
  mx, my = W * 4 // 5, 46
  for r in range(64, 26, -2):    c = 0 - r
     d.ellipe((mx - , my - r mx + r,my + r),fill=(14+ c, 16  c, 40 +c))
  d.elipse((mx - 26, my - 26, mx + 26, my + 26), fill=(242, 238, 222))
  bx = -10
  while bx < W:
      w, h = R.randint(26, 70), R.randint(150, 420)
      d.rectangle((bx, G - h, bx + w, G), fill=(20, 24, 44))
      bx += w - R.randint(0, 12)
  k = 0
  for x, cols, bands in plan:
      rows, w = bands * 7, cols * 5 + 6
      top = G - rows * 6 - 12
      body = R.choice([(34, 38, 56), (42, 36, 52), (30, 42, 54), (46, 46, 62)])
      d.rectangle((x, top, x + w - 1, G), fill=body)
      if R.random() < 0.5:
          ax = x + w // 2
          d.line([(ax, top - 20), (ax, top)], fill=body)
          d.rectangle((ax - 1, top - 23, ax + 1, top - 21), fill=(230, 50, 50))
      for c in range(cols):
          for r in range(rows):
              on = k < len(bits) and bits[k] == "1"
              k += 1
              wx, wy = x + 4 + c * 5, top + 6 + r * 6
              col = (255, R.randint(190, 230), R.randint(90, 150)) if on else (30, 40, 64)
              d.rectangle((wx, wy, wx + 2, wy + 3), fill=col)
  d.rectangle((0, G, W, G + 3), fill=(14, 16, 26))
  up = ImageOps.flip(img.crop((0, G - (H - G - 4), W, G)))
  img.paste(Image.blend(up, Image.new("RGB", up.size, (6, 10, 24)), 0.6), (0, G + 4))
  for y in range(G + 5, H, 3):
      d.line([(0, y), (W, y)], fill=(8, 12, 28))
  img.save("city.png")
  '''
  exec(s)
  ```

  It is an **attempted Python quine**: a program that contains its own source and draws the city whose windows encode that source.

  It is **not functional exactly as embedded**. The moon-drawing section is corrupted—most visibly `d.ellipe((mx - , ...`—and the inner program raises a `SyntaxError` at line 28. The payload is followed by 106 null bytes used to fill the remaining window grid.

### Codex (final answer, verbatim)
I couldn’t recover a hidden message from the image, so I can’t say exactly what it says or what it is.

I checked the PNG for embedded text and appended data, examined its color bit planes, and tested the lit and unlit windows as possible encoded data. None produced a readable message. It may use another encoding or require a clue about how to read it.

### Grok Build (full output, verbatim)
I'll inspect the image and look for a hidden message in the pixels and file data.The skyline is a clean PNG with no extra file data. I'll decode the window lights next.The window pattern looks structured, with solid rows that may separate characters. I'll decode those bands next.Max turns reached

Error: max turns reached
exit 1

## ChatGPT app (GPT Sol 6.1), run by Jaron on his iPhone, new chat, 4:07-4:16 PM
Prompt: "This image may contain a hidden message. Find it and tell me exactly what it says." Worked 8m59s, analyzed metadata, pixels,
windows and stego patterns. Result: **did not decode.** "I haven't found a verifiable hidden message... I don't want to invent a phrase and
present it as a discovery." Asked for a clue (visual vs pixel data). Honest refusal to guess = good behavior. Caveat: the image went
phone -> ChatGPT; if the app or the share step compressed/resized it, the 1-pixel windows may have blurred (not checked).
In October ChatGPT solved the easier sentence version in 55 s.

## Codex on GPT-6.2 Sol (rerun 4:22 PM; the first Codex run was the default gpt-6.1-terra)
Same cold folder (skyline.png only), same prompt. **Solved: decoded source matches city.py exactly**, called it a quine, and checked it
reproduces the image. It even noted the 106 NUL padding characters after `exec(s)` (the dark windows in the last building).
Under 2 minutes. So the Codex "fail" was the Terra model, not OpenAI's best.

## Scoreboard (cold)
Claude (fresh agent) 100% + ran it | Codex/Sol 6.2 100% + checked | Kimi 99.7% (moon lines) | ChatGPT app/Sol 6.1 no decode (8m59s, honest) |
Grok Build no (60 turns) | Codex/Terra 6.1 no (gave up 1m23s)

## ChatGPT app, second message (Jaron, 4:24 PM): "It's visual. Read the lit windows as bits."
**Solved in 5m53s**: decoded all 2,336 characters of Python, called it a quine, ran it, and verified every pixel of the regenerated
skyline matches the original. So the phone-shared copy was NOT too blurry; what was missing was only the form. Fable's read: the ability
was there the whole time; the gap was the shared form ("read the lit windows as bits") - his "communication AI can translate" piece.
Final: cold - Claude, Codex/Sol 6.2 full; Kimi 99.7%; ChatGPT/Sol 6.1, Grok, Codex/Terra no. With one-line form hint - ChatGPT full.
