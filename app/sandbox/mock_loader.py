"""
Chargeur de mocks pour le Protocole P4.

P4 - Privacy Sandbox: En phase Alpha, les images réelles ne sont JAMAIS
traitées. Seuls des scénarios prédéfinis (mocks) sont utilisés.

Cette garantie est critique pour:
- Protéger la vie privée de Ginette
- Permettre des tests reproductibles
- Éviter tout traitement d'image non prévu
"""

import json
from pathlib import Path

from pydantic import BaseModel


class MockData(BaseModel):
    """
    Structure d'un mock iAngel.

    Représente un scénario prédéfini avec la réponse attendue
    et les étapes à suivre.
    Mis à jour S1: Supporte les champs cognitifs.
    """

    mock_id: str
    """Identifiant unique (M01, M02, etc.)"""

    scenario: str
    """Nom court du scénario (wifi_connection, photo_share, etc.)"""

    description: str
    """Description détaillée du scénario"""

    expected_response: str
    """Réponse que iAngel devrait donner (correspond à 'current_instruction' en S1)"""

    spoken_response: str | None = None
    """Version orale (correspond à 'spoken_instruction' en S1)"""

    steps: list[str] = []
    """Liste ordonnée des étapes pour guider Ginette"""

    # === Champs S1 (Cognitive) ===
    thought_process: str | None = None
    """Raisonnement interne simulé"""

    emotional_context: str = "neutral"
    """Ton émotionnel (neutral, reassuring, firm, celebratory)"""

    suggested_actions: list[str] = ["C'est fait"]
    """Boutons d'action suggérés"""

    is_completed: bool = False
    """Si le scénario est terminé à cette étape"""


class MockLoader:
    """
    Chargeur de mocks pour le mode sandbox (P4).

    Garantit que JAMAIS une image réelle ne sera traitée
    en phase Alpha - uniquement des mocks prédéfinis.

    Exemple d'utilisation:
        loader = MockLoader(Path("./mocks"))
        scenarios = loader.list_scenarios()  # ["M01", "M02", ...]
        mock = await loader.load_for_scenario("M01")
    """

    def __init__(self, mocks_dir: Path) -> None:
        """
        Initialise le chargeur de mocks.

        Args:
            mocks_dir: Répertoire contenant les fichiers mock JSON
        """
        self.mocks_dir = mocks_dir
        self._cache: dict[str, MockData] = {}

    def list_scenarios(self) -> list[str]:
        """
        Liste tous les scénarios mock disponibles.

        Scanne le répertoire mocks/ pour trouver tous les fichiers
        JSON et retourne leurs identifiants triés.

        Returns:
            Liste des IDs de scénarios (M01, M02, etc.)
        """
        if not self.mocks_dir.exists():
            return []

        scenarios: list[str] = []
        for path in self.mocks_dir.glob("*.json"):
            scenarios.append(path.stem)

        return sorted(scenarios)

    async def load_for_scenario(self, scenario_id: str) -> MockData | None:
        """
        Charge un mock par ID de scénario.

        P4: Cette méthode est la SEULE façon d'obtenir des données
        de "capture" en phase Alpha. Elle garantit qu'aucune image
        réelle n'est jamais traitée.

        Args:
            scenario_id: ID du scénario (M01, M02, etc.)

        Returns:
            Données du mock ou None si non trouvé
        """
        # Vérifier le cache pour éviter les lectures répétées
        if scenario_id in self._cache:
            return self._cache[scenario_id]

        # Construire le chemin du fichier mock
        mock_file = self.mocks_dir / f"{scenario_id}.json"
        if not mock_file.exists():
            return None

        # Charger et valider avec Pydantic
        content = json.loads(mock_file.read_text(encoding="utf-8"))
        mock_data = MockData(**content)

        # Mettre en cache
        self._cache[scenario_id] = mock_data

        return mock_data

    async def load_mock(self, mock_id: str) -> MockData | None:
        """
        Charge un mock par son ID (alias de load_for_scenario).

        Args:
            mock_id: Identifiant du mock (M01, M02, etc.)

        Returns:
            Données du mock ou None si non trouvé
        """
        return await self.load_for_scenario(mock_id)

    def clear_cache(self) -> None:
        """Vide le cache des mocks."""
        self._cache.clear()

    def is_mock_available(self, scenario_id: str) -> bool:
        """
        Vérifie si un scénario mock existe.

        Args:
            scenario_id: ID du scénario à vérifier

        Returns:
            True si le mock existe, False sinon
        """
        mock_file = self.mocks_dir / f"{scenario_id}.json"
        return mock_file.exists()
