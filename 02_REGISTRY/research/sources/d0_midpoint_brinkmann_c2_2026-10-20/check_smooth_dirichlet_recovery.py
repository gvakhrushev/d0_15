"""Bounded check of arbitrary smooth Dirichlet Brinkmann recovery.

This checks the NEW harmonic lift and native centered curvature readout.
The existing independently varied 40+2 theorem is consumed, not recomputed.
The continuum profile is a rational harmonic function with poles outside the
closed square; it is not a fixed finite/bandlimited exponential ansatz.
"""
import json
import math
import numpy as np
from scipy.sparse import diags, eye, kron
from scipy.sparse.linalg import splu

P = (math.sqrt(5) - 1) / 2
FUGACITY = 2.0**-20
Q = 1 - FUGACITY * 4 * P**3
R = 1 - FUGACITY * 4 * P**3 * (1 + P**6)
LAMBDA = -2 * P**-5 * (R/Q + P**6)
POLE_1 = 1.4 + 0.3j
POLE_2 = -0.6 + 1.2j


def psi(u):
    u = np.asarray(u)
    return np.stack([0.025 * np.sin(1.3 * u), 0.018 * np.cos(0.7 * u)], axis=-1)


def psi_prime(u):
    u = np.asarray(u)
    return np.stack([0.025 * 1.3 * np.cos(1.3 * u), -0.018 * 0.7 * np.sin(0.7 * u)], axis=-1)


def holomorphic(t, z, order=0):
    a = 0.03 * (1 + 0.2 * np.sin(t))
    b = 0.02 * np.cos(1.3 * t)
    return (a * (-1) ** order * math.factorial(order) / (z - POLE_1) ** (order + 1)
            - 1j * b * (-1) ** order * math.factorial(order + 1) / (z - POLE_2) ** (order + 2))


def laplacian_grid(w, h):
    return (w[2:, 1:-1] + w[:-2, 1:-1] + w[1:-1, 2:] + w[1:-1, :-2]
            - 4 * w[1:-1, 1:-1]) / h**2


def harmonic_dirichlet(boundary):
    n = boundary.shape[0] - 1
    m = n - 1
    a = diags([-np.ones(m - 1), 2 * np.ones(m), -np.ones(m - 1)], [-1, 0, 1], format="csc")
    matrix = (kron(a, eye(m), format="csc") + kron(eye(m), a, format="csc"))
    rhs = np.zeros((m, m))
    rhs[0, :] += boundary[0, 1:-1]
    rhs[-1, :] += boundary[-1, 1:-1]
    rhs[:, 0] += boundary[1:-1, 0]
    rhs[:, -1] += boundary[1:-1, -1]
    solution = boundary.copy()
    solution[1:-1, 1:-1] = splu(matrix).solve(rhs.ravel()).reshape(m, m)
    return solution


