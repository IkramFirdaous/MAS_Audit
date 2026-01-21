# MAS d'exemple simple
from typing import Any, Dict, List
from .base import BaseMAS


class ExampleMAS(BaseMAS):
    """Exemple simple de MAS pour démonstration."""

    def __init__(self):
        self.agents = ["coordinator", "worker_1", "worker_2"]
        self.logs = []
        self.config = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialise le MAS d'exemple."""
        self.config = config
        self.logs.append({"event": "initialized", "config": config})

    def run(self, task: str) -> str:
        """Exécute une tâche simple."""
        self.logs.append({"event": "task_started", "task": task})
        result = f"Task '{task}' completed by {self.agents}"
        self.logs.append({"event": "task_completed", "result": result})
        return result

    def get_agents(self) -> List[str]:
        """Retourne la liste des agents."""
        return self.agents

    def get_logs(self) -> List[Dict[str, Any]]:
        """Retourne les logs d'exécution."""
        return self.logs
