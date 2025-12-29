"""
Tests du MockLoader - Protocole P4.

P4 - Privacy Sandbox: En phase Alpha, les images réelles ne sont JAMAIS
traitées. Seuls des scénarios prédéfinis (mocks) sont utilisés.

Cette garantie est critique pour:
- Protéger la vie privée de Ginette
- Permettre des tests reproductibles
- Éviter tout traitement d'image non prévu
"""

import json
from pathlib import Path

import pytest

from app.sandbox.mock_loader import MockData, MockLoader


@pytest.fixture
def temp_mocks_dir(tmp_path: Path) -> Path:
    """Crée un répertoire temporaire pour les mocks de test."""
    mocks_dir = tmp_path / "mocks"
    mocks_dir.mkdir()
    return mocks_dir


@pytest.fixture
def sample_mock_data() -> dict:
    """Données mock de test."""
    return {
        "mock_id": "TEST01",
        "scenario": "test_scenario",
        "description": "Scénario de test",
        "expected_response": "Réponse attendue pour le test",
        "steps": ["Étape 1", "Étape 2", "Étape 3"],
    }


@pytest.fixture
def populated_mocks_dir(temp_mocks_dir: Path, sample_mock_data: dict) -> Path:
    """Répertoire mocks avec des fichiers de test."""
    # Créer plusieurs fichiers mock
    mock1 = temp_mocks_dir / "M01.json"
    mock1.write_text(json.dumps(sample_mock_data), encoding="utf-8")

    mock2_data = {
        "mock_id": "M02",
        "scenario": "photo_share",
        "description": "Ginette veut partager une photo",
        "expected_response": "Je vois une photo dans votre galerie.",
        "steps": ["Ouvrez la galerie", "Sélectionnez la photo"],
    }
    mock2 = temp_mocks_dir / "M02.json"
    mock2.write_text(json.dumps(mock2_data), encoding="utf-8")

    return temp_mocks_dir


class TestMockData:
    """Tests du modèle MockData (Pydantic)."""

    def test_valid_mock_data(self, sample_mock_data: dict) -> None:
        """MockData accepte des données valides."""
        mock = MockData(**sample_mock_data)

        assert mock.mock_id == "TEST01"
        assert mock.scenario == "test_scenario"
        assert mock.description == "Scénario de test"
        assert mock.expected_response == "Réponse attendue pour le test"
        assert len(mock.steps) == 3

    def test_mock_data_without_steps(self) -> None:
        """MockData accepte des données sans étapes (liste vide par défaut)."""
        data = {
            "mock_id": "M00",
            "scenario": "simple",
            "description": "Test simple",
            "expected_response": "Réponse",
        }
        mock = MockData(**data)

        assert mock.steps == []

    def test_mock_data_validation(self) -> None:
        """MockData rejette des données invalides."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            MockData(mock_id=123, scenario=None)  # type: ignore[arg-type]


class TestMockLoaderInit:
    """Tests d'initialisation du MockLoader."""

    def test_init_with_path(self, temp_mocks_dir: Path) -> None:
        """MockLoader s'initialise avec un chemin."""
        loader = MockLoader(temp_mocks_dir)

        assert loader.mocks_dir == temp_mocks_dir

    def test_init_creates_empty_cache(self, temp_mocks_dir: Path) -> None:
        """MockLoader démarre avec un cache vide."""
        loader = MockLoader(temp_mocks_dir)

        assert loader._cache == {}


