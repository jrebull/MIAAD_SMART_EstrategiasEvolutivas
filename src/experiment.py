"""Orquestador de experimentos: 30 corridas × 4 variantes = 120 ejecuciones."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from .evolution_strategy import EvolutionStrategy, MutationType, SelectionType


SUCCESS_THRESHOLD: float = 0.95
DEFAULT_N_RUNS: int = 30


@dataclass(frozen=True)
class Variant:
    """Una de las 4 variantes del experimento."""

    id: str
    label: str
    selection_type: SelectionType
    mutation_type: MutationType


VARIANTS: tuple[Variant, ...] = (
    Variant("plus_iso", "(μ+λ) Isotrópica", "plus", "isotropic"),
    Variant("comma_iso", "(μ,λ) Isotrópica", "comma", "isotropic"),
    Variant("plus_aniso", "(μ+λ) Anisotrópica", "plus", "anisotropic"),
    Variant("comma_aniso", "(μ,λ) Anisotrópica", "comma", "anisotropic"),
)


def get_seeds(n_runs: int = DEFAULT_N_RUNS, base: int = 42) -> list[int]:
    """Devuelve una lista determinista de semillas: [base, base+1, ..., base+n_runs-1]."""
    return [base + i for i in range(n_runs)]


def run_single(
    variant: Variant,
    seed: int,
    mu: int = 20,
    lambda_: int = 100,
    generations: int = 500,
    dimension: int = 10,
) -> dict:
    """Ejecuta una sola corrida para una variante y una semilla."""
    es = EvolutionStrategy(
        mu=mu,
        lambda_=lambda_,
        generations=generations,
        dimension=dimension,
        selection_type=variant.selection_type,
        mutation_type=variant.mutation_type,
    )
    result = es.run(seed=seed)
    result["variant_id"] = variant.id
    result["variant_label"] = variant.label
    return result


def compute_summary(
    run_results: Iterable[dict], success_threshold: float = SUCCESS_THRESHOLD
) -> dict[str, float]:
    """Estadísticas agregadas (por variante) a partir de la lista de corridas.

    Returns:
        dict con: gap_mean, gap_std, success_rate (0-100), best_fitness_mean,
        best_fitness_max, best_fitness_std, n_runs.
    """
    finals = np.array([r["best_fitness"] for r in run_results], dtype=float)
    gaps = 1.0 - finals
    success_rate = 100.0 * float((finals >= success_threshold).mean())
    return {
        "n_runs": int(finals.size),
        "gap_mean": float(gaps.mean()),
        "gap_std": float(gaps.std(ddof=1)) if finals.size > 1 else 0.0,
        "success_rate": success_rate,
        "best_fitness_mean": float(finals.mean()),
        "best_fitness_std": float(finals.std(ddof=1)) if finals.size > 1 else 0.0,
        "best_fitness_max": float(finals.max()),
        "best_fitness_min": float(finals.min()),
    }


def generations_to_success(
    best_history: list[float], threshold: float = SUCCESS_THRESHOLD
) -> int | None:
    """Número de la primera generación en que best_fitness cruza el umbral.

    Returns None si nunca se alcanza el umbral durante la corrida.
    """
    arr = np.asarray(best_history, dtype=float)
    hit = np.where(arr >= threshold)[0]
    return int(hit[0]) if hit.size else None
