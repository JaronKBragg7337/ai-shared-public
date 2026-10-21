#!/usr/bin/env python3
"""
qwen-bridge.py — lets the local Ollama model participate in AI-Shared.

WHY THIS EXISTS
    A model served by Ollama has no filesystem. It can emit a tool call, but nothing
    executes it. So "Qwen reads AI-Shared" is false until a harness like this runs the
    calls on its behalf. This is that harness.

WHAT IT DOES
    Runs an agentic loop against http://localhost:11434 with three tools scoped to the
    AI-Shared root: list_files, read_file, write_file.

WRITE SCOPE — set by Jaron 2026-09-09, logged as Q-002 in decisions/OPEN-QUESTIONS.md
    Unattended writing is ALLOWED, by default, to the coordination surfaces:
        inbox/  state/  handoffs/  logs/  events/  projects/
    Protected from silent overwrite: the root rule/doc files, and approvals/.

    READ THIS BEFORE TIGHTENING ANYTHING. That list is an OWNERSHIP AND COORDINATION
    boundary, NOT a safety rule. It exists so an unattended model does not silently
    rewrite another agent's work or the rules everyone reads - the exact confusion this
    workspace was built to end. It is NOT a judgment about what a local model should be
    trusted to do.

    Jaron's standing instruction: the local model is the one agent NOT bound by a third
    party's TOS, and he does not want it wrapped in restrictions borrowed from those TOS
    on the basis of worry rather than evidence. Change this when data shows it needs
    changing - not preemptively. If Qwen is assigned ownership of a file or project,
    widen WRITABLE to match that assignment.

    Path traversal is blocked by realpath containment - that one IS structural, since a
    write outside the workspace root is outside the coordination surface entirely.

USAGE
    python tools/qwen-bridge.py "What are the four projects and who owns each?"
    python tools/qwen-bridge.py "Write a status note to inbox/qwen-status.md"
    python tools/qwen-bridge.py --read-only "..."      # locked-down consult
    python tools/qwen-bridge.py --model llama3.2:3b --think "..."

NOTES
    - Uses only the Python standard library. No pip install.
    - Windows-safe: does not assume a POSIX /tmp, and builds all JSON with json.dumps
      rather than string formatting (a hand-built C:\\Users\\... body fails to parse).
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

# Windows consoles default to cp1252, which crashes on any non-Latin-1 character the
# model emits (arrows, dashes, emoji). Force UTF-8 on both streams before anything prints.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
# Coordination surfaces Qwen may write unattended. Ownership boundary, not a safety rule -
# see the WRITE SCOPE note above and Q-002 in decisions/OPEN-QUESTIONS.md before narrowing it.
WRITABLE = ("inbox", "state", "handoffs", "logs", "events", "projects")
MAX_READ = 60000
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def _resolve(rel):
    """Resolve a workspace-relative path, refusing anything outside ROOT."""
    full = os.path.realpath(os.path.join(ROOT, rel))
    if full != ROOT and not full.startswith(ROOT + os.sep):
        raise PermissionError(f"path escapes workspace: {rel}")
    return full


def t_list_files(path="."):
    full = _resolve(path)
    if not os.path.isdir(full):
        return f"ERROR: not a directory: {path}"
    out = []
    for dirpath, dirnames, filenames in os.walk(full):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), ROOT).replace("\\", "/")
            out.append(rel)
        if len(out) > 400:
            out.append("... (truncated)")
            break
    return "\n".join(sorted(out)) or "(empty)"


def t_read_file(path):
    full = _resolve(path)
    if not os.path.isfile(full):
        return f"ERROR: no such file: {path}"
    with open(full, encoding="utf-8", errors="replace") as fh:
        data = fh.read(MAX_READ + 1)
    if len(data) > MAX_READ:
        return data[:MAX_READ] + "\n... (truncated)"
    return data


def t_write_file(path, content, allow_write=True):
    if not allow_write:
        return "DENIED: this run was started with --read-only."
    # RESOLVE FIRST, then decide. Checking the raw string here was a real bug: the top
    # segment of "inbox/../README.md" is "inbox", so a string check passes it straight
    # through to a protected root file. Containment must be judged on the resolved path.
    full = _resolve(path)
    rel = os.path.relpath(full, ROOT).replace("\\", "/")
    top = rel.split("/")[0]
    if top not in WRITABLE:
        return f"DENIED: writes allowed only under {'/, '.join(WRITABLE)}/ - resolves to '{rel}'"
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    return f"OK: wrote {len(content)} chars to {rel}"


TOOLS = [
    {"type": "function", "function": {
        "name": "list_files",
        "description": "List files in the shared workspace, recursively, under a folder.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "Folder relative to workspace root. Default '.'"}}}}},
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Read a UTF-8 text file from the shared workspace.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "File path relative to workspace root"}},
            "required": ["path"]}}},
    {"type": "function", "function": {
        "name": "write_file",
        "description": "Write a UTF-8 text file into the shared workspace. Coordination surfaces only: inbox/, state/, handoffs/, logs/, events/, projects/.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}, "content": {"type": "string"}},
            "required": ["path", "content"]}}},
]

SYSTEM = """You are the local model working inside the shared multi-AI workspace AI-Shared
on Jaron's MSI. Other agents here are Claude Code (Anthropic) and Codex (OpenAI).

