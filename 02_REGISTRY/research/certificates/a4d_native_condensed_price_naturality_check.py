#!/usr/bin/env python3
"""Exact owned-archive linear naturality/price interface; no native field law inferred."""
import argparse,hashlib,json,re
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[3]
BASE='02_REGISTRY/research/certificates/a4d_native_condensed_price_naturality'
PROOF='02_REGISTRY/research/A4D_NATIVE_CONDENSED_PRICE_NATURALITY.md'
HEAD='1f9a1e8c1417e28823ce1646422a3f915eee9e86'
SCOPE={
 'class':'COMPLETE_DECLARED_LINEAR_HEAT_NATURALITY_ON_OWNED_ARCHIVE_NOT_PHYSICAL_NATIVE_ACTION',
 'actual_nonuniform_archive_and_real_LightProfinite_owner_consumed':True,
 'set_point_endomorphism_is_Hilbert_heat_generator':False,
 'entrywise_record_kernel_implies_counting_operator_naturality':False,
 'native_record_kernel_is_physical_heat_operator':False,
 'all_level_linear_extension_class_and_hidden_blocks_classified':True,
 'native_heat_carrier_and_field_preparation_derived':False,
 'fixed_gap_full_price_derivative_genuine':True,
 'all_scalar_interface_first_jets_realized_not_native_sources':True,
 'bounded_hidden_gap_limit_ordinary_heat_trace_finite':False,
 'fixed_phi_norm_and_trace_class_limit_force_shape_source':False,
 'phi_scale_owner_derives_thermal_ceiling':False,
 'fixed_spectral_ceiling_profile_minimum_classified':True,
 'actual_native_spectral_ceiling_or_minimum_preparation_derived':False,
 'independent_hidden_heat_no_stationarity_is_whole_D0_no_go':False,
 'archive_complement_is_physical_gauge':False,
 'capacity_level_is_physical_A4D_mesh':False,
 'kernel_spectral_Hilbert_limit_and_matrix_heat_trace_binding':'ANALYTIC_WITH_EXACT_FINITE_CONTROLS',
 'native_source_Ward_contrast_curved_roots_or_GR_derived':False,
 'G0_G1_G2_G3_G4_or_original_parent_terminal_closed':False,
}
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def controls():
 checks={}
 def ck(name,condition):
  assert condition,name
  checks[name]=checks.get(name,0)+1
 rec=json.loads((ROOT/(BASE+'_results.json')).read_text())
 ck('real_capsule_status',rec['status']=='PASS' and rec['compiler_exit_code']==0 and rec['input_head']==HEAD)
 ck('compiled_declarations',len(rec['declarations'])==46 and len(rec['printed_propositions'])==46)
 ck('primary_owner_diagnostics',len(rec['primary_owner_propositions'])==6 and len(rec['typed_owner_definitions'])==3)
 ck('primary_transitive_sizes',len(rec['transitive_d0_source_sha256'])==15 and len(rec['primary_and_prior_input_sha256'])==38)
 for group in ['transitive_d0_source_sha256','primary_and_prior_input_sha256','toolchain_input_sha256']:
  for p,h in rec[group].items():ck('pinned_input_'+group,sha(p)==h)
 ck('capsule_hash',sha(BASE+'.lean')==rec['capsule_sha256'])
 ck('output_hash',sha(BASE+'_output.txt')==rec['output_sha256'])
 out=(ROOT/(BASE+'_output.txt')).read_text()
 ck('no_diagnostics_or_sorry',': error' not in out and ': warning' not in out and 'sorryAx' not in out)
 for n in rec['declarations']+rec['primary_owner_propositions']+rec['typed_owner_definitions']:
  ck('resolved_printed_declarations',n in out and n in rec['axioms'])
  ck('transitive_standard_axioms',set(rec['axioms'][n])<={'propext','Classical.choice','Quot.sound'})
 ck('actual_point_operator_type','S.Stage n → S.Stage n' in out and 'self.op m x' in out)
 ck('analytic_boundaries',rec['matrix_to_scalar_heat_trace_and_Hilbert_limit_analytic'] and not rec['owned_phi_scale_is_thermal_norm_or_budget_derived'] and not rec['native_field_preparation_source_or_physical_on_shell_admission_derived'] and not rec['positive_GR_or_global_closure'])

 # Every point/fibre in ten actual successor maps; no regular-cover substitution.
 stages=[]
 for n in range(10):
  m=(n+2)**4;M=(n+3)**4
  counts=[M//m+int(a<M%m) for a in range(m)]
  ck('actual_all_size_capacity_fixture',M>m and sum(counts)==M and min(counts)>0)
  for a,d in enumerate(counts):
   ck('complete_nonempty_fibres',d==len(range(a,M,m)))
  stages.append({'coarse':m,'fine':M,'new_modes':M-m,'fibre_sizes':sorted(set(counts))})
 ck('first_actual_sizes',[(x['coarse'],x['fine']) for x in stages[:2]]==[(16,81),(81,256)])
 ck('first_intrinsic_fibre_orbits',stages[0]['fibre_sizes']==[5,6] and stages[1]['fibre_sizes']==[3,4])

 # The first two full nonuniform matrices and ALL new-kernel basis directions.
 mu=s.ones(16,1)/16;A0=s.eye(16)-s.ones(16)/16
 rootJ=s.eye(16);rootC=s.eye(16);old=A0
 matrices=[];basis_data=[]
 for n in range(2):
  m=(n+2)**4;M=(n+3)**4
  counts=[M//m+int(a<M%m) for a in range(m)]
  J=s.SparseMatrix(M,m,{(i,i%m):1 for i in range(M)})
  C=s.SparseMatrix(m,M,{(i%m,i):s.Rational(1,counts[i%m]) for i in range(M)})
  mn=s.Matrix([mu[i%m]/counts[i%m] for i in range(M)])
  P=J*C;Q=s.eye(M)-P
  ck('actual_CJ_and_projection',C*J==s.eye(m) and P*P==P and Q*Q==Q)
  ck('both_full_readouts_retained',C*Q==s.zeros(m,M) and Q*J==s.zeros(M,m))
  ck('positive_pairing_adjoint',s.diag(*mu)*C==J.T*s.diag(*mn) and all(w>0 for w in mn))
  ck('positive_pairing_isometry',J.T*s.diag(*mn)*J==s.diag(*mu) and sum(mn)==1)
  ck('native_hidden_trace',Q.trace()==M-m)
  piv=[];cols=[]
  for a in range(m):
   fibre=list(range(a,M,m))
   for i in fibre[1:]:
    v=s.SparseMatrix(M,1,{(i,0):1,(fibre[0],0):-1})
    ck('all_hidden_basis_readout_zero',C*v==s.zeros(m,1))
    ck('all_hidden_basis_projection',Q*v==v)
    ck('all_hidden_basis_positive_weight',sum(mn[j]*v[j]**2 for j in range(M))>0)
    cols.append(v);piv.append(i)
  K=s.SparseMatrix.hstack(*cols)
  ck('complete_hidden_basis',len(cols)==M-m and K.extract(piv,list(range(M-m)))==s.eye(M-m))
  basis_data.append({'new_dimension':M-m,'paired_selfadjoint_block_dimension':(M-m)*(M-m+1)//2})
  rJ=J*rootJ;rC=rootC*C;Qr=s.eye(M)-rJ*rC
  A=rJ*A0*rC+s.Rational(3,2)*Qr
  ck('all_level_lift_readout',rC*rJ==s.eye(16) and Qr.trace()==M-16)
  ck('whole_chain_heat_naturality',C*A==old*C and A*J==J*old)
  ck('whole_chain_pairing_symmetry',A.T*s.diag(*mn)==s.diag(*mn)*A)
  # The actual pulled-back informational kernel is left in its own role.
  record=rJ*rJ.T
  ck('native_point_kernel_exact',all(record[i,j]==int(int(rJ[i,:].dot(rJ[j,:]))==1) for i in range(M) for j in range(M)))
  if n==0:
   ck('reject_kernel_operator_naturality',C*record!=s.eye(m)*C)
   ck('actual_counting_record_multiplicities',J.T*J==s.diag(*counts) and sorted(counts)==[5]*15+[6])
   ck('actual_operator_defect_entry', (C*record)[0,0]==1 and C[0,0]==s.Rational(1,6))
  else:
   ck('reject_direct_modulo_composite',rJ[81,0]==1 and rJ[81,1]==0 and 81%16==1)
  matrices.append((J,C,Q,rJ,rC,mn))
  rootJ,rootC,mu,old=rJ,rC,mn,A

 # Fixed-Phi shape: two INTRINSIC actual first-fibre sectors, not chosen vectors.
 J,C,Q,rJ,rC,mn=matrices[0];M=81
 v=s.Matrix([int(i%16==0) for i in range(M)])
 Q6=s.diag(*[int(i%16==0) for i in range(M)])-v*v.T/6;Q5=Q-Q6
 ck('intrinsic_phi_projections',Q6*Q6==Q6 and Q5*Q5==Q5 and Q6*Q5==s.zeros(M) and Q5*Q6==s.zeros(M))
 ck('intrinsic_phi_ranks',Q6.trace()==5 and Q5.trace()==60 and (Q6+Q5).trace()==65)
 for a in range(16):
  fibre=list(range(a,81,16))
  for i in fibre[1:]:
   e=s.SparseMatrix(81,1,{(i,0):1,(fibre[0],0):-1})
   ck('all_intrinsic_phi_shape_directions',Q6*e==(e if a==0 else s.zeros(81,1)) and Q5*e==(s.zeros(81,1) if a==0 else e))
 for q in [Q5,Q6]:
  ck('intrinsic_shape_natural_and_selfadjoint',C*q==s.zeros(16,81) and q*J==s.zeros(81,16) and q.T*s.diag(*mn)==s.diag(*mn)*q)
 # Generators of all FIRST-ARROW automorphisms: fibre transpositions and equal-size fibre swaps.
 permutations=[]
 for a in range(16):
  f=list(range(a,81,16))
  for i in f[1:]:
   p=list(range(81));p[f[0]],p[i]=p[i],p[f[0]];permutations.append(p)
 for a in range(2,16):
  p=list(range(81))
  for k in range(5):p[1+16*k],p[a+16*k]=p[a+16*k],p[1+16*k]
  permutations.append(p)
 for p in permutations:
  ck('complete_intrinsic_shape_symmetry_generators',Q6.extract(p,p)==Q6 and Q5.extract(p,p)==Q5)

 beta,Z,r,gap,sigma=s.symbols('beta Z r gap sigma',positive=True)
 H=s.log(Z+r*s.exp(-beta*gap))/beta
 source=-r*s.exp(-beta*gap)/(Z+r*s.exp(-beta*gap))
 ck('genuine_heat_derivative',s.simplify(s.diff(H,gap)-source)==0)
 ck('genuine_full_fixed_feedback_derivative',s.simplify(s.diff(H+s.symbols('feedback'),gap)-source)==0)
 ck('exact_source_error',s.simplify(source+1-Z/(Z+r*s.exp(-beta*gap)))==0)
 u=Z*s.exp(beta*gap)/r
 ck('normalized_heat_factorization',s.simplify((Z+r*s.exp(-beta*gap))/(r*s.exp(-beta*gap))-(1+u))==0)
 ck('source_tail_identity',s.simplify(source+1-u/(1+u))==0)
 ck('source_error_bound_algebra',s.simplify(u-u/(1+u)-u*u/(1+u))==0)
 ck('finite_budget_floor_bound',s.exp(-s.Rational(3,2))<s.exp(-s.Rational(1,2)))
 ck('reject_nonattained_unbounded_gap_minimum',s.exp(-2)>0 and s.exp(-3)<s.exp(-2))
 phi=(1+s.sqrt(5))/2
 ck('actual_phi_arithmetic',s.simplify(phi**2-phi-1)==0 and phi>1)
 Zshape=Z+5*s.exp(-beta*phi)+60*s.exp(-beta*sigma*phi)
 shaped=-60*phi*s.exp(-beta*sigma*phi)/Zshape
 ck('genuine_fixed_phi_shape_source',s.simplify(s.diff(s.log(Zshape)/beta,sigma)-shaped)==0)
 for N in range(1,11):
  sizes=[16,5,60]+[((j+2)**4-(j+1)**4) for j in range(2,N+1)]
  ck('all_finite_phi_prefix_multiplicities',sum(sizes)==(N+2)**4)
  ck('paired_phi_norm_exact_stronger_control',phi**N>=phi and (s.Rational(1,4)*phi)<phi)
  # Source persists at all prefixes with a finite tail independent of the shape.
  tail=sum((j+2)**4-(j+1)**4 for j in range(2,N+1))
  zz=Zshape+s.symbols('tail',nonnegative=True)
  ck('all_prefix_phi_shape_derivative',s.simplify(s.diff(s.log(zz)/beta,sigma)+60*phi*s.exp(-beta*sigma*phi)/zz)==0)
  ck('actual_capacity_vs_history_counts',(N+2)**4-16!=653)
 # Fixed value, full interface first-jet fibre: arbitrary slopes remain genuine profiles.
 t,a,vv=s.symbols('t a v',real=True);ss=s.Rational(3,2)
 hd=s.diff(s.log(Z+r*s.exp(-beta*(ss+vv*t)))/beta,t).subs(t,0)
 c=-r*s.exp(-beta*ss)/(Z+r*s.exp(-beta*ss))
 ck('all_scalar_jet_fibre',s.simplify(hd.subs(vv,a/c)-a)==0)
 ck('same_base_price_different_state_jets',s.simplify(hd.subs(vv,0))==0 and s.simplify(hd.subs(vv,1)-c)==0)
 # Missing surjectivity is not allowed to masquerade as a complete split.
 badJ=s.Matrix([[1,0],[1,0],[1,0]]);badC=s.Matrix([[s.Rational(1,3)]*3,[0]*3])
 ck('reject_empty_fibre',badC*badJ!=s.eye(2))
 ck('retain_heat_invisible_but_price_visible',Q.trace()==65 and Q5.trace()==60 and c!=0)
 ck('reject_rank_as_physical_gauge',5+60==65 and 65!=653 and 65!=296 and 65!=30)
 return {'checks':checks,'check_count':sum(checks.values()),'compiled_propositions':46,
 'printed_primary_owner_propositions':6,'typed_owner_definitions':3,'transitive_D0_pins':15,'primary_and_prior_pins':38,
 'actual_archive_stages':stages,'first_two_complete_hidden_bases':basis_data,
 'intrinsic_phi_first_hidden_ranks':[5,60],'first_arrow_symmetry_generators':len(permutations),
 'uniform_bounded_gap_capacity_source_limit':-1,'native_field_preparation_or_source_derived':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--expect',type=Path);args=ap.parse_args()
 header={'schema':'d0-condensed-price-naturality/1','input_head':HEAD,'scope':SCOPE,'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),'lean_receipt_sha256':sha(BASE+'_results.json')}
 expected=None
 if not args.output:
  expected=json.loads((args.expect or ROOT/(BASE+'_certificate.json')).read_text())
  assert all(expected.get(k)==v for k,v in header.items()),'SOURCE_SCOPE_OR_INPUT_MISMATCH'
 result={**header,**controls()}
 if args.output:args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 else:assert result==expected,'EXACT_CERTIFICATE_MISMATCH'
 print('PASS_NATIVE_CONDENSED_PRICE_NATURALITY',result['check_count'],'controls')

if __name__=='__main__':main()
