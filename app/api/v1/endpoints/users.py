from fastapi import APIRouter, Depends
from app.mcp.fi_mcp import FiMCP
from app.prompts.user_details import FETCH_USER_DETAILS_SYSTEM_PROMPT
from app.schemas.user_details import UserInfo
from app.api.deps import get_fi_mcp
from app.services import user_service

router = APIRouter()

@router.get("/")
async def get_users():
    """Get all users."""
    return {"message": "Users fetched successfully"}


@router.post("/user-info")
async def user_info(fi_mcp: FiMCP = Depends(get_fi_mcp)):
    """Get user info from Fi MCP."""
    try:
        user_info : UserInfo = await fi_mcp.get_response(FETCH_USER_DETAILS_SYSTEM_PROMPT)
        return {"message": "User info fetched successfully", "user_info": user_info}
    except Exception as e:
        return {"message": "Error fetching user info", "error": str(e)}