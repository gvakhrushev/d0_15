#!/usr/bin/env python3
"""Exact original CAR16 + complete dephased Julia comparison.

This is an observable/source certificate, not a selected native action.
Expected output is separate; the checker never updates a receipt.
"""
from itertools import combinations
import json
import sympy as s


def zero(M):
    return all(s.simplify(x) == 0 for x in M)


def inner(a, b):
    return s.trigsimp(s.simplify((a.conjugate().T*b)[0]))


def simplify(x):
    return s.trigsimp(s.simplify(s.expand_complex(x)))


basis = [I for k in range(5) for I in combinations(range(4), k)]
where = {I: i for i, I in enumerate(basis)}


def exterior(A):
    G = s.zeros(16)
    for col, I in enumerate(basis):
        for p, old in enumerate(I):
            for new in range(4):
                if A[new, old] == 0:
                    continue
                word = list(I)
                word[p] = new
                if len(set(word)) != len(word):
                    continue
                inv = sum(word[i] > word[j] for i in range(len(word))
                          for j in range(i+1, len(word)))
                G[where[tuple(sorted(word))], col] += (-1)**inv*A[new, old]
    return G


E = lambda i, j: s.eye(4)[:, i]*s.eye(4)[:, j].T
eta = s.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                [0, 0, -1, 0], [0, 0, 0, -1]])
N2, N3 = E(1, 2)+E(2, 0), E(1, 3)+E(3, 0)
B2, B3 = E(0, 2)+E(2, 1), E(0, 3)+E(3, 1)
J, B = E(2, 3)-E(3, 2), E(1, 1)-E(0, 0)
original = [N2, N3, B2, B3, J, B]
gens = [exterior(X) for X in original]
grade = s.diag(*[len(I) for I in basis])
parity = s.diag(*[(-1)**len(I) for I in basis])
for X, G in zip(original, gens):
    assert zero(X.T*eta+eta*X)
    assert zero(G*grade-grade*G)
    assert zero(G*parity-parity*G)
assert zero(gens[0]*gens[3]-gens[3]*gens[0]-gens[4])

eplus, circular = s.zeros(16, 1), s.zeros(16, 1)
eplus[where[(0,)]] = 1
circular[where[(2,)]] = 1/s.sqrt(2)
circular[where[(3,)]] = s.I/s.sqrt(2)
assert zero(gens[4]*eplus)
assert zero(gens[4]*circular-s.I*circular)
assert zero(gens[4]**3+gens[4])
beta, t = s.symbols('beta t', real=True)
psi = s.cos(beta)*eplus+s.sin(beta)*circular
U = s.eye(16)+s.sin(t)*gens[4]+(1-s.cos(t))*gens[4]**2
assert zero(U.T*U-s.eye(16))
assert inner(psi, psi) == 1
gamma = s.Rational(1, 4)
V = s.Matrix.vstack(U/2, s.sqrt(3)*s.eye(16)/2)
V0 = V.subs(t, 0)
assert zero(V.conjugate().T*V-s.eye(16))
aa, bb, cc = V0*eplus, V0*psi, V*psi
for v in (aa, bb, cc):
    assert inner(v, v) == 1
w_beta = s.sin(beta)**2
coherent = inner(aa, bb)*inner(bb, cc)*inner(cc, aa)
assert simplify(coherent-(1-w_beta)*(1-w_beta/4+w_beta*s.exp(s.I*t)/4)) == 0
berry_beta = simplify(-s.I*inner(cc, cc.diff(beta)))
berry_t = simplify(-s.I*inner(cc, cc.diff(t)))
assert berry_beta == 0
assert simplify(berry_t-w_beta/4) == 0

