"""
Configuration pytest pour iAngel.

Fixtures partagées entre tous les tests.
"""

from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.main import create_app


@pytest.fixture(scope="session")
def app():
    """Crée une instance de l'application pour les tests."""
    return create_app()


@pytest.fixture(scope="session")
def client(app):
    """Client de test synchrone."""
    return TestClient(app)


@pytest.fixture
async def async_client(app) -> AsyncGenerator[AsyncClient, None]:
    """Client de test asynchrone."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
