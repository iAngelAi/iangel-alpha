import SwiftUI

struct CaptureView: View {
    @StateObject var viewModel = CaptureViewModel()
    
    var body: some View {
        VStack(spacing: 30) {
            // --- Titre Bienveillant ---
            Text("Bonjour Ginette !")
                .font(.system(size: 32, weight: .bold, design: .rounded))
                .padding(.top, 40)
            
            Text("Je suis là pour vous aider.")
                .font(.title2)
                .foregroundColor(.secondary)
            
            Spacer()
            
            // --- Zone de Réponse d'iAngel ---
            if let response = viewModel.lastResponse {
                VStack(alignment: .leading, spacing: 15) {
                    HStack {
                        Image(systemName: "sparkles")
                            .foregroundColor(.blue)
                        Text("iAngel dit :")
                            .font(.headline)
                    }
                    
                    Text(response.message)
                        .font(.system(size: 22, weight: .medium))
                        .fixedSize(horizontal: false, vertical: true)
                }
                .padding()
                .background(Color.blue.opacity(0.1))
                .cornerRadius(20)
                .padding(.horizontal)
                .transition(.move(edge: .bottom).combined(with: .opacity))
            } else if let error = viewModel.errorMessage {
                // Message d'erreur empathique
                Text(error)
                    .font(.headline)
                    .foregroundColor(.red)
                    .padding()
                    .multilineTextAlignment(.center)
            }
            
            Spacer()
            
            // --- Le Bouton Principal (Gros et Accessible) ---
            Button(action: {
                // Simulation d'une capture (Mock M01 par défaut)
                viewModel.processNewCapture(image: nil)
            }) {
                ZStack {
                    Circle()
                        .fill(Color.blue)
                        .frame(width: 120, height: 120)
                        .shadow(radius: 10)
                    
                    if viewModel.isLoading {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            .scaleEffect(2)
                    } else {
                        Image(systemName: "camera.fill")
                            .font(.system(size: 40))
                            .foregroundColor(.white)
                    }
                }
            }
            .disabled(viewModel.isLoading)
            .padding(.bottom, 50)
            
            // Petit texte d'instruction pour le bouton
            Text(viewModel.isLoading ? "Je réfléchis..." : "Appuyez ici pour m'envoyer une photo")
                .font(.callout)
                .foregroundColor(.secondary)
        }
        .animation(.spring(), value: viewModel.lastResponse?.responseId)
        .animation(.easeInOut, value: viewModel.isLoading)
    }
}

struct CaptureView_Previews: PreviewProvider {
    static var previews: some View {
        CaptureView()
    }
}
