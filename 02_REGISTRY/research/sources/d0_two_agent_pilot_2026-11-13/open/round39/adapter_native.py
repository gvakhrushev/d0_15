#!/usr/bin/env python3
"""Lazy native fixed-point adapter, parameterized by an actual controlled Ω DAG.

No unknown Ω oracle is emitted: the caller supplies a native controlled-loader
DAG and proves its anchor-isometry and read-only external-control contract.
Every inverse in the lazy grammar is a literal primitive-by-primitive inverse.
"""
from pathlib import Path
from collections import Counter
import importlib.util,sys,json
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
def load(n,p):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);sys.modules[n]=m;spec.loader.exec_module(m);return m
s=load('b39_a16',D/'round16/source_select.py');nb=s.nb;logic=s.logic

def layout(w=0,external_count=0):
 assert type(w) is int and 0<=w<=32768 and type(external_count) is int and external_count>=0
 branch=0;rebit=1;data=list(range(2,24));private=list(range(24,24+w));cursor=24+w;external=list(range(cursor,cursor+external_count));cursor+=external_count
 N=23+w;flag=cursor;work=list(range(cursor+1,cursor+N-1));port=cursor+N-1;spin=[port+1,port+2];aux=port+3;old=port+4
 assert len(work)==N-2
 return {'branch':branch,'rebit':rebit,'data':data,'V_private':private,'external':external,'start_controls':[branch]+data+private,
         'predicate_flag':flag,'predicate_work':work,'port':port,'spin':spin,'aux_arbitrary':aux,'oldRIGHT_witness':old,'qubits':port+5}

def fixed(lay,phase_k,correction_l,h_k):
 branch=lay['branch'];h=lay['rebit'];port=lay['port'];spin=tuple(lay['spin']);N=len(lay['start_controls'])
 assert h not in lay['start_controls'] and len(set(lay['start_controls']))==N and len(lay['predicate_work'])==N-2
 H=nb.boolean_word('H',h_k,target=branch,port=port,spin=spin)
 good=nb.selective_rotation([branch],[0],h,phase_k,port,spin)
 flag_phase=nb.selective_rotation([lay['predicate_flag']],[1],h,phase_k,port,spin)
 Flogical=list(logic.pattern_gate(lay['start_controls'],0,lay['predicate_flag'],lay['predicate_work']))
 Fblocks=[s.lower(s.gate(op,*wire),h_k,port,spin,lay['aux_arbitrary']) for op,*wire in Flogical]
 # Chronological F, controlled phase, literal inverse F: no hidden cleanup.
 start=Fblocks+[flag_phase]+[nb.inverse_literal(x,port,spin) for x in reversed(Fblocks)]
 correction=nb.repeat(correction_l,nb.gate('G',h))
 return {'H':H,'good':[good],'start':start,'correction':correction,'Flogical':Flogical}

def validate_loader(lay,tree,sam_controls=(),untouched_external=()):
 """Check declared namespace/targets; semantic anchor bound remains external."""
 nb.validate_schema(tree,lay['qubits'],lay['port'],tuple(lay['spin']),(lay['oldRIGHT_witness'],))
 forbidden={lay['rebit'],lay['predicate_flag'],*lay['predicate_work'],lay['oldRIGHT_witness'],*untouched_external}
 readonly={lay['branch'],*sam_controls}
 assert not forbidden.intersection(readonly)
 for leaf in nb.leaves(tree):
  assert not forbidden.intersection(leaf['wires'])
  if leaf['op'] in ('G','CX'):assert leaf['wires'][-1] not in readonly
  elif leaf['op']=='SourceI':assert not readonly.intersection(leaf['wires'])
 return True


def _inverted_n_times(tree,n,port,spin):
 for _ in range(n):tree=nb.inverse_literal(tree,port,spin)
 return tree

def adapter_blocks(lay,controlled_loader,phase_k,correction_l,h_k,levels=8,reverse=False,
                   sam_controls=(),untouched_external=()):
 """Yield real native DAG blocks; no giant flatten or inverse cancellation.

 Each nested inverse is applied literally, even if two inverses compose
 mathematically to the original operation. Caller validates controlled_loader's
 strict branch semantics and uniform source-isometry bound. SAM and untouched
 external wires must be explicitly supplied by the caller for validation.
 """
 assert 0<=levels<=8
 validate_loader(lay,controlled_loader,sam_controls,untouched_external)
 fixedparts=fixed(lay,phase_k,correction_l,h_k);port=lay['port'];spin=tuple(lay['spin']);H=fixedparts['H'];good=fixedparts['good'];start=fixedparts['start']
 def leaf(blocks,depth):
  for tree in (reversed(blocks) if depth%2 else blocks):yield _inverted_n_times(tree,depth,port,spin)
 def walk(n,depth):
  if n==0:
   yield from leaf([H,controlled_loader,H],depth);return
  children=[('A',0),('G',0),('A',1),('S',0),('A',0)]
  for kind,extra in (reversed(children) if depth%2 else children):
   if kind=='A':yield from walk(n-1,depth+extra)
   elif kind=='G':yield from leaf(good,depth)
   else:yield from leaf(start,depth)
 correction=fixedparts['correction']
 if reverse:
  yield from leaf([correction],1);yield from walk(levels,1)
 else:
  yield from walk(levels,0);yield correction

def native_counts(tree,port):
 op=tree['op']
 if op=='seq':
  c=Counter()
  for v in tree['children']:c.update(native_counts(v,port))
  return c
 if op=='repeat':return Counter({x:int(tree['count'])*n for x,n in native_counts(tree['child'],port).items()})
 if op=='G':return Counter({'G_port' if tree['wires'][0]==port else 'G_other':1})
 assert op in ('CX','SourceI');return Counter({op:1})
def raw_inverse_counts(c):
 return Counter({'G_port':c['G_port']+c['G_other'],'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
def native_budget(w,phase_k,correction_l,h_k,cv_counts=None,levels=8):
 """Exact paid inventory by linear recurrence, including inverses of inverses."""
 N=23+w;X=Counter({'G_other':4*h_k,'CX':6,'SourceI':2});CCX=Counter({'G_port':6*h_k,'G_other':6*h_k,'CX':68,'SourceI':24});CX=Counter({'CX':1});H=Counter({'G_other':2*h_k,'CX':6,'SourceI':2})
 def mul(c,n):return Counter({k:v*n for k,v in c.items() if v*n})
 F=mul(X,2)+mul(CX,2*N-1)+mul(CCX,2*N-3)
 flagphase=Counter({'G_port':phase_k,'G_other':phase_k,'CX':8,'SourceI':4});good=Counter({'G_other':2*phase_k,'CX':2})
 start=F+flagphase+raw_inverse_counts(F);R=mul(H,2)+Counter(cv_counts or {})
 for _ in range(levels):R=mul(R,2)+raw_inverse_counts(R)+good+start
 R.update({'G_other':correction_l})
 return R,raw_inverse_counts(R)
