"""
Gestion de l'état des conversations (State Management).

Permet de conserver le contexte du ReasoningEngine entre deux requêtes API stateless.
Pour S0: Implémentation en mémoire (InMemoryStateStore).
Pour S2: Remplacer par Redis ou PostgreSQL.
"""

from abc import ABC, abstractmethod
from typing import Any, Literal
from dataclasses import dataclass, field
from datetime import datetime
from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.reasoning import ReasoningEngine, ReasoningState
from app.models.database import Conversation, Message


class DialogueMessage(BaseModel):
    """Représente un échange unique dans la conversation."""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    # Pour le vocal ou des métadonnées techniques
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ConversationState:
    """État complet d'une conversation."""
    conversation_id: str
    engine: ReasoningEngine
    history: list[DialogueMessage] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: Literal["user", "assistant", "system"], content: str, **metadata: Any) -> None:
        """Ajoute un message à l'historique."""
        self.history.append(DialogueMessage(
            role=role,
            content=content,
            metadata=metadata
        ))
        self.last_updated = datetime.utcnow()


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


class PostgresStateStore(BaseStateStore):
    """
    Implémentation persistante via SQLAlchemy (Phase S2).
    Compatible avec PostgreSQL (Railway) et SQLite (Local).
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_state(self, conversation_id: str) -> ConversationState | None:
        """Récupère l'état depuis la DB et reconstruit l'objet ConversationState."""
        stmt = (
            select(Conversation)
            .where(Conversation.conversation_id == conversation_id)
            .options(selectinload(Conversation.messages))
        )
        result = await self.session.execute(stmt)
        db_conv = result.scalar_one_or_none()

        if not db_conv:
            return None

        # Reconstruire le moteur de raisonnement
        engine = ReasoningEngine()
        engine._state = ReasoningState(db_conv.reasoning_state)
        engine._steps_completed = db_conv.steps_completed

        # Reconstruire l'historique
        history = [
            DialogueMessage(
                role=msg.role, # type: ignore
                content=msg.content,
                timestamp=msg.created_at,
                metadata=msg.metadata_json
            )
            for msg in db_conv.messages
        ]

        return ConversationState(
            conversation_id=db_conv.conversation_id,
            engine=engine,
            history=history,
            last_updated=db_conv.last_updated
        )

    async def save_state(self, conversation_id: str, state: ConversationState) -> None:
        """Sauvegarde ou met à jour l'état dans la DB."""
        # Vérifier si elle existe déjà
        stmt = (
            select(Conversation)
            .where(Conversation.conversation_id == conversation_id)
            .options(selectinload(Conversation.messages))
        )
        result = await self.session.execute(stmt)
        db_conv = result.scalar_one_or_none()

        if not db_conv:
            db_conv = Conversation(
                conversation_id=conversation_id,
                device_id=state.metadata.get("device_id", "unknown"),
                reasoning_state=state.engine.state.value,
                steps_completed=state.engine.steps_completed
            )
            self.session.add(db_conv)
            await self.session.flush() # Pour avoir l'ID
        else:
            db_conv.reasoning_state = state.engine.state.value
            db_conv.steps_completed = state.engine.steps_completed
            db_conv.last_updated = datetime.utcnow()

        # Synchroniser les nouveaux messages
        # Note: Dans un environnement performant, on ajouterait seulement le dernier.
        # Ici, on simplifie pour le skeleton S2.
        current_msg_count = len(db_conv.messages)
        new_messages = state.history[current_msg_count:]

        for msg in new_messages:
            db_msg = Message(
                conversation_id=db_conv.id,
                role=msg.role,
                content=msg.content,
                metadata_json=msg.metadata,
                created_at=msg.timestamp
            )
            self.session.add(db_msg)

        await self.session.commit()


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
