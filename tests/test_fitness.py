"""Tests de la función objetivo Elipsoide Invertido."""

import numpy as np
import pytest

from src.fitness import inverted_ellipsoid


def test_optimo_global_es_uno():
    x_star = np.full(10, 2.0)
    assert inverted_ellipsoid(x_star) == pytest.approx(1.0)


def test_valor_en_cero():
    x = np.zeros(10)
    # sum((0-2)^2 / i) para i=1..10 = 4 * H_10 ≈ 4 * 2.9289 ≈ 11.7167
    # exp(-11.7167) ≈ 8.15e-6
    val = inverted_ellipsoid(x)
    assert 0.0 < val < 1.0
    assert val == pytest.approx(np.exp(-np.sum(4.0 / np.arange(1, 11))))


def test_vectorizado_batch():
    batch = np.array([np.full(10, 2.0), np.zeros(10), np.full(10, 5.0)])
    out = inverted_ellipsoid(batch)
    assert out.shape == (3,)
    assert out[0] == pytest.approx(1.0)
    assert out[0] > out[1] > out[2]


def test_dim_invalida():
    with pytest.raises(ValueError):
        inverted_ellipsoid(np.zeros((2, 3, 4)))
