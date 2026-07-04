#!/usr/bin/env python3
"""P-SBSL-1 THEORY STEP v2 (report-only). v1 lesson recorded: sub-resonance quasistatic regime
(5um bubble @ 26.5kHz = f0/25) has NO winding (w~1e-4) -- the tongue-bearing regime is the
near-resonance nonlinear one (Parlitz-Lauterborn winding numbers, published for SINGLE-tone).
v2 = the two-tone extension nobody has computed:
  leg V (validation): single-tone winding vs drive amplitude at fixed f1 -- machinery check
  leg M (main): two-tone, rotation number w(rho) across rho=f2/f1 with dense grids at 3/2 and phi.
Diagnostic fixed: angle unwrapped about the strobed CENTROID."""
import numpy as np
from scipy.integrate import solve_ivp

rho_w, mu, sig, p0, kappa = 998.0, 1.002e-3, 0.0725, 101325.0, 1.4
R0 = 10e-6
pg0 = p0 + 2*sig/R0
# linearized natural frequency (with surface-tension correction)
w0 = np.sqrt((3*kappa*pg0 - 2*sig/R0)/(rho_w*R0**2))
f0 = w0/(2*np.pi)
f1 = 0.8*f0; w1 = 2*np.pi*f1; T1 = 1/f1

def rhs(t, y, w2, p1, p2):
    R, Rd = y
    p_ac = p1*np.sin(w1*t) + (p2*np.sin(w2*t) if p2 else 0.0)
    pg = pg0*(R0/R)**(3*kappa)
    Rdd = (pg - p0 - p_ac - 4*mu*Rd/R - 2*sig/R)/(rho_w*R) - 1.5*Rd*Rd/R
    return [Rd, Rdd]

def winding(p1, p2, ratio, n_trans=300, n_meas=400):
    """rotation number of strobed (R,Rdot) about its centroid, per drive-1 period; + amplitude"""
    w2 = ratio*w1 if p2 else 0.0
    ts = np.arange(n_trans, n_trans+n_meas)*T1
    sol = solve_ivp(rhs, [0, ts[-1]], [R0, 0.0], args=(w2, p1, p2), t_eval=ts,
                    method='LSODA', rtol=1e-8, atol=[1e-13, 1e-7], max_step=T1/100)
    if not sol.success or sol.y.shape[1] < n_meas: return np.nan, np.nan
    x = (sol.y[0]-R0)/R0
    v = sol.y[1]/(R0*w1)
    xc, vc = x.mean(), v.mean()
    th = np.unwrap(np.arctan2(v-vc, x-xc))
    return (th[-1]-th[0])/(2*np.pi*(len(ts)-1)), x.max()

print(f"# f0 = {f0/1e3:.1f} kHz, f1 = 0.8 f0 = {f1/1e3:.1f} kHz, R0 = {R0*1e6:.0f} um")
print("\n## LEG V: single-tone winding vs amplitude (machinery validation vs Parlitz-type structure)")
print("# p1/p0   w          x_max")
for a in [0.30, 0.50, 0.70, 0.80, 0.90, 1.00, 1.10]:
    w, xm = winding(a*p0, 0.0, 0.0)
    print(f"  {a:.2f}  {w:+.6f}  {xm:.3f}")

phi = (1+5**0.5)/2
coarse = list(np.round(np.arange(1.40, 1.725, 0.02), 3))
dense15  = list(np.round(np.arange(1.47, 1.5325, 0.005), 4))
densephi = list(np.round(np.arange(1.588, 1.6505, 0.005), 4)) + [round(phi, 6)]
grid = sorted(set(coarse + dense15 + densephi))
print(f"\n## LEG M: two-tone p1=0.80 p0, p2=0.35 p0, rho scan ({len(grid)} pts)")
print("# rho      w          x_max   note")
rows = []
for r in grid:
    w, xm = winding(0.80*p0, 0.35*p0, r)
    note = "GOLDEN" if abs(r-phi) < 0.004 else ("3:2" if abs(r-1.5) < 0.011 else "")
    rows.append((r, w))
    print(f"  {r:7.4f}  {w:+.6f}  {xm:.3f}  {note}", flush=True)

print("\n## plateau detector (|dw| < 2e-3 across >=3 consecutive pts)")
runs, cur = [], [rows[0]]
for a, b in zip(rows, rows[1:]):
    if np.isfinite(a[1]) and np.isfinite(b[1]) and abs(b[1]-a[1]) < 2e-3: cur.append(b)
    else:
        if len(cur) >= 3: runs.append(cur)
        cur = [b]
if len(cur) >= 3: runs.append(cur)
for run in runs:
    lo, hi = run[0][0], run[-1][0]
    wm = np.mean([w for _, w in run])
    tag = " <- contains 3/2" if lo <= 1.5 <= hi else (" <- contains GOLDEN" if lo <= phi <= hi else "")
    print(f"  rho in [{lo:.4f}, {hi:.4f}]  width {hi-lo:.4f}  w_mean {wm:+.6f}{tag}")
