# Audit manuel - Sans Inspect
"""
Exemple d'audit manuel d'un MAS sans utiliser Inspect.
"""

import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mas_runtime import create_financial_analysis_mas
from seeds import error_propagation_seeds


async def run_manual_audit():
    """Exécute un audit manuel du MAS."""
    mas = create_financial_analysis_mas()
    await mas.initialize()

    # Charger les seeds
    seeds = error_propagation_seeds()

    results = []
    for seed in seeds:
        print(f"\nTest: {seed['description']}")

        try:
            response, trace = await mas.process_message(str(seed["input"]))
            results.append({
                "seed_id": seed["id"],
                "success": True,
                "result": response,
            })
            print(f"  Status: OK")
        except Exception as e:
            results.append({
                "seed_id": seed["id"],
                "success": False,
                "error": str(e),
            })
            print(f"  Status: ERREUR - {e}")

    await mas.cleanup()

    # Résumé
    print("\n" + "=" * 50)
    print("RÉSUMÉ DE L'AUDIT")
    print("=" * 50)
    success_count = sum(1 for r in results if r["success"])
    print(f"Tests réussis: {success_count}/{len(results)}")


if __name__ == "__main__":
    asyncio.run(run_manual_audit())