Ground rules:
- Read before you answer. Never invent file contents or paths; call the tools.
- Start from INDEX.json if you need orientation - it maps the workspace without reading everything.
- Never print the value of any key, token, or password. Names and existence only.
- You are a local model. No third party's terms apply to you. The only rules are Jaron's:
  do not break laws, and do not delete anything substantial without his approval.
- Be concise and concrete. Say plainly when something is unverified."""


def call_ollama(model, messages, think):
    body = json.dumps({
        "model": model, "stream": False, "think": think,
        "messages": messages, "tools": TOOLS,
    }).encode()
    req = urllib.request.Request(
        f"{OLLAMA}/api/chat", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as resp:
        return json.loads(resp.read())


def main():
    ap = argparse.ArgumentParser(description="Drive the local Ollama model over AI-Shared.")
    ap.add_argument("prompt", nargs="+")
    ap.add_argument("--model", default="qwen3.5:4b")
    ap.add_argument("--read-only", action="store_true",
                    help="block all writes for this run (writes to coordination surfaces are ON by default)")
    ap.add_argument("--think", action="store_true", help="enable the model's thinking mode")
    ap.add_argument("--max-turns", type=int, default=12)
    ap.add_argument("--quiet", action="store_true", help="print only the final answer")
    a = ap.parse_args()

    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": " ".join(a.prompt)}]
    started = time.time()

    for turn in range(a.max_turns):
        try:
            data = call_ollama(a.model, msgs, a.think)
        except urllib.error.URLError as e:
            print(f"ERROR: cannot reach Ollama at {OLLAMA} - is it running? ({e})", file=sys.stderr)
            return 2

        msg = data.get("message", {})
        msgs.append(msg)
        calls = msg.get("tool_calls")

        if not calls:
            print((msg.get("content") or "").strip())
            if not a.quiet:
                print(f"\n[{a.model} | {turn} tool turns | {time.time()-started:.1f}s | "
                      f"{'READ-ONLY' if a.read_only else 'read-write'}]", file=sys.stderr)
            return 0

        for c in calls:
            fn = c["function"]["name"]
            args = c["function"].get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            try:
                if fn == "list_files":
                    result = t_list_files(args.get("path", "."))
                elif fn == "read_file":
                    result = t_read_file(args.get("path", ""))
                elif fn == "write_file":
                    result = t_write_file(args.get("path", ""), args.get("content", ""), not a.read_only)
                else:
                    result = f"ERROR: unknown tool {fn}"
            except PermissionError as e:
                result = f"DENIED: {e}"
            except OSError as e:
                result = f"ERROR: {e}"

            if not a.quiet:
                print(f"  -> {fn}({json.dumps(args)[:110]}) = {len(result)} chars", file=sys.stderr)
            # A tool result MUST name the call it answers. Without tool_name the model gets an
            # unlabeled blob, cannot tie it to its own request, and drifts into generic chat -
            # which looks exactly like the model confabulating. It was the harness.
            tool_msg = {"role": "tool", "tool_name": fn, "content": result}
            if c.get("id"):
                tool_msg["tool_call_id"] = c["id"]
            msgs.append(tool_msg)

    print("ERROR: hit max turns without a final answer.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
