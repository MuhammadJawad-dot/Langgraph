from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from app.graph.llm import llm
from app.tools.duckduckgo import duckduckgo_search
from app.tools.serpapi import serpapi_search
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage,ToolMessage
from langgraph.graph.message import add_messages
from app.state.research_state import ResearchState
import json

# class AgentState(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]

tools = [duckduckgo_search,serpapi_search]
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: ResearchState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

def collect_search_results(
    state: ResearchState
):

    all_results = []

    for message in state["messages"]:

        if isinstance(message, ToolMessage):

            try:

                results = json.loads(
                    message.content
                )

                if isinstance(results, list):
                    all_results.extend(results)

            except (
                json.JSONDecodeError,
                TypeError,
            ):
                continue

    return {
        "search_results": all_results
    }

tool_node = ToolNode(tools)

def should_continue(state: ResearchState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return "finish"

graph_builder = StateGraph(ResearchState)


graph_builder.add_node(
    "search_agent",
    agent_node
)

graph_builder.add_node(
    "tools",
    tool_node
)

graph_builder.add_node(
    "collect_results",
    collect_search_results
)


graph_builder.add_edge(
    START,
    "search_agent"
)


# Agent → Tools OR Collect Results

graph_builder.add_conditional_edges(
    "search_agent",
    should_continue,
    {
        "tools": "tools",
        "finish": "collect_results",
    }
)


# Tools → Agent

graph_builder.add_edge(
    "tools",
    "search_agent"
)


# Collect → END

graph_builder.add_edge(
    "collect_results",
    END
)


# --------------------------------------------------
# Compile
# --------------------------------------------------

web_search_graph = graph_builder.compile()