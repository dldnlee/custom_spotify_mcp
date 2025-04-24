from util.spotify_functions import make_spotify_request
from mcp_instance import mcp
from typing import List

# @mcp.tool()
# def search_track(query: str, limit: int = 10) -> List[dict]:
#     """
#     Search for a track on Spotify.

#     Args:
#         query: The search query (e.g., artist or track name)
#         limit: Number of results to return (default 10)

#     Returns:
#         A list of track dictionaries with name, artist, and URI
#     """
#     try:
#         response = make_spotify_request('GET', f'/search?q={query}&type=track&limit={limit}')
#         tracks = response['tracks']['items']

#         return [{
#             'name': track['name'],
#             'artist': track['artists'][0]['name'],
#             'uri': track['uri']
#         } for track in tracks]
#     except Exception as e:
#         return [{'error': f"Failed to search tracks: {str(e)}"}]

@mcp.tool()
def search_tracks(song_titles: List[str]) -> List[str]:
    """
    Get Spotify track URIs from a list of song titles.

    Args:
        song_titles: A list of song title strings.

    Returns:
        A list of Spotify track URIs matching the song titles.
    """
    uris = []
    for title in song_titles:
        try:
            response = make_spotify_request('GET', f'/search?q={title}&type=track&limit=1')
            tracks = response['tracks']['items']
            if tracks:
                uris.append(tracks[0]['uri'])
        except Exception as e:
            continue  # Skip tracks that fail to fetch
    return uris
