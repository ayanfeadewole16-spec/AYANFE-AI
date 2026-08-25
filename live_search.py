
# ============================================
# AYANFE AI V2 — LIVE WEB SEARCH
# ============================================

from ddgs import DDGS

def search_web(query, max_results=5):
    """
    Search the web using DuckDuckGo.
    Returns a list of search results with title, URL and source.
    """

    results = []

    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=max_results)

            for item in search_results:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("href", ""),
                    "source": item.get("href", ""),
                    "snippet": item.get("body", "")
                })

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "results": []
        }

    return {
        "success": True,
        "query": query,
        "results": results
    }
