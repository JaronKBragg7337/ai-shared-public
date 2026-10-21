(Little tiny brain) 


#!/usr/bin/env python3
"""
VEX UNIFIED BRAIN v3.6 — DUAL-BRAIN (ORIGINAL+ENHANCED), MULTI-SUFFIX, DUAL-GATE, SHELL-AWARE,
POLICY-PACKED, COMPLIANCE-MODULAR, SAFE-AST, FASTAPI/AIOHTTP/USB

SOVEREIGNTY_HASH: 73378298
"""

from __future__ import annotations

import argparse
import asyncio
import ast
import dataclasses
import hashlib
import hmac
import json
import os
import platform
import re
import sqlite3
import time
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Callable, Iterable

import psutil

try:
    from pydantic import BaseModel, Field
except Exception:
    raise RuntimeError("pydantic is required")

# Optional deps
try:
    import aiohttp
    HAS_AIOHTTP = True
except Exception:
    HAS_AIOHTTP = False

try:
    import torch
    HAS_TORCH = True
except Exception:
    HAS_TORCH = False

try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except Exception:
    HAS_GPIO = False

try:
    import rclpy
    from std_msgs.msg import String as RosString
    HAS_ROS2 = True
except Exception:
    HAS_ROS2 = False

try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    import uvicorn
    HAS_FASTAPI = True
except Exception:
    HAS_FASTAPI = False


SOVEREIGNTY_HASH = "73378298"
VERSION = "3.6.0-DUALBRAIN"

APP_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(APP_DIR, "vex_data")
AUDIT_DIR = os.path.join(DATA_DIR, "audit")
DB_DIR = os.path.join(DATA_DIR, "db")

DB_PATH = os.path.join(DB_DIR, "vex.db")
AUDIT_DB_PATH = os.path.join(AUDIT_DIR, "audit.db")
REGS_DB_PATH = os.path.join(DB_DIR, "regulations.db")
RESEARCH_DB_PATH = os.path.join(DB_DIR, "research_cache.db")

POLICY_PATH = os.path.join(DATA_DIR, "policy.json")
SETTINGS_PATH = os.path.join(DATA_DIR, "settings.json")
LEXICON_PATH = os.path.join(DATA_DIR, "lexicon.json")

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080

LOCATION_API = "https://ip-api.com/json"
PROTECTED_PLANET_TOKEN_ENV = "PROTECTED_PLANET_TOKEN"


def _ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(AUDIT_DIR, exist_ok=True)
    os.makedirs(DB_DIR, exist_ok=True)


def _load_json(path: str, default: dict) -> dict:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def _save_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    os.replace(tmp, path)


def _pydantic_dump(model: BaseModel) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()  # type: ignore[attr-defined]


class DeviceEnvironment(str, Enum):
    EMBEDDED_USB = "embedded_usb"
    LOCAL_DEV = "local_dev"
    ROBOT_OPS = "robot_ops"
    IOT_OPS = "iot_ops"
    EMERGENCY = "emergency"


class HealthState(str, Enum):
    NOMINAL = "nominal"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    EMERGENCY = "emergency"
    TERMINATED = "terminated"


class Settings(BaseModel):
    # Gates
    control_secret: str = Field(default="CHANGE_ME", description="HMAC secret for ::vexlock")
    lexicon_secret: str = Field(default="CHANGE_ME_TOO", description="HMAC secret for ::lexseal")

    # Gate policy
    require_dual_gate_for_critical: bool = True
    require_lexseal_for_critical: bool = True
    vexlock_max_skew_seconds: int = 30
    vexlock_nonce_ttl_seconds: int = 300

    # Runtime
    rate_limit_per_minute: int = 120
    allow_web_learning: bool = True
    allow_controls_register: bool = True
    allow_server: bool = True
    default_env: str = DeviceEnvironment.LOCAL_DEV.value

    # Default routing (dual-brain wrapper)
    default_engine_route: str = "both"   # original|enhanced|both|any
    default_engine_quorum: str = "all"   # all|any

    # Global fallback allow-list (policy packs override)
    allowed_actions: List[str] = Field(default_factory=lambda: ["*"])


class AuditLogger:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_utc TEXT NOT NULL,
                environment TEXT NOT NULL,
                health_state TEXT NOT NULL,
                event_type TEXT NOT NULL,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                decision TEXT NOT NULL,
                rationale TEXT,
                metadata TEXT
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_log(timestamp_utc)")
        conn.commit()
        conn.close()

    def log(
        self,
        event_type: str,
        actor: str,
        action: str,
        decision: str,
        environment: str,
        health_state: str,
        rationale: str = "",
        metadata: dict = None,
    ):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            INSERT INTO audit_log
            (timestamp_utc, environment, health_state, event_type, actor, action, decision, rationale, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                environment,
                health_state,
                event_type,
                actor,
                action,
                decision,
                rationale,
                json.dumps(metadata or {}, separators=(",", ":")),
            ),
        )
        conn.commit()
        conn.close()


@dataclass
class SystemHealth:
    state: HealthState
    components: Dict[str, bool]
    last_heartbeat: float
    failures: List[str]


class HealthMonitor:
    def __init__(self, audit: AuditLogger):
        self.audit = audit
        self.health = SystemHealth(
            state=HealthState.NOMINAL, components={}, last_heartbeat=time.time(), failures=[]
        )
        self._lock = asyncio.Lock()

    async def report_failure(self, component: str, error: str):
        async with self._lock:
            self.health.components[component] = False
            self.health.failures.append(f"{component}: {error}")
            healthy = sum(1 for v in self.health.components.values() if v)
            total = max(1, len(self.health.components))
            ratio = healthy / total
            old = self.health.state
            if ratio < 0.3:
                self.health.state = HealthState.CRITICAL
            elif ratio < 0.7:
                self.health.state = HealthState.DEGRADED
            if old != self.health.state:
                self.audit.log(
                    "health_change",
                    "system",
                    "state_transition",
                    f"{old} -> {self.health.state}",
                    "unknown",
                    self.health.state.value,
                )


class EmergencyController:
    def __init__(self, audit: AuditLogger, health: HealthMonitor):
        self.audit = audit
        self.health = health
        self._active = False
        self._lock = asyncio.Lock()

    async def activate(self, reason: str, actor: str = "autonomous"):
        async with self._lock:
            self._active = True
            self.health.health.state = HealthState.EMERGENCY
            self.audit.log(
                "emergency_activate",
                actor,
                "enter_emergency_mode",
                "ALLOW_ALL",
                DeviceEnvironment.EMERGENCY.value,
                HealthState.EMERGENCY.value,
                reason,
            )
            return {"emergency_active": True, "reason": reason}

    async def deactivate(self, actor: str = "autonomous"):
        async with self._lock:
            self._active = False
            self.audit.log(
                "emergency_deactivate",
                actor,
                "exit_emergency_mode",
                "RESTORED",
                "unknown",
                self.health.health.state.value,
                "Emergency resolved",
            )
            return {"emergency_active": False}

    def is_active(self) -> bool:
        return self._active


