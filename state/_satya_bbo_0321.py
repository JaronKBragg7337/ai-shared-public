import json,sys
sys.path.insert(0,r"C:\Users\lilli\AI-Shared\tools")
import executor as X
m=X.Mcp()
for slug in ["aec-cfb-bayl-arzst-2026-10-03","aec-cfb-cin-arz-2026-10-03","aec-cfb-frest-washst-2026-10-03","aec-cfb-txst-sdst-2026-10-03","atc-intf-usa-mex-2026-10-03-usa"]:
    try:
        r=m.call("polymarket_bbo",{"slug":slug})
        print("BBO",slug,r)
    except Exception as e:
        print("BBO",slug,"ERR",e)
# cancel order schema probe - dry with wrong id should show fields
try:
    r=m.call("polymarket_cancel_order",{"market_slug":"aec-cfb-bayl-arzst-2026-10-03","order_id":"CWPJ7KN62YH8"})
    print("CANCEL",r)
except Exception as e:
    print("CANCEL ERR",e)
# also try orderId variants after
