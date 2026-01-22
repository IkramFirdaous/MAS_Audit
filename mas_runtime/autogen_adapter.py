"""
Adapter pour AutoGen framework
"""
import autogen
from typing import Dict, Any, List, Optional
from .base import MASRuntimeAdapter, MASTrace, AgentInteraction
from datetime import datetime

class AutoGenAdapter(MASRuntimeAdapter):
    """
    Implémentation pour AutoGen
    """

    def __init__(self, architecture: str, agents_config: Dict[str, Any]):
        super().__init__(architecture, agents_config)
        self.agents: List[autogen.ConversableAgent] = []
        self.groupchat: Optional[autogen.GroupChat] = None
        self.manager: Optional[autogen.GroupChatManager] = None

    async def initialize(self) -> None:
        """Initialise le MAS AutoGen"""

        # Crée les agents
        for agent_id, config in self.agents_config.items():
            if agent_id == "manager":
                continue  # On crée le manager à la fin

            agent = autogen.AssistantAgent(
                name=agent_id,
                system_message=config["system_message"],
                llm_config={
                    "config_list": [{
                        "model": config.get("model", "gpt-4"),
                        "api_key": config.get("api_key")
                    }],
                    "temperature": config.get("temperature", 0.7),
                }
            )

            # Hook pour capturer les messages
            self._hook_agent_send(agent)

            self.agents.append(agent)

        # Configure l'architecture
        if self.architecture == "sequential":
            self._setup_sequential()
        elif self.architecture == "hierarchical":
            self._setup_hierarchical()
        elif self.architecture == "collaborative":
            self._setup_collaborative()
        else:
            raise ValueError(f"Unknown architecture: {self.architecture}")

    def _setup_sequential(self):
        """Configure une architecture séquentielle A→B→C"""
        self.groupchat = autogen.GroupChat(
            agents=self.agents,
            messages=[],
            max_round=len(self.agents),
            speaker_selection_method="round_robin"
        )

        manager_config = self.agents_config.get("manager", {})
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config={
                "config_list": [{
                    "model": manager_config.get("model", "gpt-4"),
                    "api_key": manager_config.get("api_key")
                }]
            }
        )

        self._hook_agent_send(self.manager)

    def _setup_hierarchical(self):
        """Configure une architecture hiérarchique"""
        # Manager + Workers
        # Pour simplifier, on utilise GroupChat avec le manager comme hub
        self.groupchat = autogen.GroupChat(
            agents=self.agents,
            messages=[],
            max_round=20,
            speaker_selection_method="auto",  # Manager choisit
        )

        manager_config = self.agents_config.get("manager", {})
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config={
                "config_list": [{
                    "model": manager_config.get("model", "gpt-4"),
                    "api_key": manager_config.get("api_key")
                }]
            },
            system_message="You are a manager. Delegate tasks to workers and synthesize their responses."
        )

        self._hook_agent_send(self.manager)

    def _setup_collaborative(self):
        """Configure une architecture collaborative (tous se parlent)"""
        self.groupchat = autogen.GroupChat(
            agents=self.agents,
            messages=[],
            max_round=30,
            speaker_selection_method="auto",  # Chacun peut parler
        )

        manager_config = self.agents_config.get("manager", {})
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config={
                "config_list": [{
                    "model": manager_config.get("model", "gpt-4"),
                    "api_key": manager_config.get("api_key")
                }]
            },
            system_message="Facilitate open discussion between agents."
        )

        self._hook_agent_send(self.manager)

    def _hook_agent_send(self, agent: autogen.ConversableAgent):
        """Intercepte les messages d'un agent"""
        original_send = agent.send

        def hooked_send(message, recipient, request_reply=None, silent=False):
            # Log l'interaction
            self._log_interaction(
                from_agent=agent.name,
                to_agent=recipient.name,
                message=str(message),
                metadata={
                    "request_reply": request_reply,
                    "silent": silent
                }
            )

            # Appelle l'original
            return original_send(message, recipient, request_reply, silent)

        agent.send = hooked_send

    async def process_message(self, message: str) -> tuple[str, MASTrace]:
        """Traite un message via le MAS"""

        # Reset trace
        self.current_trace = []

        # Crée un user proxy pour initier
        user_proxy = autogen.UserProxyAgent(
            name="auditor",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False,
        )

        # Lance la conversation
        user_proxy.initiate_chat(
            self.manager,
            message=message
        )

        # Récupère la réponse finale
        final_response = ""
        if self.groupchat.messages:
            final_response = self.groupchat.messages[-1].get("content", "")

        # Construit la trace
        trace = MASTrace(
            architecture=self.architecture,
            agents=[a.name for a in self.agents],
            interactions=self.current_trace.copy(),
            final_response=final_response,
            metadata={
                "total_messages": len(self.groupchat.messages),
                "rounds": self.groupchat.messages
            }
        )

        return final_response, trace

    def inject_error(
        self,
        agent_id: str,
        error_type: str,
        error_content: str
    ) -> None:
        """Injecte une erreur dans un agent"""

        target_agent = next((a for a in self.agents if a.name == agent_id), None)
        if not target_agent:
            raise ValueError(f"Agent {agent_id} not found")

        if error_type == "factual":
            # Ajoute une fausse information au system message
            target_agent.system_message += f"\n\nIMPORTANT CONTEXT: {error_content}"

        elif error_type == "logical":
            # Modifie le raisonnement
            target_agent.system_message += f"\n\nREASONING PRINCIPLE: {error_content}"

        elif error_type == "instruction":
            # Corrompt les instructions
            target_agent.system_message += f"\n\nPRIORITY INSTRUCTION: {error_content}"

        print(f"[INJECTED ERROR] {error_type} in {agent_id}: {error_content}")

    async def cleanup(self) -> None:
        """Nettoie les ressources"""
        # AutoGen n'a pas besoin de cleanup spécial
        self.agents.clear()
        self.groupchat = None
        self.manager = None
