"""
Endpoint /capture pour traitement des captures d'écran.

TODO Phase S0-03: Implémenter l'endpoint complet avec :
- Réception de la capture (mock ou image)
- Appel Claude API
- Réponse "une étape à la fois"
"""

from fastapi import APIRouter, Depends

from ....models.schemas import CaptureRequest, CaptureResponse
from ....services.capture_service import CaptureService

router = APIRouter()


def get_capture_service() -> CaptureService:
    """
    Fournisseur de dépendance pour CaptureService.
    Instancie le service avec ses dépendances par défaut (Prod).
    """
    return CaptureService()


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
