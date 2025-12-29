"""
Schémas de structure cognitive (Reasoning Engine S1).

Définit comment le LLM doit structurer sa "pensée".
C'est le contrat strict entre le Prompt Système et le Code Python.
"""

from typing import Literal
from pydantic import BaseModel, Field

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
    
    emotional_context: Literal["neutral", "reassuring", "celebratory", "firm"] = Field(
        default="neutral",
        description="Le ton émotionnel à adopter pour cette étape."
    )
    
    suggested_actions: list[str] = Field(
        default_factory=list,
        description="Actions rapides suggérées (ex: 'C'est fait', 'Je ne trouve pas')."
    )
