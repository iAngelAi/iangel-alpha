"""
Point d'entrée FastAPI iAngel.

Factory pattern avec create_app() pour tests et déploiement.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import get_settings
from app.core.database import Base, db_manager
from app.core.middleware import create_request_id_middleware, setup_error_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Gère le cycle de vie de l'application.

    Startup:
        - Initialisation des connexions (Phase S2)
        - Création des tables (Phase S2 - Alpha)
    """
    settings = get_settings()

    # Startup
    if settings.debug:
        print(f"🚀 iAngel {settings.app_version} démarre en mode {settings.environment}")

    # Phase S2: Initialiser la DB avec les settings actuels
    db_manager.initialize(settings)

    # Phase S2: Créer les tables si elles n'existent pas
    if db_manager.engine:
        async with db_manager.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            if settings.debug:
                print("📁 Base de données initialisée (Tables créées)")

    yield

    # Shutdown
    await db_manager.close()
    if settings.debug:
        print("👋 iAngel s'arrête proprement")


def create_app() -> FastAPI:
    """
    Factory function pour créer l'application FastAPI.

    Returns:
        Application FastAPI configurée.
    """
    settings = get_settings()

    app = FastAPI(
        title="iAngel API",
        description=(
            "API backend pour iAngel, l'ange-gardien numérique "
            "qui accompagne les aînés québécois dans leur quotidien technologique."
        ),
        version=settings.app_version,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan,
    )

    # CORS pour développement iOS
    if settings.environment == "development":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # TODO: Restreindre en production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Gestionnaire d'exceptions empathiques
    setup_error_handlers(app)

    # Middleware Request ID (pour traçabilité)
    app.middleware("http")(create_request_id_middleware())

    # Routeur API avec préfixe /api/v1
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app


# Instance pour uvicorn
app = create_app()
