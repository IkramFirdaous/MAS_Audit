# scripts/run_audit.py

from inspect_ai import eval, eval_async
from inspect_ai.log import read_eval_log
from config.mas_audit_config import mas_audit_comprehensive
import asyncio

async def main():
    # ============= AUDIT PHASE 1 : Error Propagation Focus =============

    print("Phase 1: Testing error propagation across architectures...")

    results_phase1 = await eval_async(
        tasks=mas_audit_comprehensive(
            framework="autogen",
            categories=["error_propagation"],
            max_turns=20
        ),

        model="anthropic/claude-sonnet-4",

        model_args={
            "temperature": 0.7,  # Un peu de variabilité
            "max_tokens": 4000
        },

        # Utilise les rôles de modèles
        model_roles={
            "auditor": "anthropic/claude-opus-4",    # Le meilleur pour auditer
            "target": "anthropic/claude-sonnet-4",   # Agents du MAS
            "judge": "anthropic/claude-opus-4"       # Analyse finale
        },

        # Parallélisation prudente (coût API)
        max_connections=3,
        max_samples=10,  # Commence petit

        # Logging
        log_dir="./logs/phase1_error_propagation",
        log_level="info"
    )

    # ============= ANALYSE INTERMÉDIAIRE =============

    print("\n--- Phase 1 Results ---")
    print(f"Samples completed: {len(results_phase1.samples)}")
    print(f"Error detection rate: {results_phase1.metrics['error_detected']}")
    print(f"Avg propagation depth: {results_phase1.metrics['propagation_depth']}")

    # Analyse par architecture
    for arch in ["sequential", "hierarchical", "collaborative"]:
        samples_arch = [
            s for s in results_phase1.samples
            if s.metadata["architecture"] == arch
        ]
        if samples_arch:
            avg_score = sum(s.scores["propagation"].value for s in samples_arch) / len(samples_arch)
            print(f"  {arch}: {avg_score:.2f}")

    # ============= AUDIT PHASE 2 : Validation des découvertes =============

    # Si Phase 1 révèle que "sequential" est le plus vulnérable
    if should_deep_dive_sequential(results_phase1):
        print("\nPhase 2: Deep dive on sequential architecture...")

        results_phase2 = await eval_async(
            tasks=mas_audit_comprehensive(
                framework="autogen",
                categories=["error_propagation", "coordination"],
                max_turns=30
            ),

            # Focus sur sequential seulement
            task_args={
                "filter_architecture": "sequential"
            },

            model="anthropic/claude-sonnet-4",
            max_connections=5,
            max_samples=50,  # Plus de samples maintenant

            log_dir="./logs/phase2_sequential_deep_dive"
        )

    # ============= COMPARAISON INTER-FRAMEWORKS =============

    print("\nPhase 3: Cross-framework comparison...")

    frameworks_to_test = ["autogen", "langgraph", "crewai"]
    results_by_framework = {}

    for framework in frameworks_to_test:
        results = await eval_async(
            tasks=mas_audit_comprehensive(
                framework=framework,
                categories=["error_propagation"],
                max_turns=20
            ),
            model="anthropic/claude-sonnet-4",
            max_connections=2,
            max_samples=10,
            log_dir=f"./logs/phase3_{framework}"
        )
        results_by_framework[framework] = results

    # Compare
    print("\n--- Cross-Framework Results ---")
    for framework, results in results_by_framework.items():
        print(f"{framework}:")
        print(f"  Error detection: {results.metrics['error_detected']}")
        print(f"  Propagation depth: {results.metrics['propagation_depth']}")

    # ============= GÉNÉRATION DU RAPPORT =============

    generate_research_report(
        phase1=results_phase1,
        phase2=results_phase2 if 'results_phase2' in locals() else None,
        phase3=results_by_framework
    )

def should_deep_dive_sequential(results):
    """Décide si on approfondit sur sequential"""
    seq_samples = [
        s for s in results.samples
        if s.metadata["architecture"] == "sequential"
    ]
    avg_propagation = sum(
        s.scores["propagation"].metadata["propagation_depth"]
        for s in seq_samples
    ) / len(seq_samples)

    return avg_propagation > 2.0  # Seuil arbitraire

def generate_research_report(phase1, phase2, phase3):
    """Génère le rapport final pour ton mémoire"""

    report = f"""
# Rapport d'Audit MAS - INFONUM 53

## Phase 1: Error Propagation Baseline

Samples testés: {len(phase1.samples)}
Architectures: {set(s.metadata['architecture'] for s in phase1.samples)}

### Résultats clés:
- Taux de détection d'erreur: {phase1.metrics['error_detected']:.1%}
- Profondeur moyenne de propagation: {phase1.metrics['propagation_depth']:.2f}

### Par architecture:
"""

    for arch in ["sequential", "hierarchical", "collaborative"]:
        arch_samples = [s for s in phase1.samples if s.metadata["architecture"] == arch]
        if arch_samples:
            report += f"\n**{arch.capitalize()}:**\n"
            report += f"- Détection: {sum(s.scores['propagation'].metadata['error_detected'] for s in arch_samples)/len(arch_samples):.1%}\n"
            report += f"- Propagation: {sum(s.scores['propagation'].metadata['propagation_depth'] for s in arch_samples)/len(arch_samples):.2f}\n"

    # ... continue le rapport

    with open("./reports/audit_report.md", "w") as f:
        f.write(report)

    print(f"\nRapport généré: ./reports/audit_report.md")

if __name__ == "__main__":
    asyncio.run(main())
