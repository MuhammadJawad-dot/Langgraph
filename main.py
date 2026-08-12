from langchain_core.messages import HumanMessage
from app.agents.analysis_agent import analysis_graph
from app.agents.fact_check_agent import fact_check_graph
from app.agents.web_search_agent import web_search_graph
from app.agents.writing_agent import writing_graph
from app.utils.report_writer import save_report_txt

def main():

    question=(
        "What are the main benefits and capabilities of LangGraph supervisor architecture?"
    )

    state = web_search_graph.invoke(
        {
            "question": question,

            "messages": [
                HumanMessage(
                    content=(
                        f"Reasearch this question:"
                        f"{question}."
                        f"Search the web and collect "
                        f"reliable sources."

                    )
                )
            ],
        }
    )

    print("\nSEARCH COMPLETE")
    print(
        f"Sources found: "
        f"{len(state['search_results'])}"
    )
    # ----------------------------------------------
    # 2. Analysis Agent
    # ----------------------------------------------

    state = analysis_graph.invoke(state)

    print("\nANALYSIS")
    print("=" * 80)

    print(state["analysis"])

    print("\nCLAIMS")
    print("=" * 80)

    for claim in state["claims"]:
        print("-", claim)

    state = fact_check_graph.invoke(state)

    print("\nFACT CHECKS")
    print("=" * 80)

    for check in state["fact_checks"]:

        print("\nCLAIM:")
        print(check["claim"])

        print("\nSTATUS:")
        print(check["status"])

        print("\nEVIDENCE:")
        print(check["evidence"])

        print("\nSOURCE:")
        print(check["source"])

        print("-" * 80)
     # ==============================================
    # 4. WRITING
    # ==============================================

    state = writing_graph.invoke(
        state
    )

   
    file_path=save_report_txt(
        report=state["final_report"],
        filename="supervisor_architecture_benefits.txt"
    )

    print("\nREPORT Successfully Generated to:")
    print(file_path)

if __name__ == "__main__":
    main()