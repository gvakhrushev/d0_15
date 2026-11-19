#!/usr/bin/env python3
"""Full K(9,11,13) global two/three-history reconstruction.

Scientific scope: positive SCALAR supported Markov transitions only. Does not
select a physical D0 action, a full128 instrument, or Lorentz Einstein law.
Requires numpy; deterministically verifies all 718 edges and 1287 triangles.
"""
import math
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import lsqr

SIZES = (9, 11, 13)
N = sum(SIZES)
A = range(0, 9)
B = range(9, 20)
C = range(20, 33)
ZONE = np.array([0] * 9 + [1] * 11 + [2] * 13)
SUPPORT = ZONE[:, None] != ZONE[None, :]
UNDIRECTED = [(i, j) for i in range(N) for j in range(i+1, N) if SUPPORT[i, j]]
assert len(UNDIRECTED) == 359 and int(SUPPORT.sum()) == 718


def primitive_cost(y):
    """A real nonreversible, nonlinear, nonconstant full 718-edge price."""
    i, j = np.indices((N, N), dtype=float)
    x = 0.18*np.sin(.317*(i+1)+.199*(j+1)) + .07*np.cos(.31*i-.07*j)
    v = .13*np.sin(.23*i+.41*j)+.08*np.cos(.37*i-.19*j)
    w = .02*np.sin(.17*i-.31*j)
    return x+y*v+.5*y*y*w, v+y*w


def from_cost(y):
    cost, dc = primitive_cost(y)
    k = np.where(SUPPORT, np.exp(cost), 0.0)
    return k, dc


def perron(k):
    """The full primitive Perron operator, not the degree-normalized walk."""
    vals, vecs = np.linalg.eig(k)
    idx = int(np.argmax(vals.real))
    lam = float(vals[idx].real)
    assert lam > 0 and abs(vals[idx].imag) < 1e-10
    r = vecs[:, idx].real
    if r.sum() < 0:
        r = -r
    assert np.min(r) > 0
    r /= math.sqrt(float(np.dot(r, r)))
    assert np.max(abs(k @ r - lam*r)) < 2e-11
    p = k*(r[None, :]/r[:, None])/lam
    assert np.max(abs(p.sum(axis=1)-1)) < 2e-11
    return lam, r, p


def stationary(p):
    # Solve the Markov stationary equation without assuming reversibility.
    mat = np.eye(N)-p.T+np.ones((N, N))/N
    pi = np.linalg.solve(mat, np.ones(N)/N)
    assert np.min(pi) > 0 and abs(pi.sum()-1) < 2e-11
    assert np.max(abs(pi @ p - pi)) < 2e-11
    return pi


def cycle_data(p):
    """359 reciprocal products and ALL 1287 oriented triangle half-affinities."""
    logp = np.zeros((N, N))
    logp[SUPPORT] = np.log(p[SUPPORT])
    b = np.zeros((N, N))
    for i, j in UNDIRECTED:
        b[i, j] = b[j, i] = .5*(logp[i, j]+logp[j, i])
    tri = np.zeros(SIZES)
    for ai, a in enumerate(A):
        for bi, bb in enumerate(B):
            for ci, c in enumerate(C):
                tri[ai, bi, ci] = .5*(
                    logp[a, bb]+logp[bb, c]+logp[c, a]
                    -logp[bb, a]-logp[c, bb]-logp[a, c])
    return b, tri


def triple_contrast(tri):
    """All 960 constraints: one each for nonbaseline a,b,c."""
    x = tri
    t = (x[1:, 1:, 1:]-x[0:1, 1:, 1:]-x[1:, 0:1, 1:]
         -x[1:, 1:, 0:1]+x[0:1, 0:1, 1:]+x[0:1, 1:, 0:1]
         +x[1:, 0:1, 0:1]-x[0, 0, 0])
    assert t.shape == (8, 10, 12)
    return float(np.max(abs(t)))


