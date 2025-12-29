"""
Client Anthropic (Claude) pour iAngel.

Implémente l'interface LLMProvider.
Gère l'authentification et les appels API vers Claude 3.5 Sonnet.
"""

import anthropic
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential

from ...config import get_settings
from .base import LLMProvider, LLMResponse
from ..errors import TimeoutError, ServiceUnavailableError, RateLimitError
from .schemas import PedagogicalDecision

class ClaudeClient(LLMProvider):
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.anthropic_api_key and not settings.sandbox_mode:
            print("⚠️ ATTENTION: Clé API Anthropic manquante!")
        
        self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        self.model = settings.anthropic_model

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def generate_decision(
        self,
        system_prompt: str,
        user_message: str,
        image_data: str | None = None,
    ) -> PedagogicalDecision:
        """
        Génère une décision structurée via Tool Use.
        C'est la méthode S1 privilégiée.
        """
        tool_definition = {
            "name": "emit_decision",
            "description": "Émet la décision pédagogique finale pour guider l'utilisateur.",
            "input_schema": PedagogicalDecision.model_json_schema()
        }

        messages = []
        if image_data:
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": user_message}
                ],
            })
        else:
            messages.append({"role": "user", "content": user_message})

        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=messages, # type: ignore
                tools=[tool_definition],
                tool_choice={"type": "tool", "name": "emit_decision"} # Force l'outil
            )
            
            # Extraction du Tool Use
            for block in response.content:
                if block.type == "tool_use" and block.name == "emit_decision":
                    return PedagogicalDecision(**block.input)
            
            raise ValueError("Claude n'a pas utilisé l'outil de décision.")

        except Exception as e:
            # En S1, on veut mapper les erreurs proprement
            if isinstance(e, anthropic.APIConnectionError):
                raise ServiceUnavailableError(f"Claude injoignable: {e}")
            raise e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def generate(
        self,
        system_prompt: str,
        user_message: str,
        image_data: str | None = None,
        *,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        """
        Appelle Claude avec retry automatique.
        Supporte le texte et l'image (Vision).
        """
        messages = []
        
        if image_data:
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg", # TODO: Détecter le type réel
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": user_message
                    }
                ],
            })
        else:
            messages.append({"role": "user", "content": user_message})

        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=messages, # type: ignore
            )
            
            # Extraction propre du texte
            content_text = ""
            for block in response.content:
                if block.type == "text":
                    content_text += block.text

            return LLMResponse(
                content=content_text,
                model=response.model,
                tokens_used=response.usage.output_tokens
            )

        except anthropic.APIConnectionError as e:
            raise ServiceUnavailableError(f"Claude injoignable: {e}")
        except anthropic.RateLimitError as e:
            raise RateLimitError(f"Quota Claude dépassé: {e}")
        except anthropic.APIStatusError as e:
            if e.status_code == 529: # Overloaded
                raise ServiceUnavailableError("Claude est surchargé")
            raise Exception(f"Erreur Claude {e.status_code}: {e.message}")

