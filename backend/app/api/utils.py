from fastapi import APIRouter

router = APIRouter(prefix="/utils", tags=["utils"])


@router.get("/health-check/")
async def health_check() -> bool:
    """Health check endpoint for the API.

    Returns
    -------
    bool
        Always True if the service is running.
    """
    return True
