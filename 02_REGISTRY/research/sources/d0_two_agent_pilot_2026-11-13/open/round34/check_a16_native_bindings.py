#!/usr/bin/env python3
"""Sample actual global native blocks and source-copy target invariants."""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json,itertools
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');p=D/'round16/source_select.py';digest=sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('b34_bind_a16',p);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
nb=a.nb;tables=json.loads((D/'round15/SOURCE_DISPATCH_TABLES.json').read_text());comp=json.loads((D/'round15/SOURCE_DISPATCH_COMPILATION.json').read_text());k=int(json.loads((D/'round14/NATIVE_BOOLEAN_ANGLE.json').read_text())['k']);out_roots={}
for name,root in tables['roots'].items():
 size=comp['walks'][name]['walk_logical_wire_count']+a.instruction_plan(root['degree'])['wire_count']-65
 port=size;spin=(size+1,size+2);aux=size+3;old=size+4
 # Compare actual first emitted macros against separate A15 event input and
 # independent A14 direct constructors, including actual global port indices.
 events=(e['event'] for e in a.walk_test_events(name,tables) if e['kind']=='controller')
 logical=itertools.chain.from_iterable(a.dispatch.event_word(e,tables) for e in events);native=a.walk_native_blocks(name,k);ops=[]
 for _ in range(64):
  op,*w=next(logical);block=next(native)
  if op=='CX':expected=nb.gate('CX',*w)
  elif op=='X':expected=nb.boolean_word('X',k,target=w[0],port=port,spin=spin)
  else:
   assert op=='CCX';expected=nb.boolean_word('CCX',k,control=w[:2],target=w[2],aux=aux,port=port,spin=spin)
  assert block==expected;nb.validate_schema(block,size+5,port,spin,(old,));ops.append(op)
 out_roots[name]={'logical_wires':size,'port':port,'checked_global_first_blocks':len(ops),'first_block_types':sorted(set(ops))}
# Check actual selected instruction native macros with all local copy banks and
# protected selectors. This is not full flattened walk simulation.
checked=0;nodes=0
for degree in [(82,0),(2,2)]:
 plan=a.instruction_plan(degree);q=plan['layout'];size=plan['wire_count'];port=size;spin=(size+1,size+2);aux=size+3;old=size+4
 immutable=set(q['negative']+q['leaf']+q['coffset']+q['qoffset']+q['kind']+q['a']+q['b']+q['h']+q['delta_choi']+q['delta_car']+sum(q['CAR_RIGHT'],[]))
 calls=plan['copy_calls']; picks={0,len(calls)-1,len(calls)//2}
 for i in sorted(picks):
  call=calls[i];tree=a.lower(call['IR'],k,port,spin,aux);nb.validate_schema(tree,size+5,port,spin,(old,))
  for g in nb.leaves(tree):
   op=g['op'];w=g['wires'];nodes+=1
   assert old not in w
   if op in ('G','CX'):assert w[-1] not in immutable
   if op=='SourceI':assert w==[port,*spin]
  checked+=1
assert sha256(p.read_bytes()).hexdigest()==digest
out={'status':'PASS_A16_NATIVE_GLOBAL_PREFIX_AND_SELECTED_BINDINGS','source_sha256':digest,'walk_roots':out_roots,'selected_native_copy_blocks_checked':checked,'selected_native_syntactic_primitive_leaves_checked':nodes,'source_record_and_delta_not_targeted_by_native_primitives':True,'protected_oldRIGHT_not_touched':True,'scope':'first 64 actual lazy native blocks of each walk plus selected logical-copy lowering samples; not the full astronomical walk or all marks','GR_closed':False}
Path(__file__).with_name('A16_NATIVE_BINDINGS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
