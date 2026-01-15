"""
Modèles de données SQLAlchemy (Phase S2).

Définit la structure des tables pour la persistance des conversations.
"""

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Conversation(Base):
    """
    Table des conversations.
    Stocke l'état global du ReasoningEngine pour un utilisateur.
    """
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conversation_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    device_id: Mapped[str] = mapped_column(String(100), index=True)

    # État du moteur de raisonnement (sérialisé)
    reasoning_state: Mapped[str] = mapped_column(String(50), default="idle")
    steps_completed: Mapped[list[str]] = mapped_column(JSON, default=list)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relations
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at"
    )


class Message(Base):
    """
    Table des messages (historique).
    Stocke chaque échange individuel.
    """
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"))

    role: Mapped[str] = mapped_column(String(20)) # user, assistant, system
    content: Mapped[str] = mapped_column(Text)

    # Métadonnées S1 (spoken, emotion, etc.)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relations
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
