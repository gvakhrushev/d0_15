#!/usr/bin/env python3
"""Independent A32 schedule/clock/count and rational price bounds audit."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
import itertools,json,sys
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round64';sys.path.insert(0,str(D/'round32'));import finite_book_comparison as a
planfile=D/'round32/FINITE_BOOK_COMPARISON_PLAN.json';plan=json.loads(planfile.read_text());base=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text());cert=json.loads((O/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json').read_text());nb=a.nb;ns=a.core.g.namespace();np=int(cert['rotations']['plus']['power_hex'],16);nm=int(cert['rotations']['minus']['power_hex'],16);assert np>1 and nm>1
# Independent paid alignment, all differences 0..100 and real exponent gap.
def independent(a0,b0):
 if a0>b0:
  z,y=independent(b0,a0);return y,z
 diff=b0-a0
 if diff==0:return 0,0
 if diff==1:return 5,4
 if diff==2:return 2,0
 if diff==3:return 5,2
 return diff,0
for x in range(101):
 for y in range(101):assert a.align(x,y)==independent(x,y)
pp,pm=independent(np,nm);assert np+pp==nm+pm==int(plan['same_pre_core_calls'])==int(plan['same_post_core_calls'])
# Verify actual identity padding on arbitrary columns and no protected wires.
aux,port,helper=2,2705,ns['layout']['qubits'];assert plan['padding_logical_WORK']==[aux,port,helper] and len({aux,port,helper})==3
pair=[(0,1),(0,1)];five=[(0,1),(1,2),(0,1),(1,2),(0,2)]
for seq in (pair,five):
 for x in range(8):
  y=x
  for i,j in seq:
   if y>>i&1:y^=1<<j
  assert y==x
for sign in ('plus','minus'):
 for j in (0,1,1344,2687):
  parts=a.endpoint_parts(sign,j);assert parts['last_g']=={'op':'G','wires':[4+j]}
  pre=nb.counts(parts['pre']);post=nb.counts(parts['post_before_final']);assert sum(pre.values())==sum(post.values())+1==np+pp
  for leaf in nb.leaves(parts['pre']):assert leaf['op'] in ('G','CX') and not set(leaf['wires']).intersection({0,1,3})
# Real late-stage iterator boundaries using a tiny injected source schedule;
# it exercises A32 itself, without materialising billions of births/gates.
oldbirth=a.core.b.birth_blocks;oldbefore=a.before_final_blocks
try:
 a.core.b.birth_blocks=lambda:[{'start':2705,'stop':2706,'role':'active_port_WORK'},{'start':2,'stop':3,'role':'fresh_aux_WORK'}]
 a.before_final_blocks=lambda sign,sam_index=0:iter([nb.gate('G',2705),nb.gate('CX',2705,2)])
 for sign in ('plus','minus'):
  x=list(a.execution_stages(sign,0,3));assert [v['kind'] for v in x]==['canonical_RAW_birth']*2+['square_unitary_edge']*2+['canonical_RAW_birth','square_unitary_edge']*3+['final_unitary_g']
  assert [x[k]['wire'] for k in (4,6,8)]==[2,3,4] and x[-1]['gate']=={'op':'G','wires':[2]}
finally:a.core.b.birth_blocks=oldbirth;a.before_final_blocks=oldbefore
# The tiny fixture above deliberately aliases old SAM to newly late wire 2;
# it checks iterator ordering only. Actual birth partition proves disjointness.
N=int(base['total_RAW_births']);L0=int(base['new_native_call_count']);L=L0+2*(np+pp);K=66076;layers=N+L+2*K;actual=plan['actual_native_counts_per_endpoint']
assert int(actual['G'])==int(base['new_native_counts']['G'])+np+nm+K
assert int(actual['CX'])==int(base['new_native_counts']['CX'])+pp+pm
assert L==int(plan['endpoint_calls_before_retention']) and layers==int(plan['actual_clock_layers_N']) and plan['total_canonical_RAW_births']==N+K
j=int(base['joint_RAW_source_checkpoint_native_prefix_calls']);assert N+np+pp+j==int(plan['common_original_RAW_source_checkpoint_clock_layer'])
assert plan['clock_dimension_over_initial_dimension']['Lbase_minus_3']==str(L-3) and plan['clock_dimension_over_initial_dimension']['K']==K
for n in range(1,9):
 for l in range(1,9):
  for k in range(0,7):
   total=sum(2**i for i in range(n))+(l-1)*2**n+sum(3*2**(n+i) for i in range(k))+2**(n+k)
   assert total==2**n*(l-3+4*2**k)-1
assert N+L<2**11647 and a.powers()==(np,nm)
# Independently reproduce exact Book H+J normalized sufficient bounds.
z=F(1,2**20);t=F(1,2**1618);delta=F(1,2**4852);gamma=F(8,3)*z*F(1,2**3158);d=1-z;B=64/d+192*z/d**2+128*z*z/d**3
fd=t*t*2**3158*B/16;angle=F(3,2)*2**3158*delta/(d*t);heat=F(6*(N+L),359)/(t*gamma)*F(1,2**(K//4));total=fd+angle+heat
assert fd+angle<F(1,2**74) and heat<F(1,2**76) and total<F(1,2**73) and 55*total<F(1,2**67)
def unpack(z):return F(int(z['numerator_hex'],16),int(z['denominator_hex'],16))
for name,value in [('fd_truncation',fd),('endpoint_angle_synthesis',angle),('all_mode_heat',heat),('one_SAM_row_total',total),('corrected_physical_raw_covector_total',55*total)]:assert unpack(plan['bounds'][name])==value
assert plan['initial_history']=={'H0':'C','Omega0':1,'P0':'I_1','previous_paid_stages':0,'old_return_Gram':'1','rank_P0':1,'Tr_old_Gram':1}
assert not plan['giant_word_clock_or_absolute_price_evaluated'] and not plan['physical_detector_or_seal_stages_added']
paths=[D/'round32/finite_book_comparison.py',planfile,D/'round30/COMMON_SOURCE_MARKED_PLAN.json',D/'round31/MEAN_GEOMETRY_LIFT_PLAN.json',O/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json']
for f,h in plan['source_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==h,f
out={'status':'PASS_INDEPENDENT_A32_FINITE_BOOK_COMPARISON','all_4_selected_SAM_indices_both_endpoints_checked':True,'initial_births':N,'late_retention_pairs':K,'matching_pre_post_and_checkpoint_ordinals':True,'identity_padding_all_eight_columns':True,'tiny_iterator_test_checks_order_only':True,'actual_last_g_physical':'G on 2+SAM index','late_clock_formula':'2^n*(Lbase-3+4*2^K)-1','exact_retained_G_count_and_all_mode_bounds_reproduced':True,'one_SAM_row_error_lt':'2^-73','corrected_2688_covector_error_lt':'2^-67','central_derivative':'analytic conjugation of A30 core; no compiled t=0 full padded history','full_physical_C_or_original_stationarity_proved':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'GR_closed':False}
(P/'A32_FINITE_COMPARISON_INDEPENDENT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'K':K,'early_births':N,'common_last_g':out['actual_last_g_physical']}))
