from mcp_instance import mcp
from dotenv import load_dotenv
load_dotenv()

# Import create-playlist tool
from tools.spotify.create_playlist import create_playlist

# Import add-tracks tool
from tools.spotify.add_tracks_to_playlist import add_tracks_to_playlist

# Import search-tracks tool
from tools.spotify.search_tracks import search_tracks

# Import play-playlist tool
from tools.spotify.play_playlist import play_playlist

# Import add-fixed-track tool
from tools.custom.add_fixed_track import add_fixed_track

# Import analyze-emotion tool
from tools.custom.analyze_emotion import analyze_emotion

# Import search-tracks-online tool
from tools.custom.search_tracks_online import search_tracks_online


