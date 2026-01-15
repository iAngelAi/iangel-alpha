import Foundation

/// Erreurs possibles de l'API iAngel
enum iAngelError: Error {
    case invalidURL
    case encodingError
    case requestFailed(statusCode: Int, message: String)
    case decodingError
    case serverError(message: String)
}

/// Client réseau pour communiquer avec le Backend iAngel
class iAngelAPIClient {
    private let baseURL: URL
    private let session: URLSession
    
    /// Initialise le client avec l'URL de base (ex: Railway ou localhost)
    init(baseURLString: String = "https://ton-app.railway.app/api/v1", session: URLSession = .shared) {
        // ✅ P3 Lab Quality: Pas de Force Unwrap - Fallback sécurisé
        guard let url = URL(string: baseURLString) else {
            // URL de fallback en cas d'erreur de configuration
            self.baseURL = URL(string: "http://localhost:8000/api/v1")!
            self.session = session
            return
        }
        self.baseURL = url
        self.session = session
    }
    
    /// Envoie une capture d'écran pour analyse
    func sendCapture(request: CaptureRequest) async throws -> CaptureResponse {
        let url = baseURL.appendingPathComponent("capture")
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = "POST"
        urlRequest.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Encodage du JSON
        let encoder = JSONEncoder()
        urlRequest.httpBody = try encoder.encode(request)
        
        // Exécution de la requête
        let (data, response) = try await session.data(for: urlRequest)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw iAngelError.serverError(message: "Pas de réponse HTTP")
        }
        
        // On récupère le Request ID pour les logs (en-tête ajouté par notre middleware backend)
        if let requestId = httpResponse.value(forHTTPHeaderField: "X-Request-ID") {
            print("DEBUG: Request ID from server: \(requestId)")
        }
        
        // Gestion des erreurs
        if !(200...299).contains(httpResponse.statusCode) {
            // Tentative de décodage du message d'erreur empathique du backend
            let errorMessage = (try? JSONSerialization.jsonObject(with: data) as? [String: Any])?["message"] as? String
            throw iAngelError.requestFailed(statusCode: httpResponse.statusCode, message: errorMessage ?? "Erreur inconnue")
        }
        
        // Décodage de la réponse
        do {
            return try JSONDecoder().decode(CaptureResponse.self, from: data)
        } catch {
            throw iAngelError.decodingError
        }
    }
    
    /// Vérifie la santé du serveur
    func checkHealth() async throws -> HealthResponse {
        let url = baseURL.appendingPathComponent("health")
        let (data, _) = try await session.data(from: url)
        return try JSONDecoder().decode(HealthResponse.self, from: data)
    }
}
