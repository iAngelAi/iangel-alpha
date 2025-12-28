# 📚 iAngel — Bibliothèque de Scripts de Briefing Claude
## Architecture de Prompts pour Développement Structuré

**Version:** 1.0.0  
**Date:** 2025-12-28  
**Projet:** iAngel MVP Alpha  
**Méthode:** Walking Skeleton + Briefing par Composant

---

## 🎯 PRINCIPE FONDAMENTAL

> **"Un composant = Un briefing = Un comportement uniforme de Claude"**

Cette bibliothèque contient des **scripts de briefing préconfigurés** pour chaque composant du MVP. Quand tu es prêt à implémenter un composant, tu fournis le script correspondant à Claude dans une nouvelle conversation.

### Pourquoi cette approche?

1. **Cohérence** — Claude reçoit les mêmes contraintes à chaque composant
2. **Conformité** — Protocole P4 (captures prédéfinies) intégré à chaque briefing
3. **Qualité Lab PRO** — Standards de typage strict, gestion d'erreur empathique
4. **Traçabilité** — Tu peux auditer quel briefing a produit quel code

---

## 📋 STRUCTURE DES PHASES

```
PHASE S0: WALKING SKELETON (3-4 jours)
├── S0-01: Structure Repo + FastAPI
├── S0-02: Endpoint /health
├── S0-03: Endpoint /capture (skeleton)
├── S0-04: Mock Image Loader (Sandbox P4)
├── S0-05: Projet Xcode SwiftUI
├── S0-06: APIClient iOS
└── S0-07: UI Skeleton (Bouton + TextField + Réponse)

PHASE S1: CORE ENGINE (5-6 jours)
├── S1-01: Reasoning Engine
├── S1-02: LLM Abstraction Layer
├── S1-03: Mock Library (5 scénarios)
├── S1-04: State Machine
└── S1-05: System Prompts calibrés

PHASE S2: POLISH (4-5 jours)
├── S2-01: Onboarding iOS
├── S2-02: Gestion Erreurs Backend
├── S2-03: Gestion Erreurs iOS
├── S2-04: Messages Réconfortants
└── S2-05: Persistance Conversation

PHASE S3: SHIP (2-3 jours)
├── S3-01: TestFlight Configuration
├── S3-02: Sentry Intégration
├── S3-03: UptimeRobot Setup
└── S3-04: Protocole de Test
```

---

## 🚦 GATE DE VALIDATION PAR PHASE

| Phase | Gate | Critère de Passage |
|:-----:|:----:|-------------------|
| **S0** | SKELETON | "Je tape une question sur iPhone → j'obtiens une réponse de Claude" |
| **S1** | CORE | "Les 5 scénarios mocks retournent des réponses une étape à la fois" |
| **S2** | POLISH | "1 testeur pilote complète le flux SANS poser de question" |
| **S3** | SHIP | "3 testeurs Alpha complètent le flux SANS aide externe" |

---

## 📁 FICHIERS DE CETTE BIBLIOTHÈQUE

### Phase S0 — Walking Skeleton
| Fichier | Composant | Priorité |
|---------|-----------|:--------:|
| `S0-01_BRIEF_repo_structure.md` | Structure repo + FastAPI minimal | P0 |
| `S0-02_BRIEF_endpoint_health.md` | Endpoint /health | P0 |
| `S0-03_BRIEF_endpoint_capture.md` | Endpoint /capture skeleton | P0 |
| `S0-04_BRIEF_mock_loader.md` | Sandbox P4 - Mock Image Loader | P0 |
| `S0-05_BRIEF_xcode_project.md` | Projet Xcode SwiftUI | P0 |
| `S0-06_BRIEF_api_client_ios.md` | APIClient iOS | P0 |
| `S0-07_BRIEF_ui_skeleton.md` | UI minimal (Bouton + Text) | P0 |

### Phase S1 — Core Engine
| Fichier | Composant | Priorité |
|---------|-----------|:--------:|
| `S1-01_BRIEF_reasoning_engine.md` | Moteur "Une étape à la fois" | P0 |
| `S1-02_BRIEF_llm_abstraction.md` | Interface multi-provider | P1 |
| `S1-03_BRIEF_mock_library.md` | 5 captures prédéfinies | P0 |
| `S1-04_BRIEF_state_machine.md` | États LIBRE/TECHNIQUE/PAUSE | P0 |
| `S1-05_BRIEF_system_prompts.md` | System prompt calibré | P0 |

### Phase S2 — Polish
| Fichier | Composant | Priorité |
|---------|-----------|:--------:|
| `S2-01_BRIEF_onboarding_ios.md` | 3 écrans max | P0 |
| `S2-02_BRIEF_error_handling_backend.md` | Jamais de 500 visible | P0 |
| `S2-03_BRIEF_error_handling_ios.md` | Messages réconfortants | P0 |
| `S2-04_BRIEF_loading_states.md` | "Je réfléchis..." | P1 |
| `S2-05_BRIEF_conversation_persistence.md` | Historique visible | P1 |

### Phase S3 — Ship
| Fichier | Composant | Priorité |
|---------|-----------|:--------:|
| `S3-01_BRIEF_testflight.md` | Configuration TestFlight | P0 |
| `S3-02_BRIEF_sentry.md` | Monitoring erreurs | P1 |
| `S3-03_BRIEF_uptime_robot.md` | Monitoring disponibilité | P2 |
| `S3-04_BRIEF_test_protocol.md` | Documentation testeurs | P0 |

---

## 🔧 COMMENT UTILISER UN SCRIPT DE BRIEFING

### Étape 1: Ouvrir une nouvelle conversation Claude

### Étape 2: Copier-coller le script correspondant au composant

### Étape 3: Attendre la confirmation "BRIEFING CHARGÉ — PRÊT"

### Étape 4: Demander l'implémentation

Exemple:
```
Toi: [Colle le contenu de S0-01_BRIEF_repo_structure.md]
Claude: "BRIEFING S0-01 CHARGÉ — Prêt à créer la structure du repo"
Toi: "Implémente"
Claude: [Génère le code conforme]
```

---

## ⚠️ RÈGLES CRITIQUES INTÉGRÉES À CHAQUE BRIEFING

### 1. Protocole P4 (CRITIQUE)
> **JAMAIS d'images réelles utilisateur en Alpha**
> Le backend utilise des captures prédéfinies (mocks)

### 2. Philosophie "Une Étape à la Fois"
> **JAMAIS de listes numérotées 1., 2., 3. dans les réponses à Ginette**
> Une seule instruction atomique, puis attente de validation

### 3. Ginette-Proofing
> **JAMAIS d'erreur technique visible** (500, Timeout, JSON Error)
> Messages empathiques uniquement

### 4. Standards Lab PRO
> **Python:** Typage strict (pas de `Any`), Pydantic V2
> **Swift:** MVVM strict, pas de `!` (force unwrap)

---

## 🎯 PROCHAINE ACTION

**Commence par:** `S0-01_BRIEF_repo_structure.md`

**Rappel Roadmap:**
```
JOUR 1 (Backend skeleton)
├── S0-01: Créer repo GitHub + structure ← TU ES ICI
├── S0-02: FastAPI minimal /health
├── S0-03: Déployer sur Railway
└── S0-04: Valider /health retourne 200
```

---

*Bibliothèque de Briefing — Projet iAngel MVP Alpha*
*🔥 POUR GINETTE 🔥*
