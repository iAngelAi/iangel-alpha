# 🔧 BRIEFING COMPOSANT S0-05
## Projet Xcode SwiftUI

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S0-05 |
| **Phase** | S0 — Walking Skeleton |
| **Composant** | Structure du projet iOS |
| **Priorité** | P0 (Critique) |
| **Dépendances** | Aucune côté iOS (parallèle à S0-01) |
| **Durée estimée** | 1-2 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S0-05 — PROJET XCODE SWIFTUI
══════════════════════════════════════════════════════════════

Tu vas créer la STRUCTURE INITIALE du projet iOS iAngel.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPÉCIFICATION COMPORTEMENTALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF:
Créer un projet Xcode SwiftUI avec:
1. Structure MVVM stricte
2. Configuration pour iOS 16+ (cible Ginette)
3. Architecture prête pour le déploiement TestFlight
4. Fichiers de base pour les fonctionnalités Alpha

CIBLE UTILISATEUR:
> Ginette, 72 ans, anxieuse face à la technologie.
> iPhone pas trop récent mais pas trop ancien (iOS 16+).
> Grandes polices, contrastes élevés, navigation simple.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTRAINTES ARCHITECTURALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STACK IMPOSÉE (ADR P3):
- SwiftUI (PAS UIKit sauf nécessité absolue)
- iOS 16.0+ minimum
- Architecture MVVM stricte
- Combine pour la réactivité
- async/await (PAS de callbacks)

STRUCTURE DE FICHIERS:
```
iAngel/
├── iAngel.xcodeproj
├── iAngel/
│   ├── iAngelApp.swift              # Point d'entrée
│   ├── ContentView.swift            # Vue racine
│   ├── Info.plist                   # Configuration
│   │
│   ├── App/
│   │   ├── AppState.swift           # État global
│   │   └── Configuration.swift      # URLs, constantes
│   │
│   ├── Features/
│   │   ├── Onboarding/              # Phase S2
│   │   │   ├── OnboardingView.swift
│   │   │   └── OnboardingViewModel.swift
│   │   │
│   │   ├── Capture/
│   │   │   ├── CaptureView.swift    # Écran principal
│   │   │   ├── CaptureViewModel.swift
│   │   │   └── CaptureButton.swift  # Bouton flottant
│   │   │
│   │   └── Conversation/
│   │       ├── ConversationView.swift
│   │       ├── ConversationViewModel.swift
│   │       └── MessageBubble.swift
│   │
│   ├── Services/
│   │   ├── APIClient.swift          # Communication backend
│   │   └── DeviceIdentifier.swift   # ID unique appareil
│   │
│   ├── Models/
│   │   ├── Message.swift            # Modèle message
│   │   ├── CaptureRequest.swift     # DTO requête
│   │   └── CaptureResponse.swift    # DTO réponse
│   │
│   ├── Components/
│   │   ├── LoadingView.swift        # "Je réfléchis..."
│   │   ├── ErrorView.swift          # Messages empathiques
│   │   └── PrimaryButton.swift      # Bouton accessible
│   │
│   ├── Extensions/
│   │   ├── Color+iAngel.swift       # Palette couleurs
│   │   └── Font+iAngel.swift        # Typographie accessible
│   │
│   └── Resources/
│       ├── Assets.xcassets          # Images, icônes
│       └── Localizable.strings      # Textes (FR uniquement Alpha)
│
└── iAngelTests/
    └── iAngelTests.swift
```

PATTERNS OBLIGATOIRES:
```swift
// MVVM STRICT — ViewModel injecté dans View
struct CaptureView: View {
    @StateObject private var viewModel = CaptureViewModel()
    // ...
}

// PAS DE FORCE UNWRAP
// ❌ let value = optional!
// ✅ guard let value = optional else { return }

// GESTION MÉMOIRE
// ✅ [weak self] dans les closures
Task { [weak self] in
    await self?.fetchData()
}

// ASYNC/AWAIT (PAS DE CALLBACKS)
// ✅ 
func fetchResponse() async throws -> CaptureResponse {
    // ...
}

// ❌
func fetchResponse(completion: @escaping (Result<CaptureResponse, Error>) -> Void) {
    // ...
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES CRITIQUES (À NE JAMAIS OUBLIER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. UTILISATEUR CIBLE: GINETTE (72 ans)
   > Accessibilité OBLIGATOIRE:
   > - Dynamic Type supporté
   > - Contrastes suffisants
   > - Tappable areas minimum 44x44 points
   > - VoiceOver friendly (accessibilityLabel sur les boutons)

2. PAS DE FORCE UNWRAP (`!`)
   > Chaque `!` est un crash potentiel pour Ginette.
   > Utilise `guard let`, `if let`, ou `??` (valeur par défaut).

3. GESTION D'ERREUR EMPATHIQUE
   > L'ErrorView ne montre JAMAIS de message technique.
   > "Oups, quelque chose s'est mal passé. On réessaie?"
   > PAS: "Error: URLSession task failed with error..."

4. CONFIGURATION EXTERNALISÉE
   > L'URL du backend NE DOIT PAS être hardcodée.
   > Utilise Configuration.swift avec possibilité de changer
   > entre dev/staging/prod.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONFIGURATION XCODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SETTINGS PROJET:
- Deployment Target: iOS 16.0
- Swift Language Version: 5.9
- Build Configuration: Debug + Release
- Code Signing: Automatic (Apple Development)

INFO.PLIST REQUIS:
```xml
<key>NSCameraUsageDescription</key>
<string>iAngel a besoin de prendre des captures pour vous aider.</string>

<key>UILaunchStoryboardName</key>
<string>LaunchScreen</string>

<key>UIRequiresFullScreen</key>
<true/>

<key>UISupportedInterfaceOrientations</key>
<array>
    <string>UIInterfaceOrientationPortrait</string>
</array>
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMAT DE RÉPONSE ATTENDU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pour les fichiers CRITIQUES (iAngelApp.swift, ContentView.swift, 
Configuration.swift, AppState.swift):
1. Code complet avec commentaires
2. Explication de 1 ligne du rôle

Pour les autres fichiers:
1. Structure avec TODO comments
2. Signature des classes/structs principales

À LA FIN:
- Instructions pour créer le projet dans Xcode
- Checklist de vérification (build, run on simulator)

══════════════════════════════════════════════════════════════
CONFIRME QUE TU AS CHARGÉ CE BRIEFING EN RÉPONDANT:
"BRIEFING S0-05 CHARGÉ — Prêt à créer le projet Xcode SwiftUI"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] Projet s'ouvre dans Xcode sans erreur
- [ ] Build réussit sur iOS Simulator
- [ ] Structure MVVM respectée
- [ ] Aucun `!` (force unwrap) dans le code
- [ ] Configuration.swift contient URL backend paramétrable
- [ ] Dynamic Type fonctionne (changer taille texte dans Settings)

---

## 🧪 TEST DE VALIDATION

```
1. Ouvrir iAngel.xcodeproj dans Xcode
2. Select iPhone 15 Pro Simulator
3. Cmd+R (Run)
4. App se lance sans crash
5. ContentView affiche "Hello iAngel" (placeholder)
```

---

## 🔗 COMPOSANT SUIVANT

Après validation S0-05, passer à: `S0-06_BRIEF_api_client_ios.md`
