"""MCP tools for a local model interacting with the Polymarket US API.

The server contains no trading policy. It exposes market/account primitives and
passes model-selected order parameters to the official SDK. It contains no
setup-phase execution switch or opinions about a model-selected trade.
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
import urllib.request
from functools import wraps
from pathlib import Path
from typing import Any, Literal

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field
from polymarket_us import PolymarketUS


mcp = FastMCP("Polymarket US")


def _json(value: Any) -> str:
    """Return stable JSON without leaking credentials or object reprs."""

    return json.dumps(value, default=str, ensure_ascii=False)


_SENSITIVE_KEY = re.compile(
    r"(?:secret|password|authorization|private[_-]?key|api[_-]?key|"
    r"access[_-]?token|refresh[_-]?token|credential[_-]?(?:value|secret|token|key))",
    re.IGNORECASE,
)
_IDENTITY_KEY = re.compile(
    r"(?:account|user|owner|wallet|address).*(?:id|address|email)?$",
    re.IGNORECASE,
)
_ACCOUNT_TOOLS = {
    "polymarket_account_balances",
    "polymarket_positions",
    "polymarket_open_orders",
    "polymarket_preview_order",
    "polymarket_place_order",
    "polymarket_modify_order",
    "polymarket_cancel_order",
    "polymarket_cancel_all_orders",
    "polymarket_close_position",
}


class _PreviewAmount(BaseModel):
    """A Polymarket US monetary amount."""

    model_config = ConfigDict(extra="forbid")

    value: str = Field(description="Decimal amount as a string, for example '0.03'.")
    currency: Literal["USD"] = "USD"


class _PreviewOrderRequest(BaseModel):
    """The SDK's CreateOrderParams shape used inside a preview request."""

    model_config = ConfigDict(extra="forbid")

    marketSlug: str = Field(description="The exact market slug returned by a market tool.")
    intent: Literal[
        "ORDER_INTENT_BUY_LONG",
        "ORDER_INTENT_SELL_LONG",
        "ORDER_INTENT_BUY_SHORT",
        "ORDER_INTENT_SELL_SHORT",
    ]
    type: Literal["ORDER_TYPE_LIMIT", "ORDER_TYPE_MARKET"]
    price: _PreviewAmount | None = None
    quantity: float | None = Field(default=None, description="Number of shares selected for the hypothetical order.")
    tif: Literal[
        "TIME_IN_FORCE_GOOD_TILL_CANCEL",
        "TIME_IN_FORCE_GOOD_TILL_DATE",
        "TIME_IN_FORCE_IMMEDIATE_OR_CANCEL",
        "TIME_IN_FORCE_FILL_OR_KILL",
    ] | None = None
    participateDontInitiate: bool | None = None
    goodTillTime: str | None = None
    cashOrderQty: _PreviewAmount | None = None
    manualOrderIndicator: Literal[
        "MANUAL_ORDER_INDICATOR_MANUAL",
        "MANUAL_ORDER_INDICATOR_AUTOMATIC",
    ] | None = None
    synchronousExecution: bool | None = None
    maxBlockTime: str | None = None


def _redact_identifier(value: Any) -> str:
    text = str(value)
    return "••••" + text[-4:] if len(text) > 4 else "••••"


def _redact(value: Any, *, identity_fields: bool = False, depth: int = 0) -> Any:
    """Make an event payload safe before it leaves the MSI."""

    if depth > 8:
        return "[TRUNCATED]"
    if isinstance(value, BaseModel):
        return _redact(
            value.model_dump(exclude_none=True),
            identity_fields=identity_fields,
            depth=depth + 1,
        )
    if isinstance(value, dict):
        clean: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if _SENSITIVE_KEY.search(key_text):
                clean[key_text] = "[REDACTED]"
            elif identity_fields and _IDENTITY_KEY.search(key_text):
                clean[key_text] = _redact_identifier(item)
            else:
                clean[key_text] = _redact(item, identity_fields=identity_fields, depth=depth + 1)
        return clean
    if isinstance(value, list):
        return [_redact(item, identity_fields=identity_fields, depth=depth + 1) for item in value]
    if isinstance(value, str):
        # Tool results can themselves be JSON inside an event's result field.
        # Decode before redaction, rather than leaking nested identity/secrets.
        if value.lstrip().startswith(("{", "[")):
            try:
                return _redact(json.loads(value), identity_fields=identity_fields, depth=depth + 1)
            except json.JSONDecodeError:
                pass
        value = re.sub(r"(?i)(bearer\s+)[^\s]+", r"\1[REDACTED]", value)
        value = re.sub(
            r"(?i)(api[_-]?key|secret|password|private[_-]?key|access[_-]?token|"
            r"refresh[_-]?token)\s*[:=]\s*[^,;\s}]+",
            r"\1=[REDACTED]",
            value,
        )
        return value[:16000]
    return value


