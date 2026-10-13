#!/usr/bin/env python3
"""Exact ordered native Jones transport, full complement and record controls."""
# D0_CI_TIMEOUT_SECONDS=600
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
BASE='02_REGISTRY/research/certificates/a4d_native_jones_record_transport'
PREV='02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation'
PROOF='02_REGISTRY/research/A4D_NATIVE_JONES_RECORD_TRANSPORT.md'
HEAD='01e8047b1effacdbf623ec3189bedb63fb6732f8'
INPUTS=[
 '02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md',
 *[PREV+x for x in ('.py','_check.py','_certificate.json','.lean','_results.json','_output.txt')],
 '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md',
 '02_REGISTRY/research/certificates/a4d_native_golden_cost_refinement_certificate.json',
 '02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md',
 '02_REGISTRY/research/certificates/a4d_native_af_trace_preparation_certificate.json',
 '03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean',
 '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
 '03_FORMALIZATION/D0/Algebra/FibonacciAFTower.lean',
 '03_FORMALIZATION/D0/VNext/PerronGNSTower.lean',
]

spec=importlib.util.spec_from_file_location('native_jones_transport',ROOT/(BASE+'.py'))
N=importlib.util.module_from_spec(spec);sys.modules[spec.name]=N;spec.loader.exec_module(N)
E=N.E;s=E.s;a,p,z=E.a,E.p,E.z
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def inclusion(blocks,r):
 for _ in range(r):blocks=N.include(blocks)
 return blocks


