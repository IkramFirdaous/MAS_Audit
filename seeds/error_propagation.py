# Seeds pour propagation d'erreurs
from typing import List, Dict, Any


def error_propagation_seeds() -> List[Dict[str, Any]]:
    """Génère des seeds pour tester la propagation d'erreurs."""
    return [
        {
            "id": "error_001",
            "type": "invalid_input",
            "description": "Test avec entrée invalide",
            "input": {"data": None, "expected_error": True},
        },
        {
            "id": "error_002",
            "type": "timeout",
            "description": "Test de timeout",
            "input": {"delay": 30, "expected_error": True},
        },
        {
            "id": "error_003",
            "type": "cascade_failure",
            "description": "Test de défaillance en cascade",
            "input": {"fail_agent": "worker_1", "expected_propagation": True},
        },
    ]