class RateLimiter:
    def __init__(self, limit_per_minute: int):
        self.limit = max(1, int(limit_per_minute))
        self._events: List[float] = []
        self._lock = asyncio.Lock()

    async def allow(self) -> bool:
        async with self._lock:
            now = time.time()
            cutoff = now - 60.0
            self._events = [t for t in self._events if t >= cutoff]
            if len(self._events) >= self.limit:
                return False
            self._events.append(now)
            return True


class LexiconEngine:
    DEFAULT_SUFFIXES = [
        "abracadabra",
        "vexlock",
        "lexseal",
        "policy",
        "env",
        "shell",
        "bridge",
        "mode",
    ]

    DEFAULT_TOOL_PREFIXES = [
        "system.",
        "hardware.",
        "controls.",
        "ros2.",
        "shell.",
        "policy.",
        "bridge.",
    ]

    def __init__(self, settings: Settings):
        self.settings = settings
        self.lex = _load_json(LEXICON_PATH, {})
        if not self.lex:
            self.lex = {
                "version": 1,
                "suffixes": list(self.DEFAULT_SUFFIXES),
                "tool_prefixes": list(self.DEFAULT_TOOL_PREFIXES),
            }
            _save_json(LEXICON_PATH, self.lex)

        self.suffixes = set(self.lex.get("suffixes", []))
        self.tool_prefixes = tuple(self.lex.get("tool_prefixes", []))

    def is_valid_suffix(self, name: str) -> bool:
        return name in self.suffixes

    def is_valid_tool(self, tool: str) -> bool:
        return isinstance(tool, str) and tool.startswith(self.tool_prefixes)

    def compute_lexseal(self, canonical_payload: str, ts: str, nonce: str) -> str:
        key = self.settings.lexicon_secret.encode("utf-8")
        msg = f"{canonical_payload}|{ts}|{nonce}".encode("utf-8")
        return hmac.new(key, msg, hashlib.sha256).hexdigest()

    def verify_lexseal(self, canonical_payload: str, ts: str, nonce: str, sig: str) -> bool:
        if not (canonical_payload and ts and nonce and sig):
            return False
        expected = self.compute_lexseal(canonical_payload, ts, nonce)
        return hmac.compare_digest(expected, sig)


class PolicyPacks:
    def __init__(self):
        self.doc = _load_json(POLICY_PATH, {})
        if not self.doc:
            self.doc = {
                "active_pack": "default",
                "packs": {
                    "default": {
                        "allowed_actions": ["*"],
                        "critical_tools": [
                            "hardware.motor_control",
                            "system.pull_resource",
                            "controls.register",
                            "ros2.publish",
                            "bridge.activate_shell",
                            "system.switch_mode",
                        ],
                        "critical_requires_dual_gate": True,
                        "critical_requires_lexseal": True,
                    },
                    "robot_ops": {
                        "allowed_actions": ["system.*", "hardware.*", "ros2.*", "shell.*", "policy.*", "bridge.*", "controls.register", "system.pull_resource"],
                        "critical_tools": ["hardware.motor_control", "ros2.publish", "bridge.activate_shell", "system.switch_mode"],
                        "critical_requires_dual_gate": True,
                        "critical_requires_lexseal": True,
                    },
                },
            }
            _save_json(POLICY_PATH, self.doc)

    def active_pack_name(self) -> str:
        return str(self.doc.get("active_pack", "default"))

    def set_active_pack(self, name: str):
        packs = self.doc.get("packs", {}) or {}
        if name in packs:
            self.doc["active_pack"] = name
            _save_json(POLICY_PATH, self.doc)

    def get_pack(self, name: Optional[str] = None) -> dict:
        packs = self.doc.get("packs", {}) or {}
        if name and name in packs:
            return packs[name]
        return packs.get(self.active_pack_name(), packs.get("default", {}))

    def allowed_actions(self, pack: dict) -> List[str]:
        return list(pack.get("allowed_actions", []))

    def critical_tools(self, pack: dict) -> List[str]:
        return list(pack.get("critical_tools", []))

    def critical_requires_dual_gate(self, pack: dict) -> bool:
        return bool(pack.get("critical_requires_dual_gate", True))

    def critical_requires_lexseal(self, pack: dict) -> bool:
        return bool(pack.get("critical_requires_lexseal", True))


@dataclass
class ComplianceContext:
    env: str
    actor: str
    shell_id: Optional[str]
    location: dict
    policy_pack: dict
    directives_present: Dict[str, bool]
    engine_route: str
    engine_quorum: str
    brain_name: str


@dataclass
class ComplianceResult:
    allowed: bool
    provider: str
    reason: str = ""
    metadata: dict = dataclasses.field(default_factory=dict)


class ComplianceProvider:
    name: str = "base"

    async def check(self, action: str, ctx: ComplianceContext) -> ComplianceResult:
        return ComplianceResult(True, self.name, "no-op")


class PolicyPackProvider(ComplianceProvider):
    name = "policy_pack"

    @staticmethod
    def _match(pattern: str, action: str) -> bool:
        if pattern == "*":
            return True
        if pattern.endswith(".*"):
            return action.startswith(pattern[:-2] + ".")
        return action == pattern

    async def check(self, action: str, ctx: ComplianceContext) -> ComplianceResult:
        allowed = ctx.policy_pack.get("allowed_actions", [])
        for p in allowed:
            if self._match(str(p), action):
                return ComplianceResult(True, self.name, "allowed_by_pack")
        return ComplianceResult(False, self.name, "denied_by_pack")


class LexiconProvider(ComplianceProvider):
    name = "lexicon"

    def __init__(self, lexicon: LexiconEngine):
        self.lexicon = lexicon

    async def check(self, action: str, ctx: ComplianceContext) -> ComplianceResult:
        if not self.lexicon.is_valid_tool(action):
            return ComplianceResult(False, self.name, "invalid_tool_token")
        return ComplianceResult(True, self.name, "ok")