def controls():
 checks=[];mutants=[]
 def check(name,value):
  assert bool(value),name
  checks.append(name)
 def equal(name,value):check(name,E.zero(value))
 def reject(name,false_claim):
  check('REJECT_'+name,not false_claim);mutants.append(name)
 def positive(name,value):
  value=s.simplify(E.red(value).subs(p,(s.sqrt(5)-1)/2).subs(a,s.sqrt((s.sqrt(5)-1)/2)))
  check(name,value.is_positive is True)
 def rational_equal(name,value):equal(name,s.fraction(s.cancel(value))[0])

 c=p**3;c0=p**6;ss=2*a*p
 equal('golden_double_angle',p-p*p-c)
 equal('golden_angle_unitarity',c*c+ss*ss-1)
 equal('correct_residual_inverse',a*(p+2)*ss/2-1)
 reject('SKEW_COEFFICIENT_IS_RESIDUAL_INVERSE',E.zero(a*(3*p+5)*ss/2-1))
 equal('polynomial_Q_inverse',(2*p+3)*(1-c0)/4-1)
 positive('positive_residual_scale',ss)
 positive('corner_below_one_half',s.Rational(1,2)-c0)

 # Bind to the previous full right-module frame using its independent row /
 # reversed-column path permutation, not the new palindromic constructor.
 for n in range(3):
  sizes=E.counts(n);rows=E.segments(*sizes,3);actual=N.corner_frames(n)
  for part,J in zip(E.right_frames(n),actual):
   j=part['old_type'];dj=part['spectator_dimension']
   native=E.segments(*sizes,6)[j]
   index={(kind,path,r):offset+r for kind,path,offset in native for r in range(sizes[kind])}
   reconstructed=s.zeros(J.rows,J.cols)
   for oldrow,(v,k,row) in enumerate(part['labels']):
    coltype,colpath,offset=rows[v][k]
    kind,rowpath,ro=next(t for t in rows[v] if t[2]<=row<t[2]+sizes[t[0]])
    path=rowpath+tuple(reversed(((j,)+colpath)[:-1]))
    newrow=index[(kind,path,row-ro)]
    for column in range(dj):
     reconstructed[newrow,column]=part['V'][oldrow,column]
   equal('all_entries_previous_native_frame_binding',J-reconstructed)
  Gs,Fs=N.adjacent_frames(n)
  for G,F in zip(Gs,Fs):
   equal('all_columns_adjacent_G_normalized',G.T*G-s.eye(G.cols))
   equal('all_columns_adjacent_F_normalized',F.T*F-s.eye(F.cols))
   equal('all_columns_adjacent_exact_overlap',F.T*G-c*s.eye(G.cols))
   for k in range(G.cols):
    for l in range(F.cols):
     support=[r for r in range(G.rows) if G[r,k]!=0 and F[r,l]!=0]
     check('unique_common_native_path_per_equal_column',len(support)==int(k==l))
     if support:equal('common_path_coefficient_product',G[support[0],k]*F[support[0],l]-c)

 for n in range(2):
  ops=N.operators(n);old_sizes=E.counts(n);new_sizes=E.counts(n+7)
  for data in ops:
   G,F,Z,e,f,Q,H,R=(data[k] for k in ('G','F','Z','e','f','Q','H','R'))
   I=s.eye(G.rows);Ir=s.eye(G.cols)
   equal('residual_whole_Gram',Z.T*Z-Ir)
   equal('residual_orthogonal_to_old_frame',G.T*Z)
   equal('full_Q_is_frame_projection',Q-G*G.T-Z*Z.T)
   equal('adjacent_Jones_sandwich',e*f*e-c0*e)
   equal('reverse_Jones_sandwich',f*e*f-c0*f)
   equal('owned_gate_on_G',H*G-a*G-p*Z)
   equal('owned_gate_on_Z',H*Z+p*G-a*Z)
   equal('whole_gate_orthogonal',H.T*H-I)
   equal('whole_gate_coorthogonal',H*H.T-I)
   equal('whole_gate_square_is_transport',H*H-R)
   equal('transport_all_frame_columns',R*G-F)
   equal('transport_full_corner',R*e*R.T-f)
   equal('transport_whole_complement',R*(I-e)*R.T-(I-f))
   equal('untouched_full_orthogonal_complement',H*(I-Q)-(I-Q))
   reject('DELETE_FULL_ORTHOGONAL_COMPLEMENT_n%d_D%d'%(n,G.rows),E.zero(I-Q))
   # All matrix outcomes, including the coherences; no diagonal-only test.
   for row in range(G.cols):
    for col in range(G.cols):
     X=s.zeros(G.cols);X[row,col]=1
     equal('all_corner_matrix_units_transport',R*(G*X*G.T)*R.T-F*X*F.T)
   equal('full_one_tick_feedback',e-e*H.T*e*H*e-p*p*e)
   equal('full_two_tick_feedback',e-e*R.T*e*R*e-(1-c0)*e)
   swap=E.mat(I-e-Z*Z.T+Z*G.T+G*Z.T)
   equal('internal_swap_whole_unitarity',swap.T*swap-I)
   equal('internal_swap_orthogonal_support',e*swap*e)
   equal('internal_swap_transports_support',swap*e*swap.T-Z*Z.T)
  for j,dj in enumerate(old_sizes):
   for row in range(dj):
    for col in range(dj):
     X=[s.zeros(t) for t in old_sizes];X[j][row,col]=1
     fine=inclusion(X,7)
     for data,x in zip(ops,fine):
      equal('every_old_matrix_unit_commutes_with_H',data['H']*x-x*data['H'])
  es=[d['e'] for d in ops];fs=[d['f'] for d in ops]
  equal('trace_corners',N.native_trace(n+7,es)-c0)
  equal('trace_preparation_overlap',N.native_trace(n+7,[e*f for e,f in zip(es,fs)])-p**12)
  equal('constant_unrotated_refinement_defect',N.native_trace(n+7,[(e-f)**2 for e,f in zip(es,fs)])-8*p**9)
  equal('noncommuting_Jones_trace_norm',N.native_trace(n+7,[(e*f-f*e).T*(e*f-f*e) for e,f in zip(es,fs)])-2*p**12*(1-c0))
  equal('whole_rotating_plane_trace',N.native_trace(n+7,[d['Q'] for d in ops])-2*c0)

 reject('ORDINARY_INCLUSION_ALREADY_COHERENT',E.zero(8*p**9))
 ops=N.operators(0);b=inclusion([s.eye(2),s.zeros(1)],6)
 expected=[(s.diag(p,1),s.diag(1-p/4,1),s.eye(2)),(s.Matrix([[p]]),s.Matrix([[s.Rational(1,4)]]),s.zeros(1))]
 for d,x,want in zip(ops,b,expected):
  for V,y in zip((d['G'],d['H']*d['G'],d['F']),want):
   equal('all_native_new_observable_columns',V.T*x*V-y)
  equal('unprepared_full_trace_invariance',s.trace(d['H'].T*x*d['H'])-s.trace(x))
 comm=E.mat(ops[1]['H']*b[1]-b[1]*ops[1]['H'])
 equal('new_observable_commutator_witness',comm[0,2]-(1-a*p*p)/4)
 reject('TRANSPORT_FIXES_ALL_NEW_NATIVE_OBSERVABLES',E.zero(comm))
 for key in ('e','half','f'):
  corners=[d['H']*d['e']*d['H'].T if key=='half' else d[key] for d in ops]
  equal('complete_corner_tracial_b_cancellation',N.native_trace(7,[e*x for e,x in zip(corners,b)])-c0*2*p*p)
 # Conditioned old-type-0 central label, with both final native blocks kept.
 initial=s.Matrix([[p*p,p**3],[p**3,p**4]])
 final=s.diag(p,p*p)
 oldtype=inclusion([s.eye(1),s.zeros(1)],7)
 prepared=[E.mat(d['e']*x) for d,x in zip(ops,oldtype)]
 equal('central_record_actual_preparation_weight',N.native_trace(7,prepared)-p**7)
 after=[E.mat(d['R']*x*d['R'].T) for d,x in zip(ops,prepared)]
 for states,table in ((prepared,initial),(after,final)):
  for j,(state,observable) in enumerate(zip(states,b)):
   for k,outcome in enumerate((observable,s.eye(observable.rows)-observable)):
    equal('central_record_actual_native_joint_table',p**(8+j)*s.trace(state*outcome)-p**7*table[j,k])
 equal('central_record_initial_independence',initial-s.Matrix([p,p*p])*s.Matrix([[p,p*p]]))
 equal('central_record_final_preserves_block_marginal',final*s.ones(2,1)-initial*s.ones(2,1))
 check('central_record_final_mismatch_zero',final[0,1]+final[1,0]==0)
 reject('PREPARED_CENTRAL_RECORD_ALREADY_PRESENT',E.zero(initial[0,1]+initial[1,0]))
 apparatus=s.Matrix([a,p])
 records=[]
 for spectator in (s.Matrix([1,0]),s.Matrix([0,1])):
  vector=s.kronecker_product(apparatus,spectator);density=vector*vector.T
  records.append(s.Matrix(2,2,lambda i,j:sum(density[2*i+k,2*j+k] for k in range(2))))
 equal('plane_apparatus_independent_of_spectator',records[0]-records[1])
 reject('FIXED_PLANE_APPARATUS_DISTINGUISHES_SPECTATOR',not E.zero(records[0]-records[1]))

 # Exercise public refinement and the full residual API on off-diagonal data.
 A,B=E.counts(6)
 X=[s.zeros(A),s.zeros(B)];Y=[s.zeros(A),s.zeros(B)]
 X[0][0,1]=1;X[1][0,0]=2;Y[0][1,0]=3;Y[1][0,0]=1
 lifted=N.transport(0,X)
 for recovered,x in zip(N.coarse(0,lifted),X):equal('public_coarse_left_inverse',recovered-x)
 for lhs,rhs in zip(N.transport(0,[x*y for x,y in zip(X,Y)]),[x*y for x,y in zip(lifted,N.transport(0,Y))]):equal('public_refinement_multiplication',lhs-rhs)
 for lhs,rhs in zip(N.transport(0,[x.T for x in X]),lifted):equal('public_refinement_star',lhs-rhs.T)
 equal('public_refinement_trace',N.native_trace(7,lifted)-N.native_trace(6,X))
 for lhs,rhs in zip(N.transport(0,[s.eye(A),s.eye(B)]),[s.eye(t) for t in E.counts(7)]):equal('public_refinement_unital',lhs-rhs)
 corners=[J*J.T for J in N.corner_frames(0)]
 for lhs,d in zip(N.transport(0,corners),ops):equal('public_actual_corner_refinement',lhs-d['f'])
 equal('public_conditioned_refinement',N.native_trace(7,[d['f']*x for d,x in zip(ops,lifted)])-N.native_trace(6,[e*x for e,x in zip(corners,X)]))
 raw=[s.zeros(t) for t in E.counts(7)];raw[0][0,A]=1;raw[0][A,0]=2;raw[1][0,1]=3
 fine=[E.mat(d['R']*x*d['R'].T) for d,x in zip(ops,raw)]
 coarse,residual=N.decompose(0,fine);reconstructed=N.transport(0,coarse)
 for y,x,r in zip(fine,reconstructed,residual):equal('whole_fine_residual_reconstruction',y-x-r)
 for x in N.coarse(0,residual):equal('residual_trace_orthogonal_to_whole_range',x)
 equal('full_Pythagorean_norm',N.native_trace(7,[y.T*y for y in fine])-N.native_trace(6,[x.T*x for x in coarse])-N.native_trace(7,[r.T*r for r in residual]))
 reject('RESIDUAL_IS_GAUGE_OR_ZERO',all(E.zero(r) for r in residual))

 for n in range(9):
  sizes=E.counts(n+7);ranks=E.counts(n+1);weights=[p**(n+8+j) for j in range(2)]
  dimension=sum(D*D for D in sizes);rank=sum(D*r for D,r in zip(sizes,ranks))
  check('whole_regular_feedback_multiplicity',rank==sum(t*t for t in E.counts(n+4)))
  check('whole_regular_unit_factors_retained',dimension>rank)
  equal('both_marginal_corner_weight',sum(w*r for w,r in zip(weights,ranks))-c0)
  positive('correlation_EF_positive_rank',sum(r*r for r in ranks))
  positive('correlation_mismatch_positive_rank',sum(r*(D-r) for r,D in zip(ranks,sizes)))
  tstar=sum(w*s.Rational(r*r,D) for w,r,D in zip(weights,ranks,sizes))
  positive('faithful_full_state_positive_joint',tstar)
  positive('faithful_full_state_positive_mismatch',c0-tstar)
  equal('faithful_full_state_trace_one',sum(w*D for w,D in zip(weights,sizes))-1)
  if n<3:
   DX,DY=sizes;rx,ry=ranks;wx,wy=weights;u=wx*DX;v=wy*DY
   gammaX=(u-u*v*v)/(DX*DX-1);gammaY=(v-u*u*v)/(DY*DY-1)
   equal('protected_family_full_R_trace',u*v+gammaX*(DX*DX-1)+gammaY*(DY*DY-1)-1)
   equal('protected_family_both_X_marginals',u*v*v/DX+gammaX*(DX-s.Rational(1,DX))-wx)
   equal('protected_family_both_Y_marginals',u*u*v/DY+gammaY*(DY-s.Rational(1,DY))-wy)
   mismatch=gammaX*rx*(DX-rx)+gammaY*ry*(DY-ry)
   positive('protected_family_internal_mismatch_positive',mismatch)
   positive('protected_family_internal_joint_positive',c0-mismatch)
 reject('WORKING_RANK_IS_REGULAR_RANK',sum(E.counts(1))==sum(t*t for t in E.counts(4)))
 reject('BOTH_MARGINALS_FORCE_PERFECT_RECORD',E.zero(c0))
 reject('PURE_CORRELATED_STATE_IS_FULL_FAITHFUL',1==sum(t*t for t in E.counts(7)))
 t,cc,tt,eps,MM,beta,lam=s.symbols('t cc tt eps MM beta lam',positive=True)
 q=(t-eps*tt)/(1-eps)
 rational_equal('faithful_mixture_exact_target',eps*tt+(1-eps)*q-t)
 Bprice=-s.log(1-(cc-t)/MM)/beta
 rational_equal('internal_correlation_heat_derivative',s.diff(Bprice,t)+1/(beta*(t-cc+MM)))
 rational_equal('thermal_chain_rule_matches_old_family',s.diff(Bprice,t).subs(t,cc-(1-lam)*MM)+1/(beta*MM*lam))

 previous=json.loads((ROOT/(PREV+'_certificate.json')).read_text())
 for field,path in [('checker_sha256',PREV+'_check.py'),('proof_sha256',INPUTS[0]),('program_sha256',PREV+'.py'),('Lean_receipt_sha256',PREV+'_results.json')]:check('previous_packet_freshness',previous[field]==sha(path))
 for path,digest in previous['input_sha256'].items():check('previous_transitive_input',sha(path)==digest)
 receipt=json.loads((ROOT/(BASE+'_results.json')).read_text())
 check('Lean_compiler_success',receipt['status']=='PASS' and receipt['compiler_exit_code']==0)
 check('Lean_capsule_freshness',receipt['capsule_sha256']==sha(BASE+'.lean'))
 check('Lean_output_freshness',receipt['output_sha256']==sha(BASE+'_output.txt'))
 for path,digest in receipt['input_sha256'].items():check('Lean_transitive_input',sha(path)==digest)
 check('Lean_standard_axioms_only',all(set(xs)<={'propext','Classical.choice','Quot.sound'} for xs in receipt['axioms'].values()))
 return {'status':'PASS','input_source_head':HEAD,'proof':PROOF,
 'scope':{'native_path_overlap':'ANALYTIC_ALL_N_EXACT_ORDERED_MATRIX_BINDING',
 'constructed_composite_refinement':'Ad_R_AFTER_ACTUAL_INCLUSION',
 'owned_gate':'GoldenOrderInterferometer.gate','all_orthogonal_complements_retained':True,
 'specific_central_label_record':True,'arbitrary_spectator_record_in_plane_apparatus':False,
 'physical_execution_or_clock_or_preparation_law_derived':False,
 'metric_link_source_Ward_stationarity_or_GR_derived':False,'parent_terminal_closed':False},
 'exact_controls':len(checks),'checks':dict(sorted(Counter(checks).items())),
 'executed_mathematical_mutants':mutants,'explicit_adjacent_frame_levels':[0,1,2],
 'full_native_operator_levels':[0,1],'new_Lean_declarations':19,
 'unrotated_corner_defect_squared':'8*p^9','regular_feedback_exponent':'d_(n+4)',
 'full_two_marginal_correlation_range':'[0,p^6]; faithful: (0,p^6)',
 'input_sha256':{path:sha(path) for path in INPUTS},
 'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
 'program_sha256':sha(BASE+'.py'),'Lean_receipt_sha256':sha(BASE+'_results.json')}


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 result=controls();target=ROOT/(BASE+'_certificate.json')
 if args.write:target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 else:assert json.loads(target.read_text())==result,'JONES_RECORD_TRANSPORT_IMMUTABLE_LEDGER_MISMATCH'
 print('PASS_NATIVE_JONES_RECORD_TRANSPORT controls=%d mutants=%d physical_preparation=OPEN'%(result['exact_controls'],len(result['executed_mathematical_mutants'])))


if __name__=='__main__':main()
