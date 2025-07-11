from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check() -> dict[str, str]:
    """Check if the API is healthy.

    Returns:
    --------
        dict: A dictionary containing the status of the API.
    """
    return {"status": "healthy"}
