#!/usr/bin/env python3
"""Independently check A16 literal native reversals and full count accounting."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,sys,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sp=D/'round16/source_select.py';cp=D/'round16/SOURCE_SELECT_COMPILATION.json';lp=D/'round16/DYNAMIC_PAIR_LIBRARY.json';hashes={str(p):sha256(p.read_bytes()).hexdigest() for p in [sp,cp,lp]}
spec=importlib.util.spec_from_file_location('b34_count_a16',sp);a=importlib.util.module_from_spec(spec);sys.modules[spec.name]=a;spec.loader.exec_module(a)
comp=json.loads(cp.read_text());lib=json.loads(lp.read_text());assert comp['source_sha256']==hashes[str(sp)]
def gate(op,*w):return {'op':op,'wires':list(w)}
def seq(*c):return {'op':'seq','children':list(c)}
def swap(x,y):return seq(gate('CX',x,y),gate('CX',y,x),gate('CX',x,y))
def g_inverse(q,port,spin):
 z=gate('SourceI',port,*spin);body=seq(z,z,{'op':'repeat','count':'1','child':gate('G',port)},z,z)
 return body if q==port else seq(swap(q,port),body,swap(q,port))
visited=0
def check_inverse(t,u,port,spin):
 global visited;visited+=1;op=t['op']
 if op=='seq':
  assert u['op']=='seq' and len(t['children'])==len(u['children'])
  for x,y in zip(reversed(t['children']),u['children']):check_inverse(x,y,port,spin)
 elif op=='repeat':
  assert u['op']=='repeat' and t['count']==u['count'];check_inverse(t['child'],u['child'],port,spin)
 elif op=='SourceI':assert u=={'op':'repeat','count':'3','child':t}
 elif op=='CX':assert t==u
 elif op=='G':assert u==g_inverse(t['wires'][0],port,spin)
 else:raise AssertionError(op)
def cnt(t,port):
 op=t['op']
 if op=='seq':
  c=Counter()
  for x in t['children']:c.update(cnt(x,port))
  return c
 if op=='repeat':return Counter({k:int(t['count'])*v for k,v in cnt(t['child'],port).items()})
 if op=='G':return Counter({'G_port' if t['wires'][0]==port else 'G_other':1})
 return Counter({op:1})
def normalize(c):return {k:int(c.get(k,0)) for k in ['G_port','G_other','CX','SourceI']}
for name,t in lib['templates'].items():
 port=t['native_layout']['port'];spin=t['native_layout']['spin'];f=t['native_forward_DAG'];r=t['native_literal_reverse_DAG']
 check_inverse(f,r,port,spin)
 assert normalize(cnt(f,port))==normalize(t['native_forward_resources'])
 assert normalize(cnt(r,port))==normalize(t['native_raw_inverse_resources'])
counts=Counter();error=0
for name,walk in comp['walks'].items():
 plan=a.instruction_plan(walk['root']['degree']);logical=Counter(x[0] for x in a.ideal_gates(a.instruction_ir(plan)))
 assert dict(logical)==walk['instruction_logical_counts']
 macros=logical['X']+logical['H']+logical['CCX'];assert macros==walk['instruction_error_macros']
 n=walk['root']['slots']; c=Counter({op:v*n for op,v in logical.items()});c.update({'H':2,'X':1,'CCX':2,'Z':1});assert dict(c)==walk['walk_SELECT_test_logical_counts']
 e=macros*n+2+1+2;assert e==walk['walk_SELECT_test_error_macros'];times=2 if name.startswith('H_f') else 8
 counts.update({op:times*v for op,v in c.items()});error+=times*e
assert dict(counts)==comp['one_report_SELECT_test_logical_counts'] and error==comp['one_report_SELECT_test_approximate_macros']
prev=json.loads((D/'round15/PREPROCESSOR_READY_COMPOSITION.json').read_text())['seven_report_known_approximate_macros']['sum'];combined=prev+7*error
assert combined==comp['seven_report_all_known_approximate_macros'] and comp['seven_report_all_known_error_strictly_below']==f'2^-{4096-combined.bit_length()}'
for p,h in hashes.items():assert sha256(Path(p).read_bytes()).hexdigest()==h
out={'status':'PASS_A16_INDEPENDENT_NATIVE_REVERSE_AND_COUNTS','input_sha256':hashes,'literal_reverse_syntactic_nodes_checked':visited,'pair_templates_checked':[12,22],'one_report_logical_counts':dict(counts),'one_report_error_macros':error,'seven_reports_known_error_macros':combined,'known_error_bound':comp['seven_report_all_known_error_strictly_below'],'basis':'operator norm telescoping conditional on A14 per-macro bound; no full physical word/marks/clock budget','scope':'literal reverse trees and logical counts of actual A16; does not independently prove A14 approximation theorem','GR_closed':False}
Path(__file__).with_name('A16_NATIVE_COUNTS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
