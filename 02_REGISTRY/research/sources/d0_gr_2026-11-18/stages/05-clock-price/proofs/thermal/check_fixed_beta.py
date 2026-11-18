"""Original K(9,11,13) heat at one beta on the two-birth SourceI example.

Positive matrix Taylor coefficients and Newton identities for its full temporal
polynomial are independent of the two projected feedback moment identities.
Decimals are multiprecision diagnostics. The proof supplies truncation bounds.
"""
import json
import mpmath as mp

mp.mp.dps = 140
p = (mp.sqrt(5) - 1) / 2
beta = 2*p**2
groups = [9, 11, 13]
c = [mp.mpf(1)/(35-size) for size in groups]
edge = [[mp.mpf(0) if i == j else groups[j]*mp.sqrt(c[i]*c[j])
         for j in range(3)] for i in range(3)]
width = 85
depth = 125
zero = tuple([mp.mpf(0)]*12)
identity = tuple([mp.mpf(i//3 == i%3) for i in range(9)] + [mp.mpf(1)]*3)
prev = [zero]*(width+2)
prev[0] = identity
sums = [mp.mpf(0)]*(width+1)
sums[0] = 33
for k in range(1, depth+1):
    following = [zero]*(width+2)
    for j in range(min(k, width)+1):
        high, low = prev[j+1], prev[abs(j-1)]
        radial = prev[j]
        entries = []
        for u in range(3):
            v, w = (u+1)%3, (u+2)%3
            for col in range(3):
                i = 3*u+col
                entries.append((edge[u][v]*radial[3*v+col]
                                +edge[u][w]*radial[3*w+col]
                                +c[u]*(high[i]+low[i]))*beta/k)
        entries.extend(c[u]*(high[9+u]+low[9+u])*beta/k for u in range(3))
        following[j] = tuple(entries)
        sums[j] += sum(entries[i] for i in (0,4,8)) + sum(
            (groups[u]-1)*entries[9+u] for u in range(3))
    prev = following
a = [mp.exp(-beta)*v for v in sums]
assert all(0 < (n+1)*a[n+1] <= beta*a[n]/22 for n in range(75))

def multiply(P, Q):
    out = [0]*(len(P)+len(Q)-1)
    for i, left in enumerate(P):
        if left:
            for j, right in enumerate(Q):
                out[i+j] += left*right
    return out

def scalar_heat(L):
    # Whole canonical determinant: two data sectors. Each sign of L_i has
    # multiplicity two. No earlier gate precedes the births on these histories.
    A, B = p+1j*p**2, p**2+1j*p
    first = [mp.mpc(0)]*(2*L+4)
    first[0], first[L+2], first[L+1], first[2*L+3] = 1, -A, -B, 1j
    second = [mp.mpc(0)]*(2*L+1)
    second[0], second[L], second[2*L] = 1, -(1+1j), 1j
    poly = multiply(first, second)
    D = 16*L+12
    moments = [mp.mpc(0)]
    for n in range(1, 76):
        coeff = poly[n] if n<len(poly) else 0
        moment = -n*coeff-sum(poly[i]*moments[n-i] for i in range(
            1, min(n, len(poly))))
        moments.append(moment)
    centered = sum(a[n]*(4*mp.re(moments[n])) for n in range(1, 76))
    baseline = D*(359+2*a[0])
    H = mp.log(baseline+4*centered)/beta
    Y = (mp.exp(beta*H)-baseline)/4
    return D, H, Y

A, B = p+1j*p**2, p**2+1j*p
g = {(1,0):4, (1,1):4*mp.re(B), (1,2):4*mp.re(A),
     (2,0):0, (2,1):0, (2,2):2*mp.re(B**2),
     (2,3):4*mp.re(A*B-1j), (2,4):2*mp.re(A**2)}
rows = []
for L in [5, 9, 15]:
    D, H, Y = scalar_heat(L)
    residual = Y
    samples = {}
    for (m,s), coeff in g.items():
        n = m*L+s
        observed = residual/(n*a[n])
        q = beta/(22*(n+1))
        k = (m+1)*L-n
        bound = D*mp.power(q,k)/(n*(1-q))
        if s < 2*m:
            bound += (16*3**m/mp.mpf(m))*(q/(1-q)+q/(n*(1-q)**2))
        error = abs(observed-coeff)
        assert error <= bound
        if (m,s) in [(1,0), (1,2), (2,4)]:
            samples[f"g_{m}_{s}"] = dict(
                normalized=mp.nstr(observed,22), exact=mp.nstr(coeff,22),
                abs_error=mp.nstr(error,8), rigorous_resolution_bound=mp.nstr(bound,8))
        residual -= n*a[n]*coeff
    rows.append(dict(L=L, N=L+2, D=D, H=mp.nstr(H,45), readouts=samples))
print(json.dumps(dict(status="PASS", cases=rows, notes=[
    "Scalar H fixed beta, paid pairs only; finite quotients use preceding exact coefficients.",
    "Decimal calculations diagnostic. The source document proves the universal domain bound."
]), indent=2))
