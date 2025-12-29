"""
Service de traitement des captures d'écran.

Orchestre le flux complet:
1. Gestion de l'état (StateStore)
2. Analyse d'image (LLM ou Mock)
3. Moteur de raisonnement (ReasoningEngine)
"""

from ..models.schemas import CaptureRequest, CaptureResponse
from ..config import get_settings
from ..core.state import InMemoryStateStore, ConversationState, ReasoningEngine, BaseStateStore
from ..core.llm.claude import ClaudeClient
from ..core.llm.base import LLMProvider
from ..core.llm.prompts import SYSTEM_PROMPT_S1
from ..sandbox.mock_loader import MockLoader
from pathlib import Path

class CaptureService:
    """
    Service de traitement des captures d'écran.
    """

    def __init__(
        self, 
        state_store: BaseStateStore | None = None,
        llm_client: LLMProvider | None = None
    ) -> None:
        self.settings = get_settings()
        
        # Injection ou valeurs par défaut
        self.state_store = state_store or InMemoryStateStore()
        # Note: Pour S1, on a besoin du vrai ClaudeClient (avec generate_decision)
        # Si on passe un MockLLMProvider générique, ça plantera sauf s'il a generate_decision.
        # Pour l'instant, on suppose que l'interface est respectée (Duck Typing).
        self.llm_client = llm_client or ClaudeClient()
        self.mock_loader = MockLoader(self.settings.mocks_dir)

    async def process_capture(self, request: CaptureRequest) -> CaptureResponse:
        """
        Traite une capture et génère une réponse empathique.
        """
        # 1. Gatekeeper P4 (Sandbox)
        if self.settings.sandbox_mode:
            mock = await self.mock_loader.load_for_scenario(request.mock_id)
            if not mock:
                return self._create_fallback_response("Désolé, je ne trouve pas ce scénario de test.")
            
            return CaptureResponse(
                message=mock.expected_response,
                spoken_message=mock.spoken_response or mock.expected_response,
                step_number=1,
                mock_used=mock.mock_id,
                confidence=1.0,
                conversation_id=request.conversation_id or "sandbox_conv"
            )

        # 2. Gestion de l'état (State Management)
        conversation_id = request.conversation_id or "new_conv"
        state = await self.state_store.get_state(conversation_id)
        
        if not state:
            engine = ReasoningEngine()
            state = ConversationState(conversation_id=conversation_id, engine=engine)
        
        engine = state.engine

        # 3. Analyse (LLM S1 - Structured Output)
        user_msg = request.question or "Que dois-je faire ?"
        
        # Pour supporter l'injection de dépendance (MockLLMProvider n'a pas generate_decision),
        # on fait un check runtime. En prod, c'est ClaudeClient.
        if hasattr(self.llm_client, "generate_decision"):
            decision = await self.llm_client.generate_decision( # type: ignore
                system_prompt=SYSTEM_PROMPT_S1,
                user_message=user_msg,
                image_data=request.image_data
            )
            # 4. Moteur de Raisonnement (P2 S1)
            instruction = engine.process_decision(decision)
            spoken = decision.spoken_instruction
            confidence = 0.9 # Claude est confiant
        else:
            # Fallback S0 (Texte simple)
            llm_response = await self.llm_client.generate(
                system_prompt="Tu es iAngel.",
                user_message=user_msg,
                image_data=request.image_data
            )
            instruction = engine.analyze(llm_response.content)
            spoken = instruction
            confidence = 0.5

        # 5. Sauvegarde
        await self.state_store.save_state(conversation_id, state)

        # 6. Réponse
        return CaptureResponse(
            message=instruction,
            spoken_message=spoken,
            step_number=len(engine.steps_completed) + 1,
            conversation_id=conversation_id,
            confidence=confidence,
            awaiting_validation=True
        )

    def _create_fallback_response(self, message: str) -> CaptureResponse:
        # Fallback minimaliste conforme au schéma
        return CaptureResponse(
            message=message,
            spoken_message=message,
            step_number=1,
            confidence=0.0
        )