class TestListScenarios:
    """Tests de list_scenarios()."""

    def test_list_empty_directory(self, temp_mocks_dir: Path) -> None:
        """list_scenarios() retourne liste vide si pas de mocks."""
        loader = MockLoader(temp_mocks_dir)

        scenarios = loader.list_scenarios()

        assert scenarios == []

    def test_list_nonexistent_directory(self, tmp_path: Path) -> None:
        """list_scenarios() retourne liste vide si répertoire inexistant."""
        loader = MockLoader(tmp_path / "nonexistent")

        scenarios = loader.list_scenarios()

        assert scenarios == []

    def test_list_scenarios_finds_json_files(self, populated_mocks_dir: Path) -> None:
        """list_scenarios() trouve tous les fichiers JSON."""
        loader = MockLoader(populated_mocks_dir)

        scenarios = loader.list_scenarios()

        assert "M01" in scenarios
        assert "M02" in scenarios

    def test_list_scenarios_sorted(self, populated_mocks_dir: Path) -> None:
        """list_scenarios() retourne les IDs triés."""
        loader = MockLoader(populated_mocks_dir)

        scenarios = loader.list_scenarios()

        assert scenarios == sorted(scenarios)

    def test_list_scenarios_excludes_non_json(self, temp_mocks_dir: Path) -> None:
        """list_scenarios() ignore les fichiers non-JSON."""
        # Créer un fichier non-JSON
        (temp_mocks_dir / "readme.txt").write_text("Not a mock")
        (temp_mocks_dir / "M01.json").write_text('{"mock_id": "M01", "scenario": "test", "description": "Test", "expected_response": "OK"}')

        loader = MockLoader(temp_mocks_dir)
        scenarios = loader.list_scenarios()

        assert "readme" not in scenarios
        assert "M01" in scenarios


class TestLoadForScenario:
    """Tests de load_for_scenario() - P4 critique."""

    @pytest.mark.asyncio
    async def test_load_existing_scenario(
        self, populated_mocks_dir: Path, sample_mock_data: dict
    ) -> None:
        """load_for_scenario() charge un mock existant."""
        loader = MockLoader(populated_mocks_dir)

        mock = await loader.load_for_scenario("M01")

        assert mock is not None
        assert mock.mock_id == sample_mock_data["mock_id"]
        assert mock.scenario == sample_mock_data["scenario"]

    @pytest.mark.asyncio
    async def test_load_nonexistent_scenario(self, temp_mocks_dir: Path) -> None:
        """load_for_scenario() retourne None si mock inexistant."""
        loader = MockLoader(temp_mocks_dir)

        mock = await loader.load_for_scenario("NONEXISTENT")

        assert mock is None

    @pytest.mark.asyncio
    async def test_load_caches_result(self, populated_mocks_dir: Path) -> None:
        """load_for_scenario() met en cache le résultat."""
        loader = MockLoader(populated_mocks_dir)

        # Premier chargement
        mock1 = await loader.load_for_scenario("M01")
        # Deuxième chargement (depuis cache)
        mock2 = await loader.load_for_scenario("M01")

        assert mock1 is mock2  # Même instance
        assert "M01" in loader._cache

    @pytest.mark.asyncio
    async def test_load_validates_json_structure(self, temp_mocks_dir: Path) -> None:
        """load_for_scenario() valide la structure JSON avec Pydantic."""
        # Créer un JSON invalide (manque champs requis)
        invalid_mock = temp_mocks_dir / "INVALID.json"
        invalid_mock.write_text('{"mock_id": "X"}', encoding="utf-8")

        loader = MockLoader(temp_mocks_dir)

        with pytest.raises(Exception):  # Pydantic ValidationError
            await loader.load_for_scenario("INVALID")


class TestLoadMock:
    """Tests de load_mock() - alias de load_for_scenario."""

    @pytest.mark.asyncio
    async def test_load_mock_is_alias(self, populated_mocks_dir: Path) -> None:
        """load_mock() est un alias de load_for_scenario()."""
        loader = MockLoader(populated_mocks_dir)

        mock1 = await loader.load_for_scenario("M01")
        mock2 = await loader.load_mock("M01")

        assert mock1 == mock2


class TestClearCache:
    """Tests de clear_cache()."""

    @pytest.mark.asyncio
    async def test_clear_cache_empties_cache(self, populated_mocks_dir: Path) -> None:
        """clear_cache() vide le cache."""
        loader = MockLoader(populated_mocks_dir)
        await loader.load_for_scenario("M01")
        await loader.load_for_scenario("M02")

        loader.clear_cache()

        assert loader._cache == {}

    @pytest.mark.asyncio
    async def test_reload_after_clear_cache(self, populated_mocks_dir: Path) -> None:
        """Après clear_cache(), les mocks peuvent être rechargés."""
        loader = MockLoader(populated_mocks_dir)
        mock1 = await loader.load_for_scenario("M01")

        loader.clear_cache()
        mock2 = await loader.load_for_scenario("M01")

        # Instances différentes (rechargé du fichier)
        assert mock1 is not mock2
        assert mock1.mock_id == mock2.mock_id


