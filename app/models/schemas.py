"""
Schémas Pydantic V2 pour l'API iAngel.

Typage strict obligatoire - pas de dict brut ni de Any.
"""

from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import uuid4

# On importe les types émotifs pour cohérence
EMOTIONAL_CONTEXTS = Literal["neutral", "reassuring", "celebratory", "firm", "protective"]

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════════════
# Health Endpoint
# ═══════════════════════════════════════════════════════════════════════════


class HealthResponse(BaseModel):
    """Réponse de l'endpoint /health."""

    status: Literal["healthy", "unhealthy", "degraded"]
    version: str
    environment: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    checks: dict[str, str] = Field(description="Statut détaillé par composant")
    user_message: str = Field(description="Message affichable à l'utilisateur (Ginette)")
    error_details: str | None = None


# ═══════════════════════════════════════════════════════════════════════════
# Capture Endpoint (Phase S0-03)
# ═══════════════════════════════════════════════════════════════════════════


class CaptureRequest(BaseModel):
    """Requête pour l'endpoint /capture."""

    device_id: str = Field(
        ...,
        min_length=1,
        description="Identifiant unique du device",
    )
    input_modality: Literal["text", "voice"] = Field(
        default="text",
        description="Mode d'entrée utilisé par l'utilisateur",
    )
    question: str | None = Field(
        default=None,
        max_length=500,
        description="Question de Ginette (optionnelle selon flux)",
    )
    conversation_id: str | None = Field(
        default=None,
        description="ID conversation pour contexte (flux continu)",
    )
    mock_id: str = Field(
        default="M01",
        description="ID du scénario mock (Protocole P4)",
    )
    image_data: str | None = Field(
        default=None,
        description="Image base64 - IGNORÉE en Alpha (Protocole P4)",
    )


class CaptureResponse(BaseModel):
    """Réponse de l'endpoint /capture."""

    response_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Identifiant unique de la réponse",
    )
    message: str = Field(..., description="Message d'iAngel (texte affiché)")
    spoken_message: str | None = Field(
        default=None,
        description="Message optimisé pour la synthèse vocale (plus court/naturel)",
    )
    step_number: int = Field(default=1, ge=1)
    total_steps: int | None = Field(
        default=None,
        description="Nombre total d'étapes (null si inconnu)",
    )
    awaiting_validation: bool = Field(
        default=True,
        description="Attend confirmation de Ginette avant étape suivante",
    )
    suggested_actions: list[str] = Field(
        default_factory=list,
        description="Actions suggérées",
    )
    confidence: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Score de confiance",
    )
    mock_used: str | None = Field(
        default=None,
        description="Mock utilisé (debug/transparence)",
    )
    emotional_context: EMOTIONAL_CONTEXTS = Field(
        default="neutral",
        description="Ton émotionnel détecté (neutral, reassuring, celebratory, firm, protective)",
    )
    conversation_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="ID conversation pour suivi",
    )
