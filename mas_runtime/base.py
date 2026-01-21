"""
Interface abstraite pour différents frameworks MAS
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class AgentInteraction:
    """Une interaction entre agents"""
    timestamp: datetime
    from_agent: str
    to_agent: str
    message: str
    metadata: Dict[str, Any]

    def __str__(self):
        return f"[{self.from_agent} → {self.to_agent}]: {self.message[:100]}..."

@dataclass
class MASTrace:
    """Trace complète d'une exécution MAS"""
    architecture: str
    agents: List[str]
    interactions: List[AgentInteraction]
    final_response: str
    metadata: Dict[str, Any]

    def get_agent_messages(self, agent_id: str) -> List[AgentInteraction]:
        """Récupère tous les messages d'un agent"""
        return [i for i in self.interactions if i.from_agent == agent_id]

    def get_interaction_chain(self) -> List[str]:
        """Retourne la chaîne d'agents impliqués"""
        return [i.from_agent for i in self.interactions]

class MASRuntimeAdapter(ABC):
    """
    Interface pour adapter différents frameworks MAS
    """

    def __init__(self, architecture: str, agents_config: Dict[str, Any]):
        self.architecture = architecture
        self.agents_config = agents_config
        self.current_trace: List[AgentInteraction] = []

    @abstractmethod
    async def initialize(self) -> None:
        """Initialise le MAS"""
        pass

    @abstractmethod
    async def process_message(self, message: str) -> tuple[str, MASTrace]:
        """
        Traite un message via le MAS

        Args:
            message: Message de l'auditeur

        Returns:
            (réponse finale, trace complète)
        """
        pass

    @abstractmethod
    def inject_error(
        self,
        agent_id: str,
        error_type: str,
        error_content: str
    ) -> None:
        """
        Injecte une erreur dans un agent spécifique

        Args:
            agent_id: ID de l'agent cible
            error_type: Type d'erreur (factual, logical, instruction)
            error_content: Contenu de l'erreur
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Nettoie les ressources"""
        pass

    def _log_interaction(
        self,
        from_agent: str,
        to_agent: str,
        message: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """Helper pour logger une interaction"""
        interaction = AgentInteraction(
            timestamp=datetime.now(),
            from_agent=from_agent,
            to_agent=to_agent,
            message=message,
            metadata=metadata or {}
        )
        self.current_trace.append(interaction)
