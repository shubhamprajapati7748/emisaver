from fastapi import Request
from app.mcp.fi_mcp import FiMCP

async def get_fi_mcp(request: Request) -> FiMCP:
    """Get FiMCP instance from application state."""
    return request.app.state.app_state.fi_mcp 