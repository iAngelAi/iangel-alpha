# iAngel - L'Ange Gardien Numérique (Alpha)

> **Pour Ginette.** Parce que la technologie ne devrait jamais faire peur.

iAngel est un assistant IA bienveillant conçu pour protéger et guider les aînés techno-vulnérables. Il privilégie la sécurité émotionnelle, le pas-à-pas ("One step at a time") et l'absence totale de jargon.

![Status](https://img.shields.io/badge/Status-Alpha_S4-blue)
![Quality](https://img.shields.io/badge/Tests-100%25_Passed-brightgreen)
![License](https://img.shields.io/badge/License-Proprietary-red)

---

## 🏗 Architecture "Béton Armé"

Le système repose sur une architecture découplée et robuste :

*   **Cerveau (Backend) :** Python 3.11+, FastAPI, PostgreSQL (via SQLAlchemy Async).
    *   *Reasoning Engine :* Machine à états finis pour le guidage pas-à-pas.
    *   *LLM :* Anthropic Claude 3.5 Sonnet (avec support Vision).
    *   *Sécurité :* Middleware empathique, validation Pydantic stricte.
*   **Corps (Mobile) :** iOS 17+, SwiftUI.
    *   *Interface :* Réactive aux émotions (couleurs, avatar).
    *   *Voix :* Synthèse vocale (TTS) intégrée pour rassurer.

## 🚀 Démarrage Rapide

### Prérequis
*   Python 3.11+
*   `uv` (Package manager)
*   Clé API Anthropic (pour le mode Production)

### Installation
```bash
# 1. Cloner le projet
git clone <repo_url>
cd iangel-alpha

# 2. Installer les dépendances
uv sync

# 3. Configurer l'environnement
cp .env.example .env
# (Éditez .env avec vos clés)
```

### Lancer le Backend
```bash
# Mode Développement (Reload actif)
./start_server.sh
```
L'API sera disponible sur `http://localhost:8000`.
Documentation interactive : `http://localhost:8000/docs`.

### Lancer les Tests (Rigueur Absolue)
```bash
# Exécute la suite de 100 tests isolés
uv run pytest tests/
```

---

## 🛡️ Protocoles de Sécurité (Pédagogie S3)

1.  **Validation Émotionnelle :** iAngel analyse l'image et le texte pour détecter la panique.
2.  **Check-in Automatique :** Si l'instruction est complexe, iAngel demande "Est-ce que c'est clair ?".
3.  **Boucle de Sécurité :** En cas d'échec répété, le système propose une alternative ou passe le relais à un humain (simulé en Alpha).

---

## 📂 Structure du Projet

```
iangel-alpha/
├── app/
│   ├── core/           # Cœur du réacteur (Reasoning, State, LLM)
│   ├── api/            # Routes FastAPI (v1)
│   ├── models/         # Schémas Pydantic & SQLAlchemy
│   └── services/       # Logique métier (Capture, Health)
├── ios/                # Application iPhone (SwiftUI)
├── tests/              # Suite de tests (Unit + Integration)
├── mocks/              # Scénarios de test (Json)
└── Officials_docs/     # Documentation de référence
```

---

**Développé avec ❤️ et Rigueur au Québec.**