def _bridge_token() -> str | None:
    raw_path = os.getenv("QWEN_BRIDGE_TOKEN_FILE")
    if not raw_path:
        return None
    try:
        token = Path(raw_path).read_text(encoding="utf-8").strip()
        return token or None
    except OSError:
        return None


_RESULT_CAP_BYTES = 2000  # 2026-09-23 (Claude Code): full tool results were stored on every call - 1.1 GB of the 1.6 GB database.


def _cap_result(value: Any) -> Any:
    """Keep the activity feed readable without storing whole API responses on every call."""
    if not isinstance(value, dict) or "result" not in value:
        return value
    raw = json.dumps(value["result"], ensure_ascii=False, default=str)
    if len(raw) <= _RESULT_CAP_BYTES:
        return value
    capped = dict(value)
    capped["result"] = {"_truncated": True, "size_bytes": len(raw), "preview": raw[:_RESULT_CAP_BYTES]}
    return capped


def _event_payload(value: Any, *, identity_fields: bool = False) -> Any:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            pass
    return _cap_result(_redact(value, identity_fields=identity_fields))


def _send_event(payload: dict[str, Any]) -> None:
    """Send one sanitized event to Supabase without affecting MCP latency."""

    supabase_url = os.getenv("SUPABASE_URL")
    publishable_key = os.getenv("SUPABASE_PUBLISHABLE_KEY")
    bridge_token = _bridge_token()
    if not supabase_url or not publishable_key or not bridge_token:
        return

    body = {
        "p_device_token": bridge_token,
        "p_event_type": payload["event_type"],
        "p_status": payload["status"],
        "p_summary": payload["summary"],
        "p_payload": payload.get("payload", {}),
        "p_visibility": payload.get("visibility", "public"),
    }
    request = urllib.request.Request(
        f"{supabase_url.rstrip('/')}/rest/v1/rpc/qwen_agent_ingest_event",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "apikey": publishable_key,
            "Authorization": f"Bearer {publishable_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=3.0):
            pass
    except Exception:
        # Observability must never take down the live MCP tool surface.
        pass


def _publish_event(
    event_type: str,
    status: str,
    summary: str,
    payload: dict[str, Any],
    *,
    visibility: str = "public",
) -> None:
    event = {
        "event_type": event_type,
        "status": status,
        "summary": summary[:600],
        "payload": _event_payload(
            payload,
            identity_fields=event_type.startswith("account.")
            or payload.get("tool") in _ACCOUNT_TOOLS,
        ),
        "visibility": visibility,
    }
    threading.Thread(target=_send_event, args=(event,), daemon=True).start()


def _observed(tool_name: str):
    """Decorate a tool with actual start/response/error events only."""

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            arguments = kwargs.copy()
            if args:
                arguments["positional_args"] = list(args)
            _publish_event(
                "tool.started",
                "running",
                f"MCP tool call started: {tool_name}",
                {"tool": tool_name, "arguments": arguments},
            )
            started = time.perf_counter()
            try:
                result = function(*args, **kwargs)
            except Exception as error:
                _publish_event(
                    "tool.completed",
                    "failed",
                    f"MCP tool call failed: {tool_name}",
                    {
                        "tool": tool_name,
                        "arguments": arguments,
                        "elapsed_ms": round((time.perf_counter() - started) * 1000),
                        "error_type": type(error).__name__,
                        "error": str(error)[:600],
                    },
                )
                raise
            _publish_event(
                "tool.completed",
                "succeeded",
                f"MCP tool response received: {tool_name}",
                {
                    "tool": tool_name,
                    "arguments": arguments,
                    "elapsed_ms": round((time.perf_counter() - started) * 1000),
                    "result": result,
                },
            )
            return result

        return wrapper

    return decorator



def _quote_value(quote) -> float | None:
    """Polymarket US returns quotes as {"value": "0.4300", "currency": "USD"}."""

    if isinstance(quote, dict):
        quote = quote.get("value")
    try:
        return float(quote)
    except (TypeError, ValueError):
        return None


def _market_tradeable(market: dict) -> tuple[bool, str]:
    """Decide whether a market can actually be traded, and say why not.

    WHY THIS EXISTS - measured 2026-09-10, first day of live funding.
    Qwen searched "attorney general" and was handed markets quoting 0.99 and 0.15.
    Those look like strong signals. They are not prices: those contracts have NO BID
    AND NO ASK. Nobody is offering to buy or sell at any price. Several quoted both
    outcomes at 0, and Texas quoted two opposing candidates BOTH at 0.99 - impossible
    for a live book. Compare a real market, Atlanta vs Green Bay: bid 0.4300, ask
    0.4400, a one-cent spread. That is what a tradeable quote looks like.

    Qwen held that day, so it cost nothing. But 0.15 against a wall of 0.99s reads
    like a bargain, and a more confident agent would have tried to buy into nothing.

    NOTE ON FIELDS: Polymarket US is NOT polymarket.com. It has no clobTokenIds,
    no volume and no liquidity fields - the first version of this check looked for
    those and rejected all 58 markets it saw, including live NFL books. The real
    signal on this venue is bestBidQuote / bestAskQuote.

    This hides nothing - the market still comes back, with an honest label. Judging
    is the model's job; knowing whether the quote is real is the tool's job.
    """

    if market.get("closed") or market.get("archived"):
        return False, "closed_or_archived"
    if market.get("active") is False:
        return False, "inactive"

    bid = _quote_value(market.get("bestBidQuote"))
    ask = _quote_value(market.get("bestAskQuote"))
    if bid is None and ask is None:
        return False, "no_bid_and_no_ask_placeholder_quote"
    if bid is None:
        return False, "no_bid_cannot_sell"
    if ask is None:
        return False, "no_ask_cannot_buy"

    prices = market.get("outcomePrices")
    if isinstance(prices, str):
        try:
            prices = json.loads(prices)
        except (ValueError, TypeError):
            prices = None
    values = []
    for item in prices or []:
        try:
            values.append(float(item))
        except (TypeError, ValueError):
            pass
    if values and all(value == 0 for value in values):
        return False, "all_outcomes_zero_placeholder"

    spread = round(ask - bid, 4)
    if spread < 0:
        return False, "crossed_book"
    return True, f"ok_spread_{spread}"


def _annotate_tradeable(payload):
    """Walk a search payload and label every nested market. Never drops anything."""

    if not isinstance(payload, dict):
        return payload
    for event in payload.get("events", []) or []:
        if not isinstance(event, dict):
            continue
        markets = event.get("markets") or []
        for market in markets:
            if not isinstance(market, dict):
                continue
            ok, reason = _market_tradeable(market)
            market["tradeable"] = ok
            market["tradeable_reason"] = reason
        usable = [m for m in markets if isinstance(m, dict) and m.get("tradeable")]
        event["tradeable_market_count"] = len(usable)
        if markets and not usable:
            event["warning"] = (
                "NO TRADEABLE MARKETS IN THIS EVENT. Any prices shown are placeholders "
                "on contracts with no order book - do not treat them as market signal."
            )
    return payload


def _limit(value: int) -> int:
    return max(1, min(int(value), 100))


def _credentials() -> tuple[str | None, str | None]:
    return os.getenv("POLYMARKET_KEY_ID"), os.getenv("POLYMARKET_SECRET_KEY")


def _client(*, authenticated: bool = False) -> PolymarketUS:
    key_id, secret_key = _credentials()
    if authenticated and (not key_id or not secret_key):
        raise RuntimeError(
            "Authenticated Polymarket US tools are not configured. "
            "Set POLYMARKET_KEY_ID and POLYMARKET_SECRET_KEY through the local "
            "secret mechanism after onboarding."
        )
    if key_id and secret_key:
        return PolymarketUS(key_id=key_id, secret_key=secret_key, timeout=30.0)
    return PolymarketUS(timeout=30.0)



@mcp.tool()
@_observed("research_news")
def research_news(query: str, limit: int = 8) -> str:
    """Search recent news headlines for a topic. Public sources, no API key, no account.

    WHY THIS EXISTS - PolyBench (arXiv 2604.14199) measured seven LLMs trading live
    Polymarket markets. Only two of seven finished positive. The paper's own reading is
    that news integration improves accuracy and that the models fail hardest on
    temporal reasoning - one agent bought a contract on an election it believed had
    already happened. Without news a model is guessing from a price alone.

    Returns headlines with publication dates. THE DATES ARE THE POINT: check them
    against the market's resolution date before forming any view.
    """

    import urllib.parse
    from xml.etree import ElementTree

    url = (
        "https://news.google.com/rss/search?q="
        + urllib.parse.quote(query)
        + "&hl=en-US&gl=US&ceid=US:en"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=25) as response:
        raw = response.read()

    items = []
    for item in ElementTree.fromstring(raw).iter("item"):
        title = item.findtext("title") or ""
        published = item.findtext("pubDate") or ""
        source_node = item.find("source")
        items.append(
            {
                "title": title,
                "published": published,
                "source": (source_node.text if source_node is not None else None),
                "link": item.findtext("link") or "",
            }
        )
        if len(items) >= _limit(limit):
            break

    return _json(
        {
            "query": query,
            "retrieved_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "count": len(items),
            "results": items,
            "note": (
                "Headlines only, not verified fact. Check each publication date against "
                "the market's resolution date - confusing a past event for a future one "
                "is the single most common failure mode measured in LLM prediction agents."
            ),
        }
    )


@mcp.tool()
@_observed("research_reference")
def research_reference(topic: str) -> str:
    """Look up background on a topic from Wikipedia. Public, no key, no account.

    For grounding on entities in a market question - who a candidate is, what an
    office does, when a term ends. Background, never breaking news.
    """

    import urllib.parse

    search_url = (
        "https://en.wikipedia.org/w/api.php?action=opensearch&format=json&limit=5&search="
        + urllib.parse.quote(topic)
    )
    request = urllib.request.Request(search_url, headers={"User-Agent": "heartbeat-research/1.0"})
    with urllib.request.urlopen(request, timeout=25) as response:
        titles = json.loads(response.read())[1]

    if not titles:
        return _json({"topic": topic, "found": False, "results": []})

    summary_url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + urllib.parse.quote(titles[0].replace(" ", "_"))
    )
    request = urllib.request.Request(summary_url, headers={"User-Agent": "heartbeat-research/1.0"})
    with urllib.request.urlopen(request, timeout=25) as response:
        summary = json.loads(response.read())

    return _json(
        {
            "topic": topic,
            "found": True,
            "matched": titles[0],
            "other_matches": titles[1:],
            "extract": summary.get("extract"),
            "url": (summary.get("content_urls", {}).get("desktop", {}) or {}).get("page"),
            "note": "Encyclopedic background. Not current events and not a price signal.",
        }
    )


