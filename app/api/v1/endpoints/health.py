"""
Endpoint de santé /health.

Sert de probe pour Railway et UptimeRobot.
La version est lue depuis config, jamais hardcodée.
"""

from fastapi import APIRouter, Depends

from ....models.schemas import HealthResponse
from ....services.health_service import HealthService
from ....core.probes import BaseProbe, ProbeResult

router = APIRouter()


# --- Probes S0 (Mocks) ---
# En S2, ces classes seront déplacées dans app/infrastructure/probes/

class MockDatabaseProbe(BaseProbe):
    async def check(self) -> ProbeResult:
        # S0: On simule que la DB est "skip" ou "ok" (mock)
        return ProbeResult(name="database", status="skip")

class MockLLMProbe(BaseProbe):
    async def check(self) -> ProbeResult:
        # S0: On ne ping pas vraiment Anthropic (coût)
        return ProbeResult(name="llm_api", status="skip")


def get_health_service() -> HealthService:
    """Dependency Provider pour HealthService."""
    service = HealthService()
    # En S0, on enregistre les mocks
    service.register_probe(MockDatabaseProbe())
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
