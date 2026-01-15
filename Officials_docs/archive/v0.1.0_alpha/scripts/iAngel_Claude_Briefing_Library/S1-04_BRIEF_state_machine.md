# 🔧 BRIEFING COMPOSANT S1-04
## State Machine — États de Conversation

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S1-04 |
| **Phase** | S1 — Core Engine |
| **Composant** | Machine à états de la conversation |
| **Priorité** | P0 (Requis pour flux multi-étapes) |
| **Dépendances** | S1-01 (Reasoning Engine) |
| **Durée estimée** | 2-3 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S1-04 — STATE MACHINE
══════════════════════════════════════════════════════════════

Tu vas implémenter la MACHINE À ÉTATS de conversation iAngel.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ÉTATS DE LA CONVERSATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```
                    ┌──────────────┐
     Nouvelle       │              │
     capture   ────►│    IDLE      │◄────── Fin de tâche
                    │              │
                    └──────┬───────┘
                           │
                    Question reçue
                           │
                           ▼
                    ┌──────────────┐
                    │              │
                    │  ANALYZING   │ ← Claude analyse l'image
                    │              │
                    └──────┬───────┘
                           │
                    Analyse terminée
                           │
                           ▼
                    ┌──────────────┐
          ┌────────│              │
          │        │  STEP_GIVEN  │ ← Instruction donnée
          │        │              │
          │        └──────┬───────┘
          │               │
          │      Validation utilisateur
          │               │
          │               ▼
          │        ┌──────────────┐
          │        │              │
          └───────►│  VALIDATED   │ ← Utilisateur confirme
                   │              │
                   └──────┬───────┘
                          │
                   Étape suivante?
                    /           \
                  OUI           NON
                   │             │
                   ▼             ▼
            ┌──────────┐   ┌──────────┐
            │STEP_GIVEN│   │ COMPLETE │
            └──────────┘   └──────────┘
```

FICHIER À CRÉER:
```
app/core/session.py
```

CODE:
```python
from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class ConversationState(str, Enum):
    IDLE = "idle"
    ANALYZING = "analyzing"
    STEP_GIVEN = "step_given"
    VALIDATED = "validated"
    COMPLETE = "complete"
    ERROR = "error"

class SessionData(BaseModel):
    session_id: str
    device_id: str
    state: ConversationState
    current_step: int
    total_steps: int | None
    mock_id: str | None
    created_at: datetime
    updated_at: datetime
    context: dict  # Stockage libre pour le moteur

class SessionManager:
    def __init__(self):
        self.sessions: dict[str, SessionData] = {}
    
    def create_session(self, device_id: str) -> SessionData:
        """Crée une nouvelle session."""
        ...
    
    def transition(self, session_id: str, new_state: ConversationState) -> SessionData:
        """Change l'état avec validation des transitions."""
        ...
    
    def is_awaiting_validation(self, session_id: str) -> bool:
        """Vérifie si on attend une confirmation utilisateur."""
        ...
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRANSITIONS VALIDES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| De | Vers | Condition |
|----|------|-----------|
| IDLE | ANALYZING | Nouvelle capture reçue |
| ANALYZING | STEP_GIVEN | Claude a répondu |
| ANALYZING | ERROR | Erreur Claude/timeout |
| STEP_GIVEN | VALIDATED | Utilisateur confirme |
| VALIDATED | STEP_GIVEN | Étape suivante |
| VALIDATED | COMPLETE | Tâche terminée |
| ERROR | IDLE | Reset par utilisateur |
| * | IDLE | Nouvelle capture (reset) |

⚠️ CONTRAINTES:
- Transition invalide = raise InvalidTransitionError
- Log chaque transition pour debug
- Session expire après 30 minutes d'inactivité

══════════════════════════════════════════════════════════════
CONFIRME: "BRIEFING S1-04 CHARGÉ — Prêt à implémenter State Machine"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] Enum ConversationState avec 6 états
- [ ] SessionManager gère création/transitions
- [ ] Transitions invalides lèvent exception
- [ ] is_awaiting_validation() fonctionne
- [ ] Session expire après 30 min

---

## 🔗 COMPOSANT SUIVANT

Après validation: `S1-05_BRIEF_system_prompts.md`
