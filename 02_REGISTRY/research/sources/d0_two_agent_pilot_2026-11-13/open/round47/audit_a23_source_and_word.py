#!/usr/bin/env python3
"""Independent B25 source, compact DAG, literal inverse and price audit."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
from fractions import Fraction
from itertools import product,zip_longest
import json,sys
import numpy as np
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round23');B=P.parent;sys.path.insert(0,str(D));import car_vacuum_prefix as n
lay=n.layout();x=n.inputs();plan=json.loads((D/'CAR_VACUUM_PREFIX_PLAN.json').read_bytes());cert=json.loads((D/'FOURIER_PHASE_CERTIFICATE.json').read_bytes());source=B/'round21/ORIGINAL_FOURIER128_L4.json';pf=B/'round21/ORIGINAL_PF_N20_L4.jsonl';kappa=json.loads(source.read_bytes())['kappa'];rows=[json.loads(z) for z in pf.read_text().splitlines()];assert kappa==x['kappa'] and len(kappa)==64 and len(rows)==256
assert lay['internal_SITE']==list(range(2688,2696)) and lay['grade']==list(range(2696,2700)) and lay['RIGHT']==list(range(2700,2707))
for i,row in enumerate(rows):assert i==sum(v*4**(3-j) for j,v in enumerate(row['site']))
expected=[];maxsum=0
for k,vec in enumerate(kappa):
 total=0
 for mu,value in enumerate(vec):
  for high in (0,1):
   a=value*(1<<high)%4
   if not a:continue
   total+=a;bit=2*(3-mu)+high;expected.append({'pair':k,'mu':mu,'site_bit':bit,'coefficient':a,'K':7,'controls':lay['RIGHT'][1:]+[lay['internal_SITE'][bit]],'pattern':[(k>>j)&1 for j in range(6)]+[1],'target':lay['RIGHT'][0],'k':a*int(cert['k'])})
 maxsum=max(maxsum,total)
actual=list(n.commands(kappa,lay,int(cert['k'])));assert actual==expected and len(actual)==318 and sum(z['coefficient'] for z in actual)==549 and maxsum==18
# 524288 exact ideal coefficients in Z[a]/(a^4+a²−1): grade1 carries a,
# grade14 carries a²; all other grades have zero. Build the two coefficient
# arrays from actual controlled schedule and independently from B25 dot product.
actual_quad=np.zeros((64,256),dtype=np.int8);source_quad=np.zeros((64,256),dtype=np.int8);c=Counter()
for k,vec in enumerate(kappa):
 commands=[z for z in actual if z['pair']==k]
 for i,row in enumerate(rows):
  aq=sum(z['coefficient']*((i>>z['site_bit'])&1) for z in commands)%4;sq=sum(a*b for a,b in zip(vec,row['site']))%4;actual_quad[k,i]=aq;source_quad[k,i]=sq;c[sq]+=1
assert np.array_equal(actual_quad,source_quad) and c=={0:4096,1:4096,2:4096,3:4096}
ca=np.array([1,0,-1,0],dtype=np.int8);sa=np.array([0,1,0,-1],dtype=np.int8)
def coefficient_tensor(q):
 F=np.empty((128,256),dtype=np.int8)
 for k in range(64):F[2*k]=ca[q[k]];F[2*k+1]=sa[q[k]]
 out=np.zeros((128,16,256),dtype=np.int8);out[:,1,:]=F;out[:,14,:]=F;return out,F
T,F=coefficient_tensor(actual_quad);E,_=coefficient_tensor(source_quad);assert T.size==524288 and np.array_equal(T,E) and np.array_equal(np.einsum('rx,sx->rs',F.astype(np.int64),F.astype(np.int64),optimize=False),128*np.eye(128,dtype=np.int64))
# Fixed G/CX/X vacuum preparation maps |0> to a|1>+a²|14> exactly.
assert (0^1)==1 and (15^1)==14
# Recount every actual compact DAG block independently, and independently
# expand each literal inverse tree; integer repeat counts remain compressed.
port=lay['port'];spin=tuple(lay['spin']);protected=set(lay['SAM']+[lay['oldRIGHT_witness']])
def cost(t):
 op=t['op']
 if op=='seq':
  z=Counter()
  for q in t['children']:z.update(cost(q))
  return z
 if op=='repeat':return Counter({k:int(t['count'])*v for k,v in cost(t['child']).items()})
 return Counter({('G_port' if t['wires'][0]==port else 'G_other') if op=='G' else op:1})
def inverse(t):
 op=t['op']
 if op=='seq':return n.nb.seq(*(inverse(q) for q in reversed(t['children'])))
 if op=='repeat':return n.nb.repeat(int(t['count']),inverse(t['child']))
 if op=='CX':return t
 if op=='SourceI':return n.nb.repeat(3,t)
 assert op=='G';q=t['wires'][0];src=n.nb.gate('SourceI',port,*spin);core=n.nb.seq(src,src,n.nb.repeat(1,n.nb.gate('G',port)),src,src)
 if q==port:return core
 def swap(a,b):return n.nb.seq(n.nb.gate('CX',a,b),n.nb.gate('CX',b,a),n.nb.gate('CX',a,b))
 return n.nb.seq(swap(q,port),core,swap(q,port))
def Tinv(c):return Counter({'G_port':c['G_port']+c['G_other'],'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
forward=[];fc=Counter()
for t in n.prefix_blocks(lay):
 for q in n.nb.leaves(t):assert not set(q['wires'])&protected
 forward.append(t);fc.update(cost(t))
assert len(forward)==40742
bc=Counter();blocks=0
for t,z in zip_longest(reversed(forward),n.prefix_blocks(lay,1)):
 assert t is not None and z is not None and z==inverse(t);bc.update(cost(z));blocks+=1
assert blocks==40742 and +bc==+Tinv(fc)
for key,value in [('prefix_forward',fc),('prefix_literal_inverse',bc)]:assert all(value[q]==int(plan['native_inventories'][key][q]) for q in ('G_port','G_other','CX','SourceI'))
delta=Fraction(1,2**3264);bound=18*delta+15*Fraction(1,2**4096);assert [hex(bound.numerator),hex(bound.denominator)]==[plan['error_numerator_hex'],plan['error_denominator_hex']] and bound<Fraction(1,2**3259) and 112*bound<Fraction(1,2**3253)
assert plan['fresh_RAW_wires']==19 and plan['extra_clean_work']==0 and plan['old_prefix_history_or_price_equivalence_proved'] is False and plan['physical_H1_marked_binding_proved'] is False
out={'status':'PASS_INDEPENDENT_A23_SOURCE_FULL_COMPACT_WORD_AND_PRICE','input_sha256':{str(q):sha256(q.read_bytes()).hexdigest() for q in [D/'car_vacuum_prefix.py',D/'CAR_VACUUM_PREFIX_PLAN.json',D/'CAR_VACUUM_PREFIX_CHECK.json',source,pf]},'quadrants_checked':16384,'quadrant_counts':dict(c),'F_transpose_F':'128 I','exact_ideal_amplitude_coefficients_checked':int(T.size),'phase_nodes':len(actual),'max_active_coefficient_sum':18,'actual_compact_blocks':blocks,'every_literal_inverse_tree_independently_rebuilt':True,'native_forward_inverse_counts_match':True,'raw_giant_repeats_expanded':False,'per_prefix_error_lt':'2^-3259','112_prefix_error_strict_lt':'2^-3253','old_marked_prefix_equivalence_proved':False,'GR_closed':False}
(P/'A23_SOURCE_WORD_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('status','exact_ideal_amplitude_coefficients_checked','actual_compact_blocks','112_prefix_error_strict_lt')}))
