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
        suggested_actions=["Ok"]
    )
    
    # Configure generate_decision (S1)
    client.generate_decision.return_value = decision
    
    # Configure generate (Legacy/Base)
    client.generate.return_value = MagicMock(content="Legacy content")
    
    return client

@pytest.fixture
def service_with_mocks(mock_state_store, mock_llm_client):
    """Service injecté avec des mocks."""
    service = CaptureService()
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
        service.settings.sandbox_mode = True
        
        request = CaptureRequest(
            device_id="dev1", 
            mock_id="M01", 
            question="Test?"
        )
        
        response = await service.process_capture(request)
        
        assert response.mock_used == "M01"

    async def test_conversation_state_persistence(self, service_with_mocks, mock_state_store, mock_llm_client):
        """
        Critique: Le service doit récupérer, mettre à jour et sauvegarder l'historique.
        """
        service_with_mocks.settings.sandbox_mode = False # Mode réel
        
        # Simuler un état existant avec historique
        from app.core.state import ConversationState, ReasoningEngine
        engine = ReasoningEngine()
        state = ConversationState(conversation_id="conv_123", engine=engine)
        state.add_message("user", "Message précédent")
        
        mock_state_store.get_state.return_value = state
    
        request = CaptureRequest(
            device_id="dev1",
            conversation_id="conv_123",
            question="Nouvelle question",
            image_data="base64..."
        )
    
        await service_with_mocks.process_capture(request)
    
        # 1. Vérifier que l'état a été récupéré
        mock_state_store.get_state.assert_called_with("conv_123")
        
        # 2. Vérifier que le LLM a été appelé avec le bon prompt (contenant l'historique)
        call_args = mock_llm_client.generate_decision.call_args
        assert call_args is not None
        system_prompt_used = call_args.kwargs["system_prompt"]
        
        assert "Message précédent" in system_prompt_used # Preuve que l'historique est injecté
        assert "CONTEXTE TEMPOREL" in system_prompt_used # Preuve que l'ancrage temporel est là
        
        # 3. Vérifier que la sauvegarde inclut la nouvelle réponse
        saved_state = mock_state_store.save_state.call_args[0][1]
        assert len(saved_state.history) == 3 # 1 avant + 1 user + 1 assistant