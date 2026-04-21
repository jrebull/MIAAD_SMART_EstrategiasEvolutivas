#!/usr/bin/env python3
"""Genera las figuras del reporte a partir de los CSVs de `results/`.

Figuras producidas en `Figures/` a 300 DPI, fondo blanco, etiquetas en español:

- convergence_comparison.png — convergencia promedio (4 variantes) con banda ±1σ
- convergence_log.png — convergencia en escala logarítmica de (1 - fitness)
- gap_comparison.png — Gap promedio con barras de error por variante
- success_rate.png — tasa de éxito (%) por variante
- generations_to_success.png — generaciones hasta f≥0.95 por variante
- sigma_evolution.png — evolución de σ (isotrópico vs anisotrópico por dimensión)

Uso:

    python generate_figures.py

Requiere haber ejecutado antes `python run_experiments.py`.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "Figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# --- paleta UACJ de alto contraste; line styles distintos para B/N ---
VARIANT_ORDER = ["plus_iso", "comma_iso", "plus_aniso", "comma_aniso"]
VARIANT_LABELS = {
    "plus_iso":    r"$(\mu + \lambda)$ Isotrópica",
    "comma_iso":   r"$(\mu , \lambda)$ Isotrópica",
    "plus_aniso":  r"$(\mu + \lambda)$ Anisotrópica",
    "comma_aniso": r"$(\mu , \lambda)$ Anisotrópica",
}
VARIANT_COLORS = {
    "plus_iso":    "#003CA6",
    "comma_iso":   "#C8962E",
    "plus_aniso":  "#555559",
    "comma_aniso": "#B71C1C",
}
VARIANT_LINESTYLES = {
    "plus_iso":    "-",
    "comma_iso":   "--",
    "plus_aniso":  "-.",
    "comma_aniso": ":",
}


# ---------------------------------------------------------------------------
# Ajustes globales de matplotlib
# ---------------------------------------------------------------------------
plt.rcParams.update(
    {
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.grid": True,
        "grid.alpha": 0.3,
        "font.size": 12,
        "axes.labelsize": 13,
        "axes.titlesize": 14,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
    }
)


# ---------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------
def plot_convergence(convergence_df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    for variant in VARIANT_ORDER:
        sub = convergence_df[convergence_df["variant"] == variant]
        gen_stats = sub.groupby("generation")["best_fitness"].agg(["mean", "std"])
        gens = gen_stats.index.to_numpy()
        mean = gen_stats["mean"].to_numpy()
        std = gen_stats["std"].to_numpy()
        color = VARIANT_COLORS[variant]
        ax.plot(
            gens,
            mean,
            label=VARIANT_LABELS[variant],
            color=color,
            linestyle=VARIANT_LINESTYLES[variant],
            linewidth=2.2,
        )
        ax.fill_between(gens, mean - std, mean + std, color=color, alpha=0.15)
    ax.set_xlabel("Generación")
    ax.set_ylabel("Mejor fitness (promedio de 30 corridas)")
    ax.set_title("Convergencia de las 4 variantes de Estrategia Evolutiva")
    ax.legend(loc="lower right", framealpha=0.95)
    ax.set_xlim(0, gens.max())
    ax.set_ylim(0, 1.02)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_convergence_log(convergence_df: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    for variant in VARIANT_ORDER:
        sub = convergence_df[convergence_df["variant"] == variant]
        gen_stats = sub.groupby("generation")["best_fitness"].mean()
        gens = gen_stats.index.to_numpy()
        gap = np.clip(1.0 - gen_stats.to_numpy(), 1e-18, None)
        ax.plot(
            gens,
            gap,
            label=VARIANT_LABELS[variant],
            color=VARIANT_COLORS[variant],
            linestyle=VARIANT_LINESTYLES[variant],
            linewidth=2.2,
        )
    ax.set_yscale("log")
    ax.set_xlabel("Generación")
    ax.set_ylabel(r"Gap promedio $1 - f(\mathbf{x}_{\mathrm{mejor}})$  (escala logarítmica)")
    ax.set_title("Velocidad de convergencia — vista logarítmica")
    ax.legend(loc="upper right", framealpha=0.95)
    ax.set_xlim(0, gens.max())
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_gap_bars(summary_df: pd.DataFrame, output_path: Path) -> None:
    gap_stats = (
        summary_df.groupby("variant")["gap"]
        .agg(["mean", "std"])
        .reindex(VARIANT_ORDER)
    )
    fig, ax = plt.subplots(figsize=(9, 6))
    x = np.arange(len(VARIANT_ORDER))
    colors = [VARIANT_COLORS[v] for v in VARIANT_ORDER]
    # el Gap es ~0 a escala lineal; usamos escala log para que se vea
    means = np.clip(gap_stats["mean"].to_numpy(), 1e-20, None)
    stds = gap_stats["std"].to_numpy()
    ax.bar(x, means, yerr=stds, color=colors, edgecolor="black", linewidth=0.8, capsize=6)
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(
        [VARIANT_LABELS[v] for v in VARIANT_ORDER], rotation=10, ha="center"
    )
    ax.set_ylabel(r"Gap final promedio  $1 - f(\mathbf{x}_{\mathrm{mejor}})$ (log)")
    ax.set_title("Gap al final de 500 generaciones por variante")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_success_rate(summary_df: pd.DataFrame, output_path: Path) -> None:
    rates = (
        summary_df.groupby("variant")["success"]
        .mean()
        .reindex(VARIANT_ORDER)
        * 100.0
    )
    fig, ax = plt.subplots(figsize=(9, 6))
    x = np.arange(len(VARIANT_ORDER))
    colors = [VARIANT_COLORS[v] for v in VARIANT_ORDER]
    bars = ax.bar(x, rates.to_numpy(), color=colors, edgecolor="black", linewidth=0.8)
    for bar, rate in zip(bars, rates.to_numpy()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{rate:.1f}%",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )
    ax.set_xticks(x)
    ax.set_xticklabels([VARIANT_LABELS[v] for v in VARIANT_ORDER], rotation=10, ha="center")
    ax.set_ylabel(r"Tasa de éxito (%)  con $f(\mathbf{x}) \geq 0.95$")
    ax.set_ylim(0, 110)
    ax.set_title("Tasa de éxito por variante — 30 corridas independientes")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_generations_to_success(summary_df: pd.DataFrame, output_path: Path) -> None:
    df = summary_df[summary_df["generations_to_success"] >= 0].copy()
    fig, ax = plt.subplots(figsize=(9, 6))
    data = [
        df[df["variant"] == v]["generations_to_success"].to_numpy()
        for v in VARIANT_ORDER
    ]
    bp = ax.boxplot(
        data,
        tick_labels=[VARIANT_LABELS[v] for v in VARIANT_ORDER],
        patch_artist=True,
        medianprops={"color": "black", "linewidth": 2},
        showmeans=True,
        meanprops={"marker": "D", "markerfacecolor": "white",
                   "markeredgecolor": "black", "markersize": 7},
    )
    for patch, variant in zip(bp["boxes"], VARIANT_ORDER):
        patch.set_facecolor(VARIANT_COLORS[variant])
        patch.set_alpha(0.75)
    ax.set_ylabel("Generación en la que se cruza $f \\geq 0.95$")
    ax.set_title("Velocidad de convergencia al umbral de éxito")
    plt.setp(ax.get_xticklabels(), rotation=10, ha="center")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_sigma_evolution(sigma_payload: dict, output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # --- Isotrópica: una curva por variante iso (promedio de 30 corridas)
    ax_iso = axes[0]
    for variant in ["plus_iso", "comma_iso"]:
        entry = sigma_payload[variant]
        sigma_mean = np.asarray(entry["sigma_mean_across_runs"], dtype=float)
        ax_iso.plot(
            np.arange(sigma_mean.size),
            sigma_mean,
            label=VARIANT_LABELS[variant],
            color=VARIANT_COLORS[variant],
            linestyle=VARIANT_LINESTYLES[variant],
            linewidth=2.2,
        )
    ax_iso.set_yscale("log")
    ax_iso.set_xlabel("Generación")
    ax_iso.set_ylabel(r"$\sigma$ global (media poblacional, promedio 30 corridas)")
    ax_iso.set_title("Auto-adaptación isotrópica")
    ax_iso.legend(loc="upper right")

    # --- Anisotrópica: 10 curvas (una por dimensión) de plus_aniso,
    #     promedio de la media poblacional en las 30 corridas
    ax_aniso = axes[1]
    entry = sigma_payload["plus_aniso"]
    sigma_mean = np.asarray(entry["sigma_mean_across_runs"], dtype=float)  # (G, D)
    G, D = sigma_mean.shape
    # recortamos al rango en el que la dinámica es interesante (antes del colapso a SIGMA_MIN)
    g_max = min(150, G)
    cmap = plt.get_cmap("viridis")
    for i in range(D):
        ax_aniso.plot(
            np.arange(g_max),
            sigma_mean[:g_max, i],
            color=cmap(i / (D - 1)),
            linewidth=1.8,
            label=f"$\\sigma_{{{i + 1}}}$",
        )
    ax_aniso.set_yscale("log")
    ax_aniso.set_xlabel("Generación")
    ax_aniso.set_ylabel(r"$\sigma_i$ (media poblacional, promedio 30 corridas)")
    ax_aniso.set_title(
        r"Auto-adaptación anisotrópica: $(\mu+\lambda)$ — una curva por dimensión"
    )
    ax_aniso.legend(loc="upper right", ncol=2, fontsize=9)

    fig.suptitle(
        "Evolución de los parámetros de mutación  (promedio de las 30 corridas)",
        fontsize=14,
    )
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    convergence_df = pd.read_csv(RESULTS_DIR / "convergence_data.csv")
    summary_df = pd.read_csv(RESULTS_DIR / "summary.csv")
    sigma_payload = json.loads((RESULTS_DIR / "sigma_evolution.json").read_text())

    plot_convergence(convergence_df, FIGURES_DIR / "convergence_comparison.png")
    plot_convergence_log(convergence_df, FIGURES_DIR / "convergence_log.png")
    plot_gap_bars(summary_df, FIGURES_DIR / "gap_comparison.png")
    plot_success_rate(summary_df, FIGURES_DIR / "success_rate.png")
    plot_generations_to_success(summary_df, FIGURES_DIR / "generations_to_success.png")
    plot_sigma_evolution(sigma_payload, FIGURES_DIR / "sigma_evolution.png")

    print("Figuras generadas en:", FIGURES_DIR)
    for p in sorted(FIGURES_DIR.glob("*.png")):
        print(f"  - {p.name}")


if __name__ == "__main__":
    main()
