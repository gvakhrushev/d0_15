#!/usr/bin/env python3
"""B88 original-address current source and paid processor echo audit."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from collections import Counter
import json,sys
import sympy as sp
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round30'));import marked_source_schedule as a30
sys.path.insert(0,str(D/'round43'));import local_q_price as a43
plan=a30.g.namespace();slots=plan['source_slots'];reports={r['bank']:r for r in plan['reports']};rf=reports['f'];rq=reports['q']
def group(bank,kind):return {(x['walk'],x['copy']):(i,x) for i,x in enumerate(slots) if x['bank']==bank and x['kind']==kind}
fc=group('f','Choi');fm=group('f','CAR');qm=group('q','CAR')
assert len(fc)==180 and len(fm)==len(qm)==16 and set(fm)==set(qm)
assert Counter(k[0] for k in fm)==Counter({f'T{i}':2 for i in range(1,9)})
perm={};rows=[]
for key in sorted(fm):
    fi,f=fm[key];qi,q=qm[key]
    assert len(f['source'])==len(q['source'])==12 and len(f['RIGHT'])==len(q['RIGHT'])==7
    assert len(f['private'])==len(q['private'])==3
    for x,y in zip(f['source']+f['RIGHT'],q['source']+q['RIGHT']):
        assert x!=y and x not in perm and y not in perm;perm[x]=y;perm[y]=x
    rows.append({'walk':key[0],'copy':key[1],'f_slot':fi,'q_slot':qi,
       'f_DATA_physical_start':a30.b.physical_wire(f['source'][0]),'q_DATA_physical_start':a30.b.physical_wire(q['source'][0]),
       'f_RIGHT_physical_start':a30.b.physical_wire(f['RIGHT'][0]),'q_RIGHT_physical_start':a30.b.physical_wire(q['RIGHT'][0]),
       'DATA_width':12,'RIGHT_width':7})
assert len(perm)==608 and all(perm[perm[x]]==x for x in perm)
assert len({a30.b.physical_wire(x) for x in perm})==608
fl=set(range(rf['private_start'],rf['private_start']+rf['private_width'])) if False else None
# Do not expand 1.49 billion wires: interval proofs for all unmodified locals.
def inf(q,r):return r['private_start']<=q<r['private_start']+r['private_width']
fcar={q for _,x in fm.values() for q in x['source']+x['RIGHT']}
qcar={q for _,x in qm.values() for q in x['source']+x['RIGHT']}
fchoi={q for _,x in fc.values() for q in x['source']}
assert len(fcar)==len(qcar)==304 and len(fchoi)==3960
assert all(inf(q,rf) for q in fcar|fchoi) and all(inf(q,rq) for q in qcar)
assert all(not inf(q,rf) for q in qcar) and not fcar.intersection(fchoi)
assert all(perm[x] in qcar for x in fcar) and all(q not in perm for q in fchoi)
L=plan['layout'];fix={*L['SAM'],*L['SITE'],L['port'],L['aux_arbitrary'],*L['spin'],L['oldRIGHT_witness'],L['qubits']}
assert not fix.intersection(perm)
# The source preparation private helpers are retained, not substituted into
# report DATA/RIGHT. Original f processor private interval is reused.
all_private={q for _,x in list(fm.values())+list(qm.values()) for q in x['private']}
assert len(all_private)==96 and not all_private.intersection(perm)
N=plan['local_report']['logical_wire_count'];ns=a30.g.ns
def wire(q):
    x=ns.report_wire(plan,rf,q);return perm.get(x,x)
assert [wire(j) for j in range(8)]==L['SITE'] and wire(8)==rf['sigma']
assert all(wire(N+i)==ns.report_wire(plan,rf,N+i) for i in range(5))
assert not set(L['SAM']).intersection(perm)
stages=a30.stages();fwd=[i for i,x in enumerate(stages) if x=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0}];rev=[i for i,x in enumerate(stages) if x=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1}]
first_report=next(i for i,x in enumerate(stages) if x['kind']=='REPORT')
assert len(fwd)==len(rev)==1 and fwd[0]+1==rev[0] and rev[0]+1==first_report
assert sum(x['kind']=='SOURCE' for x in stages[:fwd[0]])==1372
# Every source is in the paid frame; its existing inverse uses two Z gadgets
# (four high-precision rotations) per G^{-1}. Check its first/last actual trees.
frame=a30.stage_blocks({'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1})
first=next(frame);last=None
for last in frame:pass
for tree in (first,last):
    _,pending,c=a30.c.production_compiler().transform(tree,0)
    assert pending==0 and c==Counter({'Z':2})
assert len(a30.resource_wires())==29848
eta=a30.inventory()['eta_common_new'];eps_frame=4*29848*F(1,2**7432)
assert eps_frame<F(1,2**7400) and eta+eps_frame<F(1,2**3232)
# Recompute the proposed echo actual G/CX counts and all-column error.
j=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
f={k:int(v) for k,v in j['native_forward_resources'].items()};r={k:int(v) for k,v in j['native_literal_raw_reverse_resources'].items()}
assert r['G_port']==f['G_port']+f['G_other'] and r['G_other']==0
assert r['CX']==f['CX']+6*f['G_other'] and r['SourceI']==3*f['SourceI']+4*(f['G_port']+f['G_other'])
p={k:f[k]+r[k] for k in f};census=json.loads((O/'round58/CZ_EXACT_OCCURRENCES.json').read_text())
assert census['CZ_per_report']==75196
CZ=2*75196;S_cz=20*75196;X_cz=28*75196
assert p['SourceI']>=S_cz and (p['SourceI']-S_cz)%2==0 and p['CX']>=X_cz
pairs=(p['SourceI']-S_cz)//2
cert=json.loads((D/'round38/POST_ANGLE_CERTIFICATE.json').read_text())
assert cert['status']=='PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS' and cert['error_bits']==20000
k=int(cert['rotations']['pi8']['exponent_hex'],16)
G=p['G_port']+p['G_other']+16*k*pairs+32*k*CZ
CX=p['CX']-X_cz+2*pairs+8*CZ
length=G+CX;weighted=16*pairs+32*CZ;ee=F(weighted,2**20000)
assert weighted.bit_length()==4154 and ee<F(1,2**15846) and ee<F(1,2**14623)
assert length.bit_length()==24233
# Re-run REAL A16->A17->A25 Hq source-copy templates through the
# f->q CAR mapping, both literal inverse depths, with A45 precision k.
rr=a30.g.report;ss=rr.s;nb=a30.c.nb;rp=plan['local_report']
walk=next(z for z in rp['walks'] if z['label']=='T1')
tables,events,records,ip,record,mapping,hh,root_phase,size=rr.walk_structure(walk['root'])
compiler=a30.c.Compiler(L['port'],L['spin'],L['qubits'],k);checked=0
for ri in (0,len(records)-1):
 mm=list(mapping)
 for aa,bb in zip(record,records[ri]):mm[aa]=bb
 for call in (z for z in ip['copy_calls'] if z['kind']==2):
  base=ss.lower(ss.map_ir(call['IR'],mm),a30.g.boolean_k(),size,(size+1,size+2),size+3)
  for depth in (0,1):
   tree=nb.inverse_literal(base,size,(size+1,size+2)) if depth else base
   tree=rr.a.remap_native(tree,lambda q:rr.a.global_wire(walk,q) if q<walk['local_wires'] else rp['native_port']+q-walk['local_wires'])
   tree=rr.a.remap_native(tree,wire)
   raw=list(nb.leaves(tree));assert any(set(v['wires'])&qcar for v in raw)
   assert not any(set(v['wires'])&fcar for v in raw)
   compiled,pending,cnt=compiler.transform(tree)
   assert pending==0 and cnt['CZ']==1 and cnt['CZ_depth_'+str(depth)]==1
   assert all(z['op'] in ('G','CX') and not set(z['wires']).intersection({*L['spin'],L['oldRIGHT_witness']}) for z in nb.leaves(compiled))
   checked+=1
assert checked==8
cfg=a43.extend_configuration(a43.old.production_configuration());newN=cfg['Nbase']+length
assert newN.bit_length()==25457 and 4*(newN.bit_length()+3158+1638+75+1+cfg['dimension_debt'])==137444
assert ee/(F(1,2**1618)*F(1,2**3158))<F(1,2**11070)
# Original A16 CAR SELECT acts nontrivially on the selected DATA on
# legitimate all-column inputs. This is one exact local node, not a claim
# that the full later REPORT was physically executed or measured.
select=a30.g.report.s;pair=select.pair_plan(12);ww=list(select.ideal_gates(pair['logical_IR']));layout=pair['layout']
def put(state,key,value):return select.logic.put(state,layout[key],value)
state=0
for key,value in [('a',81),('b',80),('data',81),('h',1),('delta',0)]:state=put(state,key,value)
def run(word,state):
 phase=1
 for op,*w in word:
  if op=='X':state^=1<<w[0]
  elif op=='CX':state^=((state>>w[0])&1)<<w[1]
  elif op=='CCX':state^=((state>>w[0])&(state>>w[1])&1)<<w[2]
  elif op=='Z':phase*=(-1)**((state>>w[0])&1)
  elif op=='CZ':phase*=(-1)**((state>>w[0])&(state>>w[1])&1)
  else:raise ValueError(op)
 return state,phase
end,phase=run(ww,state);expected=put(state,'data',80)
assert (end,phase)==(expected,1) and end!=state
back,phaseback=run(list(select.ideal_gates(pair['logical_IR'],True)),end)
assert back==state and phaseback*phase==1
# Abstract exact fixture with branch-correlated environment; the target is
# the FULL isometry, including R. Orthogonal D acts on selected source and
# processor workspace, I on R/old. Both exact echo and altered mark checked.
R=sp.Rational;I=sp.eye
v0=sp.Matrix([1,0]);v1=sp.Matrix([R(3,5),R(4,5)]);rr0=sp.Matrix([1,0]);rr1=sp.Matrix([R(5,13),R(12,13)])
e0=sp.Matrix([1,0]);e1=sp.Matrix([0,1]);work=sp.Matrix([1,0])
V=sp.kronecker_product(e0,v0,rr0,work).row_join(sp.kronecker_product(e1,v1,rr1,work));assert V.T*V==I(2)
rot=sp.Matrix([[R(5,13),-R(12,13)],[R(12,13),R(5,13)]])
DD=sp.kronecker_product(I(2),I(2),I(2),rot)
assert DD.T*DD==I(16) and DD.T*DD*V==V and DD*V!=V
# Discarding a branch-dependent R would change off-diagonal SAM effect.
X=sp.kronecker_product(sp.Matrix([[0,1],[1,0]]),I(8));corr=(V.T*X*V)[0,1]
assert corr==(v0.T*v1)[0]*(rr0.T*rr1)[0] and corr!=(v0.T*v1)[0]
# Reusing D, rather than a true inverse, is NOT automatically an exact echo.
assert DD*DD!=I(16)
files=[Path(__file__),Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'),D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',D/'round17/GLOBAL_REPORT_ASSEMBLY_RU.md',D/'round17/GLOBAL_REPORT_COMPILATION.json',
 D/'round17/report_assembly.py',D/'round16/source_select.py',D/'round16/DYNAMIC_SOURCE_SELECT_RU.md',D/'round25/h1_namespace.py',D/'round25/H1_NAMESPACE_PLAN.json',
 D/'round25/reversible_report_stream.py',D/'round29/gcx_compiler.py',D/'round29/gcx_birth_clock.py',
 D/'round30/marked_source_schedule.py',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',
 D/'round38/POST_ANGLE_CERTIFICATE.json',D/'round43/LOCAL_Q_PRICE_RU.md',D/'round43/local_q_price.py',
 O/'round25/targets.py',O/'round58/CZ_EXACT_OCCURRENCES.json',O/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',
 O/'round86/B86_ORIGINAL_MARK_ADMISSION_RU.md']
out={'status':'COMPOSITE_CURRENT_ISOMETRY_AND_PAID_PROCESSOR_ECHO_CONDITIONAL_AUDIT',
 'selected_f_Choi_copies':180,'selected_q_CAR_copies':16,'source_binding_swap_pairs':304,
 'q_car_physical_bindings':rows,'real_mapped_Hq_CAR_templates_checked':checked,'common_SITE_preserved':True,'f_sigma_and_report_private_reused':True,
 'all_old_RIGHT_and_remainders_retained':True,'zero_new_source_births_for_echo':True,
 'pre_REPORT_decoded_prefix_error_lt':'2^-3232',
 'per_inverse_BR_resource_replacement_rotations':4,
 'echo_SI_pairs_hex':hex(pairs),'echo_SI_pairs_bit_length':pairs.bit_length(),'echo_CZ_macros':CZ,
 'echo_G_hex':hex(G),'echo_CX_hex':hex(CX),'echo_total_gate_count_hex':hex(length),'new_Nbase_hex':hex(newN),
 'echo_error_numerator_hex':hex(weighted),'echo_error_denominator_power_of_two':20000,
 'echo_weighted_rotation_error_units_bit_length':weighted.bit_length(),
 'echo_all_column_error_lt':'2^-15846','echo_G_plus_CX_count_bit_length':length.bit_length(),
 'new_Nbase_bit_length':newN.bit_length(),'new_K':137444,
 'echo_error_divided_by_tgs_lt':'2^-11070',
 'reuse_is_an_independent_eighth_bank':False,'later_REPORT_select_nontrivial_on_selected_source':True,
 'all_original_Dnu_prefix_marks_verified':False,'original_task_admission_proved':False,
 'physical_C_closed':False,'GR_closed':False,
 'source_sha256':{str(f.resolve()):sha256(f.read_bytes()).hexdigest() for f in files}}
Path(__file__).with_name('B88_COMPOSITE_PROCESSOR_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
