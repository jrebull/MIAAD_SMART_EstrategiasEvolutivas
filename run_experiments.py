#!/usr/bin/env python3
"""Orquestador de los 120 experimentos (4 variantes × 30 corridas).

Guarda resultados en `results/`:

- `results/convergence_data.csv`: variant, run, generation, best_fitness, avg_fitness
- `results/summary.csv`: variant, run, final_best_fitness, gap, success
- `results/sigma_evolution.json`: evolución detallada de σ para las variantes
  aniso/iso (una corrida representativa por variante — la de mejor fitness final).

Uso:

    python run_experiments.py

Tiempo esperado: <5 minutos para 120 ejecuciones.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.experiment import (
    DEFAULT_N_RUNS,
    SUCCESS_THRESHOLD,
    VARIANTS,
    compute_summary,
    generations_to_success,
    get_seeds,
    run_single,
)


PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def main(
    mu: int = 20,
    lambda_: int = 100,
    generations: int = 500,
    dimension: int = 10,
    n_runs: int = DEFAULT_N_RUNS,
) -> None:
    seeds = get_seeds(n_runs=n_runs)

    convergence_rows: list[dict] = []
    summary_rows: list[dict] = []
    sigma_payload: dict[str, dict] = {}

    total = len(VARIANTS) * n_runs
    t0 = time.perf_counter()

    sigma_histories_by_variant: dict[str, list[np.ndarray]] = {v.id: [] for v in VARIANTS}

    with tqdm(total=total, desc="Experimentos", unit="corrida") as pbar:
        for variant in VARIANTS:
            variant_results = []
            for seed in seeds:
                res = run_single(
                    variant,
                    seed=seed,
                    mu=mu,
                    lambda_=lambda_,
                    generations=generations,
                    dimension=dimension,
                )
                variant_results.append(res)

                for g, (bf, af) in enumerate(
                    zip(res["best_fitness_history"], res["avg_fitness_history"])
                ):
                    convergence_rows.append(
                        {
                            "variant": variant.id,
                            "variant_label": variant.label,
                            "run": seed,
                            "generation": g,
                            "best_fitness": bf,
                            "avg_fitness": af,
                        }
                    )
                final_best = res["best_fitness"]
                gen_to_success = generations_to_success(
                    res["best_fitness_history"], SUCCESS_THRESHOLD
                )
                summary_rows.append(
                    {
                        "variant": variant.id,
                        "variant_label": variant.label,
                        "run": seed,
                        "final_best_fitness": final_best,
                        "gap": 1.0 - final_best,
                        "success": bool(final_best >= SUCCESS_THRESHOLD),
                        "generations_to_success": (
                            gen_to_success if gen_to_success is not None else -1
                        ),
                    }
                )
                sigma_histories_by_variant[variant.id].append(
                    np.asarray(res["sigma_history"], dtype=float)
                )
                pbar.update(1)

            best_run = max(variant_results, key=lambda r: r["best_fitness"])
            if variant.mutation_type == "isotropic":
                sigma_hist_rep = [float(s) for s in best_run["sigma_history"]]
            else:
                sigma_hist_rep = [
                    np.asarray(s, dtype=float).tolist() for s in best_run["sigma_history"]
                ]
            stacked = np.stack(sigma_histories_by_variant[variant.id])
            sigma_mean = stacked.mean(axis=0)
            sigma_payload[variant.id] = {
                "label": variant.label,
                "mutation_type": variant.mutation_type,
                "representative_seed": best_run["seed"],
                "representative_best_fitness": best_run["best_fitness"],
                "sigma_history": sigma_hist_rep,
                "sigma_mean_across_runs": sigma_mean.tolist(),
            }

    elapsed = time.perf_counter() - t0

    convergence_df = pd.DataFrame(convergence_rows)
    summary_df = pd.DataFrame(summary_rows)
    convergence_df.to_csv(RESULTS_DIR / "convergence_data.csv", index=False)
    summary_df.to_csv(RESULTS_DIR / "summary.csv", index=False)

    (RESULTS_DIR / "sigma_evolution.json").write_text(
        json.dumps(sigma_payload, indent=2)
    )

    per_variant = []
    print("\n=== Resumen por variante ===\n")
    for variant in VARIANTS:
        runs_v = [r for r in summary_rows if r["variant"] == variant.id]
        finals = [r["final_best_fitness"] for r in runs_v]
        stats = compute_summary(
            [{"best_fitness": f} for f in finals]
        )
        gens_success = [
            r["generations_to_success"] for r in runs_v if r["generations_to_success"] >= 0
        ]
        stats["variant"] = variant.id
        stats["variant_label"] = variant.label
        stats["gens_to_success_mean"] = (
            float(np.mean(gens_success)) if gens_success else float("nan")
        )
        stats["gens_to_success_std"] = (
            float(np.std(gens_success, ddof=1)) if len(gens_success) > 1 else 0.0
        )
        per_variant.append(stats)
        print(
            f"{variant.label:>22s} | "
            f"Gap = {stats['gap_mean']:.3e} ± {stats['gap_std']:.3e} | "
            f"Éxito = {stats['success_rate']:5.1f}% | "
            f"Gen→0.95 = {stats['gens_to_success_mean']:6.2f} ± {stats['gens_to_success_std']:5.2f} | "
            f"f prom = {stats['best_fitness_mean']:.6f}"
        )

    (RESULTS_DIR / "per_variant_summary.json").write_text(
        json.dumps(per_variant, indent=2)
    )

    print(
        f"\nTotal: {total} corridas en {elapsed:.2f} s "
        f"({elapsed / total * 1000:.1f} ms/corrida)"
    )
    print(f"Resultados guardados en {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
