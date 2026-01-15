"""
Gestion des erreurs empathiques pour Ginette.

RÈGLE ABSOLUE: Jamais de message technique brut visible par l'utilisateur.
Chaque erreur doit être rassurante et compréhensible pour une personne de 72 ans.
"""

from typing import Any, Literal

from fastapi import HTTPException, status


# Mapping des messages empathiques par type d'erreur
EMPATHIC_MESSAGES: dict[str, str] = {
    "validation_error": (
        "Je n'ai pas bien compris votre demande. "
        "Pourriez-vous reformuler avec d'autres mots?"
    ),
    "internal_error": (
        "Oups, j'ai eu un petit souci technique. "
        "On réessaie ensemble dans quelques instants?"
    ),
    "timeout": (
        "Je réfléchis plus fort que d'habitude... "
        "La connexion semble lente, un instant s'il vous plaît."
    ),
    "not_found": (
        "Je ne trouve pas ce que vous cherchez. "
        "Voulez-vous m'expliquer autrement?"
    ),
    "rate_limit": (
        "Je dois reprendre mon souffle! "
        "Laissez-moi quelques secondes et on continue."
    ),
    "service_unavailable": (
        "Je suis un peu débordé en ce moment. "
        "Pouvez-vous réessayer dans une minute?"
    ),
    "default": (
        "Quelque chose d'inattendu s'est passé. "
        "Ne vous inquiétez pas, on va trouver une solution ensemble."
    ),
}


ErrorType = Literal[
    "validation_error",
    "internal_error",
    "timeout",
    "not_found",
    "rate_limit",
    "service_unavailable",
    "default",
]


class EmpathicHTTPException(HTTPException):
    """
    Exception HTTP avec message empathique pour Ginette.

    Encapsule l'erreur technique tout en présentant un message rassurant.
    """

    def __init__(
        self,
        status_code: int,
        error_type: ErrorType = "default",
        technical_detail: str = "",
    ) -> None:
        """
        Initialise l'exception empathique.

        Args:
            status_code: Code HTTP standard
            error_type: Type d'erreur pour sélection du message
            technical_detail: Détail technique (pour logs, pas visible user)
        """
        empathic_message = EMPATHIC_MESSAGES.get(
            error_type,
            EMPATHIC_MESSAGES["default"],
        )

        # En production, on cache les détails techniques
        detail: dict[str, Any] = {
            "message": empathic_message,
            "error_type": error_type,
        }

        # Détail technique uniquement en dev
        if technical_detail and not self._is_production():
            detail["technical_detail"] = technical_detail

        super().__init__(
            status_code=status_code,
            detail=detail,
        )

    @staticmethod
    def _is_production() -> bool:
        """Vérifie si en production (cache le détail technique)."""
        from app.config import get_settings

        return get_settings().is_production


# === Exceptions pré-configurées pour usage courant ===


class ValidationError(EmpathicHTTPException):
    """Erreur de validation des données."""

    def __init__(self, technical_detail: str = "") -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_type="validation_error",
            technical_detail=technical_detail,
        )


class InternalError(EmpathicHTTPException):
    """Erreur interne serveur."""

    def __init__(self, technical_detail: str = "") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_type="internal_error",
            technical_detail=technical_detail,
        )


class TimeoutError(EmpathicHTTPException):
    """Timeout lors d'un appel externe."""

    def __init__(self, technical_detail: str = "") -> None:
        super().__init__(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            error_type="timeout",
            technical_detail=technical_detail,
        )


class NotFoundError(EmpathicHTTPException):
    """Ressource non trouvée."""

    def __init__(self, technical_detail: str = "") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_type="not_found",
            technical_detail=technical_detail,
        )


class RateLimitError(EmpathicHTTPException):
    """Rate limit atteint."""

    def __init__(self, technical_detail: str = "") -> None:
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_type="rate_limit",
            technical_detail=technical_detail,
        )


class ServiceUnavailableError(EmpathicHTTPException):
    """Service temporairement indisponible."""

    def __init__(self, technical_detail: str = "") -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_type="service_unavailable",
            technical_detail=technical_detail,
        )


class iAngelError(EmpathicHTTPException):
    """
    Exception de base iAngel avec message utilisateur personnalisé.

    Permet de définir un message empathique custom tout en
    conservant les détails techniques pour les logs.
    """

    def __init__(
        self,
        user_message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        technical_detail: str = "",
    ) -> None:
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            user_message: Message empathique à afficher à Ginette
            status_code: Code HTTP (défaut 400)
            technical_detail: Détail technique pour les logs
        """
        self._user_message = user_message
        super().__init__(
            status_code=status_code,
            error_type="default",
            technical_detail=technical_detail,
        )
        # Override le message empathique par défaut avec le message personnalisé
        if isinstance(self.detail, dict):
            self.detail["message"] = user_message

    @property
    def user_message(self) -> str:
        """Retourne le message personnalisé."""
        return self._user_message


class CaptureError(iAngelError):
    """Erreur lors du traitement d'une capture d'écran."""

    def __init__(self, technical_detail: str = "") -> None:
        super().__init__(
            user_message=(
                "Je n'ai pas réussi à bien voir votre écran. "
                "Pourriez-vous reprendre une photo?"
            ),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            technical_detail=technical_detail,
        )
