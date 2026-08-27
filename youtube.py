# ============================================
# AYANFE AI V2 — YOUTUBE SEARCH
# ============================================

from ddgs import DDGS


def is_youtube_request(text):

    text = text.lower()

    keywords = [
        "youtube",
        "youtube video",
        "video on youtube",
        "find me a video",
        "find a video"
    ]

    return any(
        keyword in text
        for keyword in keywords
    )


def search_youtube(query, max_results=5):

    results = []

    search_query = (
        f"site:youtube.com/watch {query}"
    )

    try:

        with DDGS() as ddgs:

            search_results = ddgs.text(
                search_query,
                max_results=max_results
            )

            for item in search_results:

                url = item.get(
                    "href",
                    ""
                )

                if "youtube.com/watch" in url:

                    results.append({
                        "title": item.get(
                            "title",
                            ""
                        ),
                        "url": url,
                        "description": item.get(
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


def get_best_youtube_video(query):

    result = search_youtube(
        query,
        max_results=5
    )

    if not result["success"]:

        return result

    if not result["results"]:

        return {
            "success": False,
            "error": "No YouTube video was found.",
            "results": []
        }

    best = result["results"][0]

    return {
        "success": True,
        "title": best["title"],
        "url": best["url"],
        "description": best["description"]
    }
