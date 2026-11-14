#!/usr/bin/env python3
"""Lazy actual G/CX/SourceI Julia words with paid literal inverses.

Each source sector is a read-only branch/address/SAM controlled word. Huge
Walsh expansions are streamed term-by-term, never silently treated as an
oracle. Certified k values are supplied by PROPER_LINK_ANGLE_LIBRARY.
"""
from pathlib import Path
from collections import Counter
import importlib.util,sys,json,gzip
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sp=importlib.util.spec_from_file_location('b42_native_boolean',D/'round14/native_boolean.py');nb=importlib.util.module_from_spec(sp);sys.modules[sp.name]=nb;sp.loader.exec_module(nb)
ORDER=(0,2,3,1)
def library(path=None):
 with gzip.open(path or P/'PROPER_LINK_ANGLE_LIBRARY.json.gz','rt') as f:return json.load(f)
def layout(nsam=6):
 assert 0<=nsam<=6
 address=list(range(12));sam=list(range(12,12+nsam));branch=12+nsam;t=branch+1;modes=list(range(t+1,t+5));aux=t+5;port=t+6;spin=[t+7,t+8];old=t+9
 return {'address':address,'SAM':sam,'branch':branch,'julia_flag':t,'modes':modes,'aux_arbitrary':aux,'port':port,'spin':spin,'oldRIGHT_witness':old,'qubits':old+1}
def pairs(i,j):
 between=ORDER[min(ORDER.index(i),ORDER.index(j))+1:max(ORDER.index(i),ORDER.index(j))];rest=[a for a in range(4) if a not in (i,j)]
 for k in range(4):
  x=sum(((k>>u)&1)<<q for u,q in enumerate(rest));sign=(-1)**sum((x>>q)&1 for q in between)
  yield x|(1<<i),x|(1<<j),sign

def selective_terms(controls,pattern,target,k,lay,common_controls=23,reverse=False,inverse_depth=None):
 """Yield exact Walsh native DAG terms in chronological/literal-inverse order."""
 K=len(controls);assert 0<=K<=common_controls and len(pattern)==K and len(set(controls+[target,lay['port'],*lay['spin']]))==K+4
 assert all(x in (0,1) for x in pattern) and k>0
 depth=int(reverse) if inverse_depth is None else inverse_depth;assert depth>=0
 power=k*(1<<(common_controls-K));masks=range((1<<K)-1,-1,-1) if depth%2 else range(1<<K)
 for mask in masks:
  selected=[i for i in range(K) if mask>>i&1];cx=[nb.gate('CX',controls[i],target) for i in selected];sign=(-1)**sum(pattern[i] for i in selected)
  tree=nb.seq(*cx,nb.rotation_power(target,sign*power,lay['port'],tuple(lay['spin'])),*reversed(cx))
  for _ in range(depth):tree=nb.inverse_literal(tree,lay['port'],tuple(lay['spin']))
  yield tree

def sector_controls(lay,entry):
 assert len(entry['SAM_pattern'])==len(lay['SAM'])
 return [*lay['address'],*lay['SAM'],lay['branch']],[(entry['address']>>i)&1 for i in range(len(lay['address']))]+list(entry['SAM_pattern'])+[1]

def commands(lay,entry,family,controlled_x):
 """High-level chronology; no native operation omitted, masks emitted later."""
 if 'family_id' in entry:assert entry['family_id']==family['family']
 controls,pat=sector_controls(lay,entry);modes=lay['modes'];t=lay['julia_flag']
 def lift(rotations,flag,inverse):
  for r in (reversed(rotations) if inverse else rotations):
   i,j=r['i'],r['j'];ps=list(pairs(i,j))
   for a,b,sign in (reversed(ps) if inverse else ps):
    assert ((a>>i)&1)==1 and ((a>>j)&1)==0 and b==a^(1<<i)^(1<<j)
    transformed=a^(1<<j)  # CX(i,j): source is (i,j)=(1,1)
    others=[q for q in range(4) if q!=i]
    cs=controls+[t]+[modes[q] for q in others];vs=pat+[flag]+[(transformed>>q)&1 for q in others]
    # G target bit i is 1 in source: positive desired pair sine requires
    # negative native sine. sign=-1 needs forward, sign=+1 literal inverse.
    yield {'kind':'fock','controls':cs,'pattern':vs,'target':modes[i],'cx_control':modes[i],'cx_target':modes[j],'k':int(r['k']),'inverse_depth':int(sign==1)+int(inverse)}
 yield from lift(family['R'],0,True)
 yield from lift(family['L'],1,True)
 yield {'kind':'X','controls':controls,'pattern':pat,'target':t,'k':int(controlled_x['k']),'phase_k':int(controlled_x['phase']['k'])}
 for b0,b1 in ((0,0),(1,0),(0,1),(1,1)):
  key='00' if b0==b1 else str(b0)+str(b1);r=family['diagonal'][key]
  yield {'kind':'rotation','controls':controls+[modes[0],modes[1]],'pattern':pat+[b0,b1],'target':t,'k':int(r['k']),'reverse':False}
 yield from lift(family['L'],0,False)
 yield from lift(family['R'],1,False)

