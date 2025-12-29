import Foundation
import SwiftUI

/// Gère l'état et la logique de l'écran de capture pour Ginette
class CaptureViewModel: ObservableObject {
    // --- États de l'UI ---
    @Published var lastResponse: CaptureResponse?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var showSuccessCelebration: Bool = false
    
    private let apiClient: iAngelAPIClient
    
    /// Initialisation avec injection du client API
    init(apiClient: iAngelAPIClient = iAngelAPIClient()) {
        self.apiClient = apiClient
    }
    
    /// Action principale : Envoyer une capture d'écran
    func processNewCapture(image: UIImage?, question: String? = nil, mockId: String = "M01") {
        // Déclenchement du chargement
        self.isLoading = true
        self.errorMessage = nil
        
        // Simulation d'encodage image (TODO réel: conversion base64)
        let base64Image = "FAKE_BASE64_FOR_S0" 
        
        let request = CaptureRequest(
            deviceId: UIDevice.current.identifierForVendor?.uuidString ?? "unknown_device",
            inputModality: .text, // Par défaut en texte pour S0
            question: question,
            conversationId: lastResponse?.conversationId, // Continuité de conversation
            mockId: mockId,
            imageData: base64Image
        )
        
        // Appel asynchrone au Backend
        Task {
            do {
                let response = try await apiClient.sendCapture(request: request)
                
                // Retour sur le thread principal pour mettre à jour l'UI
                await MainActor.run {
                    self.lastResponse = response
                    self.isLoading = false
                    
                    if response.isCompleted {
                        self.showSuccessCelebration = true
                    }
                }
            } catch let error as iAngelError {
                await MainActor.run {
                    self.isLoading = false
                    // iAngelError contient déjà des messages empathiques du backend
                    switch error {
                    case .requestFailed(_, let message):
                        self.errorMessage = message
                    default:
                        self.errorMessage = "Oups! J'ai un petit souci technique. On réessaie?"
                    }
                }
            } catch {
                await MainActor.run {
                    self.isLoading = false
                    self.errorMessage = "Une erreur imprévue est survenue. Vérifiez votre connexion."
                }
            }
        }
    }
    
    /// Efface l'état pour une nouvelle question
    func reset() {
        self.lastResponse = nil
        self.errorMessage = nil
        self.showSuccessCelebration = false
    }
}
