"""Original full query, unmatched scene sector, and its complete clock price.

These smooth operators retain the original two-tick query/cut. Variable
angles are comparison-chart inputs, not newly admitted physical pulses.
"""
import mpmath as mp

ACTIVE, UNMATCHED = 528, 21920


def golden():
    return (mp.sqrt(5)-1)/2


def rotation(angle):
    return mp.matrix([[mp.cos(angle), -mp.sin(angle)],
                      [mp.sin(angle), mp.cos(angle)]])


def kron(a, b):
    return mp.matrix([[a[i//b.rows, j//b.cols]*b[i % b.rows, j % b.cols]
                       for j in range(a.cols*b.cols)] for i in range(a.rows*b.rows)])


def tail(E):
    r, s = mp.sqrt(1-E), mp.sqrt(E)
    return mp.matrix([[r, 0, -s, 0], [0, r, 0, -s],
                      [0, s, 0, r], [s, 0, r, 0]])


def angles(x, y):
    p = golden()
    return mp.asin(mp.sqrt(p*p*(1+x))), mp.asin(p-p*p*y)


def query(x, y):
    e, m = angles(x, y)
    t = tail(mp.sin(e)**2)
    return kron(t*t, rotation(2*m))


def phases(x, y):
    e, m = angles(x, y)
    return (2*(e+m), -2*(e+m), 2*(e-m), -2*(e-m),
            2*m, -2*m, 2*m, -2*m), (2*e, -2*e, 0, 0)


def bands(x, y):
    p = golden()
    E, m = p*p*(1+x), p-p*p*y
    B, ell = 4*m*m*(1-m*m), 4*E*(1-E)
    return ell+(1-ell)*B, B


def feedback(x, y, zeta):
    a, b = bands(x, y)
    return -mp.log1p(-zeta*a)-mp.log1p(-zeta*b)


def character(angle, N, beta, derivative=False):
    if type(N) is not int or N < 1 or beta < 0:
        raise ValueError("literal positive clock length and nonnegative beta required")
    terms = [(angle+2*mp.pi*k)/N for k in range(N)]
    if derivative:
        return -beta/N*mp.fsum(mp.sin(t)*mp.exp(-beta*(1-mp.cos(t))) for t in terms)
    return mp.fsum(mp.exp(-beta*(1-mp.cos(t))) for t in terms)


def partitions(x, y, N, beta):
    e, m = angles(x, y)
    k = lambda a: character(a, N, beta)
    return 4*(k(2*(e+m))+k(2*(e-m))+2*k(2*m)), 4*(k(0)+k(2*e))


def price(operands, counts, N, beta, zeta):
    if len(operands) != len(counts) or any(type(c) is not int or c < 1 for c in counts):
        raise ValueError("one positive actual integer count per address required")
    z = mp.fsum(c*(ACTIVE*z8+UNMATCHED*z4)
        for (x, y), c in zip(operands, counts) for z8, z4 in (partitions(x, y, N, beta),))
    return mp.log(z)/beta+ACTIVE*mp.fsum(c*feedback(x, y, zeta)
                                                       for (x, y), c in zip(operands, counts))


def source_coefficients(N, beta, copies, zeta):
    p = golden(); theta = mp.asin(p)
    z8, z4 = partitions(0, 0, N, beta)
    denominator = beta*copies*(ACTIVE*z8+UNMATCHED*z4)
    k2, k4 = (character(t*theta, N, beta, True) for t in (2, 4))
    hx = 4*mp.sqrt(p)*(ACTIVE*k4+UNMATCHED*k2)/denominator
    hy = -8*p**mp.mpf("1.5")*ACTIVE*(k4+2*k2)/denominator
    r, q = 1-zeta+zeta*p**12, 1-zeta+zeta*p**6
    jx, jy = 4*zeta*p**11/r, -8*zeta*p**6*(p**6/r+1/q)
    return dict(hx=hx, hy=hy, jx=jx, jy=jy, aN=ACTIVE*jx+hx,
                bN=ACTIVE*jy+hy, lambdaN=(ACTIVE*jy+hy)/(ACTIVE*jx+hx), lambda0=jy/jx,
                unmatched_hx=4*mp.sqrt(p)*UNMATCHED*k2/denominator)
