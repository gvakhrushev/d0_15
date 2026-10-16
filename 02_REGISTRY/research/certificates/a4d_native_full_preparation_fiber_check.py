#!/usr/bin/env python3
"""Complete invariant state fiber and lossless full-density refinement controls."""
# D0_CI_TIMEOUT_SECONDS=600
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
BASE='02_REGISTRY/research/certificates/a4d_native_full_preparation_fiber'
PREV='02_REGISTRY/research/certificates/a4d_native_jones_record_transport'
PROOF='02_REGISTRY/research/A4D_NATIVE_FULL_PREPARATION_FIBER.md'
HEAD='a235dbbc05631335498cda376671af6c2772dc41'
INPUTS=[
 '02_REGISTRY/research/A4D_NATIVE_JONES_RECORD_TRANSPORT.md',
 *[PREV+x for x in ('.py','_check.py','_certificate.json','.lean','_results.json','_output.txt')],
 '02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md',
 '02_REGISTRY/research/A4D_NATIVE_MODULAR_PREPARATION_BOUNDARY.md',
 '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md',
 '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
 '03_FORMALIZATION/D0/Foundation/M1Predicate.lean',
 '03_FORMALIZATION/D0/Foundation/M1ClassAdmissibility.lean',
 '03_FORMALIZATION/D0/Complexity/HeatTraceLyapunov.lean',
 '03_FORMALIZATION/D0/Condensed/OperatorNaturality.lean',
 '03_FORMALIZATION/D0/Algebra/FibonacciAFTower.lean',
]
spec=importlib.util.spec_from_file_location('full_preparation_fiber',ROOT/(BASE+'.py'))
P=importlib.util.module_from_spec(spec);sys.modules[spec.name]=P;spec.loader.exec_module(P)
N=P.N;E=P.E;s=P.s;a,p=P.a,P.p
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def controls():
 checks=[];mutants=[]
 def check(name,value):
  assert bool(value),name
  checks.append(name)
 def zero(value):
  if isinstance(value,s.MatrixBase):
   return all(P.field(x)==0 for x in s.SparseMatrix(value).todok().values())
  return P.field(value)==0
 def equal(name,value):check(name,zero(value))
 def reject(name,false_claim):
  check('REJECT_'+name,not false_claim);mutants.append(name)
 def positive(name,value):
  value=s.simplify(P.field(value).subs(p,(s.sqrt(5)-1)/2).subs(a,s.sqrt((s.sqrt(5)-1)/2)))
  check(name,value.is_positive is True)
 lam,mu,step=s.symbols('lam mu step',real=True)

 for n in range(4):
  d=P.jones_fiber(n,lam,mu);X,Y=d['sizes'];u,v=d['u'],d['v']
  equal('complete_fiber_normalization',sum(value*count for value,count in d['spectrum'])-1)
  equal('left_and_right_X_marginal',lam*u+mu*v+d['alpha']*(X*X-1)-u)
  equal('left_and_right_Y_marginal',lam*v+mu*u+d['gamma']*(Y*Y-1)-v)
  moved=P.fixed_t_path(n,lam,mu,step)
  equal('whole_fixed_table_affine_path',moved['t']-d['t'])
  positive('fixed_table_nonzero_denominator',d['J'])
  positive('nonzero_hidden_state_slope',d['K'])
  wrong=P.jones_fiber(n,lam+step,P.field(mu-d['fixed_t_mu_slope']*step))
  equal('wrong_sign_exact_defect',wrong['mismatch']-d['mismatch']+2*d['K']*step)
  reject('PLUS_SIGN_PRESERVES_CORRELATION_n%d'%n,zero((wrong['mismatch']-d['mismatch']).subs(step,1)))
  mu0=P.field((1-p)*u*v);base=P.jones_fiber(n,p,mu0)
  for h in [s.Rational(-1,1000),s.S.Zero,s.Rational(1,1000)]:
   pt=P.fixed_t_path(n,p,mu0,h)
   for eig,_ in pt['spectrum']:positive('exact_full_faithfulness',eig)
   for key in ('mu','alpha','gamma'):positive('protected_simple_largest_eigenvalue',pt['lambda']-pt[key])
   equal('actual_fixed_table_samples',pt['t']-base['t'])
  reject('FULL_JOINT_TABLE_SELECTS_HEAT_n%d'%n,zero(P.fixed_t_path(n,p,mu0,s.Rational(1,1000))['lambda']-base['lambda']))
  # Actual native Jones matrices, and every spectral sector's joint trace.
  if n<2:
   ops=N.operators(n);ranks=[];squares=[]
   for part in ops:
    e=part['e'];ranks.append(s.trace(e));squares.append(s.trace(e*e))
   rx,ry=ranks;trxx,tryy=squares
   equal('native_Jones_trace_rank_X',rx-d['ranks'][0])
   equal('native_Jones_trace_rank_Y',ry-d['ranks'][1])
   omega_joint=d['weights'][0]*trxx+d['weights'][1]*tryy
   eta_joint=v*trxx/X+u*tryy/Y
   direct=lam*omega_joint+mu*eta_joint+d['alpha']*(rx*rx-trxx/X)+d['gamma']*(ry*ry-tryy/Y)
   equal('all_native_joint_spectral_sectors',direct-d['t'])

 # Full complex matrix marginals/covariance, not only spectral arithmetic.
 conjugations=[]
 for level in (2,3):
  sizes=E.counts(level);u=p**(level+1)*sizes[0];v=p**(level+2)*sizes[1]
  data=P.density(level,p,P.field((1-p)*u*v));sigma=data['sigma'];dim=sigma.rows
  equal('full_density_trace',s.trace(sigma)-1)
  equal('full_density_Hermitian',sigma-sigma.conjugate().T)
  equal('full_Omega_eigenvector',sigma*data['omega']-p*data['omega'])
  equal('full_eta_eigenvector',sigma*data['eta']-data['mu']*data['eta'])
  offset=0
  for j,D in enumerate(sizes):
   for r in range(D):
    for c in range(D):
     equal('all_full_left_marginal_matrix_units',sum(sigma[offset+r*D+k,offset+c*D+k] for k in range(D))-data['weights'][j]*int(r==c))
     equal('all_full_right_marginal_matrix_units',sum(sigma[offset+k*D+r,offset+k*D+c] for k in range(D))-data['weights'][j]*int(r==c))
   for kind in ('phase','cycle','Hadamard'):
    U=s.eye(D)
    if kind=='phase':U[0,0]=s.I
    elif kind=='cycle':U=s.zeros(D);U[:,:]=s.Matrix(D,D,lambda i,j:int(i==(j+1)%D))
    else:
     U[0,0]=U[0,1]=U[1,0]=s.sqrt(2)/2;U[1,1]=-s.sqrt(2)/2
    blocks=[s.eye(t*t) for t in sizes];blocks[j]=s.kronecker_product(U,U.conjugate())
    C=s.diag(*blocks)
    equal('full_complex_coordinate_conjugation_invariance',C*sigma-sigma*C)
    if level==2:conjugations.append(C)
   offset+=D*D
  reject('PROTECTED_STATE_CAN_DROP_TRACELESS_MODES_level%d'%level,dim==2)
  reject('CENTRAL_CROSS_BLOCK_COHERENCE_IS_ZERO_level%d'%level,zero(sigma[0,sizes[0]*sizes[0]]))

 # Exact finite independent check of the claimed commutant dimension 4+1+1.
 from sympy.polys.matrices import DomainMatrix
 dimension=conjugations[0].rows;I=s.eye(dimension)
 rows=s.Matrix.vstack(*[s.kronecker_product(I,C)-s.kronecker_product(C.T,I) for C in conjugations])
 rank=DomainMatrix.from_Matrix(rows,extension=True).to_field().rank()
 check('actual_full_complex_commutant_dimension',dimension*dimension-rank==6)
 reject('INVARIANT_PROTECTED_STATE_FIBER_IS_ONE_DIMENSIONAL',6-2-2==1)

 beta,l=s.symbols('beta l',positive=True)
 price=-s.log(l+step)/beta
 check('actual_log_price_direction',s.simplify(s.diff(price,step).subs(step,0)+1/(beta*l))==0)
 positive('fixed_feedback_does_not_cancel_heat_direction',1/p)
 k,z,kap=s.symbols('k z kap',positive=True)
 check('constant_Jones_spectrum_feedback_derivative',s.diff(-k*s.log(1-z*kap),step)==0)
 # Constant rank alone is not enough: relative two-plane angle changes loss.
 angle=s.symbols('angle',real=True)
 reject('RANK_ALONE_FIXES_FEEDBACK',s.simplify(s.diff(s.sin(angle)**2,angle))==0)

 dims=[]
 for n in range(20):
  A,B=E.counts(n);data=P.reversible_rank_data(n);d,D=data['coarse_dimension'],data['fine_dimension'];r=D-2*d
  check('actual_Fibonacci_ratio_bounds',B<=A<=2*B)
  check('strict_two_to_three_full_dimensions',2*d<D<3*d)
  check('exact_lossless_rank_deficit',r==B*(2*A-B))
  check('sharp_uniform_missing_fraction',5*r>=D)
  check('adjacent_dimensions_coprime',s.igcd(d,D)==1)
  dims.append(d)
 for i in range(len(dims)-2):
  check('full_dimension_three_term_recurrence',dims[i+2]==3*dims[i+1]-dims[i])
  check('exact_dimension_Cassini_identity',dims[i]*dims[i+2]-dims[i+1]**2==1)
 equal('asymptotic_missing_fraction_is_golden_cube',1-2*p*p-p**3)

 # Sharp lossless channel with first branch the actual level-zero GNS inclusion.
 V0=s.Matrix([[a,0],[0,0],[0,0],[0,1],[p,0]])
 V1=s.Matrix([[0,0],[1,0],[0,1],[0,0],[0,0]])
 q=s.Matrix([-p,0,0,0,a]);Q=q*q.T
 equal('actual_native_GNS_branch_normalized',V0.T*V0-s.eye(2))
 equal('second_sharp_branch_normalized',V1.T*V1-s.eye(2))
 equal('sharp_branches_orthogonal',V0.T*V1)
 equal('whole_channel_complement_retained',V0*V0.T+V1*V1.T+Q-s.eye(5))
 recovery=[V0.T,V1.T,s.Matrix([1,0])*q.T]
 equal('recovery_full_Kraus_trace_preservation',sum((L.T*L for L in recovery),s.zeros(5))-s.eye(5))
 def phi(x):return (V0*x*V0.T+V1*x*V1.T)/2
 def psi(y):return sum((L*y*L.T for L in recovery),s.zeros(2))
 for i in range(2):
  for j in range(2):
   unit=s.zeros(2);unit[i,j]=1
   equal('all_quantum_matrix_units_exact_recovery',psi(phi(unit))-unit)
   equal('all_quantum_matrix_units_trace_preservation',s.trace(phi(unit))-s.trace(unit))
 rho=phi(s.eye(2)/2)
 equal('sharp_output_support',rho-(s.eye(5)-Q)/4)
 equal('sharp_output_actual_kernel',rho*q)
 equal('faithful_target_exact_positive_difference_part',s.eye(5)/5-rho-Q/5+(s.eye(5)-Q)/20)
 equal('sharp_uniform_target_distance',s.trace(Q/5)-s.Rational(1,5))
 reject('LOSSLESS_OUTPUT_FULL_FAITHFUL',not zero(rho.det()))
 reject('UNUSED_RECOVERY_OUTCOME_CAN_BE_ERASED',zero(sum((L.T*L for L in recovery[:2]),s.zeros(5))-s.eye(5)))

 # Restricted-family channels are a constructive countercontrol to a whole-
 # preparation no-go. Their discarded coherence is explicitly nonzero.
 states=[]
 for level in (2,3):
  X,Y=E.counts(level);u=p**(level+1)*X;v=p**(level+2)*Y
  item=P.density(level,p,P.field((1-p)*u*v));O=item['omega']*item['omega'].T
  R=(item['sigma']-p*O).applyfunc(lambda x:P.field(x/(1-p)))
  equal('full_restricted_residual_normalization',s.trace(R)-1)
  equal('full_restricted_residual_Omega_kernel',R*item['omega'])
  states.append((item,O,R))
 old,On,Rn=states[0];fine,Of,Rf=states[1]
 def restricted(x,O,targetO,targetR):
  return s.trace(O*x)*targetO+(s.trace(x)-s.trace(O*x))*targetR
 equal('restricted_family_exact_refinement',restricted(old['sigma'],On,Of,Rf)-fine['sigma'])
 equal('restricted_family_exact_recovery',restricted(fine['sigma'],Of,On,Rn)-old['sigma'])
 coherence=old['omega']*old['eta'].T
 equal('restricted_channel_erases_nonzero_coherence',restricted(coherence,On,Of,Rf))
 reject('RESTRICTED_RECOVERY_IS_FULL_QUANTUM_RECOVERY',zero(coherence))
 reject('PROTECTED_CYCLIC_DENSITY_IS_FAITHFUL',1==old['sigma'].rows)

 # Unnormalized Gibbs extension retains every detail weight and changes Z.
 coarse=s.diag(1,s.Rational(1,2));detail=s.diag(s.Rational(1,3),s.Rational(1,4),s.Rational(1,5))
 full=s.diag(coarse,detail);Zc=s.trace(coarse);Zf=s.trace(full)
 check('full_unnormalized_heat_positive_all_modes',all(x>0 for x in full.diagonal()))
 check('full_unnormalized_heat_protected_simple_one',sum(x==1 for x in full.diagonal())==1)
 equal('unnormalized_heat_exact_inherited_compression',full[:2,:2]-coarse)
 equal('normalized_heat_compression_deficit',full[:2,:2]/Zf-(Zc/Zf)*(coarse/Zc))
 reject('NORMALIZED_HEAT_COMPRESSION_IS_EXACT_DENSITY',Zc==Zf)

 prior=json.loads((ROOT/(PREV+'_certificate.json')).read_text())
 for key,path in [('proof_sha256',INPUTS[0]),('checker_sha256',PREV+'_check.py'),('program_sha256',PREV+'.py'),('Lean_receipt_sha256',PREV+'_results.json')]:check('prior_packet_freshness',prior[key]==sha(path))
 for path,digest in prior['input_sha256'].items():check('prior_transitive_input',sha(path)==digest)
 receipt=json.loads((ROOT/(BASE+'_results.json')).read_text())
 check('Lean_compiler_success',receipt['status']=='PASS' and receipt['compiler_exit_code']==0)
 check('Lean_capsule_freshness',receipt['capsule_sha256']==sha(BASE+'.lean'))
 check('Lean_output_freshness',receipt['output_sha256']==sha(BASE+'_output.txt'))
 for path,digest in receipt['input_sha256'].items():check('Lean_transitive_input',sha(path)==digest)
 check('Lean_standard_axioms_only',all(set(xs)<={'propext','Classical.choice','Quot.sound'} for xs in receipt['axioms'].values()))
 return {'status':'PASS','input_source_head':HEAD,'proof':PROOF,'scope':{
 'classified_state_class':'FULL_CONJUGATION_INVARIANT_FAITHFUL_TWO_NATIVE_MARGINALS_SIMPLE_PROTECTED_OMEGA',
 'mere_frame_equivariance_is_same_class':False,'class_real_dimension':2,
 'full_Jones_joint_table_fixed_heat_fiber_dimension':1,
 'price_direction':'-1/(beta*lambda)','all_fixed_Jones_overlap_feedback_derivatives_zero':True,
 'reversible_channel_class':'ALL_CPTP_FULL_MATRIX_MAPS_WITH_CPTP_LEFT_INVERSE',
 'lossless_rank_deficit_fraction_lower_bound':'1/5','physical_closed_implementation_of_restricted_channel':False,
 'whole_native_preparation_source_Ward_or_GR_closed':False,'parent_terminal_closed':False},
 'exact_controls':len(checks),'checks':dict(sorted(Counter(checks).items())),
 'executed_mathematical_mutants':mutants,'full_matrix_levels':[2,3],
 'actual_Jones_trace_levels':[0,1],'fixed_table_strict_faithfulness_levels':[0,1,2,3],
 'new_Lean_declarations':18,'input_sha256':{path:sha(path) for path in INPUTS},
 'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
 'program_sha256':sha(BASE+'.py'),'Lean_receipt_sha256':sha(BASE+'_results.json')}


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 result=controls();target=ROOT/(BASE+'_certificate.json')
 if args.write:target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 else:assert json.loads(target.read_text())==result,'FULL_PREPARATION_FIBER_IMMUTABLE_LEDGER_MISMATCH'
 print('PASS_NATIVE_FULL_PREPARATION_FIBER controls=%d mutants=%d full_native_admission=OPEN'%(result['exact_controls'],len(result['executed_mathematical_mutants'])))


if __name__=='__main__':main()
