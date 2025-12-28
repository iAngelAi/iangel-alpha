# 🔧 BRIEFING COMPOSANT S2-01
## Onboarding iOS — Premier Contact avec Ginette

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S2-01 |
| **Phase** | S2 — Polish |
| **Composant** | Écrans d'accueil première utilisation |
| **Priorité** | P0 (Première impression = critique) |
| **Dépendances** | S0-05 (Projet iOS) |
| **Durée estimée** | 3-4 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S2-01 — ONBOARDING iOS
══════════════════════════════════════════════════════════════

Tu vas créer l'ONBOARDING pour Ginette, 72 ans.

C'est sa première impression d'iAngel. Ça doit être:
- SIMPLE (3 écrans max)
- RASSURANT (pas de jargon)
- RAPIDE (< 30 secondes)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FLOW ONBOARDING (3 ÉCRANS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ÉCRAN 1: BIENVENUE
```
┌────────────────────────────────────┐
│                                    │
│         [Illustration douce]       │
│                                    │
│      Bonjour, je suis iAngel       │
│                                    │
│   Votre guide pour la technologie  │
│                                    │
│        [ Commencer → ]             │
│                                    │
└────────────────────────────────────┘
```

ÉCRAN 2: COMMENT ÇA MARCHE
```
┌────────────────────────────────────┐
│                                    │
│      [Illustration capture]        │
│                                    │
│   Montrez-moi votre écran,         │
│   et posez votre question.         │
│                                    │
│   Je vous guide, une étape         │
│   à la fois.                       │
│                                    │
│        [ Suivant → ]               │
│                                    │
└────────────────────────────────────┘
```

ÉCRAN 3: PRÊT
```
┌────────────────────────────────────┐
│                                    │
│       [Illustration rassurante]    │
│                                    │
│     Prenez votre temps.            │
│     Je suis patiente.              │
│                                    │
│        [ C'est parti! ]            │
│                                    │
└────────────────────────────────────┘
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FICHIERS À CRÉER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```
iAngel/Features/Onboarding/
├── OnboardingView.swift          # Vue conteneur
├── OnboardingPageView.swift      # Composant page
├── OnboardingViewModel.swift     # État + navigation
└── OnboardingComplete.swift      # Marque fin onboarding
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES GINETTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. TEXTE GROS (minimum 20pt)
2. PAS de skip (on veut qu'elle lise)
3. PAS de dots de pagination (confus)
4. Boutons TRÈS visibles (44x44pt minimum)
5. Animations DOUCES (pas de flash)
6. UserDefaults pour savoir si déjà vu

══════════════════════════════════════════════════════════════
CONFIRME: "BRIEFING S2-01 CHARGÉ — Prêt à créer l'Onboarding"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] 3 écrans maximum
- [ ] Texte 20pt minimum
- [ ] Boutons 44x44pt minimum
- [ ] UserDefaults mémorise completion
- [ ] VoiceOver fonctionne

---

## 🔗 COMPOSANT SUIVANT

Après validation: `S2-02_BRIEF_error_handling_backend.md`
