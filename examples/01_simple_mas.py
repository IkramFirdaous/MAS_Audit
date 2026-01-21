# MAS standalone - Exemple simple
"""
Exemple d'utilisation d'un MAS standalone sans Inspect.
"""

import sys
sys.path.insert(0, "..")

from mas_runtime import ExampleMAS


def main():
    # Créer et initialiser le MAS
    mas = ExampleMAS()
    mas.initialize({"mode": "demo"})

    # Exécuter une tâche
    result = mas.run("Calculer la somme de 1 à 10")
    print(f"Résultat: {result}")

    # Afficher les logs
    print("\nLogs:")
    for log in mas.get_logs():
        print(f"  - {log}")


if __name__ == "__main__":
    main()
