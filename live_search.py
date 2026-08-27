# ============================================
# AYANFE AI V2 — LIVE WEB SEARCH
# ============================================

from ddgs import DDGS


def search_web(query, max_results=5):

    """
    Search the public web.

    Returns titles, URLs and snippets.
    """

    results = []

    try:

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=max_results
            )

            for item in search_results:

                results.append({
                    "title": item.get(
                        "title",
                        ""
                    ),

                    "url": item.get(
                        "href",
                        ""
                    ),

                    "source": item.get(
                        "href",
                        ""
                    ),

                    "snippet": item.get(
                        "body",
                        ""
                    )
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


def format_search_results(search_result):

    """
    Convert search results into readable
    context for AYANFE.
    """

    if not search_result.get("success"):

        return ""

    results = search_result.get(
        "results",
        []
    )

    if not results:

        return ""

    output = []

    for result in results:

        output.append(
            f"Title: {result.get('title', '')}\n"
            f"Source: {result.get('source', '')}\n"
            f"Information: {result.get('snippet', '')}"
        )

    return "\n\n".join(output)
