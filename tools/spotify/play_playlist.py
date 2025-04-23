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
