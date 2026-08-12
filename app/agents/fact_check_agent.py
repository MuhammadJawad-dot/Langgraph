from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from app.prompts.fact_checker import FACT_CHECK_PROMPT
from app.graph.llm import llm
from app.state.research_state import ResearchState



class FactCheckResult(BaseModel):

    claim: str = Field(
        description="The factual claim being checked"
    )

    status: str = Field(
        description=(
            "Verification status: verified, "
            "partially_verified, contradicted, "
            "or unverified"
        )
    )

    evidence: str = Field(
        description="Evidence supporting the verification decision"
    )

    source: str = Field(
        description="URL of the strongest supporting source"
    )
class FactCheckOutput(BaseModel):

    results: list[FactCheckResult]


structured_llm = llm.with_structured_output(
    FactCheckOutput
)

# --------------------------------------------------
# Agent
# --------------------------------------------------

def fact_check_agent(
    state: ResearchState
):

    question = state["question"]

    claims = state.get(
        "claims",
        []
    )

    search_results = state.get(
        "search_results",
        []
    )

    prompt = FACT_CHECK_PROMPT.format(
        question=question,
        claims=claims,
        search_results=search_results,
    )

    result = structured_llm.invoke(prompt)

    fact_checks = []

    for item in result.results:

        fact_checks.append(
            {
                "claim": item.claim,
                "status": item.status,
                "evidence": item.evidence,
                "source": item.source,
            }
        )

    return {
        "fact_checks": fact_checks
    }


# --------------------------------------------------
# Graph
# --------------------------------------------------

graph_builder = StateGraph(
    ResearchState
)

graph_builder.add_node(
    "fact_check_agent",
    fact_check_agent
)

graph_builder.add_edge(
    START,
    "fact_check_agent"
)

graph_builder.add_edge(
    "fact_check_agent",
    END
)

fact_check_graph = graph_builder.compile()