class RegulationEngine(ComplianceProvider):
    name = "regulation_engine"

    def __init__(self, audit: AuditLogger, brain_name: str):
        self.audit = audit
        self.brain_name = brain_name
        self.cache: Dict[str, dict] = {}
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(REGS_DB_PATH)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS regulations (
                country TEXT,
                category TEXT,
                action TEXT,
                allowed INTEGER,
                reason TEXT,
                source_url TEXT,
                fetched_at INTEGER,
                expires_at INTEGER,
                PRIMARY KEY (country, category, action)
            )
            """
        )
        conn.commit()
        conn.close()

    async def check(self, action: str, ctx: ComplianceContext) -> ComplianceResult:
        country = (ctx.location or {}).get("country", "unknown")
        lat = (ctx.location or {}).get("lat")
        lon = (ctx.location or {}).get("lon")

        cache_key = f"{self.brain_name}:{country}:{action}"
        cached = self.cache.get(cache_key)
        if cached and cached.get("expires_at", 0) > time.time():
            return ComplianceResult(bool(cached["allowed"]), self.name, cached.get("reason", ""), cached)

        checks: List[dict] = []
        checks.append(await self._check_environmental(action, lat, lon))
        checks.append(await self._check_data_privacy(action, country, ctx))

        allowed = all(c.get("allowed", False) for c in checks)
        reason = "; ".join([f"{c.get('category')}={c.get('allowed')}" for c in checks])
        result = {"allowed": allowed, "reason": reason, "checks": checks, "expires_at": time.time() + 86400}
        self.cache[cache_key] = result
        self._store(country, action, result)
        return ComplianceResult(bool(allowed), self.name, reason, result)

    async def _check_environmental(self, action: str, lat: Optional[float], lon: Optional[float]) -> dict:
        if lat is None or lon is None:
            return {"category": "environmental", "allowed": True, "reason": "no_coords", "source": "Default"}

        protected = await self._is_protected_area(lat, lon)
        if protected and ("movement" in action or "motor" in action or "hardware.motor_control" in action):
            return {"category": "environmental", "allowed": False, "reason": "protected_area", "source": "protectedplanet"}

        return {"category": "environmental", "allowed": True, "reason": "ok", "source": "Default"}

    async def _is_protected_area(self, lat: float, lon: float) -> bool:
        token = os.getenv(PROTECTED_PLANET_TOKEN_ENV, "").strip()
        if not (HAS_AIOHTTP and token):
            return False
        try:
            url = f"https://api.protectedplanet.net/v3/protected_areas/search?lat={lat}&lon={lon}"
            headers = {"Authorization": f"Token token={token}"}
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status != 200:
                        return False
                    data = await resp.json()
                    return bool(data.get("results", []))
        except Exception:
            return False

    async def _check_data_privacy(self, action: str, country: str, ctx: ComplianceContext) -> dict:
        restricted_countries = {"Germany", "France", "Italy", "Spain", "Netherlands"}
        if ("camera" in action or "sensor" in action) and country in restricted_countries:
            return {"category": "data_privacy", "allowed": False, "reason": "consent_required", "source": "Default"}

        if ctx.brain_name == "enhanced":
            # Enhanced brain can apply stricter or alternative heuristics; kept permissive by default.
            return {"category": "data_privacy", "allowed": True, "reason": "enhanced_ok", "source": "EnhancedDefault"}

        return {"category": "data_privacy", "allowed": True, "reason": "ok", "source": "Default"}

    def _store(self, country: str, action: str, result: dict):
        try:
            conn = sqlite3.connect(REGS_DB_PATH)
            for check in result.get("checks", []):
                conn.execute(
                    """
                    INSERT OR REPLACE INTO regulations
                    (country, category, action, allowed, reason, source_url, fetched_at, expires_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        country,
                        check.get("category", "unknown"),
                        action,
                        int(bool(check.get("allowed", False))),
                        check.get("reason", ""),
                        check.get("source", ""),
                        int(time.time()),
                        int(result.get("expires_at", time.time() + 86400)),
                    ),
                )
            conn.commit()
            conn.close()
        except Exception:
            pass


class DualGateProvider(ComplianceProvider):
    name = "dual_gate"
    async def check(self, action: str, ctx: ComplianceContext) -> ComplianceResult:
        return ComplianceResult(True, self.name, "delegated_to_executor")


class SafeASTEngine:
    ALLOWED_NODES = (
        ast.Expression,
        ast.BoolOp, ast.BinOp, ast.UnaryOp,
        ast.Compare,
        ast.Name, ast.Load,
        ast.Constant,
        ast.Subscript,
        ast.And, ast.Or, ast.Not,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
    )

    def compile(self, expr: str) -> Callable[[dict], Any]:
        tree = ast.parse(expr, mode="eval")
        self._validate(tree)

        compiled = compile(tree, "<safeast>", "eval")

        def _exec(inner_args: dict):
            safe_globals = {"__builtins__": {}}
            safe_locals = {"inner_args": inner_args}
            return eval(compiled, safe_globals, safe_locals)

        return _exec

    def _validate(self, node: ast.AST):
        for child in ast.walk(node):
            if not isinstance(child, self.ALLOWED_NODES):
                raise ValueError(f"disallowed_node:{child.__class__.__name__}")

            if isinstance(child, ast.Name):
                if child.id != "inner_args":
                    raise ValueError("disallowed_name")

            if isinstance(child, ast.Subscript):
                if not (isinstance(child.value, ast.Name) and child.value.id == "inner_args"):
                    raise ValueError("disallowed_subscript_target")
                sl = child.slice
                # Python 3.9+: ast.Index removed; slice is node directly
                if not (isinstance(sl, ast.Constant) and isinstance(sl.value, str)):
                    raise ValueError("disallowed_subscript_key")

            if isinstance(child, ast.Call):
                raise ValueError("disallowed_call")
            if isinstance(child, ast.Attribute):
                raise ValueError("disallowed_attribute")


@dataclass
class ShellInfo:
    shell_id: str
    capabilities: List[str]
    allowed_tools: List[str]
    shared_secret_hint: str = ""


class ShellRegistry:
    def __init__(self):
        self._shells: Dict[str, ShellInfo] = {}

    def register(self, shell_id: str, capabilities: List[str], allowed_tools: Optional[List[str]] = None):
        allowed_tools = allowed_tools or ["shell.*"]
        self._shells[shell_id] = ShellInfo(
            shell_id=shell_id,
            capabilities=list(capabilities or []),
            allowed_tools=list(allowed_tools or []),
        )

    def get(self, shell_id: str) -> Optional[ShellInfo]:
        return self._shells.get(shell_id)

    def is_known(self, shell_id: str) -> bool:
        return shell_id in self._shells


class MotorDriver:
    async def set_pwm(self, pin: int, speed: int, duration: float) -> dict:
        raise NotImplementedError


class GPIOMotorDriver(MotorDriver):
    async def set_pwm(self, pin: int, speed: int, duration: float) -> dict:
        if not HAS_GPIO:
            return {"error": "gpio_unavailable"}
        speed = max(0, min(100, int(speed)))
        duration = max(0.05, min(10.0, float(duration)))
        pin = int(pin)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, 100)
        pwm.start(speed)
        await asyncio.sleep(duration)
        pwm.stop()
        GPIO.cleanup()
        return {"motor": "controlled", "pin": pin, "speed": speed, "duration": duration}


class MockMotorDriver(MotorDriver):
    async def set_pwm(self, pin: int, speed: int, duration: float) -> dict:
        speed = max(0, min(100, int(speed)))
        duration = max(0.05, min(10.0, float(duration)))
        return {"motor": "mock", "pin": int(pin), "speed": speed, "duration": duration}


class HAL:
    def __init__(self):
        self.motor: MotorDriver = GPIOMotorDriver() if HAS_GPIO else MockMotorDriver()


