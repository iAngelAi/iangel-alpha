# 🚀 GUIDE RAPIDE — Bibliothèque de Briefings iAngel

## Comment utiliser ces scripts

### Étape 1: Identifier où tu es

```
PHASE S0 (Skeleton)   → Tu commences? → S0-01
PHASE S1 (Core)       → Skeleton fonctionne? → S1-01
PHASE S2 (Polish)     → Core testé? → S2-01
PHASE S3 (Ship)       → Prêt pour testeurs? → S3-01
```

### Étape 2: Ouvrir une NOUVELLE conversation Claude

### Étape 3: Copier-coller le contenu du script correspondant

### Étape 4: Attendre la confirmation

```
Claude: "BRIEFING S0-01 CHARGÉ — Prêt à créer la structure du repo"
```

### Étape 5: Demander l'implémentation

```
Toi: "Implémente"
```

---

## 📁 Fichiers de la bibliothèque

### Phase S0 — Walking Skeleton (Jours 1-4)
| Fichier | Composant |
|---------|-----------|
| `S0-01_BRIEF_repo_structure.md` | Structure repo + FastAPI |
| `S0-02_BRIEF_endpoint_health.md` | Endpoint /health |
| `S0-03_BRIEF_endpoint_capture.md` | Endpoint /capture |
| `S0-04_BRIEF_mock_loader.md` | Sandbox P4 |
| `S0-05_BRIEF_xcode_project.md` | Projet iOS |
| `S0-06_BRIEF_api_client_ios.md` | APIClient |
| `S0-07_BRIEF_ui_skeleton.md` | UI minimale |

### Phase S1 — Core Engine (Jours 5-10)
| Fichier | Composant |
|---------|-----------|
| `S1-01_BRIEF_reasoning_engine.md` | Moteur "une étape" |
| `S1-02_BRIEF_llm_abstraction.md` | Interface LLM |
| `S1-03_BRIEF_mock_library.md` | 5 scénarios test |
| `S1-04_BRIEF_state_machine.md` | États conversation |
| `S1-05_BRIEF_system_prompts.md` | Prompts calibrés |

### Phase S2 — Polish (Jours 11-15)
| Fichier | Composants |
|---------|-----------|
| `S2-01_BRIEF_onboarding_ios.md` | Onboarding |
| `S2-02_to_S2-05_BRIEFS.md` | Errors + Loading + Persistence |

### Phase S3 — Ship (Jours 16-18)
| Fichier | Composants |
|---------|-----------|
| `S3-01_to_S3-04_BRIEFS.md` | TestFlight + Sentry + Tests |

---

## 🎯 Gates de Validation

| Phase | Test | Critère |
|:-----:|------|---------|
| **S0** | E2E basique | "Question sur iPhone → Réponse Claude" |
| **S1** | Scénarios mocks | "5 mocks passent en mode une étape" |
| **S2** | Test pilote | "1 personne sans questions" |
| **S3** | Alpha | "3 testeurs sans aide" |

---

## ⚠️ Rappels Critiques

1. **PROTOCOLE P4** — JAMAIS d'images réelles utilisateur
2. **UNE ÉTAPE** — JAMAIS de listes numérotées
3. **GINETTE** — JAMAIS d'erreur technique visible
4. **TYPAGE** — JAMAIS de `Any` en Python ni `!` en Swift

---

## 🏁 Checklist de Démarrage

```
[ ] Repo GitHub créé (iAngelAi/iangel-alpha)
[ ] Railway account configuré
[ ] Apple Developer account actif
[ ] Variables .env prêtes (ANTHROPIC_API_KEY, etc.)
[ ] 10 testeurs identifiés
```

---

**🔥 POUR GINETTE — Le foyer reste allumé! 🔥**
