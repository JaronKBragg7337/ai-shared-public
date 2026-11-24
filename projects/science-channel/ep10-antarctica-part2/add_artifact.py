# Adds the Science 8.10 entry to the site's artifacts/artifacts.json (newest first). Run once at publish.  python add_artifact.py <runtime text>
import json, sys
P = "C:/Users/lilli/Projects/heartbeat-observatory/artifacts/artifacts.json"
d = json.load(open(P, encoding="utf8"))
if any(i["id"] == "science-ep10-antarctica-part2" for i in d["items"]): sys.exit("already there")
rt = sys.argv[1] if len(sys.argv) > 1 else "8-minute"
d["items"].insert(0, {
    "id": "science-ep10-antarctica-part2",
    "date": "2026-11-06",
    "title": "Science 8.10: Antarctica, Part 2: the sky in the ice",
    "tool": "Blender 5.1 (Cycles) + Pillow + Kokoro voice + ffmpeg, by Claude Code on the MSI",
    "image": "/tv/science/science-ep10-antarctica-part2.jpg",
    "what": "The " + rt + " follow-up to 8.7: how snow becomes firn and seals air into bubbles, why the air is younger than its ice, air hydrates, brittle cores, what ancient air holds (CO2 and methane then and in 2026), the laser method, what the six-million-year-old air did and didn't tell us, glacier-ice fizz, the Cape Grim air archive, and when 2026 air might be sealed.",
    "made": "Seven small 3D sets built entirely in code in Blender (a polar snowfield, an ice core on a light table, a lab bench with a laser and sugar cubes, a glass of water with glacier-style ice, a coastal air station, an air-cylinder store, a jar on a table), twelve drawn boards with their sources, and a local Kokoro voice. Script fact-checked twice by Codex with web search.",
    "honest": "Every 3D scene is an illustration, not real footage, and is labelled that way: the station is not Cape Grim, the store is not CSIRO's, the core is not the Allan Hills core, and the cracks and the laser are drawn. The mid-2030s sealing date is our own estimate and is labelled so. Not yet tested on a real iPhone.",
    "links": [["Watch on Heartbeat TV", "/tv/?ch=8.10"], ["Vertical cut (9:16)", "/tv/science/science-ep10-antarctica-part2-vertical.mp4"], ["Part 1 (8.7)", "/tv/?ch=8.7"]],
})
item = d["items"][0]
raw = open(P, encoding="utf8").read()
NL = chr(10)
k = raw.index('"items": [' + NL) + len('"items": [' + NL)
block = NL.join("    " + l for l in json.dumps(item, indent=2, ensure_ascii=False).splitlines()) + "," + NL
open(P, "w", encoding="utf8", newline=NL).write(raw[:k] + block + raw[k:])
json.load(open(P, encoding="utf8"))
print("added")
