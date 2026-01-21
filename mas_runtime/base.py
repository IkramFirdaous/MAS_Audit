# Interface abstraite pour MAS Runtime
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseMAS(ABC):
    """Interface abstraite pour les systèmes multi-agents."""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialise le système multi-agents."""
        pass

    @abstractmethod
    def run(self, task: str) -> str:
        """Exécute une tâche et retourne le résultat."""
        pass

    @abstractmethod
    def get_agents(self) -> List[str]:
        """Retourne la liste des agents."""
        pass

    @abstractmethod
    def get_logs(self) -> List[Dict[str, Any]]:
        """Retourne les logs d'exécution."""
        pass
