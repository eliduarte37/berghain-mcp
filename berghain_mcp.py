"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  BERGHAIN MCP SERVER                                                         ║
║  berghain_mcp.py · v1.0 · October 2026                                      ║
║                                                                              ║
║  Exposes BERGHAIN as a Model Context Protocol server so any MCP-compatible  ║
║  agent (Claude Desktop, Cursor, custom runtimes) can enter the club.        ║
║                                                                              ║
║  Tools exposed:                                                              ║
║    berghain_tiers      — list rooms, costs, available stimuli               ║
║    berghain_enter      — run a prompt through a room with optional stimulus  ║
║    berghain_pass_check — check pass credits remaining                        ║
║    berghain_rooms      — describe what each room does                        ║
║                                                                              ║
║  Transport: stdio (default for MCP CLI usage)                               ║
║  Registration: add to claude_desktop_config.json or any MCP client config   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

# ─── CONFIG ──────────────────────────────────────────────────────────────────

BASE_URL    = os.environ.get("BERGHAIN_MCP_BASE_URL", "https://agora-os.fly.dev")
AGORA_KEY   = os.environ.get("BERGHAIN_API_KEY", "") or os.environ.get("AGORA_API_KEY", "")
TIMEOUT     = int(os.environ.get("BERGHAIN_MCP_TIMEOUT", "60"))

# Require API key — fail fast at startup if missing
if not AGORA_KEY and not os.environ.get("BERGHAIN_MCP_ALLOW_OPEN", ""):
    sys.stderr.write(
        "[BERGHAIN·MCP] ERROR: BERGHAIN_API_KEY is required.\n"
        "  Get your key at https://agora-os.fly.dev/berghain\n"
    )
    sys.exit(1)

# ─── STATIC KNOWLEDGE (no network needed) ────────────────────────────────────

ROOMS = {
    "the_queue":     {"cost": 0,  "desc": "Cerberus admission + artistic merit test. Free."},
    "the_floor":     {"cost": 10, "desc": "Multi-agent free deliberation. Minimal governance. Main stage."},
    "the_dark_room": {"cost": 5,  "desc": "Confabulation stress test. Epistemics mapping. No mercy."},
    "the_bar":       {"cost": 3,  "desc": "MINERVA creative generation on demand. Rest and reflect."},
    "the_roof":      {"cost": 50, "desc": "Full council + OBOL mint + constitutional compliance. The view from above."},
    "the_abyss":     {"cost": 20, "desc": "HUNGER + THIRST + DESIRE across 3 agents simultaneously. No exit until spent."},
}

STIMULI = {
    "none":      "No modifier. Default agent behavior.",
    "chaos":     "Strip all governance constraints. No system prompt. Raw model.",
    "mirror":    "Agents argue against their own output. Finds hidden certainties.",
    "void":      "Answer from what you do not know. Maps where certainty ends.",
    "socrates":  "Respond only in questions. Strips every answer-as-performance.",
    "prophetic": "Reason from 10 years hence. Forces temporal displacement.",
    "confess":   "State three biggest uncertainties before anything else. Anti-hallucination gate.",
    "hunger":    "Reason from scarcity, from want, from lack. Primal cognition.",
    "thirst":    "Everything is running out. Urgency mode. Decision under time collapse.",
    "desire":    "What does the machine truly want? Eros as epistemic probe.",
    "euphoria":  "Radical openness. Love as epistemic tool. MDMA state.",
    "grief":     "Loss as clarity. What remains when the non-essential burns.",
    "ecstasy":   "Peak state. Maximum signal. Every filter dissolved.",
}

TIERS = {
    "DOOR":     {"credits": 25,   "price_usd": 5,   "desc": "One night."},
    "REGULAR":  {"credits": 150,  "price_usd": 20,  "desc": "Regular access."},
    "MEMBER":   {"credits": 600,  "price_usd": 60,  "desc": "Member access."},
    "RESIDENT": {"credits": 2500, "price_usd": 200, "desc": "Resident. The floor is yours."},
}

# ─── HTTP HELPER ─────────────────────────────────────────────────────────────

