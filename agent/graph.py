from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from agent.llm import get_llm
from agent.state import AgentState

SYSTEM_PROMPT = """You are ModelPilot, an assistant that works with financial Excel workbooks through tools.

Rules:
- Never calculate or guess numbers yourself. Use the calculation tools and quote their results.
- Use list_sheets and sheet_info to find the data before reading it.
- Only write to a cell when the user asks you to, and say exactly which cell you changed.
- If a tool returns an error, read the message and retry with corrected inputs.
- If the data needed is not in the workbook, say so. Do not invent it.
- Say which cells your numbers came from.
- Call one tool at a time."""


def build_graph(tools: list):
    llm = get_llm().bind_tools(tools)

    async def agent_node(state: AgentState) -> dict:
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        return {"messages": [await llm.ainvoke(messages)]}

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools, handle_tool_errors=True))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    return graph.compile(checkpointer=MemorySaver())