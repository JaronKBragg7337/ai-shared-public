# Pages through the WHOLE Polymarket US activity history (read-only) and saves it to state/polymarket-activities-all.json.
# The desk tools only read the newest 100; this follows nextCursor to the start. Run with the polymarket venv python.
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
_kf = os.path.join(ROOT, "runtime", "polymarket-us-agent", "Polymarket.txt")  # same file the MCP service uses
_kid, _sec = open(_kf, encoding="utf-8-sig").read().strip().split(None, 1)
os.environ["POLYMARKET_KEY_ID"] = _kid; os.environ["POLYMARKET_SECRET_KEY"] = _sec.strip()
sys.path.insert(0, os.path.join(ROOT, "runtime", "polymarket-us-agent"))
import server as S
allacts, cur, pages = [], None, 0
with S._client(authenticated=True) as c:
    while True:
        params = {"limit": 100}
        if cur: params["cursor"] = cur
        r = c.portfolio.activities(params)
        r = r if isinstance(r, dict) else json.loads(S._json(r))
        acts = r.get("activities") or []; allacts += acts; pages += 1
        cur = r.get("nextCursor")
        if r.get("eof") or not cur or not acts or pages > 200: break
json.dump(allacts, open(os.path.join(ROOT, "state", "polymarket-activities-all.json"), "w"), indent=0)
ts = [a.get("trade", {}).get("aggressorExecution", {}).get("transactTime") or (a.get("accountBalanceChange") or {}).get("createTime") or "" for a in allacts]
ts = [t for t in ts if t]
print(f"pages {pages}, activities {len(allacts)}, oldest {min(ts) if ts else '?'}, newest {max(ts) if ts else '?'}")
