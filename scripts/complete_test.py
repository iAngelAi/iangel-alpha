import os
import asyncio
from dotenv import load_dotenv
from app.services.capture_service import CaptureService, CaptureRequest
from app.core.state import InMemoryStateStore

async def test_full_logic():
    print("🧠 Test Standalone du Cerveau S1 (Haiku)")
    load_dotenv()
    
    # On force le mode réel
    os.environ["SANDBOX_MODE"] = "false"
    
    # Initialisation du service (avec injection manuelle pour être sûr)
    service = CaptureService()
    service.settings.sandbox_mode = False
    
    conv_id = "test_standalone_process"
    
    # --- TOUR 1 ---
    print("\n--- TOUR 1 : Demande WiFi ---")
    req1 = CaptureRequest(
        device_id="standalone_dev",
        conversation_id=conv_id,
        question="Aide-moi à me connecter au WiFi."
    )
    resp1 = await service.process_capture(req1)
    print(f"iAngel dit : {resp1.message}")
    
    # --- TOUR 2 ---
    print("\n--- TOUR 2 : Ginette dit 'C'est fait' ---")
    req2 = CaptureRequest(
        device_id="standalone_dev",
        conversation_id=conv_id,
        question="C'est fait, je vois les noms des réseaux."
    )
    resp2 = await service.process_capture(req2)
    print(f"iAngel dit : {resp2.message}")
    
    if resp1.message != resp2.message:
        print("\n✅ SUCCÈS : L'historique a été pris en compte !")
    else:
        print("\n❌ ÉCHEC : Répétition du message.")

if __name__ == "__main__":
    asyncio.run(test_full_logic())
