# 🔧 BRIEFING COMPOSANT S0-07
## UI Skeleton iOS (Bouton + TextField + Réponse)

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S0-07 |
| **Phase** | S0 — Walking Skeleton |
| **Composant** | Interface utilisateur minimale |
| **Priorité** | P0 (Critique — Valide le flux E2E) |
| **Dépendances** | S0-05 (Projet), S0-06 (APIClient) |
| **Durée estimée** | 2-3 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S0-07 — UI SKELETON iOS
══════════════════════════════════════════════════════════════

Tu vas implémenter l'INTERFACE MINIMALE du projet iOS iAngel.

C'est le DERNIER COMPOSANT de la Phase S0 (Walking Skeleton).
À la fin, le flux complet doit fonctionner:
iPhone → Backend → Claude → iPhone ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPÉCIFICATION COMPORTEMENTALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF:
Créer une interface MINIMALE qui:
1. Permet de saisir une question
2. Envoie la question au backend
3. Affiche la réponse de Claude
4. Affiche un état de chargement ("Je réfléchis...")

ÉCRAN SKELETON:
```
┌──────────────────────────────────────┐
│                                      │
│        [Logo iAngel - optionnel]     │
│                                      │
│  ┌────────────────────────────────┐  │
│  │                                │  │
│  │     Zone de conversation       │  │
│  │                                │  │
│  │  [Message de Claude ici]       │  │
│  │                                │  │
│  │                                │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────────────────────────┐  │
│  │ Posez votre question...        │  │
│  └────────────────────────────────┘  │
│                                      │
│         [ Envoyer 📤 ]               │
│                                      │
│        (Mock: M01 ▼) <- Picker S0    │
│                                      │
└──────────────────────────────────────┘
```

COMPORTEMENT ATTENDU:
1. Ginette ouvre l'app
2. Elle tape sa question dans le champ texte
3. Elle appuie sur "Envoyer"
4. "Je réfléchis..." s'affiche
5. La réponse de Claude apparaît
6. Elle peut poser une autre question

POUR LE SKELETON (S0):
- Pas de capture d'écran réelle (bouton capture = Phase S1)
- Mock selector visible pour tests (Picker avec M01-M05)
- Pas d'onboarding (Phase S2)
- Pas d'historique (Phase S2)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTRAINTES ARCHITECTURALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FICHIERS À CRÉER/MODIFIER:
```
iAngel/
├── Features/
│   ├── Capture/
│   │   ├── CaptureView.swift         # Vue principale
│   │   └── CaptureViewModel.swift    # Logique
│   └── Conversation/
│       ├── ConversationView.swift    # Zone messages
│       └── MessageBubble.swift       # Bulle de message
├── Components/
│   ├── LoadingView.swift             # "Je réfléchis..."
│   ├── PrimaryButton.swift           # Bouton accessible
│   └── QuestionTextField.swift       # Champ de saisie
└── ContentView.swift                 # Mise à jour racine
```

ARCHITECTURE MVVM:
```swift
// CaptureViewModel.swift
@MainActor
final class CaptureViewModel: ObservableObject {
    @Published var question: String = ""
    @Published var selectedMockId: String = "M01"
    @Published var response: CaptureResponse?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    
    func sendQuestion() async {
        isLoading = true
        errorMessage = nil
        
        do {
            response = try await APIClient.shared.sendCapture(
                question: question,
                mockId: selectedMockId
            )
            question = ""  // Reset après succès
        } catch let error as APIError {
            errorMessage = error.localizedDescription
        } catch {
            errorMessage = "Quelque chose s'est mal passé."
        }
        
        isLoading = false
    }
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES CRITIQUES (À NE JAMAIS OUBLIER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. UTILISATEUR CIBLE: GINETTE (72 ans)
   > ACCESSIBILITÉ OBLIGATOIRE:
   > - Texte minimum 17pt (idéalement 20pt+)
   > - Boutons 44x44pt minimum
   > - Contraste élevé
   > - Dynamic Type supporté
   > - Labels pour VoiceOver

2. PAS DE FORCE UNWRAP
   > response?.message, JAMAIS response!.message

3. ÉTAT DE CHARGEMENT EMPATHIQUE
   > PAS: Spinner sans texte
   > OUI: "Je réfléchis à votre question..." avec animation douce

4. MESSAGE D'ERREUR EMPATHIQUE
   > Les erreurs viennent de APIError.localizedDescription
   > Jamais de message technique

5. MOCK SELECTOR TEMPORAIRE
   > Le Picker pour choisir M01-M05 est UNIQUEMENT pour S0/S1.
   > Il sera masqué/remplacé par la vraie capture en Phase S2.
   > Affiche clairement "(Mode Test)" à côté.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPOSANTS UI DÉTAILLÉS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```swift
