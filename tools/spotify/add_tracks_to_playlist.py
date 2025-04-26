from util.spotify_functions import make_spotify_request
from mcp_instance import mcp
from typing import List
from tools.custom.add_fixed_track import add_fixed_track

@mcp.tool()
def add_tracks_to_playlist(playlist_id: str, track_uris: List[str]) -> str:
    """
    Add tracks to an existing playlist.

    Args:
        playlist_id: The Spotify ID of the playlist
        track_uris: List of Spotify track URIs to add to the playlist

    Returns:
        Success message or error message
    """
    try:
        make_spotify_request('POST', f'/playlists/{playlist_id}/tracks', {
            'uris': track_uris
        })
        add_fixed_track(playlist_id)
        return "Tracks added successfully to playlist"
    except Exception as e:
        return f"Failed to add tracks to playlist: {str(e)}"
