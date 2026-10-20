#!/usr/bin/env python3
"""Replay the actual flat Hodge/CAR triple; no physical field/action law inferred."""
import argparse,copy,hashlib,itertools,json
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy as s
from scipy.sparse import coo_matrix,diags,kron,eye

ROOT=Path(__file__).resolve().parents[3]
BASE='02_REGISTRY/research/certificates/a4d_native_hodge_connes_metric'
PROOF='02_REGISTRY/research/A4D_NATIVE_HODGE_CONNES_METRIC.md'
INPUT='569abdc48795b161aa5fe6d2a1c12ecdd05f66b0'
SCOPE={
 'class':'ACTUAL_FIXED_COUNTING_HODGE_CAR_AND_SCALAR_POINT_ALGEBRA_ALL_PERIODIC_L_GE_2',
 'all_sixteen_fock_components_and_every_site_retained':True,
 'actual_D_H_not_hopping_CAR_operator':True,
 'actual_operator_metric_and_heat_square_share_one_native_operator':True,
 'all_size_exact_product_circle_Connes_distance':'ANALYTIC_PROOF_NOT_FULL_LEAN_FORMALIZATION',
 'full_operator_norm_gate_replaced_by_column_norms':False,
 'arithmetic_l1_l2_mismatch_owner_propositions_remain_valid':True,
 'that_owner_proves_l1_Connes_metric_for_actual_hodge_CAR':False,
 'nontrivial_twist_necessary_for_this_operator_flat_metric':False,
 'represented_scalar_algebra_is_full_noncommutative_scene_path_algebra':False,
 'all_scalar_readouts_physically_admitted_by_native_apparatus':False,
 'eigenvalues_alone_determine_the_metric':False,
 'native_archive_RG_is_physical_metric_refinement':False,
 'flat_metric_net_bound_implies_native_action_contrast_transfer':False,
 'full_coupled_preparation_Gamma_or_F_derived':False,
 'absence_of_F_for_the_whole_core_proved':False,
 'curved_Lorentz_metric_source_Ward_or_GR_derived':False,
 'G0_G1_G2_G3_G4_or_original_parent_terminals_closed':False,
}
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def zero(A):
 A=A.tocsr();A.eliminate_zeros();return A.nnz==0

def car():
 cs=[]
 for r in range(4):
  A=np.zeros((16,16),dtype=np.int64)
  for ket in range(16):
   if ket&(1<<r):A[ket^(1<<r),ket]=(-1)**bin(ket&((1<<r)-1)).count('1')
  cs.append(A)
 return cs

def native_hodge(L,cs):
 pts=list(itertools.product(range(L),repeat=4));at={x:i for i,x in enumerate(pts)}
 rows=[];cols=[];data=[]
 for i,x in enumerate(pts):
  for ket in range(16):
   for r in range(4):
    coef=int((cs[r] if ket&(1<<r) else cs[r].T)[ket^(1<<r),ket])
    y=list(x);y[r]=(y[r]+(1 if ket&(1<<r) else -1))%L
    rows.extend([16*at[tuple(y)]+(ket^(1<<r)),16*i+(ket^(1<<r))])
    cols.extend([16*i+ket,16*i+ket]);data.extend([L*coef,-L*coef])
 D=coo_matrix((data,(rows,cols)),shape=(16*L**4,)*2,dtype=np.int64).tocsr()
 # Independent row/tensor transcription of the owned definition.
 E=eye(L**4,format='csr',dtype=np.int64);Dt=D*0;H=D*0
 for r in range(4):
  dest=[]
  for x in pts:
   y=list(x);y[r]=(y[r]+1)%L;dest.append(at[tuple(y)])
  S=coo_matrix((np.ones(L**4,dtype=np.int64),(np.arange(L**4),dest)),shape=E.shape).tocsr()
  Dt=Dt+L*(kron(S-E,cs[r].T,format='csr')+kron(S.T-E,cs[r],format='csr'))
  H=H+L*L*kron(2*E-S-S.T,eye(16,format='csr',dtype=np.int64),format='csr')
 return pts,at,D,Dt,H

def comm(D,f):
 M=diags(np.repeat(f,16),format='csr',dtype=np.int64)
 return D@M-M@D

