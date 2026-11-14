#!/usr/bin/env python3
"""Same-initial paired endpoint schedule, exact paid identity padding."""
from pathlib import Path
from hashlib import sha256
import json,sys,sympy as s
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');P=Path(__file__).resolve().parent;sys.path.insert(0,str(D/'round30'));import marked_source_schedule as core
nb=core.c.nb;cert=json.loads((P/'FINITE_SAM_ROTATION_CERTIFICATE.json').read_text());nplus=int(cert['rotations']['plus']['power_hex'],16);nminus=int(cert['rotations']['minus']['power_hex'],16);assert nplus>0 and nminus>0
# Five CX identity in chronological convention, all eight arbitrary columns.
word=[(0,1),(1,2),(0,1),(1,2),(0,2)]
for x in range(8):
 y=x
 for a,b in word:
  if y>>a&1:y^=1<<b
 assert y==x
# Every difference, including 1 and 3, has aligned lengths using only
# 2/5-stage identities. Both padding lengths are paid.
def align(a,b):
 if a==b:return 0,0
 if a>b:
  pb,pa=align(b,a);return pa,pb
 delta=b-a
 return {1:(5,4),2:(2,0),3:(5,2)}.get(delta,(delta,0))
def decompose(n):
 assert n>=0
 if n==0:return (0,0)
 b=n%2;assert n-5*b>=0
 return ((n-5*b)//2,b)
for i in range(30):
 for j in range(30):
  x,y=align(i,j);assert i+x==j+y and 2*decompose(x)[0]+5*decompose(x)[1]==x and 2*decompose(y)[0]+5*decompose(y)[1]==y
pp,pm=align(nplus,nminus);assert nplus+pp==nminus+pm
# Both core starts and ends share a stage index. Post padding is inserted
# BEFORE the final positive SAM G, making the real closing g equal on ±.
# All padding acts on three distinct existing live WORK wires.
work=[2692,2693,2694];sam=core.g.namespace()['layout']['SAM'][0];assert len(set(work+[sam]))==4
A=nb.gate('CX',work[0],work[1]);B=nb.gate('CX',work[1],work[2]);C=nb.gate('CX',work[0],work[2]);pair=nb.seq(A,A);five=nb.seq(A,B,A,B,C)
def pad(length):
 a,b=decompose(length);chunks=[]
 if a:chunks.append(nb.repeat(a,pair))
 if b:chunks.append(five)
 return nb.seq(*chunks)
pre_plus=nb.seq(nb.repeat(nplus,nb.gate('G',sam)),pad(pp));pre_minus=nb.seq(nb.repeat(nminus,nb.gate('G',sam)),pad(pm));post_plus=nb.seq(nb.repeat(nminus-1,nb.gate('G',sam)),pad(pm),nb.gate('G',sam));post_minus=nb.seq(nb.repeat(nplus-1,nb.gate('G',sam)),pad(pp),nb.gate('G',sam))
for a,b in ((pre_plus,pre_minus),(post_plus,post_minus)):
 assert sum(nb.counts(a).values())==sum(nb.counts(b).values())
for t in (post_plus,post_minus):assert t['children'][-1]==nb.gate('G',sam)
# Exact central difference of the real diagonal core in one SAM coordinate.
p=(s.sqrt(5)-1)/2;v=s.Matrix([s.sqrt(p),p]);t=s.symbols('t',real=True);R=s.Matrix([[s.cos(t),-s.sin(t)],[s.sin(t),s.cos(t)]]);M=s.diag(s.Rational(3,5),s.Rational(4,5));f=(v.T*R.T*M*R*v)[0];der=s.diff(f,t).subs(t,0);assert s.simplify((f-f.subs(t,-t))-der*s.sin(2*t))==0
paths=[D/'round30/marked_source_schedule.py',P/'FINITE_SAM_ROTATION_CERTIFICATE.json']
out={'status':'PASS_SAME_INITIAL_ALIGNED_ENDPOINT_SCHEDULE','t':'2^-20','endpoint_pre_plus_post_minus':'G^n_plus; core; G^n_minus','endpoint_pre_minus_post_plus':'G^n_minus; core; G^n_plus','same_initial_birth_layout':True,'same_paid_pre_core_stage_count':True,'same_paid_post_core_stage_count':True,'padding_plus_hex':hex(pp),'padding_minus_hex':hex(pm),'padding_plus_2_5_decomposition':[hex(z) for z in decompose(pp)],'padding_minus_2_5_decomposition':[hex(z) for z in decompose(pm)],'five_CX_identity_all_columns':True,'closing_gate_logical':{'op':'G','wires':[sam]},'closing_gate_same_for_both_endpoints':True,'example_rotation_per_endpoint_error_lt':'2^-3299','exact_core_scalar_central_difference':'c_prime(0)*sin(2t)/(2t)','source_mark_transport_or_physical_admission_proved':False,'actual_total_price_or_thermal_difference_proved':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'GR_closed':False}
(P/'SAME_INITIAL_ENDPOINT_SCHEDULE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'padding_difference_bits':abs(nplus-nminus).bit_length(),'closing_g':out['closing_gate_logical']}))
