"""
Tests de l'historique des conversations (S1).

Vérifie que iAngel a maintenant une mémoire structurée pour
ne pas oublier les doutes de Ginette.
"""

import pytest
from app.core.state import ConversationState, DialogueMessage
from app.core.reasoning import ReasoningEngine

class TestStateHistory:

    def test_add_message_to_history(self):
        """Vérifie l'ajout simple d'un message."""
        state = ConversationState(conversation_id="test_123", engine=ReasoningEngine())
        
        state.add_message("user", "Je ne trouve pas le bouton WiFi")
        state.add_message("assistant", "Ne vous inquiétez pas, il est en haut à droite.", mood="reassuring")
        
        assert len(state.history) == 2
        assert state.history[0].role == "user"
        assert state.history[1].role == "assistant"
        assert state.history[1].metadata["mood"] == "reassuring"

    def test_history_order_preserved(self):
        """Vérifie que l'ordre chronologique est respecté."""
        state = ConversationState(conversation_id="test_seq", engine=ReasoningEngine())
        messages = ["Bonjour", "Comment ça va ?", "Bien et vous ?"]
        
        for msg in messages:
            state.add_message("user", msg)
            
        assert [m.content for m in state.history] == messages

    def test_last_updated_refreshed(self):
        """Le timestamp de mise à jour doit changer à chaque message."""
        state = ConversationState(conversation_id="test_time", engine=ReasoningEngine())
        old_time = state.last_updated
        
        state.add_message("user", "Hello")
        
        assert state.last_updated > old_time
