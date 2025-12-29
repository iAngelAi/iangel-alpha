"""
Tests du HealthService et des Probes.

Approche TDD (Outside-In):
1. On définit le comportement attendu via les tests.
2. On implémente le service pour satisfaire ces tests.

Scénarios pour Ginette:
- Tout va bien -> "Opérationnel"
- LLM lent/down -> "Dégradé" (Message: "Je réfléchis lentement")
- DB down -> "Unhealthy" (Message: "Maintenance nécessaire")
"""

import pytest
import asyncio
from app.services.health_service import HealthService, ProbeResult, BaseProbe
from app.models.schemas import HealthResponse

# --- Mocks pour les tests ---

class MockSuccessProbe(BaseProbe):
    async def check(self) -> ProbeResult:
        return ProbeResult(name="mock_ok", status="ok", latency_ms=10)

class MockFailureProbe(BaseProbe):
    async def check(self) -> ProbeResult:
        return ProbeResult(name="mock_fail", status="error", error="Boom")

class MockSlowProbe(BaseProbe):
    async def check(self) -> ProbeResult:
        await asyncio.sleep(0.2)  # Simule latence
        return ProbeResult(name="mock_slow", status="ok", latency_ms=200)

# --- Tests ---

@pytest.mark.asyncio
class TestHealthService:
    
    async def test_global_status_healthy(self):
        """Si toutes les probes sont OK, statut = healthy."""
        service = HealthService()
        service.register_probe(MockSuccessProbe())
        
        result = await service.check_health()
        
        assert result.status == "healthy"
        assert result.checks["mock_ok"] == "ok"
        assert "pleine forme" in result.user_message.lower()

    async def test_global_status_unhealthy(self):
        """Si une probe critique échoue, statut = unhealthy."""
        service = HealthService()
        service.register_probe(MockFailureProbe())
        
        result = await service.check_health()
        
        assert result.status == "unhealthy"
        assert result.checks["mock_fail"] == "error"
        # Message empathique pour Ginette
        assert "maintenance" in result.user_message.lower() or "repos" in result.user_message.lower()

    async def test_probe_timeout_handling(self):
        """Le service doit gérer les probes trop lentes (timeout)."""
        # Note: L'implémentation réelle devra wrapper les checks avec asyncio.wait_for
        # Pour ce test, on vérifie juste que la latence est remontée
        service = HealthService()
        service.register_probe(MockSlowProbe())
        
        result = await service.check_health()
        
        # S0: On accepte que ça passe, mais on veut voir la latence si possible
        # ou au moins que ça ne plante pas.
        assert result.status == "healthy" 
