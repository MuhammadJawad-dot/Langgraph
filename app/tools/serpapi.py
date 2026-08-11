import json

from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import tool


@tool
def serpapi_search(query: str) -> str:
    """
    Search the web using SerpAPI.

    Use this tool when external web information
    is required from a search engine API.
    """

    search = SerpAPIWrapper()

    result = search.results(query)

    organic_results = result.get(
        "organic_results",
        []
    )

    results = []

    for item in organic_results:

        results.append(
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "content": item.get("snippet", ""),
            }
        )

    return json.dumps(results)