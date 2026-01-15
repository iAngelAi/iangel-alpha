"""
Service de santé (HealthService).

Responsabilité:
- Orchestrer les sondes (Probes)
- Agréger les résultats
- Déterminer le statut global (healthy, degraded, unhealthy)
- Formater le message pour Ginette
"""

from app.core.probes import BaseProbe, ProbeResult
from app.models.schemas import HealthResponse
from app.config import get_settings

class HealthService:
    def __init__(self) -> None:
        self.probes: list[BaseProbe] = []

    def register_probe(self, probe: BaseProbe) -> None:
        """Ajoute une sonde à surveiller."""
        self.probes.append(probe)

    async def check_health(self) -> HealthResponse:
        """Exécute toutes les sondes et retourne le bilan."""
        settings = get_settings()
        checks: dict[str, str] = {}
        global_status = "healthy"
        errors = []

        for probe in self.probes:
            try:
                # TODO: Ajouter timeout ici (asyncio.wait_for)
                result = await probe.check()
                checks[result.name] = result.status
                
                if result.status == "error":
                    global_status = "unhealthy"
                    errors.append(f"{result.name}: {result.error}")
            except Exception as e:
                checks["unknown"] = "error"
                global_status = "unhealthy"
                errors.append(str(e))

        # Logique message Ginette
        if global_status == "healthy":
            msg = "Je me sens en pleine forme! Tout est opérationnel."
        elif global_status == "degraded":
            msg = "Je suis un peu lent aujourd'hui, merci de votre patience."
        else:
            msg = "Je dois prendre un petit moment de repos (Maintenance)."

        return HealthResponse(
            status=global_status,  # type: ignore[arg-type]
            version=settings.app_version,
            environment=settings.environment,
            checks=checks,
            user_message=msg,
            error_details="; ".join(errors) if errors else None
        )
