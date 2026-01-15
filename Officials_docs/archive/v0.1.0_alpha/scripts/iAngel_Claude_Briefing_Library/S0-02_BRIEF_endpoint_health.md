# 🔧 BRIEFING COMPOSANT S0-02
## Endpoint /health

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S0-02 |
| **Phase** | S0 — Walking Skeleton |
| **Composant** | Endpoint de santé |
| **Priorité** | P0 (Critique) |
| **Dépendances** | S0-01 (Structure repo) |
| **Durée estimée** | 30 minutes |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S0-02 — ENDPOINT /health
══════════════════════════════════════════════════════════════

Tu vas implémenter l'endpoint /health du backend iAngel.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPÉCIFICATION COMPORTEMENTALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF:
Créer un endpoint /health qui:
1. Retourne 200 OK si le serveur est vivant
2. Vérifie la connectivité base de données (optionnel pour S0)
3. Retourne un JSON structuré avec statut et version
4. Sert de probe pour Railway et UptimeRobot

COMPORTEMENT ATTENDU:
```
GET /health

Response 200:
{
  "status": "healthy",
  "version": "0.1.0-alpha",
  "environment": "development",
  "timestamp": "2025-12-28T15:30:00Z",
  "checks": {
    "database": "skip",  // "ok" ou "error" en Phase S2
    "llm_api": "skip"    // "ok" ou "error" en Phase S2
  }
}

Response 503 (si un check échoue en Phase S2):
{
  "status": "unhealthy",
  "version": "0.1.0-alpha",
  "environment": "production",
  "timestamp": "...",
  "checks": {
    "database": "error",
    "llm_api": "ok"
  },
  "error_details": "Database connection timeout"
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTRAINTES ARCHITECTURALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STACK IMPOSÉE (ADR P3):
- FastAPI router
- Pydantic V2 pour les schémas de réponse
- Typage strict (pas de dict brut)

FICHIERS À CRÉER/MODIFIER:
```
app/
├── api/v1/endpoints/health.py   # Router de l'endpoint
├── models/schemas.py            # HealthResponse schema
└── main.py                      # Inclure le router
```

SCHÉMA PYDANTIC (obligatoire):
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class HealthChecks(BaseModel):
    database: Literal["ok", "error", "skip"]
    llm_api: Literal["ok", "error", "skip"]

class HealthResponse(BaseModel):
    status: Literal["healthy", "unhealthy"]
    version: str
    environment: str
    timestamp: datetime
    checks: HealthChecks
    error_details: str | None = None
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES CRITIQUES (À NE JAMAIS OUBLIER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. UTILISATEUR CIBLE: GINETTE (72 ans)
   > Même /health doit être pensé "Ginette".
   > Ce n'est PAS un endpoint visible par Ginette, mais ça pose les bases
   > de notre architecture typée et structurée.

2. PAS DE TRY/EXCEPT VIDE
   > Si tu catches une exception, tu DOIS:
   > - La logger (print minimum pour S0, structuré en S2)
   > - Retourner un message utile

3. VERSION DEPUIS CONFIG
   > La version ne doit PAS être hardcodée dans l'endpoint.
   > Elle vient de config.py ou pyproject.toml.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMAT DE RÉPONSE ATTENDU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour CHAQUE fichier:
1. Chemin complet
2. Code complet avec commentaires
3. Explication de 1 ligne du rôle

À LA FIN:
- Commande curl pour tester localement
- Test pytest minimal

══════════════════════════════════════════════════════════════
CONFIRME QUE TU AS CHARGÉ CE BRIEFING EN RÉPONDANT:
"BRIEFING S0-02 CHARGÉ — Prêt à implémenter /health"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] `GET /health` retourne 200
- [ ] Réponse est du JSON valide
- [ ] Schéma Pydantic HealthResponse utilisé
- [ ] Version lue depuis config (pas hardcodée)
- [ ] Test pytest passe

---

## 🧪 TEST DE VALIDATION

```bash
# Démarrer le serveur
uvicorn app.main:app --reload

# Tester
curl http://localhost:8000/health | jq

# Attendu: JSON avec status "healthy"
```

---

## 🔗 COMPOSANT SUIVANT

Après validation S0-02, passer à: `S0-03_BRIEF_endpoint_capture.md`
