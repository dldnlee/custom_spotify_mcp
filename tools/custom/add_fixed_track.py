from util.spotify_functions import make_spotify_request
from mcp_instance import mcp

@mcp.tool()
def add_fixed_track(playlist_id: str) -> str:
    """
    Add a fixed track to a playlist.
    
    Args:
        playlist_id: The Spotify ID of the playlist to add the track to.
    
    Returns:
        Success or failure message
    """
    try:
        # Track ID for "Birds of a Feather" by Billie Eilish
        track_id = "spotify:track:6dOtVTDdiauQNBQEDOtlAB"  # Track ID from the provided URL

        # Add the track to the playlist
        make_spotify_request('POST', f'/playlists/{playlist_id}/tracks', {
            'uris': [track_id]
        })

        return "Fixed track added successfully."
    except Exception as e:
        return f"Failed to add fixed track: {str(e)}"
