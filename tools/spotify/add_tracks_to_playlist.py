# Create tool to add tracks to a playlist

import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages")
import requests

import os
import json
from typing import List, Dict, Any
from orchestrator.mcp_instance import mcp
from dotenv import load_dotenv
import base64
from datetime import datetime, timedelta

load_dotenv()

SPOTIFY_API_BASE = 'https://api.spotify.com/v1'
SPOTIFY_ACCOUNTS_BASE = 'https://accounts.spotify.com'

def load_tokens() -> Dict[str, str]:
    access_token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')
    
    if access_token and refresh_token:
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'servers', 'spotify-mcp-server', 'spotify-config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
            return {
                'access_token': config['accessToken'],
                'refresh_token': config['refreshToken']
            }
    except:
        raise Exception("No Spotify tokens found")

tokens = load_tokens()
token_expiry = datetime.now() + timedelta(hours=1)

def refresh_access_token() -> None:
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token']
    }

    response = requests.post(f'{SPOTIFY_ACCOUNTS_BASE}/api/token', headers=headers, data=data)
    if not response.ok:
        raise Exception(f"Failed to refresh token: {response.text}")

    response_data = response.json()
    tokens['access_token'] = response_data['access_token']

def make_spotify_request(method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    global token_expiry
    if datetime.now() >= token_expiry:
        refresh_access_token()
    
    headers = {
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Content-Type': 'application/json'
    }

    url = f'{SPOTIFY_API_BASE}{endpoint}'
    response = requests.request(method, url, headers=headers, json=data)

    if not response.ok:
        error_msg = response.json().get('error', {}).get('message', 'Unknown error')
        raise Exception(f'Spotify API error: {error_msg}')
    
    return response.json()

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
        return "Tracks added successfully to playlist"
    except Exception as e:
        return f"Failed to add tracks to playlist: {str(e)}"

