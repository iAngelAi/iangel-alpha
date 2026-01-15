# 🔧 BRIEFING COMPOSANT S1-02
## LLM Abstraction Layer

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S1-02 |
| **Phase** | S1 — Core Engine |
| **Composant** | Interface multi-provider LLM |
| **Priorité** | P1 (Important pour évolutivité) |
| **Dépendances** | S1-01 (Reasoning Engine) |
| **Durée estimée** | 2-3 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S1-02 — LLM ABSTRACTION LAYER
══════════════════════════════════════════════════════════════

Tu vas implémenter une COUCHE D'ABSTRACTION pour les LLM.

Objectif: Permettre de changer de provider (Claude → GPT-4 → Gemini)
sans modifier le code métier.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPÉCIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FICHIERS À CRÉER:
```
app/core/llm/
├── __init__.py
├── base.py              # Interface abstraite
├── claude_client.py     # Implémentation Claude
└── mock_client.py       # Pour tests sans API
```

INTERFACE ABSTRAITE:
```python
from abc import ABC, abstractmethod
from pydantic import BaseModel

class LLMMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    image_data: bytes | None = None

class LLMResponse(BaseModel):
    content: str
    model: str
    tokens_used: int
    latency_ms: int

class BaseLLMClient(ABC):
    @abstractmethod
    async def complete(
        self,
        messages: list[LLMMessage],
        system_prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> LLMResponse:
        """Génère une complétion."""
        pass
    
    @abstractmethod
    async def complete_with_image(
        self,
        messages: list[LLMMessage],
        image_data: bytes,
        system_prompt: str
    ) -> LLMResponse:
        """Génère une complétion avec analyse d'image."""
        pass
```

IMPLÉMENTATION CLAUDE:
```python
class ClaudeClient(BaseLLMClient):
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
    
    async def complete_with_image(...):
        # Utilise l'API Vision de Claude
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES CRITIQUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. RETRY AUTOMATIQUE (3 tentatives avec backoff)
2. TIMEOUT 30 secondes (Ginette est patiente)
3. LOG tous les appels (tokens, latence) pour monitoring
4. MockLLMClient pour tests sans API réelle

══════════════════════════════════════════════════════════════
CONFIRME: "BRIEFING S1-02 CHARGÉ — Prêt à implémenter LLM Abstraction"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] Interface BaseLLMClient abstraite
- [ ] ClaudeClient implémenté
- [ ] MockLLMClient pour tests
- [ ] Retry automatique sur erreur
- [ ] Logging tokens/latence

---

## 🔗 COMPOSANT SUIVANT

Après validation: `S1-03_BRIEF_mock_library.md`
