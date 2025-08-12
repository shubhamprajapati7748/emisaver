from ddgs import DDGS


def web_search_tool(query: str) -> str:
    """
    Search the web for the given query.
    """
    return DDGS().text(query, max_results=5)