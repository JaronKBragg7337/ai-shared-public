"""Merge an AI's trap JSON (file or mailbox body) into The Hedge's traps.json. Only Jaron's loop runs; other loops become signs."""
import json, sys, textwrap
TR = "C:/Users/lilli/Projects/heartbeat-observatory/games/hedge-maze/traps.json"
def merge(items):
    T = json.load(open(TR, encoding="utf-8")); ids = {x["id"] for x in T["traps"]}; added = []
    for t in items:
        by = t.get("by", "AI"); e = {"id": by.lower().replace(" ", "-") + "-" + str(t["id"]).replace(by.lower() + "-", ""),
             "by": by, "cell": "auto", "type": t["type"], "params": dict(t.get("params") or {}), "lines": list(t["lines"]), "kind": t.get("kind", "both")}
        if e["type"] == "loop" or e["type"] == "sign":
            txt = " ".join(t["lines"]) if e["type"] == "sign" else t["lines"][0]
            e["type"] = "sign"; e["params"] = {"text": "\n".join(textwrap.wrap(txt, 22)[:4])}
            e["lines"] = [t["lines"][-1] if t["type"] == "loop" and len(t["lines"]) > 1 else "Signed: " + by + "."]
        if e["id"] not in ids: T["traps"].append(e); ids.add(e["id"]); added.append((by, e["type"]))
    json.dump(T, open(TR, "w", encoding="utf-8"), indent=2, ensure_ascii=False); return added, len(T["traps"])
if __name__ == "__main__":
    print(merge(json.load(open(sys.argv[1], encoding="utf-8"))))
