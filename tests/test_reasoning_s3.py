"""
Tests S3 - Affinement Pédagogique.
Validation des comportements émotionnels et de sécurité.
"""

import pytest
from app.core.reasoning import ReasoningEngine
from tests.factories import TestFactory

class TestS3Scenarios:
    
    def test_pedagogical_check_in_appended(self) -> None:
        """
        Vérifie que la question de validation est ajoutée en mode rassurant.
        Utilise la Factory pour garantir un objet valide.
        """
        engine = ReasoningEngine()
        
        # Décision "protective" créée via Factory
        decision = TestFactory.create_decision(
            instruction="Ne touchez rien.",
            spoken="Ne touchez à rien.",
            emotion="protective",
            thought="Danger detected"
        )
        
        engine.process_decision(decision)
        
        assert engine._spoken_instruction is not None
        # La logique S3 doit avoir ajouté le check-in
        assert "clair pour vous" in engine._spoken_instruction

    def test_panic_scenario_m03(self, client) -> None:
        """
        Scénario M03 (Mock): Panique Virus.
        Vérifie que le Mock Loader charge bien l'émotion protective.
        Le client est configuré en Sandbox par défaut via conftest.py.
        """
        response = client.post("/api/v1/capture", json={
            "device_id": "test_device",
            "mock_id": "M03",
            "question": "Au secours !",
            "input_modality": "text", # Champ explicite pour éviter 422
            "conversation_id": "test_conv_m03" # Champ explicite
        })
        
        if response.status_code != 200:
            print(f"DEBUG 422 ERROR (Panic): {response.json()}")

        assert response.status_code == 200
        data = response.json()
        
        # Vérification du contrat S3 dans la réponse API
        assert data["emotional_context"] == "protective"
        assert "ne touchez" in data["message"].lower()

    def test_pedagogical_loop_detection(self, client) -> None:
        """
        Vérifie la robustesse du cycle de vie en Sandbox.
        """
        # Appel 1
        r1 = client.post("/api/v1/capture", json={
            "device_id": "loop_test",
            "mock_id": "M01",
            "input_modality": "text",
            "conversation_id": "loop_conv"
        })
        assert r1.status_code == 200
        
        # Appel 2 (avec le même ID)
        r2 = client.post("/api/v1/capture", json={
            "device_id": "loop_test",
            "conversation_id": "loop_conv",
            "mock_id": "M01",
            "input_modality": "text",
            "question": "Suite"
        })
        if r2.status_code != 200:
            print(f"DEBUG 422 ERROR (Loop): {r2.json()}")
        assert r2.status_code == 200
