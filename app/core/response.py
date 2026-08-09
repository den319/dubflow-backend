from typing import Any
from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Universal API response wrapper."""
    message: str
    success: bool
    data: Any = None


def success_response(message: str, data: Any = None) -> dict:
    """Build a success response in the universal format."""
    return {
        "message": message,
        "success": True,
        "data": data,
    }


def error_response(message: str, data: Any = None) -> dict:
    """Build an error response in the universal format."""
    return {
        "message": message,
        "success": False,
        "data": data,
    }