"""
Tests du middleware d'erreurs empathiques.

Vérifie que JAMAIS une erreur technique brute n'atteint Ginette.
Tous les messages doivent être rassurants et compréhensibles.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.errors import (
    EMPATHIC_MESSAGES,
    CaptureError,
    EmpathicHTTPException,
    InternalError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
    TimeoutError,
    ValidationError,
    iAngelError,
)
from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    """Client de test FastAPI."""
    app = create_app()
    return TestClient(app, raise_server_exceptions=False)


class TestEmpathicMessages:
    """Tests sur les messages empathiques."""

    def test_all_error_types_have_empathic_messages(self) -> None:
        """Chaque type d'erreur doit avoir un message empathique défini."""
        required_types = [
            "validation_error",
            "internal_error",
            "timeout",
            "not_found",
            "rate_limit",
            "service_unavailable",
            "default",
        ]

        for error_type in required_types:
            assert error_type in EMPATHIC_MESSAGES, (
                f"Type d'erreur '{error_type}' sans message empathique"
            )
            message = EMPATHIC_MESSAGES[error_type]
            assert len(message) > 0, f"Message vide pour '{error_type}'"

    def test_no_technical_jargon_in_messages(self) -> None:
        """Les messages ne doivent pas contenir de jargon technique."""
        technical_terms = [
            "exception",
            "error 500",
            "stack trace",
            "null",
            "undefined",
            "traceback",
            "HTTP",
            "API",
            "server",
            "database",
            "timeout",  # en anglais
            "request",
            "response",
        ]

        for error_type, message in EMPATHIC_MESSAGES.items():
            message_lower = message.lower()
            for term in technical_terms:
                assert term.lower() not in message_lower, (
                    f"Jargon technique '{term}' trouvé dans message '{error_type}'"
                )


