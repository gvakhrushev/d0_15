from __future__ import annotations

import numpy as np
from typing import Tuple


def eigvals_symmetric(M: np.ndarray) -> np.ndarray:
    return np.linalg.eigvalsh(M)


def heat_trace(lam: np.ndarray, t: np.ndarray) -> np.ndarray:
    # P(t) = sum exp(-t*λ)
    return np.exp(-np.outer(t, lam)).sum(axis=1)


def spectral_dimension_analytic(lam: np.ndarray, t: np.ndarray) -> np.ndarray:
    """
    dS(t) = 2 t * Tr(L e^{-tL}) / Tr(e^{-tL})
          = 2 t * sum(λ e^{-tλ}) / sum(e^{-tλ})
    No numerical gradient, no grid sensitivity.
    """
    e = np.exp(-np.outer(t, lam))
    num = (e * lam[None, :]).sum(axis=1)
    den = e.sum(axis=1)
    return 2.0 * t * (num / den)


def factorization_check(P_fib: np.ndarray, P_space: np.ndarray, P_scene: np.ndarray) -> Tuple[float, float]:
    err_abs = float(np.max(np.abs(P_fib - P_space * P_scene)))
    rel = np.abs(P_fib - P_space * P_scene) / np.maximum(1e-300, np.abs(P_fib))
    err_rel = float(np.max(rel))
    return err_abs, err_rel
