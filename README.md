# Custom Spotify MCP

This project is a custom MCP server that integrates Spotify to generate playlists based on user emotions.

## Setup Instructions

Follow these steps to set up and run the project:

### 1. Install Dependencies
Install `uv` using Homebrew:
```bash
brew install uv
```

### 2. Clone the Repository
Clone this repository to a directory of your choice:
```bash
git clone <repository-url>
cd <repository-directory>
```

### 3. Initialize the Environment
Open a terminal in the cloned directory and run:
```bash
uv init
```

### 4. Create Environment Variables
```bash
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback (Needs to be identical with the URI saved in Spotify Developer's App Settings)
```
Run 
```bash
python3 util/spotify_auth.py
```
or 
```bash
python util/spotify_auth.py
```
To generate the access tokens. Needs to be created every hour

### 4. Install MCP Server to Claude
```bash
mcp install server.py
```

### TroubleShooting
If uv init doesn't work, manually add the required libraries:
```bash
uv add "mcp[cli]"
uv add "requests"
```

### Notes
Ensure you have created a Spotify Developer App and configured:
  - Client ID
	-	Client Secret
	-	Redirect URI
	-	These credentials should be securely added in spotify_auth.py.
	-	You may need to adjust mcp.yaml to properly configure your tool for the MCP ecosystem.

### Useful Links
	•	Spotify API Documentation
	•	Model Context Protocol Python SDK










