"""Run the Polymarket MCP server over loopback HTTP for the OpenClaw Gateway."""

import os

from server import mcp


if __name__ == "__main__":
    mcp.settings.host = os.getenv("POLYMARKET_MCP_HOST", "127.0.0.1")
    mcp.settings.port = int(os.getenv("POLYMARKET_MCP_PORT", "8765"))
    mcp.run(transport="streamable-http")
