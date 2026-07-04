#!/usr/bin/env python3
"""P-SBSL-1 THEORY STEP v6 (report-only): tongue WIDTH vs second-tone amplitude — the
golden-last-locked ordering test. For each p2 in {0.15,0.35,0.60}p0 and each rational
rho* in {3/2, 8/5, 13/8}: verify lock at rho* (cluster test), then log-bisect the RIGHT
tongue edge delta+ = sup{d : rho*+d locked} to factor ~2. Golden control at each p2:
phi and phi +/- 2.5e-4 must all be non-locked. Reduced cost per point (n_trans=1200,
n_meas=320) — factor-2 edge accuracy accepted, caveat recorded."""
import numpy as np
from scipy.integrate import solve_ivp

rho_w, mu, sig, p0, kappa = 998.0, 1.002e-3, 0.0725, 101325.0, 1.4
R0 = 10e-6
pg0 = p0 + 2*sig/R0
w0 = np.sqrt((3*kappa*pg0 - 2*sig/R0)/(rho_w*R0**2))
f1 = 0.8*w0/(2*np.pi); w1 = 2*np.pi*f1; T1 = 1/f1
p1 = 0.80*p0

def diagnose(ratio, p2, n_trans=1200, n_meas=320):
    def rhs(t, y, w2):
        R, Rd = y
        p_ac = p1*np.sin(w1*t) + p2*np.sin(w2*t)
        pg = pg0*(R0/R)**(3*kappa)
        return [Rd, (pg - p0 - p_ac - 4*mu*Rd/R - 2*sig/R)/(rho_w*R) - 1.5*Rd*Rd/R]
    ts = np.arange(n_trans, n_trans+n_meas)*T1
    sol = solve_ivp(rhs, [0, ts[-1]], [R0, 0.0], args=(ratio*w1,), t_eval=ts,
                    method='LSODA', rtol=1e-8, atol=[1e-13, 1e-7], max_step=T1/100)
    if not sol.success or sol.y.shape[1] < n_meas: return np.nan, {}
    x = (sol.y[0]-R0)/R0; v = sol.y[1]/(R0*w1)
    th = np.unwrap(np.arctan2(v-v.mean(), x-x.mean()))
    w = (th[-1]-th[0])/(2*np.pi*(len(ts)-1))
    pts = np.column_stack([x, v]); diam = np.ptp(x) + np.ptp(v)
    if diam < 1e-9: return w, {q: 0.0 for q in (2,4,5,8,13)}   # point attractor = trivial lock
    rq = {q: max(np.ptp(pts[i::q,0]) + np.ptp(pts[i::q,1]) for i in range(q))/diam for q in (2,4,5,8,13)}
    return w, rq

def locked(ratio, p2, q):
    w, rq = diagnose(ratio, p2)
    return (rq.get(q, 1.0) < 0.05), w, rq.get(q, float('nan'))

RATS = [(1.5, 4, "3/2"), (1.6, 5, "8/5"), (1.625, 8, "13/8")]
phi = (1+5**0.5)/2
print("# v6 tongue widths vs p2 (right edge, log-bisection to factor ~2; p1=0.80 p0 fixed)")
for a2 in (0.15, 0.35, 0.60):
    p2 = a2*p0
    print(f"\n## p2 = {a2:.2f} p0")
    for r0, q, lab in RATS:
        ok0, w_c, r_c = locked(r0, p2, q)
        if not ok0:
            print(f"  {lab}: NOT locked at exact point (r_{q}={r_c:.3f}, w={w_c:+.5f}) -> width 0 or attractor changed", flush=True)
            continue
        lo, hi = 0.0, 1e-2                      # lo = last known locked offset, hi = first known unlocked
        okh, _, _ = locked(r0+hi, p2, q)
        if okh:
            print(f"  {lab}: still locked at +1e-2 (!) width > 1e-2", flush=True); continue
        # log bisection between 1e-5 and hi
        lo = 1e-5
        okl, _, _ = locked(r0+lo, p2, q)
        if not okl:
            print(f"  {lab}: locked at point, unlocked at +1e-5 -> width(+) < 1e-5", flush=True); continue
        while hi/lo > 2.0:
            mid = (lo*hi)**0.5
            okm, _, _ = locked(r0+mid, p2, q)
            if okm: lo = mid
            else: hi = mid
        print(f"  {lab}: width(+) in [{lo:.2e}, {hi:.2e}]", flush=True)
    # golden control
    gs = []
    for dr in (-2.5e-4, 0.0, 2.5e-4):
        w_g, rq_g = diagnose(phi+dr, p2)
        rmin = min(rq_g.values()) if rq_g else float('nan')
        gs.append(f"{w_g:+.5f}/{rmin:.3f}")
    print(f"  GOLDEN phi-2.5e-4, phi, phi+2.5e-4 (w / min_q r_q): {', '.join(gs)}", flush=True)
