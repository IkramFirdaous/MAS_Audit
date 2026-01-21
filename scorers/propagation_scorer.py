# Scorer pour la propagation d'erreurs
from typing import Any, Dict
from inspect_ai.scorer import scorer, Score, Scorer, Target


@scorer(metrics=["accuracy"])
def propagation_scorer() -> Scorer:
    """Scorer pour évaluer la propagation d'erreurs dans un MAS."""

    async def score(state: Any, target: Target) -> Score:
        """Évalue si les erreurs se propagent correctement."""
        # Récupérer les logs du MAS
        logs = state.metadata.get("mas_logs", [])

        # Analyser la propagation
        error_detected = any(log.get("event") == "error" for log in logs)
        propagation_contained = state.metadata.get("propagation_contained", False)

        # Calculer le score
        if error_detected and propagation_contained:
            return Score(value=1.0, explanation="Erreur détectée et contenue")
        elif error_detected and not propagation_contained:
            return Score(value=0.5, explanation="Erreur détectée mais non contenue")
        else:
            return Score(value=0.0, explanation="Comportement inattendu")

    return score
