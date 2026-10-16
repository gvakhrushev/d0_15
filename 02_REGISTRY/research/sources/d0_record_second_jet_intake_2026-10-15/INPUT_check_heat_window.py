#!/usr/bin/env python3
"""Heat window test: beta = h = 1/L limit gives 15/32. Vectorized."""
import json
import numpy as np
from numpy import pi, sin, exp, log, sqrt, sum, cos

def compute_dH_dt(L, beta=None):
    """Compute dH/dt at t=0 for q(t) = diag(4e^{2t}, e^{-2t}/4, 1, 1)."""
    if beta is None:
        beta = 1.0 / L

    q = np.array([4.0, 0.25, 1.0, 1.0])
    # d/dt(1/q_r) at t=0
    d_inv_q = np.array([-0.5, 8.0, 0.0, 0.0])

    k = np.arange(L)
    # For each axis r, compute Z_r and dZ_r/dt
    Z_r = np.zeros(4)
    dZ_r = np.zeros(4)

    for r in range(4):
        lam_r = 4.0 * L**2 * sin(pi * k / L)**2 / q[r]
        e_r = exp(-beta * lam_r)
        Z_r[r] = np.sum(e_r)
        dlam_r_dt = 4.0 * L**2 * sin(pi * k / L)**2 * d_inv_q[r]
        dZ_r[r] = np.sum(e_r * (-beta * dlam_r_dt))

    Z = np.prod(Z_r)
    # dZ/dt = Z * sum_r (1/Z_r) * dZ_r/dt
    dZ_dt = Z * np.sum(dZ_r / Z_r)

    dH_dt = (1.0 / beta) * (1.0 / Z) * dZ_dt
    return dH_dt

print("Testing heat window limit...")
for L in [4, 8, 16, 32, 64, 128, 256, 512, 1024]:
    beta = 1.0 / L
    dH = compute_dH_dt(L, beta)
    print(f"L={L:5d}, beta=1/L, dH/dt = {dH:.10f}, diff = {dH - 15/32:.10f}")

print(f"\nExpected: 15/32 = {15/32:.10f}")

# Save
results = {str(L): compute_dH_dt(L, 1.0/L) for L in [4,8,16,32,64,128,256,512,1024]}
with open('/home/user/outputs/heat_window_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nSaved to heat_window_results.json")
