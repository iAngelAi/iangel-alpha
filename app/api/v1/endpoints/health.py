"""
Endpoint de santé /health.

Sert de probe pour Railway et UptimeRobot.
La version est lue depuis config, jamais hardcodée.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schemas import HealthResponse
from app.services.health_service import HealthService
from app.core.probes import BaseProbe, ProbeResult
from app.core.database import get_db
from app.infrastructure.probes import DatabaseProbe

router = APIRouter()


# --- Probes Restants (Mocks) ---
class MockLLMProbe(BaseProbe):
    async def check(self) -> ProbeResult:
        # S0: On ne ping pas vraiment Anthropic (coût)
        return ProbeResult(name="llm_api", status="skip")


def get_health_service(db: AsyncSession = Depends(get_db)) -> HealthService:
    """Dependency Provider pour HealthService."""
    service = HealthService()
    # Phase S2: Sonde réelle pour la DB
    service.register_probe(DatabaseProbe(db))
    # S1: Toujours mocké pour l'instant
    service.register_probe(MockLLMProbe())
    return service


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Vérification de santé du service",
    description="Retourne le statut du backend iAngel et de ses dépendances.",
    tags=["Health"],
)
async def health_check(
    service: HealthService = Depends(get_health_service)
) -> HealthResponse:
    """
    Vérifie la santé du service via le HealthService.

    Returns:
        HealthResponse avec statut actuel, version et message pour Ginette.
    """
    return await service.check_health()
