#!/usr/bin/env python3
"""Apply the owned finite-memory entropy algorithm to original stopped all128.

Floating controls validate the new contraction/adjoint against complete leaf
amplitudes. The proof is algebraic. No new price, native test or eigenvalue
floor is introduced. The exact owned CAR16 builder is consumed, not replayed.
"""
import ast
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s
from sympy.polys.domains import QQ_I
from sympy.polys.matrices import DomainMatrix


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


ROOT = Path(sys.argv[1]).resolve()
OWNER = '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/check_paid_port_cost.py'
SOURCE_SHA = '36a091aff2dc826aeabfac0c60a453a80c5bbfc23ecdaf0fd554b17cd8dd1bf3'
source = (ROOT / OWNER).read_bytes()
need(hashlib.sha256(source).hexdigest() == SOURCE_SHA, 'owned builder pin')
tree = ast.parse(source)
definitions = [x for x in tree.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))]


class Python39Popcount(ast.NodeTransformer):
    # API compatibility only: identical nonnegative integer population count.
    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'bit_count' and not node.args:
            return ast.copy_location(ast.Call(func=ast.Name(id='_popcount', ctx=ast.Load()), args=[node.func.value], keywords=[]), node)
        return node


module = ast.fix_missing_locations(Python39Popcount().visit(ast.Module(body=definitions, type_ignores=[])))
ns = {'s': s, 'QQ_I': QQ_I, 'DomainMatrix': DomainMatrix, 'checks': [], '_popcount': lambda n: bin(n).count('1')}
exec(compile(module, OWNER, 'exec'), ns)
ns['O'], ns['I'] = ns['Mat'](s.zeros(16)), ns['Mat'](s.eye(16))
ns['C'] = [ns['creator'](r) for r in range(4)]
ns['G'] = ns['C'][2] * ns['C'][3].H - ns['C'][3] * ns['C'][2].H
rows, drows, D, dD, Delta, dDelta, exact_k, exact_dk = ns['row_fixture'](True)
p = (np.sqrt(5.0) - 1) / 2
ell = np.log(1 / p)


def array(value):
    return np.array(value.dm.to_Matrix().evalf(), dtype=complex)


def pair(value, index):
    return (array(value[0]) + p * array(value[1])) * (np.sqrt(p) if index % 2 else 1)


K = [pair(k, i) for i, k in enumerate(exact_k)]
dK = [pair(k, i) for i, k in enumerate(exact_dk)]
I = np.eye(16)
G = array(ns['G'])
creators = [array(x) for x in ns['C']]
need(np.max(abs(sum(k.conj().T @ k for k in K) - I)) < 3e-14, 'actual all128 completeness')
need(len(K) == 128, 'all original labels retained, including structural zeros')
theta0 = np.arctan2(4, 3)


def native(theta):
    """Same old original32-word/2-coefficient builder at a genuine link angle."""
    U = I + np.sin(theta) * G + (1 - np.cos(theta)) * G @ G
    words = []
    for r in range(4):
        cr = creators[r]
        ql, qr = cr @ cr.conj().T, cr.conj().T @ cr
        left, right0 = I - ql / 5, I - qr / 5
        ur = U if r == 2 else I
        phase = 1j if r == 3 else 1
        z = .6 * cr @ ur * phase
        right = ur.conj().T @ right0 @ ur
        for item in ((z, left), (z.conj().T, right), (-.6 * cr, -left), (-.6 * cr.conj().T, -right0)):
            words.extend((item, item))
    rs = [sum(((-1) ** bin(label & j).count('1')) * words[j][coeff] for j in range(32)) / 32
          for label in range(32) for coeff in range(2)]
    a = rs[0]
    return [z for j, n in enumerate(rs)
            for z in (((I if j == 0 else 0 * I) - 2 * p**2 * n.conj().T @ a),
                      -2 * p * np.sqrt(p) * n.conj().T @ a)]


