#!/usr/bin/env python3
"""Actual lazy native SITE writer: RAW inverse, R0, U†, R0, U."""
from pathlib import Path
from collections import Counter
import importlib.util,sys,json,gzip
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
s=importlib.util.spec_from_file_location('b45_native_boolean',D/'round14/native_boolean.py');nb=importlib.util.module_from_spec(s);sys.modules[s.name]=nb;s.loader.exec_module(nb)
def library():
 with gzip.open(P/'SITE_ANGLE_LIBRARY.json.gz','rt') as f:return json.load(f)
def layout():return {'SITE':list(range(8)),'aux_arbitrary':8,'port':9,'spin':[10,11],'oldRIGHT_witness':12,'qubits':13}
def validate(lay):
 w=[*lay['SITE'],lay['aux_arbitrary'],lay['port'],*lay['spin'],lay['oldRIGHT_witness'],*lay.get('protected_external',[])];assert len(lay['SITE'])==8 and len(w)==len(set(w)) and all(type(q) is int and 0<=q<lay['qubits'] for q in w)
def inverse(t,depth,lay):
 for _ in range(depth):t=nb.inverse_literal(t,lay['port'],tuple(lay['spin']))
 return t
def commands(lib,lay):
 validate(lay);out=[]
 for node in lib['tree_nodes']:
  ctr=[lay['SITE'][i] for i in node['control_bits']];target=lay['SITE'][node['target_bit']];out.append({'controls':ctr,'pattern':node['pattern'],'target':target,'k':int(lib['angles'][node['angle_id']]['k']),'level':node['level'],'prefix':node['prefix']})
 return out
def phase_command(lib,lay):return {'controls':list(lay['SITE']),'pattern':[0]*8,'target':lay['aux_arbitrary'],'k':int(lib['reflection_phase']['k'])}
def selective_blocks(cmd,lay,depth=0,control_power=8):
 assert type(depth) is int and depth>=0;ctr=cmd['controls'];pat=cmd['pattern'];K=len(ctr);assert K<=control_power and len(ctr)==len(set(ctr))==len(pat) and cmd['target'] not in ctr
 k=cmd['k']*(1<<(control_power-K));masks=range((1<<K)-1,-1,-1) if depth%2 else range(1<<K)
 for mask in masks:
  subset=[j for j in range(K) if mask>>j&1];cx=[nb.gate('CX',ctr[j],cmd['target']) for j in subset];sign=(-1)**sum(pat[j] for j in subset)
  tree=nb.seq(*cx,nb.rotation_power(cmd['target'],sign*k,lay['port'],tuple(lay['spin'])),*reversed(cx))
  yield inverse(tree,depth,lay)
def gray_phase_blocks(cmd,lay,depth=0,control_power=8):
 """All-zero phase using a closed Gray cycle; exact literal d-fold inverse."""
 ctr=cmd['controls'];K=len(ctr);assert 1<=K<=control_power and cmd['pattern']==[0]*K and cmd['target'] not in ctr
 N=1<<K;k=cmd['k']*(1<<(control_power-K));idx=range(2*N-1,-1,-1) if depth%2 else range(2*N)
 for pos in idx:
  if pos%2==0:t=nb.repeat(k,nb.gate('G',cmd['target']))
  else:
   step=(pos+1)//2;bit=K-1 if step==N else (step&-step).bit_length()-1;t=nb.gate('CX',ctr[bit],cmd['target'])
  yield inverse(t,depth,lay)
def gray_phase_cost(cmd,depth=0,control_power=8):
 K=len(cmd['controls']);N=1<<K;k=cmd['k']*(1<<(control_power-K));c=Counter({'G_other':N*k,'CX':N})
 for _ in range(depth):c=inv(c)
 return c
def tree_blocks(lib,lay,depth=0):
 cmd=commands(lib,lay)
 for z in (reversed(cmd) if depth%2 else cmd):yield from selective_blocks(z,lay,depth)
def site_blocks(lib,lay=None,depth=0):
 """Entire actual writer or d-fold literal inverse, in chronological blocks."""
 lay=lay or layout();validate(lay);groups=['RAW','R','Uinv','R','U']
 for g in (reversed(groups) if depth%2 else groups):
  if g=='RAW':
   raw=[nb.rotation_power(q,-1,lay['port'],tuple(lay['spin'])) for q in lay['SITE']]
   for t in (reversed(raw) if depth%2 else raw):yield inverse(t,depth,lay)
  elif g=='R':yield from gray_phase_blocks(phase_command(lib,lay),lay,depth)
  else:yield from tree_blocks(lib,lay,depth+int(g=='Uinv'))
def inv(c):return Counter({'G_port':c['G_port']+c['G_other'],'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
def cost(cmd,depth=0,control_power=8):
 K=len(cmd['controls']);N=1<<K;neg=N//2 if any(cmd['pattern']) else 0;k=cmd['k']*(1<<(control_power-K));c=Counter({'G_port':neg*k,'G_other':(N-neg)*k,'CX':K*N+6*neg,'SourceI':4*neg})
 for _ in range(depth):c=inv(c)
 return c
def inventory(lib,lay=None):
 lay=lay or layout();validate(lay);u=Counter()
 for z in commands(lib,lay):u.update(cost(z))
 r=gray_phase_cost(phase_command(lib,lay));raw=Counter({'G_port':8,'CX':48,'SourceI':32});site=raw+r+inv(u)+r+u
 return {'U_forward':u,'U_literal_inverse':inv(u),'RAW_inverse8':raw,'R_zero':r,'SITE_forward':site,'SITE_literal_inverse':inv(site)}


def bind_to_choi(choi,site_wires,qubits,extra_readonly=()):
 """Use A21 port/Spin/aux while reserving all loader/adapter external wires."""
 protected=[*choi['SAM'],*choi['address'],*choi['choi_input'],*choi['choi_output'],choi['branch'],choi['phase_rebit'],*choi['comparator_scratch'],*extra_readonly]
 out={'SITE':list(site_wires),'aux_arbitrary':choi['aux_arbitrary'],'port':choi['port'],'spin':choi['spin'],'oldRIGHT_witness':choi['oldRIGHT_witness'],'qubits':qubits,'protected_external':protected}
 validate(out);return out
