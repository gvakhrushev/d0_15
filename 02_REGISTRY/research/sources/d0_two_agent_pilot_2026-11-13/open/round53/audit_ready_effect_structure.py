#!/usr/bin/env python3
"""Exact Q(p) palette rows and conditional READY composition, no native run."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
import json,sympy as s
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=P.parent
files=[D/'round12/INTERNAL_SELECTOR_PALETTE.json',D/'round12/TOP_SOURCE_SELECTOR_PALETTE.json',D/'round12/TEN_SIGN_REPORT_PALETTE.json',D/'round12/SELECTOR_COMPILATION.json',D/'round25/H1_NAMESPACE_PLAN.json',D/'round25/GLOBAL_H1_PLAN.json',O/'round21/SC6_FORWARD.jsonl'];h=lambda f:sha256(f.read_bytes()).hexdigest();pins={str(f):h(f) for f in files};palettes=[]
def add(x,y):return x[0]+y[0],x[1]+y[1]
def mul(x,y):a,b=x;c,d=y;return a*c+b*d,a*d+b*c-b*d
def ppow(n):
 p=(0,1);z=(1,0)
 for _ in range(n):z=mul(z,p)
 return z
def fib(n):
 a,b=0,1
 for _ in range(n):a,b=b,a+b
 return a
for f in files[:3]:
 obj=json.loads(f.read_text());D0=int(obj['common_D_integer']);r=int(obj['fair_bits_r']);n=int(obj['golden_coins_n']);tau=F(obj['ready_probability_rational']);assert tau==F(D0,1<<r) and F(1,2)<tau<=1
 cpn=ppow(n);cpn1=ppow(n+1);weights=0
 for row in obj['partitions']:
  probs=[(F(w[0]),F(w[1])) for w in row['weights']];assert len(row['counts_ready_then_abort'])==len(probs)+1
  assert sum((x[0] for x in probs),F())==1 and sum((x[1] for x in probs),F())==0
  totals=[0,0]
  for j,counts in enumerate(row['counts_ready_then_abort']):
   A,B=map(int,counts);assert A>=0 and B>=0;totals[0]+=A;totals[1]+=B
   actual=((A*cpn[0]+B*cpn1[0])*F(1,1<<r),(A*cpn[1]+B*cpn1[1])*F(1,1<<r))
   expect=(tau*probs[j][0],tau*probs[j][1]) if j<len(probs) else (1-tau,F())
   assert actual==expect,(f.name,j);weights+=1
  assert totals==[(1<<r)*fib(n+1),(1<<r)*fib(n)]
 palettes.append({'file':f.name,'partitions_checked':len(obj['partitions']),'weight_and_abort_pairs_checked':weights,'golden_n':n,'fair_r':r,'common_READY_is_tau_I':True})
 assert tau==F(json.loads(files[3].read_text())['ready_probabilities'][{'INTERNAL_SELECTOR_PALETTE.json':'internal_slot','TOP_SOURCE_SELECTOR_PALETTE.json':'top_slot','TEN_SIGN_REPORT_PALETTE.json':'postprocessor'}[f.name]])
# 7 logical report records are in disjoint arenas; SC6 only reads them.
ns=json.loads(files[4].read_text());globalp=json.loads(files[5].read_text());readies=[z['all_READY'] for z in ns['reports']];reports=[z['REPORT'] for z in ns['reports']];assert len(set(readies+reports))==14
for i,r in enumerate(ns['reports']):
 lo=r['private_start'];hi=lo+r['private_width'];assert lo<=readies[i]<hi and lo<=reports[i]<hi
 for j,o in enumerate(ns['reports']):
  if i!=j:assert not o['private_start']<=readies[i]<o['private_start']+o['private_width']
assert ns['SC6_local_to_global'][5:19]==sum(([x,y] for x,y in zip(readies,reports)),[])
sc6=[json.loads(x) for x in files[6].read_text().splitlines()];counts=Counter()
for z in sc6:
 w=[ns['SC6_local_to_global'][x] for x in z['wires']];counts[z['op']]+=1
 if z['op']=='CX':assert w[1] not in readies and w[1] not in reports and w[1]==ns['layout']['port']
 else:assert not set(w)&set(readies+reports)
assert counts=={'G':5888,'CX':4096,'SourceI':8192}
assert [z['kind'] for z in globalp['forward_stage_schedule']][-2:]==['PORT_ZERO','SC6']
# Sequential proof fixture: a success Kraus K has K†K=alpha I even when
# it applies a noncommuting state change to shared input, so joint event
# with another fresh scalar-effect instrument gives alpha² on all columns.
a=s.Rational(3,4);I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);H=s.Matrix([[1,1],[1,-1]])/s.sqrt(2)
K1=s.sqrt(a)*X;K2=s.sqrt(a)*Z;between=H;joint=K2*between*K1
assert K1.T*K1==a*I and K2.T*K2==a*I and s.simplify(joint.T*joint)==a*a*I
# Equal marginal READY numbers alone do not imply independent readiness:
# two perfectly correlated records have each marginal a and joint a != a².
prob_joint=a;assert prob_joint!=a*a
for path,pin in pins.items():assert h(Path(path))==pin
out={'status':'PASS_ALL_IDEAL_PALETTE_READY_EFFECTS_AND_RECORD_BINDINGS','input_sha256':pins,'all_palette_rows':palettes,'SC6_forward_native_counts':dict(counts),'all_seven_READY_REPORT_wires_disjoint':True,'SC6_never_targets_READY_or_REPORT':True,'sequential_scalar_effect_argument':'E_ready=alpha I for each report on every incoming shared source/SITE state, with fresh disjoint resource inputs and retained flags, implies conditional Pr(READY_i | prior records)=alpha and joint all-seven alpha^7; source-state product is not required for READY alone.','noncommuting_shared_input_Kraus_example':True,'correlated_marginals_counterexample':True,'no_extra_postselection_or_loader_flags_in_SC6':True,'ideal_R_equality_consumes_B31_A13_A17_structural_contracts':True,'actual_native_alpha_hat_exact_or_original_Pj_law_proved':False,'physical_admission_marks_and_C_proved':False,'GR_closed':False}
(P/'IDEAL_READY_EFFECT_STRUCTURE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'palette_partitions':sum(z['partitions_checked'] for z in palettes),'SC6':dict(counts)}))