def emit_command(cmd,lay,common_controls=23,reverse=False):
 p=lay['port'];sp=tuple(lay['spin']);kind=cmd['kind'];depth=int(reverse)+int(cmd.get('inverse_depth',cmd.get('reverse',False)))
 if kind=='fock':
  x=nb.gate('CX',cmd['cx_control'],cmd['cx_target']);yield x
  yield from selective_terms(cmd['controls'],cmd['pattern'],cmd['target'],cmd['k'],lay,common_controls,inverse_depth=depth)
  yield x;return
 if kind=='rotation':
  yield from selective_terms(cmd['controls'],cmd['pattern'],cmd['target'],cmd['k'],lay,common_controls,inverse_depth=depth);return
 assert kind=='X'
 # Phase aux by independently certified pi iff controls and target=1, then rotate target by certified pi/2.
 c=cmd['controls'];b=cmd['pattern'];q=cmd['target'];k=cmd['k'];parts=('rotation','phase') if reverse else ('phase','rotation')
 for part in parts:
  if part=='phase':yield from selective_terms(c+[q],b+[1],lay['aux_arbitrary'],cmd['phase_k'],lay,common_controls,reverse)
  else:yield from selective_terms(c,b,q,k,lay,common_controls,reverse)

def sector_blocks(lay,entry,family,x,common_controls=23,reverse=False):
 """Stream every native DAG term; caller need not materialize 2^23 masks."""
 cmd=list(commands(lay,entry,family,x))
 for x in (reversed(cmd) if reverse else cmd):yield from emit_command(x,lay,common_controls,reverse)

def select_cost(controls,pattern,k,common_controls=23,reverse=False):
 K=len(controls);assert K<=common_controls;number=1<<K;neg=number//2 if any(pattern) else 0;pos=number-neg;power=k*(1<<(common_controls-K))
 c=Counter({'G_other':pos*power,'G_port':neg*power,'CX':K*number+6*neg,'SourceI':4*neg})
 return invert_cost(c) if reverse else c

def invert_cost(c):return Counter({'G_port':c['G_port']+c['G_other'],'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
def command_cost(cmd,common_controls=23,reverse=False):
 kind=cmd['kind'];depth=int(reverse)+int(cmd.get('inverse_depth',cmd.get('reverse',False)));c=cmd['controls'];p=cmd['pattern'];k=cmd['k']
 if kind in ('rotation','fock'):
  out=select_cost(c,p,k,common_controls)
  for _ in range(depth):out=invert_cost(out)
  if kind=='fock':out.update({'CX':2})
  return out
 assert kind=='X';return select_cost(c,p,k,common_controls,reverse)+select_cost(c+[cmd['target']],p+[1],cmd['phase_k'],common_controls,reverse)
def sector_cost(lay,entry,family,x,common_controls=23,reverse=False):
 out=Counter()
 for cmd in commands(lay,entry,family,x):out.update(command_cost(cmd,common_controls,reverse))
 return out

def prefix_compatible_global_layout():
 """Wire binding compatible with A19 Choi prefix; extra work stays spectator."""
 return {'all_SAM':list(range(2688)),'address':list(range(2688,2700)),
         'choi_input':list(range(2700,2705)),'modes':list(range(2705,2709)),
         'julia_flag':2709,'branch':2710,'port':2711,'spin':[2712,2713],
         'aux_arbitrary':2714,'oldRIGHT_witness':2715,'phase_rebit':2716,
         'comparator_scratch':list(range(2717,2739)),'qubits':2739}
def bind_global(global_lay,entry):
 out=dict(global_lay);out['SAM']=[global_lay['all_SAM'][i] for i in entry['SAM_indices']]
 allw=[*out['address'],*out['SAM'],out['branch'],out['julia_flag'],*out['modes'],out['aux_arbitrary'],out['port'],*out['spin'],out['oldRIGHT_witness'],out['phase_rebit'],*out['comparator_scratch']]
 assert len(allw)==len(set(allw));return out
def bank_blocks(bank,lib,global_lay=None,reverse=False):
 """Full proper-link bank SELECT, literal inverse when reverse=True.

One externally chosen bank at a time. Anchor, coframe and padding addresses
are exactly idle here. The source sector list remains coherent and read-only.
"""
 global_lay=global_lay or prefix_compatible_global_layout();entries=lib['catalogue'][bank];families={r['family']:r for r in lib['families']}
 for entry in (reversed(entries) if reverse else entries):
  yield from sector_blocks(bind_global(global_lay,entry),entry,families[entry['family_id']],lib['controlled_X'],reverse=reverse)
