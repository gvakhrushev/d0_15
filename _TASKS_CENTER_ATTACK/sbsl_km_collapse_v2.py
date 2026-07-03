#!/usr/bin/env python3
"""KM collapse v2: caveat-(ii) closure. Long runs (600 collapses) at phi and 3/2 + Monte-Carlo
finite-sample entropy reference for the uniform distribution at matched n. If phi's entropy sits
inside the uniform reference band, equidistribution is quantitatively supported at this n."""
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

def ent36(ph, n=None):
    hist, _ = np.histogram(ph if n is None else ph[:n], bins=36, range=(0, 2*np.pi))
    p = hist/hist.sum(); p = p[p > 0]
    return -(p*np.log(p)).sum()/np.log(36)

def collapse_phases(ratio, p2, n_trans=50, n_meas=650):
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
    return (w2*np.array(times)) % (2*np.pi)

phi = (1+5**0.5)/2
rng = np.random.default_rng(12345)
for lab, r in [("PHI", round(phi,6)), ("3/2", 1.5)]:
    ph = collapse_phases(r, 0.25*p0)
    n = len(ph)
    ents = [ent36(rng.uniform(0, 2*np.pi, n)) for _ in range(400)]
    lo, hi = np.percentile(ents, [2.5, 97.5])
    e = ent36(ph)
    inside = "INSIDE" if lo <= e <= hi else "OUTSIDE"
    print(f"  {lab}: n={n}, ent={e:.4f}; uniform-reference 95% band at this n: [{lo:.4f}, {hi:.4f}] -> {inside}", flush=True)
