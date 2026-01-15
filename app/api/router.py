"""
Routeur principal de l'API iAngel.

Agrège tous les endpoints v1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import capture, health

api_router = APIRouter()

# Health endpoint (sans préfixe additionnel)
api_router.include_router(health.router, tags=["Health"])

# Capture endpoint
api_router.include_router(capture.router, tags=["Capture"])
