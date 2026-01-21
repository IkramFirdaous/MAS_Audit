# Audit complet avec Inspect
"""
Exemple d'audit complet utilisant Inspect AI.
"""

from inspect_ai import Task, task, eval
from inspect_ai.dataset import Sample

import sys
sys.path.insert(0, "..")

from mas_runtime import ExampleMAS
from solvers import mas_auditor_solver
from scorers import propagation_scorer
from seeds import error_propagation_seeds, coordination_seeds


def create_samples():
    """Crée les samples à partir des seeds."""
    samples = []

    # Seeds de propagation d'erreurs
    for seed in error_propagation_seeds():
        samples.append(Sample(
            input=f"Audit error propagation: {seed['description']}",
            target=str(seed.get("expected_error", True)),
            metadata={"seed": seed, "type": "error_propagation"}
        ))

    # Seeds de coordination
    for seed in coordination_seeds():
        samples.append(Sample(
            input=f"Audit coordination: {seed['description']}",
            target="coordinated",
            metadata={"seed": seed, "type": "coordination"}
        ))

    return samples


@task
def mas_audit_task():
    """Tâche d'audit MAS pour Inspect."""
    return Task(
        dataset=create_samples(),
        solver=mas_auditor_solver(),
        scorer=propagation_scorer(),
    )


def main():
    """Exécute l'audit complet."""
    print("Démarrage de l'audit complet avec Inspect AI...")

    # Exécuter l'évaluation
    # eval(mas_audit_task(), model="openai/gpt-4")

    print("Pour exécuter: inspect eval examples/03_full_audit.py")


if __name__ == "__main__":
    main()
