"""
Tests du contrat cognitif S1 (Reasoning Engine).

Vérifie que la structure de pensée est respectée et robuste.
"""

import json
import pytest
from pydantic import ValidationError
from app.core.llm.schemas import PedagogicalDecision

class TestPedagogicalDecisionSchema:
    
    def test_valid_decision_parsing(self):
        """Un JSON valide du LLM doit être parsé correctement."""
        raw_llm_output = {
            "thought_process": "L'utilisateur est confus. Il faut le rassurer avant d'agir.",
            "current_instruction": "Appuyez sur le bouton bleu.",
            "spoken_instruction": "C'est simple, appuie sur le bouton bleu.",
            "is_completed": False,
            "emotional_context": "reassuring",
            "suggested_actions": ["C'est fait"]
        }
        
        decision = PedagogicalDecision(**raw_llm_output)
        
        assert decision.is_completed is False
        assert decision.emotional_context == "reassuring"
        assert len(decision.suggested_actions) == 1

    def test_invalid_emotion_raises_error(self):
        """Une émotion inconnue doit lever une erreur de validation."""
        raw_invalid = {
            "thought_process": "...",
            "current_instruction": "...",
            "spoken_instruction": "...",
            "emotional_context": "angry" # Pas dans la liste autorisée
        }
        
        with pytest.raises(ValidationError):
            PedagogicalDecision(**raw_invalid)

    def test_missing_fields_raises_error(self):
        """Si le LLM oublie l'instruction orale, on doit le savoir."""
        raw_incomplete = {
            "thought_process": "...",
            "current_instruction": "..."
            # Manque spoken_instruction
        }
        
        with pytest.raises(ValidationError):
            PedagogicalDecision(**raw_incomplete)
