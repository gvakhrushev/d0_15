#!/usr/bin/env python3
"""Decisive new exact checks only; no imported certificate is executed.

The source theorem supplies the all-depth/all-field argument. This checks its
actual CAR16 link application, forty literal tangent controls and the original
positive-observer sign. Alpha is a formal symbol: the identities therefore
include the unchanged native alpha=p^2 h^2/128 without numeric rounding.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--root', type=Path, default=HERE.parents[4],
                    help='root containing the pinned original source paths')
ROOT = parser.parse_args().root.resolve()
checks = []
PINNED_INPUTS = {
    '02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md':
        '2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79',
    '02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md':
        'a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915',
    '02_REGISTRY/research/A4D_NATIVE_FULL128_JONES_OBSERVER_SO3_QUOTIENT_2026_10_20.md':
        '610a6688f8f1ea91c93462d4cedf716eec321dd5032ba35a0d2ffb7262ffca61',
    '02_REGISTRY/research/A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md':
        'c5b2f1021e8da573221f4327bacae67934470a368966456bf328b19fc51555fb',
    '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/FULL128_HEAT_PRICE_RECYCLING_BRIDGE.md':
        'a8cdbd52e52275cb7e41aa84b8bd69e9fb36170f75d8481c6568fb3ea1a2bce0',
}


def require(condition, name):
    if not bool(condition):
        raise ArithmeticError(name)
    checks.append(name)


def equal(a, b):
    if isinstance(a, s.MatrixBase):
        return all(s.expand(v) == 0 for v in a - b)
    return s.simplify(a - b) == 0


def eq(a, b, name):
    require(equal(a, b), name)


for name, digest in PINNED_INPUTS.items():
    require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest,
            'input_pin_'+Path(name).name)

I = s.eye(16)
O = s.zeros(16)
ORDER = (0, 2, 3, 1)


def creator(role):
    bit = ORDER[role]
    out = s.zeros(16)
    for mask in range(16):
        if not (mask >> bit) & 1:
            out[mask | (1 << bit), mask] = (-1) ** (
                (mask & ((1 << bit) - 1)).bit_count())
    return out


c = [creator(r) for r in range(4)]
nu, h, bJ = s.Rational(3, 5), s.Rational(1, 4), s.Rational(4, 5)
gap = (1 - bJ) / 2
eq(bJ**2 + nu**2, 1, 'actual_rational_Julia_margin')
C = [nu * cr for cr in c]
projections = [cr * cr.H for cr in c]
L = [I + (bJ - 1) * nr for nr in projections]
R = [I + (bJ - 1) * (I - nr) for nr in projections]
for r in range(4):
    eq(L[r]**2, I - C[r] * C[r].H, f'left_defect_{r}')
    eq(R[r]**2, I - C[r].H * C[r], f'right_defect_{r}')


def recycle(X):
    return sum((C[r].H*X*C[r] + C[r]*X*C[r].H
                + L[r]*X*L[r] + R[r]*X*R[r]
                for r in range(4)), O) / 8


eq(recycle(I), I, 'paired_original_Julia_unital')
z = [s.I, 1, 1, 1]  # Actual L4 Fourier character (1,0,0,0).
D = sum(((z[r]-1)*C[r] + (s.conjugate(z[r])-1)*C[r].H
         for r in range(4)), O) / h
lam = 2 * nu**2 / h**2
eq(D.H, D, 'true_positive_shifted_adjoint')
eq(D**2, lam*I, 'actual_flat_CAR16_scalar_shell')
Gamma = c[2]*c[3].H - c[3]*c[2].H
eq(Gamma.H, -Gamma, 'original_rotation_23_is_skew')
eq(D*Gamma, Gamma*D, 'actual_D_commutes_rotation_23')
eq(recycle(Gamma), (1-gap)*Gamma, 'owned_Clifford_gap_directly_consumed')
eq(s.trace(Gamma), 0, 'rotation_source_full_trace_zero')
eq(s.trace(-Gamma**2), 8, 'rotation_source_nonzero_all_grade_norm')

# Physical smooth link convention U_0(t)=exp(h t Omega23).
dotD = nu*(z[0]*c[0]*Gamma + s.conjugate(z[0])*Gamma.H*c[0].H)
dotDelta = D*dotD + dotD*D
eq(dotDelta, -2*s.I*nu**2/h*Gamma, 'literal_physical_link_Delta_first_jet')
dotF = recycle(dotDelta)-dotDelta
eq(dotF, -gap*dotDelta, 'literal_nonzero_first_moment_jet')
require(dotF != O, 'operator_source_is_not_annihilated')
eq(dotF, s.Rational(36,125)*s.I*Gamma, 'exact_new_fixture_coefficient')

# Forty actual homogeneous field tangent controls, no rank computation.
alpha = s.symbols('alpha', real=True)
b = 1-alpha*lam


def Nstar(X):
    return X + alpha*(D*recycle(X)*D-2*lam*X)


def Phistar(X):
    return X + 2*alpha*(D*recycle(X)*D-lam*X)


def check_tangent(X, label, scalar=False):
    F = recycle(X)-X
    eq(s.trace(F), 0, label+'_first_moment_trace')
    if scalar:
        eq(X, s.trace(X)*I/16, label+'_CAR_scalar_derivative')
        eq(F, O, label+'_operator_moment_zero')
    # Exact differentiated original three-round recurrence at E_j=b^j I.
    dotE = O
    for j in range(3):
        dotE = Nstar(dotE)-alpha*b**j*X
    dotK = dotE + 3*alpha*b**2*X
    eq(s.trace(dotK), 0, label+'_actual_three_round_trace_source')
    collapsed = -alpha**2*(Nstar(D*F*D)+2*b*D*F*D)
    eq(dotK, collapsed, label+'_collapsed_source_identity')
    # Original unthinned paid-port application: dY_{j+1}=Phi* dY_j at
    # this scalar block, since the actual (dPhi*)(Delta) block is zero.
    source = X
    cost_source = O
    for _ in range(3):
        cost_source += source
        source = Phistar(source)
    eq(s.trace(cost_source), 3*s.trace(X), label+'_original_paid_port_R_source')


for r in range(4):
    for a in range(4):
        dvD = ((z[r]-1)*c[a]+(s.conjugate(z[r])-1)*c[a].H)/h
        check_tangent(D*dvD+dvD*D, f'coframe_{r}_{a}', scalar=True)

eta = s.diag(1,-1,-1,-1)
gens = []
for a in range(4):
    for j in range(a+1,4):
        G = s.zeros(4)
        G[a,j] = 1
        G[j,a] = -eta[a,a]/eta[j,j]
        eq(G.T*eta+eta*G, s.zeros(4), f'proper_Lorentz_generator_{a}_{j}')
        rep = sum((G[i,l]*c[i]*c[l].H for i in range(4)
                   for l in range(4)), O)
        gens.append((a,j,rep))
for r in range(4):
    for a,j,rep in gens:
        # Differentiate C_r Lambda(exp(h t G)) S_r and its true adjoint.
        dD = nu*(z[r]*c[r]*rep+s.conjugate(z[r])*rep.H*c[r].H)
        check_tangent(D*dD+dD*D, f'proper_link_{r}_{a}_{j}')

# All-depth expression is a polynomial identity before original alpha is used.
rcoef = 1-alpha*lam*(1+gap)
eq(Nstar(Gamma), rcoef*Gamma, 'actual_Nstar_rotation_eigenvalue')
for m in (2,3,5,7):
    exact_sum = sum((b**j*rcoef**(m-1-j) for j in range(m)), s.Integer(0))
    closed = (b**m-rcoef**m)/(b-rcoef)
    eq(exact_sum, closed, f'all_depth_geometric_sum_{m}')
    coeff1 = m*alpha*b**(m-1)-alpha*exact_sum
    coeff2 = alpha**2*lam*gap*sum((j*b**(j-1)*rcoef**(m-1-j)
                                 for j in range(1,m)), s.Integer(0))
    eq(coeff1, coeff2, f'collapsed_nonzero_source_coefficient_{m}')

# Same finite formula on the DISTINCT primary physical coframe C_r=h*nu*c_r.
# This check prevents transferring the fixed-nu nonzero limit to that carrier.
nu_physical = h*nu
b_physical = s.sqrt(1-nu_physical**2)
Cph = [nu_physical*cr for cr in c]
Lph = [I+(b_physical-1)*nr for nr in projections]
Rph = [I+(b_physical-1)*(I-nr) for nr in projections]
TphGamma = sum((Cph[j].H*Gamma*Cph[j]+Cph[j]*Gamma*Cph[j].H
                +Lph[j]*Gamma*Lph[j]+Rph[j]*Gamma*Rph[j]
                for j in range(4)), O)/8
eq(TphGamma, (1+b_physical)*Gamma/2, 'primary_scaled_actual_recycling_gap')
DeltaDotPh = h**2*dotDelta
eq(DeltaDotPh, -2*s.I*h*nu**2*Gamma, 'primary_scaled_actual_link_jet')
eq(h**2*lam, 2*nu**2, 'primary_scaled_lattice_energy')

# Do not silently omit the moving Stinespring contribution in theorem (2).
Delta2 = s.diag(1,3)
A2 = s.Matrix([[0,1],[-1,0]])
F2 = Delta2*A2-A2*Delta2
for j in (2,3,5):
    frechet = sum((Delta2**r*F2*Delta2**(j-1-r) for r in range(j)), s.zeros(2))
    eq(frechet, Delta2**j*A2-A2*Delta2**j, f'moving_isometry_commutator_{j}')
require(F2 != s.zeros(2), 'freezing_Kraus_jet_would_fail')

# Independent 4x4 check of the actual positive-observer convention in null basis.
etaN = s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
n0 = s.Matrix([1,1,0,0])/s.sqrt(2)
nd = s.Matrix([0,0,1,0])
eq((n0.T*etaN*n0)[0], 1, 'null_bisector_unit_observer')
eq((n0.T*etaN*nd)[0], 0, 'genuine_observer_tangent')
eq((nd.T*etaN*nd)[0], -1, 'genuine_hyperbolic_observer_curve')
hf = etaN*n0
df = etaN*nd
eq(-etaN+2*hf*hf.T, s.eye(4), 'native_positive_pairing_is_identity_at_base')
dh = 2*(df*hf.T+hf*df.T)
expected_dh = s.zeros(4)
for j in (0,1):
    expected_dh[j,2] = expected_dh[2,j] = -s.sqrt(2)
eq(dh, expected_dh, 'literal_observer_pairing_derivative_sign')
cs = s.symbols('c0:4', real=True)
ss = s.symbols('s0:4', real=True)
avec = s.Matrix([cs[j]-1+s.I*ss[j] for j in range(4)])
mudot = s.expand((avec.H*dh*avec)[0])
eq(mudot, -2*s.sqrt(2)*((cs[2]-1)*(cs[0]+cs[1]-2)
                       +ss[2]*(ss[0]+ss[1])), 'observer_symbol_full_first_jet')
evenpart = s.expand(mudot.subs({ss[0]:0,ss[1]:0,ss[2]:0,ss[3]:0}))
Apart = (1-cs[2])*((1-cs[0])+(1-cs[1]))
eq(evenpart, -2*s.sqrt(2)*Apart, 'observer_even_source_has_negative_sign')
for j in range(4):
    ar = s.zeros(4,1)
    ar[j] = s.I-1
    eq((ar.H*dh*ar)[0], 0, f'full_Riesz_first_shell_observer_jet_{j}')

result = {
    'status': 'PASS',
    'input_commit': 'f569c786730301e1603ee64062beccc6b20d05e7',
    'checks': len(checks),
    'scope': 'new exact source-moment identities and literal CAR16/observer applications; no old suite replay',
    'full_Book_price_or_minimality_selected': False,
    'all_depth_and_all_ambient_claims_method': 'analytic proof in source_moment_collapse.md',
    'native_fixture': {'nu':'3/5', 'h':'1/4', 'Fourier_character':['i',1,1,1],
                       'physical_link':'U_0(t)=exp(h*t*Omega_23)',
                       'dotF':'(36/125)*i*Gamma_23', 'trace_dotF':0},
    'sources': PINNED_INPUTS,
    'check_names': checks,
}
print(json.dumps(result, indent=2))
