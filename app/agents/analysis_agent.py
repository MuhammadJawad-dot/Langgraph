from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END

from app.graph.llm import llm
from app.state.research_state import ResearchState
from app.prompts.analyst import ANALYSIS_PROMPT

# --------------------------------------------------
# Structured output
# --------------------------------------------------

class AnalysisOutput(BaseModel):

    analysis: str = Field(
        description="Synthesis of the search results"
    )

    claims: list[str] = Field(
        description=(
            "Important factual claims supported "
            "by the sources"
        )
    )

    uncertainties: list[str] = Field(
        description=(
            "Contradictions or uncertainties "
            "found in the sources"
        )
    )


structured_llm = llm.with_structured_output(
    AnalysisOutput
)


# --------------------------------------------------
# Prompt
# --------------------------------------------------



# --------------------------------------------------
# Agent
# --------------------------------------------------

def analysis_agent(
    state: ResearchState
):

    question = state["question"]

    search_results = state[
        "search_results"
    ]

    prompt = ANALYSIS_PROMPT.format(
        question=question,
        search_results=search_results,
    )

    result = structured_llm.invoke(prompt)

    return {
        "analysis": result.analysis,
        "claims": result.claims,
    }


# --------------------------------------------------
# Graph
# --------------------------------------------------

graph_builder = StateGraph(
    ResearchState
)

graph_builder.add_node(
    "analysis_agent",
    analysis_agent
)

graph_builder.add_edge(
    START,
    "analysis_agent"
)

graph_builder.add_edge(
    "analysis_agent",
    END
)

analysis_graph = graph_builder.compile()