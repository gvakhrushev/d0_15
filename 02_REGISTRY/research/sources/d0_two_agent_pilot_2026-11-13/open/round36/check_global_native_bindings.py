#!/usr/bin/env python3
"""Check concrete A17 native remaps on global A16 walk and B31 banks."""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json,itertools
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');P=D/'round17';source=P/'report_assembly.py';digest=sha256(source.read_bytes()).hexdigest();spec=importlib.util.spec_from_file_location('b36_global_native',source);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
plan=json.loads((P/'GLOBAL_REPORT_PLAN.json').read_text());tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());k=int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k']);bank=json.loads((a.B31/'NATIVE_FAIR_BANK.json').read_text());port=plan['native_port'];spin=tuple(plan['native_spin']);aux=plan['native_aux_arbitrary'];old=plan['protected_oldRIGHT_witness'];checks=0
for walk in (plan['walks'][0],plan['walks'][1],plan['walks'][2],plan['walks'][-1]):
 size=walk['local_wires'];assert [port+i for i in range(5)]==[port,*spin,aux,old]
 def gm(w):return (w if w<8 else walk['private_start']+w-8) if w<size else port+w-size
 assert [gm(i) for i in range(8)]==list(range(8)) and [gm(size+i) for i in range(5)]==[port,*spin,aux,old]
 # Compare actual A16 native blocks mapped by A17 to the very same A15
 # elementary event with independently mapped global wires.
 events=(e['event'] for e in a.s.walk_test_events(walk['root'],tables) if e['kind']=='controller')
 sourceword=itertools.chain.from_iterable(a.s.dispatch.event_word(e,tables) for e in events)
 srcnative=a.s.walk_native_blocks(walk['root'],k)
 for _ in range(32):
  op,*w=next(sourceword);tree=a.remap_native(next(srcnative),gm);glob=[gm(x) for x in w]
  if op=='CX':want=a.s.nb.gate('CX',*glob)
  elif op=='X':want=a.s.nb.boolean_word('X',k,target=glob[0],port=port,spin=spin)
  else:assert op=='CCX';want=a.s.nb.boolean_word('CCX',k,control=glob[:2],target=glob[2],aux=aux,port=port,spin=spin)
  assert tree==want;a.s.nb.validate_schema(tree,plan['native_wire_count_including_oldRIGHT_witness'],port,spin,(old,));checks+=1
# Actual B31 native macro binding at first/interior/last outputs. 148 logical
# local wires include shared special port/spin/aux/oldRIGHT after 143 births.
leaves=0
for j in (0,plan['fair_bank_count']//2,plan['fair_bank_count']-1):
 mapped=[a.fair_bank_wire(plan,j,i) for i in range(148)];assert len(set(mapped))==148 and mapped[84]==a.fair_output(plan,j)
 assert mapped[143:]==[port,*spin,aux,old]
 tree=a.fair_bank_native(plan,j,bank);a.s.nb.validate_schema(tree,plan['native_wire_count_including_oldRIGHT_witness'],port,spin,(old,))
 for leaf in a.s.nb.leaves(tree):assert not set(leaf['wires']).intersection(range(9));leaves+=1
assert sha256(source.read_bytes()).hexdigest()==digest
out={'status':'PASS_GLOBAL_A16_AND_B31_NATIVE_BINDINGS','source_sha256':digest,'walks_sampled':['S1','S2','T1','T8'],'global_A16_native_prefix_blocks_checked':checks,'actual_B31_banks_checked':3,'B31_syntactic_native_leaves_checked':leaves,'all_shared_special_port_spin_aux_mapped_correctly':True,'protected_oldRIGHT_untouched':True,'scope':'sampled lazy native blocks and schema; no full native stream execution or birth admission','GR_closed':False}
Path(__file__).with_name('GLOBAL_NATIVE_BINDINGS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
