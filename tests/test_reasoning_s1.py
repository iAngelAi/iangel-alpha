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
            "emotional_context": "angry", # Pas dans la liste autorisée
            "suggested_actions": ["Ok"]
        }
        
        with pytest.raises(ValidationError):
            PedagogicalDecision(**raw_invalid)

    def test_missing_fields_raises_error(self):
        """Si le LLM oublie l'instruction orale, on doit le savoir."""
        raw_incomplete = {
            "thought_process": "...",
            "current_instruction": "...",
            # Manque spoken_instruction
            "suggested_actions": ["Ok"]
        }
        
        with pytest.raises(ValidationError):
            PedagogicalDecision(**raw_incomplete)

    # === TESTS DE ROBUSTESSE UTILISATEUR (Phase S1) ===

    def test_dead_end_prevention(self):
        """
        FAILLE POTENTIELLE: Si le LLM donne une instruction sans bouton d'action,
        l'utilisateur (Ginette) est bloqué.
        Le schéma DOIT refuser une décision non-terminée sans suggested_actions.
        """
        raw_dead_end = {
            "thought_process": "Je demande de cliquer.",
            "current_instruction": "Cliquez ici.",
            "spoken_instruction": "Cliquez ici.",
            "is_completed": False,
            "suggested_actions": [], # VIDE = DANGER POUR GINETTE
            "emotional_context": "neutral"
        }
        
        # Ce test doit lever une erreur si le schéma est bien sécurisé.
        # S'il passe sans erreur, c'est que le code est FAIBLE.
        with pytest.raises(ValidationError, match="dead_end"):
            PedagogicalDecision(**raw_dead_end)

    def test_lazy_thinking_prevention(self):
        """
        FAILLE POTENTIELLE: Le LLM copie le prompt dans la pensée.
        Le schéma doit forcer une distinction entre pensée interne et parole.
        """
        text = "Faites ceci."
        raw_lazy = {
            "thought_process": text,
            "current_instruction": text,
            "spoken_instruction": text, # Copier-coller = Pas d'effort cognitif
            "is_completed": False,
            "suggested_actions": ["Ok"],
            "emotional_context": "neutral"
        }
        
        with pytest.raises(ValidationError, match="lazy_thinking"):
            PedagogicalDecision(**raw_lazy)

    def test_danger_mode_support(self):
        """
        Vérifie que le mode 'firm' est accepté pour les alertes de sécurité.
        """
        raw_danger = {
            "thought_process": "L'utilisateur va cliquer sur un lien phishing.",
            "current_instruction": "N'APPUYEZ PAS ! C'est dangereux.",
            "spoken_instruction": "Attention, ne touchez à rien. C'est une arnaque.",
            "is_completed": False,
            "emotional_context": "firm",
            "suggested_actions": ["J'ai compris"]
        }
        
        decision = PedagogicalDecision(**raw_danger)
        assert decision.emotional_context == "firm"