need(max(np.max(abs(a-b)) for a, b in zip(K, native(theta0))) < 2e-15,
     'changed-angle definition agrees with owned exact original rows')
rho = np.diag(np.arange(1, 17) / 136)
psi = np.diag(np.sqrt(np.diag(rho))).astype(complex)
delta = array(Delta)
generator = delta @ rho - rho @ delta
need(np.max(abs(generator + generator.conj().T)) < 1e-14, 'actual preparation generator is skew')
need(np.linalg.norm(generator) > 1e-6, 'genuine nonconstant preparation variation')
dpsi = generator @ psi

# New literal exit-map substitution, with its genuinely moving link source.
eps = p*p/1024
nr, dnr, dd = [array(x) for x in rows], [array(x) for x in drows], array(dD)
deltadot, datadirac = array(dDelta), array(D)
native_exit = sum(k @ rho @ k.conj().T for k in K[1:])
new_exit = (eps * sum(n.conj().T @ datadirac @ rho @ datadirac @ n for n in nr)
            - eps**2 * delta @ rho @ delta / 4)
need(np.max(abs(native_exit-new_exit)) < 2e-15, 'literal exit CP-minus-blank identity')
native_exit_jet = sum(dk @ rho @ k.conj().T + k @ rho @ dk.conj().T
                     for k, dk in zip(K[1:], dK[1:]))
new_exit_jet = eps * sum(dn.conj().T @ datadirac @ rho @ datadirac @ n
                        + n.conj().T @ (dd @ rho @ datadirac + datadirac @ rho @ dd) @ n
                        + n.conj().T @ datadirac @ rho @ datadirac @ dn
                        for n, dn in zip(nr,dnr)) - eps**2 * (
                            deltadot @ rho @ delta + delta @ rho @ deltadot) / 4
need(np.max(abs(native_exit_jet-new_exit_jet)) < 3e-14, 'exit first source keeps recycling and negative block')

def preparation_unitary(t):
    values, vectors = np.linalg.eigh(-1j * generator)
    return (vectors * np.exp(1j * t * values)) @ vectors.conj().T


def leaves(ks, ps, n, dks=None, dps=None):
    """Every j<cap/alpha!=blank and the unique unresolved cap leaf."""
    blank = ks[0]
    v, dv = ps.copy(), (np.zeros_like(ps) if dps is None else dps.copy())
    amplitudes, derivatives, costs = [], [], []
    for j in range(n):
        for a in range(1, 128):
            amplitudes.append((ks[a] @ v).ravel())
            costs.append((j + 1 + a % 2) + (j + 1) * np.log(64) / ell)
            if dks is not None:
                derivatives.append((dks[a] @ v + ks[a] @ dv).ravel())
        if dks is not None:
            dv = dks[0] @ v + blank @ dv
        v = blank @ v
    amplitudes.append(v.ravel())
    costs.append(n * (1 + np.log(64) / ell))
    if dks is not None:
        derivatives.append(dv.ravel())
    return np.column_stack(amplitudes), (np.column_stack(derivatives) if derivatives else None), np.array(costs)


def entropy_amplitude(a, da=None):
    u, singular, vh = np.linalg.svd(a, full_matrices=False)
    mass = singular**2
    logs = np.zeros_like(mass)
    np.log(mass, out=logs, where=mass > 0)
    val = -mass @ logs / ell
    if da is None:
        return val
    gradient = (-2 / ell) * (u * (singular * (logs + 1))) @ vh
    return val, np.vdot(gradient, da).real


def pointer(a, da=None):
    prob = np.sum(abs(a)**2, axis=0)
    logp = np.zeros_like(prob)
    np.log(prob, out=logp, where=prob > 0)
    val = -prob @ logp / ell
    if da is None:
        return val
    dp = 2 * np.sum(a.conj() * da, axis=0).real
    return val, -(logp + 1) @ dp / ell, prob, dp


def act(k, x, l=None):
    if l is None:
        l = k
    return np.einsum('ai,irjs,bj->arbs', k, x.reshape(16,16,16,16), l.conj(), optimize=True).reshape(256,256)


