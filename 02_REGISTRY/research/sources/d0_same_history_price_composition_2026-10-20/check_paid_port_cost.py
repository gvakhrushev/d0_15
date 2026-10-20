#!/usr/bin/env python3
"""Exact new all128 cost1/2 transform on the original CAR16 Julia rows.

All calculations use rational complex sparse matrices and Q[p]/(p²+p−1).
Port1's sqrt(p) is carried explicitly in its CP quadratic, not rounded.
No Lean, detector fitting, new physical price or expected-record rewrite.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as s
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix

parser=argparse.ArgumentParser()
parser.add_argument('--root',type=Path,required=True)
ROOT=parser.parse_args().root.resolve()
PINNED_SHA256={
    '02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md':
        '2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79',
    '02_REGISTRY/research/sources/d0_native_full128_order_readout_2026-10-19/check_two_round_complete_shannon_order_source.py':
        '72ade8304bd29471115ebb9961df5225307229004c07ddc35d7f31221e566bf4',
}
SOURCE_FILES=tuple(PINNED_SHA256)
checks = []


class Mat:
    """Exact sparse Gaussian-rational arithmetic; no expression expansion."""
    _op_priority=1000

    def __init__(self, value):
        self.dm=(value if isinstance(value,DomainMatrix) else
                 DomainMatrix.from_Matrix(value).convert_to(QQ_I).to_sparse())

    def __add__(self, other):
        if other == 0:
            return self
        return Mat(self.dm.add(other.dm))

    __radd__=__add__

    def __neg__(self):
        return Mat(self.dm.neg())

    def __sub__(self, other):
        return self+-other

    def __mul__(self, other):
        if isinstance(other,Mat):
            return Mat(self.dm.matmul(other.dm))
        return Mat(self.dm.scalarmul(QQ_I.from_sympy(s.sympify(other))))

    __rmul__=__mul__

    def __truediv__(self, value):
        return self*(1/s.sympify(value))

    @property
    def H(self):
        return Mat(self.dm.transpose().applyfunc(lambda z: QQ_I(z.x,-z.y),QQ_I))

    def __eq__(self, other):
        return isinstance(other,Mat) and self.dm==other.dm

    def trace(self):
        items=self.dm.to_dok()
        return QQ_I.to_sympy(sum((items.get((j,j),QQ_I.zero) for j in range(16)),QQ_I.zero))


def trace(a):
    return a.trace() if isinstance(a,Mat) else s.trace(a)


def require(test, label):
    if not test:
        raise ArithmeticError(label)
    checks.append(label)


def eq(a, b, label):
    if isinstance(a, tuple):
        require(all(equal(x,y) for x,y in zip(a,b)),label)
    else:
        require(equal(a,b),label)


def equal(a,b):
    if isinstance(a,str):
        return a==b
    if isinstance(a,Mat):
        return a==b
    if isinstance(a,s.MatrixBase):
        return all(s.expand(x)==0 for x in a-b)
    return s.expand(a-b)==0


def clean(a):
    if isinstance(a,Mat):
        return a
    if isinstance(a,s.MatrixBase):
        return s.ImmutableSparseMatrix(a.applyfunc(s.expand))
    return s.expand(a)


for rel, digest in PINNED_SHA256.items():
    eq(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),digest,
       'pinned_input_'+Path(rel).name)


O = Mat(s.zeros(16))
I = Mat(s.eye(16))


def creator(role):
    entries = {}
    for mask in range(16):
        if not (mask >> role) & 1:
            sign = (-1) ** ((mask & ((1 << role) - 1)).bit_count())
            entries[(mask | (1 << role), mask)] = sign
    return Mat(s.ImmutableSparseMatrix(16, 16, entries))


C = [creator(r) for r in range(4)]
G = C[2] * C[3].H - C[3] * C[2].H
eq(G.H, -G, 'literal_CAR16_J23_is_skew')
for r in range(4):
    for j in range(4):
        eq(C[r] * C[j].H + C[j].H * C[r], I if r == j else O,
           f'CAR16_anticommutator_{r}_{j}')


# Q[p] pairs. Each component is a rational complex sparse matrix or scalar.
def add(a, b):
    return clean(a[0] + b[0]), clean(a[1] + b[1])


def neg(a):
    return -a[0], -a[1]


def mul(a, b):
    ac, bd = a[0] * b[0], a[1] * b[1]
    return clean(ac + bd), clean(a[0] * b[1] + a[1] * b[0] - bd)


def scale(c, a):
    return c * a[0], c * a[1]


def adj(a):
    return a[0].H, a[1].H


def pmul(a):
    return a[1], a[0] - a[1]


def tr(a):
    return trace(a[0]), trace(a[1])


def scalar_identity(a):
    return a[0] * I, a[1] * I


def cp(k, x):
    return mul(mul(k, x), adj(k))


def row_fixture(rotated):
    """Actual 32-word / 2-coefficient Walsh Julia row, old labels unchanged."""
    nu = s.Rational(3, 5)
    # On occupancy 0 or 2 of roles2,3, G=0. On occupancy1, G²=-I.
    U = I + s.Rational(4, 5) * G + s.Rational(2, 5) * G * G if rotated else I
    eq(U.H * U, I, f'actual_compact_link_orthogonal_{rotated}')
    dU = G * U
    words, dwords = [], []
    for r in range(4):
        QL, QR = C[r] * C[r].H, C[r].H * C[r]
        L0, R0 = I - QL / 5, I - QR / 5
        phase = s.I if r == 3 else s.Integer(1)
        Ur = U if r == 2 else I
        dUr = dU if r == 2 else O
        P = nu * C[r] * Ur * phase
        dP = nu * C[r] * dUr * phase
        L, dL = L0, O
        R = Ur.H * R0 * Ur
        dR = dUr.H * R0 * Ur + Ur.H * R0 * dUr
        eq(L * L, I - P * P.H, f'left_Julia_root_{rotated}_{r}')
        eq(R * R, I - P.H * P, f'right_Julia_root_{rotated}_{r}')
        eq(R * dR + dR * R, -(dP.H * P + P.H * dP),
           f'actual_root_jet_{rotated}_{r}')
        for item, derivative in zip(
                ((P, L), (P.H, R), (-nu*C[r], -L0), (-nu*C[r].H, -R0)),
                ((dP, dL), (dP.H, dR), (O, O), (O, O))):
            for _ in range(2):
                words.append(item)
                dwords.append(derivative)
    rows, drows = [], []
    for label in range(32):
        signs = [s.Rational((-1) ** (label & j).bit_count(), 32) for j in range(32)]
        for coeff in range(2):
            rows.append(clean(sum((signs[j] * words[j][coeff] for j in range(32)), O)))
            drows.append(clean(sum((signs[j] * dwords[j][coeff] for j in range(32)), O)))
    eq(len(rows), 64, f'all64_original_controller_rows_{rotated}')
    eq(sum((N * N.H for N in rows), O), I, f'complete_original_row_{rotated}')
    eq(sum((dN*N.H + N*dN.H for N, dN in zip(rows, drows)), O), O,
       f'complete_original_row_jet_{rotated}')
    A, dA = rows[0], drows[0]
    eq(A.H, A, f'actual_blank_A_hermitian_{rotated}')
    eq(dA.H, dA, f'actual_blank_A_jet_hermitian_{rotated}')
    D, dD = 64*A, 64*dA  # actual h=1/4, A=hD/16
    Delta = D*D
    dDelta = dD*D+D*dD
    Ks, dKs = [], []
    for j, (N, dN) in enumerate(zip(rows, drows)):
        M, dM = N.H*A, dN.H*A+N.H*dA
        # K0=delta I−2p²M, K1=sqrt(p)*(−2pM).
        Ks.append(((I if j == 0 else O)-2*M, 2*M))
        dKs.append((-2*dM, 2*dM))
        Ks.append((O, -2*M))
        dKs.append((O, -2*dM))
    return rows, drows, D, dD, Delta, dDelta, Ks, dKs


def raw_map(Ks, X, x=s.Integer(1), mark_power=0):
    result = (O, O)
    for idx, K in enumerate(Ks):
        port = idx % 2
        term = cp(K, X)
        if port:
            term = pmul(term)  # exact sqrt(p) quadratic from port1
        result = add(result, scale(x ** (1+port) * (1+port) ** mark_power, term))
    return result


def raw_jet(Ks, dKs, X, x):
    result = (O, O)
    for idx, (K, dK) in enumerate(zip(Ks, dKs)):
        port = idx % 2
        term = add(mul(mul(dK, X), adj(K)), mul(mul(K, X), adj(dK)))
        if port:
            term = pmul(term)
        result = add(result, scale(x ** (1+port), term))
    return result


def T(rows, X):
    return sum((N.H * X * N for N in rows), O)


def dT(rows, drows, X):
    return sum((dN.H*X*N + N.H*X*dN for N, dN in zip(rows, drows)), O)


rho = Mat(s.diag(*[s.Rational(j+1, 136) for j in range(16)]))
eq(trace(rho), 1, 'normalized_faithful_preparation_16_reference_columns')
epsilon = (s.Rational(1, 1024), -s.Rational(1, 1024))
x = s.Rational(2, 3)
ax = (s.Integer(1), x-1)  # p²+px
shell_result = None

for rotated in (False, True):
    rows, drows, D, dD, Delta, dDelta, Ks, dKs = row_fixture(rotated)
    eq(len(Ks), 128, f'all128_original_Kraus_outcomes_{rotated}')
    complete = (O, O)
    port1 = (O, O)
    for i, K in enumerate(Ks):
        effect = mul(adj(K), K)
        if i % 2:
            effect = pmul(effect)
            port1 = add(port1, effect)
        complete = add(complete, effect)
    eq(complete, (I, O), f'all128_Kraus_completeness_{rotated}')
    expected_port1 = scale(s.Rational(1, 1024), (-Delta, 2*Delta))
    eq(port1, expected_port1, f'all128_actual_port1_effect_{rotated}')
    X = (rho, O)
    recycle = T(rows, D*rho*D)
    anticommutator = (Delta*rho+rho*Delta)/2
    expected = scale(x, add(X, mul(epsilon, add(mul(ax, (recycle,O)), (-anticommutator,O)))))
    eq(raw_map(Ks, X, x), expected, f'exact_actual128_paid_cost_transfer_{rotated}')
    require(raw_map(Ks,X,x) != scale(x,raw_map(Ks,X)),
            f'scalar_clock_factor_without_cost_deformation_fails_{rotated}')
    blank_effect=mul(adj(Ks[0]),Ks[0])
    exit_effect=add((I,O),neg(blank_effect))
    require(port1 != exit_effect,
            f'actual_paid_port1_is_not_total_exit_mark_{rotated}')

    # A true original proper-link jet: all Julia-root and adjoint terms kept.
    drecycle = dT(rows, drows, D*rho*D)+T(rows, dD*rho*D+D*rho*dD)
    danti = (dDelta*rho+rho*dDelta)/2
    expected_jet = scale(x, mul(epsilon, add(mul(ax, (drecycle,O)), (-danti,O))))
    eq(raw_jet(Ks, dKs, X, x), expected_jet,
       f'exact_actual128_full_link_and_root_source_{rotated}')
    Phi = raw_map(Ks, X)
    paid_recycle = mul(pmul(epsilon), (recycle,O))
    eq(raw_map(Ks, X, mark_power=1), add(Phi, paid_recycle),
       f'exact_all128_first_cost_mark_{rotated}')
    eq(raw_map(Ks, X, mark_power=2), add(Phi, scale(3,paid_recycle)),
       f'exact_all128_second_cost_mark_{rotated}')

    # Same oldRIGHT Gram under a moving LEFT-unitary preparation.
    H = Delta*rho-rho*Delta
    drho = H*rho-rho*H
    eq(H.H, -H, f'preparation_LEFT_generator_skew_{rotated}')
    eq(trace(drho), 0, f'preparation_normalization_jet_{rotated}')
    full_source = add(raw_jet(Ks,dKs,X,x), raw_map(Ks,(drho,O),x))
    expected_full_source = add(expected_jet,
                              scale(x, add((drho,O), mul(epsilon,
                                  add(mul(ax,(T(rows,D*drho*D),O)),
                                      (-(Delta*drho+drho*Delta)/2,O))))))
    eq(full_source, expected_full_source,
       f'joint_full128_field_and_preparation_source_{rotated}')
    if rotated:
        require(trace(Delta*drho) != 0, 'moving_preparation_source_is_really_nonzero')
        require(tr(raw_map(Ks,(drho,O),x)) != (0,0),
                'freezing_preparation_fails_actual_scalar_partition_source')
    # At a pure mesh rescaling, A=hD/16 and the actual rows stay fixed.
    # dD=-D, depsilon=2epsilon: both terms must cancel.
    L = add(mul(ax,(recycle,O)),(-anticommutator,O))
    clock_jet = add(mul(scale(2,epsilon),L),mul(epsilon,scale(-2,L)))
    eq(clock_jet,(O,O),f'actual_clock_D_compensation_{rotated}')
    require(mul(epsilon,scale(-2,L)) != (O,O),
            f'freezing_clock_creates_false_source_{rotated}')

    if not rotated:
        lam = s.Rational(288,25)
        eq(Delta, lam*I, 'original_nonzero_flat_Fourier_shell_lambda')
        r = scale(lam, pmul(epsilon))
        eq(port1,scalar_identity(r),'all128_scalar_shell_port1_exact')
        one_factor = scale(x,add((s.Integer(1),s.Integer(0)),scale(x-1,r)))
        eq(tr(raw_map(Ks,X,x)),one_factor,'all128_shell_one_round_partition')
        state1 = raw_map(Ks,X,x)
        eq(tr(raw_map(Ks,state1,x)),mul(one_factor,one_factor),
           'all128_squared_complete_two_round_partition')
        # All 16384 two-round histories are contracted, without selecting outcomes.
        M1rho = raw_map(Ks,X,mark_power=1)
        M2rho = raw_map(Ks,X,mark_power=2)
        u2 = add(raw_map(Ks,M1rho),raw_map(Ks,Phi,mark_power=1))
        v2 = add(add(raw_map(Ks,M2rho),
                     scale(2,raw_map(Ks,M1rho,mark_power=1))),
                 raw_map(Ks,Phi,mark_power=2))
        mean = tr(u2)
        variance = add(tr(v2),neg(mul(mean,mean)))
        eq(mean,scale(2,add((1,0),r)),'all128_two_round_mean_exact')
        eq(variance,scale(2,add(r,neg(mul(r,r)))),
           'all128_two_round_variance_exact')
        require(variance != (0,0),'actual_port_cost_has_nonzero_variance')
        shell_result = {'lambda':str(lam),'port1_Qp':list(map(str,r)),
                        'two_round_mean_Qp':list(map(str,mean)),
                        'two_round_variance_Qp':list(map(str,variance)),
                        'x':str(x), 'two_round_partition_Qp':list(map(str,tr(raw_map(Ks,state1,x))))}

# Closed-form derivatives are checked independently at arbitrary integer n.
t, rr = s.symbols('t r',real=True)
n = s.symbols('n',integer=True,positive=True)
logZ = -n*t+n*s.log(1-rr+rr*s.exp(-t))
eq(s.simplify(-s.diff(logZ,t).subs(t,0)),n*(1+rr),'all_n_scalar_shell_mean_derivative')
eq(s.simplify(s.diff(logZ,t,2).subs(t,0)),n*rr*(1-rr),'all_n_scalar_shell_variance_derivative')

result = {'status':'PASS','checked_conditions':len(checks),
          'scope':'actual original full128 Golden port cost1/2 transform and source; no complete Info or GR identification',
          'all_outcomes_per_round':128,'all_CAR_grades':16,
          'oldRIGHT_reference':'identity action; full rank16 witness is purifiable and may tensor spectators',
          'fixture_reference_scope':'rank16 Fourier density / 16 active purification columns; not a replay of the original full-site fixedRIGHT128 Riesz preparation',
          'exact_field':'Q(i)[p]/(p^2+p-1); no floating point',
          'scalar_shell':shell_result,
          'input_sha256':{rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in SOURCE_FILES},
          'checks':checks}
print(json.dumps(result,indent=2,sort_keys=True))
