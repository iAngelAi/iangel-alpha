"""
Models Pydantic pour iAngel.

Schémas de données avec typage strict.
"""

from .schemas import (
    CaptureRequest,
    CaptureResponse,
    HealthResponse,
)

__all__ = [
    "HealthResponse",
    "CaptureRequest",
    "CaptureResponse",
]
