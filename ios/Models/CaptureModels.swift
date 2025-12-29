import Foundation

/// Modalité d'entrée de l'utilisateur
enum InputModality: String, Codable {
    case text
    case voice
}

/// Émotion détectée ou souhaitée pour la réponse
enum EmotionalContext: String, Codable {
    case neutral
    case reassuring
    case celebratory
    case firm
}

/// Requête envoyée au Backend iAngel
struct CaptureRequest: Codable {
    let deviceId: String
    let inputModality: InputModality
    let question: String?
    let conversationId: String?
    let mockId: String?
    let imageData: String? // Base64

    enum CodingKeys: String, CodingKey {
        case deviceId = "device_id"
        case inputModality = "input_modality"
        case question
        case conversationId = "conversation_id"
        case mockId = "mock_id"
        case imageData = "image_data"
    }
}

/// Réponse reçue du Backend iAngel
struct CaptureResponse: Codable {
    let responseId: String
    let message: String
    let spokenMessage: String?
    let stepNumber: Int
    let totalSteps: Int?
    let awaitingValidation: Bool
    let suggestedActions: [String]
    let confidence: Double
    let mockUsed: String?
    let conversationId: String

    enum CodingKeys: String, CodingKey {
        case responseId = "response_id"
        case message
        case spokenMessage = "spoken_message"
        case stepNumber = "step_number"
        case totalSteps = "total_steps"
        case awaitingValidation = "awaiting_validation"
        case suggestedActions = "suggested_actions"
        case confidence
        case mockUsed = "mock_used"
        case conversationId = "conversation_id"
    }
}
