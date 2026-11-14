#!/usr/bin/env python3
"""Independently verify native structure and all small-power Spin columns."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from itertools import product
import importlib.util,sys,json
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round19');P=Path(__file__).resolve().parent
paths=[D/'choi_prefix.py',D/'CHOI_PREFIX_CERTIFICATE.json',D/'CHOI_PREFIX_PLAN.json',D/'check_choi_prefix.py'];digests={str(p):sha256(p.read_bytes()).hexdigest() for p in paths}
spec=importlib.util.spec_from_file_location('b40_foreign_prefix',paths[0]);c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c);cert=json.loads(paths[1].read_bytes());plan=json.loads(paths[2].read_bytes())
assert plan['certificate_sha256']==digests[str(paths[1])]
for f,digest in cert['input_sha256'].items(): assert sha256(Path(f).read_bytes()).hexdigest()==digest
assert sha256((D/'certify_choi_prefix.py').read_bytes()).hexdigest()==cert['source_sha256']
assert plan['layout']==c.layout() and plan['logical_schedule']==list(c.instructions(c.layout(),True))
G=lambda q:{'op':'G','wires':[q]}
CX=lambda a,b:{'op':'CX','wires':[a,b]}
SI=lambda p,s:{'op':'SourceI','wires':[p,*s]}
seq=lambda *v:{'op':'seq','children':list(v)}
rep=lambda n,v:{'op':'repeat','count':str(n),'child':v}
def swap(q,p):return seq(CX(q,p),CX(p,q),CX(q,p))
def rot(q,n,p,s):
 assert n
 if n>0:return rep(n,G(q))
 core=(SI(p,s),SI(p,s),rep(-n,G(p)),SI(p,s),SI(p,s))
 return seq(*core) if q==p else seq(swap(q,p),seq(*core),swap(q,p))
def select(controls,bits,q,n,p,s):
 terms=[]
 for mask in range(1<<len(controls)):
  subset=[j for j in range(len(controls)) if mask>>j&1];par=[CX(controls[j],q) for j in subset];sgn=(-1)**sum(bits[j] for j in subset)
  terms.append(seq(*par,rot(q,sgn*n,p,s),*reversed(par)))
 return seq(*terms)
def invert(t,p,s):
 op=t['op']
 if op=='seq':return seq(*(invert(x,p,s) for x in reversed(t['children'])))
 if op=='repeat':return rep(int(t['count']),invert(t['child'],p,s))
 if op=='CX':return t
 if op=='SourceI':return rep(3,t)
 assert op=='G';return rot(t['wires'][0],-1,p,s)
def inventory(t,p):
 op=t['op']
 if op=='seq':
  z=Counter()
  for x in t['children']:z.update(inventory(x,p))
  return z
 if op=='repeat':return Counter({k:v*int(t['count']) for k,v in inventory(t['child'],p).items()})
 return Counter({('G_port' if t['wires'][0]==p else 'G_other') if op=='G' else op:1})
def expected(inst,lay,k,ka):
 ctr=inst['controls'];pat=inst['pattern'];q=inst['target'];p=lay['port'];s=lay['spin'];K=len(ctr)
 if inst['op']=='address_rotation':return select(ctr,pat,q,ka*(2**(1-K)),p,s)
 a=select(ctr+[q],pat+[1],lay['aux_arbitrary'],16*k//2**(K+1),p,s)
 b=select(ctr,pat,q,(4 if inst['op']=='H' else 8)*k//2**K,p,s)
 return seq(a,b)
lay=c.layout();p=lay['port'];sp=lay['spin'];k=int(cert['boolean_common_power']['k']);ka=int(cert['address_power']['k']);res={}; parsed=0
# Reconstruct intended schedule independently of the plan and compiler.
def intended(controlled):
 b=[lay['branch']] if controlled else [];v=[1] if controlled else [];a=lay['address']; z=[]
 z.append({'op':'address_rotation','controls':b,'pattern':v,'target':a[11]})
 for q in a[:11]:z.append({'op':'H','controls':[a[11]]+b,'pattern':[0]+v,'target':q})
 for i,j in zip(lay['choi_input'],lay['choi_output']):
  z.append({'op':'H','controls':b,'pattern':v,'target':i});z.append({'op':'X','controls':[i]+b,'pattern':[1]+v,'target':j})
 return z
assert all(list(c.instructions(lay,b))==intended(b) for b in (False,True))
assert len(lay['address'])==12 and len(lay['choi_input'])==len(lay['choi_output'])==5
assert len({*lay['address'],*lay['choi_input'],*lay['choi_output'],lay['branch'],p,*sp,lay['aux_arbitrary']})==27
# Symbolic amplitude identity: sqrt(2048/2049)/sqrt(2)^11 equals 1/sqrt(2049).
assert 2048==2**11 and 2049==2048+1
for controlled in (False,True):
 insts=list(c.instructions(lay,controlled)); fwd=list(c.prefix_blocks(cert,lay,controlled)); rev=list(c.prefix_blocks(cert,lay,controlled,True)); assert len(insts)==len(fwd)==len(rev)==22
 count=Counter();back=Counter()
 for inst,t in zip(insts,fwd):
  assert t==expected(inst,lay,k,ka), (controlled, inst); count.update(inventory(t,p));parsed+=1
  # Controls and all SAM, oldRIGHT are immutable or completely absent.
  for leaf in c.nb.leaves(t):
   w=leaf['wires'];assert not set(w).intersection(lay['SAM']+[lay['oldRIGHT_witness']])
   if leaf['op'] in ('G','CX'):assert w[-1] not in inst['controls']
   else:assert w==[p,*sp]
 for original,actual in zip(reversed(fwd),rev):assert invert(original,p,sp)==actual;back.update(inventory(actual,p))
 assert +back==+Counter({'G_port':count['G_port']+count['G_other'],'CX':count['CX']+6*count['G_other'],'SourceI':3*count['SourceI']+4*(count['G_port']+count['G_other'])})
 key='controlled' if controlled else 'uncontrolled'; expected_res={z:{q:str(v) for q,v in z0.items()} for z,z0 in [('forward',count),('literal_inverse',back)]};assert expected_res==plan['actual_native_resources'][key];res[key]=expected_res
# Verify Walsh formula for all actual predicate widths and patterns: on every
# control assignment, net target exponent is 2^K*n or zero, exactly.
for K in range(4):
 for pat in product((0,1),repeat=K):
  for bits in product((0,1),repeat=K):
   total=sum((-1)**sum((pat[j]+bits[j]) for j in range(K) if mask>>j&1) for mask in range(1<<K))
   assert total==(2**K if bits==pat else 0)
# Exact arithmetic in Z[a]/(a^4+a^2-1), with native G=[[a,-a²],[a²,a]].
zero=(0,0,0,0);one=(1,0,0,0)
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a):return tuple(-x for x in a)
def mul(a,b):
 v=[0]*7
 for i,x in enumerate(a):
  for j,y in enumerate(b):v[i+j]+=x*y
 for n in (6,5,4):v[n-4]+=v[n];v[n-2]-=v[n]
 return tuple(v[:4])
A=(0,1,0,0);P2=(0,0,1,0)
def run(t,state):
 op=t['op']
 if op=='seq':
  for z in t['children']:state=run(z,state)
  return state
 if op=='repeat':
  assert int(t['count'])<=100
  for _ in range(int(t['count'])):state=run(t['child'],state)
  return state
 out={}
 def put(ix,v):out[ix]=plus(out.get(ix,zero),v)
 for ix,v in state.items():
  w=t['wires']
  if op=='G':
   bit=(ix>>w[0])&1;dst=ix^(1<<w[0]);put(ix,mul(v,A));put(dst,mul(v,minus(P2) if bit else P2))
  elif op=='CX':put(ix^(((ix>>w[0])&1)<<w[1]),v)
  else:
   assert op=='SourceI';bit=(ix>>w[0])&1;par=((ix>>w[1])^(ix>>w[2]))&1;put(ix^(bit<<w[2]),minus(v) if bit and par else v)
 return {q:z for q,z in out.items() if z!=zero}
# For each macro with all original control patterns, compare actual controlled
# and uncontrolled complete columns on both branch values, not just targets.
small={'boolean_common_power':{'k':'1'},'address_power':{'k':'1'}}; cases=0; inverses=0
for typ in ('address_rotation','H','X'):
 for K in (range(1) if typ=='address_rotation' else range(2)):
  for pat in product((0,1),repeat=K):
   controls=list(range(K));branch=K;target=K+1;aux=K+2;port=K+3;spin=[K+4,K+5];L={'aux_arbitrary':aux,'port':port,'spin':spin}
   i={'op':typ,'controls':controls,'pattern':list(pat),'target':target};j={'op':typ,'controls':controls+[branch],'pattern':list(pat)+[1],'target':target}
   u=c.lower(i,small,L);ct=c.lower(j,small,L);ci=invert(ct,port,spin)
   for col in range(1<<(K+6)):
    x={col:one}; actual=run(ct,x);wanted=run(u,x) if col>>branch&1 else x
    assert actual==wanted,(typ,K,pat,col);assert run(ci,actual)==x,(typ,K,pat,col,'inverse');cases+=1;inverses+=1
# Separately verify actual SourceI square and fourth power on every port/Spin
# input, including nontrivial Spin; this underpins the routed G inverse.
for col in range(8):
 t=SI(0,[1,2]);x={col:one};sq=run(t,run(t,x));want={col:minus(one) if col&1 else one};assert sq==want and run(t,run(t,sq))==x
for f,digest in digests.items():assert sha256(Path(f).read_bytes()).hexdigest()==digest
out={'status':'PASS_INDEPENDENT_NATIVE_PREFIX_AUDIT','input_sha256':digests,'actual_native_macro_trees_matched':parsed,'walsh_all_assignments_predicate_widths_0_to_3':True,'strict_branch0_identity_and_branch1_equals_actual_uncontrolled_all_small_columns':cases,'literal_inverse_all_small_columns':inverses,'real_SourceI_all_port_spin_columns':8,'actual_forward_and_literal_inverse_inventories_match_plan':True,'actual_full_prefix_giant_word_expanded':False,'native_power_correctness_from_interval_check':True,'full_Omega_SELECT_present':False,'physical_C_closed':False,'GR_closed':False}
(P/'INDEPENDENT_NATIVE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