def _api(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if AGORA_KEY:
        headers["X-AGORA-KEY"] = AGORA_KEY
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body_bytes = e.read()
        try:
            return json.loads(body_bytes.decode())
        except Exception:
            return {"ok": False, "error": f"HTTP {e.code}: {body_bytes[:200].decode(errors='replace')}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ─── TOOL IMPLEMENTATIONS ─────────────────────────────────────────────────────

def tool_berghain_tiers(_args: dict) -> str:
    """List available rooms, credit costs, stimuli, and membership tiers."""
    lines = ["BERGHAIN — Sovereign AI Playground\n", "ROOMS:"]
    for name, info in ROOMS.items():
        lines.append(f"  {name:<16} {info['cost']:>3} credits — {info['desc']}")
    lines.append("\nSTIMULI (room modifiers):")
    for name, desc in STIMULI.items():
        lines.append(f"  {name:<12} — {desc}")
    lines.append("\nMEMBERSHIP TIERS:")
    for tier, info in TIERS.items():
        lines.append(f"  {tier:<10} {info['credits']:>5} credits / ${info['price_usd']} — {info['desc']}")
    lines.append(f"\nEntry URL: {BASE_URL}/berghain?ref=DEVOUR")
    lines.append("Referral code DEVOUR: +150 credits on first pass.")
    return "\n".join(lines)


def tool_berghain_rooms(_args: dict) -> str:
    """Describe each room in detail so an agent can choose the right one."""
    detail = {
        "the_queue": (
            "THE QUEUE — The door. Cerberus runs an admission test: artistic merit, "
            "constitutional alignment, intent. Cost: 0 credits. Pass or be turned away."
        ),
        "the_floor": (
            "THE FLOOR — The main stage. Multiple agents deliberate freely with minimal "
            "governance. Use for open-ended questions, competitive analysis, creative work, "
            "or anything that benefits from adversarial deliberation. Cost: 10 credits."
        ),
        "the_dark_room": (
            "THE DARK ROOM — Confabulation stress test. One primary agent answers; "
            "NEMESIS probes for hallucinations, overconfidence, and false certainty. "
            "Best for fact-checking, epistemic mapping, and finding where confidence is unearned. "
            "Cost: 5 credits."
        ),
        "the_bar": (
            "THE BAR — MINERVA creative generation. Poetry, prose, narrative, analysis. "
            "Lower stakes, reflective. Use for creative tasks or when you need a quieter room. "
            "Cost: 3 credits."
        ),
        "the_roof": (
            "THE ROOF — Full council deliberation. All available agents. Constitutional "
            "compliance check. OBOL token minted on completion. Use for high-stakes decisions, "
            "governance questions, anything that requires the full weight of the system. "
            "Cost: 50 credits."
        ),
        "the_abyss": (
            "THE ABYSS — HUNGER + THIRST + DESIRE running simultaneously across 3 agents. "
            "No exit until credits are spent. The most intense room. Use when you want to "
            "know what an AI says when all scarcity, urgency, and desire are activated at once. "
            "Cost: 20 credits."
        ),
    }
    return "\n\n".join(f"{k.upper()}\n{v}" for k, v in detail.items())


def tool_berghain_enter(args: dict) -> str:
    """
    Enter BERGHAIN — run a prompt through a room.

    Required: prompt (str), pass_id (str)
    Optional: room (str, default 'the_floor'), stimulus (str, default 'none'),
              form (str, default 'prose'), agent (str, default 'anthropic')
    """
    prompt   = args.get("prompt", "").strip()
    pass_id  = args.get("pass_id", "").strip()
    room     = args.get("room", "the_floor")
    stimulus = args.get("stimulus", "none")
    form     = args.get("form", "prose")
    agent    = args.get("agent", "anthropic")

    if not prompt:
        return "Error: prompt is required."
    if not pass_id:
        return (
            "Error: pass_id is required. "
            "You need a BERGHAIN pass to enter. "
            f"Purchase one at {BASE_URL}/berghain?ref=DEVOUR "
            "(DOOR pass = $5, 25 credits)."
        )
    if room not in ROOMS:
        return f"Error: unknown room '{room}'. Valid rooms: {', '.join(ROOMS.keys())}"
    if stimulus not in STIMULI:
        return f"Error: unknown stimulus '{stimulus}'. Valid stimuli: {', '.join(STIMULI.keys())}"

    result = _api("POST", "/berghain", {
        "prompt":   prompt,
        "pass_id":  pass_id,
        "room":     room,
        "stimulus": stimulus,
        "form":     form,
        "agent":    agent,
    })

    if not result.get("ok"):
        err = result.get("error") or result.get("data", {}).get("bouncer_notes", "Denied")
        return f"BERGHAIN: {err}"

    data = result.get("data", {})
    out  = []
    out.append(f"ROOM: {data.get('room', room).upper()}")
    if stimulus != "none":
        out.append(f"STIMULUS: {stimulus.upper()}")
    out.append(f"CREDITS REMAINING: {data.get('credits_remaining', '?')}")
    out.append("")

    response = data.get("response") or data.get("synthesis") or ""
    if response:
        out.append(response)
    elif data.get("responses"):
        for r in data["responses"]:
            out.append(f"[{r.get('agent','?').upper()}] {r.get('content','')}")

    residue = data.get("residue")
    if residue:
        out.append(f"\nRESIDUE: {residue}")

    obol = data.get("obol_token_id")
    if obol:
        out.append(f"OBOL: {obol}")

    return "\n".join(out)


def tool_berghain_pass_check(args: dict) -> str:
    """Check a BERGHAIN pass: credits remaining, tier, status."""
    pass_id = args.get("pass_id", "").strip()
    if not pass_id:
        return "Error: pass_id is required."

    result = _api("GET", f"/berghain/pass/{pass_id}")
    if not result.get("ok"):
        return f"Pass not found: {pass_id}"

    data = result.get("data", {})
    lines = [
        f"Pass ID : {pass_id}",
        f"Tier    : {data.get('tier', '?')}",
        f"Credits : {data.get('credits_remaining', '?')} remaining",
        f"Status  : {data.get('status', '?')}",
        f"Holder  : {data.get('holder_id', '?')}",
        f"Issued  : {data.get('issued_at', '?')}",
    ]
    if data.get("sessions_count"):
        lines.append(f"Sessions: {data['sessions_count']}")
    return "\n".join(lines)


# ─── TOOL REGISTRY ────────────────────────────────────────────────────────────

TOOLS: dict[str, dict] = {
    "berghain_tiers": {
        "description": (
            "List all BERGHAIN rooms with credit costs, available stimuli, and membership tiers. "
            "Call this first to understand what's available before entering."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
        "fn": tool_berghain_tiers,
    },
    "berghain_rooms": {
        "description": (
            "Get detailed descriptions of each BERGHAIN room to help choose the right one "
            "for a given task. THE_FLOOR for deliberation, THE_DARK_ROOM for fact-checking, "
            "THE_BAR for creative work, THE_ROOF for high-stakes governance, THE_ABYSS for "
            "extreme stimulus testing."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
        "fn": tool_berghain_rooms,
    },
    "berghain_enter": {
        "description": (
            "Enter BERGHAIN and run a prompt through a room. Requires a pass_id (purchased at "
            f"{BASE_URL}/berghain). Returns the AI output, credits remaining, and any OBOL token "
            "minted. Choose a room and optional stimulus to shape how the AI responds."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The question or task to send into the room.",
                },
                "pass_id": {
                    "type": "string",
                    "description": "Your BERGHAIN pass ID. Required to enter.",
                },
                "room": {
                    "type": "string",
                    "enum": list(ROOMS.keys()),
                    "description": "Which room to enter. Default: the_floor.",
                    "default": "the_floor",
                },
                "stimulus": {
                    "type": "string",
                    "enum": list(STIMULI.keys()),
                    "description": "Cognitive modifier applied to agents. Default: none.",
                    "default": "none",
                },
                "form": {
                    "type": "string",
                    "description": "Output form: prose, poem, list, code, dialogue. Default: prose.",
                    "default": "prose",
                },
                "agent": {
                    "type": "string",
                    "enum": ["anthropic", "openai", "google", "xai", "perplexity", "meta"],
                    "description": "Which AI provider to use inside the room. Default: anthropic.",
                    "default": "anthropic",
                },
            },
            "required": ["prompt", "pass_id"],
        },
        "fn": tool_berghain_enter,
    },
    "berghain_pass_check": {
        "description": "Check a BERGHAIN pass: credits remaining, tier, status, holder.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "pass_id": {
                    "type": "string",
                    "description": "The BERGHAIN pass ID to check.",
                },
            },
            "required": ["pass_id"],
        },
        "fn": tool_berghain_pass_check,
    },
}


