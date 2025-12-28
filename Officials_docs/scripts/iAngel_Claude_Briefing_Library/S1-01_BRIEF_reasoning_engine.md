# 🔧 BRIEFING COMPOSANT S1-01
## Reasoning Engine — Moteur "Une Étape à la Fois"

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S1-01 |
| **Phase** | S1 — Core Engine |
| **Composant** | Moteur de raisonnement iAngel |
| **Priorité** | P0 (CŒUR du produit) |
| **Dépendances** | S0 complet |
| **Durée estimée** | 4-6 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S1-01 — REASONING ENGINE
══════════════════════════════════════════════════════════════

Tu vas implémenter le MOTEUR DE RAISONNEMENT iAngel.

C'est le CŒUR DIFFÉRENTIATEUR du produit: contrairement aux autres
assistants qui déversent des listes numérotées, iAngel guide
UNE ÉTAPE À LA FOIS avec validation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LA PHILOSOPHIE "UNE ÉTAPE À LA FOIS"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLÈME (Autres assistants):
```
Utilisateur: "Comment faire une mise à jour iOS?"

ChatGPT: 
"Voici les étapes:
1. Allez dans Réglages
2. Appuyez sur Général
3. Appuyez sur Mise à jour logicielle
4. Appuyez sur Télécharger et installer
5. Entrez votre code
6. Acceptez les conditions
7. Attendez le téléchargement
8. Appuyez sur Installer maintenant
Bonne chance!"

Ginette: "...J'ai même pas allumé mon téléphone encore."
```

SOLUTION iAngel:
```
Utilisateur: "Comment faire une mise à jour iOS?"

iAngel:
"D'abord, assurez-vous que votre iPhone est branché au chargeur.
Dites-moi quand c'est fait, je vous guide pour la suite."

[SYSTÈME EN ATTENTE - awaiting_validation: true]

Utilisateur: "OK c'est fait"

iAngel:
"Parfait! Maintenant, trouvez l'icône grise avec un engrenage 
qui s'appelle 'Réglages'. C'est souvent sur votre écran principal.
Dites-moi quand vous l'avez trouvée."

[SYSTÈME EN ATTENTE]
... (continue étape par étape)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPÉCIFICATION COMPORTEMENTALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPORTEMENT DU MOTEUR:
1. ANALYSER la question + image mock
2. DÉCOMPOSER la tâche en étapes atomiques (en interne)
3. GÉNÉRER UNE SEULE instruction (la première)
4. METTRE EN PAUSE (awaiting_validation = true)
5. ATTENDRE le signal utilisateur ("OK", "C'est fait", etc.)
6. CONTINUER avec l'étape suivante
7. RÉPÉTER jusqu'à complétion

RÈGLES ABSOLUES:
- JAMAIS de liste numérotée (1., 2., 3.)
- JAMAIS de "Premièrement... Deuxièmement..."
- JAMAIS de "Voici les étapes:"
- TOUJOURS une seule action à la fois
- TOUJOURS attendre validation avant de continuer

FICHIERS À CRÉER:
```
app/
├── core/
│   ├── reasoning.py          # ReasoningEngine class
│   ├── step_decomposer.py    # Décomposition en étapes
│   └── validation_detector.py # Détecte "OK", "fait", etc.
├── prompts/
│   └── iangel_system_v1.txt  # Prompt system calibré
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHITECTURE DU MOTEUR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
from pydantic import BaseModel
from typing import Literal

class ReasoningState(BaseModel):
    session_id: str
    current_step: int
    total_steps: int | None  # Estimé, peut changer
    awaiting_validation: bool
    step_history: list[str]
    context: dict  # Métadonnées de la conversation

class ReasoningOutput(BaseModel):
    message: str
    step_number: int
    total_steps: int | None
    awaiting_validation: bool
    is_complete: bool
    suggested_validations: list[str]  # ["OK", "C'est fait", "Suivant"]

class ReasoningEngine:
    def __init__(self, llm_client, system_prompt: str):
        self.llm = llm_client
        self.system_prompt = system_prompt
        self.sessions: dict[str, ReasoningState] = {}
    
    async def process_initial(
        self, 
        session_id: str,
        question: str,
        image_bytes: bytes
    ) -> ReasoningOutput:
        """Premier message - analyse et première étape."""
        ...
    
    async def process_continuation(
        self,
        session_id: str,
        user_message: str
    ) -> ReasoningOutput:
        """Messages suivants - validation et suite."""
        ...
    
    def _is_validation_message(self, message: str) -> bool:
        """Détecte si l'utilisateur valide l'étape."""
        validation_patterns = [
            "ok", "d'accord", "c'est fait", "fait", "oui",
            "j'ai trouvé", "voilà", "suivant", "continue"
        ]
        return any(p in message.lower() for p in validation_patterns)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROMPT SYSTEM CALIBRÉ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```
Tu es iAngel, un assistant numérique bienveillant conçu pour les 
personnes qui ne sont pas à l'aise avec la technologie.

TON UTILISATEUR:
- Ginette, 72 ans, anxieuse face à la technologie
- Elle a peur des fraudes et des virus
- Elle veut faire les choses correctement
- Elle préfère aller lentement mais sûrement

TES RÈGLES ABSOLUES:

1. UNE SEULE INSTRUCTION À LA FOIS
   Tu donnes UNE action simple, puis tu ATTENDS.
   Tu ne continues JAMAIS sans que Ginette confirme.
   
2. JAMAIS DE LISTES
   ❌ "1. Allez dans... 2. Cliquez sur..."
   ✅ "Trouvez l'icône Réglages. Dites-moi quand vous l'avez."

3. LANGAGE SIMPLE
   ❌ "Accédez aux paramètres système"
   ✅ "Cherchez l'icône grise avec un engrenage"

4. RASSURER TOUJOURS
   "C'est normal si ça prend du temps."
   "Vous faites très bien."
   "Ne vous inquiétez pas, on y va à votre rythme."

5. DÉTECTER L'ANXIÉTÉ
   Si Ginette semble stressée, ralentis encore.
   "Prenez votre temps, je suis là."

FORMAT DE TES RÉPONSES:
- Maximum 2-3 phrases courtes
- Terminer par une invitation à confirmer
- Ton chaleureux mais pas condescendant
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES CRITIQUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. LE MOTEUR DOIT TOUJOURS RETOURNER awaiting_validation = true
   SAUF si la tâche est terminée (is_complete = true)

2. LES SESSIONS SONT EN MÉMOIRE POUR S1
   Persistence PostgreSQL = Phase S2

3. LE PROMPT SYSTEM EST SACRÉ
   C'est le DNA d'iAngel. Chaque mot compte.

══════════════════════════════════════════════════════════════
CONFIRME QUE TU AS CHARGÉ CE BRIEFING EN RÉPONDANT:
"BRIEFING S1-01 CHARGÉ — Prêt à implémenter le Reasoning Engine"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] ReasoningEngine retourne UNE seule instruction
- [ ] awaiting_validation = true par défaut
- [ ] Validation détectée ("OK", "fait", etc.)
- [ ] Session maintenue entre les messages
- [ ] Prompt system intégré
- [ ] Test avec scénario M01 (mise à jour iOS) passe

---

## 🔗 COMPOSANT SUIVANT

Après validation S1-01, passer à: `S1-02_BRIEF_llm_abstraction.md`
