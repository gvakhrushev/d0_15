#!/usr/bin/env python3
"""P-SBSL-1 COLLAPSE-REGIME PILOT v1 (report-only). Keller-Miksis with acoustic radiation
damping, SBSL-grade drive (p1=1.25 atm @ 26.5 kHz, R0=4.5 um) + second tone p2=0.25 atm at
f2 = rho*f1. THE pre-registered observable: the flash/collapse PHASE against tone 2 —
theta_k = (w2 * t_k) mod 2pi at main-collapse events t_k. Locked response -> theta_k occupies
few discrete values (low circular entropy); quasiperiodic -> equidistributes (high entropy).
Pilot grid: 3/2, 8/5, 13/8, phi, sqrt2, generic 1.55. Control leg: single-tone periodicity."""
import numpy as np
from scipy.integrate import solve_ivp

rho_w, mu, sig, p0, kappa, c = 998.0, 1.002e-3, 0.0725, 101325.0, 1.4, 1481.0
R0 = 4.5e-6
f1 = 26.5e3; w1 = 2*np.pi*f1; T1 = 1/f1
p1 = 1.25*p0
pg0 = p0 + 2*sig/R0

def make_rhs(w2, p2):
    def pdrv(t):  return p1*np.sin(w1*t) + (p2*np.sin(w2*t) if p2 else 0.0)
    def dpdrv(t): return p1*w1*np.cos(w1*t) + (p2*w2*np.cos(w2*t) if p2 else 0.0)
    def rhs(t, y):
        R, Rd = y
        M = Rd/c
        pg  = pg0*(R0/R)**(3*kappa)
        dpg = -3*kappa*pg/R*Rd
        ps  = pg - 2*sig/R - 4*mu*Rd/R
        pL  = ps - p0 - pdrv(t)
        # KM: (1-M) R Rdd + 1.5(1-M/3) Rd^2 = (1+M) pL/rho + R/(rho c) d(ps - pdrv)/dt
        # d(ps)/dt approx dpg + 2 sig Rd/R^2 + 4 mu Rd^2/R^2 (drop Rdd viscous term, standard)
        dps = dpg + 2*sig*Rd/R**2 + 4*mu*Rd**2/R**2
        num = (1+M)*pL/rho_w + R*(dps - dpdrv(t))/(rho_w*c) - 1.5*(1-M/3)*Rd*Rd
        return [Rd, num/((1-M)*R)]
    return rhs

def collapse_phases(ratio, p2, n_trans=50, n_meas=200):
    w2 = ratio*w1 if p2 else 0.0
    t_end = (n_trans+n_meas)*T1
    sol = solve_ivp(make_rhs(w2, p2), [0, t_end], [R0, 0.0], method='LSODA',
                    rtol=1e-10, atol=[1e-13, 1e-4], max_step=T1/200, dense_output=False,
                    t_eval=np.linspace(0, t_end, (n_trans+n_meas)*400))
    if not sol.success: return None
    R = sol.y[0]; t = sol.t
    mask = t > n_trans*T1
    # main collapses: local minima below 0.6 R0, separated by > 0.5 T1
    Rm, tm = R[mask], t[mask]
    idx = np.where((Rm[1:-1] < Rm[:-2]) & (Rm[1:-1] < Rm[2:]) & (Rm[1:-1] < 0.6*R0))[0] + 1
    times = []
    for i in idx:
        if not times or tm[i] - times[-1] > 0.5*T1: times.append(tm[i])
    times = np.array(times)
    if len(times) < 20: return dict(n=len(times), ent=np.nan, nbins=0, rmin=Rm.min()/R0, times=times)
    ph = (w2*times) % (2*np.pi) if p2 else (w1*times) % (2*np.pi)
    # circular entropy over 36 bins, normalized: 1 = uniform, 0 = single bin
    hist, _ = np.histogram(ph, bins=36, range=(0, 2*np.pi))
    p = hist/hist.sum(); p = p[p > 0]
    ent = -(p*np.log(p)).sum()/np.log(36)
    return dict(n=len(times), ent=ent, nbins=int((hist > 0).sum()), rmin=Rm.min()/R0, times=times)

print("# KM collapse pilot: R0=4.5um, f1=26.5kHz, p1=1.25p0; entropy over 36 phase bins (1=uniform)")
print("## control: single-tone (phase vs tone 1 - expect locked, few bins)")
r = collapse_phases(0.0, 0.0)
print(f"  single-tone: n_collapses={r['n']}, R_min={r['rmin']:.3f} R0, ent={r['ent']:.3f}, bins={r['nbins']}", flush=True)
phi = (1+5**0.5)/2
print("## two-tone p2=0.25 p0, phase vs tone 2")
for rho_r, lab in [(1.5, "3/2"), (1.6, "8/5"), (1.625, "13/8"), (round(phi,6), "PHI"),
                   (round(2**0.5,6), "sqrt2"), (1.55, "generic 1.55")]:
    r = collapse_phases(rho_r, 0.25*p0)
    if r is None: print(f"  {lab}: INTEGRATION FAILED", flush=True); continue
    print(f"  {lab:12s} rho={rho_r:.6f}: n={r['n']}, R_min={r['rmin']:.3f}, ent={r['ent']:.3f}, bins={r['nbins']}", flush=True)
