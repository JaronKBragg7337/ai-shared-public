"""Read-only protocol inventory; does not call trading/account tools."""
import asyncio
import json
import os
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    root = Path(__file__).resolve().parent
    env = {k: v for k, v in os.environ.items() if k in ('SystemRoot', 'WINDIR', 'PATH', 'TEMP', 'TMP', 'USERPROFILE', 'APPDATA', 'LOCALAPPDATA')}
    env['PM_TRADER_HOME'] = str(root / 'data')
    params = StdioServerParameters(command=str(root / '.venv/Scripts/pm-trader.exe'), args=['mcp'], env=env)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.list_tools()
            print(json.dumps({'tools': [t.name for t in result.tools], 'count': len(result.tools)}))

asyncio.run(main())
