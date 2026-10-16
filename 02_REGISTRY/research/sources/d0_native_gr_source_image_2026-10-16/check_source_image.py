#!/usr/bin/env python3
"""Exact source-image/Einstein countercheck for the stored-adjoint D0 chart.

Research-only; no claim about physical admission, native stationary roots, or
continuum convergence. Requires SymPy. All matrix arithmetic is exact Q.
"""
import json
from itertools import combinations
from sympy import Matrix, eye, ones, diag, Rational, trace, zeros

ETA = diag(1, -1, -1, -1)
F = eye(4) + ones(4)  # F=(a-b)I+bJ, a=2, b=1, regular
Q = F * ETA * F.T
G = Q.inv()
V = ETA * F.T  # columns are the four native legs
W = V[1:4, :]   # spatial portions; 3 x 4
TAU = V[0, :].T
INDEX = [(i, j) for i in range(4) for j in range(i, 4)]


def check(test, message):
    if not test:
        raise RuntimeError(message)


def symcovector_matrix(M):
    """Tr(E dQ) as a 10-coordinate linear form, preserving offdiag factor 2."""
    return [M[i, j] if i == j else 2 * M[i, j] for i, j in INDEX]


def metric_tangents(active):
    """All allowed δu for this Fourier support, modulo observer/link gauge.

    For r active, δτ_r=0 and w_r·δw_r=0. Otherwise 4 entries free.
    Observer n and SO3 link jets do not alter the intrinsic Lorentz Gram Q.
    """
    directions = []
    for r in range(4):
        w = W[:, r]
        spatial = Matrix([list(w)]).nullspace() if r in active else list(eye(3).columnspace())
        for dw in spatial:
            dW = zeros(3, 4)
            dW[:, r] = dw
            dq = -(dW.T * W + W.T * dW)
            check(dq == dq.T, "bad symmetric Gram tangent")
            directions.append(dq)
        if r not in active:
            dtau = zeros(4, 1)
            dtau[r] = 1
            directions.append(dtau * TAU.T + TAU * dtau.T)
    return directions


def bianchi_matrix(k):
    qk = Q * k
    return Matrix([[sum(qk[i] * int((min(i, j), max(i, j)) == (a, b))
                        for i in range(4)) for a, b in INDEX]
                   for j in range(4)])


def linear_einstein(h, k):
    """Linearized covariant Einstein tensor on constant g=Q^-1.

    Perturbation h exp(i k x), Fourier convention ∂ -> i k.
    """
    kup = Q * k
    k2 = (k.T * Q * k)[0]
    htr = trace(Q * h)
    kh = kup.T * h
    ric = Rational(1, 2) * (k2 * h + (k * k.T) * htr - k * kh - kh.T * k.T)
    return ric - Rational(1, 2) * G * trace(Q * ric)


def check_similarity():
    # Exact finite similarity: not an independent physical weight variation.
    D = diag(1, 2, 3)
    rho = diag(Rational(1, 2), Rational(1, 3), Rational(1, 6))
    I = eye(3)
    I[0, 1] = Rational(1, 7)
    Din = I * D * I.inv()
    rin = I * rho * I.inv()
    check(trace(rho * D**2) == trace(rin * Din**2), "matter trace similarity failed")
    check(trace(D**4) == trace(Din**4), "heat spectral moment similarity failed")
    return True


def check_null_wave():
    # e=I+H N, H=x^2+y^2; det e=1 and native own-leg rule holds.
    from sympy import symbols, diff, simplify
    t, x, y, z = symbols('t x y z')
    coords = (t, x, y, z)
    H = x*x + y*y
    N = zeros(4)
    N[0, 0] = N[0, 3] = Rational(1, 2)
    N[3, 0] = N[3, 3] = -Rational(1, 2)
    e = eye(4) + H*N
    f = eye(4) - H*N
    nullk = Matrix([1, 0, 0, 1])
    check(N*N == zeros(4), "N not nilpotent")
    check(simplify(e*f - eye(4)) == zeros(4), "F != e^-1")
    check(e.det() == 1, "null wave volume not constant")
    check(simplify(e.T*ETA*e - ETA - H*nullk*nullk.T) == zeros(4), "null Kerr-Schild metric failed")
    check(all(diff(f[r, c], coords[r]) == 0 for r in range(4) for c in range(4)),
          "stored own-leg rule failed with A=I")
    check(diff(H, x, 2) + diff(H, y, 2) == 4, "nonvacuum control failed")
    # Independent second-derivative calculation at x=y=0. All Christoffels
    # vanish here, so the origin Ricci is the exact second-jet expression.
    gfull = e.T * ETA * e
    base = {t:0, x:0, y:0, z:0}
    check(all(simplify(diff(gfull[a,b], coord)).subs(base) == 0
              for a in range(4) for b in range(4) for coord in coords),
          "metric first jets should vanish at wave origin")
    second = [[[[simplify(diff(gfull[i,j], coords[a], coords[b])).subs(base)
                 for b in range(4)] for a in range(4)] for j in range(4)]
              for i in range(4)]
    ric0 = zeros(4)
    for m in range(4):
        for n in range(4):
            ric0[m,n] = Rational(1,2)*sum(
                ETA[a,a]*(second[a][n][a][m] + second[a][m][a][n]
                          -second[m][n][a][a] - second[a][a][m][n])
                for a in range(4))
    check(ric0 == 2*nullk*nullk.T, "Ricci second-jet computation failed")
    check(trace(ETA*ric0) == 0 and ric0 != zeros(4), "tracefree Einstein control failed")
    # Independent nonflat Ricci-flat H=x^2-y^2 curvature component.
    H_vac=x*x-y*y
    gvac=(eye(4)+H_vac*N).T*ETA*(eye(4)+H_vac*N)
    R_0101_at_origin = -Rational(1,2)*diff(gvac[0,0],x,2).subs(base)
    check(R_0101_at_origin != 0 and diff(H_vac,x,2)+diff(H_vac,y,2)==0,
          "nonflat vacuum negative control failed")
    check(diff(e[0, 0], x).subs({x:1,y:0}) != 0,
          "torsion/coframe variation unexpectedly zero")
    return {"det_e":1, "scalar_R_at_origin":0,"Ric00_at_origin":ric0[0,0],
            "volume_weight_jet":0,"vacuum_R0101_at_origin":R_0101_at_origin}


