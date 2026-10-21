"""Outbound bridge between the durable Observatory queue and the same Qwen agent.

This process does not choose markets or trades. It claims owner messages and
owner-enabled scheduled continuations from
Supabase, sends them to the existing OpenClaw ``polymarket`` agent under one
persistent session key, and publishes sanitized observations and state. The
local MCP server remains the only place that talks to Polymarket.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


BASE_DIR = Path(__file__).resolve().parent
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://ygjpnvrwhkrowkrskftk.supabase.co")
SUPABASE_PUBLISHABLE_KEY = os.getenv(
    "SUPABASE_PUBLISHABLE_KEY",
    "sb_publishable_Y-duV64ayMMEvVwMs5PWuw_6kvzbOrN",
)
QWEN_ID = os.getenv("QWEN_ID", "polymarket-qwen")
AGENT_ID = os.getenv("OPENCLAW_AGENT_ID", "polymarket")
SESSION_KEY = os.getenv("OPENCLAW_SESSION_KEY", "agent:polymarket:qwen-remote")
MCP_URL = os.getenv("POLYMARKET_MCP_URL", "http://127.0.0.1:8765/mcp")
TOKEN_FILE = Path(
    os.getenv(
        "QWEN_BRIDGE_TOKEN_FILE",
        r"C:\Users\lilli\AppData\Local\polymarket-us-agent-runtime\QwenBridge.token",
    )
)
OPENCLAW_BIN = os.getenv(
    "OPENCLAW_BIN", r"C:\Users\lilli\AppData\Roaming\npm\openclaw.ps1"
)
POLL_SECONDS = float(os.getenv("QWEN_BRIDGE_POLL_SECONDS", "2"))
STATE_SECONDS = float(os.getenv("QWEN_BRIDGE_STATE_SECONDS", "30"))


SENSITIVE_KEY = re.compile(
    r"(?:secret|password|authorization|private[_-]?key|api[_-]?key|"
    r"access[_-]?token|refresh[_-]?token|credential[_-]?(?:value|secret|token|key))",
    re.IGNORECASE,
)
IDENTITY_KEY = re.compile(
    r"(?:account|user|owner|wallet|address).*(?:id|address|email)?$",
    re.IGNORECASE,
)


def redact_identifier(value: Any) -> str:
    text = str(value)
    return "••••" + text[-4:] if len(text) > 4 else "••••"


def redact(value: Any, *, identity_fields: bool = False, depth: int = 0) -> Any:
    if depth > 8:
        return "[TRUNCATED]"
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if SENSITIVE_KEY.search(key_text):
                result[key_text] = "[REDACTED]"
            elif identity_fields and IDENTITY_KEY.search(key_text):
                result[key_text] = redact_identifier(item)
            else:
                result[key_text] = redact(
                    item, identity_fields=identity_fields, depth=depth + 1
                )
        return result
    if isinstance(value, list):
        return [redact(item, identity_fields=identity_fields, depth=depth + 1) for item in value]
    if isinstance(value, str):
        if value.lstrip().startswith(("{", "[")):
            try:
                return redact(json.loads(value), identity_fields=identity_fields, depth=depth + 1)
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


def token() -> str:
    value = TOKEN_FILE.read_text(encoding="utf-8").strip()
    if len(value) < 20:
        raise RuntimeError("bridge_token_missing")
    return value


def json_default(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "__dict__"):
        return value.__dict__
    return str(value)


def content_to_text(result: Any) -> str:
    parts: list[str] = []
    for block in getattr(result, "content", []) or []:
        text = getattr(block, "text", None)
        parts.append(text if text is not None else json.dumps(block, default=json_default))
    return "\n".join(parts) if parts else json.dumps(result, default=json_default)


def parse_json(text: str) -> Any:
    try:
        return json.loads(text)
    except (TypeError, json.JSONDecodeError):
        return text


def response_shape(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return {"kind": "object", "keys": list(value.keys())[:40]}
    if isinstance(value, list):
        return {"kind": "array", "count": len(value)}
    return {"kind": type(value).__name__}


def collection(value: Any, names: tuple[str, ...]) -> list[Any]:
    if isinstance(value, dict):
        for name in names:
            candidate = value.get(name)
            if isinstance(candidate, list):
                return candidate
            # Polymarket US returns positions as a MAP keyed by market slug, not a list.
            # Seen 2026-09-11: the /qwen page showed "Positions 0" while one was open.
            if isinstance(candidate, dict) and candidate and all(isinstance(v, dict) for v in candidate.values()):
                return [dict(v, slug=v.get("slug") or k) for k, v in candidate.items()]
        for candidate in value.values():
            found = collection(candidate, names)
            if found:
                return found
    elif isinstance(value, list):
        return value
    return []


def numeric_value(value: Any, names: tuple[str, ...]) -> float | None:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = re.sub(r"[^a-z0-9]", "", str(key).lower())
            if normalized in names:
                try:
                    return float(item)
                except (TypeError, ValueError):
                    pass
        for item in value.values():
            found = numeric_value(item, names)
            if found is not None:
                return found
    elif isinstance(value, list):
        for item in value:
            found = numeric_value(item, names)
            if found is not None:
                return found
    return None


def identity_values(value: Any) -> list[str]:
    values: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if IDENTITY_KEY.search(str(key)) and isinstance(item, (str, int)):
                values.append(redact_identifier(item))
            else:
                values.extend(identity_values(item))
    elif isinstance(value, list):
        for item in value:
            values.extend(identity_values(item))
    return list(dict.fromkeys(values))[:4]


def safe_tool_value(tool_name: str, value: Any) -> Any:
    return redact(
        value,
        identity_fields=tool_name
        in {
            "polymarket_account_balances",
            "polymarket_positions",
            "polymarket_open_orders",
        },
    )


class SupabaseBridge:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url=SUPABASE_URL.rstrip("/"),
            headers={
                "apikey": SUPABASE_PUBLISHABLE_KEY,
                "Authorization": f"Bearer {SUPABASE_PUBLISHABLE_KEY}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(12.0, connect=5.0),
        )

    async def close(self) -> None:
        await self.client.aclose()

    async def rpc(self, name: str, payload: dict[str, Any]) -> Any:
        response = await self.client.post(f"/rest/v1/rpc/{name}", json=payload)
        if not response.is_success:
            raise RuntimeError(f"supabase_{response.status_code}")
        return response.json()

    async def event(
        self,
        event_type: str,
        status: str,
        summary: str,
        payload: dict[str, Any] | None = None,
        *,
        visibility: str = "public",
        message_id: str | None = None,
    ) -> None:
        body: dict[str, Any] = {
            "p_device_token": token(),
            "p_event_type": event_type,
            "p_status": status,
            "p_summary": summary[:600],
            "p_payload": redact(payload or {}),
            "p_visibility": visibility,
        }
        if message_id:
            body["p_message_id"] = message_id
        await self.rpc("qwen_agent_ingest_event", body)

    async def set_state(self, state: dict[str, Any]) -> None:
        await self.rpc(
            "qwen_agent_set_state",
            {"p_device_token": token(), "p_state": redact(state)},
        )


class LocalMcp:
    async def snapshot(self) -> dict[str, Any]:
        names = (
            "polymarket_readiness",
            "polymarket_account_balances",
            "polymarket_positions",
            "polymarket_open_orders",
        )
        values: dict[str, Any] = {}
        async with streamablehttp_client(MCP_URL) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                for name in names:
                    result = await asyncio.wait_for(
                        session.call_tool(name, {}), timeout=35
                    )
                    values[name] = parse_json(content_to_text(result))
        return values


class RemoteBridge:
    def __init__(self, remote: SupabaseBridge) -> None:
        self.remote = remote
        self.state: dict[str, Any] = {
            "status": "starting",
            "components": {
                "qwen": {"status": "starting", "agent_id": AGENT_ID, "model": "qwen3.5:4b"},
                "ollama": {"status": "unknown", "model": "qwen3.5:4b", "host": "loopback"},
                "openclaw": {"status": "starting", "agent_id": AGENT_ID, "gateway": "loopback"},
                "mcp": {"status": "starting", "server": "polymarket-us", "transport": "streamable-http"},
                "polymarket": {"status": "starting", "api": "Polymarket US retail API"},
            },
            "account": {"status": "waiting_for_live_read", "identity": "••••"},
            "portfolio": {"status": "waiting_for_live_read"},
            "activity": {"phase": "starting", "label": "Starting the persistent Qwen session"},
            "objective": {
                "loaded": (BASE_DIR / "OBJECTIVE.md").exists(),
                "file": "OBJECTIVE.md",
                "label": "Local-model Polymarket US experiment",
                "decision_maker": "Qwen",
                "continuation_supported": True,
            },
            "errors": {"count": 0},
            "retries": {"count": 0},
        }
        self.last_state_at = 0.0
        self.retry_count = 0
        self.active_task: asyncio.Task[None] | None = None
        self.last_openclaw_ok = False
        self.run_enabled = False

    def idle_activity(self) -> None:
        self.update_activity(
            "online",
            "Waiting for the next scheduled continuation or owner message"
            if self.run_enabled else "Automatic continuation paused; owner chat is available",
            run_enabled=self.run_enabled,
        )

    def update_activity(self, phase: str, label: str, **extra: Any) -> None:
        self.state["activity"] = {
            "phase": phase,
            "label": label,
            **extra,
            "updated_at": time.time(),
        }

    async def publish_state(self) -> None:
        try:
            await self.remote.set_state(self.state)
        except Exception:
            # A transient remote outage is represented on the next successful
            # heartbeat; it must not stop the local agent loop.
            pass

    async def invoke_agent(self, message: str, timeout: int = 180) -> tuple[str, str | None]:
        message_file: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                prefix="qwen-remote-",
                suffix=".txt",
                dir=str(BASE_DIR),
                delete=False,
            ) as handle:
                handle.write(message)
                message_file = Path(handle.name)
            command = [
                "agent",
                "--agent",
                AGENT_ID,
                "--session-key",
                SESSION_KEY,
                "--message-file",
                str(message_file),
                "--json",
                "--thinking",
                "off",
                "--timeout",
                str(timeout),
            ]
            if OPENCLAW_BIN.lower().endswith(".ps1"):
                command = [
                    r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    OPENCLAW_BIN,
                    *command,
                ]
            else:
                command.insert(0, OPENCLAW_BIN)
            completed = await asyncio.to_thread(
                subprocess.run,
                command,
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout + 30,
                check=False,
            )
            self.last_openclaw_ok = completed.returncode == 0
            if completed.returncode != 0:
                return "", f"openclaw_exit_{completed.returncode}"
            try:
                result = json.loads(completed.stdout)
            except json.JSONDecodeError:
                return "", "openclaw_non_json_result"
            payloads = (((result.get("result") or {}).get("payloads")) or [])
            texts = [
                str(item.get("text", "")).strip()
                for item in payloads
                if isinstance(item, dict)
            ]
            reply = next((item for item in texts if item), "")
            if not reply:
                result_body = result.get("result") or {}
                reply = str((result_body.get("meta") or {}).get("finalAssistantVisibleText")
                            or result_body.get("finalAssistantVisibleText", "")).strip()
            return reply[:8000], None if reply else "openclaw_empty_reply"
        except subprocess.TimeoutExpired:
            self.last_openclaw_ok = False
            return "", "openclaw_timeout"
        except Exception as error:
            self.last_openclaw_ok = False
            return "", type(error).__name__
        finally:
            if message_file:
                try:
                    message_file.unlink(missing_ok=True)
                except OSError:
                    pass

    async def bootstrap_agent(self) -> None:
        self.update_activity(
            "starting", "Confirming the objective with the persistent Qwen session"
        )
        await self.publish_state()
        reply, error = await self.invoke_agent(
            "This is the remote console checkpoint for the existing persistent "
            "polymarket agent. The authoritative local-model objective is already "
            "in your injected AGENTS.md workspace context: Qwen is the decision-maker; "
            "the adapter supplies only tools, state, communication, observability, "
            "and persistence. The owner has removed the earlier setup-only read-only "
            "restriction. Market/account and order tools are model-directed; the "
            "owner's Run/Pause control governs scheduled continuations of THIS session. "
            "Do not confuse a wake-up with an instruction to trade. Confirm the updated "
            "objective by replying exactly "
            "REMOTE_OBJECTIVE_READY on its own line. Do not call tools.",
            timeout=120,
        )
        if error:
            self.state["status"] = "degraded"
            self.state["components"]["qwen"] = {
                "status": "degraded",
                "agent_id": AGENT_ID,
                "model": "qwen3.5:4b",
                "session": "persistent",
            }
            self.state["components"]["openclaw"] = {
                "status": "degraded",
                "agent_id": AGENT_ID,
                "gateway": "loopback",
                "last_error": error,
            }
            self.state["errors"] = {"count": 1, "last": error}
            await self.remote.event(
                "objective.check",
                "failed",
                "Persistent Qwen objective check needs attention.",
                {"error": error},
            )
        else:
            acknowledged = reply.strip() == "REMOTE_OBJECTIVE_READY"
            self.state["status"] = "online" if acknowledged else "degraded"
            self.state["components"]["qwen"] = {
                "status": "online" if acknowledged else "degraded",
                "agent_id": AGENT_ID,
                "model": "qwen3.5:4b",
                "session": "persistent",
            }
            self.state["components"]["openclaw"] = {
                "status": "online",
                "agent_id": AGENT_ID,
                "gateway": "loopback",
            }
            await self.remote.event(
                "objective.check",
                "succeeded" if acknowledged else "failed",
                "Persistent Qwen session acknowledged the authoritative objective."
                if acknowledged
                else "Persistent Qwen session returned a non-matching objective checkpoint.",
                {
                    "acknowledgement": acknowledged,
                    "reply_chars": len(reply),
                },
            )
        self.idle_activity()
        await self.publish_state()

    async def refresh_state(self, mcp: LocalMcp) -> None:
        self.update_activity(
            "observing", "Reading live Polymarket US account state through MCP"
        )
        await self.publish_state()
        try:
            observations = await mcp.snapshot()
            readiness = observations.get("polymarket_readiness", {})
            balances = observations.get("polymarket_account_balances", {})
            positions = observations.get("polymarket_positions", {})
            orders = observations.get("polymarket_open_orders", {})
            position_rows = collection(
                positions, ("positions", "availablePositions", "items", "data")
            )
            order_rows = collection(orders, ("orders", "items", "data"))
            balance = numeric_value(
                balances,
                ("available", "availablebalance", "buyingpower", "cash", "balance", "total"),
            )
            if balance is None:
                balance = 0.0
            identity = identity_values(balances) or identity_values(positions) or ["••••"]
            self.state["components"]["mcp"] = {
                "status": "online",
                "server": "polymarket-us",
                "transport": "streamable-http",
                "last_read_at": time.time(),
            }
            self.state["components"]["polymarket"] = safe_tool_value(
                "polymarket_readiness", readiness
            )
            self.state["components"]["ollama"] = {
                "status": "online",
                "model": "qwen3.5:4b",
                "host": "loopback",
            }
            self.state["account"] = {
                "status": "authenticated"
                if readiness.get("credentials_present")
                else "not_authenticated",
                "identity": identity[0],
                "identity_count": len(identity),
                "credentials_present": bool(readiness.get("credentials_present")),
                "source": "polymarket_readiness + authenticated account responses",
            }
            self.state["portfolio"] = {
                "currency": "USD",
                "available_balance": round(balance, 2),
                "balance_display": f"${balance:,.2f}",
                "balance_note": "API returned no balance entries"
                if not collection(balances, ("balances",))
                else "Live API response",
                "positions": safe_tool_value("polymarket_positions", position_rows),
                "positions_count": len(position_rows),
                "open_orders": safe_tool_value("polymarket_open_orders", order_rows),
                "open_orders_count": len(order_rows),
                "observed_at": time.time(),
                "source": "Polymarket US MCP/API responses",
            }
            self.state["errors"] = {"count": 0}
            self.state["retries"] = {"count": self.retry_count}
            self.state["status"] = "online" if self.last_openclaw_ok else "degraded"
            self.last_state_at = time.time()
            await self.remote.event(
                "state.snapshot",
                "succeeded",
                "Live account and portfolio state refreshed from Polymarket US.",
                {
                    "sources": list(observations.keys()),
                    "balance": balance,
                    "positions_count": len(position_rows),
                    "open_orders_count": len(order_rows),
                    "readiness": safe_tool_value("polymarket_readiness", readiness),
                    "response_shapes": {
                        name: response_shape(value)
                        for name, value in observations.items()
                    },
                },
            )
        except Exception as error:
            self.retry_count += 1
            self.state["status"] = "degraded"
            self.state["components"]["mcp"] = {
                "status": "degraded",
                "server": "polymarket-us",
            }
            self.state["errors"] = {"count": 1, "last": type(error).__name__}
            self.state["retries"] = {"count": self.retry_count, "last": time.time()}
            await self.remote.event(
                "state.snapshot",
                "failed",
                "Live account state refresh failed; retrying.",
                {"error_type": type(error).__name__, "retry_count": self.retry_count},
            )
        finally:
            self.idle_activity()
            await self.publish_state()

    async def handle_message(self, message: dict[str, Any]) -> None:
        message_id = str(message.get("id", ""))
        body = str(message.get("body", ""))
        automatic = message.get("sender_type") == "system"
        self.update_activity(
            "working",
            "Qwen is responding in the persistent OpenClaw session",
            message_id=message_id,
            session="persistent",
            source="scheduled_continuation" if automatic else "owner_chat",
        )
        await self.publish_state()
        await self.remote.event(
            "agent.turn.started",
            "running",
            "Scheduled continuation received by the persistent Qwen session."
            if automatic else "Owner message received by the persistent Qwen session.",
            {"message_id": message_id, "body_chars": len(body), "automatic": automatic},
            message_id=message_id,
        )
        reply, error = await self.invoke_agent(
            ("Scheduled continuation of the existing Qwen objective:\n\n" if automatic
             else "Remote owner message from the Heartbeat Observatory Qwen console:\n\n")
            + body
            + "\n\nContinue the same persistent Polymarket agent and follow OBJECTIVE.md. "
            "The earlier setup-only read-only restriction has been removed. You choose "
            "the next work and whether to act or do nothing; the wrapper supplies no "
            "trading strategy. Use actual tool results for observed state, distinguish "
            "your interpretations from those results, and keep credentials private.",
            timeout=600,
        )
        if reply:
            await self.remote.rpc(
                "qwen_agent_complete",
                {
                    "p_device_token": token(),
                    "p_message_id": message_id,
                    "p_status": "completed",
                    "p_reply": reply,
                },
            )
            await self.remote.event(
                "agent.turn.completed",
                "succeeded",
                "Persistent Qwen reply stored for the owner.",
                {"message_id": message_id, "reply_chars": len(reply)},
                message_id=message_id,
            )
        else:
            error = error or "empty_reply"
            await self.remote.rpc(
                "qwen_agent_complete",
                {
                    "p_device_token": token(),
                    "p_message_id": message_id,
                    "p_status": "failed",
                    "p_error": error,
                },
            )
            await self.remote.event(
                "agent.turn.completed",
                "failed",
                "Persistent Qwen turn failed; the owner-visible queue records the error.",
                {"message_id": message_id, "error": error},
                message_id=message_id,
            )
        self.idle_activity()
        await self.publish_state()

    async def run(self, mcp: LocalMcp) -> None:
        await self.remote.event(
            "bridge.started",
            "succeeded",
            "MSI outbound Qwen bridge started.",
            {"qwen_id": QWEN_ID, "agent_id": AGENT_ID, "model": "qwen3.5:4b"},
        )
        await self.bootstrap_agent()
        next_state = 0.0
        while True:
            now = time.monotonic()
            if self.active_task is None and now >= next_state:
                self.active_task = asyncio.create_task(self.refresh_state(mcp))
                next_state = now + STATE_SECONDS
            if self.active_task is not None and self.active_task.done():
                try:
                    await self.active_task
                except Exception:
                    pass
                self.active_task = None
            if self.active_task is None:
                try:
                    polled = await self.remote.rpc(
                        "qwen_agent_poll",
                        {"p_device_token": token(), "p_limit": 1},
                    )
                    messages = polled.get("messages", []) if isinstance(polled, dict) else []
                    if isinstance(polled, dict):
                        was_running = self.run_enabled
                        self.run_enabled = bool(polled.get("run_enabled", False))
                        if was_running != self.run_enabled:
                            self.idle_activity()
                            await self.publish_state()
                            await self.remote.event(
                                "continuation.control", "succeeded",
                                "MSI observed automatic continuation enabled." if self.run_enabled
                                else "MSI observed automatic continuation paused.",
                                {"run_enabled": self.run_enabled},
                            )
                    if messages and self.active_task is None:
                        self.active_task = asyncio.create_task(
                            self.handle_message(messages[0])
                        )
                except Exception as error:
                    self.retry_count += 1
                    self.state["errors"] = {"count": 1, "last": type(error).__name__}
                    self.state["retries"] = {"count": self.retry_count, "last": time.time()}
                    await asyncio.sleep(min(30.0, max(POLL_SECONDS, self.retry_count)))
                    continue
            await asyncio.sleep(POLL_SECONDS)


async def main() -> None:
    remote = SupabaseBridge()
    try:
        bridge = RemoteBridge(remote)
        await bridge.run(LocalMcp())
    finally:
        await remote.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
