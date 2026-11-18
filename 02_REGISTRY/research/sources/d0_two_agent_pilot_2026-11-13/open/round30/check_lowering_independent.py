#!/usr/bin/env python3
"""Independent arithmetic and wire invariant audit of A14 A13-lowering data."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,sys,json,hashlib
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
A13=D/'round13';A14=D/'round14';read=lambda x:json.loads(x.read_text())
angle=read(A14/'NATIVE_BOOLEAN_ANGLE.json');k=int(angle['k']);library=read(A14/'NATIVE_BOOLEAN_LIBRARY.json');lower=read(A14/'NATIVE_SELECTOR_LOWERING.json')
assert int(library['k'])==int(lower['k'])==k and k.bit_length()==4111
# Closed inventory formulas independently expanded from parity Walsh terms.
forward={'X':{'G':4*k,'CX':6,'SourceI':2},'H':{'G':2*k,'CX':6,'SourceI':2},'CCX':{'G':12*k,'CX':68,'SourceI':24}}
reverse={'X':{'G':4*k,'CX':24*k+6,'SourceI':16*k+6},'H':{'G':2*k,'CX':12*k+6,'SourceI':8*k+6},'CCX':{'G':12*k,'CX':36*k+68,'SourceI':48*k+72}}
for name in ('X','H','CCX'):
 t=library['templates'][name];assert {o:int(v) for o,v in t['forward_inventory'].items()}==forward[name]
 assert {o:int(v) for o,v in t['literal_raw_inverse_inventory'].items()}==reverse[name]
 assert sum(forward[name].values())==({'X':4*k+8,'H':2*k+8,'CCX':12*k+92}[name])
 assert sum(reverse[name].values())==({'X':44*k+12,'H':22*k+12,'CCX':96*k+140}[name])
# Recursively re-count the actual saved DAG rather than trust its inventory.
def inventory(tree):
 op=tree['op']
 if op=='seq':
  acc={'G':0,'CX':0,'SourceI':0}
  for child in tree['children']:
   c=inventory(child)
   for j in acc:acc[j]+=c[j]
  return acc
 if op=='repeat':
  n=int(tree['count']);assert n>0 and str(n)==tree['count'];return {j:n*v for j,v in inventory(tree['child']).items()}
 assert op in ('G','CX','SourceI');return {j:int(op==j) for j in ('G','CX','SourceI')}
for name in forward:
 t=library['templates'][name];assert inventory(t['forward'])==forward[name] and inventory(t['literal_raw_inverse'])==reverse[name]
# Independently reconstruct the literal raw inverse *tree* from the actual
# forward leaves. The giant repeats stay symbolic, never shortened.
def leaf(op,*w):return {'op':op,'wires':list(w)}
def seq(*xs):return {'op':'seq','children':list(xs)}
def sw(a,b):return seq(leaf('CX',a,b),leaf('CX',b,a),leaf('CX',a,b))
def exact_inverse(tree):
 op=tree['op']
 if op=='seq':return seq(*(exact_inverse(x) for x in reversed(tree['children'])))
 if op=='repeat':return {'op':'repeat','count':tree['count'],'child':exact_inverse(tree['child'])}
 if op=='CX':return tree
 if op=='SourceI':return {'op':'repeat','count':'3','child':tree}
 assert op=='G';q=tree['wires'][0];src=leaf('SourceI',4,5,6)
 core=seq(src,src,{'op':'repeat','count':'1','child':leaf('G',4)},src,src)
 return core if q==4 else seq(sw(q,4),core,sw(q,4))
for name in forward:
 t=library['templates'][name];assert exact_inverse(t['forward'])==t['literal_raw_inverse']
# Native operand audit at each syntactic leaf of canonical templates.
spec=importlib.util.spec_from_file_location('a14_nb_review',A14/'native_boolean.py');nb=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nb;spec.loader.exec_module(nb)
leaf_counts={}
for name in ('X','H','CCX'):
 t=library['templates'][name];leafs=list(nb.leaves(t['forward']));leaf_counts[name]=len(leafs)
 for g in leafs:
  w=g['wires'];assert len(set(w))==len(w) and not set(w)&{7}
  if g['op']=='SourceI':assert w==[4,5,6]
  elif g['op']=='CX':assert not set(w)&{5,6} and w[-1] not in (0,1)
  else:assert g['op']=='G' and w[0] not in (0,1,5,6,7)
# 5 actual A13 circuits: recompute totals and exact logical error bounds.
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();results=[]
for row in lower['circuits']:
 path=A13/row['logical_circuit_file'];obj=read(path);obj=obj[row['circuit_dictionary_key']] if row['circuit_dictionary_key'] else obj
 assert row['logical_circuit_sha256']==sha(path) and row['logical_gate_counts']==obj['terminal_gate_counts']
 c=obj['terminal_gate_counts'];size=obj['wire_count'];assert row['native_wire_count']==size+5
 assert (row['port'],row['spin'],row['arbitrary_aux'],row['protected_oldRIGHT'])==(size,[size+1,size+2],size+3,size+4)
 f={'G':0,'CX':c.get('CX',0),'SourceI':0};v=dict(f)
 for name in ('X','CCX'):
  for op in f:f[op]+=c.get(name,0)*forward[name][op];v[op]+=c.get(name,0)*reverse[name][op]
 assert {op:int(z) for op,z in row['native_forward_inventory'].items()}==f
 assert {op:int(z) for op,z in row['native_literal_raw_reverse_inventory'].items()}==v
 N=c.get('X',0)+c.get('CCX',0);assert F(row['error_upper'])==F(N,2**4096)
 assert row['declared_inputs_read_only_at_every_primitive'] and row['oldRIGHT_untouched_at_every_primitive']
 results.append({'circuit':row['logical_circuit_file'],'key':row['circuit_dictionary_key'],'logical_occurrences':sum(c.values()),'approximate_occurrences':N,'native_wire_count':size+5,'inventory_checked':True})
assert len(results)==5
known=7*(3776997052+9403481772);assert known==92263351768 and known<2**37
assert int(lower['known_seven_report_approximate_macro_occurrences'])==known and F(lower['known_seven_report_error_upper'])==F(known,2**4096)
assert F(known,2**4096)<F(1,2**4059) and F(1,2**4096)<F(1,2**3243)
# SHA binding of immutable loaded artifacts and owner interval source.
files=[A14/x for x in ['NATIVE_BOOLEAN_ANGLE.json','NATIVE_BOOLEAN_LIBRARY.json','NATIVE_SELECTOR_LOWERING.json','native_boolean.py','lower_native_selectors.py']]+[A13/x for x in ['reversible_selectors.py','CIRCUIT_COMPILATION.json']]
assert lower['native_library_sha256']==sha(A14/'NATIVE_BOOLEAN_LIBRARY.json') and lower['logical_iterator_sha256']==sha(A13/'reversible_selectors.py')
res={'status':'PASS_INDEPENDENT_LOWERING_COUNTS_AND_WIRING','input_sha256':{str(f):sha(f) for f in files},'k_binary_length':k.bit_length(),
 'native_forward_and_literal_raw_reverse_formula_checked':True,'saved_DAG_independent_recount':True,'literal_inverse_tree_reconstructed':True,'syntactic_leaves_checked':leaf_counts,'logical_controls_not_native_targets':True,'oldRIGHT_not_addressed':True,
 'circuits':results,'seven_report_approximate_occurrences':known,'seven_report_error_strict_lt':'2^-4059','per_macro_tolerance':'2^-4096',
 'required_for_full_claim':['all remaining logical source-DAG dispatch, loaders, marks and quantum payload routing','actual births and full clock','target full alpha and physical C'],
 'giant_native_word_flattened_or_executed':False,'GR_closed':False}
(P/'LOWERING_REVIEW.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:res[k] for k in ['status','k_binary_length','saved_DAG_independent_recount','seven_report_approximate_occurrences','seven_report_error_strict_lt']}))
