"""
Module de raisonnement iAngel - Protocole P2.

Règle P2: "Une étape à la fois" - JAMAIS plusieurs instructions simultanées.
Le système DOIT attendre la validation avant de proposer l'étape suivante.

Cette architecture garantit que Ginette (72 ans) ne soit jamais submergée
par trop d'informations à la fois.
"""

from enum import Enum
from .llm.schemas import PedagogicalDecision


class ReasoningState(str, Enum):
    """
    États du moteur de raisonnement.

    Le cycle de vie normal est:
    IDLE -> ANALYZING -> AWAITING_VALIDATION -> IDLE (ou COMPLETED)
    """

    IDLE = "idle"
    """Aucune session active, prêt pour nouvelle analyse."""

    ANALYZING = "analyzing"
    """Analyse en cours du contexte utilisateur."""

    AWAITING_VALIDATION = "awaiting"
    """Attend la validation de l'utilisateur avant de continuer."""

    COMPLETED = "completed"
    """Session terminée avec succès."""


class ReasoningEngine:
    """
    Moteur de raisonnement P2 - Une étape à la fois.

    Garantit que Ginette reçoit UNE SEULE instruction à la fois
    et que le système attend sa validation avant de continuer.
    """

    def __init__(self) -> None:
        """Initialise le moteur en état IDLE."""
        self._state = ReasoningState.IDLE
        self._current_instruction: str | None = None
        self._spoken_instruction: str | None = None
        self._steps_completed: list[str] = []
        self._last_decision: PedagogicalDecision | None = None

    @property
    def state(self) -> ReasoningState:
        """État actuel du moteur."""
        return self._state

    @property
    def current_instruction(self) -> str | None:
        """Instruction en cours d'attente de validation."""
        return self._current_instruction

    @property
    def steps_completed(self) -> list[str]:
        """Liste des étapes validées."""
        return self._steps_completed.copy()

    def process_decision(self, decision: PedagogicalDecision) -> str:
        """
        Traite une décision structurée du LLM (S1).
        
        Met à jour l'état du moteur selon la décision cognitive.
        """
        self._state = ReasoningState.ANALYZING
        self._last_decision = decision
        
        if decision.is_completed:
            self.complete()
            return decision.current_instruction

        self._current_instruction = decision.current_instruction
        self._spoken_instruction = decision.spoken_instruction
        self._state = ReasoningState.AWAITING_VALIDATION
        
        return decision.current_instruction

    def analyze(self, context: str) -> str:
        """
        Analyse le contexte (Mode S0 / Fallback).
        Pour S1, utiliser process_decision().
        """
        self._state = ReasoningState.ANALYZING

        # S0 Behavior (Stub)
        instruction = "Regardez l'écran et dites-moi ce que vous voyez."

        self._current_instruction = instruction
        self._state = ReasoningState.AWAITING_VALIDATION

        return instruction

    def validate_step(self) -> bool:
        """
        Valide l'étape courante.
        """
        if self._state != ReasoningState.AWAITING_VALIDATION:
            return False

        if self._current_instruction:
            self._steps_completed.append(self._current_instruction)

        self._current_instruction = None
        self._spoken_instruction = None
        self._state = ReasoningState.IDLE

        return True

    def complete(self) -> None:
        self._state = ReasoningState.COMPLETED
        self._current_instruction = None
        self._spoken_instruction = None

    def reset(self) -> None:
        self._state = ReasoningState.IDLE
        self._current_instruction = None
        self._spoken_instruction = None
        self._steps_completed.clear()
        self._last_decision = None

    def can_proceed(self) -> bool:
        return self._state == ReasoningState.IDLE