rho = psi*psi.conjugate().T
rhot = U*rho*U.conjugate().T
sig0 = s.diag(gamma*rho, (1-gamma)*rho)
sigt = s.diag(gamma*rhot, (1-gamma)*rho)
assert simplify(s.trace(sig0)-1) == 0
assert simplify(s.trace(sigt)-1) == 0
nplus = exterior(E(0, 0))
anchor = s.diag(nplus, nplus)
Z = s.trace(anchor*sig0*sigt)
expected = s.Rational(5, 8)*(1-w_beta)*(1-w_beta/10+w_beta*s.exp(s.I*t)/10)
assert simplify(Z-expected) == 0
bad_term = s.trace(nplus*((1-gamma)*rho)**2)
assert simplify(bad_term-s.Rational(9, 16)*(1-w_beta)) == 0
# A triple of dephased DENSITIES is a different comparison.
rhoa = eplus*eplus.T
siga = s.diag(gamma*rhoa, (1-gamma)*rhoa)
Z3 = s.trace(siga*sig0*sigt)
assert simplify(Z3-s.Rational(7, 16)*(1-w_beta)*(
    1-w_beta/28+w_beta*s.exp(s.I*t)/28)) == 0

# Full 32x32 output spaces, not a reduced flagless swap.
d = 32
swap = s.SparseMatrix(d*d, d*d,
                      {(j*d+i, i*d+j): 1 for i in range(d) for j in range(d)})
