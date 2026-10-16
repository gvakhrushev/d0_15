#!/usr/bin/env python3
"""Replay the existing golden cost, full Fibonacci inclusion and GNS adjoint."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import sympy as s

STEM = '02_REGISTRY/research/certificates/a4d_native_golden_cost_refinement'
PROOF = '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md'
INPUT = '123d9e969ec56705b4b485adb59a36c19f5a8797'
SCOPE = {
    'actual_cost_cut_and_Perron_measure_bridge': True,
    'actual_full_matrix_inclusion_and_conditional_expectation': True,
    'all_rectangular_and_duplicate_complement_directions_retained': True,
    'same_profinite_support_by_two_cofinality_bounds': True,
    'normalized_GNS_column_bound_to_actual_recorded_gate': True,
    'physical_operation_admission_from_unitary_extension': False,
    'every_old_block_splits_at_every_cost_level': False,
    'cost_clock_is_physical_proper_time': False,
    'cost_cut_is_independent_golden_tensor_readout': False,
    'ordinary_bootstrap_trace_replaced_by_AF_trace': False,
    'GNS_cyclic_state_faithful_on_full_endomorphism_algebra': False,
    'Perron_scale_identity_selects_heat_generator': False,
    'Fibonacci_AF_identified_with_33_718_or_four_role_lattice': False,
    'complex_all_level_construction_claimed_entirely_Lean': False,
    'native_F_source_Ward_stationarity_curved_roots_or_GR_closed': False,
    'T0_T3_or_original_parent_terminals_closed': False,
}


class Q:
    """Exact Q(p), p^2+p=1. No floating-point decisions."""
    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)
    @staticmethod
    def co(x):
        return x if isinstance(x, Q) else Q(x)
    def __add__(self, other):
        o = self.co(other)
        return Q(self.a+o.a, self.b+o.b)
    __radd__ = __add__
    def __neg__(self):
        return Q(-self.a, -self.b)
    def __sub__(self, other):
        return self + -self.co(other)
    def __rsub__(self, other):
        return self.co(other) + -self
    def __mul__(self, other):
        o = self.co(other)
        return Q(self.a*o.a+self.b*o.b,
                 self.a*o.b+self.b*o.a-self.b*o.b)
    __rmul__ = __mul__
    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        z, x = Q(1), self
        while n:
            if n & 1:
                z = z*x
            x, n = x*x, n//2
        return z
    def __eq__(self, other):
        o = self.co(other)
        return self.a == o.a and self.b == o.b
    def __repr__(self):
        return f'Q({self.a},{self.b})'


def mathematics():
    checks = Counter()
    def ck(name, predicate):
        assert bool(predicate), name
        checks[name] += 1

    p = Q(0, 1)
    ck('owned_golden_closure', p+p**2 == 1)
    def cost(w):
        return sum(1 if b else 2 for b in w)
    def code(w):
        return tuple(c for b in w for c in ((0,) if b else (1, 0)))
    def weight(w):
        return p**cost(w)
    leaves = [()]
    a, b = 1, 0
    previous = None
    for n in range(13):
        codes = [code(w)[:n] for w in leaves]
        counts = Counter(t[-1] if t else 0 for t in codes)
        ck('exact_rooted_counts', counts[0] == a and counts[1] == b)
        ck('owner_mass_at_every_cut', a*p**n+b*p**(n+1) == 1)
        ck('all_cut_mass_retained', sum(map(weight, leaves), Q()) == 1)
        ck('injective_code_cut_no_postselection', len(set(codes)) == len(leaves) == a+b)
        ck('forbid_11_language', all((1,1) not in tuple(zip(t,t[1:])) for t in codes))
        ck('prefix_free_complete_cut', all(cost(w) >= n and (not w or cost(w[:-1]) < n) for w in leaves))
        for w, t in zip(leaves, codes):
            ending = t[-1] if t else 0
            ck('literal_cost_length', len(code(w)) == cost(w))
            ck('pending_return_fixes_next_symbol', len(code(w)) == n+ending and (not ending or code(w)[n] == 0))
            ck('two_exact_weights', weight(w) == p**(n+ending))
            state, probability = 0, Q(1)
            for letter in t:
                probability *= (p if letter == 0 else p**2) if state == 0 else 1
                state = letter
            ck('rooted_Perron_probability', probability == weight(w))
            ck('both_cofinality_bounds', len(w) <= n and 2*len(w) >= n)
        if previous is not None:
            parent_mass = {w: Q() for w in previous}
            for w in leaves:
                parent = w if w in parent_mass else w[:-1]
                ck('unique_previous_prefix', parent in parent_mass)
                parent_mass[parent] += weight(w)
            ck('literal_measure_refinement', all(v == weight(w) for w,v in parent_mass.items()))
        previous = leaves
        leaves = [v for w in leaves for v in ((w+(True,),w+(False,)) if cost(w) == n else (w,))]
        a, b = a+b, a

    # The corpus owner's pathCount starts at (1,1), exactly one rooted step later.
    aa, bb = 1, 1
    for level in range(11):
        ck('AF_trace_normalization', aa*p**(level+1)+bb*p**(level+2) == 1)
        ck('all_full_increment_dimensions', (aa+bb)**2+aa**2 == aa**2+bb**2+aa**2+2*aa*bb)
        if level < 5:
            ck('literal_owner_dimensions', aa*aa+bb*bb == [2,5,13,34,89][level])
        aa, bb = aa+bb, aa
    ck('rank_ratio_is_not_declared_phi_scale', Q(3) != Q(2)*(1+p))

    # Sparse full GNS maps in the unnormalized matrix-unit coordinates.
    q = s.symbols('p', real=True)
    relation = q*q+q-1
    def red(x):
        return s.rem(s.expand(x), relation, q)
    def zero(M):
        return all(red(x) == 0 for x in M.todok().values())
    aa, bb = 1, 1
    for level in range(4):
        coarse = [('A',i,j) for i in range(aa) for j in range(aa)] + [('B',i,j) for i in range(bb) for j in range(bb)]
        fine = [('Z',i,j) for i in range(aa+bb) for j in range(aa+bb)] + [('W',i,j) for i in range(aa) for j in range(aa)]
        ci, fi = {v:i for i,v in enumerate(coarse)}, {v:i for i,v in enumerate(fine)}
        nc, nf = len(coarse), len(fine)
        J, C = s.SparseMatrix(nf,nc,{}), s.SparseMatrix(nc,nf,{})
        for v,k in ci.items():
            block,i,j = v
            if block == 'A':
                J[fi['Z',i,j],k] = J[fi['W',i,j],k] = 1
                C[k,fi['Z',i,j]], C[k,fi['W',i,j]] = q, q**2
            else:
                J[fi['Z',aa+i,aa+j],k] = C[k,fi['Z',aa+i,aa+j]] = 1
        Wc = s.SparseMatrix(nc,nc,{(k,k):1 if v[0]=='A' else q for v,k in ci.items()})
        Wf = s.SparseMatrix(nf,nf,{(k,k):q if v[0]=='Z' else q**2 for v,k in fi.items()})
        P = J*C
        ck('full_literal_isometry', zero(J.T*Wf*J-Wc))
        ck('full_literal_conditional_adjoint', zero(Wc*C-J.T*Wf))
        ck('full_literal_retraction', zero(C*J-s.eye(nc)))
        ck('full_orthogonal_projection', zero(P*P-P) and zero(P.T*Wf-Wf*P))
        ck('full_projection_trace', red(s.trace(P)) == nc and nf-nc == aa*aa+2*aa*bb)
        off = [k for (block,i,j),k in fi.items() if block=='Z' and ((i<aa) != (j<aa))]
        ck('both_rectangular_blocks_retained', len(off) == 2*aa*bb)
        for k in off:
            ck('unread_rectangular_direction_has_positive_weight', C[:,k] == s.zeros(nc,1) and Wf[k,k] == q)
        for i in range(aa):
            for j in range(aa):
                v = s.SparseMatrix(nf,1,{(fi['Z',i,j],0):q**2,(fi['W',i,j],0):-q})
                ck('nonzero_duplicate_complement', zero(C*v) and red((v.T*Wf*v)[0]) == red(q**3))
        aa, bb = aa+bb, aa

    # The star/trace law is also exercised on complex, non-diagonal matrices.
    for aa,bb in [(1,1),(2,1),(3,2)]:
        A=s.Matrix(aa,aa,lambda i,j:i+2*j+1+s.I*(i-j+1))
        B=s.Matrix(bb,bb,lambda i,j:2*i-j+s.I*(i+j+1))
        W=s.Matrix(aa,aa,lambda i,j:3*i-j+2+s.I*(j-2*i))
        U=s.Matrix(aa,bb,lambda i,j:1+s.I*(i+j+1))
        V=s.Matrix(bb,aa,lambda i,j:2+s.I*(i-j-1))
        diag=s.diag(A,B)
        Z=A.row_join(U).col_join(V.row_join(B))
        def frob(M):
            return s.trace(M.conjugate().T*M).expand()
        E=q*A+q**2*W
        lhs=q*(frob(A)+frob(B)+frob(U)+frob(V))+q**2*frob(W)-(frob(E)+q*frob(B))
        rhs=q**3*frob(A-W)+q*(frob(U)+frob(V))
        ck('complex_full_Pythagorean_identity', red(lhs-rhs) == 0)
        ck('complex_trace_preservation', red(q*s.trace(diag)+q**2*s.trace(A)-(s.trace(A)+q*s.trace(B))) == 0)
        ck('complex_star_preservation', s.diag(A.conjugate().T,B.conjugate().T) == diag.conjugate().T)
        ck('actual_full_algebra_multiplication', s.diag(A*A,B*B) == diag*diag)

    r=(s.sqrt(5)-1)/2
    g=s.Matrix([[s.sqrt(r),-r],[r,s.sqrt(r)]])
    simp=lambda M:M.applyfunc(s.simplify)
    P=g*s.diag(1,0)*g.T
    ck('actual_golden_normalized_GNS_column', simp(g*s.Matrix([1,0])-s.Matrix([s.sqrt(r),r])) == s.zeros(2,1))
    ck('actual_golden_full_unitary', simp(g.T*g) == s.eye(2))
    ck('actual_refined_projector', simp(P-s.Matrix([[r,r*s.sqrt(r)],[r*s.sqrt(r),r**2]])) == s.zeros(2))
    recorded=s.Matrix([[s.sqrt(r),0,-r,0],[0,s.sqrt(r),0,-r],[0,r,0,s.sqrt(r)],[r,0,s.sqrt(r),0]])
    ck('literal_recorded_blank_column', simp(recorded*s.Matrix([1,0,0,0])-s.Matrix([s.sqrt(r),0,0,r])) == s.zeros(4,1))
    ck('column_identity_is_not_full_gate_identity', g.rows == 2 and recorded.rows == 4)
    x,y,w,u,v=s.symbols('x y w u v',real=True)
    ck('generic_complete_residual', red(q*(x*x+y*y+u*u+v*v)+q*q*w*w-((q*x+q*q*w)**2+q*y*y)-(q**3*(x-w)**2+q*(u*u+v*v))) == 0)
    return dict(sorted(checks.items()))


MUTATIONS = {
    'return_code_wrong': ('else (1, 0)))','else (1, 1)))'),
    'return_cost_wrong': ('sum(1 if b else 2 for b in w)','sum(1 if b else 1 for b in w)'),
    'pending_branch_resplit': ('if cost(w) == n else (w,)', 'if cost(w) >= n else (w,)'),
    'Perron_return_wrong': ('(p if letter == 0 else p**2)', '(p if letter == 0 else p)'),
    'full_expectation_wrong': ('= q, q**2','= q, q'),
    'fine_duplicate_weight_wrong': ("q if v[0]=='Z' else q**2", "q if v[0]=='Z' else q"),
    'drop_rectangular_energy': ('rhs=q**3*frob(A-W)+q*(frob(U)+frob(V))','rhs=q**3*frob(A-W)'),
    'golden_GNS_coefficient_wrong': ('[[s.sqrt(r),-r],[r,s.sqrt(r)]]','[[r,-r],[r,r]]'),
}


def validate_ledger(root, ledger):
    assert ledger['input_head'] == INPUT
    assert ledger['scope'] == SCOPE
    for path,digest in ledger['inputs'].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest() == digest, path
    receipt=json.loads((root/(STEM+'_results.json')).read_text())
    assert receipt['returncode'] == 0 and receipt['new_declarations'] == 24
    capsule=(root/(STEM+'.lean')).read_text()
    names=re.findall(r'^#check (D0\.Research\.GoldenCostRefinement\.\w+)$',capsule,re.M)
    assert len(names) == len(set(names)) == 24 and names == receipt['declarations']
    assert receipt['capsule_sha256'] == hashlib.sha256(capsule.encode()).hexdigest()
    assert receipt['output_sha256'] == hashlib.sha256((root/(STEM+'_output.txt')).read_bytes()).hexdigest()
    assert receipt['axiom_union'] == ['Classical.choice','Quot.sound','propext']
    for path,digest in receipt['transitive_d0_source_sha256'].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest() == digest, path
    output=(root/(STEM+'_output.txt')).read_text()
    assert 'error:' not in output and 'sorryAx' not in output
    for name in receipt['declarations']:
        assert name in output and (
            "'"+name+"' depends on axioms:" in output or
            "'"+name+"' does not depend on any axioms" in output)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path)
    ap.add_argument('--math-only',action='store_true')
    ap.add_argument('--write-certificate',action='store_true')
    args=ap.parse_args()
    root=args.repo.resolve() if args.repo else Path(__file__).resolve().parents[3]
    if args.math_only:
        print(json.dumps(mathematics()))
        return
    path=root/(STEM+'_certificate.json')
    if args.write_certificate:
        assert not path.exists(), 'refuse to replace an existing certificate'
        results=json.loads((root/(STEM+'_results.json')).read_text())
        pins=set(results['transitive_d0_source_sha256']) | {PROOF, STEM+'.lean',STEM+'_output.txt',STEM+'_results.json',STEM+'_check.py','03_FORMALIZATION/lean-toolchain','03_FORMALIZATION/lake-manifest.json','03_FORMALIZATION/D0/Geometry/FibonacciBratteliRefinement.lean'}
        ledger={'input_head':INPUT,'scope':SCOPE,'inputs':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sorted(pins)},'checks':mathematics(),'math_mutants':list(MUTATIONS)}
        path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
    ledger=json.loads(path.read_text())
    validate_ledger(root,ledger)
    checks=mathematics()
    assert checks == ledger['checks'] and list(MUTATIONS) == ledger['math_mutants']
    text=Path(__file__).read_text()
    for name,(old,new) in MUTATIONS.items():
        assert text.count(old) >= 1, name
        # Only mutate the mathematics body; the mutation catalogue is unchanged.
        prefix,suffix=text.split('\nMUTATIONS = ',1)
        assert prefix.count(old) == 1, (name,prefix.count(old))
        mutant=prefix.replace(old,new)+'\nMUTATIONS = '+suffix
        with tempfile.TemporaryDirectory(prefix='d0-cost-') as folder:
            temp=Path(folder)/'mutant.py'
            temp.write_text(mutant)
            run=subprocess.run([sys.executable,str(temp),'--repo',str(root),'--math-only'],text=True,capture_output=True,timeout=90)
            assert run.returncode != 0 and 'AssertionError' in run.stderr, (name,run.returncode,run.stderr[-300:])
    rejected=0
    for key,value in SCOPE.items():
        bad=json.loads(json.dumps(ledger)); bad['scope'][key]=not value
        try: validate_ledger(root,bad)
        except AssertionError: rejected+=1
        else: raise AssertionError(('false scope accepted',key))
    print(json.dumps({'verdict':'PASS_GOLDEN_COST_FULL_FIBONACCI_REFINEMENT','exact_controls':sum(checks.values()),'groups':len(checks),'executed_math_mutants_rejected':len(MUTATIONS),'false_scope_ledgers_rejected':rejected,'new_Lean_propositions':24,'native_F_T0_T3_or_GR_closed':False},sort_keys=True))


if __name__ == '__main__':
    main()
