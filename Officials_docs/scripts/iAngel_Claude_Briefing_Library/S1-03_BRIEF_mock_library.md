# 🔧 BRIEFING COMPOSANT S1-03
## Mock Library — 5 Scénarios de Test

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S1-03 |
| **Phase** | S1 — Core Engine |
| **Composant** | Bibliothèque de captures prédéfinies |
| **Priorité** | P0 (Requis pour tests) |
| **Dépendances** | S0-04 (Mock Loader) |
| **Durée estimée** | 2-3 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S1-03 — MOCK LIBRARY (5 SCÉNARIOS)
══════════════════════════════════════════════════════════════

Tu vas créer les 5 CAPTURES PRÉDÉFINIES pour tester le moteur iAngel.

⚠️ PROTOCOLE P4: Ces mocks remplacent les vraies images en Alpha.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LES 5 SCÉNARIOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| ID | Scénario | Image | Questions Types |
|----|----------|-------|-----------------|
| M01 | Mise à jour iOS | Popup "iOS 18.2 disponible" | "C'est tu sécuritaire?" |
| M02 | Popup Windows | Fausse alerte "Virus détecté!" | "C'est tu un virus?" |
| M03 | Email Desjardins | Email de phishing | "C'est tu une fraude?" |
| M04 | Facture Vidéotron | Facture mensuelle PDF | "Comment je paie ça?" |
| M05 | Erreur app | "L'application a cessé" | "Qu'est-ce que ça veut dire?" |

FICHIERS À CRÉER:
```
mocks/
├── M01_ios_update.png
├── M02_windows_popup.png
├── M03_email_desjardins.png
├── M04_facture_videotron.png
├── M05_app_error.png
├── registry.json             # Métadonnées
└── expected_responses/       # Réponses attendues
    ├── M01_expected.json
    ├── M02_expected.json
    └── ...
```

REGISTRY.JSON:
```json
{
  "mocks": [
    {
      "id": "M01",
      "filename": "M01_ios_update.png",
      "scenario": "Mise à jour iOS",
      "description": "Popup de mise à jour iOS 18.2",
      "expected_anxiety_level": "low",
      "expected_steps": 5,
      "test_questions": [
        "C'est tu sécuritaire?",
        "Est-ce que je dois faire ça?"
      ]
    }
  ]
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. IMAGES RÉALISTES mais GÉNÉRIQUES (pas de vraies données)
2. Créer/sourcer des screenshots type (Canva, captures modifiées)
3. expected_responses doit valider le comportement "une étape"
4. Chaque scénario teste un type d'anxiété différent

══════════════════════════════════════════════════════════════
CONFIRME: "BRIEFING S1-03 CHARGÉ — Prêt à créer la Mock Library"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] 5 images PNG présentes dans /mocks/
- [ ] registry.json valide
- [ ] Chaque mock a des questions types
- [ ] expected_responses pour tests automatisés

---

## 🔗 COMPOSANT SUIVANT

Après validation: `S1-04_BRIEF_state_machine.md`
