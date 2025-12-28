# 🔧 BRIEFING COMPOSANT S0-03
## Endpoint /capture (Skeleton)

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S0-03 |
| **Phase** | S0 — Walking Skeleton |
| **Composant** | Endpoint capture (version minimale) |
| **Priorité** | P0 (Critique) |
| **Dépendances** | S0-02 (/health), S0-04 (Mock Loader) |
| **Durée estimée** | 2-3 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S0-03 — ENDPOINT /capture (SKELETON)
══════════════════════════════════════════════════════════════

Tu vas implémenter l'endpoint /capture du backend iAngel en version SKELETON.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPÉCIFICATION COMPORTEMENTALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF:
Créer un endpoint /capture qui:
1. Accepte une question utilisateur (texte)
2. Accepte un ID de mock (PAS d'image réelle - Protocole P4)
3. Charge l'image mock correspondante
4. Envoie au LLM (Claude) pour analyse
5. Retourne une réponse structurée

⚠️ CRITICAL — PROTOCOLE P4 v1.1:
> En Alpha, le backend NE TRAITE JAMAIS d'images réelles.
> L'image binaire envoyée par le client est IGNORÉE.
> Le système utilise des captures PRÉDÉFINIES (mocks).

COMPORTEMENT ATTENDU:
```
POST /api/v1/capture

Request Body:
{
  "device_id": "device_abc123",
  "question": "C'est tu un virus?",
  "mock_id": "M02",           // ID du scénario mock
  "image_data": "base64..."   // IGNORÉ en Alpha (Protocole P4)
}

Response 200:
{
  "response_id": "resp_uuid",
  "message": "Je vois une fenêtre popup qui...",
  "step_number": 1,
  "total_steps": null,        // Inconnu au début
  "awaiting_validation": true,
  "suggested_actions": ["Dire OK quand prêt"],
  "confidence": 0.85,
  "mock_used": "windows_popup.png"  // Transparent pour debug
}

Response 422 (Validation Error):
{
  "detail": "La question ne peut pas être vide"
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTRAINTES ARCHITECTURALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STACK IMPOSÉE (ADR P3):
- FastAPI router
- Pydantic V2 pour entrées/sorties
- Anthropic SDK pour Claude 3.5 Sonnet
- Typage strict (pas de Any)

FICHIERS À CRÉER/MODIFIER:
```
app/
├── api/v1/endpoints/capture.py  # Router de l'endpoint
├── models/schemas.py            # CaptureRequest, CaptureResponse
├── services/capture_service.py  # Logique métier
├── sandbox/mock_loader.py       # Chargeur de mocks (S0-04)
└── core/llm/claude_client.py    # Client Anthropic
```

SCHÉMAS PYDANTIC (obligatoires):
```python
from pydantic import BaseModel, Field
from typing import Literal
import uuid

class CaptureRequest(BaseModel):
    device_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1, max_length=500)
    mock_id: str = Field(default="M01")  # ID du mock à utiliser
    image_data: str | None = None  # IGNORÉ en Alpha

class CaptureResponse(BaseModel):
    response_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message: str
    step_number: int = 1
    total_steps: int | None = None
    awaiting_validation: bool = True
    suggested_actions: list[str] = []
    confidence: float = Field(ge=0.0, le=1.0)
    mock_used: str | None = None  # Pour debug/transparence
```

ARCHITECTURE SERVICE:
```python
# capture_service.py doit:
# 1. Recevoir la requête
# 2. Charger le mock via mock_loader (S0-04)
# 3. Construire le prompt avec question + image mock
# 4. Appeler Claude via claude_client
# 5. Parser et structurer la réponse
# 6. Retourner CaptureResponse
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES CRITIQUES (À NE JAMAIS OUBLIER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PROTOCOLE P4 — SANDBOX ALPHA (⚠️ LE PLUS IMPORTANT)
   > L'image_data de la requête est COMPLÈTEMENT IGNORÉE.
   > Le mock_loader charge une image prédéfinie selon mock_id.
   > RAISON: Zéro risque légal pour données sensibles en Alpha.

2. UTILISATEUR CIBLE: GINETTE (72 ans)
   > Les messages d'erreur doivent être EMPATHIQUES.
   > PAS: "422 Unprocessable Entity"
   > OUI: "Je n'ai pas bien compris votre question. Pouvez-vous reformuler?"

3. UNE ÉTAPE À LA FOIS
   > Le champ awaiting_validation DOIT être true par défaut.
   > Le message ne doit contenir qu'UNE SEULE instruction.
   > PAS de listes numérotées (1., 2., 3.).

4. RETRY SUR ERREUR LLM
   > Si Claude timeout ou erreur 500, retry 3 fois avec backoff.
   > Après 3 échecs, message empathique (pas d'erreur technique).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROMPT SYSTEM POUR CLAUDE (SKELETON)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour la Phase S0 (skeleton), utilise ce prompt simple:

```
Tu es iAngel, un assistant numérique bienveillant pour les personnes
qui ne sont pas à l'aise avec la technologie.

RÈGLES ABSOLUES:
1. Tu donnes UNE SEULE instruction à la fois, jamais de liste
2. Tu attends que l'utilisateur confirme avant de continuer
3. Tu utilises un langage simple, sans jargon technique
4. Tu es patient et rassurant

L'utilisateur te montre une capture d'écran et te pose une question.
Analyse l'image et réponds de manière rassurante.
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMAT DE RÉPONSE ATTENDU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour CHAQUE fichier:
1. Chemin complet
2. Code complet avec commentaires
3. Explication de 1 ligne du rôle

À LA FIN:
- Commande curl pour tester
- Test pytest minimal
- Exemple de log attendu

══════════════════════════════════════════════════════════════
CONFIRME QUE TU AS CHARGÉ CE BRIEFING EN RÉPONDANT:
"BRIEFING S0-03 CHARGÉ — Prêt à implémenter /capture (Protocole P4 actif)"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] `POST /api/v1/capture` accepte le body JSON
- [ ] image_data est IGNORÉ (log confirme)
- [ ] Mock image chargé depuis /mocks/
- [ ] Claude appelé et réponse reçue
- [ ] Réponse respecte schéma CaptureResponse
- [ ] awaiting_validation = true par défaut
- [ ] Message d'erreur empathique (pas de 500 brut)

---

## 🧪 TEST DE VALIDATION

```bash
# Démarrer le serveur
uvicorn app.main:app --reload

# Tester avec curl
curl -X POST http://localhost:8000/api/v1/capture \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test_device",
    "question": "C est tu un virus?",
    "mock_id": "M02"
  }' | jq

# Attendu: JSON avec message de Claude, awaiting_validation: true
```

---

## 🔗 COMPOSANT SUIVANT

Après validation S0-03, passer à: `S0-04_BRIEF_mock_loader.md`
