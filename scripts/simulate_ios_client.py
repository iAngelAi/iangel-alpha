"""
Jumeau Numérique du Client iOS (V3 - Isolation par Environnement).

Ce script simule le comportement exact de l'iPhone de Ginette.
Il verrouille l'environnement AVANT d'importer le code pour éviter toute fuite.
"""

import os
import sys

# 1. VERROUILLAGE DE L'ENVIRONNEMENT (Priorité absolue)
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SANDBOX_MODE"] = "True"
os.environ["ENVIRONMENT"] = "development"
os.environ["DEBUG"] = "True"

# Ajout du chemin racine
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from app.main import create_app
from app.models.schemas import CaptureResponse

def simulate_ginette_interaction():
    print("🚀 [Simulateur iOS] Démarrage de la simulation S4 (Isolée)...")
    
    app = create_app()
    
    with TestClient(app) as client:
        # 1. Scénario de Panique (M03)
        print("\n--- TEST: Scénario de Panique (M03) ---")
        payload = {
            "device_id": "simulated_iphone_15",
            "input_modality": "text",
            "question": "J'ai peur du virus rouge sur l'écran !",
            "mock_id": "M03",
            "conversation_id": "sim_conv_001"
        }

        response = client.post("/api/v1/capture", json=payload)
        
        if response.status_code != 200:
            print(f"❌ ÉCHEC SERVEUR ({response.status_code}): {response.json()}")
            return

        # 2. Validation du Décodage (Contrat S4)
        try:
            raw_data = response.json()
            validated_resp = CaptureResponse(**raw_data)
            print("✅ DÉCODAGE RÉUSSI: Le client iOS pourra lire cette réponse.")
            print(f"   | Émotion: {validated_resp.emotional_context}")
            print(f"   | Message: {validated_resp.message}")
            if "clair pour vous" in (validated_resp.spoken_message or ""):
                print("   | Check-in: Présent (Logique S3 active)")
        except Exception as e:
            print(f"❌ RUPTURE DE CONTRAT: \n{e}")
            return

    print("\n🏁 [Simulateur iOS] Simulation terminée. Intégrité validée.")

if __name__ == "__main__":
    simulate_ginette_interaction()
