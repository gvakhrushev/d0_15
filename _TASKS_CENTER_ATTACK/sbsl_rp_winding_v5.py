#!/usr/bin/env python3
"""P-SBSL-1 THEORY STEP v5 (report-only) — the decisive attractor-type diagnostic.
v4 showed: no clean 1/4 plateau at 5e-4 step; three rho values reproduce w=0.24985 to 2e-6
(locked-orbit signature: offset -1.5e-4 = finite-strobe edge effect) while neighbors wander
(coexisting torus OR unconverged transients). v5 decides: (a) long transient n_trans=2000;
(b) CLUSTER TEST — a period-q locked orbit strobes onto q tight clusters (ratio -> 0), a torus
strobes onto a curve (ratio O(1)). ratio_q := max over clusters (index mod q) of cluster diameter,
divided by attractor diameter."""
import numpy as np
from scipy.integrate import solve_ivp

rho_w, mu, sig, p0, kappa = 998.0, 1.002e-3, 0.0725, 101325.0, 1.4
R0 = 10e-6
pg0 = p0 + 2*sig/R0
w0 = np.sqrt((3*kappa*pg0 - 2*sig/R0)/(rho_w*R0**2))
f1 = 0.8*w0/(2*np.pi); w1 = 2*np.pi*f1; T1 = 1/f1
p1, p2 = 0.80*p0, 0.35*p0

def rhs(t, y, w2):
    R, Rd = y
    p_ac = p1*np.sin(w1*t) + p2*np.sin(w2*t)
    pg = pg0*(R0/R)**(3*kappa)
    return [Rd, (pg - p0 - p_ac - 4*mu*Rd/R - 2*sig/R)/(rho_w*R) - 1.5*Rd*Rd/R]

def diagnose(ratio, n_trans=2000, n_meas=800):
    ts = np.arange(n_trans, n_trans+n_meas)*T1
    sol = solve_ivp(rhs, [0, ts[-1]], [R0, 0.0], args=(ratio*w1,), t_eval=ts,
                    method='LSODA', rtol=1e-8, atol=[1e-13, 1e-7], max_step=T1/100)
    x = (sol.y[0]-R0)/R0; v = sol.y[1]/(R0*w1)
    th = np.unwrap(np.arctan2(v-v.mean(), x-x.mean()))
    w = (th[-1]-th[0])/(2*np.pi*(len(ts)-1))
    pts = np.column_stack([x, v])
    diam = np.ptp(x) + np.ptp(v)
    ratios = {}
    for q in (4, 8):
        cd = max(np.ptp(pts[i::q, 0]) + np.ptp(pts[i::q, 1]) for i in range(q))
        ratios[q] = cd/diam
    return w, ratios

phi = (1+5**0.5)/2
cases = [
    (1.62500,  "13/8 exact (w~1/8 candidate)"),
    (1.62450,  "13/8 - 5e-4"),
    (1.63000,  "1/4-region repeat pt"),
    (1.63250,  "1/4-region repeat pt"),
    (1.63500,  "1/4-region repeat pt"),
    (1.63100,  "1/4-region in-between"),
    (1.63350,  "1/4-region in-between"),
    (round(phi,6), "GOLDEN"),
    (1.66000,  "rigid-torus control"),
]
print("# v5 attractor diagnostic: n_trans=2000, n_meas=800")
print("# rho        w          r4       r8       verdict guide: r_q<0.02 locked-q; both O(1) torus")
for r, lab in cases:
    w, rq = diagnose(r)
    print(f"  {r:9.6f}  {w:+.6f}  {rq[4]:.4f}   {rq[8]:.4f}   {lab}", flush=True)
