#!/usr/bin/env python3
"""Exact J-commutation certificates for actual native macro building blocks."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,json,sys
import sympy as S
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sys.modules[name]=m;sp.loader.exec_module(m);return m
nb=load('b47_nb',D/'round14/native_boolean.py');gray=load('b47_gray',D/'round22/gray_reflection.py')
J=S.Matrix([[0,-1],[1,0]]);X=S.Matrix([[0,1],[1,0]]);c,s=S.symbols('c s',real=True);R=c*S.eye(2)+s*J
assert X*J*X==-J and R*J==J*R and (X*R*X)*J==J*(X*R*X)
# A14 actual Walsh primitive: compare each emitted sandwich to own parity
# construction, for every subset and patterns on K <=4. Since its controls are
# disjoint from aux, each complete sandwich is R(theta) or R(-theta) on aux.
terms=0
for K in range(1,5):
 controls=list(range(K));aux=K;port=K+1;spin=(K+2,K+3)
 for patternint in range(1<<K):
  patt=[patternint>>i&1 for i in range(K)];tree=nb.selective_rotation(controls,patt,aux,1,port,spin)
  assert len(tree['children'])==1<<K
  for mask,t in enumerate(tree['children']):
   wires=[controls[i] for i in range(K) if mask>>i&1];parity=[nb.gate('CX',x,aux) for x in wires];sign=(-1)**sum(patt[i] for i in range(K) if mask>>i&1)
   assert t==nb.seq(*parity,nb.rotation_power(aux,sign,port,spin),*reversed(parity));terms+=1
# Verify A14 CCX exactly composes phase target aux and rotation target logical.
for k in (1,7):
 cs=[0,1];t=2;aux=3;p=4;sp=(5,6)
 assert nb.boolean_word('CCX',k,control=cs,target=t,aux=aux,port=p,spin=sp)==nb.seq(nb.selective_rotation([*cs,t],[1,1,1],aux,k,p,sp),nb.selective_rotation(cs,[1,1],t,k,p,sp))
 for gate in ('X','H'):
  tree=nb.boolean_word(gate,k,target=t,port=p,spin=sp)
  assert all(aux not in x['wires'] for x in nb.leaves(tree))
# Actual Gray emitter, exact parity toggles, returns aux target to even X
# parity for every control word. Its intervening rotations become signed R's;
# angle may depend on controls, but every resulting R commutes with J.
gray_rows=[]
for K in range(1,11):
 ctr=list(range(K));aux=K;p=K+1;sp=(K+2,K+3);ts=1<<K
 actual=list(gray.blocks(ctr,aux,1,p,sp));assert len(actual)==ts+1
 assert actual[0]==nb.repeat(1,nb.gate('G',aux)) and actual[-1]==nb.gate('CX',ctr[-1],aux)
 for i in range(1,ts):assert actual[i]==nb.seq(nb.gate('CX',ctr[(i&-i).bit_length()-1],aux),nb.repeat(1,nb.gate('G',aux)))
 for x in range(ts):
  parity=0
  for i in range(1,ts):parity^=(x>>((i&-i).bit_length()-1))&1
  parity^=(x>>(K-1))&1
  assert parity==0
 gray_rows.append({'K':K,'all_control_columns':ts})
# B31 actual router: rebuild all native macros, verify aux disjoint in every
# logical op and no aux in true zero/kernel raw prefix.
B31=O/'round31';sys.path.insert(0,str(B31));fr=load('b47_fair',B31/'fair_router.py');d=json.loads((B31/'NATIVE_FAIR_BANK.json').read_text());lay,logical=fr.router(28);p=d['port'];sp=tuple(d['spin']);aux=d['aux_arbitrary'];old=d['protected_oldRIGHT'];k=int(d['k']);assert p==143 and aux==146 and old==147
macros=[];ops=Counter()
for op,*w in logical:
 assert aux not in w and old not in w and p not in w and not set(sp)&set(w);ops[op]+=1
 if op=='CX':tree=nb.gate('CX',*w)
 elif op=='X':tree=nb.boolean_word('X',k,target=w[0],port=p,spin=sp)
 else:assert op=='CCX';tree=nb.boolean_word('CCX',k,control=w[:2],target=w[2],aux=aux,port=p,spin=sp)
 macros.append(tree)
assert nb.seq(*macros)==d['router_forward_DAG'];assert nb.inverse_literal(d['router_forward_DAG'],p,sp)==d['router_literal_raw_inverse_DAG']
for gate in d['zero_and_kernel_forward']['gates']:assert aux not in gate['wires'] and old not in gate['wires']
# Local owner comparator: distinct protected hypothetical shared aux must be
# outside these 23 local wires when a global interface is actually bound.
comp={}
for name in ('SC6_FORWARD.jsonl','SC6_INVERSE.jsonl'):
 gs=[json.loads(line) for line in (O/'round21'/name).read_text().splitlines()];assert len(gs)==18176
 counts=Counter(g['op'] for g in gs);assert counts=={'G':5888,'CX':4096,'SourceI':8192};i=0
 while i<len(gs):
  g=gs[i];assert all(0<=w<22 for w in g['wires'])
  if g['op']=='SourceI':assert gs[i+1]==g and g['wires']==[19,20,21];i+=2
  else:i+=1
 comp[name]={'calls':len(gs),'SourceI_as_exact_adjacent_pairs':True,'local_oldRIGHT_untouched':True}
# A17: bound native roles are outside every logical-wire index; distinct report.
plan=json.loads((D/'round17/GLOBAL_REPORT_PLAN.json').read_text());n=plan['logical_wire_count'];assert plan['native_port']==n and plan['native_spin']==[n+1,n+2] and plan['native_aux_arbitrary']==n+3 and plan['protected_oldRIGHT_witness']==n+4 and plan['report_wire']<n
assert all(w['private_start']+w['private_width']<=plan['compiler_region_end'] for w in plan['walks']);assert plan['fair_bank_extra_start']+plan['fair_bank_count']*142==n
assert all(0<=x<n for x in [*plan['sign_wires_S1_S2_T1_to_T8'],plan['report_wire'],plan['all_READY_wire'],plan['post_label_wire'],plan['post_READY_wire']])
a19=load('b48_choi_prefix',D/'round19/choi_prefix.py');a19_l=a19.layout();cert=json.loads((D/'round19/CHOI_PREFIX_CERTIFICATE.json').read_text());prefix_checks=[]
for control in (False,True):
 for ins in a19.instructions(a19_l,control):
  K=len(ins['controls']);q=ins['target'];aux=a19_l['aux_arbitrary'];p=a19_l['port'];sp=tuple(a19_l['spin']);assert len(set([*ins['controls'],q,aux,p,*sp]))==K+5
  got=a19.lower(ins,cert,a19_l)
  if ins['op']=='address_rotation':want=nb.selective_rotation(ins['controls'],ins['pattern'],q,int(cert['address_power']['k'])*2**(1-K),p,sp)
  else:
   kk=int(cert['boolean_common_power']['k']);phase=nb.selective_rotation([*ins['controls'],q],[*ins['pattern'],1],aux,16*kk//2**(K+1),p,sp);mul=4 if ins['op']=='H' else 8;want=nb.seq(phase,nb.selective_rotation(ins['controls'],ins['pattern'],q,mul*kk//2**K,p,sp))
  assert got==want;prefix_checks.append(ins['op'])
# B39 fixed point adapter's every F predicate gate uses logical roles disjoint
# from aux, while H/good/flagphase/correction address only branch and rebit.
ad=load('b48_adapter',O/'round39/adapter_native.py');al=ad.layout(0,8);fx=ad.fixed(al,3,5,7);aux=al['aux_arbitrary']
assert all(aux not in wires for op,*wires in fx['Flogical'])
assert all(aux not in leaf['wires'] for tree in [fx['H'],*fx['good'],fx['correction']] for leaf in nb.leaves(tree))
files=[D/'round14/native_boolean.py',D/'round22/gray_reflection.py',D/'round17/report_assembly.py',D/'round17/GLOBAL_REPORT_PLAN.json',D/'round16/source_select.py',D/'round19/choi_prefix.py',D/'round19/CHOI_PREFIX_CERTIFICATE.json',O/'round39/adapter_native.py',B31/'NATIVE_FAIR_BANK.json',O/'round21/SC6_FORWARD.jsonl',O/'round21/SC6_INVERSE.jsonl']
out={'status':'PASS_AUX_COMMUTING_MACROS_WITH_GLOBAL_BINDING_OBLIGATIONS','source_sha256':{str(x):sha256(x.read_bytes()).hexdigest() for x in files},'A14_exhaustive_small_actual_walsh_sandwich_terms':terms,'general_argument':'X J X = -J and R(theta)=cI+sJ; each complete CX-parity / R / parity-inverse sandwich commutes with J_aux for any controls and angle. Ops with no aux commute. Literal inverse and composition inherit commutation. Individual parity CX need not commute.','A14_CCX_actual_structure_checked':True,'A19_controlled_and_uncontrolled_all_instructions_checked':dict(Counter(prefix_checks)),'B39_fixed_point_F_predicate_gates_aux_disjoint':len(fx['Flogical']),'A22_actual_gray_cycles_checked':gray_rows,'A22_general_gray_argument':'Gray cycle returns total X parity to even; each parity-conjugated rotation is cI±sJ. Full cycle commutes with J_aux; individual emitted blocks need not.','B31_actual_router_logical_counts':dict(ops),'B31_router_full_DAG_reconstructed':True,'B31_zero_kernel_aux_untouched':True,'original_comparator_local_words':comp,'A17_namespace_disjoint_arithmetic_checked':True,'global_assembly_binding_proved':False,'all_actual_H1_generators_and_work_embedding_proved':False,'other_D_identity_or_SAM_control_proved_for_whole_H1':False,'marks_physical_admission_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'AUX_MACRO_COMMUTATION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'actual_walsh_terms':terms,'fair_router_ops':dict(ops),'comparator_calls_per_direction':18176}))
