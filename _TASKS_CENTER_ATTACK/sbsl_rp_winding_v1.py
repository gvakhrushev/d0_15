#!/usr/bin/env python3
"""P-SBSL-1 THEORY STEP v1 (report-only; the prediction was FROZEN before this computation).
Two-tone driven Rayleigh-Plesset bubble: stroboscopic rotation number w(rho) across the drive
ratio rho = f2/f1. Expected under the frozen prediction: locking plateaus (Arnold tongues) at
rational rho, no plateau at the golden ratio. First quasiperiodically-forced bubble winding
computation (literature null confirmed by scout). Moderate drive (below SBSL collapse regime) --
the locking structure, not the light emission, is the object."""
import numpy as np
from scipy.integrate import solve_ivp

rho_w, mu, sig, p0, kappa = 998.0, 1.002e-3, 0.0725, 101325.0, 1.4
R0 = 5e-6
f1 = 26.5e3; w1 = 2*np.pi*f1; T1 = 1/f1
p1, p2 = 0.50*p0, 0.30*p0
pg0 = p0 + 2*sig/R0

def rhs(t, y, w2):
    R, Rd = y
    p_ac = p1*np.sin(w1*t) + p2*np.sin(w2*t)
    pg = pg0*(R0/R)**(3*kappa)
    Rdd = (pg - p0 - p_ac - 4*mu*Rd/R - 2*sig/R)/(rho_w*R) - 1.5*Rd*Rd/R
    return [Rd, Rdd]

def rotation_number(ratio, n_trans=150, n_meas=250):
    w2 = ratio*w1
    T_end = (n_trans+n_meas)*T1
    ts = np.arange(n_trans, n_trans+n_meas)*T1
    sol = solve_ivp(rhs, [0, T_end], [R0, 0.0], args=(w2,), t_eval=ts,
                    method='LSODA', rtol=1e-9, atol=[1e-12, 1e-6], max_step=T1/50)
    if not sol.success: return np.nan
    x = (sol.y[0]-R0)/R0
    v = sol.y[1]*T1/R0
    th = np.unwrap(np.arctan2(v, x))
    return (th[-1]-th[0])/(2*np.pi*(len(ts)-1))

phi = (1+5**0.5)/2
grid = sorted(set(list(np.round(np.linspace(1.40, 1.72, 17), 4)) +
                  [1.49, 1.495, 1.50, 1.505, 1.51, round(phi,6), 1.615, 1.62, round(2**0.5,6)]))
print(f"# rho    w(rho)      note")
prev = None
for r in grid:
    w = rotation_number(r)
    note = ""
    if abs(r-1.5) < 0.02: note = "<- near 3:2"
    if abs(r-phi) < 0.005: note = "<- GOLDEN"
    if abs(r-2**0.5) < 0.005: note = "<- sqrt2"
    print(f"{r:8.4f} {w:+.6f}  {note}")
