# 🔧 BRIEFING COMPOSANT S0-04
## Mock Image Loader (Sandbox P4)

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S0-04 |
| **Phase** | S0 — Walking Skeleton |
| **Composant** | Système de chargement des captures prédéfinies |
| **Priorité** | P0 (CRITIQUE - Conformité légale) |
| **Dépendances** | S0-01 (Structure repo) |
| **Durée estimée** | 1-2 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S0-04 — MOCK IMAGE LOADER (SANDBOX P4)
══════════════════════════════════════════════════════════════

Tu vas implémenter le SYSTÈME DE SANDBOX du backend iAngel.

⚠️ CE COMPOSANT EST CRITIQUE POUR LA CONFORMITÉ LÉGALE ⚠️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTEXTE LÉGAL — PROTOCOLE P4 v1.1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLÈME:
Les utilisateurs Alpha (Ginette, 72 ans) pourraient capturer des 
écrans contenant des informations sensibles:
- Numéros de compte bancaire
- Informations médicales
- Données personnelles

SOLUTION APPROUVÉE (Rapport P4 v1.1):
> En Phase Alpha, le backend utilise EXCLUSIVEMENT des captures
> PRÉDÉFINIES (mocks). Les images réelles des utilisateurs sont
> IGNORÉES et JAMAIS stockées ni envoyées au LLM.

CONSÉQUENCE:
> Risque légal réduit à ZÉRO pour la Loi 25 / PIPEDA.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPÉCIFICATION COMPORTEMENTALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF:
Créer un MockLoader qui:
1. Reçoit un mock_id (ex: "M02")
2. Charge l'image prédéfinie correspondante depuis /mocks/
3. Retourne les bytes de l'image + métadonnées
4. Log EXPLICITEMENT que l'image réelle a été ignorée

SCÉNARIOS PRÉDÉFINIS (Phase S0-S1):
| ID | Scénario | Fichier | Description |
|----|----------|---------|-------------|
| M01 | Mise à jour iOS | ios_update.png | Popup "Mise à jour disponible" |
| M02 | Popup Windows suspect | windows_popup.png | Fausse alerte virus |
| M03 | Email Desjardins | email_desjardins.png | Email de phishing |
| M04 | Facture Vidéotron | facture_videotron.png | Facture télécom |
| M05 | Erreur application | app_error.png | Message d'erreur générique |

COMPORTEMENT ATTENDU:
```python
loader = MockLoader()

# Cas normal
result = loader.load("M02")
# -> MockImage(
#      id="M02",
#      filename="windows_popup.png",
#      image_bytes=b"...",
#      description="Fausse alerte virus Windows",
#      expected_question_type="fraude/sécurité"
#    )

# Cas mock inexistant -> Fallback sur M01
result = loader.load("M99")
# -> MockImage pour M01 (défaut) + warning log

# Logging automatique
# [INFO] MockLoader: Image réelle IGNORÉE (Protocole P4). Mock M02 chargé.
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTRAINTES ARCHITECTURALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FICHIERS À CRÉER:
```
app/
├── sandbox/
│   ├── __init__.py
│   ├── mock_loader.py       # Classe MockLoader
│   └── mock_registry.py     # Registre des mocks disponibles
mocks/
├── M01_ios_update.png
├── M02_windows_popup.png
├── M03_email_desjardins.png
├── M04_facture_videotron.png
├── M05_app_error.png
└── registry.json            # Métadonnées des mocks
```

SCHÉMAS PYDANTIC:
```python
from pydantic import BaseModel
from typing import Literal

class MockMetadata(BaseModel):
    id: str
    filename: str
    description: str
    scenario_type: Literal["security", "fraud", "billing", "error", "update"]
    expected_questions: list[str]  # Questions types pour ce scénario

class MockImage(BaseModel):
    id: str
    filename: str
    image_bytes: bytes
    metadata: MockMetadata
    
    class Config:
        arbitrary_types_allowed = True
```

INTERFACE MockLoader:
```python
class MockLoader:
    def __init__(self, mocks_dir: Path = Path("mocks")):
        ...
    
    def load(self, mock_id: str) -> MockImage:
        """Charge un mock par ID. Fallback sur M01 si inexistant."""
        ...
    
    def list_available(self) -> list[MockMetadata]:
        """Liste tous les mocks disponibles."""
        ...
    
    def log_protocol_p4(self, mock_id: str) -> None:
        """Log explicite que le Protocole P4 est respecté."""
        ...
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES CRITIQUES (À NE JAMAIS OUBLIER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. LOGGING OBLIGATOIRE
   > Chaque appel à load() DOIT logger:
   > "[P4-SANDBOX] Image utilisateur IGNORÉE. Mock {mock_id} utilisé."
   > C'est une preuve d'audit pour conformité.

2. JAMAIS DE STOCKAGE IMAGE UTILISATEUR
   > Le paramètre image_data de CaptureRequest est passé au MockLoader
   > UNIQUEMENT pour le log. Il ne doit JAMAIS être:
   > - Stocké sur disque
   > - Envoyé à un service externe
   > - Écrit dans un log (même en debug)

3. FALLBACK GRACIEUX
   > Si mock_id inexistant, retourner M01 (défaut) + warning.
   > JAMAIS d'erreur technique visible pour l'utilisateur.

4. IMAGES PLACEHOLDER POUR S0
   > Pour le skeleton, les fichiers .png peuvent être des images
   > simples (même une image 1x1 pixel). Le contenu réel sera
   > ajouté en Phase S1.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMAT DE RÉPONSE ATTENDU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour CHAQUE fichier:
1. Chemin complet
2. Code complet avec commentaires
3. Explication de 1 ligne du rôle

À LA FIN:
- Script pour générer les images placeholder
- Test pytest qui vérifie le logging P4
- Commande pour vérifier que les mocks sont chargés

══════════════════════════════════════════════════════════════
CONFIRME QUE TU AS CHARGÉ CE BRIEFING EN RÉPONDANT:
"BRIEFING S0-04 CHARGÉ — Prêt à implémenter le Sandbox P4"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] MockLoader.load("M01") retourne MockImage valide
- [ ] MockLoader.load("M99") fallback sur M01 + warning
- [ ] Log "[P4-SANDBOX]" présent à chaque load()
- [ ] registry.json contient métadonnées des 5 mocks
- [ ] Test pytest vérifie le comportement
- [ ] AUCUNE trace d'image utilisateur dans les logs

---

## 🧪 TEST DE VALIDATION

```python
# tests/test_mock_loader.py

def test_protocol_p4_logging(caplog):
    """Vérifie que le Protocole P4 est logué."""
    loader = MockLoader()
    result = loader.load("M02")
    
    assert "P4-SANDBOX" in caplog.text
    assert "Image utilisateur IGNORÉE" in caplog.text
    assert result.id == "M02"

def test_fallback_on_unknown_mock():
    """Vérifie le fallback sur M01 pour mock inconnu."""
    loader = MockLoader()
    result = loader.load("INEXISTANT")
    
    assert result.id == "M01"  # Fallback
```

---

## 🔗 COMPOSANT SUIVANT

Après validation S0-04, passer à: `S0-05_BRIEF_xcode_project.md`
