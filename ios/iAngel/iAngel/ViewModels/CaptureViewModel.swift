import Foundation
import SwiftUI
import AVFoundation

/// Gère l'état et la logique de l'écran de capture pour Ginette
class CaptureViewModel: ObservableObject {
    // --- États de l'UI ---
    @Published var lastResponse: CaptureResponse?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var showSuccessCelebration: Bool = false
    
    private let apiClient: iAngelAPIClient
    private let speechSynthesizer = AVSpeechSynthesizer()
    
    /// Initialisation avec injection du client API
    init(apiClient: iAngelAPIClient = iAngelAPIClient()) {
        self.apiClient = apiClient
    }
    
    /// Action principale : Envoyer une capture d'écran
    func processNewCapture(image: UIImage?, question: String? = nil, mockId: String = "M01") {
        // Arrêter toute parole en cours si nouvelle action
        speechSynthesizer.stopSpeaking(at: .immediate)
        
        self.isLoading = true
        self.errorMessage = nil
        
        // Simulation d'encodage image (TODO réel: conversion base64)
        let base64Image = "FAKE_BASE64_FOR_S4" 
        
        let request = CaptureRequest(
            deviceId: UIDevice.current.identifierForVendor?.uuidString ?? "unknown_device",
            inputModality: .text,
            question: question,
            conversationId: lastResponse?.conversationId,
            mockId: mockId,
            imageData: base64Image
        )
        
        Task {
            do {
                let response = try await apiClient.sendCapture(request: request)
                
                await MainActor.run {
                    self.lastResponse = response
                    self.isLoading = false
                    
                    // Déclenchement TTS (Voix iAngel)
                    let textToSpeak = response.spokenMessage ?? response.message
                    self.speak(textToSpeak)
                    
                    if response.isCompleted {
                        self.showSuccessCelebration = true
                    }
                }
            } catch let error as iAngelError {
                await MainActor.run {
                    self.isLoading = false
                    switch error {
                    case .requestFailed(_, let message):
                        self.errorMessage = message
                    default:
                        self.errorMessage = "Oups! J'ai un petit souci technique. On réessaie?"
                    }
                    if let err = self.errorMessage { self.speak(err) }
                }
            } catch {
                await MainActor.run {
                    self.isLoading = false
                    self.errorMessage = "Une erreur imprévue est survenue."
                    self.speak(self.errorMessage!)
                }
            }
        }
    }
    
    /// Synthèse vocale apaisante pour Ginette
    private func speak(_ text: String) {
        let utterance = AVSpeechUtterance(string: text)
        
        // Configuration de la voix (Français - Canada si possible)
        utterance.voice = AVSpeechSynthesisVoice(language: "fr-CA") ?? AVSpeechSynthesisVoice(language: "fr-FR")
        
        // Vitesse réduite pour meilleure compréhension (0.4 - 0.5)
        utterance.rate = 0.45
        utterance.pitchMultiplier = 1.0
        utterance.volume = 1.0
        
        speechSynthesizer.speak(utterance)
    }
    
    func reset() {
        speechSynthesizer.stopSpeaking(at: .immediate)
        self.lastResponse = nil
        self.errorMessage = nil
        self.showSuccessCelebration = false
    }
}