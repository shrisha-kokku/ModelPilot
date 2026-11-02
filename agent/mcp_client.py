from langchain_mcp_adapters.client import MultiServerMCPClient
from agent.config import MCP_SERVERS


async def load_mcp_tools():
    """Connect to the MCP server, ask what tools it has, and return them as LangChain tools."""
    client = MultiServerMCPClient(MCP_SERVERS)
    return await client.get_tools()