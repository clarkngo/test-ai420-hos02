"""Harbor Supply Co. operations agent.

Already working: the agent connects to the MCP server (mcp_server/server.py)
and can use whatever tools it serves — right now, just get_marine_weather.

Stage 1 adds the browser and database tools to the server, plus memory:
short-term (ADK session state) and long-term (a local Chroma store).

Run from the HOS folder:  adk web   (then pick "ops_agent")
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

harbor_tools = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[str(ROOT / "mcp_server" / "server.py")],
        ),
        timeout=30,
    ),
)

root_agent = Agent(
    name="ops_agent",
    model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
    description="Operations assistant for Harbor Supply Co., a marine supply store.",
    instruction=(
        "You help the staff and customers of Harbor Supply Co., a marine supply store in the Seattle area. "
        "Use your tools rather than guessing. If a tool returns status 'error', read the error, "
        "fix your input, and try once more before giving up."
    ),
    tools=[harbor_tools],
)
