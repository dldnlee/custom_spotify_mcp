from mcp_instance import mcp

@mcp.resource()
def song_search_results() -> str:
    return "[]"  # JSON list of song titles from Brave search

@mcp.resource()
def track_uris() -> str:
    return "[]"  # JSON list of Spotify track URIs

@mcp.resource()
def playlist_metadata() -> str:
    return '{"name": "", "id": "", "track_count": 0}'  # Playlist info

@mcp.resource()
def playlist_creation_log() -> str:
    return "[]"  # List of actions for debugging/log