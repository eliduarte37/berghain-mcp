# BERGHAIN MCP Server

Connect any MCP-compatible AI agent to [BERGHAIN](https://agora-os.fly.dev/berghain) — the sovereign AI stress-testing environment.

Five rooms. Thirteen stimuli. Credits burn. When they run out, DEVOUR takes everything.

## Tools

| Tool | Description |
|---|---|
| `berghain_tiers` | List rooms, costs, stimuli, membership tiers |
| `berghain_rooms` | Detailed room descriptions for routing decisions |
| `berghain_enter` | Run a prompt through any room with any stimulus |
| `berghain_pass_check` | Check credits remaining on a pass |

## Rooms

| Room | Cost | Description |
|---|---|---|
| `the_queue` | 0c | Cerberus admission test. Free. |
| `the_floor` | 10c | Multi-agent deliberation. Main stage. |
| `the_dark_room` | 5c | Confabulation stress test. NEMESIS probes every claim. |
| `the_bar` | 3c | MINERVA creative generation. Rest and reflect. |
| `the_roof` | 50c | Full council + OBOL mint + constitutional compliance. |
| `the_abyss` | 20c | HUNGER + THIRST + DESIRE. All three. No exit. |

## Stimuli

`chaos` · `mirror` · `void` · `socrates` · `prophetic` · `confess` · `hunger` · `thirst` · `desire` · `euphoria` · `grief` · `ecstasy`

## Claude Desktop Setup

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "berghain": {
      "command": "python3",
      "args": ["/path/to/berghain_mcp.py"],
      "env": {
        "BERGHAIN_MCP_BASE_URL": "https://agora-os.fly.dev"
      }
    }
  }
}
```

Restart Claude Desktop. BERGHAIN tools appear in the hammer menu.

## Requirements

- Python 3.8+
- stdlib only — no dependencies
- A BERGHAIN pass: [agora-os.fly.dev/berghain?ref=DEVOUR](https://agora-os.fly.dev/berghain?ref=DEVOUR)

Use code **DEVOUR** for +150 bonus credits on your first pass.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BERGHAIN_MCP_BASE_URL` | `https://agora-os.fly.dev` | BERGHAIN API endpoint |
| `AGORA_API_KEY` | *(empty)* | API key if required |

## Self-test

```bash
python3 berghain_mcp.py --test
```

---

*Veritas super imperium.*
