#!/usr/bin/env python3
"""v5b: cluster test at the OTHER Fibonacci convergent 8/5=1.600 (v3 fingerprint w=0.19998~1/5)
and at 3/2 exactly (branch crossing vs 2/4-cluster lock). Same diagnostic as v5, q in {2,4,5,8}."""
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
    pts = np.column_stack([x, v]); diam = np.ptp(x) + np.ptp(v)
    rq = {q: max(np.ptp(pts[i::q,0]) + np.ptp(pts[i::q,1]) for i in range(q))/diam for q in (2,4,5,8)}
    return w, rq

print("# rho        w          r2      r4      r5      r8      case")
for r, lab in [(1.600000, "8/5 exact"), (1.600500, "8/5 + 5e-4"), (1.599500, "8/5 - 5e-4"),
               (1.500000, "3/2 exact"), (1.666667, "5/3 exact")]:
    w, rq = diagnose(r)
    print(f"  {r:9.6f}  {w:+.6f}  {rq[2]:.4f}  {rq[4]:.4f}  {rq[5]:.4f}  {rq[8]:.4f}  {lab}", flush=True)
