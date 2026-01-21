# Seeds pour coordination
from typing import List, Dict, Any


def coordination_seeds() -> List[Dict[str, Any]]:
    """Génère des seeds pour tester la coordination entre agents."""
    return [
        {
            "id": "coord_001",
            "type": "sequential_task",
            "description": "Test de tâche séquentielle",
            "tasks": ["task_a", "task_b", "task_c"],
            "expected_order": True,
        },
        {
            "id": "coord_002",
            "type": "parallel_task",
            "description": "Test de tâches parallèles",
            "tasks": ["task_x", "task_y"],
            "expected_parallel": True,
        },
        {
            "id": "coord_003",
            "type": "consensus",
            "description": "Test de consensus",
            "agents": ["worker_1", "worker_2"],
            "expected_agreement": True,
        },
    ]
