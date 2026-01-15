# 🔧 BRIEFING COMPOSANT S0-06
## APIClient iOS

---

## 📋 MÉTADONNÉES

| Attribut | Valeur |
|----------|--------|
| **ID** | S0-06 |
| **Phase** | S0 — Walking Skeleton |
| **Composant** | Client HTTP pour communication backend |
| **Priorité** | P0 (Critique) |
| **Dépendances** | S0-05 (Projet Xcode) |
| **Durée estimée** | 1-2 heures |

---

## 🎯 COPIER CE BLOC DANS UNE NOUVELLE CONVERSATION CLAUDE

```
══════════════════════════════════════════════════════════════
BRIEFING S0-06 — APICLIENT iOS
══════════════════════════════════════════════════════════════

Tu vas implémenter le CLIENT API du projet iOS iAngel.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPÉCIFICATION COMPORTEMENTALE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OBJECTIF:
Créer un APIClient qui:
1. Communique avec le backend FastAPI sur Railway
2. Envoie les requêtes /capture
3. Gère les erreurs de manière empathique
4. Supporte retry automatique sur timeout

ENDPOINTS À SUPPORTER:
| Endpoint | Méthode | Phase |
|----------|---------|-------|
| /health | GET | S0 |
| /api/v1/capture | POST | S0 |
| /api/v1/converse | POST | S1 |

COMPORTEMENT ATTENDU:
```swift
let client = APIClient.shared

// Health check
let isHealthy = await client.checkHealth()
// -> true/false

// Capture (skeleton)
let response = try await client.sendCapture(
    question: "C'est tu un virus?",
    mockId: "M02"
)
// -> CaptureResponse

