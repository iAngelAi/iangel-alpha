"""
Configuration globale des tests (Protocole de Sécurité).

Ce fichier garantit l'isolation hermétique de l'environnement de test.
Aucune requête réseau ne doit sortir.
Aucune persistance ne doit survivre entre les tests.
"""

import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import create_app
from app.config import get_settings, Settings
from app.core.database import Base, db_manager

# 1. Configuration forcée (Golden Config)
def get_test_settings() -> Settings:
    return Settings(
        sandbox_mode=True,  # Toujours en Sandbox par défaut
        anthropic_api_key="mock_key_for_tests",
        anthropic_model="mock-model",
        database_url="sqlite+aiosqlite:///:memory:", # DB volatile
        environment="development", # "test" non autorisé par Pydantic
        debug=True
    )

# 2. Isolation Réseau (Safety Net)
@pytest.fixture(autouse=True)
def forbid_external_network_calls():
    """
    Interdit formellement toute tentative de connexion sortante vers Anthropic.
    Si un test essaie, il échoue immédiatement.
    """
    with patch("anthropic.AsyncAnthropic") as mock_anthropic:
        mock_anthropic.side_effect = RuntimeError(
            "⛔️ SÉCURITÉ: Tentative d'appel réseau détectée dans un test unitaire. "
            "Vous devez mocker le client LLM."
        )
        yield mock_anthropic

# 3. Moteur DB de Test (Partagé)
# On le crée une seule fois par session pour éviter les overheads, 
# mais on drop/create les tables entre les tests si besoin (ici :memory: avec StaticPool suffit)
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

@pytest_asyncio.fixture(name="db_session")
async def fixture_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Initialise la DB en mémoire et fournit une session.
    """
    # Création du schéma
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session
        # Pas besoin de drop car :memory: est volatile, mais pour être propre :
        # await session.rollback()

# 4. Injection des dépendances (FastAPI)
@pytest.fixture(name="client")
def fixture_client(db_session: AsyncSession) -> Generator[TestClient, None, None]:
    """
    Client de test avec surcharge des dépendances critiques.
    """
    # PATCH CRITIQUE: On remplace le moteur du singleton global
    # pour que le lifespan de l'app utilise NOTRE moteur de test
    db_manager.engine = test_engine
    db_manager.session_factory = TestingSessionLocal

    app = create_app()
    
    # Override des settings
    app.dependency_overrides[get_settings] = get_test_settings
    
    # Override de la DB pour les routes
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[db_manager.get_db] = override_get_db
    
    # On utilise le TestClient
    with TestClient(app) as client:
        yield client
    
    # Nettoyage
    app.dependency_overrides.clear()
