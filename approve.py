from langgraph.types import Command
from app.sub_graphs.research_graph import research_graph
from app.utils.report_writer import save_report_txt


thread_id = "research-001"

config = {
    "configurable": {
        "thread_id": thread_id
    }
}


# ==================================================
# GET CHECKPOINT
# ==================================================

snapshot = research_graph.get_state(
    config
)


# ==================================================
# CHECK
# ==================================================

if not snapshot.values:

    print(
        "No research checkpoint found."
    )

    raise SystemExit


# ==================================================
# DISPLAY RESEARCH
# ==================================================

state = snapshot.values

print("\n")
print("=" * 70)
print("HUMAN REVIEW")
print("=" * 70)

print("\nQUESTION:")
print(
    state["question"]
)


print("\nCLAIMS:")
print("-" * 70)

for index, claim in enumerate(
    state.get("claims", []),
    start=1
):

    print(
        f"{index}. {claim}"
    )


print("\nFACT CHECKS:")
print("-" * 70)

for index, check in enumerate(
    state.get("fact_checks", []),
    start=1
):

    print(
        f"\n{index}. Claim:"
    )

    print(
        check.get("claim", "")
    )

    print(
        "Status:",
        check.get("status", "")
    )

    print(
        "Evidence:",
        check.get("evidence", "")
    )

    print(
        "Source:",
        check.get("source", "")
    )


# ==================================================
# HUMAN DECISION
# ==================================================

print("\n")
print("=" * 70)

decision = input(
    "Approve research? (y/n): "
)


# ==================================================
# APPROVE
# ==================================================

if decision.lower() == "y":

    response = {

        "decision": "approved",

        "feedback": ""
    }


# ==================================================
# REJECT
# ==================================================

else:

    feedback = input(
        "\nWhy are you rejecting the research?\n> "
    )

    response = {

        "decision": "rejected",

        "feedback": feedback
    }


# ==================================================
# RESUME GRAPH
# ==================================================

result = research_graph.invoke(

    Command(
        resume=response
    ),

    config=config
)

# if "final_report" in result:
#     file_path = save_report_txt(
#         report=result["final_report"],
#         filename="research_report.txt"
#     )
#     print(f"\nReport successfully saved to: {file_path}")
print("\nWorkflow resumed.")