import os
import base64
import requests
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import json
from urllib.parse import parse_qs, urlparse

# Load environment variables
load_dotenv()

class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL and query parameters
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Check if this is the callback with the authorization code
        if 'code' in query_params:
            code = query_params['code'][0]
            
            # Exchange the authorization code for access and refresh tokens
            tokens = exchange_code_for_tokens(code)
            
            # Save tokens to .env file
            save_tokens_to_env(tokens)
            
            # Send success response to browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Authentication successful! You can close this window.')
            
            # Stop the server
            self.server.shutdown()
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Authentication failed. No authorization code received.')

def exchange_code_for_tokens(code: str) -> dict:
    """Exchange authorization code for access and refresh tokens."""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    # Create basic auth header
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    
    if not response.ok:
        raise Exception(f"Failed to get tokens: {response.text}")
    
    return response.json()

def save_tokens_to_env(tokens: dict) -> None:
    """Save tokens to .env file."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    
    # Read existing .env file
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update or add token lines
    new_lines = []
    tokens_added = False
    
    for line in lines:
        if line.startswith('SPOTIFY_ACCESS_TOKEN='):
            new_lines.append(f'SPOTIFY_ACCESS_TOKEN={tokens["access_token"]}\n')
            tokens_added = True
        elif line.startswith('SPOTIFY_REFRESH_TOKEN='):
            new_lines.append(f'SPOTIFY_REFRESH_TOKEN={tokens["refresh_token"]}\n')
            tokens_added = True
        else:
            new_lines.append(line)
    
    # If tokens weren't in the file, add them
    if not tokens_added:
        new_lines.append(f'SPOTIFY_ACCESS_TOKEN={tokens["access_token"]}\n')
        new_lines.append(f'SPOTIFY_REFRESH_TOKEN={tokens["refresh_token"]}\n')
    
    # Write back to .env file
    with open(env_path, 'w') as f:
        f.writelines(new_lines)

def main():
    # Get environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    if not client_id or not redirect_uri:
        raise Exception("SPOTIFY_CLIENT_ID and SPOTIFY_REDIRECT_URI must be set in .env file")
    
    # Create authorization URL
    scope = 'playlist-modify-public playlist-modify-private user-read-playback-state user-modify-playback-state'
    auth_url = (
        'https://accounts.spotify.com/authorize'
        f'?client_id={client_id}'
        f'&response_type=code'
        f'&redirect_uri={redirect_uri}'
        f'&scope={scope}'
    )
    
    # Start local server to handle the callback
    server = HTTPServer(('localhost', 8888), SpotifyAuthHandler)
    
    # Open the authorization URL in the default browser
    print("Opening browser for Spotify authorization...")
    webbrowser.open(auth_url)
    
    # Start the server to handle the callback
    print("Waiting for authorization...")
    server.serve_forever()
    
    print("Authentication successful! Tokens have been saved to .env file.")
  

    # Close the server
    server.server_close()

if __name__ == '__main__':
    print("Starting Spotify authentication...")
    main() 
