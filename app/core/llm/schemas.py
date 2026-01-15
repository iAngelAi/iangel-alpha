"""
Schémas de structure cognitive (Reasoning Engine S1).

Définit comment le LLM doit structurer sa "pensée".
C'est le contrat strict entre le Prompt Système et le Code Python.
"""

from typing import Literal, Self

from pydantic import BaseModel, Field, model_validator


class PedagogicalDecision(BaseModel):
    """
    Structure de décision pédagogique retournée par le LLM.
    Force le modèle à séparer le raisonnement de l'instruction.
    """

    thought_process: str = Field(
        ...,
        description="Raisonnement interne du modèle. Analyse de la situation, du contexte et de l'état émotionnel supposé."
    )

    current_instruction: str = Field(
        ...,
        description="L'instruction UNIQUE et IMMÉDIATE pour l'utilisateur. Doit être simple et directe."
    )

    spoken_instruction: str = Field(
        ...,
        description="Version de l'instruction optimisée pour la synthèse vocale (plus conversationnelle)."
    )

    is_completed: bool = Field(
        default=False,
        description="Indique si l'objectif global de l'utilisateur est atteint."
    )

    emotional_context: Literal["neutral", "reassuring", "celebratory", "firm", "protective"] = Field(
        ...,
        description="Ton émotionnel adapté à la situation."
    )

    suggested_actions: list[str] = Field(
        default_factory=list,
        description="Actions rapides suggérées (ex: 'C'est fait', 'Je ne trouve pas')."
    )

    @model_validator(mode='after')
    def check_dead_ends(self) -> Self:
        """
        Vérifie que l'utilisateur n'est pas bloqué sans action possible.
        Si la tâche n'est pas finie, il FAUT des boutons d'action.
        """
        if not self.is_completed and not self.suggested_actions:
            raise ValueError("dead_end: Impossible de continuer sans actions suggérées (suggested_actions vide).")
        return self

    @model_validator(mode='after')
    def check_lazy_thinking(self) -> Self:
        """
        Vérifie que le modèle fait un effort de distinction entre pensée et parole.
        """
        # Nettoyage basique pour comparaison
        thought = self.thought_process.strip().lower()
        spoken = self.spoken_instruction.strip().lower()

        if thought == spoken:
            raise ValueError("lazy_thinking: Le processus de pensée ne doit pas être une copie de l'instruction.")

        return self
