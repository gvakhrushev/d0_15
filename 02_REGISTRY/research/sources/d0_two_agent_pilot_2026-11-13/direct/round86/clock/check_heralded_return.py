"""Full marked factory tree of two k=89 CAR words, with a serial central NC1.

Python 3 and mpmath. No previous receipt or source checkout is required.
"""
import itertools
import json
from fractions import Fraction as F

import mpmath as mp

mp.mp.dps = 460
p = (mp.sqrt(5) - 1) / 2
a = mp.sqrt(p)
v = mp.matrix([a, p])
G = mp.matrix([[a, -p], [p, a]])
X = mp.matrix([[0, 1], [1, 0]])
eye = mp.eye(2)
plus = mp.matrix([1, 1]) / mp.sqrt(2)
minus = mp.matrix([1, -1]) / mp.sqrt(2)
z = mp.mpf(2) ** -20


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def close(x, y, label):
    error = mp.norm(x-y)
    require(error < mp.mpf('1e-450') * max(1, mp.norm(y)), label)


def inner(left, right):
    return mp.fdot(left, right)


def kron(left, right):
    return mp.matrix([[left[i//right.rows, j//right.cols]
                       * right[i%right.rows, j%right.cols]
                       for j in range(left.cols*right.cols)]
                      for i in range(left.rows*right.rows)])


def nc1_weights():
    # Actual cold root vector on a head that will be recorded and its fresh tail.
    passive = kron(v, v)
    out = (kron(mp.diag([1, 0]), G) + kron(mp.diag([0, 1]), X*G*X))
    weights = []
    for bit in (0, 1):
        sharp = eye[:, bit]
        active = out * kron(sharp, v)
        close(active, kron(sharp, G*v if bit == 0 else eye[:, 0]), 'NC1 tail')
        mask = mp.diag([1, 1, 0, 0] if bit == 0 else [0, 0, 1, 0])
        weights.append(inner(mask*passive, active)**2)
    close(weights[0], p**2, 'cold 0')
    close(weights[1], p**3, 'cold 10')
    close(G*X*(X*G*X)*v, G[:, 1], 'native dark marker')
    close(inner(v, G[:, 1]), 0, 'exactly dark')
    # Actual two-wire preparation: the first wire remains after reading the second.
    cx = mp.matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    resource = cx * kron(v, v)
    other = []
    for bit in (0, 1):
        wire = mp.matrix([resource[bit], resource[2+bit]])
        other.append(wire/mp.norm(wire))
    close(other[1], plus, 'real plus resource')
    f = weights[0]*inner(v, other[0])**2
    close(f, p**2*(a*p+p**3)**2/(p**2+p**4), 'cold weight of a failed pair')
    # Actual raw X probes of the teleporting Hadamard; retain the output resource.
    A = (p*eye-p**2*X, a*p*(eye+X))
    B = (p*eye+p**2*X, -a*p*(eye-X))
    cphase = mp.diag([1,1,1,-1])
    had = mp.matrix([[1,1],[1,-1]])/mp.sqrt(2)
    for first, second in itertools.product(range(2), repeat=2):
        seq = B[second]*A[first]
        if first == second:
            close(seq, p**3*eye if first == 0 else 0*eye, 'retry or impossible X')
            continue
        old = plus if first else minus
        fix = eye if first else X
        transfer = fix*kron(old.T, eye)*cphase*kron(eye, plus)
        close(transfer, had/mp.sqrt(2), 'transfer before keeping spent resource')
        close(seq, (1 if first else -1)*2*a*p*(old*old.T), 'real X signs')
    return f, weights


def series(q, n):
    return sum(q**j for j in range(n))


def finite_stage(retry, success, cap):
    # Enumerate the retained raw history for each first success, including signs.
    leaves = [(retry**i)*weight for i in range(cap) for weight in success]
    return sum(leaves)


def audit():
    f, (w0, w1) = nc1_weights()
    toffoli = 43
    hadamards = 2*2*toffoli
    ccz = 2*(toffoli+3)
    phases = hadamards+ccz
    n = 16
    m = 32
    h_early = f**n
    resource = finite_stage(f, [w1], n)
    phase = finite_stage(w0, [w1], m)
    xread = finite_stage(w0**2,
                         [w1*w0*inner(v,k)**2 for k in (plus,minus)], m)
    close(xread, p**5*series(p**4,m), 'two real signs')
    kappa = resource**hadamards * phase**phases * xread**hadamards
    first_plus = w1**(hadamards+phases) * (w1*w0*inner(v,plus)**2)**hadamards
    require(kappa >= first_plus > mp.mpf(2)**-2340, 'one marked path suffices')
    b = (p*mp.sin(712*mp.asin(p)))**2
    u = 2*p**3
    # Reconstruct the full two-cycle Gram from the physically occupied CAR masks.
    waves = [(1,0),(0,1),(-1,0),(0,-1)]
    cpair = [1, 1-2*b]
    rows = []
    for axis in (0, 1):
        for x in itertools.product(range(4), repeat=4):
            if x[1] >= 2:
                continue
            shifted = (x[0], x[1]+2, x[2], x[3])
            def car(site):
                c, s = waves[site[axis]]
                return mp.matrix([a,mp.sqrt(p**2-b),mp.sqrt(b)*c,mp.sqrt(b)*s])
            close(inner(car(x),car(shifted)), cpair[axis], 'complete CAR columns')
        ev = [u*(1+sgn*cpair[axis]) for sgn in (-1,1)]
        def h(e):
            return h_early+kappa*p*(p-p**3*e)**2
        rows.append(-128*sum(mp.log1p(z*(h(e)-1)) for e in ev))
    delta = rows[1]-rows[0]
    # Numerically stable second derivation of the two-cycle logdet difference.
    c = cpair[1]
    base = 1-z+z*h_early
    t = z*kappa*p
    vscale = p**3*u
    offset = p-vscale
    lowproduct = (base+t*(offset-vscale*c)**2)*(base+t*(offset+vscale*c)**2)
    contrast = ((1-c**2)*t*vscale**2
                *(2*(base-t*offset**2)+t*vscale**2*(1+c**2)))
    stable = 128*mp.log1p(contrast/lowproduct)
    require(abs(delta/stable-1) < mp.mpf('1e-95'), '460-digit full determinants')
    lower = 128*2*z*kappa*p**7*(1-z*(1+p**3))*u**2*(1-c**2)
    beta = 2*p**2
    x = beta/11
    heat = (mp.mpf(264)/359/beta*x**256/mp.factorial(256)/(1-x/257))
    require(heat < lower < stable, 'full heat cannot reverse the sign')
    # Independent exact rational certificate: 1/2<p, b>1/10000 from the
    # strictly checked angular interval below. Rational upper bound on heat.
    from math import factorial
    heat_rat = F(264,359)*2*F(1,11)**256 / factorial(256)/(1-F(1,11*257))
    require(heat_rat < F(1,2**2400), 'integer full-heat bound')
    require(128*2*F(1,2**20)*F(1,2**2340)*F(1,2**7)
            *F(1,2)*F(1,16)*F(1,2**13) == F(1,2**2377), 'integer cold bound')
    # Algebraic interval for the actual 712-G rotation; repeated squaring.
    mp.iv.dps = 80
    pi = (mp.iv.sqrt(5)-1)/2
    ai = mp.iv.sqrt(pi)
    # Binary powering controls dependency growth in the enclosing intervals.
    co, si = mp.iv.mpf(1), mp.iv.mpf(0)
    c0, s0 = ai, pi
    exp = 712
    while exp:
        if exp % 2:
            co, si = co*c0-si*s0, co*s0+si*c0
        c0, s0 = c0*c0-s0*s0, 2*c0*s0
        exp //= 2
    bi = (pi*si)**2
    require(bi > mp.iv.mpf(1)/10000 and bi < mp.iv.mpf(1)/1000, 'enclosed amplitude')
    return {
        'old_SITE_columns': 256, 'raw_resource_supplies': hadamards,
        'phase_gate_factories_both_legs': phases, 'teleport_X_cycles_both_legs': hadamards,
        'common_early_abort_cold': mp.nstr(h_early,18),
        'all_completed_factory_cold_weight': mp.nstr(kappa,18),
        'full_RC3_difference_F6_minus_F5': mp.nstr(stable,18),
        'full_RC3_strict_lower_bound_numeric': mp.nstr(lower,18),
        'full_heat_absolute_bound_numeric': mp.nstr(heat,18),
        'certified_DeltaJ_above_2pow': -2377, 'certified_abs_DeltaH_below_2pow': -2400,
        'terminal_CX_each_leaf': 256, 'central_report_dephased_before_return': False,
        'complete_Book_Cost_minus_Info': False, 'GR_closed': False,
    }


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