def reconstructed_p(b, tri):
    """Explicit no-fit cochain right inverse, followed by ONE Perron solve."""
    if triple_contrast(tri) > 1e-9:
        raise ValueError("triangle odds violate original additive-edge history")
    # Orient the graph A->B, B->C, C->A.  This constructive gauge
    # fixes exactly 32 unobservable vertex-potential directions.
    t = tri
    omega = np.zeros((N, N))
    for ai, a in enumerate(A):
        for bi, bb in enumerate(B):
            omega[a, bb] = t[ai, bi, 0]
    for bi, bb in enumerate(B):
        for ci, c in enumerate(C):
            omega[bb, c] = t[0, bi, ci]-t[0, bi, 0]
    for ci, c in enumerate(C):
        for ai, a in enumerate(A):
            omega[c, a] = (t[ai, 0, ci]-t[ai, 0, 0]
                            -t[0, 0, ci]+t[0, 0, 0])
    omega = omega-omega.T
    logw = np.where(SUPPORT, b+omega, 0.0)
    w = np.where(SUPPORT, np.exp(logw), 0.0)
    lam, r, p = perron(w)
    return lam, p, w


def native_feedback(p):
    pi = stationary(p)
    t = (np.sqrt(pi)[:, None]*p)/np.sqrt(pi)[None, :]
    f = np.eye(N)-t.T @ t
    # A conditional variance is positive semidefinite by the Markov property.
    assert np.linalg.eigvalsh(f)[0] > -2e-11
    z = 2.0**(-20)
    sign, logdet = np.linalg.slogdet(np.eye(N)-z*f)
    assert sign == 1.0
    return -logdet, f, t, pi


def direct_source(k, dlogk):
    """Exact analytic moving Perron + stationary-prior + feedback chain rule."""
    lam, r, p = perron(k)
    pi = stationary(p)
    dloglam = float(np.sum((pi[:, None]*p)*dlogk))
    b = np.sum(p*(dlogk-dloglam), axis=1)
    h = np.linalg.solve(np.eye(N)-p+np.outer(np.ones(N), pi), b)
    dlogp = dlogk-dloglam+h[None, :]-h[:, None]
    dp = p*dlogp
    assert np.max(abs(dp.sum(axis=1))) < 1e-10
    dpi = np.linalg.solve(np.eye(N)-p.T+np.outer(pi, np.ones(N)), dp.T @ pi)
    assert abs(dpi.sum()) < 1e-10
    j, f, t, _ = native_feedback(p)
    dt = np.sqrt(pi)[:, None]*dp/np.sqrt(pi)[None, :]
    dt += .5*t*(dpi[:, None]/pi[:, None]-dpi[None, :]/pi[None, :])
    df = -dt.T @ t - t.T @ dt
    z = 2.0**(-20)
    dj = z*np.trace(np.linalg.solve(np.eye(N)-z*f, df))
    return p, dp, j, float(dj)


def entropy_production_and_stokes(p, tri):
    """Original triangle H1=0: all steady edge currents are face boundaries."""
    pi = stationary(p)
    oriented = ([(a, b) for a in A for b in B]
                + [(b, c) for b in B for c in C]
                + [(c, a) for c in C for a in A])
    assert len(oriented) == 359
    index = {e: i for i, e in enumerate(oriented)}
    x = np.array([pi[u]*p[u, v] for u, v in oriented])
    y = np.array([pi[v]*p[v, u] for u, v in oriented])
    current = x-y
    force = np.log(x/y)
    ep = float(current @ force)
    assert ep >= -1e-12
    entries, rows, cols = [], [], []
    tidx = 0
    for a in A:
        for b in B:
            for c in C:
                for uv in [(a, b), (b, c), (c, a)]:
                    rows.append(index[uv])
                    cols.append(tidx)
                    entries.append(1.0)
                tidx += 1
    boundary = coo_matrix((entries, (rows, cols)), shape=(359, 1287)).tocsr()
    solve = lsqr(boundary, current, atol=1e-13, btol=1e-13, iter_lim=400)
    q = solve[0]
    assert max(abs(boundary @ q-current)) < 1e-11
    affinity = (2*tri).flatten()
    alt = float(q @ affinity)
    assert abs(alt-ep) < 2e-11
    return ep, alt, q, float(max(abs(boundary @ q-current)))


