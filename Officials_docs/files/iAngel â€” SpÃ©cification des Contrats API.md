# iAngel â€” SpÃ©cification des Contrats API
## Document SPEC-001 : Schemas Pydantic V2

**Version:** 1.0.0  
**Date:** 2025-12-22  
**Auteur:** Session DÃ©veloppement â€” Lead Full Stack  
**Statut:** PrÃªt pour implÃ©mentation  
**Destinataire:** DÃ©veloppeur Backend  

---

## Table des MatiÃ¨res

1\. [Contexte et Objectif](#1-contexte-et-objectif)
2\. [Conventions](#2-conventions)
3\. [Schemas de RequÃªte](#3-schemas-de-requÃªte)
4\. [Schemas de RÃ©ponse](#4-schemas-de-rÃ©ponse)
5\. [Enums et Types PartagÃ©s](#5-enums-et-types-partagÃ©s)
6\. [Schemas Internes](#6-schemas-internes)
7\. [Exemples JSON Complets](#7-exemples-json-complets)
8\. [Validation et Contraintes](#8-validation-et-contraintes)
9\. [TraÃ§abilitÃ©](#9-traÃ§abilitÃ©)

---

## 1. Contexte et Objectif

### 1.1 Rappel Projet

**iAngel** est une compagne conversationnelle pour personnes vulnÃ©rables technologiquement. L'API backend reÃ§oit des captures d'Ã©cran contextuelles et retourne des rÃ©ponses **une Ã©tape Ã  la fois**.

### 1.2 Objectif de ce Document

DÃ©finir **sans ambiguÃ¯tÃ©** les contrats d'entrÃ©e/sortie de l'API REST FastAPI. Ce document est la **source de vÃ©ritÃ©** pour l'implÃ©mentation du fichier `app/models/schemas.py`.

### 1.3 Protocole P4 v1.1 â€” Impact sur les Schemas

> âš ï¸ **CRITIQUE** : En mode Alpha, le champ `image` dans `CaptureRequest` est **reÃ§u mais ignorÃ©**. Le systÃ¨me charge une capture prÃ©dÃ©finie (mock) Ã  la place. Les schemas restent identiques pour prÃ©server la compatibilitÃ© future.

---

## 2. Conventions

### 2.1 Conventions de Nommage

| Ã‰lÃ©ment | Convention | Exemple |
|---------|------------|---------|
| Schemas | PascalCase | `CaptureRequest` |
| Champs | snake_case | `conversation_id` |
| Enums | SCREAMING_SNAKE_CASE | `CONVERSATION_LIBRE` |

### 2.2 Types de Base

| Type Logique | Type Python | Import |
|--------------|-------------|--------|
| UUID | `uuid.UUID` | `import uuid` |
| DateTime | `datetime.datetime` | `from datetime import datetime` |
| Optional | `T \| None` | Python 3.11+ natif |

### 2.3 Validation Pydantic V2

Tous les schemas utilisent `pydantic.BaseModel` avec :
- `model_config = ConfigDict(strict=True)` pour typage strict
- Validators personnalisÃ©s via `@field_validator`

---

## 3. Schemas de RequÃªte

### 3.1 CaptureRequest

**Endpoint:** `POST /capture`  
**Description:** Envoi d'une capture d'Ã©cran avec question contextuelle.

| Champ | Type | Requis | Contraintes | Description |
|-------|------|:------:|-------------|-------------|
| `device_id` | `str` | âœ… | Format UUID valide | Identifiant unique appareil iOS |
| `image` | `str` | âœ… | Base64 valide, max 10MB dÃ©codÃ© | Capture PNG encodÃ©e base64 |
| `question` | `str` | âœ… | 1-500 caractÃ¨res, non vide aprÃ¨s strip | Question de l'utilisateur |
| `conversation_id` | `UUID \| None` | âŒ | UUID v4 si prÃ©sent | Continuation conversation existante |

**Exemple JSON:**
```json
{
  "device_id": "A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
  "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
  "question": "C'est-tu correct ce message-lÃ ?",
  "conversation_id": null
}
```

---

### 3.2 ConverseRequest

**Endpoint:** `POST /converse`  
**Description:** Message texte simple sans image (continuation).

| Champ | Type | Requis | Contraintes | Description |
|-------|------|:------:|-------------|-------------|
| `device_id` | `str` | âœ… | Format UUID valide | Identifiant appareil |
| `message` | `str` | âœ… | 1-1000 caractÃ¨res | Texte utilisateur |
| `conversation_id` | `UUID` | âœ… | Doit exister en DB | Conversation existante |

**Exemple JSON:**
```json
{
  "device_id": "A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
  "message": "OK c'est fait!",
  "conversation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

---

### 3.3 OnboardingCompleteRequest

**Endpoint:** `POST /onboarding/complete`  
**Description:** Marquer l'onboarding comme terminÃ©.

| Champ | Type | Requis | Contraintes | Description |
|-------|------|:------:|-------------|-------------|
| `device_id` | `str` | âœ… | Format UUID valide | Identifiant appareil |
| `user_name` | `str` | âœ… | 1-50 caractÃ¨res, alphabÃ©tique + espaces | PrÃ©nom donnÃ© par l'utilisateur |

**Exemple JSON:**
```json
{
  "device_id": "A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
  "user_name": "Ginette"
}
```

---

## 4. Schemas de RÃ©ponse

### 4.1 CaptureResponse

**Endpoint:** `POST /capture` (rÃ©ponse)  
**Description:** RÃ©ponse structurÃ©e avec guidage une Ã©tape Ã  la fois.

| Champ | Type | Description |
|-------|------|-------------|
| `conversation_id` | `UUID` | ID conversation (nouveau ou existant) |
| `message` | `MessagePayload` | Contenu de la rÃ©ponse iAngel |
| `session_mode` | `SessionMode` | Mode actif de la session |

**Exemple JSON:**
```json
{
  "conversation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "message": {
    "content": "Je vois une demande de mise Ã  jour iOS. C'est correct, c'est Apple qui vous l'envoie. Avant de continuer, dites-moi: est-ce que votre tÃ©lÃ©phone est branchÃ© sur le chargeur?",
    "step_number": 1,
    "total_steps": null,
    "awaiting_validation": true
  },
  "session_mode": "ASSISTANCE_TECHNIQUE"
}
```

---

### 4.2 ConverseResponse

**Endpoint:** `POST /converse` (rÃ©ponse)  
**Description:** Identique Ã  CaptureResponse (mÃªme structure).

| Champ | Type | Description |
|-------|------|-------------|
| `conversation_id` | `UUID` | ID conversation |
| `message` | `MessagePayload` | Contenu de la rÃ©ponse |
| `session_mode` | `SessionMode` | Mode actif |

---

### 4.3 HealthResponse

**Endpoint:** `GET /health` (rÃ©ponse)  
**Description:** Ã‰tat de santÃ© de l'API.

| Champ | Type | Description |
|-------|------|-------------|
| `status` | `str` | Toujours `"healthy"` si l'API rÃ©pond |
| `version` | `str` | Version sÃ©mantique (ex: `"0.1.0-alpha"`) |
| `sandbox_mode` | `bool` | `true` en Alpha (captures prÃ©dÃ©finies actives) |
| `timestamp` | `datetime` | Heure serveur UTC |

**Exemple JSON:**
```json
{
  "status": "healthy",
  "version": "0.1.0-alpha",
  "sandbox_mode": true,
  "timestamp": "2025-12-22T14:30:00Z"
}
```

---

### 4.4 OnboardingStateResponse

**Endpoint:** `GET /onboarding/state?device_id=...` (rÃ©ponse)  
**Description:** Ã‰tat d'avancement de l'onboarding utilisateur.

| Champ | Type | Description |
|-------|------|-------------|
| `user_id` | `UUID` | ID utilisateur en base |
| `completed` | `bool` | Onboarding terminÃ©? |
| `current_step` | `str \| None` | Code Ã©tape courante si en cours |
| `user_name` | `str \| None` | PrÃ©nom si dÃ©jÃ  fourni |

**Valeurs possibles `current_step`:**

| Code | Description |
|------|-------------|
| `WELCOME` | Ã‰cran de bienvenue |
| `NAME_PROMPT` | Demande du prÃ©nom |
| `TUTORIAL_CAPTURE` | Tutoriel bouton capture |
| `FIRST_TRY` | Premier essai guidÃ© |
| `null` | TerminÃ© ou non commencÃ© |

**Exemple JSON:**
```json
{
  "user_id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
  "completed": false,
  "current_step": "NAME_PROMPT",
  "user_name": null
}
```

---

### 4.5 ErrorResponse

**Description:** RÃ©ponse d'erreur humanisÃ©e (jamais d'erreur technique brute).

| Champ | Type | Description |
|-------|------|-------------|
| `error_code` | `str` | Code machine (pour logs) |
| `message` | `str` | Message humain rassurant |
| `retry_suggested` | `bool` | SuggÃ©rer Ã  l'utilisateur de rÃ©essayer? |

**Codes d'erreur dÃ©finis:**

| Code | HTTP | Message Humain |
|------|------|----------------|
| `INVALID_REQUEST` | 400 | "Oups, quelque chose n'a pas fonctionnÃ©. Pouvez-vous rÃ©essayer?" |
| `CONVERSATION_NOT_FOUND` | 404 | "Je ne retrouve plus notre conversation. On recommence?" |
| `LLM_TIMEOUT` | 504 | "Je rÃ©flÃ©chis plus fort que d'habitude... Donnez-moi un petit moment." |
| `LLM_ERROR` | 502 | "J'ai un petit problÃ¨me de mon cÃ´tÃ©. RÃ©essayez dans quelques secondes?" |
| `INTERNAL_ERROR` | 500 | "Quelque chose s'est passÃ© de mon cÃ´tÃ©. RÃ©essayez?" |

**Exemple JSON:**
```json
{
  "error_code": "LLM_TIMEOUT",
  "message": "Je rÃ©flÃ©chis plus fort que d'habitude... Donnez-moi un petit moment.",
  "retry_suggested": true
}
```

---

## 5. Enums et Types PartagÃ©s

### 5.1 SessionMode

**Source:** PRD Section 5.1

| Valeur | Description | Comportement |
|--------|-------------|--------------|
| `CONVERSATION_LIBRE` | Mode par dÃ©faut | iAngel jase, rÃ©pond Ã  tout |
| `ASSISTANCE_TECHNIQUE` | TÃ¢che en cours | Mode "une Ã©tape Ã  la fois" actif |
| `ASSISTANCE_EN_PAUSE` | Utilisateur a dÃ©rivÃ© | TÃ¢che sauvegardÃ©e, conversation libre |

**ImplÃ©mentation Python:**
```python
from enum import Enum

class SessionMode(str, Enum):
    CONVERSATION_LIBRE = "CONVERSATION_LIBRE"
    ASSISTANCE_TECHNIQUE = "ASSISTANCE_TECHNIQUE"
    ASSISTANCE_EN_PAUSE = "ASSISTANCE_EN_PAUSE"
```

---

### 5.2 MessagePayload

**Description:** Structure imbriquÃ©e pour les rÃ©ponses iAngel.

| Champ | Type | Description |
|-------|------|-------------|
| `content` | `str` | Texte de la rÃ©ponse (1-2000 car.) |
| `step_number` | `int \| None` | Ã‰tape courante (null si conversation libre) |
| `total_steps` | `int \| None` | Total estimÃ© (null si inconnu ou conversation libre) |
| `awaiting_validation` | `bool` | Attendre confirmation utilisateur avant prochaine Ã©tape |

**RÃ¨gle critique (PRD Epic 2):**
> Quand `session_mode == ASSISTANCE_TECHNIQUE`, le champ `awaiting_validation` doit Ãªtre `true` aprÃ¨s chaque Ã©tape. Le systÃ¨me NE DOIT PAS avancer sans signal explicite de l'utilisateur.

---

## 6. Schemas Internes

### 6.1 SandboxScenario

**Usage:** Interne uniquement (non exposÃ© via API)  
**Description:** Configuration des captures prÃ©dÃ©finies (P4 v1.1)

| Champ | Type | Description |
|-------|------|-------------|
| `scenario_id` | `str` | Identifiant unique du scÃ©nario |
| `trigger_keywords` | `list[str]` | Mots-clÃ©s dÃ©clencheurs dans la question |
| `mock_image_path` | `str` | Chemin vers l'image mock |
| `expected_context` | `str` | Description pour le prompt LLM |

**ScÃ©narios Alpha dÃ©finis:**

| ID | Keywords | Image Mock | Contexte |
|----|----------|------------|----------|
| `FACTURE_TELECOM` | "facture", "vidÃ©otron", "bell", "telus" | `facture_videotron.png` | Facture tÃ©lÃ©com quÃ©bÃ©coise |
| `ERREUR_WINDOWS` | "erreur", "windows", "bleu", "problÃ¨me" | `erreur_windows.png` | Ã‰cran d'erreur Windows |
| `MAJ_IOS` | "mise Ã  jour", "ios", "iphone", "update" | `mise_a_jour_ios.png` | Notification MAJ iOS |
| `COURRIEL_SUSPECT` | "courriel", "email", "louche", "bizarre" | `courriel_suspect.png` | Email potentiellement frauduleux |
| `DEFAULT` | (aucun match) | `ecran_generique.png` | Ã‰cran gÃ©nÃ©rique pour tests |

---

## 7. Exemples JSON Complets

### 7.1 Flux Complet â€” Nouvelle Capture

**RequÃªte:**
```json
POST /capture
Content-Type: application/json
X-API-Key: <secret>
X-Device-ID: A1B2C3D4-E5F6-7890-ABCD-EF1234567890

{
  "device_id": "A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
  "image": "<base64_trÃ¨s_long>",
  "question": "J'ai reÃ§u Ã§a, c'est-tu correct?",
  "conversation_id": null
}
```

**RÃ©ponse (201 Created):**
```json
{
  "conversation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "message": {
    "content": "Je vois ce que vous avez reÃ§u. Laissez-moi regarder Ã§a attentivement.\n\nPremiÃ¨re chose: est-ce que vous connaissez l'expÃ©diteur de ce message?",
    "step_number": 1,
    "total_steps": null,
    "awaiting_validation": true
  },
  "session_mode": "ASSISTANCE_TECHNIQUE"
}
```

---

### 7.2 Flux Complet â€” Continuation

**RequÃªte:**
```json
POST /converse
Content-Type: application/json
X-API-Key: <secret>

{
  "device_id": "A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
  "message": "Non je connais pas Ã§a",
  "conversation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

**RÃ©ponse (200 OK):**
```json
{
  "conversation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "message": {
    "content": "Parfait, vous faites bien de vous mÃ©fier. Dans ce cas-lÃ , on va faire une chose simple: ne cliquez sur rien dans ce message pour l'instant.\n\nDites-moi quand c'est fait, et on continue ensemble.",
    "step_number": 2,
    "total_steps": null,
    "awaiting_validation": true
  },
  "session_mode": "ASSISTANCE_TECHNIQUE"
}
```

---

### 7.3 Flux â€” Utilisateur DÃ©rive

**RequÃªte:**
```json
POST /converse

{
  "device_id": "A1B2C3D4-E5F6-7890-ABCD-EF1234567890",
  "message": "Ah oui, Ã§a me fait penser, ma petite-fille vient souper dimanche!",
  "conversation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

**RÃ©ponse (200 OK):**
```json
{
  "conversation_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "message": {
    "content": "Oh c'est donc bien le fun! Un souper en famille, y'a rien de mieux. Vous allez cuisiner quelque chose de spÃ©cial?\n\n(Je garde en note notre affaire du message louche, on pourra y revenir quand vous voudrez.)",
    "step_number": 2,
    "total_steps": null,
    "awaiting_validation": false
  },
  "session_mode": "ASSISTANCE_EN_PAUSE"
}
```

---

## 8. Validation et Contraintes

### 8.1 Validators PersonnalisÃ©s

| Champ | Validation | Message Erreur |
|-------|------------|----------------|
| `device_id` | Regex UUID v4 | "L'identifiant d'appareil n'est pas valide" |
| `image` | Base64 dÃ©codable + taille < 10MB | "L'image est trop volumineuse ou corrompue" |
| `question` | Strip + len >= 1 | "La question ne peut pas Ãªtre vide" |
| `user_name` | AlphabÃ©tique + espaces, 1-50 car. | "Le prÃ©nom contient des caractÃ¨res non permis" |

### 8.2 Contraintes de SÃ©curitÃ©

| RÃ¨gle | ImplÃ©mentation |
|-------|----------------|
| Rate limiting | 10 req/min par device_id |
| Taille max body | 15 MB (pour images) |
| Timeout requÃªte | 30 secondes |
| Auth | Header `X-API-Key` obligatoire |

---

## 9. TraÃ§abilitÃ©

### 9.1 Sources de VÃ©ritÃ©

| Section | Document Source | Localisation |
|---------|-----------------|--------------|
| Endpoints | Brief Technique P3 | Section 4.1 |
| Payload /capture | Brief Technique P3 | Section 4.2 |
| RÃ©ponse standard | Brief Technique P3 | Section 4.3 |
| SessionMode | PRD MVP Alpha | Section 5.1 |
| ErrorResponse | PRD MVP Alpha | Section 9 (Edge Cases) |
| SandboxScenario | Rapport ConformitÃ© P4 v1.1 | Section 3 |

### 9.2 Historique des Versions

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2025-12-22 | CrÃ©ation initiale |

---

## Signatures

| RÃ´le | Nom | Date | Validation |
|------|-----|------|------------|
| Lead Full Stack | Session Dev Claude | 2025-12-22 | âœ… |
| Architecte Solutions | Session P3 | 2025-12-22 | â¬œ |
| Fondateur | Fil | ____-__-__ | â¬œ |

---

*Document gÃ©nÃ©rÃ© lors de la session DÃ©veloppement â€” 22 dÃ©cembre 2025*

**ðŸ”¥ LE FOYER RESTE ALLUMÃ‰ â€” POUR GINETTE ðŸ”¥**