# # from langchain_core.messages import HumanMessage
# # from app.sub_graphs.research_graph import research_graph
# from app.utils.report_writer import save_report_txt
# from app.services.research_runner import resume_research,start_research

# def main():
    

#     thread_id = "research-001"

#     question = (
#         "What is the status of AI development in Pakistan?"
#     )

#     print("\nStarting research...\n")

#     state = start_research(question,thread_id)

#     print("\nResearch completed.")
    
# #     question=(
# #         "What are the main benefits and capabilities of LangGraph supervisor architecture?"
# #     )

# #     state = web_search_graph.invoke(
# #         {
# #             "question": question,

# #             "messages": [
# #                 HumanMessage(
# #                     content=(
# #                         f"Reasearch this question:"
# #                         f"{question}."
# #                         f"Search the web and collect "
# #                         f"reliable sources."

# #                     )
# #                 )
# #             ],
# #         }
# #     )

# #     print("\nSEARCH COMPLETE")
# #     print(
# #         f"Sources found: "
# #         f"{len(state['search_results'])}"
# #     )
# #     # ----------------------------------------------
# #     # 2. Analysis Agent
# #     # ----------------------------------------------

# #     state = analysis_graph.invoke(state)

# #     print("\nANALYSIS")
# #     print("=" * 80)

# #     print(state["analysis"])

# #     print("\nCLAIMS")
# #     print("=" * 80)

# #     for claim in state["claims"]:
# #         print("-", claim)

# #     state = fact_check_graph.invoke(state)

# #     print("\nFACT CHECKS")
# #     print("=" * 80)

# #     for check in state["fact_checks"]:

# #         print("\nCLAIM:")
# #         print(check["claim"])

# #         print("\nSTATUS:")
# #         print(check["status"])

# #         print("\nEVIDENCE:")
# #         print(check["evidence"])

# #         print("\nSOURCE:")
# #         print(check["source"])

# #         print("-" * 80)
# #      # ==============================================
# #     # 4. WRITING
# #     # ==============================================

# #     state = writing_graph.invoke(
# #         state
# #     )

#     # file_path=save_report_txt(
#     #     report=state["final_report"],
#     #     filename="supervisor3_architecture_benefits.txt"
#     # )

#     # print("\nREPORT Successfully Generated to:")
# #     print(file_path)
# #     snapshot = research_graph.get_state(config)
# #     print(
# #     snapshot.values
# # )

# if __name__ == "__main__":
#     main()



# from langchain_core.messages import HumanMessage

# from app.sub_graphs.research_graph import research_graph


# def main():

#     question = input(
#         "Enter your research question: "
#     )

#     thread_id = "research-002"

#     config = {
#         "configurable": {
#             "thread_id": thread_id
#         }
#     }

#     initial_state = {

#         "question": question,

#         "messages": [
#             HumanMessage(
#                 content=(
#                     f"Research this question: "
#                     f"{question}"
#                 )
#             )
#         ],
#     }

#     print("\nStarting research...\n")

#     result = research_graph.invoke(
#         initial_state,
#         config=config
#     )

#     print(
#         "\nResearch workflow paused "
#         "for human approval."
#     )

#     print(
#         "Thread ID:",
#         thread_id
#     )


# if __name__ == "__main__":
#     main()
import warnings
warnings.filterwarnings("ignore", module="langgraph")

from langchain_core.messages import HumanMessage
from langgraph.types import Command
from app.utils.report_writer import save_report_txt

from app.sub_graphs.research_graph import research_graph


def main():

    question = input(
        "Enter your research question: "
    )

    thread_id = "research-002"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "question": question,

        "messages": [
            HumanMessage(
                content=f"Research this question: {question}"
            )
        ],
    }

    # ==========================================
    # START RESEARCH
    # ==========================================

    result = research_graph.invoke(
        initial_state,
        config=config
    )

    # ==========================================
    # HUMAN APPROVAL
    # ==========================================

    while True:

        snapshot = research_graph.get_state(
            config
        )

        # Graph finished
        if not snapshot.next:
            break

        # Check whether we're waiting for approval
        if "human_approval" in snapshot.next:

            state = snapshot.values

            print("\n")
            print("=" * 70)
            print("HUMAN APPROVAL REQUIRED")
            print("=" * 70)

            print("\nQUESTION:")
            print(state["question"])

            print("\nCLAIMS:")
            for i, claim in enumerate(
                state.get("claims", []),
                1
            ):
                print(f"{i}. {claim}")

            print("\nFACT CHECKS:")

            for i, check in enumerate(
                state.get("fact_checks", []),
                1
            ):
                print(f"\n{i}. Claim: {check.get('claim', '')}")
                print(f"   Status: {check.get('status', '').upper()}")
                print(f"   Evidence: {check.get('evidence', '')}")
                print(f"   Source: {check.get('source', '')}")

            decision = input(
                "\nApprove research? (y/n): "
            )

            if decision.lower() == "y":

                response = {
                    "decision": "approved",
                    "feedback": ""
                }

            else:

                feedback = input(
                    "Why are you rejecting it?\n> "
                )

                response = {
                    "decision": "rejected",
                    "feedback": feedback
                }

            # ==================================
            # RESUME GRAPH
            # ==================================

            result = research_graph.invoke(
                Command(
                    resume=response
                ),
                config=config
            )

        else:
            break

    print("\nResearch completed.")
    final_snapshot = research_graph.get_state(config)
    final_state = final_snapshot.values
    # Save the report to a text file if it exists
    if "final_report" in final_state:
        file_path = save_report_txt(
            report=final_state["final_report"],
            filename="ai2_pakistan_report.txt"
        ) 
        print(f"\nReport Successfully Saved to: {file_path}")

if __name__ == "__main__":
    main()