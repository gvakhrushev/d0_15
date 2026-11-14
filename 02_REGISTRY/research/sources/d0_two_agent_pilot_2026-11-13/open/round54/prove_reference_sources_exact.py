#!/usr/bin/env python3
"""Exact A11 geometric DAG at B25 reference boosts/rotations, no floats."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sympy as s
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');files=[D/'round11/SOURCE_TENSOR_DAG.json',O/'round21/REFERENCE_METADATA.json',O/'round25/targets.py'];h=lambda q:sha256(q.read_bytes()).hexdigest();pins={str(q):h(q) for q in files};dag=json.loads(files[0].read_text());nodes=dag['nodes'];meta=json.loads(files[1].read_text());fh=F(meta['F_h_rational']);assert fh==F(16517734400,162621047169)
# Exact Q(sqrt2) field representation.
def add(x,y):return x[0]+y[0],x[1]+y[1]
def mul(x,y):return x[0]*y[0]+2*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def cast(x):
 x=s.expand(x);a=x.coeff(s.sqrt(2),0);b=x.coeff(s.sqrt(2),1);assert s.simplify(x-a-b*s.sqrt(2))==0
 return F(int(s.numer(a)),int(s.denom(a))),F(int(s.numer(b)),int(s.denom(b)))
t=s.Rational(1,8);v=s.Rational(1,80);ca=(1+t*t)/(1-t*t);sa=2*t/(1-t*t);cb=(1-v*v)/(1+v*v);sb=2*v/(1+v*v);A=s.eye(4);A[0,0]=A[2,2]=ca;A[0,2]=A[2,0]=sa;B=s.eye(4);B[1,1]=B[2,2]=cb;B[1,2]=sb;B[2,1]=-sb;r2=s.sqrt(2)/2;T=s.Matrix([[r2,r2,0,0],[r2,-r2,0,0],[0,0,1,0],[0,0,0,-1]]);cart=s.diag(1,-1,-1,-1);null=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]]);assert T.T*T==s.eye(4) and T*cart*T.T==null
U=s.Rational(3,5)/6*T*cart;An=T*A*T.T;Bn=T*B*T.T
# Reachable geometric nodes contain no p constants. This directly evaluates
# actual pinned A11 expressions in Q(sqrt2), not a numerically sampled target.
needed=set();todo=[dag['roots']['H_f_before_inverse_PF']]
while todo:
 i=todo.pop()
 if i in needed:continue
 needed.add(i);todo.extend(nodes[i].get('args',[]))
assert all(nodes[i].get('b','0')=='0' for i in needed if nodes[i]['op']=='const')
def evaluate(link_mats):
 values={}
 for i in sorted(needed):
  z=nodes[i];op=z['op']
  if op=='const':out=(F(z['a']),F())
  elif op=='var':
   w=z['name'].split('/')
   if w[0]=='u':out=cast(U[int(w[2]),int(w[1])])
   else:assert w[0]=='M';out=cast(link_mats[int(w[2])][int(w[3]),int(w[4])])
  elif op=='add':
   out=(F(),F())
   for j in z['args']:out=add(out,values[j])
  else:
   assert op=='mul';out=(F(1),F())
   for j in z['args']:out=mul(out,values[j])
  values[i]=out
 return values[dag['roots']['H_f_before_inverse_PF']]
plus=evaluate([An,Bn,s.eye(4),s.eye(4)]);minus=evaluate([An,Bn.T,s.eye(4),s.eye(4)]);flat=evaluate([s.eye(4)]*4)
assert plus==(fh/36,F()) and minus==(-fh/36,F()) and flat==(F(),F())
# Structural homogeneity in source variables, including no accidental
# fixed offset. Compute (coframe degree, matter-X degree) sets for each node.
deg=[]
for z in nodes:
 op=z['op']
 if op=='const':out=set() if z['a']=='0' and z['b']=='0' else {(0,0)}
 elif op=='var':out={(1,0)} if z['kind']=='choi_coframe' else {(0,1)} if z['kind']=='matter_X' else {(0,0)}
 elif op=='add':out=set().union(*(deg[j] for j in z['args']))
 else:
  assert op=='mul';out={(0,0)}
  for j in z['args']:out={(a+c,b+d) for a,b in out for c,d in deg[j]}
 deg.append(out)
assert deg[dag['roots']['H_f_before_inverse_PF']]=={(2,0)} and deg[dag['roots']['H_q_before_inverse_PF']]=={(2,2)}
for path,pin in pins.items():assert h(Path(path))==pin
out={'status':'PASS_A11_REFERENCE_GEOMETRY_EXACT_QSQRT2','input_sha256':pins,'geometric_ancestor_nodes_exact':len(needed),'F_h_rational':str(fh),'Hf_xplus_at_rho1':str(plus[0]),'Hf_xminus_at_rho1':str(minus[0]),'Hf_flat_exact':str(flat[0]),'Hf_xplus_equals_Fh_over_36':True,'Hf_xminus_equals_minus_Fh_over_36':True,'coframe_and_matter_source_homogeneity':{'H_f':[2,0],'H_q':[2,2]},'arbitrary_rho_scaling':'u_ref scales sqrt(rho); hence Hf_x±=±rho*Fh/36 and Hq_ref=±rho*d_h','scope':'Exact ideal source DAG reference identities; all SAM/current-field values and native admission are separate.','GR_closed':False}
(P/'REFERENCE_GEOMETRY_EXACT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'DAG_nodes':len(needed),'xplus':str(plus[0])}))
