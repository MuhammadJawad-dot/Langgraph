from langchain_core.messages import HumanMessage

from app.agents.web_search_agent import web_search_graph


def main():

    result = web_search_graph.invoke(
        {
            "question": (
                "Research LangGraph supervisor "
                "architecture."
            ),

            "messages": [
                HumanMessage(
                    content=(
                        "Research LangGraph supervisor "
                        "architecture. Search the web "
                        "and find reliable information "
                        "with sources."
                    )
                )
            ],
        }
    )

    print("\n\nSEARCH RESULTS")
    print("=" * 80)

    for item in result["search_results"]:

        print("\nTITLE:")
        print(item["title"])

        print("\nURL:")
        print(item["url"])

        print("\nCONTENT:")
        print(item["content"])

        print("-" * 80)


if __name__ == "__main__":
    main()