assert swap*swap == s.SparseMatrix.eye(d*d)
# Anchor is diagonal: (I tensor A)SWAP |i,j> = A_ii |j,i>.
Om = s.SparseMatrix(d*d, d*d,
                    {(j*d+i, i*d+j): anchor[i, i]
                     for i in range(d) for j in range(d)
                     if i//16 == j//16 and anchor[i, i] != 0})
Ore = (Om+Om.conjugate().T)/2
Oim = (Om-Om.conjugate().T)/(2*s.I)
assert Ore == Ore.conjugate().T
assert Oim == Oim.conjugate().T
# Contract only nonzero observable entries, keeping both full indices.
mean = 0
for (i, j), val in Om.todok().items():
    mean += val*sig0[j//d, i//d]*sigt[j%d, i%d]
assert simplify(mean-Z) == 0
# Independent unconditional tomography, with all flag blocks retained.
tomography = 0
for f in range(2):
    i0 = 16*f+where[(0,)]
    for k in range(4):
        ik = 16*f+where[(k,)]
        tomography += sig0[i0, ik]*sigt[ik, i0]
assert simplify(tomography-Z) == 0

# Generic exact scalar source and its small-face Taylor coefficient.
w, k = s.symbols('w k', real=True)
p = k*w
real = 1-p+p*s.cos(t)
imag = p*s.sin(t)
D = 1-2*p*(1-p)*(1-s.cos(t))
assert s.trigsimp(real**2+imag**2-D) == 0
sw = k*s.sin(t)/D
st = p*(p+(1-p)*s.cos(t))/D
assert s.trigsimp((real*s.diff(imag, w)-imag*s.diff(real, w))/D-sw) == 0
assert s.trigsimp((real*s.diff(imag, t)-imag*s.diff(real, t))/D-st) == 0
assert s.trigsimp(s.diff(sw, t)-s.diff(st, w)) == 0
assert s.simplify(s.diff(sw, t).subs(t, 0)-k) == 0
assert s.simplify(st.subs(t, 0)-k*w) == 0
third = s.simplify(s.diff(st, t, 2).subs(t, 0))
assert s.expand(third+p*(1-p)*(1-2*p)) == 0
for kk in (s.Rational(1, 4), s.Rational(1, 10), s.Rational(1, 28)):
    assert s.simplify(s.diff(sw, t).subs({t: 0, k: kk})) == kk

# Six prescribed anchors from the existing owner, on all exterior grades.
native = []
for pole in (0, 1):
    v = s.zeros(16, 1)
    v[where[(pole,)]] = v[where[(2,)]] = 1/s.sqrt(3)
    v[where[(3,)]] = s.I/s.sqrt(3)
    assert inner(v, v) == 1
    native.append(v*v.conjugate().T)
I01 = exterior((E(1, 0)-E(0, 1))/(2*s.I))
I02 = exterior((E(2, 0)-E(0, 2))/(2*s.I))
choices = [(0, nplus), (0, exterior(E(2, 2))), (0, I01),
           (0, I02), (1, exterior(E(1, 1))), (1, I01)]
rows, visibility = [], []
for line, obs in choices:
    A = (s.eye(16)+obs)/2
    assert zero(A-A.conjugate().T)
    assert all(e >= s.Rational(1, 4) and e <= 1 for e in A.eigenvals())
    assert zero(A*parity-parity*A)
    anchor6 = s.diag(A, A)
    rr = native[line]
    sig = s.diag(rr/4, 3*rr/4)
    z0 = s.simplify(s.trace(anchor6*sig*sig))
    visibility.append(z0)
    row = []
    for X in gens:
        df = -(X+X.conjugate().T)/(4*s.sqrt(3))
        assert zero(s.sqrt(3)*df+(X+X.conjugate().T)/4)
        good = (X*rr+rr*X.conjugate().T)/4
        bad = -((X+X.conjugate().T)*rr+rr*(X+X.conjugate().T))/8
        assert s.simplify(s.trace(good+bad)) == 0
        assert zero(bad-(s.sqrt(3)/2)*(df*rr+rr*df))
        ds = s.diag(good, bad)
        row.append(s.simplify(s.im(s.trace(anchor6*sig*ds))/z0))
    rows.append(row)
M = s.Matrix(rows)
integer = s.Matrix([[0, 7, 0, 5, 4, 0], [0, -2, 0, 2, -2, 0],
                    [2, 0, 6, 0, 0, 0], [-4, 0, 4, 0, 0, 8],
                    [0, 5, 0, 7, 4, 0], [-6, 0, -2, 0, 0, 0]])
assert M*240 == integer
assert visibility == [s.Rational(5, 12), s.Rational(5, 12),
                      s.Rational(5, 16), s.Rational(5, 16),
                      s.Rational(5, 12), s.Rational(5, 16)]
assert integer.det() == 12288
assert M.det() == s.Rational(1, 15552000000)

# 20 October: general GOOD probability, then the original Golden p.
g = s.symbols('g', real=True)
s2 = g*g+(1-g)**2
general_rows, general_visibility = [], []
for line, obs in choices:
    A = (s.eye(16)+obs)/2
    AA = s.diag(A, A)
    rr = native[line]
    sig = s.diag(g*rr, (1-g)*rr)
    z0 = s.factor(s.trace(AA*sig*sig))
    general_visibility.append(z0)
    row = []
    for X in gens:
        good = g*(X*rr+rr*X.conjugate().T)
        bad = -g*((X+X.conjugate().T)*rr+rr*(X+X.conjugate().T))/2
        assert s.simplify(s.trace(good+bad)) == 0
        row.append(s.factor(s.im(s.trace(AA*sig*s.diag(good, bad)))/z0))
    general_rows.append(row)
Mg = s.Matrix(general_rows)
assert zero(Mg.subs(g, s.Rational(1, 4))-M)
numerator = (Mg*s2).applyfunc(s.factor)
det_numerator = s.factor(numerator.det())
assert s.factor(det_numerator-g**9*(1-2*g)**3/124416) == 0
assert all(s.simplify(a-b) == 0 for a, b in zip(general_visibility,
           [2*s2/3, 2*s2/3, s2/2, s2/2, 2*s2/3, s2/2]))
balanced = Mg.subs(g, s.Rational(1, 2))
assert balanced.rank() == 3
assert zero(balanced[:, 0]+balanced[:, 2])
assert zero(balanced[:, 1]+balanced[:, 3])
assert zero(balanced[:, 5])
gold = (s.sqrt(5)-1)/2
det_general = g**9*(1-2*g)**3/(124416*s2**6)
assert s.simplify(det_general.subs(g, gold**2)-gold**9/15552000) == 0
kappa = g*g/s2
assert s.simplify(kappa.subs(g, gold**2)-(5-s.sqrt(5))/10) == 0
zg = g*g*s.trace(nplus*rho*rhot)+(1-g)**2*s.trace(nplus*rho*rho)
assert simplify(zg-s2*(1-w_beta)*(1-kappa*w_beta+kappa*w_beta*s.exp(s.I*t))) == 0

# Exact quotient/source control, not deletion of an implemented label price.
y = s.symbols('y', real=True)
fstar = y+y*y
qs = [y*y/(1+y*y), 1/(1+y*y)]
avg = s.simplify(sum(q*fstar for q in qs))
assert s.simplify(avg-fstar) == 0
assert s.simplify(s.diff(avg, y, 2)-s.diff(fstar, y, 2)) == 0
# Original scene labels: a Cost bump distinguishes placement-only changes.
assert all((a < 9) != (b < 9) or (a < 20) != (b < 20)
           for a, b in [(0, 9), (9, 20), (20, 0), (9, 26), (26, 0)])
def scene_cost(a, b, field):
    return 1+(field*field if {a, b} == {9, 20} else 0)
def path_cost(path, field, perm=lambda v: v):
    return sum(scene_cost(perm(a), perm(b), field)
               for a, b in zip(path, path[1:]))
first, second = [0, 9, 20, 0], [0, 9, 26, 0]
assert s.expand(path_cost(first, y)-path_cost(second, y)-y*y) == 0
swap_c = lambda v: 26 if v == 20 else 20 if v == 26 else v
assert s.expand(path_cost(second, y, swap_c)-path_cost(first, y)) == 0

# Original four-word mixed jet; no bare nonunitary word called an instrument.
word_ab = gens[0]*gens[3]-gens[3]*gens[0]
assert zero(word_ab-gens[4])
assert zero(word_ab+word_ab.conjugate().T)
ds_ab = s.diag(gamma*(word_ab*rho+rho*word_ab.conjugate().T), s.zeros(16))
zbase = s.trace(anchor*sig0*sig0)
phase_ab = simplify(s.im(s.trace(anchor*sig0*ds_ab))/zbase)
assert simplify(phase_ab-w_beta/10) == 0

print(json.dumps({
    'status': 'PASS',
    'input_ref': '90fc38d972cc8538ce6fff2912906a496733c097',
    'CAR_dimension': 16, 'full_flag_output_dimension': 32,
    'grades_retained': list(range(5)), 'Julia_good_probability': '1/4',
    'coherent_three_ray_phase_coefficient': 'w/4',
    'dephased_two_density_Z': '(5/8)*(1-w)*(1-w/10+(w/10)*exp(i*t))',
    'dephased_three_density_phase_coefficient': 'w/28',
    'complete_BAD_BAD_contribution': '(9/16)*(1-w)',
    'two_copy_Hermitian_readout': 'PASS on full 32x32 factors, matched flag score',
    'unconditional_CAR_tomography': 'PASS',
    'full_source_mixed_partial_difference': '0',
    'small_face_scaled_source': 'd(w*theta/10)+O_C1(h^4)',
    'six_phase_visibility': [str(v) for v in visibility],
    'six_phase_Jacobian_times_240': integer.tolist(),
    'six_phase_integer_determinant': str(integer.det()),
    'six_phase_determinant': str(M.det()),
    'latest_integration_ref': 'd533539ba87aaddb567efa84beba765f608af296',
    'general_flag_phase_determinant': 'g^9*(1-2*g)^3/(124416*(g^2+(1-g)^2)^6)',
    'balanced_flag_phase_rank': 3,
    'balanced_full_density_information_claim': 'No loss from full density asserted',
    'native_Golden_pair_phase_determinant': 'p^9/15552000',
    'native_Golden_compact_phase_coefficient': '(5-sqrt(5))/10',
    'native_Golden_small_face_source': 'd(kappa*w*theta)+O_C1(h^4)',
    'arbitrary_moving_embedding_weight_source_control': 'PASS',
    'fixed_Cost_different_embedding_price_control': 'difference=y^2; simultaneous relabeling difference=0',
    'original_null_word_mixed_phase': 'w/10',
    'geometric_plaquette_mixed_phase_given_owned_jet': 'h^2*Omega*w/40',
    'whole_history_relative_phase_coherence_required': False,
    'native_readout_and_price_selected': False,
    'GR_closed': False, 'raw216_closed': False
}, indent=2, default=str))