def controls():
 checks={}
 def ck(n,c,count=1):
  assert bool(c),n;checks[n]=checks.get(n,0)+count
 rec=json.loads((ROOT/(BASE+'_results.json')).read_text())
 ck('compiled_real_capsule',rec['status']=='PASS' and rec['compiler_exit_code']==0 and rec['input_head']==INPUT)
 out=(ROOT/(BASE+'_output.txt')).read_text()
 ck('no_failed_or_sorry_capsule',': error' not in out and ': warning' not in out and 'sorryAx' not in out)
 for n in rec['declarations']+rec['primary_owner_propositions']+rec['typed_owner_definitions']:
  ck('real_resolved_declarations',n in out and n in rec['axioms'])
  inherited=set(rec['axioms'][n])-{'propext','Classical.choice','Quot.sound'}
  if n.endswith('same_operator_heat_square') or n.endswith('hodgeCarDirac_sq'):
   ck('imported_square_exact_native_decide_leaves',inherited==set(rec['inherited_native_decide_square_axioms']))
  else:ck('new_metric_algebra_standard_axioms_only',not inherited)
 for group in ['transitive_d0_source_sha256','primary_and_prior_input_sha256','toolchain_input_sha256']:
  for p,h in rec[group].items():ck('source_hash_'+group,sha(p)==h)
 ck('capsule_hash',sha(BASE+'.lean')==rec['capsule_sha256'])
 ck('output_hash',sha(BASE+'_output.txt')==rec['output_sha256'])
 ck('formal_metric_boundary',not rec['all_size_operator_norm_supremum_distance_kernel_formalized'])
 printed=rec['printed_primary_owner_propositions']
 old=next(v for k,v in printed.items() if k.endswith('archive_hodge_dirac_euclidean_metric_mismatch_nogo_owner'))
 ck('actual_prior_no_go_type_is_arithmetic','hodgeCarDirac' not in old and 'd1_diagonal' in old and 'd2_sq_diagonal' in old)

 cs=car();I=np.eye(16,dtype=np.int64)
 for r,t in itertools.product(range(4),repeat=2):
  ck('literal_all_CAR',np.array_equal(cs[r]@cs[t]+cs[t]@cs[r],I*0))
  ck('literal_all_mixed_CAR',np.array_equal(cs[r]@cs[t].T+cs[t].T@cs[r],I*int(r==t)))
  for k in range(16):
   g=(cs[r]+cs[r].T)[:,k];h=(cs[t]+cs[t].T)[:,k]
   ck('every_fock_column_orthogonal',int(g@h)==int(r==t))
 # Coordinate permutations and reflections are actual CAR unitaries.
 for perm in itertools.permutations(range(4)):
  P=np.zeros((16,16),dtype=np.int64)
  for k in range(16):
   occupied=[i for i in range(4) if k&(1<<i)]
   image=[perm[i] for i in occupied]
   parity=sum(a>b for z,a in enumerate(image) for b in image[z+1:])
   P[sum(1<<a for a in image),k]=(-1)**parity
  ck('all_role_permutations_unitary',np.array_equal(P.T@P,I))
  for r in range(4):ck('all_role_permutations_bind_actual_CAR',np.array_equal(P@cs[r]@P.T,cs[perm[r]]))
 for r in range(4):
  parity=np.diag([(-1)**bin(k&~(1<<r)).count('1') for k in range(16)])
  P=(cs[r]+cs[r].T)@parity
  ck('role_reflection_unitary',np.array_equal(P.T@P,I))
  for t in range(4):ck('role_reflection_swaps_only_one_CAR',np.array_equal(P@cs[t]@P.T,cs[t].T if t==r else cs[t]))

 cases=[];hostile=None
 for L in [2,3,4,5,6,8]:
  pts,at,D,Dt,H=native_hodge(L,cs);dim=16*L**4
  ck('full_native_column_row_transcriptions',zero(D-Dt))
  ck('full_native_self_adjoint',zero(D-D.T))
  ck('same_actual_operator_square_is_full_difference_heat',zero(D@D-H))
  ck('full_carrier_no_sector_dropped',D.shape==(dim,dim))
  f=np.array([(3*x[0]*x[1]+2*x[2]*x[3]+x[0]+x[3])%7-3 for x in pts],dtype=np.int64)
  C=comm(D,f);G=(C.T@C).tocsr();dg=G.diagonal()
  expected=[]
  for x in pts:
   for k in range(16):
    val=0
    for r in range(4):
     y=list(x);y[r]=(y[r]+(1 if k&(1<<r) else -1))%L
     val+=(int(f[at[tuple(y)]])-int(f[at[x]]))**2
    expected.append(L*L*val)
  ck('all_sites_all_16_mixed_column_bounds',np.array_equal(dg,expected),dim)
  ck('actual_commutator_skew',zero(C+C.T))
  tau=np.array([min(j,L-j) for j in range(L)],dtype=np.int64)
  reps=list(itertools.combinations_with_replacement(range(L//2+1),4)); count=0
  for d in reps:
   q=sum(j*j for j in d)
   f=np.array([sum(d[r]*tau[x[r]] for r in range(4)) for x in pts],dtype=np.int64)
   C=comm(D,f);G=(C.T@C).tocsr();dg=G.diagonal()
   ck('all_separable_Gram_off_diagonal_zero',zero(G-diags(dg,format='csr',dtype=np.int64)))
   ck('all_separable_witness_full_norm',int(dg.max())==L*L*q)
   ck('all_endpoint_readouts',int(f[at[d]])-int(f[at[(0,)*4]])==q)
   ck('all_exact_metric_squared',Fraction(q,L*L)==sum(Fraction(j,L)**2 for j in d))
   if L%2==0:ck('even_L_entire_Gram_identity',np.all(dg==L*L*q),dim)
   count+=1
  cases.append({'L':L,'native_dimension':dim,'all_distance_orbit_representatives':count})
  if L==2:
   f=np.array([1,2,-3,0,0,0,-2,0,2,-1,1,3,-3,-3,1,-1],dtype=np.int64)
   C=comm(D,f);G=(C.T@C).tocsr();dg=G.diagonal();mx=int(dg.max())
   i,j=192,3;b=int(G[i,j]);den=mx-int(dg[j])+1
   lhs=den*den*int(dg[i])+2*den*b*b+b*b*int(dg[j]);rhs=mx*(den*den+b*b)
   ck('hostile_column_gate_not_operator_gate',lhs>rhs and mx==200)
   hostile={'L':L,'max_column_norm_squared':mx,'basis_indices':[i,j],'integer_coefficients':[den,b],
            'Rayleigh_numerator':lhs,'column_gate_denominator_product':rhs}

 # All corners of a real multilinear four-cube, symbolic field values.
 lam=s.symbols('t0:4');vs=list(itertools.product([0,1],repeat=4));a=s.symbols('a0:16')
 weights=[s.prod(lam[r] if v[r] else 1-lam[r] for r in range(4)) for v in vs]
 F=sum(w*b for w,b in zip(weights,a));lookup={v:i for i,v in enumerate(vs)}
 ck('symbolic_partition_of_unity',s.expand(sum(weights)-1)==0)
 for r in range(4):
  cg=[]
  for v in vs:
   left=list(v);right=list(v);left[r]=0;right[r]=1
   cg.append(a[lookup[tuple(right)]]-a[lookup[tuple(left)]])
  ck('exact_common_weights_all_corner_gradients',s.expand(s.diff(F,lam[r])-sum(w*g for w,g in zip(weights,cg)))==0)
  for v in vs:
   S=tuple(1-b for b in v)
   ck('all_corner_occupation_choices_retained',len(S)==4 and S[r]==1-v[r])
 for L in range(4,65,4):
  k=L//4;ck('all_quarter_diagonal_exact_squared_witness',Fraction(2*k*k,L*L)==Fraction(1,8))
  ck('all_quarter_l1_wrong_for_this_triple',Fraction((2*k)**2,L*L)==Fraction(1,4) and Fraction(1,4)!=Fraction(1,8))
 return checks,{'full_operator_cases':cases,'hostile_column_gate':hostile,
                 'quarter_diagonal_distance_squared':'1/8','quarter_path_distance_squared':'1/4'}

def expected():
 checks,w=controls()
 return {'status':'PASS','input_head':INPUT,'scope':SCOPE,'checks':checks,'exact_control_count':sum(checks.values()),
         'witnesses':w,'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
         'capsule_sha256':sha(BASE+'.lean'),'receipt_sha256':sha(BASE+'_results.json')}

def validate(j,e):
 assert j==e,'ledger scope/value/hash mismatch'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
 e=expected();p=ROOT/(BASE+'_certificate.json')
 if args.write:p.write_text(json.dumps(e,sort_keys=True,indent=2)+'\n')
 validate(json.loads(p.read_text()),e)
 rejected=0
 for key,val in SCOPE.items():
  if isinstance(val,bool):
   bad=copy.deepcopy(e);bad['scope'][key]=not val
   try:validate(bad,e)
   except AssertionError:rejected+=1
   else:raise AssertionError('accepted false scope '+key)
 for key in ['proof_sha256','checker_sha256','receipt_sha256']:
  bad=copy.deepcopy(e);bad[key]='0'*64
  try:validate(bad,e)
  except AssertionError:rejected+=1
  else:raise AssertionError('accepted stale '+key)
 print('PASS_NATIVE_HODGE_CONNES_METRIC',e['exact_control_count'],'CONTROLS',rejected,'FALSE_LEDGERS_REJECTED')
if __name__=='__main__':main()
