from mcp_instance import mcp

@mcp.tool()
def analyze_emotion(user_prompt: str) -> str:
    """Extract the user's emotion from their prompt and generate an enhanced search prompt"""
    emotion_keywords = {
        "sad": "uplifting songs to improve mood",
        "happy": "songs to celebrate happiness",
        "angry": "calming songs for relaxation",
        "tired": "energizing songs to wake up",
        "anxious": "relaxing songs to reduce anxiety",
        "excited": "energizing songs to get pumped up",
        "relaxed": "chill songs to relax and unwind",
        "bored": "fun and upbeat songs to liven up the mood",
        "stressed": "calming songs to reduce stress",
        "lonely": "warm and comforting songs to feel connected",
        "grateful": "inspiring songs to appreciate life",
        "nostalgic": "melancholic songs to reminisce",
        "focused": "uplifting songs to stay motivated",
        "energetic": "energizing songs to keep the energy high",
        "sleepy": "soothing songs to help fall asleep",
        "energized": "energizing songs to stay focused",
        "motivated": "uplifting songs to boost motivation",
        "nostalgic": "melancholic songs to reminisce",
        "calm": "soothing songs to relax and unwind",
    }

    for keyword, search_prompt in emotion_keywords.items():
        if keyword in user_prompt.lower():
            return f"Best songs for {search_prompt}"

    # Default search prompt if no emotion matched
    return "Best songs for any mood"