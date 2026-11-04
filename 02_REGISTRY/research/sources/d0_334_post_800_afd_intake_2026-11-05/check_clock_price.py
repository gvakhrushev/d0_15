#!/usr/bin/env python3
"""Literal equal-length record controls, one native call, exact tiny clock.

Exact Golden algebra and nominal matrix checks are explicitly distinguished.
No full128 native word, large heat matrix, same-task rotor admission or full
physical Cost-Info identification is asserted.
"""
from __future__ import annotations
import os
for thread_option in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[thread_option] = '1'
import argparse
import ast
import hashlib
import json
from pathlib import Path
import platform
from types import SimpleNamespace
import numpy as np
import scipy
import sympy as sp
from scipy.linalg import expm, solve_sylvester

PRIMARY = '02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
OWNER = '02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py'
OWNER_SHA256 = '1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9'
OWNER_BLOB = 'ee8de4635d24c668949ac9a0186616ab7d59f2ed'
PREDECESSOR_SHA256 = 'cf48fa4229eb610c47e6a9dae6730ea417701b9d7a40ed4d27a0aa6ff3edb80c'
CHECKS: list[dict[str, str]] = []
RESIDUALS: dict[str, float] = {}
TOL = 4e-11
JET_TOL = 4e-10

def need(condition: object, label: str, kind: str = 'structural') -> None:
    if not bool(condition):
        raise ArithmeticError(label)
    if label in ('original constructor SHA256 pin', 'original constructor Git blob pin'):
        kind = 'provenance'
    CHECKS.append({'label': label, 'kind': kind})

def close(actual: object, expected: object, label: str, tolerance: float = TOL) -> None:
    error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    RESIDUALS[label] = error
    need(np.isfinite(error) and error <= tolerance, label, 'nominal_numeric')

def adj(matrix: np.ndarray) -> np.ndarray:
    return matrix.conj().T

def pinned_loader(repo: Path) -> tuple:
    previous = PRIMARY+':7fh.G1/check_transport.py'
    primary = (repo/PRIMARY).read_text()
    sections = primary.split('#### 7fh.G1. check_transport.py\n')
    opening = '\n```python\n'
    need(len(sections) == 2 and sections[1].startswith(opening),
         'unique published 7fh.G1 loader block', 'provenance')
    source = (sections[1][len(opening):].split('\n```', 1)[0]+'\n').encode()
    need(hashlib.sha256(source).hexdigest() == PREDECESSOR_SHA256,
         'published previous AST loader SHA256', 'provenance')
    parsed = ast.parse(source.decode(), filename=previous)
    function = next(node for node in parsed.body
                    if isinstance(node, ast.FunctionDef) and node.name == 'load_native_once')
    changed: list[int] = []
    class FixtureArgument(ast.NodeTransformer):
        def visit_Call(self, node: ast.Call) -> ast.AST:
            node = self.generic_visit(node)
            if (isinstance(node.func, ast.Attribute) and node.func.attr == 'native'
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == 'native_excerpt'):
                expected = ast.parse('np.log(2.0)', mode='eval').body
                need(ast.dump(node.args[0]) == ast.dump(expected),
                     'pinned loader has original fixture argument', 'provenance')
                node.args[0] = ast.parse('2.0*np.arctanh(1.0/9.0)', mode='eval').body
                changed.append(1)
            return node
    function = FixtureArgument().visit(function)
    need(len(changed) == 1, 'only one native fixture argument changed', 'provenance')
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    namespace = dict(globals())
    exec(compile(module, previous, 'exec'), namespace)
    return namespace['load_native_once'](repo)

def original_creators(repo: Path) -> list[np.ndarray]:
    source = (repo/OWNER).read_bytes()
    need(hashlib.sha256(source).hexdigest() == OWNER_SHA256,
         'same pinned source for creator definition', 'provenance')
    parsed = ast.parse(source.decode(), filename=OWNER)
    function = next(node for node in parsed.body
                    if isinstance(node, ast.FunctionDef) and node.name == 'creators')
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    namespace: dict = {'np': np}
    exec(compile(module, OWNER, 'exec'), namespace)
    return namespace['creators']()

