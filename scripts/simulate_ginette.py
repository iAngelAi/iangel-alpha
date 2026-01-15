import httpx
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"
CONV_ID = "test_ginette_session"

def print_step(title):
    print(f"\n--- {title} ---")

def simulate_dialogue():
    print("🚀 Démarrage de la simulation Ginette (S1)")
    
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        
        # --- TOUR 1 : La capture initiale ---
        print_step("TOUR 1 : Envoi de la capture (WiFi)")
        payload1 = {
            "device_id": "sim_device_001",
            "conversation_id": CONV_ID,
            "mock_id": "M01",
            "question": "Je n'ai plus internet, aide-moi."
        }
        resp1 = client.post("/capture", json=payload1)
        data1 = resp1.json()
        print(f"iAngel dit : {data1['message']}")
        print(f"Request ID : {resp1.headers.get('X-Request-ID')}")
        
        time.sleep(1)
        
        # --- TOUR 2 : Ginette valide l'étape ---
        print_step("TOUR 2 : Ginette dit 'C'est fait'")
        payload2 = {
            "device_id": "sim_device_001",
            "conversation_id": CONV_ID,
            "question": "C'est fait, je vois une liste de noms maintenant."
        }
        # Note : On n'envoie plus de mock_id ici, on veut voir si le cerveau suit
        resp2 = client.post("/capture", json=payload2)
        data2 = resp2.json()
        print(f"iAngel dit : {data2['message']}")
        
        # --- TOUR 3 : Vérification de la mémoire ---
        print_step("VÉRIFICATION : Historique")
        # On va regarder les logs ou un endpoint de debug si on en avait un
        # Mais ici on vérifie juste que data2 est différent de data1
        if data1['message'] != data2['message']:
            print("✅ SUCCÈS : iAngel a évolué dans la conversation !")
        else:
            print("❌ ÉCHEC : iAngel répète la même chose (Amnésie).")

if __name__ == "__main__":
    try:
        simulate_dialogue()
    except Exception as e:
        print(f"❌ Erreur de simulation : {e}")
