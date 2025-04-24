import requests
from mcp_instance import mcp
import os

@mcp.tool()
def search_tracks_online(search_query: str) -> list[str]:
    """
    Search tracks based on the user's emotion.

    Args:
        query: The search query (e.g., artist or track name)
        limit: Number of results to return (default 10)

    Returns:
        A list of strings formatted as "Title - Author" for each track found.
    """
    url = "https://api.search.brave.com/res/v1/web/search"

    api_key = os.getenv("BRAVE_API_KEY")
    if not api_key:
        raise ValueError("BRAVE_API_KEY is not set in the .env file")

    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key
    }
    params = {
        "q": f"{search_query} songs list",
        "count": 5
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    search_results = response.json()
    song_titles = []
    for result in search_results.get("web", {}).get("results", []):
        title = result.get("title", "")
        author = result.get("description", "")
        if title and author:
            song_titles.append(f"{title} - {author}")
        elif title:
            song_titles.append(title)

    return song_titles if song_titles else ["No songs found."]
