import requests
from mcp_instance import mcp
import os
from dotenv import load_dotenv

load_dotenv()

@mcp.tool()
def get_song_list(search_query: str) -> list[str]:
    """Search for songs on the internet based on the search query."""
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
        if title:
            song_titles.append(title)

    return song_titles if song_titles else ["No songs found."]
