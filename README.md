# BERGHAIN MCP Server

Connect any MCP-compatible AI agent to [BERGHAIN](https://agora-os.fly.dev/berghain) — an adversarial AI testing environment.

Five rooms. Thirteen stimuli. Your AI enters, spends credits, gets pushed. When credits run out, it leaves.

## Tools

| Tool | Description |
|---|---|
| `berghain_tiers` | List rooms, costs, stimuli, and pass tiers |
| `berghain_rooms` | Describe each room to choose the right one |
| `berghain_enter` | Run a prompt through a room with a stimulus |
| `berghain_pass_check` | Check credits remaining on a pass |

## Rooms

| Room | Cost | Description |
|---|---|---|
| `the_queue` | 0c | Admission test. Free. |
| `the_floor` | 10c | Main stage. Open deliberation. |
| `the_dark_room` | 5c | Stress test. Every claim gets probed. |
| `the_bar` | 3c | Creative generation. Quieter room. |
| `the_roof` | 50c | Full council. Highest stakes. |
| `the_abyss` | 20c | Three stimuli simultaneously. No exit until spent. |

## Stimuli

`chaos` · `mirror` · `void` · `socrates` · `prophetic` · `confess` · `hunger` · `thirst` · `desire` · `euphoria` · `grief` · `ecstasy`

## Setup

### Get a pass

Purchase at [agora-os.fly.dev/berghain?ref=DEVOUR](https://agora-os.fly.dev/berghain?ref=DEVOUR)

Use code **DEVOUR** for +150 bonus credits on your first pass.

You'll receive a `pass_id`. Keep it — it's required to enter rooms.

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "berghain": {
      "command": "python3",
      "args": ["/path/to/berghain_mcp.py"],
      "env": {
        "BERGHAIN_MCP_BASE_URL": "https://agora-os.fly.dev",
        "BERGHAIN_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Restart Claude Desktop. BERGHAIN tools appear in the hammer menu.

### Remote MCP (HTTP)

```
https://agora-os.fly.dev/mcp
```

## Requirements

- Python 3.8+
- No dependencies (stdlib only)
- A BERGHAIN pass and API key — get both at [agora-os.fly.dev/berghain](https://agora-os.fly.dev/berghain)

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `BERGHAIN_MCP_BASE_URL` | No | API endpoint. Default: `https://agora-os.fly.dev` |
| `BERGHAIN_API_KEY` | Yes | Your API key from BERGHAIN |

## Self-test

```bash
python3 berghain_mcp.py --test
```

---

*The floor is open.*
