#!/usr/bin/env python3
"""Parity automaton on finite actual DAGs and generic native templates.

Scope is explicit: it does not certify complete A25 coverage.
"""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round25'));import global_h1 as g
nb=g.nb
# 0 even, 1 pending odd, 2 failure. A non-SourceI while odd fails.
def compose(f,h):return tuple(h[f[i]] for i in range(3))
def power(f,n):
 r=(0,1,2)
 while n:
  if n&1:r=compose(r,f)
  f=compose(f,f);n//=2
 return r
def trans(t):
 op=t['op']
 if op=='seq':
  x=(0,1,2)
  for z in t['children']:x=compose(x,trans(z))
  return x
 if op=='repeat':return power(trans(t['child']),int(t['count']))
 if op=='SourceI':return (1,0,2)
 assert op in ('G','CX'),op
 return (0,2,2)
def state(t):return trans(t)[0]
def inv(t,d):
 for _ in range(d):t=nb.inverse_literal(t,4,(5,6))
 return t
base=[nb.z_word(4,4,(5,6)),nb.z_word(0,4,(5,6)),nb.rotation_power(0,-8,4,(5,6)),nb.boolean_word('X',7,target=0,port=4,spin=(5,6)),nb.boolean_word('H',7,target=0,port=4,spin=(5,6)),nb.boolean_word('CCX',7,control=(0,1),target=2,aux=3,port=4,spin=(5,6))]
for t in base:
 for d in range(4):assert state(inv(t,d))==0
fixtures={'boolean_rotation_templates':len(base)*4}
fair=json.loads((O/'round31/NATIVE_FAIR_BANK.json').read_text());star=json.loads((O/'round37/CAR_USTAR_NATIVE.json').read_text())
for name,t in [('fair_router',fair['router_forward_DAG']),('fair_router_literal_inverse',fair['router_literal_raw_inverse_DAG']),('fair_kernel',nb.seq(*fair['zero_and_kernel_forward']['gates'])),('fair_kernel_literal_inverse',nb.seq(*fair['zero_and_kernel_literal_inverse'])),('CAR_Ustar',star['forward_DAG']),('CAR_Ustar_literal_inverse',star['literal_raw_inverse_DAG'])]:
 assert state(t)==0,name;fixtures[name]='even_runs'
cz=g.report.s.cz.cz_word(0,1,2,(3,4));tree=nb.seq(*(nb.gate(z.op,*z.wires) for z in cz));assert state(tree)==2
out={'status':'PASS_SCOPED_SOURCE_RUN_AUTOMATON','checked_actual_DAGs_and_templates':fixtures,'actual_native_CZ_result':'fails: odd SourceI run','complete_A25_coverage_proved':False,'macro_replacement_compiler_implemented':False,'physical_C_closed':False,'GR_closed':False}
(P/'SCOPED_SOURCE_RUN_AUTOMATON.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
