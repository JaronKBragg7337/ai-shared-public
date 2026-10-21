import json,sys
sys.path.insert(0,r"C:\Users\lilli\AI-Shared\tools")
import executor as X
m=X.Mcp()
# list tools
for name in ["tools/list","list_tools","polymarket_list_tools"]:
    try:
        print("TRY",name,str(m.call(name,{}))[:500])
    except Exception as e:
        print("TRY",name,"ERR",e)
# probe common book names
for name in ["polymarket_book","get_book","poly_get_book","polymarket_market_book","polymarket_bbo","polymarket_quote","polymarket_get_market","polymarket_market"]:
    try:
        r=m.call(name,{"market_slug":"aec-cfb-cin-arz-2026-10-03"})
        print(name, str(r)[:300])
    except Exception as e:
        print(name,"ERR",type(e).__name__,e)
# cancel helpers
for name in ["polymarket_cancel","polymarket_cancel_order","polymarket_cancel_orders"]:
    try:
        r=m.call(name,{"order_id":"x"})
        print(name, str(r)[:200])
    except Exception as e:
        print(name,"ERR",e)
print("executor attrs", [a for a in dir(X) if not a.startswith("_")][:40])
