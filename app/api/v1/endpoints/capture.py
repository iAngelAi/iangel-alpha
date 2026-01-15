"""
Endpoint /capture pour traitement des captures d'écran.

TODO Phase S0-03: Implémenter l'endpoint complet avec :
- Réception de la capture (mock ou image)
- Appel Claude API
- Réponse "une étape à la fois"
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings, get_settings
from app.core.database import get_db
from app.core.state import PostgresStateStore
from app.models.schemas import CaptureRequest, CaptureResponse
from app.services.capture_service import CaptureService

router = APIRouter()


def get_capture_service(
    settings: Settings = Depends(get_settings),
    db: AsyncSession = Depends(get_db)
) -> CaptureService:
    """
    Fournisseur de dépendance pour CaptureService.
    Instancie le service avec PostgresStateStore pour la Phase S2.
    """
    state_store = PostgresStateStore(db)
    return CaptureService(settings=settings, state_store=state_store)


@router.post(
    "/capture",
    response_model=CaptureResponse,
    summary="Traiter une capture d'écran",
    description="Analyse une capture et retourne une guidance étape par étape.",
    tags=["Capture"],
)
async def process_capture(
    request: CaptureRequest,
    service: CaptureService = Depends(get_capture_service),
) -> CaptureResponse:
    """
    Traite une capture d'écran et retourne une réponse empathique.

    Délègue la logique métier au CaptureService (Architecture Propre).

    Args:
        request: Données de la capture
        service: Instance de CaptureService injectée

    Returns:
        CaptureResponse avec message et métadonnées
    """
    return await service.process_capture(request)
