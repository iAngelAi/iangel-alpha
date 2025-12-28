# 🔧 BRIEFING COMPOSANT S0-01
## Structure Repo GitHub + FastAPI Minimal

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S0-01 |
| **Phase** | S0 — Walking Skeleton |
| **Composant** | Structure du projet backend |
| **Priorité** | P0 (Critique) |
| **Dépendances** | Aucune (Premier composant) |
| **Durée estimée** | 1-2 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S0-01 — STRUCTURE REPO + FASTAPI MINIMAL
══════════════════════════════════════════════════════════════

Tu vas implémenter la STRUCTURE INITIALE du backend iAngel.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPÉCIFICATION COMPORTEMENTALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF:
Créer la structure de fichiers du repo backend conforme aux standards 
d'un laboratoire professionnel, prête pour déploiement Railway.

LIVRABLES ATTENDUS:
1. Structure de dossiers modulaire (Router/Service/Repository)
2. pyproject.toml avec dépendances minimales
3. main.py avec FastAPI vide (juste l'import)
4. .env.example avec les variables attendues
5. .gitignore Python complet
6. README.md avec instructions setup
7. Dockerfile minimal pour Railway

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTRAINTES ARCHITECTURALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STACK IMPOSÉE (ADR P3):
- Python 3.11+
- FastAPI 0.109+
- Pydantic V2 (PAS V1)
- uvicorn[standard]
- httpx (pour tests)
- python-dotenv

STRUCTURE DE DOSSIERS:
```
iangel-alpha-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée FastAPI
│   ├── config.py               # Configuration (Pydantic Settings)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py           # Routeur principal
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── health.py   # Endpoint /health
│   │           └── capture.py  # Endpoint /capture (Phase S0-03)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── reasoning.py        # Moteur (Phase S1)
│   │   ├── session.py          # State machine (Phase S1)
│   │   └── llm/
│   │       ├── __init__.py
│   │       └── base.py         # Abstraction LLM (Phase S1)
│   ├── sandbox/
│   │   ├── __init__.py
│   │   └── mock_loader.py      # Chargeur mocks P4 (Phase S0-04)
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Schémas Pydantic
│   └── services/
│       ├── __init__.py
│       └── capture_service.py  # Logique métier
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Fixtures pytest
│   └── test_health.py
├── mocks/                      # Images prédéfinies P4
│   └── .gitkeep
├── .env.example
├── .gitignore
├── pyproject.toml
├── Dockerfile
├── railway.toml
└── README.md
```

PATTERNS OBLIGATOIRES:
- TOUS les imports relatifs (pas de "from app import" dans app/)
- Typage STRICT sur toutes les fonctions
- Docstrings Google style
- NO magic strings (tout dans config.py ou constantes)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES CRITIQUES (À NE JAMAIS OUBLIER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PROTOCOLE P4 — SANDBOX ALPHA
   > Le dossier /mocks/ est CRITIQUE. En Alpha, AUCUNE image utilisateur
   > réelle ne sera traitée. Seulement des captures prédéfinies.
   > Prépare la structure pour ça.

2. UTILISATEUR CIBLE: GINETTE (72 ans)
   > L'architecture DOIT permettre des messages d'erreur EMPATHIQUES.
   > Jamais de "500 Internal Server Error" visible.
   > Prévois une structure pour la gestion d'erreur customisée.

3. PAS DE OVER-ENGINEERING
   > Phase S0 = Walking Skeleton = Minimum viable.
   > Les fichiers peuvent être vides avec juste un commentaire # TODO Phase S1
   > L'important c'est que la STRUCTURE soit correcte.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMAT DE RÉPONSE ATTENDU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour CHAQUE fichier:
1. Chemin complet
2. Code complet avec commentaires
3. Explication de 1 ligne du rôle

À LA FIN:
- Commandes pour initialiser le repo
- Commande pour vérifier que ça fonctionne

══════════════════════════════════════════════════════════════
CONFIRME QUE TU AS CHARGÉ CE BRIEFING EN RÉPONDANT:
"BRIEFING S0-01 CHARGÉ — Prêt à créer la structure du repo"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] Structure de dossiers créée
- [ ] pyproject.toml valide avec dépendances
- [ ] main.py importe FastAPI correctement
- [ ] .env.example liste toutes les variables
- [ ] Dockerfile construit sans erreur
- [ ] `python -c "from app.main import app"` ne crashe pas

---

## 🔗 COMPOSANT SUIVANT

Après validation S0-01, passer à: `S0-02_BRIEF_endpoint_health.md`