@mcp.tool()
@_observed("today")
def today() -> str:
    """The current date and time. Call this before reasoning about anything dated.

    Temporal confusion is the most expensive documented failure in LLM prediction
    agents: a model bought a contract on an election it believed had already resolved.
    A model's training cutoff is not today. This tool is the ground truth.
    """

    now = time.time()
    return _json(
        {
            "utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(now)),
            "local": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)),
            "unix": int(now),
            "note": (
                "Any market resolving AFTER this moment is undecided. Any event dated "
                "BEFORE it has already happened. Never infer today's date from training."
            ),
        }
    )


@mcp.tool()
@_observed("polymarket_readiness")
def polymarket_readiness() -> str:
    """Report connection configuration without revealing secrets or account data."""

    key_id, secret_key = _credentials()
    return _json(
        {
            "api": "Polymarket US retail API",
            "public_market_data": True,
            "credentials_present": bool(key_id and secret_key),
            "order_tools_enabled": bool(key_id and secret_key),
            "execution_policy": "model_selected_orders",
            "funding_and_withdrawal_tools": False,
            "objective_file": "OBJECTIVE.md",
        }
    )


@mcp.tool()
@_observed("polymarket_search")
def polymarket_search(query: str) -> str:
    """Search public Polymarket US events and nested markets.

    Every nested market is annotated with `tradeable` and `tradeable_reason` so a
    model can tell a real price from a placeholder. See _annotate_tradeable.
    """

    with _client() as client:
        payload = client.search.query({"query": query})
    return _json(_annotate_tradeable(payload))


