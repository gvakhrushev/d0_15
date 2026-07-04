#!/usr/bin/env python3
"""KM collapse v3: WIDTH of the flash-phase discretization window around 3/2 — the experimental
design number for P-SBSL-1 (how fine must the drive-ratio grid be in the collapse regime).
Entropy(rho) at offsets +/-{1e-3, 3e-3, 1e-2, 3e-2} around 1.5, phi reference. Same pipeline as
v1/v2 (validated)."""
import numpy as np
from scipy.integrate import solve_ivp

rho_w, mu, sig, p0, kappa, c = 998.0, 1.002e-3, 0.0725, 101325.0, 1.4, 1481.0
R0 = 4.5e-6
f1 = 26.5e3; w1 = 2*np.pi*f1; T1 = 1/f1
p1 = 1.25*p0
pg0 = p0 + 2*sig/R0

def make_rhs(w2, p2):
    def pdrv(t):  return p1*np.sin(w1*t) + p2*np.sin(w2*t)
    def dpdrv(t): return p1*w1*np.cos(w1*t) + p2*w2*np.cos(w2*t)
    def rhs(t, y):
        R, Rd = y
        M = Rd/c
        pg  = pg0*(R0/R)**(3*kappa)
        dpg = -3*kappa*pg/R*Rd
        ps  = pg - 2*sig/R - 4*mu*Rd/R
        pL  = ps - p0 - pdrv(t)
        dps = dpg + 2*sig*Rd/R**2 + 4*mu*Rd**2/R**2
        num = (1+M)*pL/rho_w + R*(dps - dpdrv(t))/(rho_w*c) - 1.5*(1-M/3)*Rd*Rd
        return [Rd, num/((1-M)*R)]
    return rhs

def ent_at(ratio, p2=0.25*p0, n_trans=50, n_meas=300):
    w2 = ratio*w1
    t_end = (n_trans+n_meas)*T1
    sol = solve_ivp(make_rhs(w2, p2), [0, t_end], [R0, 0.0], method='LSODA',
                    rtol=1e-10, atol=[1e-13, 1e-4], max_step=T1/200,
                    t_eval=np.linspace(0, t_end, (n_trans+n_meas)*400))
    R = sol.y[0]; t = sol.t
    mask = t > n_trans*T1
    Rm, tm = R[mask], t[mask]
    idx = np.where((Rm[1:-1] < Rm[:-2]) & (Rm[1:-1] < Rm[2:]) & (Rm[1:-1] < 0.6*R0))[0] + 1
    times = []
    for i in idx:
        if not times or tm[i] - times[-1] > 0.5*T1: times.append(tm[i])
    ph = (w2*np.array(times)) % (2*np.pi)
    hist, _ = np.histogram(ph, bins=36, range=(0, 2*np.pi))
    p = hist/hist.sum(); p = p[p > 0]
    return -(p*np.log(p)).sum()/np.log(36), len(times)

print("# KM v3: entropy vs offset from 3/2 (window width of flash-phase discretization)")
print("# rho        ent     n_collapses")
phi = (1+5**0.5)/2
for r in [1.47, 1.49, 1.497, 1.499, 1.5, 1.501, 1.503, 1.51, 1.53, round(phi,6)]:
    e, n = ent_at(r)
    lab = "PHI ref" if abs(r-phi) < 1e-4 else ""
    print(f"  {r:9.6f}  {e:.4f}  {n}  {lab}", flush=True)