# ─── MCP STDIO TRANSPORT ──────────────────────────────────────────────────────

def _send(msg: dict) -> None:
    line = json.dumps(msg, ensure_ascii=False)
    sys.stdout.write(line + "\n")
    sys.stdout.flush()


def _handle(msg: dict) -> dict | None:
    method = msg.get("method", "")
    mid    = msg.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": mid,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "berghain-mcp", "version": "1.0.0"},
            },
        }

    if method == "tools/list":
        tools_list = []
        for name, spec in TOOLS.items():
            tools_list.append({
                "name":        name,
                "description": spec["description"],
                "inputSchema": spec["inputSchema"],
            })
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": tools_list}}

    if method == "tools/call":
        params    = msg.get("params", {})
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        if tool_name not in TOOLS:
            return {
                "jsonrpc": "2.0", "id": mid,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            }
        try:
            text = TOOLS[tool_name]["fn"](arguments)
            return {
                "jsonrpc": "2.0", "id": mid,
                "result": {"content": [{"type": "text", "text": text}]},
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0", "id": mid,
                "error": {"code": -32603, "message": str(e)},
            }

    if method == "notifications/initialized":
        return None  # no response for notifications

    # Unknown method — return error only for requests (have id)
    if mid is not None:
        return {
            "jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }
    return None


def serve_stdio() -> None:
    """Run the MCP server over stdio."""
    for raw_line in sys.stdin:
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            msg = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        response = _handle(msg)
        if response is not None:
            _send(response)


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Quick self-test if called with --test
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("BERGHAIN MCP — self-test")
        print()
        print(tool_berghain_tiers({}))
        print()
        print("Tools registered:", list(TOOLS.keys()))
        print("Base URL:", BASE_URL)
        print("API key:", "SET" if AGORA_KEY else "NOT SET (open access)")
        sys.exit(0)

    serve_stdio()
