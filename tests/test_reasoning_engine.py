"""
Tests du moteur de raisonnement - Protocole P2.

P2: "Une étape à la fois" - Le système DOIT:
1. Retourner UNE SEULE instruction à la fois
2. Attendre la validation de Ginette avant de continuer
3. Ne JAMAIS submerger l'utilisateur avec plusieurs instructions
"""

import pytest

from app.core.reasoning import ReasoningEngine, ReasoningState


class TestReasoningState:
    """Tests de l'énumération ReasoningState."""

    def test_all_states_exist(self) -> None:
        """Tous les états nécessaires sont définis."""
        assert ReasoningState.IDLE == "idle"
        assert ReasoningState.ANALYZING == "analyzing"
        assert ReasoningState.AWAITING_VALIDATION == "awaiting"
        assert ReasoningState.COMPLETED == "completed"

    def test_states_are_strings(self) -> None:
        """Les états sont des chaînes pour sérialisation JSON."""
        for state in ReasoningState:
            assert isinstance(state.value, str)


class TestReasoningEngineInit:
    """Tests d'initialisation du ReasoningEngine."""

    def test_initial_state_is_idle(self) -> None:
        """Le moteur démarre en état IDLE."""
        engine = ReasoningEngine()

        assert engine.state == ReasoningState.IDLE

    def test_no_current_instruction_at_start(self) -> None:
        """Aucune instruction en cours au démarrage."""
        engine = ReasoningEngine()

        assert engine.current_instruction is None

    def test_empty_steps_at_start(self) -> None:
        """Aucune étape complétée au démarrage."""
        engine = ReasoningEngine()

        assert engine.steps_completed == []


class TestAnalyze:
    """Tests de la méthode analyze() - P2 critique."""

    def test_analyze_returns_single_instruction(self) -> None:
        """analyze() retourne UNE SEULE instruction (P2)."""
        engine = ReasoningEngine()

        instruction = engine.analyze("Je veux me connecter au WiFi")

        assert isinstance(instruction, str)
        assert len(instruction) > 0
        # Une seule instruction = pas de liste, pas de numérotation
        assert "\n1." not in instruction
        assert "\n2." not in instruction

    def test_state_becomes_awaiting_after_analyze(self) -> None:
        """Après analyze(), état = AWAITING_VALIDATION."""
        engine = ReasoningEngine()

        engine.analyze("contexte quelconque")

        assert engine.state == ReasoningState.AWAITING_VALIDATION

    def test_current_instruction_set_after_analyze(self) -> None:
        """L'instruction courante est définie après analyze()."""
        engine = ReasoningEngine()

        instruction = engine.analyze("contexte")

        assert engine.current_instruction == instruction
        assert engine.current_instruction is not None

    def test_cannot_analyze_while_awaiting(self) -> None:
        """
        On ne peut pas relancer analyze() si une validation est en attente.

        Note: Le comportement actuel écrase l'instruction précédente.
        En Phase S1, on pourrait lever une exception.
        """
        engine = ReasoningEngine()
        engine.analyze("première demande")
        first_instruction = engine.current_instruction

        # Actuellement, un second analyze() écrase
        engine.analyze("deuxième demande")

        # L'instruction est écrasée (comportement S0)
        # En S1, on pourrait vouloir bloquer ce cas
        assert engine.state == ReasoningState.AWAITING_VALIDATION


class TestValidateStep:
    """Tests de la méthode validate_step() - P2 critique."""

    def test_validate_returns_true_when_awaiting(self) -> None:
        """validate_step() retourne True si en état AWAITING."""
        engine = ReasoningEngine()
        engine.analyze("contexte")

        result = engine.validate_step()

        assert result is True

    def test_validate_returns_false_when_idle(self) -> None:
        """validate_step() retourne False si en état IDLE."""
        engine = ReasoningEngine()

        result = engine.validate_step()

        assert result is False

    def test_state_becomes_idle_after_validation(self) -> None:
        """Après validation, état revient à IDLE."""
        engine = ReasoningEngine()
        engine.analyze("contexte")

        engine.validate_step()

        assert engine.state == ReasoningState.IDLE

    def test_instruction_cleared_after_validation(self) -> None:
        """L'instruction courante est effacée après validation."""
        engine = ReasoningEngine()
        engine.analyze("contexte")

        engine.validate_step()

        assert engine.current_instruction is None

    def test_instruction_added_to_completed_steps(self) -> None:
        """L'instruction validée est ajoutée à l'historique."""
        engine = ReasoningEngine()
        instruction = engine.analyze("contexte")

        engine.validate_step()

        assert instruction in engine.steps_completed

    def test_multiple_validations_build_history(self) -> None:
        """Plusieurs cycles analyze/validate construisent l'historique."""
        engine = ReasoningEngine()

        # Premier cycle
        instr1 = engine.analyze("étape 1")
        engine.validate_step()

        # Deuxième cycle
        instr2 = engine.analyze("étape 2")
        engine.validate_step()

        # Troisième cycle
        instr3 = engine.analyze("étape 3")
        engine.validate_step()

        assert len(engine.steps_completed) == 3
        assert engine.steps_completed[0] == instr1
        assert engine.steps_completed[1] == instr2
        assert engine.steps_completed[2] == instr3


