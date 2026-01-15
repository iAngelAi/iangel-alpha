# 📱 GUIDE D'INTÉGRATION S1 - IOS CLIENT (iAngel)

**Date :** 13 Janvier 2026
**Version API :** 0.2.0-alpha (Phase S1 Complete)
**Statut :** 🟢 PRÊT POUR INTÉGRATION

---

## 1. Résumé Exécutif : "Le Cerveau s'éveille"

La Phase S1 a activé le **Moteur de Raisonnement** (Reasoning Engine) côté Backend.
Pour l'application iOS, cela signifie que Ginette n'est plus un simple perroquet. Elle "pense", a des émotions et propose des actions contextuelles.

**Impact Majeur :** L'interface utilisateur doit évoluer pour refléter cette intelligence.

---

## 2. Nouveaux Champs API (`CaptureResponse`)

L'endpoint `POST /api/v1/capture` retourne désormais un objet enrichi.
Votre modèle Swift `CaptureResponse` doit être mis à jour.

### Structure JSON Mise à Jour

```json
{
  "message": "Regardez le coin supérieur droit...",
  "spoken_message": "Regardez en haut à droite, vous voyez l'icône ?",
  "step_number": 1,
  "confidence": 0.9,
  "conversation_id": "conv_123",
  
  // === NOUVEAUX CHAMPS S1 ===
  "emotional_context": "reassuring",
  "suggested_actions": ["Je vois l'icône", "Je ne trouve pas"],
  "thought_process": "L'utilisateur semble perdu. Je simplifie l'étape."
}
```

### Détail des Champs

| Champ | Type | Description & Usage iOS |
|-------|------|-------------------------|
| **`spoken_message`** | `String` | **PRIORITÉ 1.** Texte optimisé pour le TTS (Synthèse vocale). Plus court, plus naturel. *Utilisez ce champ pour la voix d'iAngel.* |
| **`emotional_context`** | `Enum` | Indique le ton à adopter (Avatar/Voix/Couleur).<br>Valeurs : `neutral` (défaut), `reassuring` (bleu doux), `celebratory` (confettis/or), `firm` (ROUGE/Alerte sécurité). |
| **`suggested_actions`** | `[String]` | **CRITIQUE.** Liste des boutons de réponse à afficher en bas d'écran. Ne laissez plus l'utilisateur deviner quoi dire. |
| **`thought_process`** | `String` | *Debug Only.* Le raisonnement interne de l'IA. Peut être affiché dans une vue "Développeur" pour comprendre la logique. |

---

## 3. Directives UX / UI (Mandat Ginette)

### A. Gestion de l'Émotion (`emotional_context`)
*   **`neutral`** : Comportement standard.
*   **`reassuring`** : Si détecté, ralentir le débit vocal (TTS) légèrement. Afficher une icône apaisante.
*   **`firm` (DANGER)** :
    *   **Action :** Couper tout autre son.
    *   **Visuel :** Bordure rouge ou fond d'alerte.
    *   **Haptic :** Vibration distincte.
    *   **Usage :** Utilisé pour empêcher Ginette de cliquer sur un lien phishing.

### B. Boutons d'Action (`suggested_actions`)
*   Au lieu d'attendre passivement une réponse vocale, affichez ces suggestions sous forme de gros boutons lisibles.
*   Si la liste est vide (cas rare), affichez un bouton par défaut "J'ai fait cela".
*   Si `suggested_actions` contient "Je ne trouve pas" ou "Aide", mettez ce bouton en évidence (couleur secondaire).

### C. Voix vs Texte
*   Affichez `message` (texte complet) dans la bulle de chat.
*   Faites lire `spoken_message` (texte conversationnel) par le TTS.
*   *Pourquoi ?* Le texte écrit doit être précis ("Appuyez sur 'Réglages'"), le texte oral doit être fluide ("Appuie sur le bouton Réglages").

---

## 4. Scénarios de Test (Sandbox)

Utilisez ces IDs de mock pour tester votre UI sans dépenser de crédits LLM :

*   **`M01` (WiFi)** : Test du flux `reassuring`. Vérifiez que les boutons ["Je vois l'icône", "Je ne trouve pas"] s'affichent.
*   **`M02` (Phishing)** : Test du flux `firm`. Vérifiez l'alerte rouge et le ton impératif.

---

*Fin du Brief Technique S1.*
