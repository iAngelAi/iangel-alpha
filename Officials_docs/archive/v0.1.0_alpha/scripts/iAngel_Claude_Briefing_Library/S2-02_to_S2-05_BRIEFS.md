# 🔧 BRIEFING COMPOSANTS S2-02 à S2-05
## Error Handling & Polish

---

# S2-02 — Error Handling Backend

## 🎯 PROMPT À COPIER

```
══════════════════════════════════════════════════════════════
BRIEFING S2-02 — ERROR HANDLING BACKEND
══════════════════════════════════════════════════════════════

Implémenter la gestion d'erreur EMPATHIQUE du backend.

RÈGLE ABSOLUE: Ginette ne doit JAMAIS voir une erreur technique.

MAPPING ERREURS:
| Erreur Technique | Message Ginette |
|------------------|-----------------|
| 500 Internal | "Je réfléchis plus fort que d'habitude..." |
| Timeout | "Ça prend un peu plus de temps..." |
| Rate Limit | "Un instant, je reprends mon souffle..." |
| DB Error | "J'ai un petit souci, on réessaie?" |

FICHIERS:
```
app/
├── middleware/error_handler.py   # Middleware global
├── exceptions/ginette_errors.py  # Exceptions custom
└── utils/error_messages.py       # Messages empathiques
```

══════════════════════════════════════════════════════════════
CONFIRME: "BRIEFING S2-02 CHARGÉ — Error Handling Backend"
══════════════════════════════════════════════════════════════
```

---

# S2-03 — Error Handling iOS

## 🎯 PROMPT À COPIER

```
══════════════════════════════════════════════════════════════
BRIEFING S2-03 — ERROR HANDLING iOS
══════════════════════════════════════════════════════════════

Implémenter la gestion d'erreur côté iOS.

RÈGLES:
1. Intercepter TOUTES les erreurs réseau
2. Afficher ErrorView avec message empathique
3. Proposer "Réessayer" après chaque erreur
4. JAMAIS de crash visible

FICHIERS:
```
iAngel/Components/
├── ErrorView.swift           # Vue d'erreur empathique
└── RetryableView.swift       # Wrapper avec retry
```

ERRORVIEW DESIGN:
- Illustration douce (pas d'icône erreur rouge)
- Message empathique centré
- Bouton "Réessayer" proéminent
- Option "Annuler" discrète

══════════════════════════════════════════════════════════════
CONFIRME: "BRIEFING S2-03 CHARGÉ — Error Handling iOS"
══════════════════════════════════════════════════════════════
```

---

# S2-04 — Loading States

## 🎯 PROMPT À COPIER

```
══════════════════════════════════════════════════════════════
BRIEFING S2-04 — LOADING STATES
══════════════════════════════════════════════════════════════

Implémenter les états de chargement EMPATHIQUES.

PAS UN SPINNER VIDE. Messages rotatifs:
- "Je réfléchis à votre question..."
- "Je regarde votre écran..."
- "Un instant, je cherche..."
- "J'analyse la situation..."

FICHIERS:
```
iAngel/Components/
├── LoadingView.swift           # Avec messages rotatifs
└── LoadingMessages.swift       # Banque de messages
```

ANIMATION:
- Pulsation douce (pas de rotation rapide)
- Texte qui change toutes les 3 secondes
- Calme et rassurant

══════════════════════════════════════════════════════════════
CONFIRME: "BRIEFING S2-04 CHARGÉ — Loading States"
══════════════════════════════════════════════════════════════
```

---

# S2-05 — Conversation Persistence

## 🎯 PROMPT À COPIER

```
══════════════════════════════════════════════════════════════
BRIEFING S2-05 — CONVERSATION PERSISTENCE
══════════════════════════════════════════════════════════════

Implémenter la persistence des conversations.

BACKEND:
- PostgreSQL tables: conversations, messages
- Endpoint GET /api/v1/conversations/{device_id}
- Rétention 30 jours (conformité P4)

iOS:
- ConversationHistoryView liste les anciennes conversations
- Tap = ouvrir et continuer

FICHIERS BACKEND:
```
app/
├── models/conversation.py
├── repositories/conversation_repo.py
└── api/v1/endpoints/conversations.py
```

FICHIERS iOS:
```
iAngel/Features/History/
├── HistoryView.swift
└── HistoryViewModel.swift
```

══════════════════════════════════════════════════════════════
CONFIRME: "BRIEFING S2-05 CHARGÉ — Conversation Persistence"
══════════════════════════════════════════════════════════════
```

---

## 🎯 GATE S2 — VALIDATION

> **"1 testeur pilote complète le flux SANS poser de question"**

Protocole: Observer silencieusement, noter, ne pas parler.
