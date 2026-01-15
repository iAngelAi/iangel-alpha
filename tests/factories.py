"""
Usine de Données de Test (Golden Datasets).

Centralise la création des objets complexes pour garantir la cohérence
des tests face aux évolutions du schéma (S1 -> S2 -> S3).
"""

from typing import List, Optional
from app.core.llm.schemas import PedagogicalDecision
from app.models.schemas import CaptureRequest, CaptureResponse

class TestFactory:
    
    @staticmethod
    def create_decision(
        instruction: str = "Instruction par défaut",
        spoken: str = "Instruction vocale par défaut",
        emotion: str = "neutral",
        completed: bool = False,
        actions: Optional[List[str]] = None,
        thought: str = "Raisonnement par défaut"
    ) -> PedagogicalDecision:
        """
        Crée une décision pédagogique valide (S3 Compliant).
        """
        if actions is None:
            actions = ["Action par défaut"]
            
        return PedagogicalDecision(
            thought_process=thought,
            current_instruction=instruction,
            spoken_instruction=spoken,
            is_completed=completed,
            suggested_actions=actions,
            emotional_context=emotion
        )

    @staticmethod
    def create_request(
        question: str = "Test question",
        mock_id: str = "M01",
        conversation_id: str = "test_conv_id",
        image: Optional[str] = None
    ) -> CaptureRequest:
        """
        Crée une requête client valide.
        """
        return CaptureRequest(
            device_id="test_device",
            input_modality="text",
            question=question,
            conversation_id=conversation_id,
            mock_id=mock_id,
            image_data=image
        )
