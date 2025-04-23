from mcp_instance import mcp



# For Testing (Should be deleted)
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# For Testing (Should be deleted)
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"