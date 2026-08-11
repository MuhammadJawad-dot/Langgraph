from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class SearchResult(TypedDict):
    title: str
    url: str
    content: str


class FactCheck(TypedDict):
    claim: str
    status: str
    evidence: str
    source: str


class ResearchState(TypedDict, total=False):

    # Original user request
    question: str

    # Conversation / ReAct messages
    messages: Annotated[list[BaseMessage], add_messages]

    # Web Search Agent output
    search_results: list[SearchResult]

    # Analysis Agent output
    analysis: str
    claims: list[str]

    # Fact-Check Agent output
    fact_checks: list[FactCheck]

    # Writing Agent output
    final_report: str

    # Supervisor control
    next_agent: str