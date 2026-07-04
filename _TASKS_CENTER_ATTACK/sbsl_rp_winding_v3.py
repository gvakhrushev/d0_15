#!/usr/bin/env python3
"""P-SBSL-1 THEORY STEP v3 (report-only). v2 established: rigid-tracking branches w=1-frac(rho)
(single torus, tail rho>=1.66) and w=frac(rho)/2 (doubled torus, rho<1.5) hold EXACTLY; deviation
windows exist around 3/2 and phi; but w-resolution 1/N=2.5e-3 (twin-point scatter at phi) exceeded
the plateau tolerance. v3 = the decisive scan: N_meas=1600 (resolution ~6e-4), rho step 0.0025 in
two windows [1.470,1.535] (contains 3/2) and [1.595,1.648] (contains phi), twin points (+3.4e-5)
at 3/2 and phi as built-in error bars. Locking = interval with dw/drho ~ 0 (NOT rigid slopes
-1 or +1/2). Report whatever appears."""
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
win15  = list(np.round(np.arange(1.470, 1.5355, 0.0025), 4)) + [1.500034]
winphi = list(np.round(np.arange(1.595, 1.6485, 0.0025), 4)) + [round(phi,6), round(phi,6)+3.4e-5]
ctrl   = [1.44, 1.46, 1.66, 1.68, 1.70]
grid = sorted(set(win15 + winphi + ctrl))
print(f"# v3: f1={f1/1e3:.1f} kHz, N_meas=1600 (res ~6e-4), {len(grid)} pts")
print("# rho        w          x_max   frac/2    1-frac    note")
for r in grid:
    w, xm = winding(r)
    fr = r % 1.0
    note = "GOLDEN" if abs(r-phi) < 0.0001 else ("3:2" if abs(r-1.5) < 0.0001 else "")
    print(f"  {r:9.6f}  {w:+.6f}  {xm:.3f}  {fr/2:.4f}   {1-fr:.4f}   {note}", flush=True)
