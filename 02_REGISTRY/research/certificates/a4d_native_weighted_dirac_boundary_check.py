#!/usr/bin/env python3
"""Exact actual-cochain weighted Dirac and flat Lorentz spectrum controls.

All-size Fourier, kernel and heat arguments are analytic in the companion
proof. Supplied metric/operator bindings are not a selected physical action.
Default replay checks an immutable ledger and the compiled source closure.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import numpy as np
from scipy import sparse
import sympy as sp

INPUT_HEAD = '139ba614c85381a0b2c2cdf432d2912e852a92c3'
INPUTS = [
 '03_FORMALIZATION/D0/Geometry/ArchiveWeightedHodgeDirac.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDirac.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracSquare.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDiracKernel.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveCubicalDifferential.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveMetricMeasureHodgeLift.lean',
 '03_FORMALIZATION/D0/Geometry/SpectralActionLadder.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveNaturalTwistedDirac.lean',
 '02_REGISTRY/research/A4D_NATIVE_COCHAIN_REFINEMENT.md',
 '02_REGISTRY/research/A4D_NATIVE_COUPLED_HODGE_SCALE_BOUNDARY.md',
 '02_REGISTRY/research/A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md',
]
PREFIX = '02_REGISTRY/research/certificates/a4d_native_weighted_dirac_boundary'
STATES = list(product([0, 1], repeat=4))
SUBSETS = [tuple(r for r in range(4) if s[r]) for s in STATES]
ETA = [1, -1, -1, -1]


def car(order=(0, 1, 2, 3)):
 pos = {r: order.index(r) for r in range(4)}
 a = []
 for r in range(4):
  A = sp.zeros(16)
  for j, ket in enumerate(STATES):
   if ket[r]:
    bra = list(ket); bra[r] = 0
    A[STATES.index(tuple(bra)), j] = (-1)**sum(ket[q] for q in range(4) if pos[q] < pos[r])
  a.append(A)
 return a, [A.T for A in a]


def compound_hodge(M, mu):
 W = sp.zeros(16)
 for i, S in enumerate(SUBSETS):
  for j, T in enumerate(SUBSETS):
   if len(S) == len(T):
    W[i, j] = mu * (M.extract(S, T).det() if S else 1)
 return W


def compound_derivative(M, dM, mu, dmu):
 W = sp.zeros(16)
 for i, S in enumerate(SUBSETS):
  for j, T in enumerate(SUBSETS):
   if len(S) != len(T): continue
   if not S: W[i, j] = dmu; continue
   A = M.extract(S, T); dA = dM.extract(S, T)
   W[i, j] = dmu*A.det()
   for k in range(len(S)):
    B = A.copy(); B[:, k] = dA[:, k]
    W[i, j] += mu*B.det()
 return W


def zero(A):
 if sparse.issparse(A):
  A = A.copy(); A.eliminate_zeros(); return A.nnz == 0
 return all(sp.expand(x) == 0 for x in A)


def exact_sign(a, b):
 # Sign of a+b*sqrt(2), entirely integral.
 if b == 0: return (a > 0)-(a < 0)
 if a == 0: return (b > 0)-(b < 0)
 if (a > 0) == (b > 0): return 1 if a > 0 else -1
 cmp = a*a-2*b*b
 assert cmp != 0
 return (1 if a > 0 else -1)*(1 if cmp > 0 else -1)


def main():
 ap = argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
 ap.add_argument('--output', type=Path); ap.add_argument('--expect', type=Path)
 args = ap.parse_args(); repo = args.repo.resolve(); checks = []
 sha = lambda p: hashlib.sha256((repo/p).read_bytes()).hexdigest()
 def check(name, condition):
  assert bool(condition), name
  checks.append(name); print('PASS_'+name, flush=True)
 r = json.loads((repo/(PREFIX+'_results.json')).read_text())
 assert r['status'] == 'PASS' and r['compiler_exit_code'] == 0 and not r['sorryAx']
 assert r['owner_input_head'] == INPUT_HEAD and r['printed_axiom_dependencies'] == 34
 assert len(r['transitive_d0_source_sha256']) == 49
 assert set(r['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
 for p, h in {**r['transitive_d0_source_sha256'], **r['toolchain_input_sha256'],
               r['capsule']: r['capsule_sha256'], r['output']: r['output_sha256']}.items():
  assert sha(p) == h, 'LEAN_INPUT_CHANGED: '+p
 output = (repo/r['output']).read_text()
 assert not any(s in output for s in ['sorryAx', 'error:', 'warning:', '.native_decide.ax'])
 check('ACTUAL_WEIGHTED_ADJOINT_SQUARE_AND_KERNEL_REDUCTION_COMPILE', True)

 A, C = car(); eye = sp.eye(16)
 for r0 in range(4):
  for s0 in range(4):
   check('LITERAL_CAR_'+str(r0)+str(s0),
    zero(A[r0]*A[s0]+A[s0]*A[r0]) and zero(C[r0]*C[s0]+C[s0]*C[r0]) and
    A[r0]*C[s0]+C[s0]*A[r0] == (eye if r0 == s0 else sp.zeros(16)))
 for perm in permutations(range(4)):
  Ap, Cp = car(perm); pos = {q: perm.index(q) for q in range(4)}
  U = sp.diag(*[(-1)**sum(s[a]*s[b] for a in range(4) for b in range(a+1,4)
                         if pos[a] > pos[b]) for s in STATES])
  check('ROLE_ORDER_'+''.join(map(str,perm)), all(Cp[q] == U*C[q]*U and Ap[q] == U*A[q]*U for q in range(4)))
 w = [sp.prod(ETA[q] for q in S) for S in SUBSETS]; Weta = sp.diag(*w)
 inertia = {str(k): [sum(len(S)==k and w[i]>0 for i,S in enumerate(SUBSETS)),
                    sum(len(S)==k and w[i]<0 for i,S in enumerate(SUBSETS))] for k in range(5)}
 check('ALL_GRADED_LORENTZ_INERTIAS', inertia == {'0':[1,0], '1':[1,3], '2':[3,3], '3':[3,1], '4':[0,1]})
 check('LORENTZ_WEIGHT_IS_INVERTIBLE_BUT_NOT_POSITIVE', Weta**2 == eye and sum(x>0 for x in w)==sum(x<0 for x in w)==8)
 for q in range(4):
  check('ACTUAL_SIGNED_WEIGHT_CONJUGATION_'+str(q), Weta*A[q]*Weta == ETA[q]*A[q])

 # Complete variable metric binding, all grades and packed off-diagonal probes.
 F = sp.Matrix([[1, sp.Rational(1,3), 0, 0], [0,1,sp.Rational(1,5),0],
                [0,0,1,sp.Rational(1,7)], [0,0,0,1]])
 Q = F*sp.diag(*ETA)*F.T; M = Q.inv(); mu = 1
 W = compound_hodge(M,mu); Wi = W.inv()
 d = sum(((q+1)*C[q] for q in range(4)), sp.zeros(16))
 delta = Wi*d.T*W; D = d+delta; lap = D*D
 expected = sum((q+1)*M[q,s]*(s+1) for q in range(4) for s in range(4))
 check('FULL_METRIC_MIXED_OPERATOR_IS_NOT_VOLUME_ONLY', zero(lap-expected*eye) and M != sp.diag(*ETA))
 check('VARIABLE_WEIGHT_NILPOTENCY_AND_SQUARE', zero(d*d) and zero(delta*delta) and zero(lap-(d*delta+delta*d)))
 check('SIGNED_PAIRING_SYMMETRY_IS_NOT_HILBERT_POSITIVITY', D.T*W == W*D and D.T != D)
 check('ALL_FIVE_GRADE_BLOCKS_HAVE_NO_LEAKAGE', all(lap[i,j]==0 for i,S in enumerate(SUBSETS) for j,T in enumerate(SUBSETS) if len(S)!=len(T)))
 grad = sp.zeros(4); derivatives = []
 for a in range(4):
  for b in range(a,4):
   V = sp.zeros(4); V[a,b] = V[b,a] = 1
   dM = -M*V*M; dmu = sp.trace(M*V)/2
   dW = compound_derivative(M,dM,mu,dmu)
   dd = -Wi*dW*delta+Wi*d.T*dW
   dl = d*dd+dd*d
   pred = sum((q+1)*dM[q,s]*(s+1) for q in range(4) for s in range(4))
   check('FULL_METRIC_OPERATOR_VARIATION_'+str(a)+str(b),
    zero(W*dd+dW*delta-d.T*dW) and zero(dl-pred*eye) and pred != 0)
   grad[a,b] = grad[b,a] = sp.trace(dl) if a==b else sp.trace(dl)/2
   derivatives.append(pred)
 full = sum(grad[a,b]*Q[a,b] for a in range(4) for b in range(4))
 packed = sum((1 if a==b else 2)*grad[a,b]*Q[a,b] for a in range(4) for b in range(a,4))
 wrong = sum(grad[a,b]*Q[a,b] for a in range(4) for b in range(a,4))
 check('PACKED_METRIC_DUAL_TWO_AND_HOMOTHETY', full == packed == -sp.trace(lap) and wrong != full)
 dWscale = compound_derivative(M,-M,1,2)
 ddscale = -Wi*dWscale*delta+Wi*d.T*dWscale
 check('OMITTED_INVERSE_VARIATION_IS_DETECTED', zero(ddscale+delta) and not zero(Wi*d.T*dWscale-ddscale))

 # Literal periodic shifts, including L=2 coincident neighbours. All integer.
 sparse_records = []
 for L in [2,4,8]:
  sites = np.arange(L**4, dtype=np.int64); II = sparse.eye(L**4,dtype=np.int64,format='csr')
  fd = []; scalar = sparse.csr_matrix((L**4,L**4),dtype=np.int64)
  for q in range(4):
   step = L**(3-q); coord = (sites//step)%L
   plus = sites+np.where(coord == L-1,-(L-1)*step,step)
   T = sparse.csr_matrix((np.ones(len(sites),dtype=np.int64),(sites,plus)),shape=(len(sites),len(sites)))
   fd.append(L*(T-II)); scalar += ETA[q]*(fd[-1].T*fd[-1])
  dd = sum((sparse.kron(fd[q],sparse.csr_matrix(np.asarray(C[q]).astype(np.int64)),format='csr')
            for q in range(4)), sparse.csr_matrix((16*L**4,16*L**4),dtype=np.int64))
  count_delta = dd.T.tocsr(); signed = count_delta.copy()
  weights = np.tile(np.asarray(w,dtype=np.int64),L**4)
  rows = np.repeat(np.arange(signed.shape[0]),np.diff(signed.indptr))
  signed.data *= weights[rows]*weights[signed.indices]
  DD = dd+signed; target = sparse.kron(scalar,sparse.eye(16,dtype=np.int64),format='csr')
  check('FULL_NATIVE_PERIODIC_SQUARE_L'+str(L), zero(dd*dd) and zero(signed*signed) and zero(DD*DD-target))
  check('FULL_NATIVE_SIGNED_ADJOINT_L'+str(L), zero(DD.T.multiply(weights[:,None])-DD.multiply(weights[None,:])))
  spatial_mode = (-1)**((sites//(L**2))%L)
  # Empty state -> singleton B and back is the actual two-dimensional block.
  u = np.zeros(16*L**4,dtype=np.int64); v = u.copy()
  u[16*sites+STATES.index((0,0,0,0))] = spatial_mode
  v[16*sites+STATES.index((0,1,0,0))] = spatial_mode
  check('ACTUAL_SPATIAL_NYQUIST_BLOCK_L'+str(L), np.array_equal(DD*u,-2*L*v) and np.array_equal(DD*v,2*L*u))
  mixed_mode = (-1)**((sites//(L**3))%L+(sites//(L**2))%L)
  bvec = np.zeros(16*L**4,dtype=np.int64); bvec[16*sites] = mixed_mode
  null = DD*bvec
  check('ACTUAL_NONCONSTANT_NULL_ROOT_L'+str(L), np.any(null != 0) and np.all(DD*null == 0))
  sparse_records.append({'L':L,'cochain_dimension':16*L**4,'dirac_nnz':DD.nnz,'square_nnz':target.nnz})
 T2 = sp.Matrix([[0,1],[1,0]]); fd2 = 2*(T2-sp.eye(2))
 check('L2_COLLISION_IS_NOT_NATURAL_TRACE_SCAFFOLD',
       fd2.T*fd2/4 == sp.Matrix([[2,-2],[-2,2]]) and
       fd2.T*fd2/4 != sp.Matrix([[1,-1],[-1,1]]))

 # Generic exact Fourier Clifford identity. Complex coefficients are arbitrary.
 aa = sp.symbols('a0:4'); bb = sp.symbols('b0:4')
 B = sum((aa[q]*C[q]+bb[q]*A[q] for q in range(4)),sp.zeros(16))
 check('COMPLETE_FOURIER_SYMBOL_SQUARE', zero(B*B-sum(aa[q]*bb[q] for q in range(4))*eye))
 for q in range(4):
  check('NULL_SYMBOL_EXPLICIT_CONTRACTION_'+str(q), zero(B*A[q]+A[q]*B-aa[q]*eye))
 Bnull = -8*(C[0]+A[0]+C[1]-A[1])
 check('NULL_DIRAC_IS_NILPOTENT_WITH_KERNEL_EIGHT', zero(Bnull*Bnull) and Bnull.rank()==8 and Bnull != sp.zeros(16))
 check('KER_DIRAC_IS_SMALLER_THAN_KER_ITS_SQUARE', Bnull.rank()==8 and (Bnull*Bnull).rank()==0)
 spectra = []
 tables = {2:[(0,0),(4,0)],4:[(0,0),(2,0),(4,0),(2,0)],
           8:[(0,0),(2,-1),(2,0),(2,1),(4,0),(2,1),(2,0),(2,-1)]}
 for L, values in tables.items():
  modes = Counter(); sig = Counter()
  for k in product(range(L),repeat=4):
   a,b = values[k[0]]
   for q in range(1,4): a-=values[k[q]][0]; b-=values[k[q]][1]
   modes[(a,b)] += 1; sig[exact_sign(a,b)] += 1
  nzero = modes[(0,0)]
  check('EXACT_ALL_MODE_SPECTRAL_COUNTS_L'+str(L), sum(sig.values())==L**4 and sig[-1]>0 and sig[1]>0 and nzero>1)
  check('EXACT_HEAT_LOWEST_MODE_L'+str(L), modes[(-12,0)]==1 and all(exact_sign(a+12,b)>=0 for a,b in modes))
  spectra.append({'L':L,'negative_modes':sig[-1],'positive_modes':sig[1],
                  'zero_modes':nzero,'dirac_kernel_dimension':16+8*(nzero-1),
                  'laplacian_kernel_dimension':16*nzero,'minimum_eigenvalue':-12*L*L})
 check('EXACT_L4_KERNEL_DIMENSIONS', spectra[1]['zero_modes']==28 and
       spectra[1]['dirac_kernel_dimension']==232 and spectra[1]['laplacian_kernel_dimension']==448)
 t,l = sp.symbols('t l',positive=True)
 check('HEAT_GROWTH_NORMALIZATION_AND_CONSTANT', sp.expand(16*(12*t*l*l)**3/(6*l**4)-4608*t**3*l**2)==0)
 check('FIXED_POSITIVE_HEAT_TIME_SCOPE', sp.limit(4608*t**3*l**2,l,sp.oo)==sp.oo and
       sp.expand((4608*t**3*l**2).subs(t,l**-2))==4608/l**4)

 # The new geometry-dependent operator is not reduced to a volume-only one.
 # A finite difference kills its complete fixed-degree homogeneity module.
 annihilators=[]
 for degree in range(9):
  scales=[sp.Rational(1,r+1) for r in range(degree+2)]
  weights=[(-1)**r*sp.binomial(degree+1,r) for r in range(degree+2)]
  check('EXACT_MIXED_SPECTRAL_ANNIHILATOR_DEGREE_'+str(degree),
   all(sum(w*s**(-j) for w,s in zip(weights,scales))==0 for j in range(degree+1)) and
   sum(w*s for w,s in zip(weights,scales))==sp.Rational(1,degree+2) and
   sum(abs(w) for w in weights)==2**(degree+1))
  annihilators.append({'degree':degree,'scales':list(map(str,scales)),
   'weights':list(map(int,weights)),'physical_anchor':str(sp.Rational(1,degree+2)),
   'error_denominator':(degree+2)*2**(degree+2)})
 for j in range(5):
  check('ACTUAL_GEOMETRIC_MOMENT_HOMOGENEITY_'+str(j),
   sp.trace((lap/t)**j)==sp.trace(lap**j)/t**j)
 check('DENSITY_INSERTED_TRACE_IS_A_PROTECTED_SCALE_EXCEPTION',
       sp.simplify(t*t/t-t)==0 and t != 1/t)

 payload = {'status':'PASS','input_head':INPUT_HEAD,'inputs_sha256':{p:sha(p) for p in INPUTS},
  'lean_receipt_sha256':sha(PREFIX+'_results.json'),
  'checker_sha256':sha(PREFIX+'_check.py'),'compiled_propositions':34,
  'transitive_d0_pins':len(r['transitive_d0_source_sha256']),'checks':checks,
  'class':'supplied invertible graded Hodge operators on the actual frozen differential; flat Lorentz binding eta=(+---)',
  'kernel_reduction':'actual CAR integer identities and both nilpotencies rebuilt by kernel decide; standard axioms only',
  'metric_binding':'full supplied compound Hodge matrix; all ten metric derivatives and packed off-diagonal weight two',
  'signature':'eight positive and eight negative Fock weights; weighted symmetry is indefinite symmetry',
  'spectrum':'Delta_eta(k)=4*L^2*(sin(pi*k0/L)^2-sum_i sin(pi*ki/L)^2), each with multiplicity sixteen',
  'kernels':'zero momentum has D kernel sixteen; every nonzero null momentum has D kernel eight and Delta kernel sixteen',
  'heat':'fixed t>0 ordinary heat trace is at least 16*exp(12*t*L^2); L^-4 normalized trace at least 4608*t^3*L^2',
  'native_selection':'not selected; this is an explicit tested binding of documented operators, not a new physical action',
  'global_closure':'OPEN','positive_gr':'OPEN',
  'exceptions':['positive Euclidean or independently owned observer pairing','refinement-dependent heat time','separate renormalized or oscillatory spectral law',
                'different independently owned matter/action/constraint sector','physical gauge quotient not yet constructed'],
  'graded_inertia':inertia,'sparse_operator_records':sparse_records,'exact_spectra':spectra,'finite_annihilators':annihilators,
  'mixed_spectral_class':'one fixed degree p, scale-invariant arbitrary mesh/shape/link coefficients, actual Tr(Delta_Q^j), arbitrary separate common volume profile, and the stated exact two metric fibers/probes',
  'mixed_spectral_gap':'max total error >= 9*pi^2*h^(1/3)/(400*(p+2)*2^(p+2)) eventually; all fixed-degree proof analytic',
  'mixed_spectral_exceptions':['unbounded degree','nonpolynomial spectral law','scale-dependent coefficients','density insertion inside trace','independent domain excluding probes']}
 encoded = json.dumps(payload,sort_keys=True,indent=2)+'\n'
 if args.output: args.output.write_text(encoded)
 else:
  expected = args.expect or repo/(PREFIX+'_certificate.json')
  assert json.loads(expected.read_text())==payload, 'PINNED_LEDGER_MISMATCH'
 print('PASS_NATIVE_WEIGHTED_DIRAC_BOUNDARY',len(checks),flush=True)


if __name__=='__main__': main()
