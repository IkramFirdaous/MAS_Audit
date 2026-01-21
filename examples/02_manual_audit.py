# Audit manuel - Sans Inspect
"""
Exemple d'audit manuel d'un MAS sans utiliser Inspect.
"""

import sys
sys.path.insert(0, "..")

from mas_runtime import ExampleMAS
from seeds import error_propagation_seeds


def run_manual_audit():
    """Exécute un audit manuel du MAS."""
    mas = ExampleMAS()
    mas.initialize({"mode": "audit"})

    # Charger les seeds
    seeds = error_propagation_seeds()

    results = []
    for seed in seeds:
        print(f"\nTest: {seed['description']}")

        try:
            result = mas.run(str(seed["input"]))
            results.append({
                "seed_id": seed["id"],
                "success": True,
                "result": result,
            })
            print(f"  Status: OK")
        except Exception as e:
            results.append({
                "seed_id": seed["id"],
                "success": False,
                "error": str(e),
            })
            print(f"  Status: ERREUR - {e}")

    # Résumé
    print("\n" + "=" * 50)
    print("RÉSUMÉ DE L'AUDIT")
    print("=" * 50)
    success_count = sum(1 for r in results if r["success"])
    print(f"Tests réussis: {success_count}/{len(results)}")


if __name__ == "__main__":
    run_manual_audit()
