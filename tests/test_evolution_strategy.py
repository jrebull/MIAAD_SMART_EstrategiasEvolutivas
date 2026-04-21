"""Tests de integración del motor de Estrategias Evolutivas."""

import numpy as np
import pytest

from src.evolution_strategy import EvolutionStrategy


@pytest.fixture
def small_es_plus_iso():
    return EvolutionStrategy(
        mu=5, lambda_=20, generations=30, dimension=10,
        selection_type="plus", mutation_type="isotropic",
    )


@pytest.fixture
def small_es_plus_aniso():
    return EvolutionStrategy(
        mu=5, lambda_=20, generations=30, dimension=10,
        selection_type="plus", mutation_type="anisotropic",
    )


def test_run_retorna_estructura_correcta(small_es_plus_iso):
    r = small_es_plus_iso.run(seed=42)
    assert set(r.keys()) >= {
        "best_fitness_history",
        "avg_fitness_history",
        "best_solution",
        "best_fitness",
        "sigma_history",
        "seed",
    }
    assert len(r["best_fitness_history"]) == 30
    assert r["best_solution"].shape == (10,)
    assert r["seed"] == 42


def test_reproducibilidad_bit_a_bit(small_es_plus_iso):
    r1 = small_es_plus_iso.run(seed=123)
    r2 = small_es_plus_iso.run(seed=123)
    assert r1["best_fitness"] == r2["best_fitness"]
    assert r1["best_fitness_history"] == r2["best_fitness_history"]
    np.testing.assert_array_equal(r1["best_solution"], r2["best_solution"])


def test_plus_nunca_empeora_mejor(small_es_plus_iso):
    r = small_es_plus_iso.run(seed=7)
    history = r["best_fitness_history"]
    for i in range(1, len(history)):
        assert history[i] >= history[i - 1] - 1e-12, (
            f"En (μ+λ) el mejor no puede empeorar: gen {i} {history[i]} < gen {i-1} {history[i-1]}"
        )


def test_aniso_sigma_vector_converge_a_valores_distintos(small_es_plus_aniso):
    es = EvolutionStrategy(
        mu=20, lambda_=100, generations=200, dimension=10,
        selection_type="plus", mutation_type="anisotropic",
    )
    r = es.run(seed=1)
    # sigma_history es lista de arrays (D,)
    sigma_final = r["sigma_history"][-1]
    assert sigma_final.shape == (10,)
    # el rango de sigmas finales debe ser no trivial (los σ se diferencian entre dimensiones)
    assert sigma_final.max() / sigma_final.min() > 1.5


def test_comma_requires_lambda_mayor_mu():
    with pytest.raises(ValueError):
        EvolutionStrategy(mu=20, lambda_=20, generations=1, selection_type="comma")


def test_converge_aceptablemente_en_aniso():
    es = EvolutionStrategy(
        mu=20, lambda_=100, generations=200, dimension=10,
        selection_type="plus", mutation_type="anisotropic",
    )
    r = es.run(seed=42)
    # con 200 generaciones y aniso debería cruzar fácilmente 0.9
    assert r["best_fitness"] > 0.9