class TestCanProceed:
    """Tests de la méthode can_proceed()."""

    def test_can_proceed_when_idle(self) -> None:
        """can_proceed() retourne True si IDLE."""
        engine = ReasoningEngine()

        assert engine.can_proceed() is True

    def test_cannot_proceed_when_awaiting(self) -> None:
        """can_proceed() retourne False si AWAITING (P2: attendre validation)."""
        engine = ReasoningEngine()
        engine.analyze("contexte")

        assert engine.can_proceed() is False

    def test_can_proceed_after_validation(self) -> None:
        """can_proceed() retourne True après validation."""
        engine = ReasoningEngine()
        engine.analyze("contexte")
        engine.validate_step()

        assert engine.can_proceed() is True


class TestReset:
    """Tests de la méthode reset()."""

    def test_reset_clears_state(self) -> None:
        """reset() remet l'état à IDLE."""
        engine = ReasoningEngine()
        engine.analyze("contexte")

        engine.reset()

        assert engine.state == ReasoningState.IDLE

    def test_reset_clears_instruction(self) -> None:
        """reset() efface l'instruction courante."""
        engine = ReasoningEngine()
        engine.analyze("contexte")

        engine.reset()

        assert engine.current_instruction is None

    def test_reset_clears_history(self) -> None:
        """reset() efface l'historique des étapes."""
        engine = ReasoningEngine()
        engine.analyze("étape 1")
        engine.validate_step()
        engine.analyze("étape 2")
        engine.validate_step()

        engine.reset()

        assert engine.steps_completed == []


class TestComplete:
    """Tests de la méthode complete()."""

    def test_complete_sets_completed_state(self) -> None:
        """complete() met l'état à COMPLETED."""
        engine = ReasoningEngine()
        engine.analyze("contexte")
        engine.validate_step()

        engine.complete()

        assert engine.state == ReasoningState.COMPLETED

    def test_complete_clears_instruction(self) -> None:
        """complete() efface l'instruction courante."""
        engine = ReasoningEngine()
        engine.analyze("contexte")

        engine.complete()

        assert engine.current_instruction is None

    def test_cannot_proceed_after_complete(self) -> None:
        """can_proceed() retourne False après complete()."""
        engine = ReasoningEngine()
        engine.complete()

        assert engine.can_proceed() is False


class TestP2Protocol:
    """Tests de validation du protocole P2 complet."""

    def test_full_p2_cycle(self) -> None:
        """
        Test du cycle complet P2:
        1. Analyser demande → recevoir UNE instruction
        2. Attendre validation
        3. Valider → pouvoir continuer
        4. Répéter jusqu'à completion
        """
        engine = ReasoningEngine()

        # État initial
        assert engine.can_proceed() is True

        # Étape 1: Analyser
        instruction = engine.analyze("Ginette veut envoyer un email")
        assert isinstance(instruction, str)
        assert engine.can_proceed() is False  # P2: doit attendre

        # Étape 2: Valider
        assert engine.validate_step() is True
        assert engine.can_proceed() is True  # P2: peut continuer

        # Étape 3: Nouvelle analyse
        engine.analyze("Ginette a cliqué sur l'icône email")
        assert engine.can_proceed() is False

        # Compléter la session
        engine.validate_step()
        engine.complete()
        assert engine.state == ReasoningState.COMPLETED

    def test_steps_completed_is_immutable_copy(self) -> None:
        """steps_completed retourne une copie, pas la liste interne."""
        engine = ReasoningEngine()
        engine.analyze("test")
        engine.validate_step()

        steps = engine.steps_completed
        steps.append("tentative modification")

        # La liste interne ne doit pas être modifiée
        assert "tentative modification" not in engine.steps_completed
