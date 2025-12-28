# 🧪 iAngel MVP Alpha — Roadmap Walking Skeleton
## Approche Laboratoire Professionnel

**Version:** 1.0  
**Date:** 2025-12-28  
**Projet:** iAngel MVP Alpha  
**Stack:** FastAPI (Python) + SwiftUI (iOS) + Railway + PostgreSQL + Claude 3.5 Sonnet

---

## 📋 TABLE DES MATIÈRES

1. [Principe Fondamental](#principe-fondamental)
2. [Vue d'Ensemble des Phases](#vue-densemble-des-phases)
3. [Phase S0 — Walking Skeleton](#phase-s0--walking-skeleton)
4. [Phase S1 — Core Engine](#phase-s1--core-engine)
5. [Phase S2 — Polish](#phase-s2--polish)
6. [Phase S3 — Ship](#phase-s3--ship)
7. [Timeline Visuelle](#timeline-visuelle)
8. [Documents de Référence](#documents-de-référence)

---

## 🎯 PRINCIPE FONDAMENTAL

> **"Walking Skeleton First"** — Construire un squelette fonctionnel end-to-end AVANT d'ajouter de la chair.

### Pourquoi cette approche?

Un laboratoire professionnel ne construit **jamais**:
- ❌ Backend complet → puis iOS complet → puis intégration

Un laboratoire professionnel construit **toujours**:
- ✅ Une tranche verticale mince qui traverse toute la stack → puis élargit

### Avantages
- Détection précoce des problèmes d'intégration
- Feedback loop court
- Démonstration rapide de valeur
- Réduction du risque technique

---

## 📊 VUE D'ENSEMBLE DES PHASES

| Phase | Nom | Durée | Objectif | Gate de Validation |
|:-----:|-----|:-----:|----------|:------------------:|
| **S0** | Skeleton | 3-4 jours | Un flux end-to-end qui marche | Capture → Réponse visible sur iPhone |
| **S1** | Core | 5-6 jours | Moteur "Une étape à la fois" | 5 scénarios mocks passent |
| **S2** | Polish | 4-5 jours | UX Ginette-proof | 1 testeur pilote complète sans question |
| **S3** | Ship | 2-3 jours | TestFlight + Monitoring | 3 testeurs Alpha sans aide |

**Total estimé:** ~15-18 jours (vs 4.5 semaines estimées = marge de sécurité)

---

## 🔬 PHASE S0 — WALKING SKELETON

### Durée: 3-4 jours

### Objectif
> **Un seul flux qui traverse TOUTE la stack, même avec du "duct tape"**

### Architecture Skeleton

```
┌─────────────────────────────────────────────────────────────────┐
│                    SKELETON MVP                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   iOS (SwiftUI)              Backend (FastAPI)      Claude API   │
│   ┌──────────────┐          ┌──────────────┐      ┌──────────┐  │
│   │ 1 bouton     │ ──POST── │ /capture     │ ───► │ Prompt   │  │
│   │ 1 champ text │ ◄─JSON── │ hardcodé     │ ◄─── │ simple   │  │
│   │ 1 réponse    │          │ mock image   │      │          │  │
│   └──────────────┘          └──────────────┘      └──────────┘  │
│                                    │                             │
│                             ┌──────▼──────┐                      │
│                             │ PostgreSQL  │                      │
│                             │ 2 tables    │                      │
│                             └─────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

### Livrables S0

| # | Livrable | Critère de succès |
|---|----------|-------------------|
| 1 | **Repo GitHub** créé | `iangel-alpha` existe dans org iAngelAi |
| 2 | **Backend déployé Railway** | `/health` retourne 200 |
| 3 | **Endpoint `/capture`** | Accepte POST, répond JSON |
| 4 | **Sandbox P4 actif** | Image réelle ignorée → mock utilisé |
| 5 | **iOS projet Xcode** | Build sans crash |
| 6 | **Écran minimal** | Bouton + Champ + Affiche réponse |
| 7 | **Communication E2E** | iOS → Railway → Claude → iOS ✅ |

### Planning Détaillé S0

```
JOUR 1 (Backend skeleton)
├── 1. Créer repo GitHub + structure
├── 2. FastAPI minimal: main.py + /health
├── 3. Déployer sur Railway (même vide)
└── 4. Valider /health retourne 200

JOUR 2 (Backend + Claude)
├── 5. Endpoint /capture (accepte JSON, pas d'image encore)
├── 6. Intégration Claude SDK (prompt hardcodé)
├── 7. Sandbox: mock_image_loader.py
└── 8. Tester via curl: capture → réponse

JOUR 3 (iOS skeleton)
├── 9. Créer projet Xcode SwiftUI
├── 10. APIClient minimal (1 fonction)
├── 11. UI: Bouton + TextField + Text réponse
└── 12. Tester sur simulateur

JOUR 4 (Intégration)
├── 13. iOS → Railway (premier appel réel)
├── 14. Debug CORS/SSL si nécessaire
├── 15. PostgreSQL: 2 tables (users, messages)
└── 16. ✅ GATE S0: Flux complet fonctionne
```

### Gate S0 — Critère de passage

> **"Je tape une question sur iPhone, j'obtiens une réponse de Claude."**

Peu importe si c'est laid, si le code est sale, si y'a pas de gestion d'erreur.  
**Ça passe end-to-end.**

---

## 🔬 PHASE S1 — CORE ENGINE

### Durée: 5-6 jours

### Objectif
> **Le moteur "Une étape à la fois" fonctionne avec les mocks P4**

### Composants à Développer

| Composant | Fichier | Responsabilité |
|-----------|---------|----------------|
| **Reasoning Engine** | `core/reasoning.py` | Décomposition en étapes atomiques |
| **LLM Abstraction** | `core/llm/base.py` | Interface multi-provider |
| **Mock Library** | `core/sandbox/mocks/` | 5-7 captures prédéfinies |
| **State Machine** | `core/session.py` | LIBRE ↔ TECHNIQUE ↔ PAUSE |
| **Prompts** | `core/prompts/iangel_v1.txt` | System prompt calibré |

### Captures Prédéfinies (P4 v1.1)

| ID | Scénario | Fichier mock | Question type |
|----|----------|--------------|---------------|
| M01 | Mise à jour iOS | `ios_update.png` | "C'est-tu sécuritaire?" |
| M02 | Popup Windows suspect | `windows_popup.png` | "C'est-tu un virus?" |
| M03 | Email Desjardins | `email_desjardins.png` | "C'est-tu une fraude?" |
| M04 | Facture Vidéotron | `facture_videotron.png` | "Comment je paie ça?" |
| M05 | Erreur application | `app_error.png` | "Qu'est-ce que ça veut dire?" |

### Règle Critique — Moteur "Une Étape à la Fois"

```python
# Le moteur DOIT fonctionner comme une machine à états:
# 1. Analyser la situation
# 2. Générer UNE SEULE instruction atomique (pas de liste 1., 2., 3.)
# 3. Mettre le système en attente (awaiting_validation: true)
# 4. Attendre signal explicite de l'utilisateur pour continuer
```

### Gate S1 — Critère de passage

> **Les 5 scénarios mocks retournent des réponses "une étape à la fois"**

Test automatisé: `pytest tests/test_scenarios.py` passe.

---

## 🔬 PHASE S2 — POLISH

### Durée: 4-5 jours

### Objectif
> **L'app est utilisable par Ginette (testeur pilote)**

### Priorités de Développement

| Composant | Priorité | Critère |
|-----------|:--------:|---------|
| **Onboarding** | P0 | 3 écrans max, pas de texte long |
| **Gestion erreurs** | P0 | Jamais de "500 Error" visible |
| **Messages réconfortants** | P0 | "Je réfléchis..." pendant loading |
| **Persistance conversation** | P1 | Historique visible |
| **Sentry intégré** | P1 | Erreurs remontées silencieusement |

### Règle Critique — Ginette-Proofing

```
L'utilisateur ne doit JAMAIS voir une erreur technique brute.

❌ "500 Internal Server Error"
❌ "Request Timeout"  
❌ "JSON Parse Error"

✅ "Je réfléchis plus fort que d'habitude..."
✅ "Oups, j'ai eu un petit souci. On réessaie?"
✅ "La connexion est lente, un instant..."
```

### Gate S2 — Critère de passage

> **1 testeur pilote (proche de confiance) complète le flux SANS poser de question**

Protocole: Tu observes silencieusement, tu notes, tu ne parles pas.

---

## 🔬 PHASE S3 — SHIP

### Durée: 2-3 jours

### Objectif
> **TestFlight + Monitoring + 3 vrais testeurs Alpha**

### Checklist Finale

- [ ] App soumise TestFlight
- [ ] Consentement Alpha signé (10 testeurs max)
- [ ] Sentry dashboard configuré
- [ ] UptimeRobot sur `/health`
- [ ] Protocole de test documenté
- [ ] Canal Slack/iMessage pour feedback

### Gate S3 — Critère de Succès Alpha (PRD)

> **3 utilisateurs réels complètent le flux capture → réponse SANS aide externe.**

C'est LE critère de succès du PRD. Tout le reste est secondaire.

---

## 📈 TIMELINE VISUELLE

```
S0: SKELETON ────────────────────────────────────────────►
    [Jour 1-4]
    Backend /health → +Claude /capture → iOS basic → E2E ✓

                    S1: CORE ENGINE ─────────────────────►
                        [Jour 5-10]
                        Reasoning.py + 5 Mocks + State Machine + Tests ✓

                                           S2: POLISH ────►
                                               [Jour 11-15]
                                               Onboarding + Erreurs + Pilote ✓

                                                      S3: SHIP
                                                          [Jour 16-18]
                                                          TestFlight + 3 testeurs ✓
```

---

## 📚 DOCUMENTS DE RÉFÉRENCE

### Hiérarchie de Vérité (en cas de conflit, ces documents prévalent)

1. **Architecture (ADR P3)** — La Vérité Technique
   - Stack imposée: FastAPI + SwiftUI + Railway
   - Pas de React/Flutter

2. **Produit (PRD MVP Alpha)** — La Vérité UX
   - Philosophie "Une étape à la fois"
   - Ne jamais presser Ginette

3. **Brief Technique (P3)** — Le Scope
   - 91h budget (~4.5 semaines)
   - Pas de TTS/STT pour l'Alpha
   - Pas d'Android

4. **Conformité (Rapport P4 v1.1)** — CRITIQUE
   - Alpha utilise captures PRÉDÉFINIES (mocks)
   - Pas d'images réelles des utilisateurs
   - Risque légal réduit à zéro

### Fichiers du Projet

- `/mnt/project/iAngel_PRD_MVP_Alpha_v1.md`
- `/mnt/project/iAngel_P3_Brief_Technique_Developpeur_v1.md`
- `/mnt/project/iAngel_P3_Architecture_Decision_Records_v1.md`
- `/mnt/project/iAngel_P4_Rapport_Conformite_v1_1.js`

---

## ✅ PROCHAINE ACTION

**Question du lab PRO:** "Où est ton repo GitHub? Quel est l'état actuel du code?"

**Options:**
1. **Repo vide** → Démarrer S0 Jour 1
2. **Code existant** → Audit pour déterminer phase actuelle
3. **Prototypes éparpillés** → Décider quoi récupérer vs réécrire

---

*Document généré pour continuité de projet. À utiliser comme référence dans les nouvelles conversations Claude.*
