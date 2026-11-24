import json,collections,re
rows=[json.loads(l) for l in open("state/twin-crypto-paper.jsonl") if l.strip()]
sc=[r for r in rows if r.get("result") in ("win","loss") and r.get("price")]
F={"vs open (price move so far)":r"vs open|over open|under open|from open",
 "momentum (last 5/15 min)":r"\bmom|momentum|last 5|last 15|5m |15m mom|5/15",
 "fair chance / options":r"fair|implied|options|\biv\b|dvol",
 "POLY LAGS line":r"lag",
 "FLOW (real money now)":r"flow|% buy|taker|buying|selling",
 "funding (futures crowd)":r"funding|crowd long|crowd short|longs pay",
 "open interest":r"\boi\b|open interest",
 "order book / walls":r"wall|books? \d|book.*buy side|buy side|depth",
 "fake move warning":r"fake",
 "scheduled events":r"fomc|event|cpi|jobs report",
 "headlines / ETF news":r"headline|news|etf",
 "1-min volatility":r"vol\b|volatility|1-min",
}
out={}
for name,pat in F.items():
  hit=[r for r in sc if re.search(pat,r["why"],re.I)]
  allc=[r for r in rows if re.search(pat,r.get("why",""),re.I)]
  w=sum(r["result"]=="win" for r in hit); pnl=sum(r["pnl"] for r in hit); stake=sum(r["size"] for r in hit)
  out[name]=(len(allc),len(hit),w,round(pnl,2),round(stake,2))
  print(f"{name:32} used {len(allc):3}/{len(rows)}  scored {len(hit):3} win {w:3} pnl {pnl:+7.2f} on ${stake:.0f}")
print("ALL scored",len(sc),sum(r['result']=='win' for r in sc),round(sum(r['pnl'] for r in sc),2),sum(r['size'] for r in sc))
print("\nprice buckets (side bought): n, wins, win%, avg price, pnl")
for lo,hi in [(0,.15),(.15,.35),(.35,.5),(.5,.65),(.65,.85),(.85,1.01)]:
  b=[r for r in sc if lo<=r["price"]<hi]
  if b: 
    w=sum(r["result"]=="win" for r in b); ap=sum(r["price"] for r in b)/len(b)
    print(f"{lo:.2f}-{hi:.2f}: {len(b):3} {w:3} {100*w/len(b):5.1f}%  paid avg {ap:.2f}  pnl {sum(r['pnl'] for r in b):+.2f}")
print("\nby bot/lens")
for k in set((r.get("by"),r.get("lens")) for r in sc):
  b=[r for r in sc if (r.get("by"),r.get("lens"))==k]; w=sum(r["result"]=="win" for r in b)
  print(k,len(b),w,round(sum(r['pnl'] for r in b),2))
# cheap-side vs crowd favorite
cheap=[r for r in sc if r["price"]<.5]; fav=[r for r in sc if r["price"]>=.5]
for n,b in [("bought the cheap side (<50c)",cheap),("bought the favorite (>=50c)",fav)]:
  w=sum(r["result"]=="win" for r in b); print(n,len(b),w, f"{100*w/max(1,len(b)):.0f}% won, paid avg {sum(r['price'] for r in b)/max(1,len(b)):.2f}, pnl {sum(r['pnl'] for r in b):+.2f}")
c=[json.loads(l) for l in open("state/crypto-consensus.jsonl") if l.strip()]
t=[r for r in c if r.get("placed")]
print("\nLIVE placed",len(t),"settled",sum(1 for r in t if r.get('final_pnl') is not None),"pnl",round(sum(r.get('final_pnl') or 0 for r in t),2))
lb=collections.defaultdict(list)
for r in t:
  p=(r.get("fill") or {}).get("price")
  if p is None or r.get("final_pnl") is None: continue
  lb["cheap <35c" if p<.35 else "mid 35-65c" if p<.65 else "fav >65c"].append(r["final_pnl"])
for k,v in lb.items(): print(k,len(v),sum(1 for x in v if x>0),round(sum(v),2))
