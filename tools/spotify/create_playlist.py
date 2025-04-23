from util.spotify_functions import make_spotify_request
from mcp_instance import mcp

@mcp.tool()
def create_playlist(name: str, description: str = "", public: bool = False) -> str:
    """
    Create a new playlist on Spotify.

    Args:
        name: The name of the playlist
        description: Optional description of the playlist
        public: Whether the playlist should be public (default: False)
    """
    try:
        user_profile = make_spotify_request('GET', '/me')
        user_id = user_profile['id']

        playlist = make_spotify_request('POST', f'/users/{user_id}/playlists', {
            'name': name,
            'description': description,
            'public': public
        })

        return playlist['id']
    except Exception as e:
        return f"Failed to create playlist: {str(e)}"
