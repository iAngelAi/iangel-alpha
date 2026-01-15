"""
Gestion de la base de données (Phase S2).

Fournit l'engine SQLAlchemy asynchrone et le gestionnaire de sessions.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import Settings


class Base(DeclarativeBase):
    """Classe de base pour les modèles ORM."""
    pass


class AsyncDatabase:
    """Gestionnaire de base de données asynchrone."""

    def __init__(self) -> None:
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None

    def initialize(self, settings: Settings) -> None:
        """Initialise l'engine et la factory avec la configuration fournie."""
        # Idempotence: ne pas réinitialiser si déjà fait avec la même URL
        if self.engine:
            return

        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            future=True,
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Fournisseur de dépendance pour la session de base de données."""
        if not self.session_factory:
            # Fallback automatique si non initialisé (sécurité Ginette)
            from app.config import get_settings
            self.initialize(get_settings())
        
        if not self.session_factory: # Ne devrait plus arriver
            raise RuntimeError("Database not initialized.")

        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self) -> None:
        """Ferme proprement l'engine de base de données."""
        if self.engine:
            await self.engine.dispose()
            # On ne met pas à None ici pour éviter de casser le singleton 
            # pendant la suite des tests. En prod, le processus meurt de toute façon.




# Instance unique du gestionnaire (mais non initialisée par défaut)
db_manager = AsyncDatabase()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Alias pour l'usage dans Depends()."""
    async for session in db_manager.get_db():
        yield session
