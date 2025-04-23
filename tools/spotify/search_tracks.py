from util.spotify_functions import make_spotify_request
from mcp_instance import mcp
from typing import List

@mcp.tool()
def search_tracks(query: str, limit: int = 10) -> List[dict]:
    """
    Search for tracks on Spotify.

    Args:
        query: The search query (e.g., artist or track name)
        limit: Number of results to return (default 10)

    Returns:
        A list of track dictionaries with name, artist, and URI
    """
    try:
        response = make_spotify_request('GET', f'/search?q={query}&type=track&limit={limit}')
        tracks = response['tracks']['items']

        return [{
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'uri': track['uri']
        } for track in tracks]
    except Exception as e:
        return [{'error': f"Failed to search tracks: {str(e)}"}]
