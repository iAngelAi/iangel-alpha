"""
Tests de l'endpoint /capture et du service associé.

Vérifie le flux complet de traitement d'une capture (Happy Path).
"""

from fastapi import status

class TestCaptureEndpoint:
    """Tests pour POST /api/v1/capture."""

    def test_capture_happy_path(self, client) -> None:
        """
        Test du flux nominal (Happy Path).
        
        Vérifie que:
        1. L'endpoint accepte une requête valide.
        2. Le service est appelé (via l'intégration).
        3. La réponse est bien formatée (CaptureResponse).
        """
        payload = {
            "device_id": "test_device_123",
            "image_data": "base64_fake_image_data",
            "question": "C'est quoi ça?",
            "mock_id": "M01"
        }

        response = client.post("/api/v1/capture", json=payload)

        # Vérification du statut
        assert response.status_code == status.HTTP_200_OK

        # Vérification du contenu
        data = response.json()
        assert "message" in data
        assert "step_number" in data
        assert data["step_number"] == 1
        
        # Vérification que le mock_id est bien passé
        assert data["mock_used"] == "M01"
        
        # Vérification que le message vient bien du MockLoader (Preuve d'intégration)
        assert "icône WiFi" in data["message"]
        
        # Vérification du mode vocal (nouveau champ)
        assert "spoken_message" in data
        assert "WiFi" in data["spoken_message"]
        
        # Vérification des en-têtes (Robustesse)
        assert "X-Request-ID" in response.headers

    def test_capture_voice_input_accepted(self, client) -> None:
        """Vérifie que l'API accepte une modalité 'voice'."""
        payload = {
            "device_id": "dev123",
            "input_modality": "voice",
            "mock_id": "M02"
        }

        response = client.post("/api/v1/capture", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "suspect" in data["spoken_message"]
