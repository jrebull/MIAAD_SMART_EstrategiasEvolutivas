"""Función objetivo: Elipsoide Invertido (MAXIMIZACIÓN)."""

from __future__ import annotations

import numpy as np


def inverted_ellipsoid(x: np.ndarray) -> np.ndarray | float:
    """Evalúa el Elipsoide Invertido.

    $$f(x) = \\exp\\left(-\\sum_{i=1}^{D} \\frac{(x_i - 2.0)^2}{i}\\right)$$

    Acepta un único vector de shape (D,) o un batch de shape (N, D) y en
    ese caso devuelve un arreglo de shape (N,). El óptimo global está en
    x* = (2, 2, ..., 2) con f(x*) = 1.0.

    Args:
        x: Vector de decisión de shape (D,) o matriz (N, D).

    Returns:
        Float si x es 1D o np.ndarray (N,) si x es 2D.
    """
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        D = x.shape[0]
        i = np.arange(1, D + 1, dtype=float)
        return float(np.exp(-np.sum((x - 2.0) ** 2 / i)))
    if x.ndim == 2:
        D = x.shape[1]
        i = np.arange(1, D + 1, dtype=float)
        return np.exp(-np.sum((x - 2.0) ** 2 / i, axis=1))
    raise ValueError(f"Se esperaba x de dimensión 1 o 2, se obtuvo ndim={x.ndim}")