def one_mesh(n):
    h = 1 / n
    u = np.arange(n + 1) * h
    mids = (np.arange(n) + 0.5) * h
    material = np.vstack([psi(0), psi(0) + np.cumsum(h * psi_prime(mids), axis=0)])
    j = n // 2
    tau = mids[j]
    slope = (material[j + 1] - material[j]) / h
    energy = float(np.sum(psi_prime(tau)**2))
    x = np.arange(n + 1) * h
    xx, yy = np.meshgrid(x, x, indexing="ij")
    zz = xx + 1j * yy
    target_w = holomorphic(tau, zz).real
    wh = harmonic_dirichlet(target_w)
    target_h = -LAMBDA * energy * (xx**2 + yy**2) + target_w
    hh = -LAMBDA * energy * (xx**2 + yy**2) + wh

    # Original Cartan solution: K_x/h = one-half backward x difference,
    # living at x-h/2, and likewise for y.
    dx = (hh[1:, :] - hh[:-1, :]) / h
    dy = (hh[:, 1:] - hh[:, :-1]) / h
    zx = (xx[1:, :] - h/2) + 1j * yy[1:, :]
    zy = xx[:, 1:] + 1j * (yy[:, 1:] - h/2)
    target_dx = -2 * LAMBDA * energy * (xx[1:, :] - h/2) + holomorphic(tau, zx, 1).real
    target_dy = -2 * LAMBDA * energy * (yy[:, 1:] - h/2) - holomorphic(tau, zy, 1).imag
    mask_x = ((zx.real >= 0.25) & (zx.real <= 0.75) & (zx.imag >= 0.25) & (zx.imag <= 0.75))
    mask_y = ((zy.real >= 0.25) & (zy.real <= 0.75) & (zy.imag >= 0.25) & (zy.imag <= 0.75))
    link_error = 0.5 * max(np.max(np.abs(dx - target_dx)[mask_x]), np.max(np.abs(dy - target_dy)[mask_y]))

    # These are -2/h² times the coefficients of the EXACT original odd
    # nilpotent plaquette curvature, not a linearized curvature substitution.
    dxx = (hh[2:, 1:-1] - 2*hh[1:-1, 1:-1] + hh[:-2, 1:-1]) / h**2
    dyy = (hh[1:-1, 2:] - 2*hh[1:-1, 1:-1] + hh[1:-1, :-2]) / h**2
    zi = zz[1:-1, 1:-1]
    target_dxx = -2*LAMBDA*energy + holomorphic(tau, zi, 2).real
    target_dyy = -2*LAMBDA*energy - holomorphic(tau, zi, 2).real
    mask_i = ((zi.real >= 0.25) & (zi.real <= 0.75) & (zi.imag >= 0.25) & (zi.imag <= 0.75))
    dxy = (hh[1:, 1:] - hh[1:, :-1] - hh[:-1, 1:] + hh[:-1, :-1]) / h**2
    zm = (xx[:-1, :-1] + h/2) + 1j*(yy[:-1, :-1] + h/2)
    target_dxy = -holomorphic(tau, zm, 2).imag
    mask_m = ((zm.real >= 0.25) & (zm.real <= 0.75) & (zm.imag >= 0.25) & (zm.imag <= 0.75))
    curvature_error = max(np.max(np.abs(dxx-target_dxx)[mask_i]), np.max(np.abs(dyy-target_dyy)[mask_i]),
                          np.max(np.abs(dxy-target_dxy)[mask_m]))
    exact_source_residual = float(np.max(np.abs(laplacian_grid(hh, h) + 4*LAMBDA*np.sum(slope**2))))
    allowed_roundoff = 200 * np.finfo(float).eps * n**2 * max(1.0, float(np.max(np.abs(hh))))
    assert exact_source_residual < allowed_roundoff, (n, exact_source_residual, allowed_roundoff)
    assert np.max(np.abs(wh[[0, -1], :] - target_w[[0, -1], :])) == 0
    assert np.max(np.abs(wh[:, [0, -1]] - target_w[:, [0, -1]])) == 0
    return {
        "L": n,
        "native_equation_residual": exact_source_residual,
        "naive_sample_harmonic_residual": float(np.max(np.abs(laplacian_grid(target_w, h)))),
        "metric_grid_error": float(np.max(np.abs(hh-target_h))),
        "native_link_error": float(link_error),
        "native_curvature_error": float(curvature_error),
        "matter_record_error": float(np.max(np.linalg.norm(material-psi(u), axis=1))),
    }


def main():
    rows = [one_mesh(n) for n in (16, 32, 64, 128)]
    names = ("metric_grid_error", "native_link_error", "native_curvature_error", "matter_record_error")
    orders = {name: [math.log(rows[i-1][name]/rows[i][name], 2) for i in range(1, len(rows))] for name in names}
    assert all(v[-1] > 1.85 for v in orders.values()), orders
    # A hostile control: exact sampling of this fixed continuum wave is not
    # discretely harmonic. The Dirichlet lift is doing nontrivial work.
    assert rows[0]["naive_sample_harmonic_residual"] > 1e-5
    result = {"scope": "new smooth harmonic Dirichlet lift and native readout only; original all40+2 theorem consumed",
              "rows": rows, "observed_orders": orders,
              "proof_status": "numerical diagnostic; the uniform analytical proof establishes the theorem"}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
