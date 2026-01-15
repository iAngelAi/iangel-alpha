"""
Classe de base pour les adaptateurs LLM.

TODO Phase S1: Implémenter avec:
- Interface abstraite LLMProvider
- Adaptateur Anthropic Claude
- Gestion des erreurs et retry
- Logging des appels
"""

from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.core.llm.schemas import PedagogicalDecision


class LLMResponse(BaseModel):
    """Réponse standardisée d'un LLM."""

    content: str
    model: str
    tokens_used: int | None = None


class LLMProvider(ABC):
    """Interface abstraite pour les fournisseurs LLM."""

    @abstractmethod
    async def generate(
        self,
        system_prompt: str,
        user_message: str,
        *,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        """
        Génère une réponse du LLM.

        Args:
            system_prompt: Instructions système
            user_message: Message utilisateur
            max_tokens: Limite de tokens

        Returns:
            Réponse structurée du LLM
        """
        ...

    @abstractmethod
    async def generate_decision(
        self,
        system_prompt: str,
        user_message: str,
        image_data: str | None = None,
    ) -> PedagogicalDecision:
        """
        Génère une décision pédagogique structurée (S1).
        Obligatoire pour le Reasoning Engine.
        """
        ...
