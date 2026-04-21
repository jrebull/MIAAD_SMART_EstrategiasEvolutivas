"""Motor principal de Estrategias Evolutivas.

Soporta las 4 variantes requeridas por la práctica:

- (μ + λ) / (μ , λ) × Isotrópica / Anisotrópica

Uso típico:

    >>> es = EvolutionStrategy(mu=20, lambda_=100, generations=500,
    ...                         selection_type="plus", mutation_type="anisotropic")
    >>> resultado = es.run(seed=42)
    >>> resultado["best_fitness"]
    0.99...
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Literal

import numpy as np

from .fitness import inverted_ellipsoid
from .operators import (
    mutate_anisotropic,
    mutate_isotropic,
    select_comma,
    select_plus,
)


SelectionType = Literal["plus", "comma"]
MutationType = Literal["isotropic", "anisotropic"]


@dataclass
class Individual:
    """Representación conceptual de un individuo en la EE.

    Attributes:
        x: Vector de decisión de shape (D,).
        sigma: Parámetro(s) de estrategia. Shape () para isotrópico o (D,)
            para anisotrópico.
        fitness: Valor de f(x).
    """

    x: np.ndarray
    sigma: np.ndarray
    fitness: float


@dataclass
class EvolutionStrategy:
    """Estrategia Evolutiva auto-adaptativa (μ/1, +/, λ).

    Attributes:
        mu: Tamaño de la población de padres.
        lambda_: Número de descendientes generados por generación.
        generations: Número de generaciones a iterar.
        dimension: Dimensionalidad del espacio de búsqueda.
        bounds: (low, high) aplicado por clamping a cada x_i.
        selection_type: "plus" para (μ+λ) o "comma" para (μ,λ).
        mutation_type: "isotropic" (un σ) o "anisotropic" (un σ por coordenada).
        sigma_init: Valor inicial de σ para toda la población.
        fitness_fn: Función objetivo; debe soportar evaluación vectorizada (N, D) -> (N,).
    """

    mu: int = 20
    lambda_: int = 100
    generations: int = 500
    dimension: int = 10
    bounds: tuple[float, float] = (-5.0, 5.0)
    selection_type: SelectionType = "plus"
    mutation_type: MutationType = "isotropic"
    sigma_init: float = 1.0
    fitness_fn: Callable[[np.ndarray], np.ndarray] = field(default=inverted_ellipsoid)

    def __post_init__(self) -> None:
        if self.selection_type not in ("plus", "comma"):
            raise ValueError(f"selection_type debe ser 'plus' o 'comma', no {self.selection_type!r}")
        if self.mutation_type not in ("isotropic", "anisotropic"):
            raise ValueError(
                f"mutation_type debe ser 'isotropic' o 'anisotropic', no {self.mutation_type!r}"
            )
        if self.selection_type == "comma" and self.lambda_ <= self.mu:
            raise ValueError("Selección coma requiere λ > μ")

    def _initial_population(
        self, rng: np.random.Generator
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        low, high = self.bounds
        x = rng.uniform(low, high, size=(self.mu, self.dimension))
        if self.mutation_type == "isotropic":
            sigma = np.full(self.mu, self.sigma_init, dtype=float)
        else:
            sigma = np.full((self.mu, self.dimension), self.sigma_init, dtype=float)
        fitness = self.fitness_fn(x)
        return x, sigma, fitness

    def _mutate(
        self,
        x: np.ndarray,
        sigma: np.ndarray,
        rng: np.random.Generator,
    ) -> tuple[np.ndarray, np.ndarray]:
        if self.mutation_type == "isotropic":
            return mutate_isotropic(x, sigma, rng, self.bounds)
        return mutate_anisotropic(x, sigma, rng, self.bounds)

    def _select(
        self,
        parents_x: np.ndarray,
        parents_sigma: np.ndarray,
        parents_fitness: np.ndarray,
        offspring_x: np.ndarray,
        offspring_sigma: np.ndarray,
        offspring_fitness: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        if self.selection_type == "plus":
            return select_plus(
                parents_x,
                parents_sigma,
                parents_fitness,
                offspring_x,
                offspring_sigma,
                offspring_fitness,
                self.mu,
            )
        return select_comma(offspring_x, offspring_sigma, offspring_fitness, self.mu)

    def run(self, seed: int) -> dict:
        """Ejecuta una corrida completa y devuelve los resultados.

        Args:
            seed: Semilla para el generador numpy (determinismo bit-a-bit).

        Returns:
            dict con:

            - best_fitness_history: list[float] — mejor fitness por generación.
            - avg_fitness_history: list[float] — fitness promedio por generación.
            - best_solution: np.ndarray (D,) — mejor x encontrado.
            - best_fitness: float — f(best_solution).
            - sigma_history: list — evolución del/los σ medio(s) por generación.
            - seed: int — semilla usada.
        """
        rng = np.random.default_rng(seed)
        x, sigma, fitness = self._initial_population(rng)

        best_fitness_history: list[float] = []
        avg_fitness_history: list[float] = []
        sigma_history: list = []

        for _ in range(self.generations):
            parent_idx = rng.integers(0, self.mu, size=self.lambda_)
            off_x = x[parent_idx].copy()
            off_sigma = sigma[parent_idx].copy()
            off_x, off_sigma = self._mutate(off_x, off_sigma, rng)
            off_fitness = self.fitness_fn(off_x)

            x, sigma, fitness = self._select(
                x, sigma, fitness, off_x, off_sigma, off_fitness
            )

            best_fitness_history.append(float(fitness.max()))
            avg_fitness_history.append(float(fitness.mean()))
            if sigma.ndim == 1:
                sigma_history.append(float(sigma.mean()))
            else:
                sigma_history.append(sigma.mean(axis=0).copy())

        best_idx = int(np.argmax(fitness))
        return {
            "best_fitness_history": best_fitness_history,
            "avg_fitness_history": avg_fitness_history,
            "best_solution": x[best_idx].copy(),
            "best_fitness": float(fitness[best_idx]),
            "sigma_history": sigma_history,
            "seed": int(seed),
        }
