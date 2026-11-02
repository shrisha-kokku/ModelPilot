import asyncio
from langchain_core.messages import HumanMessage
from agent.mcp_client import load_mcp_tools
from agent.graph import build_graph

CONFIG = {"configurable": {"thread_id": "modelpilot-session"}, "recursion_limit": 15}


async def run_turn(graph, user_input: str) -> None:
    inputs = {"messages": [HumanMessage(user_input)]}
    async for update in graph.astream(inputs, config=CONFIG, stream_mode="updates"):
        for node, data in update.items():
            for msg in data["messages"]:
                if node == "tools":
                    print(f"  result from {msg.name}: {str(msg.content)[:200]}")
                elif msg.tool_calls:
                    for call in msg.tool_calls:
                        print(f"  calling {call['name']} with {call['args']}")
                else:
                    print(f"\nAgent: {msg.content}")


async def main() -> None:
    tools = await load_mcp_tools()
    print("Connected to MCP server. Tools:", [t.name for t in tools])
    graph = build_graph(tools)
    print("ModelPilot ready. Type 'quit' to exit.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"quit", "exit"}:
            break
        if user_input:
            await run_turn(graph, user_input)


asyncio.run(main())