#!/usr/bin/env python3
"""Independent A22 joint-projector/price/paid-depth assembly review."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from itertools import zip_longest
from fractions import Fraction
import sys,json
import sympy as s
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round22');sys.path.insert(0,str(D));import full_choi_bank as b
names=['full_choi_bank.py','FULL_CHOI_BANK_PLAN.json','check_full_choi_bank.py','FULL_CHOI_BANK_CHECK.json'];files=[D/x for x in names];hh=lambda p:sha256(Path(p).read_bytes()).hexdigest();digests={str(p):hh(p) for p in files};plan=json.loads(files[1].read_bytes());ownercheck=json.loads(files[3].read_bytes());assert ownercheck['plan_sha256']==digests[str(files[1])] and ownercheck['checker_sha256']==digests[str(files[2])]
for f,h in plan['source_sha256'].items():assert hh(f)==h
lay=b.layout();b.validate(lay);data=b.data(lay);private=b.private(lay);assert len(data)==22 and len(private)==24 and len(set(data+private))==46 and plan['joint_anchor_wires']==data+private
assert plan['original_DATA_columns']==1<<22 and plan['includes_padding_RAW_mixed_columns'] and plan['new_reflection_clean_work']==0
assert 'private24 initially zero' in plan['original_target'] and plan['private24_RAW_initialization_must_be_bound_to_actual_births']
ext=dict(lay,qubits=2747);b.validate(ext,range(2739,2747))
for q in [data[0],private[0],lay['SAM'][0],lay['aux_arbitrary'],lay['port'],*lay['spin'],lay['oldRIGHT_witness']]:
 try:b.validate(ext,[q]);raise AssertionError('collision accepted')
 except AssertionError as e:
  if str(e)=='collision accepted':raise
# Exact original raw vector conversion using a²=p, a⁴+a²=1.
a=s.symbols('a');M=s.Matrix([[a,a*a],[-a*a,a]]);v=s.Matrix([a,a*a]);w=M*v
assert all(s.rem(s.Poly(s.expand(x),a),s.Poly(a**4+a**2-1,a)).as_expr()==0 for x in (w-s.Matrix([1,0])))
# Derive native resource prices from exact A21 Omega totals and actual B39
# fixed DAGs; never call b.inventory, c.counts or adapter.native_budget.
def cost(t,port):
 op=t['op']
 if op=='seq':
  z=Counter()
  for q in t['children']:z.update(cost(q,port))
  return z
 if op=='repeat':return Counter({k:int(t['count'])*v for k,v in cost(t['child'],port).items()})
 return Counter({('G_port' if t['wires'][0]==port else 'G_other') if op=='G' else op:1})
def T(x):return Counter({'G_port':x['G_port']+x['G_other'],'CX':x['CX']+6*x['G_other'],'SourceI':3*x['SourceI']+4*(x['G_port']+x['G_other'])})
def times(x,k):return Counter({a:b*k for a,b in x.items()})
x=b.c.inputs();fixed=b.c.adapter.fixed(b.c.adapter_layout(lay),int(x['phase']['phase_k']),int(x['phase']['correction_l']),x['h_k']);H=cost(fixed['H'],lay['port']);G=sum((cost(q,lay['port']) for q in fixed['good']),Counter());S=sum((cost(q,lay['port']) for q in fixed['start']),Counter());C=cost(fixed['correction'],lay['port']);source=json.loads((b.D/'round21/CHOI_LOADER_PLAN.json').read_bytes());e=json.loads((D/'GRAY_REFLECTION_CERTIFICATE.json').read_bytes())['entries']['46'];r=Counter({'G_other':(1<<46)*int(e['k']),'CX':1<<46});raw=Counter({'G_port':22,'CX':132,'SourceI':88});priv=Counter({'G_port':24,'CX':144,'SourceI':96});axes=('G_port','G_other','CX','SourceI')
for bank in ('y+','y-','f','0','x+','x-','q'):
 cv=Counter({k:int(v) for k,v in source['banks'][bank]['Omega_forward'].items()});u=times(H,2)+cv
 for _ in range(8):u=times(u,2)+T(u)+G+S
 u.update(C);full=raw+r+T(u)+r+u;prepared=priv+full
 vals={'DATA22_RAW_inverse':raw,'private24_RAW_to_zero':priv,'R_joint46':r,'R_joint46_literal_inverse':T(r),'U_half_forward':u,'U_half_literal_inverse':T(u),'bank_forward':full,'bank_literal_inverse':T(full),'RAW_prepared_forward':prepared,'RAW_prepared_literal_inverse':T(prepared)}
 for key,value in vals.items():assert all(int(plan['native_inventories'][bank][key][q])==value[q] for q in axes),(bank,key)
# Error calculation uses the exact A21 fractions, not loose powers.
a21=json.loads((b.D/'round21/CHOI_LOADER_PLAN.json').read_bytes());eta=Fraction(int(a21['error_numerators_hex'][3],16),int(a21['error_denominators_hex'][3],16));delta=Fraction(1,2**3264);total=4*eta+2*delta;copy=1260*total
assert eta<Fraction(1,2**3230) and total<Fraction(1,2**3227) and copy<Fraction(1,2**3216)
assert [hex(q.numerator) for q in (eta,delta,total,copy)]==plan['exact_error_numerators_hex'] and [hex(q.denominator) for q in (eta,delta,total,copy)]==plan['exact_error_denominators_hex']
# Exact witness: only the JOINT anchor reflection works for an arbitrary U
# extension. U=X_data SWAP(data,private) sends the complete anchor isometry
# to |1,0>⊗I_ext but mixes an off-anchor clean data column with private.
def at(d,p,e):return 4*d+2*p+e
I=s.eye(8);X=s.zeros(8);W=s.zeros(8)
for d in (0,1):
 for p in (0,1):
  for e in (0,1):X[at(1-d,p,e),at(d,p,e)]=1;W[at(p,d,e),at(d,p,e)]=1
U=X*W;J=I[:,[at(0,0,0),at(0,0,1)]];V=I[:,[at(1,0,0),at(1,0,1)]];assert U*J==V
Rjoint=s.diag(*[-1 if d==0 and p==0 else 1 for d in (0,1) for p in (0,1) for e in (0,1)])
Rdata=s.diag(*[-1 if d==0 else 1 for d in (0,1) for p in (0,1) for e in (0,1)])
E=I[:,[at(d,0,e) for d in (0,1) for e in (0,1)]];wanted=-E
assert U*Rjoint*U.T*Rjoint*E==wanted and U*Rdata*U.T*Rdata*E!=wanted
# Also prove the clean-private restriction is not an arbitrary-private theorem.
assert U*Rjoint*U.T*Rjoint!=-I
# Actual forward and reversed stage chronology, including 24 extra RAW words.
for init in (False,True):
 base=([('PRIVATE_RAW',0)] if init else [])+[('DATA_RAW',0),('R',0),('U',1),('R',0),('U',0)]
 for depth in range(5):assert b.stage_schedule(depth,init)==[(k,depth+d) for k,d in (reversed(base) if depth%2 else base)]
for p,h in digests.items():assert hh(p)==h
out={'status':'PASS_INDEPENDENT_A22_FULL_RAW_CHOI_ASSEMBLY','input_sha256':digests,'all_7_bank_all_stage_forward_inverse_costs_match':True,'raw_DATA22_and_private24_separately_counted':True,'private_initial_zero_contract_not_full_private':True,'exact_joint_vs_DATA_only_counterexample':True,'exact_raw_g_inverse_birth_identity':True,'separate_SITE_and_external_collision_guard':True,'stage_orders_and_literal_depths_0_to_4_checked':True,'eta_U_lt':'2^-3230','bank_error_lt':'2^-3227','1260_banks_error_lt':'2^-3216','full_R46_word_enumerated':False,'physical_C_closed':False,'GR_closed':False}
(P/'FULL_CHOI_INDEPENDENT_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'banks':7,'exact_joint_vs_DATA_only_counterexample':True}))
