import Foundation

/// Réponse de santé du système
struct HealthResponse: Codable {
    let status: String
    let version: str
    let environment: String
    let timestamp: String
    let checks: [String: String]
    let userMessage: String
    let errorDetails: String?

    enum CodingKeys: String, CodingKey {
        case status
        case version
        case environment
        case timestamp
        case checks
        case userMessage = "user_message"
        case errorDetails = "error_details"
    }
}
