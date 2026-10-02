"""Harbor Supply Co. tool server, speaking MCP over stdio.

The course description names three kinds of external tools: APIs, web
browsers, and databases. One of each belongs in this server:
  - get_marine_weather  -> an external API        (DONE — use it as your example)
  - fetch_page          -> a web browser           (TODO, Stage 1)
  - query_database      -> a database, read-only   (TODO, Stage 1)

The ADK agent starts this file as a subprocess (see ops_agent/agent.py).
You can also run it alone to check it starts:  python mcp_server/server.py
NOTE: this is mcp 2.x. Older tutorials (and many AI assistants) write
`from mcp.server.fastmcp import FastMCP`; in 2.x that class is `MCPServer`
from `mcp.server.mcpserver`, as below.
"""

import logging
from pathlib import Path

import httpx
from mcp.server.mcpserver import MCPServer

DB = Path(__file__).resolve().parent.parent / "data" / "harbor.db"
if not DB.exists():  # e.g. in a portfolio-repo Codespace, whose devcontainer doesn't seed it
    import runpy
    runpy.run_path(str(DB.with_name("seed_db.py")))["build"]()
# Many sites (Wikipedia included) reject requests without an identifying User-Agent.
HEADERS = {"User-Agent": "AI420-course-agent/1.0 (https://github.com/clarkngo/stc-transformation; educational use)"}

logging.getLogger("httpx").setLevel(logging.WARNING)  # keep request logs out of the agent's way

server = MCPServer("harbor-tools")


# ---------- API tool (worked example) ----------

@server.tool()
def get_marine_weather(place: str) -> dict:
    """Current wind and wave conditions for a coastal place, for advising customers heading out on the water.

    Args:
        place: A city or harbor name, e.g. "Anacortes" or "Port Townsend".
    """
    try:
        geo = httpx.get("https://geocoding-api.open-meteo.com/v1/search",
                        params={"name": place, "count": 1}, timeout=15).json()
        if not geo.get("results"):
            return {"status": "error", "error": f"Couldn't find a place called '{place}'."}
        loc = geo["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        wx = httpx.get("https://api.open-meteo.com/v1/forecast", timeout=15, params={
            "latitude": lat, "longitude": lon, "wind_speed_unit": "kn",
            "current": "temperature_2m,wind_speed_10m,wind_gusts_10m"}).json()["current"]
        waves = httpx.get("https://marine-api.open-meteo.com/v1/marine", timeout=15, params={
            "latitude": lat, "longitude": lon, "current": "wave_height"}).json().get("current", {})
        return {"status": "ok", "place": f"{loc['name']}, {loc.get('admin1', '')}",
                "air_temp_c": wx["temperature_2m"], "wind_kn": wx["wind_speed_10m"],
                "gusts_kn": wx["wind_gusts_10m"], "wave_height_m": waves.get("wave_height")}
    except Exception as e:
        # Errors go back to the model as data it can read and react to, not as a crash.
        return {"status": "error", "error": str(e)}


# ---------- Browser tool: TODO (Stage 1) ----------


# ---------- Database tool: TODO (Stage 1) ----------


if __name__ == "__main__":
    server.run()  # stdio transport
