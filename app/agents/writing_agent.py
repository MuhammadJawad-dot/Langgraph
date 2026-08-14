from app.prompts.writer import WRITING_PROMPT
from app.graph.llm import llm
from pydantic import BaseModel,Field
from app.state.research_state import ResearchState
from langgraph.graph import START,END,StateGraph
class ReportOutput(BaseModel):

    title: str = Field(
        description="Title of the research report"
    )

    executive_summary: str = Field(
        description="Short summary of the research"
    )

    key_findings: list[str] = Field(
        description="Important findings from the research"
    )

    detailed_analysis: str = Field(
        description="Detailed synthesis of the research"
    )

    fact_checked_claims: list[str] = Field(
        description=(
            "Fact checked claims including their "
            "verification status and evidence"
        )
    )

    conclusion: str = Field(
        description="Final conclusion"
    )

    sources: list[str] = Field(
        description="Source URLs used in the research"
    )


structured_llm = llm.with_structured_output(
    ReportOutput
)

def writing_agent(
    state: ResearchState
):

    prompt = WRITING_PROMPT.format(
        question=state["question"],
        search_results=state.get(
            "search_results",
            []
        ),
        analysis=state.get(
            "analysis",
            ""
        ),
        claims=state.get(
            "claims",
            []
        ),
        fact_checks=state.get(
            "fact_checks",
            []
        ),
    )

    result = structured_llm.invoke(prompt)

    return {
        "final_report":result  #result.model_dump()
    }

graph_builder = StateGraph(ResearchState)
graph_builder.add_node(
    "writing_agent",
    writing_agent
)
graph_builder.add_edge(
    START,
    "writing_agent"
)
graph_builder.add_edge(
    "writing_agent",
    END
)
writing_graph = graph_builder.compile()