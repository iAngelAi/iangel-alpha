"""
Tests pour l'endpoint /health.

Vérifie le bon fonctionnement du health check.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests de l'endpoint /health."""

    def test_health_returns_200(self, client: TestClient) -> None:
        """L'endpoint health retourne un code 200."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_health_returns_healthy_status(self, client: TestClient) -> None:
        """L'endpoint health retourne un statut 'healthy'."""
        response = client.get("/api/v1/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_contains_version(self, client: TestClient) -> None:
        """L'endpoint health contient la version de l'application."""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "version" in data
        assert data["version"] == "0.1.0-alpha"

    def test_health_contains_environment(self, client: TestClient) -> None:
        """L'endpoint health contient l'environnement."""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "environment" in data
        assert data["environment"] in ["development", "staging", "production"]

    def test_health_contains_timestamp(self, client: TestClient) -> None:
        """L'endpoint health contient un timestamp ISO 8601."""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "timestamp" in data
        # Vérifie le format ISO 8601 basique
        assert "T" in data["timestamp"]


class TestHealthChecks:
    """Tests des sous-checks de santé."""

    def test_health_contains_checks(self, client: TestClient) -> None:
        """L'endpoint health contient les checks détaillés."""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "checks" in data
        checks = data["checks"]
        assert "database" in checks
        assert "llm_api" in checks

    def test_health_checks_are_skip_in_phase_s0(self, client: TestClient) -> None:
        """En Phase S2, les checks sont actifs."""
        response = client.get("/api/v1/health")
        data = response.json()
        checks = data["checks"]
        # Phase S2: la DB est vérifiée
        assert checks["database"] == "ok"
        assert checks["llm_api"] == "skip"
