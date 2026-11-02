import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(command=sys.executable, args=["-m", "mcp_server.server"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            ok = await session.call_tool(
                "calculate_growth",
                {"file_name": "sample_model.xlsx", "sheet": "Income Statement", "cell_range": "B2:B9"},
            )
            print("growth ->", ok.content[0].text)

            bad = await session.call_tool("list_sheets", {"file_name": "missing.xlsx"})
            print("error ->", bad.isError, "|", bad.content[0].text)


asyncio.run(main())