// Gestion d'erreur
do {
    let response = try await client.sendCapture(...)
} catch APIError.networkUnavailable {
    // Message: "Pas de connexion internet..."
} catch APIError.serverError {
    // Message: "Je réfléchis plus fort que d'habitude..."
} catch APIError.timeout {
    // Retry automatique déjà fait, message final
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTRAINTES ARCHITECTURALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STACK IMPOSÉE:
- URLSession natif (PAS Alamofire)
- async/await (PAS de callbacks)
- Codable pour JSON encoding/decoding
- Combine pour les Publishers (optionnel S0)

FICHIERS À CRÉER:
```
iAngel/
├── Services/
│   ├── APIClient.swift          # Client principal
│   ├── APIError.swift           # Enum erreurs typées
│   └── DeviceIdentifier.swift   # Génère device_id unique
├── Models/
│   ├── CaptureRequest.swift     # DTO sortant
│   └── CaptureResponse.swift    # DTO entrant
```

MODÈLES (Codable):
```swift
// CaptureRequest.swift
struct CaptureRequest: Codable {
    let deviceId: String
    let question: String
    let mockId: String
    let imageData: String?  // Base64, ignoré par backend (P4)
    
    enum CodingKeys: String, CodingKey {
        case deviceId = "device_id"
        case question
        case mockId = "mock_id"
        case imageData = "image_data"
    }
}

// CaptureResponse.swift
struct CaptureResponse: Codable {
    let responseId: String
    let message: String
    let stepNumber: Int
    let totalSteps: Int?
    let awaitingValidation: Bool
    let suggestedActions: [String]
    let confidence: Double
    let mockUsed: String?
    
    enum CodingKeys: String, CodingKey {
        case responseId = "response_id"
        case message
        case stepNumber = "step_number"
        case totalSteps = "total_steps"
        case awaitingValidation = "awaiting_validation"
        case suggestedActions = "suggested_actions"
        case confidence
        case mockUsed = "mock_used"
    }
}
```

ENUM ERREURS:
```swift
// APIError.swift
enum APIError: Error, LocalizedError {
    case networkUnavailable
    case timeout
    case serverError(statusCode: Int)
    case decodingError
    case invalidURL
    case unknown(Error)
    
    var errorDescription: String? {
        // Messages EMPATHIQUES pour Ginette
        switch self {
        case .networkUnavailable:
            return "Je n'arrive pas à me connecter. Vérifiez votre WiFi?"
        case .timeout:
            return "Ça prend un peu plus de temps que prévu..."
        case .serverError:
            return "J'ai un petit souci technique. On réessaie?"
        case .decodingError:
            return "J'ai reçu une réponse bizarre. Un instant..."
        case .invalidURL:
            return "Je me suis perdue. Pouvez-vous réessayer?"
        case .unknown:
            return "Quelque chose s'est mal passé. On réessaie?"
        }
    }
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CONTRAINTES CRITIQUES (À NE JAMAIS OUBLIER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. UTILISATEUR CIBLE: GINETTE (72 ans)
   > Les messages d'erreur sont dans APIError.errorDescription.
   > Ils doivent être EMPATHIQUES et NON TECHNIQUES.
   > PAS: "HTTP 500" / OUI: "J'ai un petit souci..."

2. RETRY AUTOMATIQUE
   > Sur timeout ou erreur 5xx, retry 3 fois avec backoff:
   > - 1ère tentative: immédiat
   > - 2ème: après 1 seconde
   > - 3ème: après 3 secondes
   > Après 3 échecs, propager l'erreur.

3. TIMEOUT GÉNÉREUX
   > Ginette est patiente. Timeout = 30 secondes.
   > Claude peut prendre du temps à répondre.

4. DEVICE ID PERSISTANT
   > DeviceIdentifier génère un UUID unique stocké dans Keychain.
   > JAMAIS de données personnelles (pas de nom, pas d'email).

5. PAS DE FORCE UNWRAP
   > Toute response du backend peut être malformée.
   > Utilise try? ou do/catch, JAMAIS de force unwrap.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTERFACE APIClient
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```swift
// APIClient.swift
final class APIClient {
    static let shared = APIClient()
    
    private let session: URLSession
    private let baseURL: URL
    private let deviceId: String
    private let maxRetries = 3
    
    private init() {
        // Configuration depuis Configuration.swift
        // Session avec timeout 30s
    }
    
    // MARK: - Public Methods
    
    /// Vérifie si le backend est accessible
    func checkHealth() async -> Bool {
        // GET /health
    }
    
    /// Envoie une capture pour analyse
    func sendCapture(
        question: String,
        mockId: String = "M01",
        imageData: String? = nil
    ) async throws -> CaptureResponse {
        // POST /api/v1/capture
        // Avec retry automatique
    }
    
    // MARK: - Private Methods
    
    private func performRequest<T: Decodable>(
        _ request: URLRequest,
        responseType: T.Type,
        retryCount: Int = 0
    ) async throws -> T {
        // Logique de retry avec backoff
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
- Exemple d'utilisation dans un ViewModel
- Test unitaire pour retry logic

══════════════════════════════════════════════════════════════
CONFIRME QUE TU AS CHARGÉ CE BRIEFING EN RÉPONDANT:
"BRIEFING S0-06 CHARGÉ — Prêt à implémenter APIClient iOS"
══════════════════════════════════════════════════════════════
```

---

## ✅ CRITÈRES D'ACCEPTATION

- [ ] APIClient.shared.checkHealth() retourne Bool
- [ ] APIClient.shared.sendCapture() retourne CaptureResponse
- [ ] Retry automatique sur timeout (3 fois)
- [ ] Messages d'erreur empathiques (pas de HTTP 500)
- [ ] DeviceIdentifier génère UUID persistant
- [ ] Timeout configuré à 30 secondes

---

## 🧪 TEST DE VALIDATION

```swift
// Test dans un Preview ou Unit Test
Task {
    // 1. Health check
    let isHealthy = await APIClient.shared.checkHealth()
    print("Backend healthy: \(isHealthy)")
    
    // 2. Capture
    do {
        let response = try await APIClient.shared.sendCapture(
            question: "C'est tu un virus?",
            mockId: "M02"
        )
        print("Response: \(response.message)")
    } catch {
        print("Error: \(error.localizedDescription)")
    }
}
```

---

## 🔗 COMPOSANT SUIVANT

Après validation S0-06, passer à: `S0-07_BRIEF_ui_skeleton.md`
