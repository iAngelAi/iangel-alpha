# iAngel Backend

Backend API pour iAngel, l'ange-gardien numérique qui accompagne les aînés québécois dans leur quotidien technologique.

## Prérequis

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (gestionnaire de paquets)

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/iAngelAi/iangel-alpha.git
cd iangel-alpha

# Créer l'environnement virtuel et installer les dépendances
uv venv
source .venv/bin/activate  # Linux/macOS
# ou .venv\Scripts\activate  # Windows

uv sync
```

## Configuration

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et ajouter votre clé API Anthropic
# ANTHROPIC_API_KEY=sk-ant-...
```

## Développement

```bash
# Lancer le serveur de développement
uv run uvicorn app.main:app --reload --port 8000

# Lancer les tests
uv run pytest tests/ -v

# Vérifier les types
uv run mypy app/

# Linter
uv run ruff check app/
uv run ruff format app/
```

## Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/v1/health` | GET | Vérification de santé du service |
| `/api/v1/capture` | POST | Traitement d'une capture d'écran (TODO S0-03) |

## Structure du Projet

```
iangel-alpha/
├── app/
│   ├── api/              # Endpoints REST
│   ├── core/             # Logique métier centrale
│   │   ├── errors.py     # Exceptions empathiques
│   │   ├── middleware.py # Gestionnaire d'erreurs
│   │   └── llm/          # Adaptateurs LLM
│   ├── models/           # Schémas Pydantic
│   ├── sandbox/          # Mode bac à sable (P4)
│   ├── services/         # Services métier
│   ├── config.py         # Configuration
│   └── main.py           # Point d'entrée
├── tests/                # Tests pytest
├── mocks/                # Fichiers mock (P4)
└── Officials_docs/       # Documentation officielle
```

## Phases de Développement

- **S0-01** : Structure repo + FastAPI minimal ✅
- **S0-02** : Endpoint /health détaillé (à venir)
- **S0-03** : Endpoint /capture avec Claude API (à venir)
- **S0-04** : Mocks et scénarios de test (à venir)

## Documentation

La documentation complète du projet se trouve dans le dossier `Officials_docs/`.

## Licence

Propriétaire - Tous droits réservés.
