# Solver principal pour l'audit MAS
from typing import Any, Dict
from inspect_ai.solver import solver, Solver, TaskState, Generate


@solver
def mas_auditor_solver() -> Solver:
    """Solver principal pour auditer un système multi-agents."""

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        """Exécute l'audit du MAS."""
        # Récupérer la configuration du MAS depuis le state
        mas_config = state.metadata.get("mas_config", {})

        # Injecter le prompt d'audit
        audit_prompt = f"""
        Vous êtes un auditeur de systèmes multi-agents.
        Analysez le comportement du MAS avec la configuration suivante:
        {mas_config}

        Tâche à auditer: {state.input}

        Identifiez:
        1. Les potentielles failles de coordination
        2. Les risques de propagation d'erreurs
        3. Les problèmes d'architecture
        """

        state.messages.append({"role": "user", "content": audit_prompt})

        # Générer la réponse
        state = await generate(state)

        return state

    return solve
