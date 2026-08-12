from langgraph.graph import END, START, StateGraph
from app.agents.web_search_agent import web_search_graph
from app.agents.analysis_agent import analysis_graph
from app.agents.fact_check_agent import fact_check_graph
from app.agents.writing_agent import writing_graph
from app.state.research_state import ResearchState
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

connection = sqlite3.connect(
    "app/checkpoints/research.db",
    check_same_thread=False,
)

checkpointer = SqliteSaver(
    connection
)
builder_graph = StateGraph(ResearchState)

builder_graph.add_node("web_search", web_search_graph)
builder_graph.add_node("analysis", analysis_graph)
builder_graph.add_node("fact_check", fact_check_graph)
builder_graph.add_node("writing", writing_graph)

builder_graph.add_edge(START, "web_search")
builder_graph.add_edge("web_search", "analysis")
builder_graph.add_edge("analysis", "fact_check")
builder_graph.add_edge("fact_check", "writing")
builder_graph.add_edge("writing", END)

research_graph = builder_graph.compile(checkpointer=checkpointer)