from langchain_core.messages import HumanMessage

from app.sub_graphs.research_graph import research_graph

from app.utils.report_writer import (
    save_report_txt
)


def get_config(
    thread_id: str
):

    return {
        "configurable": {
            "thread_id": thread_id
        }
    }


def start_research(
    question: str,
    thread_id: str
):

    initial_state = {

        "question": question,

        "messages": [
            HumanMessage(
                content=(
                    f"Research this question: "
                    f"{question}. "
                    f"Find reliable sources."
                )
            )
        ],
    }

    config = get_config(
        thread_id
    )

    state = research_graph.invoke(
        initial_state,
        config=config
    )

    if "final_report" in state:

        save_report_txt(
            state["final_report"]
        )

    return state


def get_research_state(
    thread_id: str
):

    config = get_config(
        thread_id
    )

    snapshot = research_graph.get_state(
        config
    )

    return snapshot


def get_research_status(
    thread_id: str
):

    snapshot = get_research_state(
        thread_id
    )

    if not snapshot.values:

        return {
            "exists": False,
            "next": None,
            "state": None,
        }

    return {
        "exists": True,
        "next": snapshot.next,
        "state": snapshot.values,
    }


def resume_research(
    thread_id: str
):

    config = get_config(
        thread_id
    )

    snapshot = research_graph.get_state(
        config
    )

    if not snapshot.values:

        raise ValueError(
            f"No checkpoint found for "
            f"thread: {thread_id}"
        )

    if not snapshot.next:

        print(
            "Research is already complete."
        )

        return snapshot.values

    print(
        f"Resuming from: "
        f"{snapshot.next}"
    )

    state = research_graph.invoke(
        None,
        config=config
    )

    if "final_report" in state:

        save_report_txt(
            state["final_report"]
        )

    return state