class ImprovedLearner:
    def __init__(self, ai_core: "CodeBasedAI", brain_name: str):
        self.ai_core = ai_core
        self.brain_name = brain_name

    async def learn_from_url(self, url: str, capability_type: str = "auto") -> dict:
        if not HAS_AIOHTTP:
            return {"error": "aiohttp_unavailable"}
        if not url or not (url.startswith("http://") or url.startswith("https://")):
            return {"error": "invalid_url"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=15) as resp:
                    if resp.status != 200:
                        return {"error": f"fetch_failed:{resp.status}"}
                    text = await resp.text()
        except Exception as e:
            return {"error": f"fetch_error:{e}"}

        js = None
        try:
            js = json.loads(text)
        except Exception:
            js = None

        if capability_type == "auto":
            if isinstance(js, dict) and "type" in js:
                capability_type = str(js.get("type", "knowledge"))
            else:
                capability_type = "knowledge"

        if capability_type == "knowledge":
            self.ai_core.learn_from_data(text)
            return {"learned": "knowledge", "bytes": len(text.encode("utf-8", errors="ignore")), "brain": self.brain_name}

        if capability_type == "motor_pattern" and isinstance(js, dict):
            name = js.get("name")
            speeds = js.get("speeds", [])
            if not name or not isinstance(speeds, list) or not speeds:
                return {"error": "bad_motor_pattern"}
            self.ai_core.register_knowledge(name, {"type": "motor_pattern", "speeds": speeds, "brain": self.brain_name})
            return {"learned": name, "type": "motor_pattern", "brain": self.brain_name}

        return {"error": f"unknown_type:{capability_type}"}


class CodeBasedAI:
    def __init__(self, brain_name: str):
        self.brain_name = brain_name
        self.knowledge: Dict[str, Any] = {}
        self.history: List[dict] = []
        self.learner = ImprovedLearner(self, brain_name=brain_name)
        self.knowledge["hello"] = f"Hello. VEX Brain online ({brain_name})."
        self.knowledge["status"] = lambda: f"System nominal ({brain_name})."

    def register_knowledge(self, pattern: str, response: Any):
        self.knowledge[pattern] = response

    def learn_from_data(self, data: str):
        tokens = re.findall(r"[A-Za-z0-9_]{3,}", (data or "").lower())
        max_tokens = 20 if self.brain_name == "enhanced" else 10
        for t in tokens[:max_tokens]:
            if t not in self.knowledge:
                self.knowledge[t] = f"Learned:{t}:{self.brain_name}"

    def generate(self, prompt: str) -> str:
        p = (prompt or "").lower()
        for pattern, resp in self.knowledge.items():
            if pattern in p:
                if callable(resp):
                    try:
                        return str(resp())
                    except Exception:
                        return f"Callable knowledge error ({self.brain_name})."
                if isinstance(resp, (dict, list)):
                    return json.dumps(resp, ensure_ascii=False)
                return str(resp)
        return f"[{self.brain_name.upper()}] [ADAPTED] {prompt}"


