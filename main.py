from langchain_core.messages import HumanMessage
from app.sub_graphs.research_graph import research_graph
from app.utils.report_writer import save_report_txt
from app.services.research_runner import resume_research,start_research

def main():
    

    thread_id = "research-001"

    question = (
        "What are the main capabilities of "
        "LangGraph for building AI agents?"
    )

    print("\nStarting research...\n")

    state = resume_research(thread_id)

    print("\nResearch completed.")
    
#     question=(
#         "What are the main benefits and capabilities of LangGraph supervisor architecture?"
#     )

#     state = web_search_graph.invoke(
#         {
#             "question": question,

#             "messages": [
#                 HumanMessage(
#                     content=(
#                         f"Reasearch this question:"
#                         f"{question}."
#                         f"Search the web and collect "
#                         f"reliable sources."

#                     )
#                 )
#             ],
#         }
#     )

#     print("\nSEARCH COMPLETE")
#     print(
#         f"Sources found: "
#         f"{len(state['search_results'])}"
#     )
#     # ----------------------------------------------
#     # 2. Analysis Agent
#     # ----------------------------------------------

#     state = analysis_graph.invoke(state)

#     print("\nANALYSIS")
#     print("=" * 80)

#     print(state["analysis"])

#     print("\nCLAIMS")
#     print("=" * 80)

#     for claim in state["claims"]:
#         print("-", claim)

#     state = fact_check_graph.invoke(state)

#     print("\nFACT CHECKS")
#     print("=" * 80)

#     for check in state["fact_checks"]:

#         print("\nCLAIM:")
#         print(check["claim"])

#         print("\nSTATUS:")
#         print(check["status"])

#         print("\nEVIDENCE:")
#         print(check["evidence"])

#         print("\nSOURCE:")
#         print(check["source"])

#         print("-" * 80)
#      # ==============================================
#     # 4. WRITING
#     # ==============================================

#     state = writing_graph.invoke(
#         state
#     )

    file_path=save_report_txt(
        report=state["final_report"],
        filename="supervisor3_architecture_benefits.txt"
    )

    # print("\nREPORT Successfully Generated to:")
#     print(file_path)
#     snapshot = research_graph.get_state(config)
#     print(
#     snapshot.values
# )

if __name__ == "__main__":
    main()