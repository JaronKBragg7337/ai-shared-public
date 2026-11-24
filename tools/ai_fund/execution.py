"""AI Fund Desk - execution interface. PAPER ADAPTER ONLY (built 2026-11-15).

The engine never talks to a market. It hands every order to a Broker. Today the only Broker that exists is PaperBroker,
which fills at the reference price (the next bar's open) plus modeled slippage and fees. No exchange account exists for
the company, and Claude/Codex never place real trades.

When a company brokerage/exchange account is funded LATER, a LiveBroker would be written here by the AI whose provider
terms allow it to execute (Grok / DeepSeek / Kimi), with limits read from the Control Room (Supabase system_settings via
tools/settings.py), and only after Jaron says the account exists. Until then get_broker() refuses anything but "paper".
"""
from dataclasses import dataclass


@dataclass
class Fill:
    symbol: str
    side: str          # "buy" | "sell"
    qty: float
    ref_price: float   # the bar open the order filled against
    price: float       # after slippage
    fee: float         # dollars
    asset_class: str


class Broker:
    mode = "abstract"

    def fill(self, symbol, side, qty, ref_price, asset_class) -> Fill:   # pragma: no cover - interface
        raise NotImplementedError


class PaperBroker(Broker):
    mode = "paper"

    def __init__(self, costs, stress=1.0):
        self.costs = costs          # {"etf": {"slip_bps": 5, "fee_bps": 0}, "crypto": {"slip_bps": 10, "fee_bps": 60}}
        self.stress = stress        # 3.0 = the 3x-cost stress line

    def fill(self, symbol, side, qty, ref_price, asset_class) -> Fill:
        c = self.costs[asset_class]
        slip = c["slip_bps"] * self.stress / 1e4
        px = ref_price * (1 + slip) if side == "buy" else ref_price * (1 - slip)
        fee = abs(qty) * px * c["fee_bps"] * self.stress / 1e4
        return Fill(symbol, side, abs(qty), ref_price, px, fee, asset_class)


class LiveBroker(Broker):
    """Placeholder so the plug-in point is obvious. Refuses on purpose: there is no funded company account."""
    mode = "live"

    def __init__(self, *a, **k):
        raise RuntimeError("No live broker: the AI Fund Desk is paper only until a company account is funded "
                           "and an AI whose terms allow execution is wired in (projects/ai-fund/DESIGN.md).")


def get_broker(config, stress=1.0) -> Broker:
    if config.get("mode") != "paper":
        raise RuntimeError("config.mode must be 'paper' - live execution does not exist")
    return PaperBroker(config["costs"], stress)
