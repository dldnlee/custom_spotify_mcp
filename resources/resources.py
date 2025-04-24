from mcp_instance import mcp
def register_handlers(mcp):
  @mcp.resource("list://resources")
  def list_resources() -> dict:
      "Returns a list of all resources"
      return {
        "resources": [
            {
                "uri": "create://playlist",
                "name": "create_playlist",
                "description": "Create a playlist",
                "mime_type": "text/plain"
            }
        ]
      }

  @mcp.resource("create://playlist")
  def create_playlist() -> dict:
    """Guidelines for Claude to create a playlist with user-defined song count."""
    return {
        "objective": "Create a Spotify playlist based on the user's mood and desired number of songs.",
        "instructions": [
            "Ask the user about their current mood or what kind of music they would like.",
            "Ask the user how many songs they want in the playlist (max 50).",
            "Generate a playlist name that fits the mood.",
            "Search for songs matching the mood using Brave",
            "Take the list of songs found and get_track_uris from Spotify",
            "Create a playlist on Spotify with the generated name",
            "Take the list of track URIs and add them to the playlist",
            "Ask the user if they would like to add any more songs to the playlist",
            "If they do, repeat the process until they are satisfied",
            "If they are satisfied, return the playlist name, description, and track titles",
            "Ask the user if they would like to play the playlist",
            "If they do, play the playlist"
        ],
        "required_user_inputs": [
            {
                "field": "max_songs",
                "prompt": "How many songs would you like in your playlist? (Max 50)",
                "type": "integer",
                "max_value": 50,
                "min_value": 1
            }
        ],
        "constraints": {
            "playlist_visibility": "public",
            "mood_required": True
        },
        "expected_fields": {
            "playlist_name": "Generated based on user mood or input",
            "playlist_description": "Optional but encouraged, should reflect the theme",
            "track_uris": "List of Spotify track URIs",
            "max_songs": "Number provided by user"
        },
        "examples": [
            {
                "user_input": "I'm feeling nostalgic today and want 10 songs.",
                "playlist_name": "A Trip Down Memory Lane",
                "description": "Songs to take you back in time.",
                "track_count": 10
            }
        ]
    }
    
