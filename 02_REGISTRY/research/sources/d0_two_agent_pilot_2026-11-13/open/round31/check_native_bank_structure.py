#!/usr/bin/env python3
"""Independently re-count and invert the saved native fair-bank DAG."""
from pathlib import Path
from collections import Counter
import hashlib,json
import fair_router as fr
P=Path(__file__).resolve().parent;path=P/'NATIVE_FAIR_BANK.json';d=json.loads(path.read_text());q=d['logical_layout'];port=d['port'];spin=d['spin'];old=d['protected_oldRIGHT'];aux=d['aux_arbitrary'];k=int(d['k'])
assert q==fr.layout(28) and len({port,*spin,old,aux})==5 and min(port,*spin,old,aux)>=q['qubits']
e=d['zero_and_kernel_forward'];assert e['blank_wires']==[] and e['old_right']==[old] and e['source_port']==port and e['source_spin']==spin
stages=e['gates'];assert len(stages)==1713
for target in range(143):
 expected=[('CX',[target,port]),('CX',[port,target]),('CX',[target,port]),('SourceI',[port,*spin]),('SourceI',[port,*spin]),('G',[port]),('SourceI',[port,*spin]),('SourceI',[port,*spin]),('CX',[target,port]),('CX',[port,target]),('CX',[target,port])]
 assert [(g['op'],g['wires']) for g in stages[11*target:11*(target+1)]]==expected
kernel=[{'op':op,'wires':list(w)} for a in q['attempts'] for op,*w in fr.parity_kernel(a)];assert stages[1573:]==kernel
# Reconstruct every literal prefix inverse independently from primitive definitions.
def leaf(op,*w):return {'op':op,'wires':list(w)}
def swap(a,b):return [leaf('CX',a,b),leaf('CX',b,a),leaf('CX',a,b)]
src=leaf('SourceI',port,*spin);inv=[]
for g in reversed(stages):
 if g['op']=='CX':inv.append(g)
 elif g['op']=='SourceI':inv.extend([g]*3)
 else:
  assert g['op']=='G';x=g['wires'][0];route=[] if x==port else swap(x,port)
  inv.extend(route+[src,src,leaf('G',port),src,src]+route)
assert inv==d['zero_and_kernel_literal_inverse'] and len(inv)==3989
# Independent recursive native counts and raw adjoint tree shape.
def count(t):
 if t['op']=='seq':
  c=Counter()
  for x in t['children']:c.update(count(x))
  return c
 if t['op']=='repeat':return Counter({x:int(t['count'])*v for x,v in count(t['child']).items()})
 return Counter({t['op']:1})
def seq(*xs):return {'op':'seq','children':list(xs)}
def sw(a,b):return seq(*swap(a,b))
def inverse(t):
 op=t['op']
 if op=='seq':return seq(*(inverse(x) for x in reversed(t['children'])))
 if op=='repeat':return {'op':'repeat','count':t['count'],'child':inverse(t['child'])}
 if op=='CX':return t
 if op=='SourceI':return {'op':'repeat','count':'3','child':t}
 assert op=='G';x=t['wires'][0];core=seq(src,src,{'op':'repeat','count':'1','child':leaf('G',port)},src,src)
 return core if x==port else seq(sw(x,port),core,sw(x,port))
fwd=d['router_forward_DAG'];rev=d['router_literal_raw_inverse_DAG'];assert inverse(fwd)==rev
fc=count(fwd);rc=count(rev);assert dict(fc)=={'G':684*k,'CX':3995,'SourceI':1350} and dict(rc)=={'G':684*k,'CX':2088*k+3995,'SourceI':2736*k+4050}
fullf=fc+Counter(g['op'] for g in stages);fullr=rc+Counter(g['op'] for g in inv)
assert {j:str(fullf[j]) for j in ('G','CX','SourceI')}==d['native_forward_inventory']
assert {j:str(fullr[j]) for j in ('G','CX','SourceI')}==d['native_literal_reverse_inventory']
assert sum(fullf.values())==684*k+7058 and sum(fullr.values())==5508*k+12034
flags={x['C'] for x in q['attempts']};B={x['B'] for x in q['attempts']};leaf_count=0
def audit(t):
 global leaf_count
 if t['op']=='seq':
  for x in t['children']:audit(x)
 elif t['op']=='repeat':audit(t['child'])
 else:
  leaf_count+=1;op=t['op'];w=t['wires'];assert old not in w and not (op=='G' and w[0] in flags|B) and not (op=='CX' and w[-1] in flags|B)
  if op=='SourceI':assert w==[port,*spin]
audit(fwd);assert len(fwd['children'])==228
res={'status':'PASS_INDEPENDENT_NATIVE_FAIR_BANK_STRUCTURE','native_bank_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'RAW_born_v_targets':143,'physical_birth_stage_ledger_emitted':False,'prefix_forward_gates_checked':len(stages),'prefix_literal_inverse_gates_checked':len(inv),
 'symbolic_router_macros':len(fwd['children']),'syntactic_primitive_leaves_audited':leaf_count,'router_literal_inverse_tree_exact':True,'flags_and_B_never_targeted_in_router':True,'protected_oldRIGHT_never_touched':True,
 'full_forward_calls':'684*k+7058','full_literal_inverse_calls':'5508*k+12034','native_giant_DAG_flattened_or_executed':False,'GR_closed':False}
(P/'NATIVE_STRUCTURE_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
