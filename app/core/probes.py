"""
Interface pour les sondes de santé (Probes).

Architecture Probe:
Chaque composant critique (DB, LLM) doit avoir sa propre sonde.
Cela permet de découpler le HealthService de l'implémentation technique des composants.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ProbeResult:
    """Résultat d'une vérification de sonde."""
    name: str
    status: str  # "ok", "error", "skip"
    latency_ms: int = 0
    error: str | None = None


class BaseProbe(ABC):
    """Classe abstraite pour toutes les sondes."""

    @abstractmethod
    async def check(self) -> ProbeResult:
        """Exécute la vérification."""
        pass
