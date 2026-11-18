#!/usr/bin/env python3
"""Independent small actual path sums and actual star algorithm, not production."""
from pathlib import Path
from hashlib import sha256
import sys,json,mpmath as mp
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round49');sys.path.insert(0,str(D));import finite_actual_target as f
nb=f.a41.e;iv=f.e.Dyadic(512);sam=(4,0,2)
def general():
 yield {'op':'repeat','count':'0x2','child':{'op':'G','wires':[1]}}
 yield {'op':'CX','wires':[4,1]}
 yield {'op':'G','wires':[3]}
 yield {'op':'CX','wires':[3,1]}
 yield {'op':'CX','wires':[0,3]}
 yield {'op':'G','wires':[1]}
def positive():
 yield {'op':'CX','wires':[4,1]}
 yield {'op':'CX','wires':[0,3]}
for factory in (general,positive):
 core=f.ActualDiagonal(5,sam,factory,path_limit=256)
 for label in range(8):
  target=core.entry(label,iv);iv2=f.e.Dyadic(1024);exact=iv2.field(f.e.compressed_entry(5,sam,label,factory))
  assert target[0]*(1<<512)<=exact[0]<=exact[1]<=target[1]*(1<<512),(label,'different actual compression')
assert list(f.indices(0))==[0] and list(f.indices(3))==list(range(8))
core=f.ActualDiagonal(5,sam,positive,path_limit=256)
for label in range(8):assert core.entry(label,iv)[0]>0
angles=[]
def collect(af):
 c,s=af(512);angles.append((c,s));return 1
blocks=list(f.post_blocks(core,selector=collect));assert len(angles)==4*(8-1)
# Full 8x8 action on the prepared xi, with multiprecision only as diagnostic;
# exact targets themselves above are outward intervals from the actual code.
mp.mp.dps=130;S=mp.mpf(2)**512
mid=lambda v:mp.mpf(int(v[0])+int(v[1]))/(2*S)
a=mid(iv.field(f.e.A));chi=mp.matrix([a**(3+bin(j).count('1')) for j in range(8)])
M=[mid(core.entry(j,iv)) for j in range(8)];vv=mp.matrix([M[j]*chi[j] for j in range(8)]);norm=mp.sqrt(sum(z*z for z in vv));vv=vv/norm
orders=list(range(7,0,-1))+list(range(1,8))+list(range(7,0,-1))+list(range(1,8))
for j,(C,S0) in zip(orders,angles):
 angle=4*mp.atan2(mid(S0),mid(C));c=mp.cos(angle);s=mp.sin(angle);u,v=vv[0],vv[j];vv[0]=c*u-s*v;vv[j]=s*u+c*v
err=mp.sqrt(sum((vv[i]-chi[i])**2 for i in range(8)));assert err<mp.mpf(2)**-100,err
# Exercise the real outward atan/grid selector for one small actual chi star.
pt=f.PositiveTarget(core);chosen=f.select_from_intervals(lambda bits:pt.star('chi',1,bits));_,q,_=f.a41.uniform_grid();assert 1<=chosen<=q
try:f.ActualDiagonal(4,(0,1,2),lambda:iter([{'op':'G','wires':[0]}])).entry(0,iv);raise AssertionError('targeted CODE accepted')
except AssertionError as ex:assert 'actual centre core' in str(ex)
out={'status':'PASS_A49_ACTUAL_FINITE_PATH_AND_POST_FIXTURES','python_version':sys.version.split()[0],'physical_work_wires':2,'all_8_CODE_labels_checked':True,'nontrivial_G_CX_repeat_and_interleaved_CODE':True,'exact_Q4_reference_enclosed':True,'positive_actual_core_all_labels':True,'four_star_lists_and_order_checked':True,'one_real_B80_selected_star':True,'actual_positive_target_post_maps_xi_to_chi_diagnostic_lt':'2^-100','diagnostic_mpmath_not_formal_interval_proof':True,'CODE_targeted_gate_rejected':True,'production_path_sum_executed':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(D/'finite_actual_target.py'):sha256((D/'finite_actual_target.py').read_bytes()).hexdigest()}}
(P/'ACTUAL_TARGET_FIXTURE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}))