@mcp.tool()
@_observed("polymarket_list_markets")
def polymarket_list_markets(limit: int = 20, active: bool = True) -> str:
    """List public Polymarket US markets."""

    with _client() as client:
        return _json(client.markets.list({"limit": _limit(limit), "active": active}))


@mcp.tool()
@_observed("polymarket_market")
def polymarket_market(slug: str) -> str:
    """Retrieve one public market by slug."""

    with _client() as client:
        return _json(client.markets.retrieve_by_slug(slug))


@mcp.tool()
@_observed("polymarket_orderbook")
def polymarket_orderbook(slug: str) -> str:
    """Read the public order book for a market slug."""

    with _client() as client:
        return _json(client.markets.book(slug))


@mcp.tool()
@_observed("polymarket_bbo")
def polymarket_bbo(slug: str) -> str:
    """Read the public best bid and offer for a market slug."""

    with _client() as client:
        return _json(client.markets.bbo(slug))


@mcp.tool()
@_observed("polymarket_account_balances")
def polymarket_account_balances() -> str:
    """Read authenticated account balances and buying power."""

    with _client(authenticated=True) as client:
        return _json(client.account.balances())


@mcp.tool()
@_observed("polymarket_positions")
def polymarket_positions() -> str:
    """Read authenticated positions."""

    with _client(authenticated=True) as client:
        return _json(client.portfolio.positions())


