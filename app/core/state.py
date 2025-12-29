"""
Gestion de l'état des conversations (State Management).

Permet de conserver le contexte du ReasoningEngine entre deux requêtes API stateless.
Pour S0: Implémentation en mémoire (InMemoryStateStore).
Pour S2: Remplacer par Redis ou PostgreSQL.
"""

from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime

from .reasoning import ReasoningEngine

@dataclass
class ConversationState:
    """État complet d'une conversation."""
    conversation_id: str
    engine: ReasoningEngine
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseStateStore(ABC):
    """Interface abstraite pour le stockage d'état."""

    @abstractmethod
    async def get_state(self, conversation_id: str) -> ConversationState | None:
        """Récupère l'état d'une conversation."""
        pass

    @abstractmethod
    async def save_state(self, conversation_id: str, state: ConversationState) -> None:
        """Sauvegarde l'état."""
        pass


class InMemoryStateStore(BaseStateStore):
    """
    Implémentation en mémoire (Singleton).
    Attention: L'état est perdu au redémarrage du serveur.
    Suffisant pour S0/Alpha.
    """
    _instance = None
    _store: dict[str, ConversationState] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryStateStore, cls).__new__(cls)
        return cls._instance

    async def get_state(self, conversation_id: str) -> ConversationState | None:
        return self._store.get(conversation_id)

    async def save_state(self, conversation_id: str, state: ConversationState) -> None:
        state.last_updated = datetime.now()
        self._store[conversation_id] = state
        self._cleanup()

    def _cleanup(self, ttl_seconds: int = 3600) -> None:
        """Nettoie les sessions expirées (Memory Leak Prevention)."""
        now = datetime.now()
        keys_to_delete = [
            k for k, v in self._store.items() 
            if (now - v.last_updated).total_seconds() > ttl_seconds
        ]
        for k in keys_to_delete:
            del self._store[k]
