from util.spotify_functions import make_spotify_request
from mcp_instance import mcp

@mcp.tool()
def play_playlist(playlist_id: str) -> str:
    """
    Start playback of a specified playlist.

    Args:
        playlist_id: The Spotify ID of the playlist to play
    
    Returns:
        Success message or error message
    """
    try:
        # Get the current user's available devices
        devices_response = make_spotify_request('GET', '/me/player/devices')
        devices = devices_response.get('devices', [])

        if not devices:
            return "No available devices found to start playback"

        # Use the first available active device
        active_device = next((device for device in devices if device['is_active']), None)
        if not active_device:
            active_device = devices[0]

        device_id = active_device['id']

        # Start playback on the device with the given playlist
        make_spotify_request('PUT', '/me/player/play', {
            'context_uri': f'spotify:playlist:{playlist_id}',
            'device_id': device_id
        })

        return f"Playback started on device {active_device['name']}"
    except Exception as e:
        return f"Failed to start playback: {str(e)}"