def trprod(a, b):
    return np.einsum('ij,ji', a, b).real


def channel(ks, ps, n, dks, dps):
    """Whole oldRIGHT remains in psi's column index; no trace over it."""
    vec, dvec = ps.ravel(), dps.ravel()
    state = np.outer(vec, vec.conj())
    dstate = np.outer(dvec, vec.conj()) + np.outer(vec, dvec.conj())
    sigma, dsigma = np.zeros_like(state), np.zeros_like(state)
    for _ in range(n):
        for k, dk in zip(ks[1:], dks[1:]):
            if not (np.any(k) or np.any(dk)):
                continue
            sigma += act(k, state)
            dsigma += act(dk, state, k) + act(k, dstate) + act(k, state, dk)
        dstate = act(dks[0], state, ks[0]) + act(ks[0], dstate) + act(ks[0], state, dks[0])
        state = act(ks[0], state)
    return sigma + state, dsigma + dstate


N = 2
A, dA, cost = leaves(K, psi, N, dK, dpsi)
need(A.shape == (256, 127*N+1), 'original stopped cut has every retained leaf')
hp, dhp, prob, dp = pointer(A, dA)
hq, dhq = entropy_amplitude(A, dA)
need(abs(sum(prob)-1) < 2e-14 and abs(sum(dp)) < 3e-13, 'complete cut and moving preparation normalized')

# Independent conditional-entropy chain evaluation on each real surviving prefix.
v, dv = psi.copy(), dpsi.copy()
chain_value, chain_source = 0.0, 0.0
for _ in range(N):
    survive = np.vdot(v,v).real
    dsurvive = 2*np.vdot(v,dv).real
    one = np.column_stack([(k@v).ravel() for k in K])
    done = np.column_stack([(dk@v+k@dv).ravel() for k,dk in zip(K,dK)])
    mass = np.sum(abs(one)**2,axis=0)
    dmass = 2*np.sum(one.conj()*done,axis=0).real
    conditional = mass/survive
    dconditional = (dmass-conditional*dsurvive)/survive
    logs = np.zeros_like(conditional)
    np.log(conditional,out=logs,where=conditional>0)
    hv = -conditional@logs/ell
    dhv = -(logs+1)@dconditional/ell
    chain_value += survive*hv
    chain_source += dsurvive*hv+survive*dhv
    dv = dK[0]@v+K[0]@dv
    v = K[0]@v
need(abs(chain_value-hp) < 4e-14 and abs(chain_source-dhp) < 2e-13,
     'complete pointer chain includes stop time and unresolved cap source')

sig, dsig = channel(K, psi, N, dK, dpsi)
need(np.max(abs(sig - A @ A.conj().T)) < 2e-14, 'owned Gram theorem applied to original stopped channel')
need(np.max(abs(dsig - dA @ A.conj().T - A @ dA.conj().T)) < 3e-13,
     'whole field/preparation first jet survives contraction')
need(hp-hq > 1e-5, 'actual positive coherence difference, no flags erased')
mu = np.exp(-ell*cost)
need(abs(sum(mu)-1) < 3e-14, 'explicit full-label product reference on this test cut')
# The old central-reference AF maximum has a real type obstruction here:
# two original ports with k!=0 are collinear but carry unequal code weights.
pair_index = next(a for a in range(2,128,2) if np.linalg.norm(K[a]) > 1e-8)
need(np.max(abs(K[pair_index+1]-K[pair_index]/np.sqrt(p))) < 1e-15,
     'literal native nonblank port proportionality')
left, right = pair_index-1, pair_index
cross = np.vdot(A[:,right],A[:,left])
commutator_entry = (mu[right]-mu[left])*cross
need(abs(cross-prob[left]/np.sqrt(p)) < 1e-14 and abs(commutator_entry)>1e-14,
     'actual stopped reference and coherent record do not commute')
