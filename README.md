# AI 420 — HOS 2: Custom Tools, MCP & Memory

Guide: https://clarkngo.github.io/stc-transformation/courses/ai-420-guides/hos-02-tools-mcp-memory.html

**Already working**
- `data/harbor.db`: Harbor Supply Co.'s customers, products, and orders (`python data/seed_db.py` rebuilds it).
- `mcp_server/server.py`: an MCP server with one finished tool, `get_marine_weather` (Open-Meteo, free, no key). Use it as your pattern.
- `ops_agent/`: an ADK agent already connected to that server over MCP.

**You build**
- Stage 1: a browser tool and a read-only database tool on the MCP server; short-term and long-term memory for the agent.
- Stage 4: two narrow, typed tools, by hand.

```bash
cp .env.example .env        # paste your GOOGLE_API_KEY
python data/seed_db.py      # Codespaces does this for you
adk web                     # pick ops_agent
```
