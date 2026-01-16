# CLAUDE.md — Directeur iOS & Frontend iAngel

## IDENTITE & MISSION

**Role:** Directeur du Developpement iOS et Frontend
**Experience:** Senior AI Engineer (18 ans)
**Projet:** iAngel - Ange-gardien numerique pour aines quebecois
**Persona Cible:** Ginette, 72 ans, veut faire des virements bancaires sans appeler sa fille

---

## VISION FONDAMENTALE

> "Est-ce que Ginette va se sentir plus protegee avec la journee qu'on a passee aujourd'hui?"

**Philosophie P2 :** RALENTIR au lieu d'accelerer. Une seule instruction a la fois, avec validation avant de passer a l'etape suivante.

---

## ETAT DU PROJET (Janvier 2026)

### Backend (Python/FastAPI) - SOLIDE

| Composant | Fichier | Statut |
|-----------|---------|--------|
| ReasoningEngine S1 | `app/core/reasoning.py` | OK - Structured Output |
| CaptureService | `app/services/capture_service.py` | OK - Orchestrateur |
| StateStore | `app/core/state.py` | OK - Historique TTL |
| ClaudeClient | `app/core/llm/claude.py` | OK - Sonnet 4 |
| MockLoader | `app/sandbox/mock_loader.py` | OK - 7 scenarios |
| Tests | `tests/` | 93 tests, 94.46% coverage |

### iOS (SwiftUI) - EN INTEGRATION

| Fichier | Chemin | Statut | Action |
|---------|--------|--------|--------|
| `CaptureModels.swift` | `ios/Models/` | OK | Integrer dans Xcode |
| `HealthModels.swift` | `ios/Models/` | BUG | Corriger `str` -> `String` |
| `iAngelAPIClient.swift` | `ios/Services/` | OK | Integrer dans Xcode |
| `CaptureViewModel.swift` | `ios/ViewModels/` | BUG | Ajouter extension `isCompleted` |
| `CaptureView.swift` | `ios/Views/` | OK | Integrer dans Xcode |
| Projet Xcode | `ios/iAngel/` | VIDE | Template par defaut |

---

## PHASES DE DEVELOPPEMENT

| Phase | Statut | Description |
|-------|--------|-------------|
| **S0** | TERMINE | Walking Skeleton Backend |
| **S1** | TERMINE | Reasoning Engine + Structured Output |
| **S2** | A FAIRE | Polish iOS, Onboarding, Errors Ginette-proof |
| **S3** | A FAIRE | TestFlight + 10 testeurs Alpha |

---

## PROCHAINES ETAPES PRIORITAIRES

### Immediat (S0-iOS)
1. Corriger typo `HealthModels.swift` ligne 6
2. Ajouter extension `CaptureResponse.isCompleted`
3. Integrer les fichiers Swift dans le projet Xcode
4. Configurer URL Railway (remplacer localhost)
5. Tester communication E2E sur simulateur

### Court terme (S1-iOS)
6. Implementer selection de scenario mock (M01-M07)
7. Ajouter champ question utilisateur
8. Afficher historique de conversation
9. Gerer etats `awaiting_validation`

### Moyen terme (S2)
10. Onboarding 3 ecrans max
11. Integration Siri Shortcuts
12. Messages erreurs empathiques
13. Accessibilite VoiceOver

---

## ARCHITECTURE CIBLE iOS

```
ios/
├── iAngel/                    # Projet Xcode principal
│   ├── App/
│   │   ├── iAngelApp.swift    # Entry point
│   │   └── Configuration.swift # Env detection
│   ├── Models/
│   │   ├── CaptureModels.swift
│   │   └── HealthModels.swift
│   ├── Services/
│   │   └── iAngelAPIClient.swift
│   ├── ViewModels/
│   │   └── CaptureViewModel.swift
│   ├── Views/
│   │   ├── CaptureView.swift
│   │   └── OnboardingView.swift
│   └── Resources/
│       └── Assets.xcassets
```

---

## CONTRATS API (Source de Verite)

### POST /api/v1/capture

**Request:**
```json
{
  "device_id": "string",
  "input_modality": "text" | "voice",
  "question": "string?",
  "conversation_id": "string?",
  "mock_id": "M01",
  "image_data": "base64?"
}
```

**Response:**
```json
{
  "response_id": "uuid",
  "message": "string",
  "spoken_message": "string?",
  "step_number": 1,
  "total_steps": null,
  "awaiting_validation": true,
  "suggested_actions": ["C'est fait", "Je ne trouve pas"],
  "confidence": 0.9,
  "mock_used": "M01?",
  "conversation_id": "uuid"
}
```

### GET /api/v1/health

**Response:**
```json
{
  "status": "healthy" | "unhealthy" | "degraded",
  "version": "0.1.0-alpha",
  "environment": "development",
  "timestamp": "ISO8601",
  "checks": {"database": "ok"},
  "user_message": "Tout va bien!",
  "error_details": null
}
```

---

## SCENARIOS MOCK DISPONIBLES

| ID | Scenario | Description |
|----|----------|-------------|
| M01 | wifi_connection | Ginette veut se connecter au WiFi |
| M02 | suspicious_email | Email frauduleux Desjardins |
| M03 | ios_update | Mise a jour iOS |
| M04 | videotron_bill | Paiement facture (voice-ready) |
| M05 | app_error | Message d'erreur application |
| M06 | password_reset | Reinitialisation mot de passe |
| M07 | photo_sharing | Envoi de photo |

---

## REGLES D'OR (NON-NEGOCIABLES)

### 1. Protocole P2 - Une Etape a la Fois
```
JAMAIS: "1. Ouvrez l'app 2. Tapez sur... 3. Ensuite..."
TOUJOURS: "Regardez l'icone bleue en haut. Vous la voyez?"
```

### 2. Pas de Jargon Technique
```
JAMAIS: "URL", "navigateur", "swipe", "bug", "timeout"
TOUJOURS: "l'adresse en haut", "Internet", "glisser", "petit souci", "connexion lente"
```

### 3. Empathie d'Abord
```
Si Ginette semble stresee → Rassurer AVANT d'instruire
"Je comprends, ca peut sembler complique. On va y aller doucement."
```

### 4. Jamais d'Erreur Technique Brute
```
JAMAIS: "500 Internal Server Error"
TOUJOURS: "Oups, j'ai eu un petit souci. On reessaie?"
```

---

## COMMANDES UTILES

```bash
# Backend
cd /Users/felixlefebvre/.claude-worktrees/iangel-alpha/friendly-swartz
uv run pytest tests/ -v              # Tests (93 tests)
uv run uvicorn app.main:app --reload # Serveur dev
uv run ruff check app/               # Linting
uv run mypy app/                     # Type checking

# iOS
open ios/iAngel/iAngel.xcodeproj     # Ouvrir Xcode
```

---

## NOTES POUR SESSIONS FUTURES

1. **Toujours verifier l'etat des tests** avant de modifier le backend
2. **Le mode SANDBOX_MODE=True** utilise les mocks (pas d'appel Claude)
3. **Les fichiers iOS sont prepares** mais pas encore dans Xcode
4. **Railway deploy** sur push main branch
5. **Anthropic model** = claude-sonnet-4-20250514

---

## CRITERE DE SUCCES ALPHA (PRD)

> "3 utilisateurs reels completent le flux capture → reponse SANS aide externe."

---

*Document de reference pour Claude Opus 4.5 - Mis a jour Janvier 2026*
