from util.spotify_functions import make_spotify_request
from mcp_instance import mcp
from typing import List

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
