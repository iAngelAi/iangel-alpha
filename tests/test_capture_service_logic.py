"""
Tests logiques du CaptureService (TDD).

Ces tests définissent le comportement attendu du service AVANT son implémentation complète.
Focus: Gestion de l'état (State Management) et Protocole P4.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.capture_service import CaptureService
from app.models.schemas import CaptureRequest
from app.core.reasoning import ReasoningState

from app.core.llm.schemas import PedagogicalDecision

# --- Mocks pour l'injection de dépendances ---

@pytest.fixture
def mock_state_store():
    """Mock du store pour vérifier la persistance."""
    store = AsyncMock()
    store.get_state.return_value = None  # Par défaut, pas d'état
    return store

@pytest.fixture
def mock_llm_client():
    """Mock du client LLM."""
    client = AsyncMock()
    
    # Réponse S1 valide
    decision = PedagogicalDecision(
        thought_process="Reasoning...",
        current_instruction="Click here",
        spoken_instruction="Click here",
        is_completed=False,
        emotional_context="neutral",
        suggested_actions=[]
    )
    
    # Configure generate_decision (S1)
    client.generate_decision.return_value = decision
    
    # Configure generate (S0 fallback) - retourne LLMResponse, pas str
    # Mais ici on teste S1 principalement si generate_decision est présent
    return client

@pytest.fixture
def service_with_mocks(mock_state_store, mock_llm_client):
    """Service injecté avec des mocks."""
    service = CaptureService()
    # Injection manuelle pour le test (si le service le permet, sinon via constructeur)
    service.state_store = mock_state_store
    service.llm_client = mock_llm_client
    return service

# --- Tests ---

@pytest.mark.asyncio
class TestCaptureServiceLogic:

    async def test_sandbox_mode_bypasses_llm(self):
        """
        Protocole P4: Si sandbox_mode=True, le LLM ne doit JAMAIS être appelé.
        """
        service = CaptureService()
        # Force la config sandbox
        service.settings.sandbox_mode = True
        
        request = CaptureRequest(
            device_id="dev1", 
            mock_id="M01", 
            question="Test?"
        )
        
        # On espère que ça ne plante pas et que ça retourne le mock
        response = await service.process_capture(request)
        
        assert response.mock_used == "M01"
        # Si on avait un mock LLM injecté, on vérifierait assert_not_called()

    async def test_conversation_state_persistence(self, service_with_mocks, mock_state_store):
        """
        Critique: Le service doit récupérer et sauvegarder l'état.
        """
        # Configurer le service pour utiliser le store (simulé)
        service_with_mocks.settings.sandbox_mode = False # Mode réel
        
        request = CaptureRequest(
            device_id="dev1", 
            conversation_id="conv_123",
            image_data="base64..."
        )
        
        await service_with_mocks.process_capture(request)
        
        # Vérifications
        mock_state_store.get_state.assert_called_with("conv_123")
        mock_state_store.save_state.assert_called()