class TestIsMockAvailable:
    """Tests de is_mock_available()."""

    def test_available_mock_returns_true(self, populated_mocks_dir: Path) -> None:
        """is_mock_available() retourne True si mock existe."""
        loader = MockLoader(populated_mocks_dir)

        assert loader.is_mock_available("M01") is True
        assert loader.is_mock_available("M02") is True

    def test_unavailable_mock_returns_false(self, populated_mocks_dir: Path) -> None:
        """is_mock_available() retourne False si mock n'existe pas."""
        loader = MockLoader(populated_mocks_dir)

        assert loader.is_mock_available("NONEXISTENT") is False


class TestP4Protocol:
    """Tests de validation du protocole P4 complet."""

    @pytest.mark.asyncio
    async def test_loader_never_processes_real_images(
        self, populated_mocks_dir: Path
    ) -> None:
        """
        P4: Le loader ne traite JAMAIS d'images réelles.

        Il ne fait que charger des fichiers JSON prédéfinis.
        Aucune méthode n'accepte de données binaires ou de chemins d'images.
        """
        loader = MockLoader(populated_mocks_dir)

        # Vérifier que seuls des scénarios prédéfinis sont disponibles
        scenarios = loader.list_scenarios()
        assert all(isinstance(s, str) for s in scenarios)

        # Charger un scénario retourne des données structurées, pas une image
        mock = await loader.load_for_scenario("M01")
        assert mock is not None
        assert isinstance(mock, MockData)
        assert hasattr(mock, "expected_response")  # Texte, pas image

    def test_mock_files_are_in_mocks_directory(
        self, populated_mocks_dir: Path
    ) -> None:
        """P4: Tous les mocks sont dans le répertoire mocks/."""
        loader = MockLoader(populated_mocks_dir)

        scenarios = loader.list_scenarios()

        for scenario_id in scenarios:
            mock_file = populated_mocks_dir / f"{scenario_id}.json"
            assert mock_file.exists(), f"Mock {scenario_id} doit être dans mocks/"

    @pytest.mark.asyncio
    async def test_mock_contains_expected_response(
        self, populated_mocks_dir: Path
    ) -> None:
        """P4: Chaque mock contient une réponse attendue prédéfinie."""
        loader = MockLoader(populated_mocks_dir)

        for scenario_id in loader.list_scenarios():
            mock = await loader.load_for_scenario(scenario_id)
            assert mock is not None
            assert mock.expected_response, f"Mock {scenario_id} sans expected_response"
            assert len(mock.expected_response) > 0


class TestRealMocksDirectory:
    """Tests avec le vrai répertoire mocks/ du projet."""

    @pytest.fixture
    def project_mocks_dir(self) -> Path:
        """Chemin vers le vrai répertoire mocks/."""
        return Path(__file__).parent.parent / "mocks"

    def test_project_mocks_directory_exists(self, project_mocks_dir: Path) -> None:
        """Le répertoire mocks/ existe dans le projet."""
        assert project_mocks_dir.exists(), "mocks/ doit exister"

    def test_at_least_one_mock_exists(self, project_mocks_dir: Path) -> None:
        """La bibliothèque de mocks est bien garnie (S0-04)."""
        loader = MockLoader(project_mocks_dir)
        scenarios = loader.list_scenarios()

        assert len(scenarios) >= 7, "Il manque des scénarios (M01-M07 attendus)"
        assert "M03" in scenarios
        assert "M07" in scenarios

    @pytest.mark.asyncio
    async def test_m01_mock_is_valid(self, project_mocks_dir: Path) -> None:
        """Les mocks critiques sont valides (M01 WiFi)."""
        loader = MockLoader(project_mocks_dir)
        mock = await loader.load_for_scenario("M01")
        assert mock is not None
        assert "WiFi" in mock.expected_response

    @pytest.mark.asyncio
    async def test_m04_mock_has_voice(self, project_mocks_dir: Path) -> None:
        """Le mock M04 (Virus) a bien une réponse vocale (Voice-Ready)."""
        loader = MockLoader(project_mocks_dir)
        mock = await loader.load_for_scenario("M04")
        assert mock is not None
        assert mock.spoken_response is not None
        assert "Respire" in mock.spoken_response