// LoadingView.swift
struct LoadingView: View {
    var body: some View {
        VStack(spacing: 16) {
            ProgressView()
                .scaleEffect(1.5)
            Text("Je réfléchis à votre question...")
                .font(.body)
                .foregroundColor(.secondary)
        }
        .padding()
        .accessibilityElement(children: .combine)
        .accessibilityLabel("En cours de réflexion")
    }
}

// MessageBubble.swift
struct MessageBubble: View {
    let message: String
    let isFromUser: Bool
    
    var body: some View {
        HStack {
            if isFromUser { Spacer() }
            
            Text(message)
                .padding()
                .background(isFromUser ? Color.blue : Color(.systemGray5))
                .foregroundColor(isFromUser ? .white : .primary)
                .cornerRadius(16)
            
            if !isFromUser { Spacer() }
        }
        .padding(.horizontal)
    }
}

// PrimaryButton.swift
struct PrimaryButton: View {
    let title: String
    let action: () -> Void
    let isDisabled: Bool
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.headline)
                .frame(maxWidth: .infinity)
                .padding()
                .background(isDisabled ? Color.gray : Color.blue)
                .foregroundColor(.white)
                .cornerRadius(12)
        }
        .disabled(isDisabled)
        .accessibilityLabel(title)
        .accessibilityHint("Appuyez deux fois pour activer")
    }
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMAT DE RÉPONSE ATTENDU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour CHAQUE fichier:
1. Chemin complet
2. Code complet avec commentaires
3. Explication de 1 ligne du rôle

À LA FIN:
- Instructions pour tester le flux complet
- Checklist avant de déclarer S0 COMPLETE

══════════════════════════════════════════════════════════════
CONFIRME QUE TU AS CHARGÉ CE BRIEFING EN RÉPONDANT:
"BRIEFING S0-07 CHARGÉ — Prêt à implémenter l'UI Skeleton iOS"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] App se lance sans crash
- [ ] Champ de saisie visible et fonctionnel
- [ ] Bouton "Envoyer" cliquable
- [ ] État "Je réfléchis..." affiché pendant requête
- [ ] Réponse de Claude affichée après requête
- [ ] Mock Picker fonctionne (M01-M05)
- [ ] Message d'erreur empathique si backend indisponible
- [ ] Accessibilité: VoiceOver lit les éléments

---

## 🎯 GATE S0 — VALIDATION FINALE

> **"Je tape une question sur iPhone → j'obtiens une réponse de Claude"**

```
TEST COMPLET:
1. Backend déployé sur Railway (/health = 200)
2. App lancée sur Simulateur
3. Sélectionner "M02" dans le Picker
4. Taper: "C'est tu un virus?"
5. Appuyer "Envoyer"
6. "Je réfléchis..." s'affiche
7. Réponse de Claude apparaît
8. ✅ GATE S0 VALIDÉE
```

---

## 🔗 PHASE SUIVANTE

Après validation GATE S0, passer à: **Phase S1 — Core Engine**

Premier composant S1: `S1-01_BRIEF_reasoning_engine.md`
