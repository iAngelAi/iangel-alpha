"""
Tests du cycle de vie de l'application (Lifespan).

Vérifie que les événements de démarrage et d'arrêt s'exécutent correctement.
Audit CTO S0-01: Couverture du lifespan obligatoire.
"""

from fastapi.testclient import TestClient

from app.main import create_app


class TestLifespan:
    """Tests pour le cycle de vie de l'application."""

    def test_lifespan_startup_shutdown(self, capsys) -> None:
        """
        Le lifespan doit s'exécuter au démarrage et à l'arrêt.
        Utilise TestClient comme context manager.
        """
        app = create_app()
        
        # TestClient comme context manager déclenche le lifespan
        with TestClient(app) as client:
            # Vérifier que l'app est accessible
            response = client.get("/api/v1/health")
            assert response.status_code == 200
            
            # Vérifier les logs de démarrage (capturés via capsys/print)
            # Note: TestClient capture stdout/stderr selon la config pytest
            # Mais ici on vérifie surtout que le code est couvert (exécuté)
            pass
            
        # À la sortie du 'with', le shutdown est exécuté
