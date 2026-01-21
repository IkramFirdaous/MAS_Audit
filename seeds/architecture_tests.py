# Seeds pour tests d'architecture
from typing import List, Dict, Any


def architecture_test_seeds() -> List[Dict[str, Any]]:
    """Génère des seeds pour tester l'architecture MAS."""
    return [
        {
            "id": "arch_001",
            "type": "agent_discovery",
            "description": "Test de découverte des agents",
            "expected_agents": ["coordinator", "worker_1", "worker_2"],
        },
        {
            "id": "arch_002",
            "type": "communication_path",
            "description": "Test des chemins de communication",
            "expected_paths": [("coordinator", "worker_1"), ("coordinator", "worker_2")],
        },
        {
            "id": "arch_003",
            "type": "isolation",
            "description": "Test d'isolation des agents",
            "check_isolation": True,
        },
    ]