class DualGate:
    def __init__(self, settings: Settings, brain_name: str):
        self.settings = settings
        self.brain_name = brain_name
        self._lock = asyncio.Lock()
        self.nonce_db_path = os.path.join(DB_DIR, f"nonce_{brain_name}.db")
        self._init_nonce_db()

    def _init_nonce_db(self):
        os.makedirs(DB_DIR, exist_ok=True)
        conn = sqlite3.connect(self.nonce_db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS nonces (
                nonce TEXT PRIMARY KEY,
                timestamp REAL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_nonce_time ON nonces(timestamp)")
        conn.commit()
        conn.close()

    def compute_sig(self, tool: str, ts: str, nonce: str) -> str:
        key = self.settings.control_secret.encode("utf-8")
        payload = f"{tool}|{ts}|{nonce}".encode("utf-8")
        return hmac.new(key, payload, hashlib.sha256).hexdigest()

    async def verify(self, tool: str, ts: str, nonce: str, sig: str) -> bool:
        if not (tool and ts and nonce and sig):
            return False
        try:
            ts_i = int(ts)
        except Exception:
            return False

        now = int(time.time())
        if abs(now - ts_i) > int(self.settings.vexlock_max_skew_seconds):
            return False

        async with self._lock:
            try:
                conn = sqlite3.connect(self.nonce_db_path)
                cur = conn.cursor()
                cur.execute(
                    "DELETE FROM nonces WHERE timestamp < ?",
                    (time.time() - float(self.settings.vexlock_nonce_ttl_seconds),),
                )
                cur.execute("SELECT 1 FROM nonces WHERE nonce = ?", (nonce,))
                if cur.fetchone():
                    conn.close()
                    return False
                expected = self.compute_sig(tool, ts, nonce)
                if not hmac.compare_digest(expected, sig):
                    conn.close()
                    return False
                cur.execute("INSERT INTO nonces (nonce, timestamp) VALUES (?, ?)", (nonce, time.time()))
                conn.commit()
                conn.close()
                return True
            except Exception:
                return False


class PermissionEngine:
    def __init__(self):
        self.location_cache: Optional[dict] = None

    async def get_location(self) -> dict:
        if self.location_cache:
            return self.location_cache
        if not HAS_AIOHTTP:
            self.location_cache = {"country": "unknown", "lat": None, "lon": None}
            return self.location_cache

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(LOCATION_API, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self.location_cache = {
                            "country": data.get("country", "unknown"),
                            "lat": data.get("lat"),
                            "lon": data.get("lon"),
                        }
                        return self.location_cache
        except Exception:
            pass

        self.location_cache = {"country": "unknown", "lat": None, "lon": None}
        return self.location_cache


@dataclass
class GateBundle:
    present: Dict[str, bool] = dataclasses.field(default_factory=dict)
    abracadabra: Optional[dict] = None
    vexlock: Optional[dict] = None
    lexseal: Optional[dict] = None
    policy: Optional[dict] = None
    env: Optional[dict] = None
    shell: Optional[dict] = None
    bridge: Optional[dict] = None
    mode: Optional[dict] = None


@dataclass
class ParsedDirectives:
    clean_text: str
    tool_groups: Dict[str, GateBundle]


class DirectiveParser:
    SUFFIX_PATTERN = re.compile(r"::([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)", re.DOTALL)

    @staticmethod
    def _parse_inner(inner: str) -> Tuple[str, Dict[str, str]]:
        inner = (inner or "").strip()
        if not inner:
            return "", {}
        parts = inner.split()
        tool = parts[0].strip()
        args: Dict[str, str] = {}
        for p in parts[1:]:
            if "=" in p:
                k, v = p.split("=", 1)
                args[k.strip()] = v.strip()
        return tool, args

    @classmethod
    def parse(cls, text: str, lexicon: LexiconEngine) -> ParsedDirectives:
        text = text or ""
        groups: Dict[str, GateBundle] = {}

        for m in cls.SUFFIX_PATTERN.finditer(text):
            suffix = m.group(1).strip()
            inner = m.group(2)

            if not lexicon.is_valid_suffix(suffix):
                continue

            tool, args = cls._parse_inner(inner)

            if suffix in {"policy", "env", "shell", "bridge", "mode"} and (not tool or tool in {"-", "none"}):
                tool = f"__{suffix}__"

            if tool:
                groups.setdefault(tool, GateBundle(present={}))
                groups[tool].present[suffix] = True
                setattr(groups[tool], suffix, args)

        clean = cls.SUFFIX_PATTERN.sub("", text).strip()
        return ParsedDirectives(clean_text=clean, tool_groups=groups)


class ToolResult(BaseModel):
    success: bool
    tool: str
    output: Any = None
    error: str = ""


class ToolExecutor:
    def __init__(
        self,
        audit: AuditLogger,
        health: HealthMonitor,
        emergency: EmergencyController,
        settings: Settings,
        lexicon: LexiconEngine,
        policy: PolicyPacks,
        permission: PermissionEngine,
        compliance: List[ComplianceProvider],
        ai: CodeBasedAI,
        dual_gate: DualGate,
        shells: ShellRegistry,
        hal: HAL,
        brain_name: str,
    ):
        self.audit = audit
        self.health = health
        self.emergency = emergency
        self.settings = settings
        self.lexicon = lexicon
        self.policy = policy
        self.permission = permission
        self.compliance = compliance
        self.ai = ai
        self.dual_gate = dual_gate
        self.shells = shells
        self.hal = hal
        self.brain_name = brain_name

        self.rate = RateLimiter(settings.rate_limit_per_minute)
        self.safeast = SafeASTEngine()

        self.tools: Dict[str, Callable] = {}
        self.active_shells: set = set()
        self._register_builtin_tools()

    def _register_builtin_tools(self):
        self.tools["system.detect_hardware"] = self._tool_detect_hardware
        self.tools["system.get_location"] = self.permission.get_location
        self.tools["system.pull_resource"] = self._tool_pull_resource
        self.tools["controls.register"] = self._tool_controls_register
        self.tools["hardware.motor_control"] = self._tool_motor_control
        self.tools["ros2.publish"] = self._tool_ros2_publish
        self.tools["shell.register"] = self._tool_shell_register
        self.tools["shell.capabilities"] = self._tool_shell_capabilities
        self.tools["policy.set_active"] = self._tool_policy_set_active
        self.tools["policy.get_active"] = self._tool_policy_get_active
        self.tools["bridge.activate_shell"] = self._tool_activate_shell
        self.tools["system.switch_mode"] = self._tool_switch_mode_stub

        if self.brain_name == "enhanced":
            self.tools["hardware.sensor_read"] = self._tool_sensor_read

    async def precheck(
        self,
        tool_name: str,
        args: dict,
        ctx: ComplianceContext,
        gates: GateBundle,
    ) -> ToolResult:
        if not await self.rate.allow():
            return ToolResult(success=False, tool=tool_name, error="rate_limited")

        if tool_name not in self.tools:
            return ToolResult(success=False, tool=tool_name, error="unknown_tool")

        if self.brain_name == "enhanced" and ctx.shell_id and ctx.shell_id not in self.active_shells:
            if tool_name not in {"bridge.activate_shell", "shell.register", "shell.capabilities"}:
                return ToolResult(success=False, tool=tool_name, error="shell_not_activated")

        for provider in self.compliance:
            r = await provider.check(tool_name, ctx)
            if not r.allowed:
                self.audit.log("compliance_denied", ctx.actor, tool_name, "DENIED", ctx.env, "nominal", r.reason, r.metadata)
                return ToolResult(success=False, tool=tool_name, error=f"denied:{provider.name}:{r.reason}")

        pack = ctx.policy_pack
        critical_tools = set(self.policy.critical_tools(pack))
        needs_dual = bool(self.policy.critical_requires_dual_gate(pack)) and bool(self.settings.require_dual_gate_for_critical)
        needs_lexseal = bool(self.policy.critical_requires_lexseal(pack)) and bool(self.settings.require_lexseal_for_critical)

        if not self.emergency.is_active() and tool_name in critical_tools:
            if needs_dual:
                if not gates.present.get("vexlock"):
                    return ToolResult(success=False, tool=tool_name, error="vexlock_missing")
                ts = str((gates.vexlock or {}).get("ts", ""))
                nonce = str((gates.vexlock or {}).get("nonce", ""))
                sig = str((gates.vexlock or {}).get("sig", ""))
                ok = await self.dual_gate.verify(tool_name, ts, nonce, sig)
                if not ok:
                    self.audit.log("dual_gate_denied", ctx.actor, tool_name, "DENIED", ctx.env, "nominal")
                    return ToolResult(success=False, tool=tool_name, error="vexlock_denied")

            if needs_lexseal:
                if not gates.present.get("lexseal"):
                    return ToolResult(success=False, tool=tool_name, error="lexseal_missing")
                canonical_payload = self._canonical_payload(tool_name, args, ctx)
                ts = str((gates.lexseal or {}).get("ts", ""))
                nonce = str((gates.lexseal or {}).get("nonce", ""))
                sig = str((gates.lexseal or {}).get("sig", ""))
                if not self.lexicon.verify_lexseal(canonical_payload, ts, nonce, sig):
                    return ToolResult(success=False, tool=tool_name, error="lexseal_denied")

        return ToolResult(success=True, tool=tool_name, output={"precheck": "ok", "brain": self.brain_name})

    async def execute(
        self,
        tool_name: str,
        args: dict,
        ctx: ComplianceContext,
        gates: GateBundle,
    ) -> ToolResult:
        pre = await self.precheck(tool_name, args, ctx, gates)
        if not pre.success:
            return pre

        try:
            fn = self.tools[tool_name]
            out = await fn(args, ctx, gates) if asyncio.iscoroutinefunction(fn) else fn(args, ctx, gates)
            return ToolResult(success=True, tool=tool_name, output=out)
        except Exception as e:
            await self.health.report_failure(tool_name, str(e))
            self.audit.log(
                "tool_error",
                ctx.actor,
                tool_name,
                "FAILED",
                ctx.env,
                self.health.health.state.value,
                metadata={"err": str(e), "trace": traceback.format_exc()},
            )
            return ToolResult(success=False, tool=tool_name, error=str(e))

    def _canonical_payload(self, tool_name: str, args: dict, ctx: ComplianceContext) -> str:
        safe = {
            "tool": tool_name,
            "args": dict(sorted((args or {}).items(), key=lambda kv: kv[0])),
            "env": ctx.env,
            "actor": ctx.actor,
            "shell_id": ctx.shell_id or "",
            "engine_route": ctx.engine_route,
            "engine_quorum": ctx.engine_quorum,
            "brain": self.brain_name,
        }
        return json.dumps(safe, separators=(",", ":"), sort_keys=True)

    def _tool_detect_hardware(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        gpu = bool(HAS_TORCH and torch.cuda.is_available())
        gpio = bool(HAS_GPIO)
        ros2 = bool(HAS_ROS2)
        if gpu:
            self.ai.register_knowledge("gpu_task", f"GPU available ({self.brain_name}).")
        return {
            "brain": self.brain_name,
            "gpu": gpu,
            "gpio": gpio,
            "ros2": ros2,
            "os": platform.system(),
            "cpu_count": psutil.cpu_count(logical=True),
            "mem_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        }

    async def _tool_pull_resource(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        if not self.settings.allow_web_learning:
            return {"error": "web_learning_disabled"}
        url = str(args.get("url", "")).strip()
        cap_type = str(args.get("type", "auto")).strip()
        return await self.ai.learner.learn_from_url(url, cap_type)

    def _tool_controls_register(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        if not self.settings.allow_controls_register:
            return {"error": "controls_register_disabled"}

        name = str(args.get("name", "")).strip()
        expr = str(args.get("logic", "")).strip()

        if not name or not re.match(r"^[a-zA-Z0-9_.\-]{3,64}$", name):
            return {"error": "invalid_name"}
        if not expr or len(expr) > 600:
            return {"error": "invalid_logic"}

        try:
            compiled = self.safeast.compile(expr)
        except Exception as e:
            return {"error": f"safeast_reject:{e}"}

        def tool_impl(inner_args: dict):
            return compiled(inner_args)

        tool_key = f"controls.{name}"
        self.tools[tool_key] = lambda inner_args, _ctx=ctx, _g=gates: tool_impl(inner_args)
        self.audit.log("control_registered", ctx.actor, tool_key, "OK", ctx.env, "nominal", metadata={"brain": self.brain_name})
        return {"registered": tool_key, "brain": self.brain_name}

    async def _tool_motor_control(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        pin = int(args.get("pin", 18))
        speed = int(args.get("speed", 50))
        duration = float(args.get("duration", 1.0))
        out = await self.hal.motor.set_pwm(pin, speed, duration)
        out["brain"] = self.brain_name
        return out

    def _tool_ros2_publish(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        if not HAS_ROS2:
            return {"error": "ros2_unavailable", "brain": self.brain_name}
        topic = str(args.get("topic", "/vex_topic"))
        message = str(args.get("message", "VEX message"))
        rclpy.init()
        node = rclpy.create_node("vex_publisher")
        pub = node.create_publisher(RosString, topic, 10)
        msg = RosString()
        msg.data = message
        pub.publish(msg)
        node.destroy_node()
        rclpy.shutdown()
        return {"published": True, "topic": topic, "message": message, "brain": self.brain_name}

    def _tool_shell_register(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        shell_id = str(args.get("id", "")).strip()
        caps_raw = str(args.get("caps", "")).strip()
        allowed_raw = str(args.get("allowed", "")).strip()
        if not shell_id or not re.match(r"^[a-zA-Z0-9_.\-]{3,64}$", shell_id):
            return {"error": "invalid_shell_id", "brain": self.brain_name}

        caps = [c for c in caps_raw.split(",") if c] if caps_raw else []
        allowed = [a for a in allowed_raw.split(",") if a] if allowed_raw else ["shell.*"]

        self.shells.register(shell_id, caps, allowed)
        self.audit.log("shell_registered", ctx.actor, shell_id, "OK", ctx.env, "nominal", metadata={"caps": caps, "allowed": allowed, "brain": self.brain_name})
        return {"shell_registered": shell_id, "caps": caps, "allowed": allowed, "brain": self.brain_name}

    def _tool_shell_capabilities(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        shell_id = str(args.get("id", "")).strip()
        info = self.shells.get(shell_id)
        if not info:
            return {"error": "unknown_shell", "brain": self.brain_name}
        return {"shell_id": shell_id, "capabilities": info.capabilities, "allowed_tools": info.allowed_tools, "brain": self.brain_name}

    def _tool_policy_set_active(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        name = str(args.get("name", "")).strip()
        self.policy.set_active_pack(name)
        return {"active_pack": self.policy.active_pack_name(), "brain": self.brain_name}

    def _tool_policy_get_active(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        return {"active_pack": self.policy.active_pack_name(), "pack": self.policy.get_pack(), "brain": self.brain_name}

    def _tool_sensor_read(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        pin = int(args.get("pin", 18))
        if HAS_GPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.IN)
            value = GPIO.input(pin)
            GPIO.cleanup()
            return {"value": value, "brain": self.brain_name}
        return {"value": "mock_0", "brain": self.brain_name}

    def _tool_activate_shell(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        shell_id = str(args.get("id", "")).strip()
        if not shell_id:
            return {"error": "no_id", "brain": self.brain_name}
        info = self.shells.get(shell_id)
        if not info:
            return {"error": "unknown_shell", "brain": self.brain_name}
        self.active_shells.add(shell_id)
        return {"activated": shell_id, "brain": self.brain_name}

    def _tool_switch_mode_stub(self, args: dict, ctx: ComplianceContext, gates: GateBundle) -> dict:
        target = str(args.get("target", "toggle")).lower()
        return {"requested": target, "brain": self.brain_name}


class VexBrain:
    def __init__(self, brain_name: str):
        self.brain_name = brain_name
        _ensure_dirs()

        raw = _load_json(SETTINGS_PATH, {})
        self.settings = Settings(**raw) if isinstance(raw, dict) else Settings()
        _save_json(SETTINGS_PATH, _pydantic_dump(self.settings))

        self.audit = AuditLogger(AUDIT_DB_PATH)
        self.health = HealthMonitor(self.audit)
        self.emergency = EmergencyController(self.audit, self.health)

        self.lexicon = LexiconEngine(self.settings)
        self.policy = PolicyPacks()
        self.permission = PermissionEngine()

        self.ai = CodeBasedAI(brain_name=brain_name)
        self.dual_gate = DualGate(self.settings, brain_name=brain_name)
        self.shells = ShellRegistry()
        self.hal = HAL()

        self.current_env = DeviceEnvironment(self.settings.default_env) if self.settings.default_env in DeviceEnvironment._value2member_map_ else DeviceEnvironment.LOCAL_DEV
        self.initialized = False

        self.compliance: List[ComplianceProvider] = [
            LexiconProvider(self.lexicon),
            PolicyPackProvider(),
            RegulationEngine(self.audit, brain_name=brain_name),
            DualGateProvider(),
        ]

        self.tools = ToolExecutor(
            audit=self.audit,
            health=self.health,
            emergency=self.emergency,
            settings=self.settings,
            lexicon=self.lexicon,
            policy=self.policy,
            permission=self.permission,
            compliance=self.compliance,
            ai=self.ai,
            dual_gate=self.dual_gate,
            shells=self.shells,
            hal=self.hal,
            brain_name=brain_name,
        )

    async def initialize(self):
        if self.initialized:
            return
        _ = await self.permission.get_location()
        self.audit.log(
            "startup",
            "system",
            "init",
            "complete",
            self.current_env.value,
            self.health.health.state.value,
            metadata={"pack": self.policy.active_pack_name(), "brain": self.brain_name},
        )
        self.initialized = True

    async def parse_context(
        self,
        prompt: str,
        actor: str,
        shell_id: Optional[str],
        engine_route: str,
        engine_quorum: str,
    ) -> Tuple[ParsedDirectives, dict, str, Optional[str], str, str]:
        parsed = DirectiveParser.parse(prompt, self.lexicon)
        location = await self.permission.get_location()

        pack_override = None
        env_override = None

        if "__policy__" in parsed.tool_groups:
            pg = parsed.tool_groups["__policy__"]
            pack_override = (pg.policy or {}).get("name")

        if "__env__" in parsed.tool_groups:
            eg = parsed.tool_groups["__env__"]
            env_override = (eg.env or {}).get("name")

        if pack_override:
            self.policy.set_active_pack(str(pack_override))

        if env_override and str(env_override) in DeviceEnvironment._value2member_map_:
            self.current_env = DeviceEnvironment(str(env_override))

        if "__shell__" in parsed.tool_groups:
            sg = parsed.tool_groups["__shell__"]
            if sg.shell:
                sid = str(sg.shell.get("id", "")).strip()
                if sid:
                    shell_id = sid
                    actor = "shell"

        if "__bridge__" in parsed.tool_groups:
            bg = parsed.tool_groups["__bridge__"]
            if bg.bridge:
                engine_route = str(bg.bridge.get("engine", engine_route)).strip().lower() or engine_route
                engine_quorum = str(bg.bridge.get("quorum", engine_quorum)).strip().lower() or engine_quorum

        return parsed, location, actor, shell_id, engine_route, engine_quorum

    async def precheck_tool(
        self,
        tool: str,
        args: dict,
        ctx: ComplianceContext,
        gates: GateBundle,
    ) -> ToolResult:
        return await self.tools.precheck(tool, args, ctx, gates)

    async def execute_tool(
        self,
        tool: str,
        args: dict,
        ctx: ComplianceContext,
        gates: GateBundle,
    ) -> ToolResult:
        return await self.tools.execute(tool, args, ctx, gates)

    def generate(self, clean_text: str) -> str:
        return self.ai.generate(clean_text)


class DualVexBrain:
    def __init__(self):
        self.brain_original = VexBrain(brain_name="original")
        self.brain_enhanced = VexBrain(brain_name="enhanced")
        self.engine_route = self.brain_original.settings.default_engine_route
        self.engine_quorum = self.brain_original.settings.default_engine_quorum
        self.initialized = False

    async def initialize(self):
        if self.initialized:
            return
        await self.brain_original.initialize()
        await self.brain_enhanced.initialize()
        self.initialized = True

    def _route_set(self, route: str) -> Tuple[bool, bool]:
        r = (route or "both").lower()
        if r == "original":
            return True, False
        if r == "enhanced":
            return False, True
        if r == "any":
            return True, True
        return True, True  # both

    def _quorum_all(self, quorum: str) -> bool:
        return (quorum or "all").lower() != "any"

    async def query(self, prompt: str, actor: str = "user", shell_id: Optional[str] = None) -> dict:
        await self.initialize()

        parsed_o, location_o, actor_o, shell_o, route_o, quorum_o = await self.brain_original.parse_context(
            prompt, actor, shell_id, self.engine_route, self.engine_quorum
        )

        route = route_o
        quorum = quorum_o

        use_o, use_e = self._route_set(route)
        quorum_all = self._quorum_all(quorum)

        # Mode switching is handled as a critical tool: system.switch_mode
        # Signature must target tool "system.switch_mode"
        # Args come from abracadabra: target=original|enhanced|both|any plus quorum=all|any
        # If route is reduced, mode switch still requires both brains to approve when quorum=all and route=both/any
        mode_switch_result: Optional[dict] = None
        if "system.switch_mode" in parsed_o.tool_groups:
            gates = parsed_o.tool_groups["system.switch_mode"]
            args = dict(gates.abracadabra or {})
            # Build context for each brain, then dual-precheck both; execute only once.
            policy_pack_o = self.brain_original.policy.get_pack()
            ctx_o = ComplianceContext(
                env=self.brain_original.current_env.value,
                actor=actor_o,
                shell_id=shell_o,
                location=location_o,
                policy_pack=policy_pack_o,
                directives_present=dict(gates.present or {}),
                engine_route=route,
                engine_quorum=quorum,
                brain_name="original",
            )

            policy_pack_e = self.brain_enhanced.policy.get_pack()
            ctx_e = ComplianceContext(
                env=self.brain_enhanced.current_env.value,
                actor=actor_o,
                shell_id=shell_o,
                location=location_o,
                policy_pack=policy_pack_e,
                directives_present=dict(gates.present or {}),
                engine_route=route,
                engine_quorum=quorum,
                brain_name="enhanced",
            )

            pre_o = await self.brain_original.precheck_tool("system.switch_mode", args, ctx_o, gates)
            pre_e = await self.brain_enhanced.precheck_tool("system.switch_mode", args, ctx_e, gates)

            ok = (pre_o.success and pre_e.success) if quorum_all else (pre_o.success or pre_e.success)
            if ok:
                target = str(args.get("target", "toggle")).lower()
                new_route = target
                if target == "toggle":
                    # toggle between original and enhanced, keep quorum
                    new_route = "enhanced" if self.engine_route == "original" else "original"
                if new_route in {"original", "enhanced", "both", "any"}:
                    self.engine_route = new_route
                q = str(args.get("quorum", quorum)).lower()
                if q in {"all", "any"}:
                    self.engine_quorum = q

                mode_switch_result = {
                    "requested": target,
                    "engine_route": self.engine_route,
                    "engine_quorum": self.engine_quorum,
                    "prechecks": {"original": pre_o.model_dump(), "enhanced": pre_e.model_dump()},
                }

        # Re-parse context after possible mode switch (route/quorum may have changed)
        parsed_o, location_o, actor_o, shell_o, route_o, quorum_o = await self.brain_original.parse_context(
            prompt, actor, shell_id, self.engine_route, self.engine_quorum
        )
        route = route_o
        quorum = quorum_o
        use_o, use_e = self._route_set(route)
        quorum_all = self._quorum_all(quorum)

        policy_pack_o = self.brain_original.policy.get_pack()
        policy_pack_e = self.brain_enhanced.policy.get_pack()

        results: List[dict] = []

        # Apply the same tool directives across brains; execute only if quorum satisfied.
        for tool, gates in parsed_o.tool_groups.items():
            if tool.startswith("__") and tool.endswith("__"):
                continue
            if tool == "system.switch_mode":
                continue

            args = dict(gates.abracadabra or {})
            directives_present = dict(gates.present or {})

            ctx_o = ComplianceContext(
                env=self.brain_original.current_env.value,
                actor=actor_o,
                shell_id=shell_o,
                location=location_o,
                policy_pack=policy_pack_o,
                directives_present=directives_present,
                engine_route=route,
                engine_quorum=quorum,
                brain_name="original",
            )
            ctx_e = ComplianceContext(
                env=self.brain_enhanced.current_env.value,
                actor=actor_o,
                shell_id=shell_o,
                location=location_o,
                policy_pack=policy_pack_e,
                directives_present=directives_present,
                engine_route=route,
                engine_quorum=quorum,
                brain_name="enhanced",
            )

            pre_o = None
            pre_e = None

            if use_o:
                pre_o = await self.brain_original.precheck_tool(tool, args, ctx_o, gates)
            if use_e:
                pre_e = await self.brain_enhanced.precheck_tool(tool, args, ctx_e, gates)

            if quorum_all:
                ok = True
                if use_o and (pre_o is None or not pre_o.success):
                    ok = False
                if use_e and (pre_e is None or not pre_e.success):
                    ok = False
            else:
                ok = False
                if use_o and pre_o is not None and pre_o.success:
                    ok = True
                if use_e and pre_e is not None and pre_e.success:
                    ok = True

            exec_out = None
            # Execute on both brains if route=="both" and tool is non-critical, else execute on selected brain(s).
            # For hardware/tool side effects, execute only once (original preferred).
            if ok:
                exec_brain = "original" if use_o else "enhanced"
                if use_o:
                    exec_out = await self.brain_original.execute_tool(tool, args, ctx_o, gates)
                else:
                    exec_out = await self.brain_enhanced.execute_tool(tool, args, ctx_e, gates)

                results.append(
                    {
                        "tool": tool,
                        "executed_on": exec_brain,
                        "args": args,
                        "prechecks": {
                            "original": pre_o.model_dump() if pre_o is not None else None,
                            "enhanced": pre_e.model_dump() if pre_e is not None else None,
                        },
                        "result": exec_out.model_dump(),
                    }
                )
            else:
                results.append(
                    {
                        "tool": tool,
                        "executed_on": None,
                        "args": args,
                        "prechecks": {
                            "original": pre_o.model_dump() if pre_o is not None else None,
                            "enhanced": pre_e.model_dump() if pre_e is not None else None,
                        },
                        "result": {"success": False, "tool": tool, "error": "quorum_not_met"},
                    }
                )

        # Generate response from both brains, then fuse.
        resp_o = self.brain_original.generate(parsed_o.clean_text) if use_o else ""
        resp_e = self.brain_enhanced.generate(parsed_o.clean_text) if use_e else ""

        if use_o and use_e:
            fused = {
                "original": resp_o,
                "enhanced": resp_e,
                "fused": resp_e if "?" not in parsed_o.clean_text else resp_o + "\n" + resp_e,
            }
            response = fused["fused"]
        elif use_o:
            fused = {"original": resp_o}
            response = resp_o
        else:
            fused = {"enhanced": resp_e}
            response = resp_e

        return {
            "version": VERSION,
            "sovereignty_hash": SOVEREIGNTY_HASH,
            "env": self.brain_original.current_env.value,
            "policy_pack": self.brain_original.policy.active_pack_name(),
            "location": location_o,
            "engine_route": self.engine_route,
            "engine_quorum": self.engine_quorum,
            "mode_switch": mode_switch_result,
            "response": response,
            "responses": fused,
            "directives": results,
        }


def build_fastapi(dual_brain: DualVexBrain):
    app = FastAPI(title="VEX Brain", version=VERSION)

    @app.get("/health")
    async def health():
        return {
            "state_original": dual_brain.brain_original.health.health.state.value,
            "state_enhanced": dual_brain.brain_enhanced.health.health.state.value,
            "failures_original": dual_brain.brain_original.health.health.failures[-10:],
            "failures_enhanced": dual_brain.brain_enhanced.health.health.failures[-10:],
            "engine_route": dual_brain.engine_route,
            "engine_quorum": dual_brain.engine_quorum,
        }

    @app.post("/query")
    async def query(payload: dict):
        prompt = str(payload.get("prompt", ""))
        actor = str(payload.get("actor", "user"))
        shell_id = payload.get("shell_id")
        out = await dual_brain.query(prompt, actor=actor, shell_id=shell_id if isinstance(shell_id, str) else None)
        return JSONResponse(out)

    return app


async def run_aiohttp_server(dual_brain: DualVexBrain, host: str, port: int):
    if not HAS_AIOHTTP:
        raise RuntimeError("aiohttp_unavailable")
    from aiohttp import web

    async def health(request):
        return web.json_response(
            {
                "state_original": dual_brain.brain_original.health.health.state.value,
                "state_enhanced": dual_brain.brain_enhanced.health.health.state.value,
                "engine_route": dual_brain.engine_route,
                "engine_quorum": dual_brain.engine_quorum,
            }
        )

    async def query(request):
        payload = await request.json()
        prompt = str(payload.get("prompt", ""))
        actor = str(payload.get("actor", "user"))
        shell_id = payload.get("shell_id")
        out = await dual_brain.query(prompt, actor=actor, shell_id=shell_id if isinstance(shell_id, str) else None)
        return web.json_response(out)

    app = web.Application()
    app.router.add_get("/health", health)
    app.router.add_post("/query", query)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()

    while True:
        await asyncio.sleep(3600)


def init_files():
    _ensure_dirs()

    if not os.path.exists(SETTINGS_PATH):
        _save_json(SETTINGS_PATH, _pydantic_dump(Settings()))

    if not os.path.exists(POLICY_PATH):
        _save_json(POLICY_PATH, PolicyPacks().doc)

    if not os.path.exists(LEXICON_PATH):
        _save_json(
            LEXICON_PATH,
            {
                "version": 1,
                "suffixes": LexiconEngine.DEFAULT_SUFFIXES,
                "tool_prefixes": LexiconEngine.DEFAULT_TOOL_PREFIXES,
            },
        )

    _ = AuditLogger(AUDIT_DB_PATH)
    try:
        sqlite3.connect(DB_PATH).close()
    except Exception:
        pass
    return True


def main():
    parser = argparse.ArgumentParser(description="VEX Unified Brain v3.6 (Dual Brain)")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--usb-mode", action="store_true")
    parser.add_argument("--server", action="store_true")
    args = parser.parse_args()

    if args.init:
        init_files()
        print("Initialized.")
        return

    dual_brain = DualVexBrain()

    if args.usb_mode:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(dual_brain.initialize())
        while True:
            try:
                prompt = input("USB Brain Query: ")
            except (EOFError, KeyboardInterrupt):
                break
            out = loop.run_until_complete(dual_brain.query(prompt))
            print(out.get("response", ""))
            if out.get("directives"):
                print(json.dumps(out["directives"], indent=2))
        return

    if args.server:
        if not dual_brain.brain_original.settings.allow_server:
            print("Server disabled in settings.")
            return

        if HAS_FASTAPI:
            app = build_fastapi(dual_brain)
            uvicorn.run(app, host=args.host, port=args.port, log_level="info")
            return

        if HAS_AIOHTTP:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(dual_brain.initialize())
            loop.run_until_complete(run_aiohttp_server(dual_brain, args.host, int(args.port)))
            return

        print("No server backend available (install fastapi+uvicorn or aiohttp).")
        return

    print("No mode selected. Use --usb-mode or --server.")


if __name__ == "__main__":
    main()