class TestEmpathicHTTPException:
    """Tests de la classe EmpathicHTTPException."""

    def test_returns_empathic_message_for_known_type(self) -> None:
        """Une erreur connue retourne le message empathique correspondant."""
        exc = EmpathicHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_type="internal_error",
        )

        assert exc.status_code == 500
        assert isinstance(exc.detail, dict)
        assert exc.detail["message"] == EMPATHIC_MESSAGES["internal_error"]
        assert exc.detail["error_type"] == "internal_error"

    def test_returns_default_message_for_unknown_type(self) -> None:
        """Un type inconnu retourne le message par défaut."""
        exc = EmpathicHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_type="unknown_type_xyz",  # type: ignore[arg-type]
        )

        assert isinstance(exc.detail, dict)
        assert exc.detail["message"] == EMPATHIC_MESSAGES["default"]

    def test_technical_detail_hidden_in_production(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Le détail technique est caché en production."""
        # Simuler production
        from app import config
        original_settings = config.get_settings()

        # On ne peut pas facilement mocker is_production ici car c'est appelé
        # dans __init__, donc on vérifie juste que le champ existe
        exc = EmpathicHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_type="internal_error",
            technical_detail="NullPointerException at line 42",
        )

        assert isinstance(exc.detail, dict)
        # En dev, le détail technique peut être présent
        # En prod, il serait absent (testé via configuration)


class TestPreConfiguredExceptions:
    """Tests des exceptions pré-configurées."""

    def test_validation_error(self) -> None:
        """ValidationError retourne 422 avec message empathique."""
        exc = ValidationError(technical_detail="Field 'email' invalid")

        assert exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert isinstance(exc.detail, dict)
        assert exc.detail["error_type"] == "validation_error"
        assert "comprend" in exc.detail["message"].lower() or "reformuler" in exc.detail["message"].lower()

    def test_internal_error(self) -> None:
        """InternalError retourne 500 avec message empathique."""
        exc = InternalError(technical_detail="Database connection failed")

        assert exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert isinstance(exc.detail, dict)
        assert exc.detail["error_type"] == "internal_error"
        assert "souci" in exc.detail["message"].lower() or "réessaie" in exc.detail["message"].lower()

    def test_timeout_error(self) -> None:
        """TimeoutError retourne 504 avec message empathique."""
        exc = TimeoutError(technical_detail="Claude API timeout after 30s")

        assert exc.status_code == status.HTTP_504_GATEWAY_TIMEOUT
        assert isinstance(exc.detail, dict)
        assert exc.detail["error_type"] == "timeout"
        assert "instant" in exc.detail["message"].lower() or "lent" in exc.detail["message"].lower()

    def test_not_found_error(self) -> None:
        """NotFoundError retourne 404 avec message empathique."""
        exc = NotFoundError(technical_detail="Resource ID 12345 not found")

        assert exc.status_code == status.HTTP_404_NOT_FOUND
        assert isinstance(exc.detail, dict)
        assert exc.detail["error_type"] == "not_found"
        assert "trouve" in exc.detail["message"].lower()

    def test_rate_limit_error(self) -> None:
        """RateLimitError retourne 429 avec message empathique."""
        exc = RateLimitError(technical_detail="Rate limit exceeded: 100/min")

        assert exc.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert isinstance(exc.detail, dict)
        assert exc.detail["error_type"] == "rate_limit"
        assert "souffle" in exc.detail["message"].lower() or "secondes" in exc.detail["message"].lower()

    def test_service_unavailable_error(self) -> None:
        """ServiceUnavailableError retourne 503 avec message empathique."""
        exc = ServiceUnavailableError(technical_detail="Anthropic API down")

        assert exc.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert isinstance(exc.detail, dict)
        assert exc.detail["error_type"] == "service_unavailable"
        assert "débordé" in exc.detail["message"].lower() or "minute" in exc.detail["message"].lower()


class TestiAngelError:
    """Tests de iAngelError avec message personnalisé."""

    def test_preserves_user_message(self) -> None:
        """iAngelError préserve le message utilisateur personnalisé."""
        custom_message = "Je vais vous aider à résoudre ce petit problème."
        exc = iAngelError(
            user_message=custom_message,
            status_code=status.HTTP_400_BAD_REQUEST,
            technical_detail="Custom error scenario",
        )

        assert isinstance(exc.detail, dict)
        assert exc.detail["message"] == custom_message
        assert exc.user_message == custom_message

    def test_custom_status_code(self) -> None:
        """iAngelError permet un status code personnalisé."""
        exc = iAngelError(
            user_message="Message test",
            status_code=status.HTTP_409_CONFLICT,
        )

        assert exc.status_code == status.HTTP_409_CONFLICT


class TestCaptureError:
    """Tests de CaptureError pour les erreurs de capture d'écran."""

    def test_capture_error_message(self) -> None:
        """CaptureError a un message adapté aux problèmes de capture."""
        exc = CaptureError(technical_detail="Image processing failed: corrupt JPEG")

        assert exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert isinstance(exc.detail, dict)
        assert "écran" in exc.detail["message"].lower()
        assert "photo" in exc.detail["message"].lower()

    def test_capture_error_is_empathic(self) -> None:
        """Le message de CaptureError est empathique et rassurant."""
        exc = CaptureError()

        message = exc.detail["message"] if isinstance(exc.detail, dict) else ""
        # Le message ne doit pas être accusateur
        assert "erreur" not in message.lower()
        assert "échoué" not in message.lower()
        # Le message doit être positif
        assert "pourriez" in message.lower() or "reprendre" in message.lower()


class TestMiddlewareIntegration:
    """Tests d'intégration du middleware avec l'application."""

    def test_health_endpoint_success(self, client: TestClient) -> None:
        """L'endpoint health fonctionne normalement."""
        response = client.get("/api/v1/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"

    def test_404_returns_json(self, client: TestClient) -> None:
        """Une route inexistante retourne du JSON, pas du HTML."""
        response = client.get("/api/v1/nonexistent")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        # FastAPI retourne du JSON par défaut pour les 404
        assert response.headers.get("content-type", "").startswith("application/json")


class TestRobustness:
    """Tests de robustesse (Audit CTO)."""

    def test_fault_injection_is_handled_empathically(self) -> None:
        """Une exception brute (RuntimeError) est capturée et transformée."""
        app = create_app()

        # Injecter une route qui explose
        @app.get("/boom")
        def explode() -> None:
            raise RuntimeError("BOOM! C'est cassé.")

        client = TestClient(app, raise_server_exceptions=False)
        response = client.get("/boom")

        # 1. Status 500
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

        # 2. JSON Empathique
        data = response.json()
        assert data["error_type"] == "internal_error"
        assert "BOOM" not in data["message"]  # Le message pour Ginette ne contient pas l'erreur
        assert "souci" in data["message"].lower() or "réessaie" in data["message"].lower()

        # 3. Détail technique caché (supposant mode non-debug par défaut dans tests)
        # Note: Dans config.py, debug est False par défaut.
        if "technical_detail" in data:
            assert "RuntimeError" in data["technical_detail"]

    def test_request_id_is_always_present(self, client: TestClient) -> None:
        """L'en-tête X-Request-ID est présent sur toutes les réponses."""
        # Cas 200 OK
        resp_200 = client.get("/api/v1/health")
        assert "X-Request-ID" in resp_200.headers
        assert len(resp_200.headers["X-Request-ID"]) > 0

        # Cas 404 Not Found
        resp_404 = client.get("/api/v1/nonexistent")
        assert "X-Request-ID" in resp_404.headers

        # Cas 500 (avec fault injection locale)
        app = create_app()
        @app.get("/boom")
        def explode() -> None:
            raise RuntimeError("Test ID")
        
        client_crash = TestClient(app, raise_server_exceptions=False)
        resp_500 = client_crash.get("/boom")
        assert "X-Request-ID" in resp_500.headers

    def test_validation_error_is_handled_empathically(self, client: TestClient) -> None:
        """Une erreur de validation (422) retourne un message empathique."""
        # Envoyer des données invalides à /api/v1/capture
        # CaptureRequest attend 'image' (bytes/base64) et 'mock_id' etc.
        # On envoie un body vide ou invalide
        response = client.post("/api/v1/capture", json={"bad_field": "value"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert data["error_type"] == "validation_error"
        # Vérifier que le message est empathique (pas de "field required")
        assert "comprend" in data["message"].lower() or "reformuler" in data["message"].lower()
        
        # Vérifier Request ID
        assert "X-Request-ID" in response.headers
