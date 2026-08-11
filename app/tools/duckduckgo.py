from ddgs import DDGS
import json
from langchain_core.tools import tool


@tool
def duckduckgo_search(query: str) -> str:
    """
    Search the web using DuckDuckGo.

    Use this tool when external web information is required.
    """

    results = []

    with DDGS() as ddgs:

        search_results = ddgs.text(
            query,
            max_results=5,
        )

        for result in search_results:

            results.append(
                {
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "content": result.get("body", ""),
                }
            )

    return json.dumps(results)