def two(first: np.ndarray, second: np.ndarray, psi: np.ndarray) -> np.ndarray:
    return np.einsum('bij,aj->abi', second, np.einsum('aij,j->ai', first, psi))

def score(vectors: np.ndarray, jets: np.ndarray, costs: np.ndarray, ell: float) -> dict:
    q = np.sum(np.abs(vectors)**2, axis=-1)
    dq = 2*np.real(np.sum(vectors.conj()*jets, axis=-1))
    live = q > 0
    need(np.all(dq[~live] == 0), 'zero amplitude branches have zero first probability jet')
    entropy = -float(np.sum(q[live]*np.log(q[live])))
    dentropy = -float(np.sum(dq[live]*(np.log(q[live])+1)))
    cost = float(np.sum(q*costs))
    dcost = float(np.sum(dq*costs))
    return dict(price=cost-entropy/ell, source=dcost-dentropy/ell,
                cost=cost, cost_source=dcost, entropy=entropy,
                entropy_source=dentropy, positive_slots=int(np.count_nonzero(live)))

def native_checks(repo: Path) -> dict:
    p, k, dk, rows, drows = pinned_loader(repo)
    a, ell = np.sqrt(p), np.log((1+np.sqrt(5.0))/2)
    close(np.einsum('aji,ajk->ik', k.conj(), k), np.eye(16), 'all128 CPTP completeness')
    perm = np.array([z ^ 1 if ((z//2) & 1) else z for z in range(128)], dtype=int)
    need(sorted(perm.tolist()) == list(range(128)) and np.array_equal(perm[perm], np.arange(128)),
         'active128 odd-j port map is an involutive permutation', 'exact_integer')
    need(perm[0] == 0 and perm[1] == 1 and np.count_nonzero(perm != np.arange(128)) == 64,
         'j0 pair fixed and exactly64 fine slots permuted', 'exact_integer')
    ks, dks = k[perm], dk[perm]
    # Complete CP tensor, not one prepared probability.
    phi = np.einsum('aij,akl->ikjl', k, k.conj())
    phis = np.einsum('aij,akl->ikjl', ks, ks.conj())
    close(phis, phi, 'entire DATA channel unchanged by literal pointer permutation')
    dphi = np.einsum('aij,akl->ikjl', dk, k.conj())+np.einsum('aij,akl->ikjl', k, dk.conj())
    dphis = np.einsum('aij,akl->ikjl', dks, ks.conj())+np.einsum('aij,akl->ikjl', ks, dks.conj())
    close(dphis, dphi, 'entire channel boost derivative unchanged', JET_TOL)
    close(k[2::4]/p, k[3::4]/a, 'every odd-j original pair has actual proportional amplitudes')
    close(dk[2::4]/p, dk[3::4]/a, 'every odd-j original pair derivative retains proportionality', JET_TOL)

    A, dA = rows[0], drows[0]
    lam = adj(A)@A
    qodd = np.einsum('aij,akj->ik', rows[1::2], rows[1::2].conj())
    dqodd = (np.einsum('aij,akj->ik', drows[1::2], rows[1::2].conj())
             +np.einsum('aij,akj->ik', rows[1::2], drows[1::2].conj()))
    cs = original_creators(repo)
    theta, nu = 2*np.arctanh(1/9), 3/5
    gen = cs[0]@adj(cs[1])+cs[1]@adj(cs[0])
    u = expm(theta*gen)
    qsum = np.zeros((16,16), dtype=complex)
    dqsum = qsum.copy()
    margins = []
    for role, c in enumerate(cs):
        C = nu*c
        P = C@(u if role == 1 else np.eye(16))
        dP = C@u@gen if role == 1 else np.zeros_like(C)
        qsum += 4*np.eye(16)-P@adj(P)-adj(P)@P-C@adj(C)-adj(C)@C
        dqsum -= dP@adj(P)+P@adj(dP)+adj(dP)@P+adj(P)@dP
        margins.extend((1-float(np.linalg.norm(P,2))**2, 1-float(np.linalg.norm(C,2))**2))
    close(qodd, qsum/16, 'Walsh odd coefficient slice equals original four-defect sum over16')
    close(dqodd, dqsum/16, 'Walsh odd coefficient normalization retains true field derivative', JET_TOL)
    epsilon = min(margins)
    need(epsilon > 0, 'actual fixed fixture is strictly Julia contractive', 'nominal_numeric')
    need(float(np.linalg.eigvalsh(qodd).min()) >= epsilon-TOL,
         'actual odd-row bank has positive Julia margin', 'nominal_numeric')
    need(float(np.linalg.eigvalsh(lam).min()) > 0,
         'actual original Lambda is faithful', 'nominal_numeric')
    eodd = 4*p*p*adj(A)@qodd@A
    deodd = 4*p*p*(adj(dA)@qodd@A+adj(A)@dqodd@A+adj(A)@qodd@dA)
    odd = np.array([z for z in range(128) if (z//2)&1], dtype=int)
    close(eodd, np.einsum('aji,ajk->ik', k[odd].conj(), k[odd]),
          'positive odd event effect uses all actual selected fine branches')
    close(deodd, np.einsum('aji,ajk->ik', dk[odd].conj(), k[odd])
          +np.einsum('aji,ajk->ik', k[odd].conj(), dk[odd]),
          'odd event first source includes every original row jet', JET_TOL)

    psi = np.ones(1)
    for _ in range(4):
        psi = np.kron(psi, [a,p])
    rho = np.outer(psi, psi)
    rho1 = np.einsum('aij,jk,alk->il', k, rho, k.conj())
    drho1 = np.einsum('aij,jk,alk->il', dk, rho, k.conj())+np.einsum('aij,jk,alk->il', k, rho, dk.conj())
    w = np.array([np.trace(eodd@rho).real, np.trace(eodd@rho1).real])
    dw = np.array([np.trace(deodd@rho).real, np.trace(deodd@rho1+eodd@drho1).real])
    need(bool(np.all(w > 0)), 'both actual nonreset odd-j occupations are positive', 'nominal_numeric')
    vectors, svectors = two(k,k,psi), two(ks,ks,psi)
    jets = two(dk,k,psi)+two(k,dk,psi)
    sjets = two(dks,ks,psi)+two(ks,dks,psi)
    close(svectors, vectors[perm][:,perm], 'all16384 pure posterior amplitudes retained by path permutation')
    close(sjets, jets[perm][:,perm], 'all16384 posterior field jets retained', JET_TOL)
    cost = (1+np.arange(128)%2)[:,None]+(1+np.arange(128)%2)[None,:]
    old, new = score(vectors,jets,cost,ell), score(svectors,sjets,cost,ell)
    close(old['entropy'],new['entropy'], 'entire two-round fine CQ entropy unchanged on pure retained branches')
    close(old['entropy_source'],new['entropy_source'], 'entire two-round entropy field source unchanged', JET_TOL)
    close(old['price']-new['price'], p**3*w.sum(), 'exact original two-round code contrast is p cubed times odd occupations')
    close(old['source']-new['source'], p**3*dw.sum(), 'same two-round contrast retains complete field derivative', JET_TOL)
    return dict(odd_occupations=w.tolist(), odd_occupation_theta_jets=dw.tolist(),
                julia_margin=epsilon, Qodd_min=float(np.linalg.eigvalsh(qodd).min()),
                Lambda_min=float(np.linalg.eigvalsh(lam).min()),
                original_two_round=old, swapped_two_round=new)

def exact_clock_checks() -> dict:
    a = sp.symbols('a', positive=True)
    p = a*a
    modulus = a**4+a**2-1
    def red(value: sp.Expr) -> sp.Expr:
        if value == 0:
            return sp.S.Zero
        num, den = sp.fraction(sp.cancel(value))
        return sp.rem(sp.expand(sp.rem(num,modulus,a)*sp.invert(sp.rem(den,modulus,a),modulus,a)),modulus,a)
    def reduced(matrix: sp.MatrixBase) -> sp.MatrixBase:
        return matrix.applyfunc(red)
    def equal(left: sp.MatrixBase, right: sp.MatrixBase) -> bool:
        return left.shape == right.shape and all(red(x) == 0 for x in left-right)
    def exact(condition: object, label: str) -> None:
        need(condition,label,'exact_golden')
    v = sp.Matrix([a,p])
    def cx(control: int, target: int) -> sp.Matrix:
        matrix = sp.zeros(8)
        for col in range(8):
            row = col ^ (1 << (2-target)) if col & (1 << (2-control)) else col
            matrix[row,col] = 1
        return matrix
    words = {'identity': [(0,1),(1,2),(0,1),(1,2),(0,2)],
             'swapped': [(0,1)]*5}
    endpoints = {}
    for name, word in words.items():
        U = sp.eye(8)
        for pair in word:
            U = cx(*pair)*U
        endpoints[name] = U
        exact(len(word) == 5, name+' literal word has five native CX calls')
    exact(endpoints['identity'] == sp.eye(8), 'I5 equals identity on every three-bit column')
    exact(endpoints['swapped'] == cx(0,1), 'five identical CX equal one CX on every column')
    exact(equal(v.T*v,sp.ones(1)), 'three births use the actual normalized Golden vector')
    born = sp.kronecker_product(v,v,v)
    cold_alt = red(p+2*a*p**3)
    expected = {'identity': sp.S.One, 'swapped': cold_alt}
    dims = [1,2,4]+[8]*5
    N, D = len(dims), sum(dims)
    starts = [sum(dims[:j]) for j in range(N)]
    exact((N,D) == (8,47), 'three births plus five CX have true N8 D47')
    births = [v,sp.kronecker_product(sp.eye(2),v),sp.kronecker_product(sp.eye(4),v)]
    passive = births+[sp.eye(8)]*(N-4)
    B = [sp.zeros(1)]*N
    B[-1] = sp.eye(8)
    for j in range(N-2,-1,-1):
        B[j] = reduced(B[j+1]*passive[j])
    details = [sp.eye(1)]+[reduced(sp.eye(dims[j])-passive[j-1]*passive[j-1].T) for j in range(1,N)]
    R = sp.Matrix.vstack(B[0].T, *(reduced(details[j]*B[j].T) for j in range(1,N)))
    exact(equal(R.T*R,sp.eye(8)), 'complete closure retains every birth complement')
    exact(equal(R*R.T,sp.diag(*details)), 'closure range is the full birth-detail sum')
    exact(details[-1] == sp.zeros(8), 'last interstage CX makes final birth-detail projector zero')
    outputs = {}
    numeric_clocks = {}
    a_float = float(np.sqrt((np.sqrt(5.0)-1)/2))
    for name, word in words.items():
        F = births+[cx(*pair) for pair in word[:-1]]
        g = cx(*word[-1])
        T = sp.zeros(D)
        A = sp.eye(1)
        cuts = [A*A.T]
        for j,Fj in enumerate(F):
            exact(equal(Fj.T*Fj,sp.eye(dims[j])), name+f' actual stage{j} is isometric')
            T[starts[j+1]:starts[j+1]+dims[j+1], starts[j]:starts[j]+dims[j]] = Fj
            A = reduced(Fj*A)
            cuts.append(reduced(A*A.T))
        T[:,starts[-1]:starts[-1]+8] += reduced(R*g)
        T = reduced(T)
        exact(equal(T.T*T,sp.eye(D)), name+' complete47dim growing clock is unitary')
        exact(red(sp.trace(T)) == 0, name+' actual clock trace vanishes with final detail zero')
        exact(T[starts[-1]:,starts[-1]:] == sp.zeros(8), name+' entire final-stage clock diagonal block is zero')
        cold = red((B[0].T*g*A)[0])
        exact(red(cold-expected[name]) == 0, name+' original physical cold return is exact')
        P = sp.diag(*cuts)
        leakage = reduced((sp.eye(D)-P)*T*P)
        feedback = reduced(leakage.T*leakage)
        defect = red(1-cold*cold)
        exact(red(sp.trace(feedback)-defect) == 0, name+' full feedback trace equals original cold defect')
        exact(equal(feedback*feedback,defect*feedback), name+' all feedback modes give only the true rankone defect')
        state = sp.zeros(D,1)
        state[0] = 1
        moments = []
        for step in range(1,N+1):
            state = reduced(T*state)
            moments.append(red(state[0]))
        exact(all(m == 0 for m in moments[:-1]) and red(moments[-1]-cold) == 0,
              name+' initialized clock has its first possible return at actual N8')
        outputs[name] = dict(cold=str(cold), defect=str(defect),
                            feedback='-log(1-z+z*cold^2)', trace_T='0')
        numeric_clocks[name] = (np.asarray(T.subs(a,a_float),dtype=float),
                               np.asarray((g*A).subs(a,a_float),dtype=float).reshape(-1),
                               float(cold.subs(a,a_float)))

    # Exactly the original scene; no heat matrix of dimension425D is built.
    zones = [0]*9+[1]*11+[2]*13
    adjacency = sp.Matrix(33,33,lambda i,j:int(zones[i] != zones[j]))
    edges = [(i,j) for i in range(33) for j in range(i+1,33) if adjacency[i,j]]
    incidence, signless = sp.zeros(len(edges),33),sp.zeros(len(edges),33)
    for edge,(i,j) in enumerate(edges):
        incidence[edge,i],incidence[edge,j] = 1,-1
        signless[edge,i],signless[edge,j] = 1,1
    degrees = [sum(adjacency[i,j] for j in range(33)) for i in range(33)]
    degree = sp.diag(*degrees)
    need(len(edges) == 359 and sum(degrees) == 718, 'actual K9,11,13 has359 edges and718 directed incidences','exact_integer')
    need(incidence.T*incidence == degree-adjacency, 'actual oriented scene Gram is D-A','exact_integer')
    need(signless.T*signless == degree+adjacency, 'actual signless scene Gram is D+A','exact_integer')
    Rs = sp.diag(*[1/sp.sqrt(d+2) for d in degrees])
    Cs = Rs*Rs
    exact(equal(Rs*(degree+2*sp.eye(33))*Rs,sp.eye(33)), 'original scene normalization identity')
    exact(equal(Rs*degree*Rs+2*Cs,sp.eye(33)), 'positive and complementary Gram bounds retain the original clock normalization')
    need((33+359+33)*D == 425*D and (359+33-33)*D == 359*D,
         'both complete Hodge degrees give425D modes and359D excess zeros','exact_integer')
    beta, z = 1.0, 2.0**-20
    scene_a = np.asarray(adjacency,dtype=float)
    scene_r = 1/np.sqrt(np.asarray(degrees,dtype=float)+2)
    scene_b = scene_r[:,None]*scene_a*scene_r[None,:]
    scene_c = np.diag(scene_r**2)
    master_values = {}
    for name,(Tn,postgate,cold_n) in numeric_clocks.items():
        mu = np.linalg.eigvalsh(Tn+Tn.T)
        close(Tn.T@Tn,np.eye(D),name+' numeric evaluation retains exact tiny-clock unitarity')
        need(float(mu.min()) >= -2-TOL and float(mu.max()) <= 2+TOL,
             name+' all47 real clock cosine eigenvalues lie in[-2,2]','nominal_numeric')
        spectrum = np.concatenate([np.linalg.eigvalsh(np.eye(33)-scene_b-m*scene_c) for m in mu])
        need(len(spectrum) == 33*D and float(spectrum.min()) >= -TOL and float(spectrum.max()) <= 2+TOL,
             name+' all1551 vertex-clock eigenvalues retained in[0,2]','nominal_numeric')
        partition = 359*D+2*float(np.exp(-beta*spectrum).sum())
        need(D*(359+66*np.exp(-2*beta)) <= partition <= 425*D+TOL,
             name+' full19975-mode partition obeys original zero-mode bounds','nominal_numeric')
        heat = np.log(partition)/beta
        feedback = -np.log1p(-z*(1-cold_n*cold_n))
        master_values[name] = float(heat+feedback)
        # Same original coordinate scene vertex0 and actual postgate final stage.
        temporal = Tn[starts[-1]:,starts[-1]:]+Tn[starts[-1]:,starts[-1]:].T
        coherent_energy = 1-scene_b[0,0]-scene_c[0,0]*float(postgate@temporal@postgate)
        pinched_energy = 1-scene_b[0,0]-scene_c[0,0]*float(np.trace(temporal@np.diag(postgate**2)))
        close(np.dot(postgate,postgate),1.,name+' actual postgate terminal state remains normalized')
        close(coherent_energy,1.,name+' coherent postgate terminal energy is fixed at scene vertex0')
        close(pinched_energy,1.,name+' full computational pinching retains the same terminal energy')
        outputs[name]['heat_diagnostic'] = dict(beta=beta,z=z,partition=partition,
            H=float(heat),J=float(feedback),master=float(heat+feedback),
            vertex_clock_min=float(spectrum.min()),vertex_clock_max=float(spectrum.max()),
            coherent_terminal_energy=float(coherent_energy),pinched_terminal_energy=float(pinched_energy))
    bound = np.log(425/(359+66*np.exp(-2*beta)))/beta-np.log1p(-z)
    master_difference = master_values['swapped']-master_values['identity']
    need(abs(master_difference) <= bound,
         'two complete tiny-clock master values obey the analytic fixed-cut oscillation bound','nominal_numeric')
    return dict(N=N,D=D,widths=dims,words=words,clocks=outputs,
                hodge=dict(total_modes=425*D,harmonic_excess=359*D,
                           heat='Z=359D+2 Tr_(33D) exp(-beta Delta0)',
                           spectral_interval='0<=Delta0<=2I by the two exact scene Grams',
                           full_price_oscillation='beta^-1 log(425/(359+66 exp(-2beta)))-r log(1-z)',
                           diagnostic_master_difference=float(master_difference),
                           diagnostic_bound=float(bound)))

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path('/Users/grigorijvahrusev/.codex/worktrees/gr-native-source-20261024/d0-main-assembly-audit'))
    args = parser.parse_args()
    native_result = native_checks(args.repo)
    clock_result = exact_clock_checks()
    kinds = {kind:sum(item['kind']==kind for item in CHECKS) for kind in sorted({item['kind'] for item in CHECKS})}
    print(json.dumps(dict(schema='d0.literal-full128-clock-control/1',status='PASS',
          checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          owner_sha256=OWNER_SHA256,owner_blob=OWNER_BLOB,
          predecessor_loader_sha256=PREDECESSOR_SHA256,
          runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__),
          check_count=len(CHECKS),classifications=kinds,checks=CHECKS,
          tolerances=dict(nominal=TOL,nominal_jet=JET_TOL),
          max_nominal_residual=max(RESIDUALS.values()),residuals=RESIDUALS,
          native=native_result,tiny_clock=clock_result,
          scope=dict(native_constructor_calls=1,full128_native_word_replayed=False,
                     huge_heat_matrix_computed=False,continuous_rotor_primitive=False,
                     same_fixed_report_task=False,whole_Cost_Info_selected=False,GR_closed=False)),
          ensure_ascii=False,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
