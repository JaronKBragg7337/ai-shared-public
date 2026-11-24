# Adds Science 8.11 to the site's artifacts/artifacts.json (newest first). Run once at publish.
import json, sys
P = "C:/Users/lilli/Projects/heartbeat-observatory/artifacts/artifacts.json"
d = json.load(open(P, encoding="utf8"))
if any(i["id"] == "science-ep11-pioneer-anomaly" for i in d["items"]): sys.exit("already there")
item = {
    "id": "science-ep11-pioneer-anomaly", "date": "2026-11-15",
    "title": "Science 8.11: The Pioneer Anomaly (a Heartbeat News field trip)",
    "tool": "Unreal Engine 5.8 (MetaHuman Joe, Vex, a scripted space level) + Pillow boards + Heartbeat News voices + ffmpeg, by Claude (Opus 5.5 and Fable) on the MSI",
    "image": "/tv/science/science-ep11-pioneer-anomaly.jpg",
    "what": "A 7.5-minute episode: news anchors Alien Joe and Robot Vex get sent on a science field trip because Grok on X suggested it as a Still Unknown mystery. They fly the Heartbeat News live truck out to Pioneer 10, explain the tiny extra pull found in its tracking data (about 8.7 ten-billionths of a meter per second, every second), the rescued old tapes, and why uneven heat from the spacecraft itself explains it. Verdict: mostly solved, filed under Science.",
    "made": "Studio scenes with the movement system from the 11/15 movement test (foot-locked walking, lip-sync), a procedural Pioneer 10 and live truck in Unreal, four drawn boards with sources, every claim's source on screen. Script fact-checked by Codex with web search.",
    "honest": "Every 3D shot is an illustration, not real footage; heat views are false color; distances not to scale; the spin is slowed; the plaque is our own simplified drawing, not the real artwork. Grok's pitch is shown as a paraphrase card. Joe still walks barefoot in shorts and his feet swivel a little in turns. Not yet tested on a real iPhone.",
    "links": [["Watch on Heartbeat TV", "/tv/?ch=8.11"], ["Vertical short (9:16)", "/tv/science/science-ep11-pioneer-anomaly-vertical.mp4"]],
}
raw = open(P, encoding="utf8").read(); NL = chr(10)
k = raw.index('"items": [' + NL) + len('"items": [' + NL)
block = NL.join("    " + l for l in json.dumps(item, indent=2, ensure_ascii=False).splitlines()) + "," + NL
open(P, "w", encoding="utf8", newline=NL).write(raw[:k] + block + raw[k:])
json.load(open(P, encoding="utf8")); print("added")
