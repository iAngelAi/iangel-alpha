"""
Tests d'intégration du flux conversationnel (S1-04).

Utilise TestFactory pour garantir la robustesse des données.
"""

import pytest
from unittest.mock import AsyncMock
from app.services.capture_service import CaptureService
from app.core.state import InMemoryStateStore
from tests.factories import TestFactory

@pytest.fixture
def memory_store():
    """Store propre pour le test."""
    store = InMemoryStateStore()
    store._store = {} 
    return store

@pytest.fixture
def mock_sequential_llm():
    """Mock LLM progressif."""
    client = AsyncMock()
    
    # Scénario: 3 étapes définies via la Factory
    step1 = TestFactory.create_decision(
        instruction="Regardez en haut.",
        emotion="neutral",
        actions=["Je vois"]
    )
    step2 = TestFactory.create_decision(
        instruction="Touchez l'icône.",
        emotion="reassuring",
        actions=["Fait"]
    )
    step3 = TestFactory.create_decision(
        instruction="Bravo.",
        emotion="celebratory",
        completed=True,
        actions=["Merci"]
    )
    
    client.generate_decision.side_effect = [step1, step2, step3]
    return client

@pytest.mark.asyncio
class TestConversationFlow:
    
    async def test_multi_turn_conversation_memory(self, memory_store, mock_sequential_llm):
        """Vérifie la persistance du contexte sur 3 tours."""
        service = CaptureService(
            state_store=memory_store,
            llm_client=mock_sequential_llm
        )
        # On force le mode Production pour utiliser le LLM (mocké)
        service.settings.sandbox_mode = False
        
        conv_id = "flow_test_id"
        
        # Tour 1
        req1 = TestFactory.create_request(question="Start", conversation_id=conv_id)
        resp1 = await service.process_capture(req1)
        assert resp1.message == "Regardez en haut."
        
        # Tour 2
        req2 = TestFactory.create_request(question="Next", conversation_id=conv_id)
        resp2 = await service.process_capture(req2)
        assert resp2.message == "Touchez l'icône."
        assert resp2.emotional_context == "reassuring"
        
        # Tour 3
        req3 = TestFactory.create_request(question="End", conversation_id=conv_id)
        resp3 = await service.process_capture(req3)
        assert resp3.message == "Bravo."
        
        # Vérification Mémoire
        final_state = await memory_store.get_state(conv_id)
        assert len(final_state.history) == 6 # 3 tours * 2 messages