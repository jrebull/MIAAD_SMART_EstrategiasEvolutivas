"""Operadores de mutación (auto-adaptativa) y selección para EE."""

from __future__ import annotations

import numpy as np

SIGMA_MIN: float = 1e-8


def mutate_isotropic(
    x: np.ndarray,
    sigma: np.ndarray,
    rng: np.random.Generator,
    bounds: tuple[float, float] = (-5.0, 5.0),
) -> tuple[np.ndarray, np.ndarray]:
    """Mutación isotrópica con auto-adaptación de un único σ por individuo.

    Fórmulas (Schwefel):

        τ       = 1 / sqrt(2D)
        σ'      = σ · exp(τ · N(0,1))
        x'      = x + σ' · N(0, I_D)

    Args:
        x: Matriz (N, D) con N individuos en D dimensiones.
        sigma: Vector (N,) con el σ global de cada individuo.
        rng: Generador numpy con semilla fija.
        bounds: Intervalo de caja (low, high) aplicado por clamping a x'.

    Returns:
        (x', σ') con las mismas formas de entrada.
    """
    N, D = x.shape
    tau = 1.0 / np.sqrt(2.0 * D)
    new_sigma = sigma * np.exp(tau * rng.standard_normal(N))
    new_sigma = np.maximum(new_sigma, SIGMA_MIN)
    noise = rng.standard_normal((N, D))
    new_x = x + new_sigma[:, None] * noise
    new_x = np.clip(new_x, bounds[0], bounds[1])
    return new_x, new_sigma


def mutate_anisotropic(
    x: np.ndarray,
    sigma: np.ndarray,
    rng: np.random.Generator,
    bounds: tuple[float, float] = (-5.0, 5.0),
) -> tuple[np.ndarray, np.ndarray]:
    """Mutación anisotrópica con auto-adaptación de un σ por coordenada.

    Fórmulas (Schwefel):

        τ_0     = 1 / sqrt(2D)
        τ_i     = 1 / sqrt(2·sqrt(D))
        σ_i'    = σ_i · exp(τ_0 · N(0,1) + τ_i · N_i(0,1))
        x_i'    = x_i + σ_i' · N_i(0,1)

    El ruido global N(0,1) es compartido por las D coordenadas de un mismo
    individuo; N_i(0,1) es independiente por coordenada.

    Args:
        x: Matriz (N, D).
        sigma: Matriz (N, D) con un σ por coordenada.
        rng: Generador numpy.
        bounds: (low, high) para clamping.

    Returns:
        (x', σ') con las mismas formas de entrada.
    """
    N, D = x.shape
    tau_global = 1.0 / np.sqrt(2.0 * D)
    tau_local = 1.0 / np.sqrt(2.0 * np.sqrt(D))
    global_noise = rng.standard_normal((N, 1))
    local_noise = rng.standard_normal((N, D))
    new_sigma = sigma * np.exp(tau_global * global_noise + tau_local * local_noise)
    new_sigma = np.maximum(new_sigma, SIGMA_MIN)
    mutation = rng.standard_normal((N, D))
    new_x = x + new_sigma * mutation
    new_x = np.clip(new_x, bounds[0], bounds[1])
    return new_x, new_sigma


def select_plus(
    parents_x: np.ndarray,
    parents_sigma: np.ndarray,
    parents_fitness: np.ndarray,
    offspring_x: np.ndarray,
    offspring_sigma: np.ndarray,
    offspring_fitness: np.ndarray,
    mu: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Selección (μ + λ): los μ mejores de la unión padres ∪ descendientes.

    Por construcción, el mejor fitness nunca decrece entre generaciones.
    """
    all_x = np.concatenate([parents_x, offspring_x], axis=0)
    all_sigma = np.concatenate([parents_sigma, offspring_sigma], axis=0)
    all_fitness = np.concatenate([parents_fitness, offspring_fitness])
    idx = np.argsort(-all_fitness, kind="stable")[:mu]
    return all_x[idx], all_sigma[idx], all_fitness[idx]


def select_comma(
    offspring_x: np.ndarray,
    offspring_sigma: np.ndarray,
    offspring_fitness: np.ndarray,
    mu: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Selección (μ , λ): los μ mejores SOLO de los λ descendientes.

    Requiere λ > μ. Los padres no sobreviven, por lo que la mejor solución
    puede empeorar entre generaciones (esto permite escapar de óptimos locales).
    """
    lambda_ = offspring_fitness.shape[0]
    if lambda_ <= mu:
        raise ValueError(f"Selección coma requiere λ > μ; se recibió λ={lambda_}, μ={mu}")
    idx = np.argsort(-offspring_fitness, kind="stable")[:mu]
    return offspring_x[idx], offspring_sigma[idx], offspring_fitness[idx]
