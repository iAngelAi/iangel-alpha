# Architecture de Référence - iAngel (Alpha S4)

**Date de mise à jour :** 15 Janvier 2026
**Version :** 0.1.0-alpha

Ce document décrit l'état technique validé du système iAngel. Toute modification ultérieure doit respecter les invariants définis ici.

---

## 1. Principes Fondamentaux

1.  **Robustesse > Vitesse :** Aucun code n'est mergé sans tests passants (100% success).
2.  **Isolation des Tests :** Les tests unitaires n'ont JAMAIS accès au réseau ni à la base de données de production.
3.  **Typage Strict :** Tout échange de données (Interne ou API) est validé par Pydantic.

## 2. Backend (FastAPI)

### Modèle de Données (Database)
Le système utilise **PostgreSQL** (via `asyncpg`) en production et **SQLite** (via `aiosqlite`) en test.
L'ORM est **SQLAlchemy 2.0+** en mode purement asynchrone.

*   `conversations` : Stocke l'état du moteur de raisonnement (`reasoning_state`) et les métadonnées.
*   `messages` : Historique immuable des échanges.

### Moteur de Raisonnement (Core)
Le `ReasoningEngine` est une machine à états finis :
*   `IDLE` : Prêt.
*   `ANALYZING` : Traitement LLM en cours.
*   `AWAITING_VALIDATION` : Instruction donnée, attente de confirmation de Ginette.
*   `COMPLETED` : Problème résolu.

### Gestion Émotionnelle (Phase S3)
Chaque réponse inclut un `emotional_context` strict :
*   `neutral` : Instruction standard.
*   `reassuring` : Détection de stress léger -> Ton doux, check-in automatique.
*   `protective` : Détection de danger (virus, arnaque) -> Ton ferme, blocage de l'action.
*   `celebratory` : Succès -> Renforcement positif.

## 3. Interface iOS (SwiftUI)

L'application iOS est un **miroir strict** du Backend.
Elle ne contient aucune logique métier complexe, seulement de l'affichage réactif.

*   **Modèles :** `CaptureRequest` et `CaptureResponse` doivent être synchronisés byte-pour-byte avec les schémas Pydantic (`app/models/schemas.py`).
*   **Synthèse Vocale :** Le champ `spoken_message` est lu par `AVSpeechSynthesizer` (voix fr-CA).

## 4. Protocole de Test (Laboratoire)

La suite de tests est la garante de la sécurité de Ginette.

*   **`tests/factories.py` :** Source de vérité pour les données de test.
*   **`tests/conftest.py` :** Gardien de l'isolation (Mocking force du réseau).
*   **Scripts de Simulation :** `scripts/simulate_ios_client.py` valide le contrat d'interface sans nécessiter Xcode.

---

## 5. Déploiement (Railway)

*   **Build :** Dockerfile multi-stage (uv).
*   **Variables d'Env :** Gérées via `app/config.py` (Pydantic Settings).
*   **Healthcheck :** `/api/v1/health` vérifie la connectivité DB réelle.
