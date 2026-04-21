#!/usr/bin/env python3
"""Exporta los resultados de `results/` a JSON para el sitio Nuxt.

Produce (en `web/public/data/`):

- convergence.json — curvas de convergencia promedio (media ± std) por variante.
- summary.json — métricas agregadas por variante.
- sigma_evolution.json — evolución del σ global y de los 10 σ_i anisotrópicos,
  promediados sobre las 30 corridas.

También copia los PNG de `Figures/` a `web/public/images/` para que
el frontend pueda referenciarlos estáticamente.

Uso:

    python export_web_data.py
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "Figures"
WEB_DATA_DIR = PROJECT_ROOT / "web" / "public" / "data"
WEB_IMAGES_DIR = PROJECT_ROOT / "web" / "public" / "images"
WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
WEB_IMAGES_DIR.mkdir(parents=True, exist_ok=True)


VARIANT_META = {
    "plus_iso":    {"label": "(μ+λ) Isotrópica",    "color": "#003CA6"},
    "comma_iso":   {"label": "(μ,λ) Isotrópica",    "color": "#C8962E"},
    "plus_aniso":  {"label": "(μ+λ) Anisotrópica",  "color": "#555559"},
    "comma_aniso": {"label": "(μ,λ) Anisotrópica",  "color": "#B71C1C"},
}
VARIANT_ORDER = list(VARIANT_META.keys())


def export_convergence(convergence_df: pd.DataFrame, out_path: Path) -> None:
    payload = {"generations": None, "variants": {}}
    for vid in VARIANT_ORDER:
        sub = convergence_df[convergence_df["variant"] == vid]
        stats = sub.groupby("generation")["best_fitness"].agg(["mean", "std"])
        stats = stats.sort_index()
        if payload["generations"] is None:
            payload["generations"] = stats.index.astype(int).tolist()
        payload["variants"][vid] = {
            "label": VARIANT_META[vid]["label"],
            "color": VARIANT_META[vid]["color"],
            "mean": [float(x) for x in stats["mean"].tolist()],
            "std": [float(x) for x in stats["std"].tolist()],
        }
    out_path.write_text(json.dumps(payload))


def export_summary(summary_df: pd.DataFrame, per_variant: list[dict], out_path: Path) -> None:
    rows = []
    by_id = {v["variant"]: v for v in per_variant}
    for vid in VARIANT_ORDER:
        stats = by_id[vid]
        rows.append(
            {
                "id": vid,
                "label": VARIANT_META[vid]["label"],
                "color": VARIANT_META[vid]["color"],
                "gap_mean": float(stats["gap_mean"]),
                "gap_std": float(stats["gap_std"]),
                "success_rate": float(stats["success_rate"]),
                "best_fitness_mean": float(stats["best_fitness_mean"]),
                "best_fitness_std": float(stats["best_fitness_std"]),
                "best_fitness_max": float(stats["best_fitness_max"]),
                "best_fitness_min": float(stats["best_fitness_min"]),
                "gens_to_success_mean": float(stats["gens_to_success_mean"]),
                "gens_to_success_std": float(stats["gens_to_success_std"]),
                "n_runs": int(stats["n_runs"]),
            }
        )
    out_path.write_text(
        json.dumps(
            {
                "variants": rows,
                "hyperparameters": {
                    "mu": 20,
                    "lambda": 100,
                    "generations": 500,
                    "dimension": 10,
                    "bounds": [-5.0, 5.0],
                    "n_runs": 30,
                    "success_threshold": 0.95,
                    "sigma_init": 1.0,
                },
            }
        )
    )


def export_sigma(sigma_payload: dict, out_path: Path) -> None:
    """Exporta la media poblacional de σ promediada sobre las 30 corridas.

    Para isotrópica: series es una lista de longitud G (generaciones).
    Para anisotrópica: series es una lista de G listas de D=10 floats.
    """
    out = {}
    for vid in VARIANT_ORDER:
        entry = sigma_payload[vid]
        mean_series = np.asarray(entry["sigma_mean_across_runs"], dtype=float)
        series = mean_series.tolist()
        out[vid] = {
            "label": VARIANT_META[vid]["label"],
            "color": VARIANT_META[vid]["color"],
            "mutation_type": entry["mutation_type"],
            "series": series,
        }
    out_path.write_text(json.dumps(out))


def copy_figures() -> None:
    for src in sorted(FIGURES_DIR.glob("*.png")):
        dst = WEB_IMAGES_DIR / src.name
        shutil.copy2(src, dst)


def main() -> None:
    convergence_df = pd.read_csv(RESULTS_DIR / "convergence_data.csv")
    summary_df = pd.read_csv(RESULTS_DIR / "summary.csv")
    per_variant = json.loads((RESULTS_DIR / "per_variant_summary.json").read_text())
    sigma_payload = json.loads((RESULTS_DIR / "sigma_evolution.json").read_text())

    export_convergence(convergence_df, WEB_DATA_DIR / "convergence.json")
    export_summary(summary_df, per_variant, WEB_DATA_DIR / "summary.json")
    export_sigma(sigma_payload, WEB_DATA_DIR / "sigma_evolution.json")
    copy_figures()

    print("JSONs exportados a:", WEB_DATA_DIR)
    for p in sorted(WEB_DATA_DIR.glob("*.json")):
        size = p.stat().st_size / 1024
        print(f"  - {p.name} ({size:.1f} KB)")
    print("PNGs copiados a:", WEB_IMAGES_DIR)
    for p in sorted(WEB_IMAGES_DIR.glob("*.png")):
        print(f"  - {p.name}")


if __name__ == "__main__":
    main()
