"""
Sondes de santé pour l'infrastructure (Phase S2).

Implémente les sondes réelles pour la base de données et autres services tiers.
"""

import time

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.probes import BaseProbe, ProbeResult


class DatabaseProbe(BaseProbe):
    """
    Sonde de santé pour la base de données.
    Exécute une requête simple (SELECT 1) pour vérifier la connectivité.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def check(self) -> ProbeResult:
        start_time = time.time()
        try:
            # Exécuter un ping simple
            await self.session.execute(text("SELECT 1"))
            latency = int((time.time() - start_time) * 1000)
            return ProbeResult(name="database", status="ok", latency_ms=latency)
        except Exception as e:
            return ProbeResult(name="database", status="error", error=str(e))
