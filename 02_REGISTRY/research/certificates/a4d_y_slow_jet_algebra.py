"""Exact coefficient arithmetic for #275; no floating point or sampled jets."""
from functools import lru_cache
import numpy as np
import sympy as sp


def fixed_h2_forcing(owner):
    """Euler coefficient in Q(z,x0)[h]/(h^3), on precisely the #259 jet."""
    zero = sp.zeros(4)
    eta, eye = owner.ETA, sp.eye(4)
    corr = [owner.corr0, zero, owner.corr2, zero]
    base = owner.BASE_WAVE
    links = [[base[p], base[p]*corr[p], base[p]*corr[p]**2/2] for p in range(4)]
    solder = [eye, (owner.alpha*eta/2).T, owner.x0*(owner.beta*eta/2).T]

    def mul(a, b):
        return [sum((a[i]*b[n-i] for i in range(n+1)), zero) for n in range(3)]

    def product(factors):
        result = [eye, zero, zero]
        for factor in factors:
            result = mul(result, factor)
        return result

    def inverse(a):
        return [eta*v.T*eta for v in a]

    @lru_cache(None)
    def face(p, a, b):
        factors = [links[p] if a == 0 else [eye, zero, zero],
                   links[(p+1)%4] if b == 0 else [eye, zero, zero],
                   inverse(links[(p+1)%4]) if a == 0 else [eye, zero, zero],
                   inverse(links[p]) if b == 0 else [eye, zero, zero]]
        pinv = inverse(product(factors))
        u, v = [j for j in range(4) if j not in (a, b)]
        area = [sum((owner.wedge(solder[i][:, u], solder[n-i][:, v])
                     for i in range(n+1)), sp.zeros(6, 1)) for n in range(3)]
        return factors, pinv, area

    result = {}
    for p in range(4):
        for role in range(4):
            totals = [0]*6
            for a, b in owner.PAIRS:
                corners = [(p, 0), ((p-1)%4, 2)] if role == a else \
                    [((p-1)%4, 1), (p, 3)] if role == b else []
                for phase, corner in corners:
                    factors, pinv, area = face(phase, a, b)
                    for gi, generator in enumerate(owner.GENERATORS):
                        varied = list(factors)
                        varied[corner] = [f*generator if corner < 2 else -generator*f
                                          for f in factors[corner]]
                        dp = product(varied)
                        other = mul(mul(pinv, dp), pinv)
                        dc = [(dp[n]+other[n])/2 for n in range(3)]
                        totals[gi] += owner.orientation(a, b)*sum(
                            (area[i].T*owner.G2*owner.STAR*owner.bivector(dc[2-i]))[0]
                            for i in range(3))
            for gi, total in enumerate(totals):
                value = sp.factor(total)
                if value != 0:
                    result[(p, role, gi)] = value
    return result


def mixed_cross_maps(owner, n0):
    """Coefficient h*a in Z[h,a]/(h^2,a^2), with a standing for a_N*h^2.

    All link jets are integral. The four times connection and eight times
    metric outputs account explicitly for the half-curvature and Gram lift.
    A product coefficient is formed before any truncation of its derivatives.
    """
    eta = np.array(owner.ETA).astype(np.int64)
    eye = np.eye(4, dtype=np.int64)
    zero = np.zeros((4, 4), dtype=np.int64)
    y = np.array(owner.Y).astype(np.int64)
    gen = [np.array(g).astype(np.int64) for g in owner.GENERATORS]
    pairing = np.array(owner.G2*owner.STAR).astype(np.int64)
    pairs = owner.PAIRS
    sh2 = np.array((owner.alpha*owner.ETA).T).astype(np.int64)
    cos, sin = (1,0,-1,0), (0,1,0,-1)

    def mul(a, b):
        return (a[0]@b[0], a[1]@b[0]+a[0]@b[1],
                a[2]@b[0]+a[0]@b[2],
                a[3]@b[0]+a[1]@b[2]+a[2]@b[1]+a[0]@b[3])

    def product(factors):
        result = (eye, zero, zero, zero)
        for factor in factors:
            result = mul(result, factor)
        return result

    def inverse(a):
        return tuple(eta@v.T@eta for v in a)

    def wedge(u, v):
        return np.array([u[a]*v[b]-u[b]*v[a] for a,b in pairs], dtype=np.int64)

    def biv(v):
        dressed = v@eta
        return np.array([dressed[a,b] for a,b in pairs], dtype=np.int64)

    connection4, metric8 = np.zeros((96,8), dtype=np.int64), np.zeros((40,8), dtype=np.int64)
    for column in range(8):
        active, weights = n0[column//2]
        tangent = sum((w*g for w,g in zip(weights,gen)), zero.copy())
        dress = cos if column%2 == 0 else sin

        def link(p, r):
            hpart = cos[p]*y if r == 0 else zero
            apart = dress[p]*tangent if r == active else zero
            return eye, hpart, apart, hpart@apart

        @lru_cache(None)
        def face(p,a,b):
            factors = (link(p,a),link((p+1)%4,b),inverse(link((p+1)%4,a)),inverse(link(p,b)))
            hol = product(factors)
            pinv = inverse(hol)
            u,v = [j for j in range(4) if j not in (a,b)]
            ar0 = wedge(eye[:,u],eye[:,v])
            ar1two = wedge(sh2[:,u],eye[:,v])+wedge(eye[:,u],sh2[:,v])
            return factors,pinv,hol,u,v,ar0,ar1two

        for p in range(4):
            for role in range(4):
                for gi,g in enumerate(gen):
                    total = 0
                    for a,b in pairs:
                        corners = [(p,0),((p-1)%4,2)] if role==a else \
                            [((p-1)%4,1),(p,3)] if role==b else []
                        for pp,corner in corners:
                            fs,pi,_,u,v,ar0,ar1two = face(pp,a,b)
                            varied = list(fs)
                            varied[corner] = tuple(f@g if corner<2 else -g@f for f in fs[corner])
                            dp = product(varied)
                            other = mul(mul(pi,dp),pi)
                            dc2a = dp[2]+other[2]
                            dc2ha = dp[3]+other[3]
                            total += owner.orientation(a,b)*int(2*ar0@pairing@biv(dc2ha)+ar1two@pairing@biv(dc2a))
                    connection4[24*p+6*role+gi,column] = total
            for qi,(qa,qb) in enumerate(owner.SYM):
                q = np.zeros((4,4),dtype=np.int64)
                q[qa,qb]=q[qb,qa]=1
                ds2 = eta@q
                total=0
                for a,b in pairs:
                    _,pi,hol,u,v,_,_ = face(p,a,b)
                    dw02 = wedge(ds2[:,u],eye[:,v])+wedge(eye[:,u],ds2[:,v])
                    dw14 = wedge(ds2[:,u],sh2[:,v])+wedge(sh2[:,u],ds2[:,v])
                    total += owner.orientation(a,b)*int(2*dw02@pairing@biv(hol[3]-pi[3])+dw14@pairing@biv(hol[2]-pi[2]))
                metric8[10*p+qi,column]=total
    return sp.Matrix(connection4.tolist())/4, sp.Matrix(metric8.tolist())/8
