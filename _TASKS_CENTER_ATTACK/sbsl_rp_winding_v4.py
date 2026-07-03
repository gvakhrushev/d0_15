#!/usr/bin/env python3
"""P-SBSL-1 THEORY STEP v4 (report-only). v3 found: (i) genuine w=1/4 subharmonic tongue
[~1.628,~1.636] (variation 2e-6, frozen amplitude); (ii) NO lock at golden (twins reproducible,
w wandering); (iii) 3/2 = rigid branch crossing frac/2 <-> (1-frac)/2, no tongue; (iv) single-point
candidate w=1/8 lock AT 13/8=1.625 (Fibonacci convergent). v4 = fine structure at step 5e-4:
tongue edges, the 13/8 window, the golden window. Output: tongue widths vs golden upper bound."""
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

def winding(ratio, n_trans=400, n_meas=1600):
    ts = np.arange(n_trans, n_trans+n_meas)*T1
    sol = solve_ivp(rhs, [0, ts[-1]], [R0, 0.0], args=(ratio*w1,), t_eval=ts,
                    method='LSODA', rtol=1e-8, atol=[1e-13, 1e-7], max_step=T1/100)
    if not sol.success or sol.y.shape[1] < n_meas: return np.nan, np.nan
    x = (sol.y[0]-R0)/R0; v = sol.y[1]/(R0*w1)
    th = np.unwrap(np.arctan2(v-v.mean(), x-x.mean()))
    return (th[-1]-th[0])/(2*np.pi*(len(ts)-1)), x.max()

phi = (1+5**0.5)/2
wA = list(np.round(np.arange(1.6270, 1.63825, 0.0005), 5))   # 1/4-tongue edges
wB = list(np.round(np.arange(1.6235, 1.62675, 0.0005), 5))   # 13/8 = 1.625 window
wC = list(np.round(np.arange(1.6155, 1.62075, 0.0005), 5))   # golden window
grid = sorted(set(wA + wB + wC))
print(f"# v4 fine structure, step 5e-4, {len(grid)} pts; locks flagged |w - p/q| < 6e-4 (q<=8)")
locks = [(1,4),(1,8),(3,16),(1,5),(1,6),(3,8),(1,3),(2,7),(3,14),(5,16)]
print("# rho        w          x_max   lock?")
for r in grid:
    w, xm = winding(r)
    tag = ""
    if np.isfinite(w):
        for pn, qn in locks:
            if abs(w - pn/qn) < 6e-4: tag = f"= {pn}/{qn}"; break
    star = " *13/8*" if abs(r-1.625) < 1e-9 else (" *PHI*" if abs(r-phi) < 3e-4 else "")
    print(f"  {r:9.5f}  {w:+.6f}  {xm:.3f}  {tag}{star}", flush=True)
