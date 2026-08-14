from langgraph.graph import END, START, StateGraph
from app.agents.web_search_agent import web_search_graph
from app.agents.analysis_agent import analysis_graph
from app.agents.fact_check_agent import fact_check_graph
from app.agents.writing_agent import writing_graph
from app.state.research_state import ResearchState
from langgraph.types import interrupt
from langchain_core.messages import HumanMessage
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

connection = sqlite3.connect(
    "app/checkpoints/research.db",
    check_same_thread=False,
)
# ==================================================
# CHECKPOINTER
# ==================================================
checkpointer = SqliteSaver(connection)

# ==================================================
# HUMAN APPROVAL NODE
# ==================================================

def human_approval(state: ResearchState):

    response = interrupt({
        "type": "human_approval",

        "question": state["question"],

        "claims": state.get(
            "claims",
            []
        ),

        "fact_checks": state.get(
            "fact_checks",
            []
        ),

        "message": (
            "Review the research and "
            "fact-check results."
        )
    })
    updates = {
        "approval": response["decision"],
        "approved_feedback": response.get("feedback", "")
    }
    if response["decision"] == "rejected":
        updates["messages"] = [HumanMessage(content=f"The previous research was rejected. Feedback: {response.get('feedback', '')}. Please search again and update the findings.")]
    return updates

    # return {
    #     "approval": response["decision"],
    #     "approved_feedback": response.get("feedback", "")
    # }
# ==================================================
# APPROVAL ROUTER
# ==================================================
def approval_router(state: ResearchState):

    if state["approval"] == "approved":

        return "writing"

    return "web_search"

    return {
        "approval": response["decision"],

        "approval_feedback": response.get(
            "feedback",
            ""
        )
    }

builder_graph = StateGraph(ResearchState)

# ==================================================
# AGENTS
# ==================================================
builder_graph.add_node("web_search", web_search_graph)
builder_graph.add_node("analysis", analysis_graph)
builder_graph.add_node("fact_check", fact_check_graph)
builder_graph.add_node("writing", writing_graph)
builder_graph.add_node("human_approval",human_approval)


builder_graph.add_edge(START, "web_search")
builder_graph.add_edge("web_search", "analysis")
builder_graph.add_edge("analysis", "fact_check")
builder_graph.add_edge("fact_check", "human_approval")
builder_graph.add_conditional_edges("human_approval",approval_router,{
    "writing":"writing",
    "web_search":"web_search"
})
builder_graph.add_edge("writing", END)

research_graph = builder_graph.compile(checkpointer=checkpointer)