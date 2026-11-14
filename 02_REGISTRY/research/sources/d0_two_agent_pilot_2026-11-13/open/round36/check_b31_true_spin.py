#!/usr/bin/env python3
"""Small-k numerical native router/inverse replay on arbitrary full columns."""
from pathlib import Path
import importlib.util,sys,random,math,json
sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'round31'))
import fair_router as fr
P=Path(__file__).resolve().parent;A14=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round14')
spec=importlib.util.spec_from_file_location('b31_small_nb',A14/'native_boolean.py');nb=importlib.util.module_from_spec(spec);sys.modules[spec.name]=nb;spec.loader.exec_module(nb)
p=(math.sqrt(5)-1)/2;a=math.sqrt(p)
def run(word,state,N,port,spin):
 for g in word:
  op=g['op'];w=g['wires'];out={}
  for i,v in state.items():
   if op=='G':
    mask=1<<(N-1-w[0]);out[i]=out.get(i,0)+a*v;out[i^mask]=out.get(i^mask,0)+(-p if i&mask else p)*v
   elif op=='CX':
    if (i>>(N-1-w[0]))&1:i^=1<<(N-1-w[1])
    out[i]=out.get(i,0)+v
   else:
    assert op=='SourceI' and w==[port,*spin]
    if (i>>(N-1-port))&1:
     if ((i>>(N-1-spin[0]))^(i>>(N-1-spin[1])))&1:v=-v
     i^=1<<(N-1-spin[1])
    out[i]=out.get(i,0)+v
  state={i:v for i,v in out.items() if abs(v)>1e-14}
 return state
rng=random.Random(3113);checks=0;maxerr=0.;reports=[]
for K in (1,2):
 q,logical=fr.router(K);port=q['qubits'];spin=(port+1,port+2);aux=port+3;old=port+4;N=old+1;macros=[]
 for op,*w in logical:
  if op=='CX':t=nb.gate('CX',*w)
  elif op=='X':t=nb.boolean_word('X',1,target=w[0],port=port,spin=spin)
  else:t=nb.boolean_word('CCX',1,control=w[:2],target=w[2],aux=aux,port=port,spin=spin)
  macros.append(t)
 tree=nb.seq(*macros);nb.validate_schema(tree,N,port,spin,(old,));inverse=nb.inverse_literal(tree,port,spin)
 forward=list(nb.expand(tree,10000));back=list(nb.expand(inverse,30000))
 for _ in range(16):
  col=rng.randrange(1<<N);state=run(forward,{col:1.0},N,port,spin)
  for i in state:
   assert ((i>>(N-1-old))&1)==((col>>(N-1-old))&1)
  state=run(back,state,N,port,spin)
  err=math.sqrt(sum((v-(1.0 if i==col else 0.0))**2 for i,v in state.items())+(0 if col in state else 1))
  maxerr=max(maxerr,err);assert err<1e-10;checks+=1
 reports.append({'K':K,'qubits':N,'forward_calls':len(forward),'literal_inverse_calls':len(back),'arbitrary_basis_checks':16})
res={'status':'PASS_SMALL_NATIVE_ROUTER_LITERAL_INVERSE','spin_representation':'literal diag(J,-J), both spin bits','scope':'k=1 float diagnostic on arbitrary data/port/spin/aux/scratch/oldRIGHT columns; no cap28 huge native execution',
 'reports':reports,'basis_checks':checks,'max_l2_error':maxerr,'prune_threshold':1e-14,'GR_closed':False}
(P/'B31_TRUE_SPIN_CHECK.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
