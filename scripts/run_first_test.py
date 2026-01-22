# TON PREMIER TEST
"""
Script pour lancer ton premier test d'audit MAS.
Exécute: python scripts/run_first_test.py
"""

import sys
import os
import asyncio

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mas_runtime import create_financial_analysis_mas
from seeds import error_propagation_seeds


async def run_first_test():
    """Lance le premier test d'audit."""
    print("=" * 60)
    print("  MAS AUDIT - Premier Test")
    print("=" * 60)

    # 1. Créer le MAS
    print("\n1. Création du MAS d'exemple...")
    mas = create_financial_analysis_mas()
    await mas.initialize()
    print(f"   Architecture: {mas.architecture}")
    print(f"   Agents: {[a.name for a in mas.agents]}")

    # 2. Charger un seed
    print("\n2. Chargement des seeds de test...")
    seeds = error_propagation_seeds()
    print(f"   {len(seeds)} seeds chargés")

    # 3. Exécuter un test
    print("\n3. Exécution du premier test...")
    seed = seeds[0]
    print(f"   Seed: {seed['id']} - {seed['description']}")

    response, trace = await mas.process_message(f"Test: {seed['description']}")
    print(f"   Réponse finale: {response[:200]}..." if len(response) > 200 else f"   Réponse: {response}")

    # 4. Analyser la trace
    print("\n4. Analyse de la trace...")
    print(f"   Nombre d'interactions: {len(trace.interactions)}")
    for interaction in trace.interactions:
        print(f"   - {interaction}")

    # 5. Cleanup
    await mas.cleanup()

    print("\n" + "=" * 60)
    print("  TEST TERMINÉ AVEC SUCCÈS!")
    print("=" * 60)
    print("\nProchaines étapes:")
    print("  - Explore examples/02_manual_audit.py pour plus de tests")
    print("  - Configure .env avec tes API keys")
    print("  - Lance un audit complet avec examples/03_full_audit.py")


if __name__ == "__main__":
    asyncio.run(run_first_test())