def run():
    check(F.det() == 5 and W.rank() == 3 and all(W[:,r].norm() != 0 for r in range(4)),
          "bad regular rank3 fixture")
    lam = Matrix([-4, 1, 1, 1])
    check(W*lam == zeros(3,1), "missing Gram null relation")
    checks = 0
    rank_by_support = {}
    bianchi_leftovers = {}
    for p in range(5):
        for tpl in combinations(range(4), p):
            active = set(tpl)
            dirs = metric_tangents(active)
            A = Matrix([symcovector_matrix(d) for d in dirs])
            rank = A.rank()
            expected = {0:10, 1:9, 2:8, 3:7, 4:5}[p]
            check(rank == expected, f"image rank mismatch at {tpl}: {rank} != {expected}")
            k = Matrix([int(i in active) for i in range(4)])
            B = bianchi_matrix(k) if p else zeros(0,10)
            dim = len((A.col_join(B)).nullspace())
            check(dim == (1 if p == 4 else 0), f"missing Bianchi-compatible source dimension at {tpl}")
            rank_by_support[''.join(map(str,tpl)) or '-'] = rank
            bianchi_leftovers[''.join(map(str,tpl)) or '-'] = dim
            checks += 2

    dirs = metric_tangents(set(range(4)))
    check(len(dirs)==8 and all(d[r,r]==0 and (lam.T*d*lam)[0] == 0
                              for d in dirs for r in range(4)),
          "all-active diagonal/Gram determinant lock failed")
    E = Matrix([[-54,6,6,6],[6,1,Rational(-3,2),Rational(-3,2)],
                [6,Rational(-3,2),1,Rational(-3,2)],
                [6,Rational(-3,2),Rational(-3,2),1]])
    k = ones(4,1)
    check(Q*k == Matrix([-5,-15,-15,-15]), "q k incorrect")
    check((k.T*Q*k)[0] == -50, "k^2 incorrect")
    check((Q*k).T*E == zeros(1,4), "Bianchi transversality failed")
    check(E != zeros(4) and all(trace(E*d)==0 for d in dirs),
          "source is not invisible to admitted metric directions")
    check(trace(Q*E) == -105, "traced source checksum failed")
    barh=Rational(2,1)*E/(k.T*Q*k)[0]
    h=barh - Rational(1,2)*G*trace(Q*barh)
    check(linear_einstein(h,k)==E, "E not produced by linearized Einstein")
    # Negative controls: radial leg tangent and wrong divergence break the result.
    radial = zeros(3,4)
    radial[:,0]=W[:,0]
    dr = -(radial.T*W+W.T*radial)
    check(trace(E*dr) != 0, "radial negative control not detected")
    bad = E.copy()
    bad[0,0] += 1
    check((Q*k).T*bad != zeros(1,4), "Bianchi negative control not detected")

    return {"status":"PASS","arithmetic":"exact-rational-sympy",
            "fixture":{"F":"I4 + J4","det_F":5,"rank_W":3,"lambda":list(lam),
                       "q": [list(Q.row(i)) for i in range(4)]},
            "metric_rank_by_support":rank_by_support,
            "bianchi_invisible_dim_by_support":bianchi_leftovers,
            "hidden_covector": [list(E.row(i)) for i in range(4)],
            "einstein_linear_source_exact":True,
            "radial_and_bianchi_mutations_rejected":True,
            "similarity_control":check_similarity(),
            "volume_nullwave":check_null_wave(),
            "support_checks":checks}


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, ensure_ascii=False, default=str, separators=(',',':')))