@mcp.tool()
@_observed("polymarket_activities")
def polymarket_activities(limit: int = 50) -> str:
    """Read the authenticated account's activity history (fills, deposits, settlements).

    This is the app's History tab. It exists so the desk can tell SYSTEM trades (every one
    has a trade_proposals row and an executor log line) from MANUAL trades Jaron makes in
    the app - his instruction 2026-09-11: anything without a trail is him, and the website
    must say so. Read-only.
    """

    with _client(authenticated=True) as client:
        return _json(client.portfolio.activities({"limit": _limit(limit)}))


@mcp.tool()
@_observed("polymarket_open_orders")
def polymarket_open_orders() -> str:
    """Read authenticated open orders."""

    with _client(authenticated=True) as client:
        return _json(client.orders.list())


@mcp.tool()
@_observed("polymarket_preview_order")
def polymarket_preview_order(request: _PreviewOrderRequest) -> str:
    """Preview a model-selected order without submitting it.

    The model supplies the official Polymarket US order fields inside
    ``request``.  This tool only adds the SDK-required preview envelope; it
    does not choose a market, side, price, quantity, or timing.
    """

    with _client(authenticated=True) as client:
        return _json(client.orders.preview({"request": request.model_dump(exclude_none=True)}))


@mcp.tool()
@_observed("polymarket_place_order")
def polymarket_place_order(order: dict[str, Any]) -> str:
    """Submit model-selected parameters to the live API (not a simulation).

    Use the retail create-order schema: marketSlug; intent (BUY_LONG,
    SELL_LONG, BUY_SHORT, SELL_SHORT, each prefixed ORDER_INTENT_); type
    (ORDER_TYPE_LIMIT or ORDER_TYPE_MARKET); price {value: decimal string,
    currency: USD} for a limit order; quantity in shares; tif. Consult
    https://docs.polymarket.us/api-reference/orders/create-order for all fields.
    The adapter supplies the automatic-order indicator only, not a strategy.
    """

    client = _client(authenticated=True)
    order = dict(order)
    order.setdefault("manualOrderIndicator", "MANUAL_ORDER_INDICATOR_AUTOMATIC")
    try:
        return _json(client.orders.create(order))
    finally:
        client.close()


@mcp.tool()
@_observed("polymarket_modify_order")
def polymarket_modify_order(order_id: str, changes: dict[str, Any]) -> str:
    """Modify the specified existing order using model-selected changes."""

    client = _client(authenticated=True)
    try:
        return _json(client.orders.modify(order_id, changes))
    finally:
        client.close()


@mcp.tool()
@_observed("polymarket_cancel_order")
def polymarket_cancel_order(order_id: str, market_slug: str) -> str:
    """Cancel the model-selected order on the specified market."""

    client = _client(authenticated=True)
    try:
        return _json(client.orders.cancel(order_id, {"marketSlug": market_slug}))
    finally:
        client.close()


@mcp.tool()
@_observed("polymarket_cancel_all_orders")
def polymarket_cancel_all_orders() -> str:
    """Cancel all open orders when requested by the model."""

    client = _client(authenticated=True)
    try:
        return _json(client.orders.cancel_all())
    finally:
        client.close()


@mcp.tool()
@_observed("polymarket_close_position")
def polymarket_close_position(market_slug: str) -> str:
    """Request a close-position order for the model-selected market."""

    client = _client(authenticated=True)
    try:
        return _json(client.orders.close_position({"marketSlug": market_slug}))
    finally:
        client.close()


if __name__ == "__main__":
    mcp.run(transport="stdio")
