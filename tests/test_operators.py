"""Tests de mutación y selección."""

import numpy as np
import pytest

from src.operators import (
    SIGMA_MIN,
    mutate_anisotropic,
    mutate_isotropic,
    select_comma,
    select_plus,
)


def test_mutacion_isotropica_cambia_sigma():
    rng = np.random.default_rng(0)
    x = np.zeros((5, 10))
    sigma = np.full(5, 1.0)
    _, new_sigma = mutate_isotropic(x, sigma, rng)
    assert new_sigma.shape == (5,)
    assert not np.allclose(new_sigma, sigma)
    assert np.all(new_sigma >= SIGMA_MIN)


def test_mutacion_isotropica_respeta_bounds():
    rng = np.random.default_rng(0)
    x = np.full((10, 10), 4.9)
    sigma = np.full(10, 100.0)  # σ enorme
    new_x, _ = mutate_isotropic(x, sigma, rng, bounds=(-5.0, 5.0))
    assert np.all(new_x >= -5.0)
    assert np.all(new_x <= 5.0)


def test_mutacion_anisotropica_shape():
    rng = np.random.default_rng(0)
    x = np.zeros((4, 10))
    sigma = np.ones((4, 10))
    new_x, new_sigma = mutate_anisotropic(x, sigma, rng)
    assert new_x.shape == (4, 10)
    assert new_sigma.shape == (4, 10)
    assert np.all(new_sigma >= SIGMA_MIN)


def test_select_plus_mantiene_los_mejores():
    parents_x = np.zeros((3, 2))
    parents_sigma = np.full(3, 0.5)
    parents_fitness = np.array([0.8, 0.5, 0.1])
    offspring_x = np.ones((3, 2))
    offspring_sigma = np.full(3, 0.5)
    offspring_fitness = np.array([0.9, 0.3, 0.2])
    x, _, f = select_plus(
        parents_x, parents_sigma, parents_fitness,
        offspring_x, offspring_sigma, offspring_fitness,
        mu=3,
    )
    assert x.shape == (3, 2)
    assert sorted(f.tolist(), reverse=True) == [0.9, 0.8, 0.5]


def test_select_comma_requiere_lambda_mayor_mu():
    offspring_x = np.zeros((3, 2))
    offspring_sigma = np.full(3, 0.5)
    offspring_fitness = np.array([0.1, 0.2, 0.3])
    with pytest.raises(ValueError):
        select_comma(offspring_x, offspring_sigma, offspring_fitness, mu=3)


def test_select_comma_ordena_desc():
    offspring_x = np.arange(20, dtype=float).reshape(10, 2)
    offspring_sigma = np.full(10, 0.5)
    offspring_fitness = np.linspace(0.1, 1.0, 10)
    _, _, f = select_comma(offspring_x, offspring_sigma, offspring_fitness, mu=3)
    assert f.tolist() == sorted(f.tolist(), reverse=True)
    assert len(f) == 3
    assert f[0] == pytest.approx(1.0)
