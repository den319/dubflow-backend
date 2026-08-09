from fastapi import APIRouter

from app.core.response import success_response

router = APIRouter()


@router.get("/health")
def health_check():
    return success_response(
        message="Server is running",
        data={"status": "ok"},
    )