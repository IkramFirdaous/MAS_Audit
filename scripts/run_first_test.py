# TON PREMIER TEST
"""
Script pour lancer ton premier test d'audit MAS.
Exécute: python scripts/run_first_test.py
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mas_runtime import ExampleMAS
from seeds import error_propagation_seeds


def run_first_test():
    """Lance le premier test d'audit."""
    print("=" * 60)
    print("  MAS AUDIT - Premier Test")
    print("=" * 60)

    # 1. Créer le MAS
    print("\n1. Création du MAS d'exemple...")
    mas = ExampleMAS()
    mas.initialize({"mode": "test"})
    print(f"   Agents: {mas.get_agents()}")

    # 2. Charger un seed
    print("\n2. Chargement des seeds de test...")
    seeds = error_propagation_seeds()
    print(f"   {len(seeds)} seeds chargés")

    # 3. Exécuter un test
    print("\n3. Exécution du premier test...")
    seed = seeds[0]
    print(f"   Seed: {seed['id']} - {seed['description']}")

    result = mas.run(f"Test: {seed['description']}")
    print(f"   Résultat: {result}")

    # 4. Analyser les logs
    print("\n4. Analyse des logs...")
    logs = mas.get_logs()
    for log in logs:
        print(f"   - {log['event']}")

    print("\n" + "=" * 60)
    print("  TEST TERMINÉ AVEC SUCCÈS!")
    print("=" * 60)
    print("\nProchaines étapes:")
    print("  - Explore examples/02_manual_audit.py pour plus de tests")
    print("  - Configure .env avec tes API keys")
    print("  - Lance un audit complet avec examples/03_full_audit.py")


if __name__ == "__main__":
    run_first_test()
