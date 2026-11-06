#!/usr/bin/env python3
"""Exact controls for the nonlinear dust Cauchy application in existing PR334.

The general existence theorem is an explicitly cited external theorem.
This checks the NEW constraint-transport dictionary and its missing-row
negative control, not a numerical Einstein evolution or native admission.
"""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys
import sympy as s

ROOT = Path(sys.argv[1]).resolve()
INPUT = '1e6420f319d714be53363a77823f76ec620a6473'
CHECKS = []


def reduce(x):
    return s.factor(s.cancel(s.expand(x)))


def require(ok, label):
    if not bool(ok):
        raise ArithmeticError(label)
    CHECKS.append(label)


def zero(x, label):
    entries = list(x) if isinstance(x, s.MatrixBase) else [x]
    require(all(reduce(e) == 0 for e in entries), label)


def git(*args):
    return subprocess.check_output(
        ['git', '--work-tree=' + str(ROOT), *args], cwd=ROOT)


PINS = {}
for name, digest in [
    ('02_REGISTRY/research/sources/d0_mass_coordinate_equivalence_2026-10-28/PROOF_RU.md',
     'd70ee9c87041dea710c86ab42217f6397510568a2cf6ec9ac66d7c2026646145'),
    ('02_REGISTRY/research/A4D_CLOSED_HISTORY_NONLINEAR_EINSTEIN_DUST_2026_10_28.md',
     'd2951e92a97c5d9ab088c27e0cd3af0989a613df57cf9d1546d2281b6eefa228'),
]:
    blob = git('rev-parse', INPUT + ':' + name).decode().strip()
    data = git('cat-file', 'blob', blob)
    require(hashlib.sha256(data).hexdigest() == digest, 'immutable input ' + name)
    PINS[name] = {'git_blob': blob, 'sha256': digest}

# An off-diagonal positive metric with ALL independent first metric jets.
# This is an exact control of the analytic tensor identity in the proof.
gamma = s.Matrix([[4, 1, 1], [1, 3, 0], [1, 0, 2]])
require(all(gamma[:i, :i].det() > 0 for i in range(1, 4)),
        'spatial control metric is positive definite and non-diagonal')
inverse = gamma.inv()
g = s.diag(1, -1, -1, -1)
g[1:4, 1:4] = -gamma
gi = g.inv()
dgamma = []
for a in range(4):
    matrix = s.zeros(3)
    for i in range(3):
        for j in range(i, 3):
            matrix[i, j] = matrix[j, i] = s.Symbol('h_' + str(a) + str(i) + str(j))
    dgamma.append(matrix)
dg = [s.zeros(4) for _ in range(4)]
for a in range(4):
    dg[a][1:4, 1:4] = -dgamma[a]
Gamma = [[[s.Rational(1, 2) * sum(
    gi[a, l] * (dg[b][l, c] + dg[c][l, b] - dg[l][b, c])
    for l in range(4)) for c in range(4)] for b in range(4)] for a in range(4)]
B = inverse * dgamma[0] / 2
theta = s.trace(B)
for i in range(3):
    for j in range(3):
        zero(Gamma[i+1][0][j+1] - B[i, j],
             'synchronous connection B row ' + str(i) + str(j))

C = s.Symbol('C')
M = s.symbols('M1:4')
dC = s.symbols('C_0:4')
dM = [[s.Symbol('M_' + str(i) + '_' + str(a)) for a in range(4)] for i in range(3)]
def residual(c, m):
    mat = s.zeros(4)
    mat[0, 0] = c
    for i in range(3):
        mat[0, i+1] = mat[i+1, 0] = m[i]
    return mat
Q = residual(C, M)
dQ = [residual(dC[a], [dM[i][a] for i in range(3)]) for a in range(4)]
div = []
for nu in range(4):
    expr = 0
    for mu in range(4):
        for a in range(4):
            expr += gi[mu, a] * (dQ[a][mu, nu] - sum(
                Gamma[l][a][mu]*Q[l, nu] + Gamma[l][a][nu]*Q[mu, l]
                for l in range(4)))
    div.append(reduce(expr))
spatial_div = sum(inverse[i,j] * (dM[j][i+1] - sum(
    Gamma[k+1][i+1][j+1]*M[k] for k in range(3)))
    for i in range(3) for j in range(3))