def main():
    y0 = .19
    k, dlogk = from_cost(y0)
    lam, r, p = perron(k)
    b, tri = cycle_data(p)
    assert triple_contrast(tri) < 1e-12
    lam2, out, w = reconstructed_p(b, tri)
    err = float(np.max(abs(p-out)))
    assert err < 2e-12 and abs(lam2-1) < 2e-12
    assert np.max(abs(cycle_data(out)[1]-tri)) < 2e-12
    p0, dp, j0, dj = direct_source(k, dlogk)
    delta = 1e-5
    def from_field(y):
        kk, _ = from_cost(y)
        pp = perron(kk)[2]
        bb, tt = cycle_data(pp)
        p_rec = reconstructed_p(bb, tt)[1]
        jj = native_feedback(p_rec)[0]
        return pp, p_rec, jj
    pplus, qplus, jplus = from_field(y0+delta)
    pminus, qminus, jminus = from_field(y0-delta)
    derr = float(np.max(abs((qplus-qminus)/(2*delta)-dp)))
    sourceerr = abs((jplus-jminus)/(2*delta)-dj)
    assert derr < 3e-9 and sourceerr < 1e-9
    ep, stokes, facecurrents, stokes_error = entropy_production_and_stokes(p, tri)

    # Strict negative control: reverse oriented cycle current, preserve
    # EVERY reciprocal two-step product on the original 718 directed support.
    adj = SUPPORT.astype(float)
    rho, rr, pp0 = perron(adj)
    uu = np.zeros(N); vv = np.zeros(N)
    uu[0], uu[1] = 1, -1
    vv[9], vv[10] = 1, -1
    q = np.outer(uu, vv)-np.outer(vv, uu)
    assert np.max(abs(adj@q)) == 0 and np.max(abs(q@adj)) == 0
    eps = .01
    ppos = perron(adj+eps*rho*q)[2]
    pneg = perron(adj-eps*rho*q)[2]
    bb1, cc1 = cycle_data(ppos)
    bb2, cc2 = cycle_data(pneg)
    assert np.max(abs(bb1-bb2)) < 2e-13
    assert np.max(abs(cc1-cc2)) > .2
    assert np.max(abs(ppos-pneg)) > .005
    ep0, _, _, _ = entropy_production_and_stokes(pp0, cycle_data(pp0)[1])
    assert abs(ep0) < 1e-13
    # General equilibrium entropy production has zero first derivative and
    # nonnegative second variation; it cannot equal an indefinite M at flat.
    def ep_eps(v):
        pp = perron(adj+v*rho*q)[2]
        return entropy_production_and_stokes(pp, cycle_data(pp)[1])[0]
    epos, eneg = ep_eps(1e-4), ep_eps(-1e-4)
    ep2 = (epos+eneg-2*ep0)/(1e-4**2)
    assert ep2 > 1e-5 and abs(epos-eneg) < 2e-8

    print("PASS complete directed edges = 718; reciprocal edges = 359; triangles = 1287")
    print("PASS 960 triple contrasts max =", f"{triple_contrast(tri):.3e}")
    print("PASS full Markov reconstruction error =", f"{err:.3e}")
    print("PASS recovered probability Perron rho =", f"{lam2:.12f}")
    print("PASS all-field source: max DP error =", f"{derr:.3e}")
    print("PASS J=-Tr log(I-zF): analytic derivative =", f"{dj:.14g}")
    print("PASS recovered determinant derivative residual =", f"{sourceerr:.3e}")
    print("PASS stationary Stokes entropy production =", f"{ep:.12g}")
    print("PASS independent 327-cycle / 1287-face pairing residual =", f"{abs(stokes-ep):.3e}")
    print("PASS face-current inverse residual =", f"{stokes_error:.3e}")
    print("PASS equilibrium entropy production Hessian positive =", f"{ep2:.12g}")
    print("PASS negative control: same ALL 359 reciprocal returns, opposite triangle odds")
    print("NOTE: full scalar bulk response ONLY; no compulsory native Book/CAR/clock link")

if __name__ == '__main__':
    main()
