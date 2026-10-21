#!/usr/bin/env python3
"""34-readout vs isospectral master-action control; standard library only."""
import json
import math
import random

N = 17
D = 2 * N
PHI = (1.0 + math.sqrt(5.0))/2.0
P = 1.0/PHI
C = P*P
Z = 0.5
ALPHA = Z*C
BETA = 1.0
A = 0.3
B = 1.7

def q_formula(t):
    assert len(t) == D
    x, y = t[:N], t[N:]
    den = 2.0*(1.0 + sum(v*v for v in t))
    return [(1.0 + 2.0*x[j] + x[j]*x[j] + y[j]*y[j])/den
            for j in range(N)] + [
            (1.0 + 2.0*y[j] + x[j]*x[j] + y[j]*y[j])/den
            for j in range(N)]

def q_born(t):
    x, y = t[:N], t[N:]
    normal = math.sqrt(1.0 + sum(v*v for v in t))
    psi = [complex(1.0 / normal)] + [
        complex(x[j], y[j])/normal for j in range(N)]
    s = 1.0 / math.sqrt(2.0)
    return [abs(s*(psi[0]+psi[j+1]))**2 for j in range(N)] + [
        abs(s*(psi[0]-1j*psi[j+1]))**2 for j in range(N)]

def bootstrap_isospectral(t):
    # Exact spectral formula for d_P=sqrt(A)*P+sqrt(B)*(I-P)
    # on C^18(grade 0) -> C^18(grade 1).
    # Heat Hodge eigenvalues A (twice), B (34-fold).
    assert len(t) == D
    zheat = 2.0*math.exp(-BETA*A) + 34.0*math.exp(-BETA*B)
    det = (1.0-Z*C)**2
    return math.log(zheat)/BETA - math.log(det)

def anchored_feedback(t):
    # 34 addressed binary tests, each with q and 1-q return ports.
    return -sum(math.log1p(-ALPHA*q)+math.log1p(-ALPHA*(1.0-q))
                for q in q_formula(t))

def axis(j, h):
    v = [0.0]*D
    v[j] = h
    return v

def main():
    zero = [0.0]*D
    checks = 0
    # Born effect identity for all 34 R/I settings.
    probes = [zero]
    rng = random.Random(20261021)
    probes += [[rng.uniform(-0.23, 0.23) for _ in range(D)] for _ in range(20)]
    for t in probes:
        for q1, q2 in zip(q_born(t), q_formula(t)):
            assert abs(q1-q2) < 4e-15
            checks += 1
    # Entire 34 x 34 Jacobian at zero: analytic identity, finite check.
    h = 1e-6
    for j in range(D):
        plus, minus = q_formula(axis(j, h)), q_formula(axis(j,-h))
        for k in range(D):
            val = (plus[k]-minus[k])/(2.0*h)
            assert abs(val-(1.0 if j==k else 0.0)) < 2e-9
            checks += 1
    # Bootstrap identically flat even though all q respond.
    base = bootstrap_isospectral(zero)
    for t in probes:
        assert bootstrap_isospectral(t) == base
        checks += 1
    # Anchor: exact stationarity and positive full Hessian.
    kappa = 2.0*ALPHA**2/(1.0-ALPHA/2.0)**2
    s0 = anchored_feedback(zero)
    h = 0.002
    for j in range(D):
        sp, sm = anchored_feedback(axis(j,h)),anchored_feedback(axis(j,-h))
        grad = (sp-sm)/(2.0*h)
        sec = (sp+sm-2*s0)/(h*h)
        assert abs(grad) < 2e-11
        assert abs(sec-kappa) < 1e-5
        checks += 2
    for _ in range(12):
        v=[rng.uniform(-0.2,0.2) for _ in range(D)]
        sp,sm = anchored_feedback([h*u for u in v]),anchored_feedback([-h*u for u in v])
        sec=(sp+sm-2*s0)/(h*h)
        pred=kappa*sum(u*u for u in v)
        assert abs(sec-pred)<3e-5, (sec,pred)
        checks +=1
    print(json.dumps({"status":"PASS", "checks":checks, "born_jacobian_rank":34,
        "master_isospectral_derivative":0,"anchor_hessian_rank":34,
        "alpha":round(ALPHA,15),"anchor_hessian_eigenvalue":round(kappa,15)},
        sort_keys=True))

if __name__ == "__main__":
    main()
