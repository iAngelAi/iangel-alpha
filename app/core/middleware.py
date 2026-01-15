"""
Middleware de gestion des erreurs Ginette-proof.

Garantit que JAMAIS une erreur technique brute n'atteint l'utilisateur.
Toutes les exceptions non gérées sont transformées en messages empathiques.
"""

import traceback
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

from app.core.errors import EMPATHIC_MESSAGES


async def empathic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handler global pour toutes les exceptions non gérées.

    Transforme les erreurs techniques en messages empathiques pour Ginette.

    Args:
        request: Requête FastAPI
        exc: Exception levée

    Returns:
        JSONResponse avec message empathique
    """
    from app.config import get_settings

    settings = get_settings()

    # Log l'erreur technique pour debugging
    error_trace = traceback.format_exc()
    print(f"[iAngel ERROR] {request.method} {request.url.path}")
    print(f"[iAngel ERROR] {type(exc).__name__}: {exc}")
    if settings.is_debug:
        print(f"[iAngel ERROR] Traceback:\n{error_trace}")

    # Construire la réponse empathique
    response_content: dict[str, str | None] = {
        "message": EMPATHIC_MESSAGES["internal_error"],
        "error_type": "internal_error",
    }

    # Ajouter détails techniques seulement en dev
    if settings.is_debug:
        response_content["technical_detail"] = f"{type(exc).__name__}: {exc}"

    response = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_content,
    )

    # Ajouter Request ID si disponible
    if hasattr(request.state, "request_id"):
        response.headers["X-Request-ID"] = request.state.request_id

    return response


async def validation_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handler pour les erreurs de validation Pydantic.

    Args:
        request: Requête FastAPI
        exc: Exception de validation

    Returns:
        JSONResponse avec message empathique
    """
    from app.config import get_settings

    settings = get_settings()

    response_content: dict[str, str | None] = {
        "message": EMPATHIC_MESSAGES["validation_error"],
        "error_type": "validation_error",
    }

    if settings.is_debug:
        response_content["technical_detail"] = str(exc)

    response = JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_content,
    )

    # Ajouter Request ID si disponible
    if hasattr(request.state, "request_id"):
        response.headers["X-Request-ID"] = request.state.request_id

    return response


def setup_error_handlers(app: FastAPI) -> None:
    """
    Configure tous les handlers d'erreurs empathiques sur l'app FastAPI.

    Args:
        app: Instance FastAPI à configurer
    """
    from fastapi.exceptions import RequestValidationError
    from pydantic import ValidationError

    # Handler pour exceptions non gérées
    app.add_exception_handler(Exception, empathic_exception_handler)

    # Handler pour erreurs de validation
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)


def create_request_id_middleware() -> Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]:
    """
    Crée un middleware qui ajoute un request ID unique.

    Utile pour traçabilité des requêtes dans les logs.

    Returns:
        Middleware callable
    """
    import uuid

    async def request_id_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response

    return request_id_middleware
