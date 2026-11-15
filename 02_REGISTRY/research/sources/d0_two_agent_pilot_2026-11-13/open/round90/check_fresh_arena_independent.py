#!/usr/bin/env python3
"""Independent fresh source/report geometry and logical commutator audit."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
import json,sys
import sympy as sp
import numpy as np
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round30'));import marked_source_schedule as a
plan=a.g.namespace();l=plan['layout'];N=l['qubits'];report=plan['local_report'];nold=sum(x['stop']-x['start'] for x in a.b.birth_blocks())
assert N==10407050784 and nold==10407050782
assert a.b.physical_wire(2)==1 and a.b.physical_wire(N)==nold-1
r={x['bank']:x for x in plan['reports']};f=r['f'];q=r['q']
assert all(x['private_width']==report['logical_wire_count']-8 for x in plan['reports'])
width=report['logical_wire_count']-8;extra=180*24+16*3
start=N+1;private=start+width;end=private+extra
assert width==1486716786 and extra==4368 and width+extra==1486721154
assert start==N+1 and a.b.physical_wire(N)==nold-1
# Extend A29's physical map ONLY on new q>N, preserving every old mapping.
def physical(logical,old_prefix=0):
 if logical<=N:return a.b.physical_wire(logical,old_prefix)
 return old_prefix+logical-3
assert physical(start)==nold and physical(end-1)==nold+width+extra-1
assert physical(N,7)==7+nold-1 and physical(start,7)==7+nold
assert end-start==width+extra and nold+width+extra==11893771936
assert all(x['private_start']+x['private_width']<=N for x in plan['reports'])
# Reconstruct same local report roles on independent fresh addresses, using f
# Choi and q CAR catalogues. Copies are generated from scratch, not remapped
# f/q source DATA. DATA reside within report interval; extra private follows it.
chosen=[];cursor=private
for _,template in [(i,z) for i,z in enumerate(plan['source_slots']) if z['bank']=='f']:
 kind=template['kind'];bank='f' if kind=='Choi' else 'q'
 src=[(i,z) for i,z in enumerate(plan['source_slots']) if z['bank']==bank and z['kind']==kind and z['walk']==template['walk'] and z['copy']==template['copy']]
 assert len(src)==1
 for oldidx,z in src:
  rr=r[bank]
  data=[start+(x-rr['private_start']) for x in z['source']]
  right=[start+(x-rr['private_start']) for x in z.get('RIGHT',[])]
  assert all(start<=x<private for x in data+right)
  k=24 if kind=='Choi' else 3
  pr=list(range(cursor,cursor+k));cursor+=k
  chosen.append({'kind':kind,'walk':z['walk'],'copy':z['copy'],'old_template_slot':oldidx,
      'fresh_DATA_start':physical(data[0]),'DATA_width':len(data),
      'fresh_RIGHT_start':physical(right[0]) if right else None,'RIGHT_width':len(right),
      'fresh_source_private_start':physical(pr[0]),'private_width':len(pr),
      'logical_data':data,'logical_right':right,'logical_private':pr})
assert len(chosen)==196 and Counter(x['kind'] for x in chosen)=={'Choi':180,'CAR':16}
assert cursor==end
wires=[q for row in chosen for q in row['logical_data']+row['logical_right']+row['logical_private']]
assert len(wires)==len(set(wires))==4264+4368
assert all(N<q<end for q in wires)
assert not set(wires).intersection(a.resource_wires())
assert not set(wires).intersection([N,*l['SAM'],*l['SITE'],l['port'],l['aux_arbitrary'],*l['spin'],l['oldRIGHT_witness']])
oldframe=set(a.resource_wires());freshframe={q for row in chosen for q in row['logical_data']+row['logical_right']}
assert len(oldframe)==29848 and len(freshframe)==4264 and len(oldframe|freshframe)==34112
# Existing seven REPORT intervals and shared old helper cannot address any
# fresh coordinate. Their ideal stages may use SITE, aux or port; all old.
for r0 in plan['reports']:
 assert r0['private_start']+r0['private_width']<=start
 assert all(not (r0['private_start']<=q<r0['private_start']+r0['private_width']) for q in freshframe)
sc6=plan['SC6_local_to_global'];assert len(sc6)==23 and len(sc6)==len(set(sc6))
assert set(sc6).isdisjoint(set(wires)|set(l['SITE'])|{N})
assert sc6[:5]==l['SC6_selectors'] and sc6[-4:]==[l['port'],*l['spin'],l['oldRIGHT_witness']]
assert set(sc6[5:19])=={z for rr in plan['reports'] for z in (rr['all_READY'],rr['REPORT'])}
# RAW-frame addition. Source prefix and exact f/q input error budgets consumed.
epschoi=a.g.choi.errors()[2];epscar=a.g.car.error_bound('q');eta_extra=180*epschoi+16*epscar
assert a.inventory()['eta_common_old']+eta_extra<F(1,2**3232)
assert 4*len(freshframe)*F(1,2**7432)<F(1,2**7400)
# Extra current bank changes SAM-controlled prefix even when the COMPLETE
# endpoint remains identical. Rebuild the source bounds, not W-only transfer.
s=F(1,2**30);e_pre=F(1,2**3232);assert 540<F(93,4)**2
lamco=F(93,4)*F(3,32)*s+2*e_pre
lamlink=19*F(27,32)*s+2*e_pre
lamcar=6*F(11,160)*s+2*e_pre
assert lamco<F(9,4)*s and lamlink<17*s and lamcar<s
radius2=540*256*F(3,16)**2+360*256*F(81,16)**2+32*F(11,10)**2
assert radius2<F(1539**2) and 1539*s+2*e_pre<1540*s
assert F(3,4)*85*2*(1540*s)**2<F(1,2**31)
# Endpoint I is unchanged, but an intermediate SAM skew insertion is not.
# This exact 2-wire illustration is a logical negative control, not a root.
J2=sp.Matrix([[0,-1],[1,0]]);Ic=sp.eye(2);Y=sp.kronecker_product(J2,Ic)
Pz=sp.diag(1,0);Po=sp.diag(0,1);Xc=sp.Matrix([[0,1],[1,0]])
U=sp.kronecker_product(Pz,Ic)+sp.kronecker_product(Po,Xc)
assert U.T*U==sp.eye(4) and U.T*sp.eye(4)*U==sp.eye(4) and U.T*Y*U!=Y
# Independent production-sized native counts derived from existing provider
# inventories (no A46 generator and no expanded word).
inv=a.inventory();choiF=Counter(a.g.choi.inventory('f')['RAW_prepared_forward']);carF=Counter(a.g.car.inventory('q')['source_forward'])
rec=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
reportF=Counter({k:int(v) for k,v in rec['native_forward_resources'].items()})
sigmaF=Counter({'G_port':1,'CX':6,'SourceI':4})
def pair_count(c):return c+a.g.inverse_counts(c)
def times(c,n):return Counter({k:v*n for k,v in c.items()})
fresh_W=times(pair_count(choiF),180)+times(pair_count(carF),16)+pair_count(sigmaF)+pair_count(reportF)
fresh_W+=Counter({'G_port':3*4264,'G_other':4264,'CX':18*4264,'SourceI':24*4264})
W_oldprofile=inv['W_old_profile']+fresh_W;CZ=16*75196
W_compiled,rotW=a.translate_counts(W_oldprofile,CZ,10*CZ)
assert rotW.bit_length()==4188 and rotW<2**4188 and sum(W_compiled.values()).bit_length()==11647
pre=inv['checkpoint_old_profile']+times(choiF,180)+times(carF,16)+sigmaF+Counter({'G_other':4264})
pre_compiled,rotpre=a.translate_counts(pre,0,0)
assert a.inventory()['eta_common_old']+eta_extra+F(rotpre,2**7432)<F(1,2**3232)
oldplan=json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text())
def decode(z):return F(int(z['numerator_hex'],16),int(z['denominator_hex'],16))
eta_old_all=decode(oldplan['canonical_input_error_bound'])
seven_report_bound=F(int(rec['seven_report_all_known_approximate_macros']),2**4096)
eW=F(rotW,2**7432);eB=2*(eta_old_all+eta_extra+seven_report_bound)+eW
assert eW<F(1,2**3244) and eB<F(1,2**3231)
# Cross-check the independently reconstructed addresses and counts against
# A46's actual namespace and inventory, without calling its output writer.
sys.path.insert(0,str(D/'round46'));import independent_current_bank as a46
p46=a46.namespace();assert p46['old_compiler_helper']==N and p46['fresh_logical_interval']==[start,end]
assert p46['layout']['qubits']==end and p46['SC6_local_to_global']==plan['SC6_local_to_global']
fresh=p46['reports'][7];actual=[p46['source_slots'][i] for i in fresh['source_slots']]
assert len(actual)==len(chosen)==196
actual_bykey={(z['kind'],z['walk'],z['copy']):z for z in actual};assert len(actual_bykey)==196
for w in chosen:
 z=actual_bykey[w['kind'],w['walk'],w['copy']]
 assert z['source']==w['logical_data'] and z.get('RIGHT',[])==w['logical_right'] and z['private']==w['logical_private']
 assert z['bank']==('f' if z['kind']=='Choi' else 'q')
 assert a46.physical_wire(z['source'][0])==w['fresh_DATA_start']
assert a46.physical_wire(N)==nold-1 and a46.physical_wire(start)==nold and len(a46.resource_wires())==34112
assert sum(x['stop']-x['start'] for x in a46.birth_blocks())==11893771936
st=a46.stages();assert sum(x['kind']=='SOURCE' for x in st)==1568 and sum(x['kind']=='REPORT' for x in st)==8
assert next(i for i,x in enumerate(st) if x.get('kind')=='REPORT' and x.get('report')==7)>max(i for i,x in enumerate(st) if x.get('kind')=='REPORT' and x.get('report',7)<7)
inv46=a46.inventory();assert inv46['W_old_profile']==W_oldprofile and inv46['W_new']==W_compiled
assert inv46['checkpoint_new']==pre_compiled and inv46['W_rotations']==rotW
assert inv46['eta_common_new']<F(1,2**3232) and inv46['replacement_error']<F(1,2**3244)
assert inv46['full_compressed_error']<=eB and inv46['full_compressed_error']<F(1,2**3231)
assert inv46['W_CZ']==CZ and inv46['W_CZ_SourceI']==10*CZ
report46=(D/'round46/INDEPENDENT_CURRENT_BANK_RU.md').read_text()
for fragment in ('Старый A29 compiler helper', 'не адресуют fresh DATA', '2^-31', 'same-task FN admission'):
 assert fragment in report46
record46=json.loads((D/'round46/INDEPENDENT_CURRENT_BANK_CHECK.json').read_text());assert record46['status']=='PASS_INDEPENDENT_CURRENT_BANK_ADDRESS_CLOCK_AND_ERROR_CHECKS'
plan46=json.loads((D/'round46/INDEPENDENT_CURRENT_BANK_PLAN.json').read_text());assert a46.build()==plan46
for source,h in plan46['source_sha256'].items():assert sha256(Path(source).read_bytes()).hexdigest()==h
cfg46=a46.production_configuration();assert cfg46['n']==11893771936 and cfg46['Nbase'].bit_length()==25457 and cfg46['K']==137444
bd46=a46.bounds();assert bd46['fresh_j2_prefix_distance']==F(9,4)*s and bd46['global_old_profile_source_distance']==1540*s
assert bd46['all_real_SAM_Q_analytic_reduction_error']<F(1,2**31)
assert bd46['Qb_finite_positive_lower']>F(1,2**45)
# Actual source prefixes of both fresh types use the existing helper, never
# identify it with old aux, and emit physical G/CX after compilation.
for kind in ('Choi','CAR'):
 si=next(i for i in fresh['source_slots'] if p46['source_slots'][i]['kind']==kind)
 tree=next(a46.stage_blocks({'kind':'SOURCE','slot':si}));mapped,pending,_=a.c.production_compiler().transform(tree,0)
 assert pending==0
 for gate in a.c.nb.leaves(mapped):
  assert gate['op'] in ('G','CX')
  assert not set(gate['wires']).intersection({0,1,3})
  for wire in gate['wires']:assert 0<=a46.physical_wire(wire)<cfg46['n']
# Exact full-matrix fixture: D acts on shared SITE+fresh only; H acts on old
# READY+port, so commute on ALL columns. No partial traces or postselection.
I=sp.eye;R=sp.Rational;G=sp.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]])
P0=sp.diag(1,0);P1=sp.diag(0,1);Z=sp.diag(1,-1);X=sp.Matrix([[0,1],[1,0]])
# tensor order SITE, fresh, old READY, port
Df=sp.kronecker_product(P0,I(2),I(2),I(2))+sp.kronecker_product(P1,G,I(2),I(2))
H=sp.kronecker_product(I(2),I(2),P0,I(2))+sp.kronecker_product(I(2),I(2),P1,Z)
assert Df.T*Df==I(16) and H.T*H==I(16) and Df*H==H*Df and Df.T*H*Df==H
# If SC6 is altered to read fresh READY/data, the exact cancellation can fail.
Hbad=sp.kronecker_product(I(2),P0,I(2),I(2))+sp.kronecker_product(I(2),P1,I(2),Z)
assert Hbad*Df!=Df*Hbad
# Native sharing PORT may break exact commutation; error is not zero by name.
E=sp.kronecker_product(I(2),I(2),I(2),G);Dn=E*Df
assert Dn*H!=H*Dn
norm=lambda m:np.linalg.norm(np.array(m,dtype=float),ord=2)
assert norm(Dn.T*H*Dn-H)<=2*norm(Dn-Df)+1e-12
# Full labelled isometry retains b-dependent old remainder. Old REPORT
# acts on SITE/old only and hence does not operate on fresh source at all.
# Constant-free G gate shows original data not reset or selected.
oldreport=sp.kronecker_product(P0,I(2),I(2),I(2))+sp.kronecker_product(P1,I(2),X,I(2))
assert oldreport*sp.kronecker_product(I(2),Z,I(2),I(2))==sp.kronecker_product(I(2),Z,I(2),I(2))*oldreport
files=[Path(__file__),D/'round46/independent_current_bank.py',D/'round46/INDEPENDENT_CURRENT_BANK_PLAN.json',D/'round46/check_independent_current_bank.py',D/'round46/INDEPENDENT_CURRENT_BANK_CHECK.json',D/'round46/INDEPENDENT_CURRENT_BANK_RU.md',D/'round25/H1_NAMESPACE_PLAN.json',D/'round25/h1_namespace.py',D/'round25/global_h1.py',
 D/'round29/gcx_birth_clock.py',D/'round30/marked_source_schedule.py',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',
 D/'round17/GLOBAL_REPORT_ASSEMBLY_RU.md',D/'round17/GLOBAL_REPORT_COMPILATION.json',
 D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',O/'round25/targets.py',O/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',
 O/'round86/B86_ORIGINAL_MARK_ADMISSION_RU.md',O/'round88/B88_COMPOSITE_PREPARED_PROCESSOR_RU.md']
out={'status':'FRESH_INDEPENDENT_ARENA_AND_LOGICAL_COMMUTATION_CONDITIONAL_AUDIT',
 'A46_final_report_checked_and_pinned':True,'A46_namespace_inventory_crosschecked':True,'A46_own_plan_rebuilt_and_pins_verified':True,'old_aux_logical_2_physical':1,'old_A29_compiler_helper_logical':N,'old_compiler_helper_physical':physical(N),
 'fresh_report_start_physical':physical(start),'fresh_report_width':width,'fresh_source_private_width':extra,
 'new_births':width+extra,'total_births':nold+width+extra,'fresh_Choi':180,'fresh_CAR':16,
 'old_frame_source_wires':len(oldframe),'fresh_frame_source_wires':len(freshframe),'new_frame_source_wires':len(oldframe|freshframe),
 'fresh_source_addresses':[ {k:v for k,v in z.items() if not k.startswith('logical_')} for z in chosen],
 'old_plus_fresh_source_prefix_error_lt':'2^-3232','fresh_full_word_replacement_error_lt':'2^-3244',
 'coarse_seven_report_compressed_error_lt':'2^-3231','new_total_CZ':CZ,
 'new_old_profile_W_counts_hex':{k:hex(v) for k,v in W_oldprofile.items()},
 'new_compiled_W_counts_hex':{k:hex(v) for k,v in W_compiled.items()},
 'new_prefix_compiled_counts_hex':{k:hex(v) for k,v in pre_compiled.items()},
 'original_SC6_is_seven_reports_only':True,'ideal_logical_fresh_D_and_original_SC6_sign_commute_all_columns':True,
 'native_fresh_D_exact_port_commutation_claimed':False,
 'updated_coframe_edge_bound_lt':'(9/4)*s','updated_all_label_source_radius_lt':'1540*s',
 'endpoint_equality_does_not_prove_inner_Q_kernel_equality':True,'additional_fresh_source_input_error_lt':'2^-3232 combined with old source',
 'original_all_columns_source_preparer_commutation_proved':False,'original_H1_FN_physical_admission_proved':False,
 'GR_closed':False,'source_sha256':{str(f.resolve()):sha256(f.read_bytes()).hexdigest() for f in files}}
Path(__file__).with_name('B90_FRESH_ARENA_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