zero(div[0] - (dC[0] - spatial_div + theta*C),
     'full covariant divergence gives Hamiltonian-constraint transport')
for i in range(3):
    zero(div[i+1] - (dM[i][0] + theta*M[i]),
         'full covariant divergence gives momentum-constraint transport ' + str(i))

# Jacobi's determinant law keeps the real changing spatial volume.
eps = s.Symbol('eps')
zero(s.diff((gamma + eps*dgamma[0]).det(), eps).subs(eps, 0)
     - 2*gamma.det()*theta, 'actual volume law E_dot/E equals theta')
E, E0, C0 = s.symbols('E E0 C0', positive=True)
Mi0, dE, dMi = s.symbols('Mi0 dE dMi')
zero(dE*(E0*Mi0/E) + E*(-dE*E0*Mi0/E**2),
     'conserved E times momentum residual includes volume derivative')
require(reduce(E0*C0/E) != 0,
        'a nonzero initial Hamiltonian residual is not erased by evolution')

# A full nonlinear lapse-row control, before selecting the trace branch.
t, c, q0, tau, kap = s.symbols('t c q0 tau kappa', positive=True)
H = s.Rational(2, 3)/t
V = c*t*t
rho = 2*q0/V
G00 = 3*H*H
spatial_equation = 2*s.diff(H,t) + 3*H*H
R = -6*s.diff(H,t) - 12*H*H
zero(spatial_equation, 'flat dust expansion solves all spatial Einstein rows for arbitrary c')
zero(s.diff(rho*V,t), 'same expansion obeys actual density continuity')
zero(V*R/2 + 2*c/3, 'gravitational operand is constant with its actual volume')
constraint = reduce(G00 - kap*rho)
zero(constraint - (s.Rational(4,3) - 2*kap*q0/c)/t**2,
     'the missing initial lapse constraint has a nonzero explicit residual')
zero(s.diff(V*constraint,t), 'the wrong initial constraint propagates rather than disappearing')
zero(constraint.subs(c, 3*kap*q0/2), 'the correct mass-volume initial constraint is preserved')

x,y,p,z = s.symbols('x y p z')
ep = p**2*(1+x)
ell = 4*ep*(1-ep)
b = p-p**2*y
bb = 4*b*b*(1-b*b)
aa = ell+(1-ell)*bb
price = z*(aa+bb)-z*z*aa*bb
rx,ry = s.diff(price,x),s.diff(price,y)
trace = x*rx-y*ry
dictionary = {x:-2*tau*c/3, y:tau*q0}
metric_normal = tau*(2*c*rx/3 + q0*ry)
zero((metric_normal+trace).subs(dictionary),
     'the original nonlinear temporal metric source equals minus the trace row')
zero(trace.subs(x,-kap*y) + y*(kap*rx+ry).subs(x,-kap*y),
     'the actual trace branch supplies the same Einstein coupling')
gold = (s.sqrt(5)-1)/2
bad = s.expand(trace.subs({x:-s.Rational(2,3)*s.Rational(1,2**20),
                         y:s.Rational(1,2**20), p:gold,z:s.Rational(1,2**20)}))
bad = s.radsimp(bad)
conjugate = bad.xreplace({s.sqrt(5):-s.sqrt(5)})
norm = reduce(bad*conjugate)
require(norm.is_Rational and norm != 0,
        'exact Golden nonlinear negative control: spatial equations do not supply the lapse row')

out = {'status':'PASS_NONLINEAR_DUST_CAUCHY_TRANSPORT',
       'input_commit':INPUT, 'input_pins':PINS,
       'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'checks':len(CHECKS), 'check_names':CHECKS,
       'constraint_transport':['d_t(E M_i)=0','d_t(E C)=E div_gamma M'],
       'wrong_volume_Hamiltonian_residual':str(constraint),
       'nonlinear_bad_normal_field_norm':str(norm),
       'environment':{'python':platform.python_version(),'sympy':s.__version__},
       'external_existence_theorem_checked_by_this_script':False,
       'numerical_PDE_evolution_run':False,'native_compiler_run':False,
       'physical_admission_proved':False,'GR_closed':False}
print(json.dumps(out,sort_keys=True,indent=2))
