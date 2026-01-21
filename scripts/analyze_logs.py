# Analyse des résultats
"""
Script pour analyser les logs d'audit MAS.
"""

import json
import os
from typing import Dict, List, Any
from collections import defaultdict


def load_logs(log_dir: str = "logs") -> List[Dict[str, Any]]:
    """Charge tous les fichiers de logs."""
    logs = []

    if not os.path.exists(log_dir):
        print(f"Répertoire {log_dir} non trouvé.")
        return logs

    for filename in os.listdir(log_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(log_dir, filename)
            with open(filepath, "r") as f:
                logs.append(json.load(f))

    return logs


def analyze_logs(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyse les logs et génère des statistiques."""
    stats = {
        "total_tests": len(logs),
        "success_count": 0,
        "failure_count": 0,
        "error_types": defaultdict(int),
        "agent_failures": defaultdict(int),
    }

    for log in logs:
        if log.get("success", False):
            stats["success_count"] += 1
        else:
            stats["failure_count"] += 1
            error_type = log.get("error_type", "unknown")
            stats["error_types"][error_type] += 1

            failed_agent = log.get("failed_agent")
            if failed_agent:
                stats["agent_failures"][failed_agent] += 1

    return stats


def print_report(stats: Dict[str, Any]) -> None:
    """Affiche un rapport d'analyse."""
    print("=" * 60)
    print("  RAPPORT D'ANALYSE DES LOGS")
    print("=" * 60)

    print(f"\nTests totaux: {stats['total_tests']}")
    print(f"Succès: {stats['success_count']}")
    print(f"Échecs: {stats['failure_count']}")

    if stats["total_tests"] > 0:
        success_rate = (stats["success_count"] / stats["total_tests"]) * 100
        print(f"Taux de succès: {success_rate:.1f}%")

    if stats["error_types"]:
        print("\nTypes d'erreurs:")
        for error_type, count in stats["error_types"].items():
            print(f"  - {error_type}: {count}")

    if stats["agent_failures"]:
        print("\nÉchecs par agent:")
        for agent, count in stats["agent_failures"].items():
            print(f"  - {agent}: {count}")

    print("=" * 60)


def main():
    """Point d'entrée principal."""
    print("Analyse des logs d'audit MAS...\n")

    logs = load_logs()

    if not logs:
        print("Aucun log trouvé.")
        print("Exécutez d'abord un audit pour générer des logs.")
        return

    stats = analyze_logs(logs)
    print_report(stats)


if __name__ == "__main__":
    main()