cc, dcc = prob @ cost, dp @ cost
positive = prob > 0
igain = prob[positive] @ np.log(prob[positive]/mu[positive]) / ell
need(abs((cc-igain)-hp) < 2e-13, 'old code-relative gain yields whole pointer net action')

# The nonlinear entropy source is the limit of the same finite adjoint;
# regularization is analytical, never a selected eigenvalue cutoff.
vals, vectors = np.linalg.eigh((sig+sig.conj().T)/2)
adjoint_errors = []
for regularizer in (1e-7, 1e-9, 1e-11):
    terminal = (vectors * (-(np.log(np.maximum(vals,0)+regularizer)+1)/ell)) @ vectors.conj().T
    states = []
    r = np.outer(psi.ravel(),psi.ravel().conj())
    for _ in range(N):
        states.append(r)
        r = act(K[0], r)
    back = terminal.copy()
    source_value = 0.0
    for j in reversed(range(N)):
        x = states[j]
        dblank = act(dK[0], x, K[0]) + act(K[0], x, dK[0])
        source_value += trprod(back, dblank)
        for a in range(1,128):
            if not (np.any(K[a]) or np.any(dK[a])):
                continue
            dx = act(dK[a], x, K[a]) + act(K[a], x, dK[a])
            source_value += trprod(terminal, dx)
        back = act(K[0].conj().T, back) + sum(act(k.conj().T, terminal) for k in K[1:] if np.any(k))
    initial_jet = np.outer(dpsi.ravel(),psi.ravel().conj()) + np.outer(psi.ravel(),dpsi.ravel().conj())
    source_value += trprod(back, initial_jet)
    direct = trprod(terminal, dsig)
    need(abs(source_value-direct) < 3e-9, 'nonlinear entropy adjoint includes preparation, both boundary and every actual row')
    adjoint_errors.append(abs(direct-dhq))
need(adjoint_errors[-1] < 1e-6, 'regularized source tends to finite-amplitude entropy first jet')

finite_difference = []
for step in (2e-5, 1e-5):
    plus = leaves(native(theta0+step),preparation_unitary(step)@psi,N)[0]
    minus = leaves(native(theta0-step),preparation_unitary(-step)@psi,N)[0]
    ph = (pointer(plus)-pointer(minus))/(2*step)
    qh = (entropy_amplitude(plus)-entropy_amplitude(minus))/(2*step)
    finite_difference.append([float(abs(ph-dhp)),float(abs(qh-dhq))])
need(max(finite_difference[-1]) < 2e-7, 'genuine compact-link and unitary-preparation finite differences')

frozen = leaves(K, psi, N, dK, np.zeros_like(dpsi))[1]
_, frozen_source = entropy_amplitude(A, frozen)
need(abs(frozen_source-dhq) > 1e-8, 'frozen preparation is rejected by the actual source')
need(abs(dhp-dhq) > 1e-7, 'pointer/coherent sources are distinct on the same original stopped execution')
print(json.dumps({'status':'PASS','input_sha256':SOURCE_SHA,'scope':'All original128 rows, cap2; rank16 Fourier purification/16 RIGHT columns of owned fixture, not primary full-site RIGHT128 evaluation.',
 'full_leaf_count':len(prob),'normalization':float(sum(prob)),
 'entropy_phi':{'pointer':float(hp),'coherent_flag':float(hq),'coherence':float(hp-hq)},
 'first_source_link_and_preparation':{'pointer':float(dhp),'coherent_flag':float(dhq),'coherence':float(dhp-dhq),'coherent_frozen_preparation':float(frozen_source),'code_test_cost':float(dcc)},
 'adjoint_regularization_errors':list(map(float,adjoint_errors)), 'finite_difference_errors':finite_difference,
 'noncentral_reference_control':{'original_nonblank_controller_label':int(pair_index//2),'commutator_entry_abs':float(abs(commutator_entry))},
 'reference':'Test product reference uniform64 x native Golden(p,p^2); not selected physical full label/controller prices.',
 'physical_Info_selection_or_GR_closure':False},indent=2))
