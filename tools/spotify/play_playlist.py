# Create tool to play the playlist created by the mcp

import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages")
import requests
import os
import json
import base64
from datetime import datetime, timedelta
from typing import Dict, Any
from mcp_instance import mcp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API endpoints
SPOTIFY_API_BASE = 'https://api.spotify.com/v1'
SPOTIFY_ACCOUNTS_BASE = 'https://accounts.spotify.com'

# Load tokens from environment or local file
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
        raise Exception("No Spotify tokens found in environment or config file")

# Store tokens and token expiry
tokens = load_tokens()
token_expiry = datetime.now() + timedelta(hours=1)

def refresh_access_token() -> None:
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise Exception("Spotify client credentials not found in environment")

    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()

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
    global token_expiry
    token_expiry = datetime.now() + timedelta(seconds=response_data['expires_in'])

def make_spotify_request(method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
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
