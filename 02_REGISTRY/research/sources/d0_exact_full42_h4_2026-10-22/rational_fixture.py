import json
import numpy as np
from pathlib import Path
from native42 import problem,ROOT_UNIFORM,ETA,L,full_source,I
OUT=Path(__file__).resolve().parent

def cayley(Y):return np.linalg.solve(I-Y/2,I+Y/2)
def inv_cayley(U):return 2*(U-I)@np.linalg.inv(U+I)
def project(Y):return np.array([np.sum(Y*G)/2 for G in L])
def encode_num(x):return format(float(x),'.17g')

def write():
 h,fields,euler=problem();nodes=fields(ROOT_UNIFORM)
 info={'version':1,'purpose':'exact rational fixed collar for same original six-face N1 field function; not original h continuum slab','h':encode_num(h),'nodes':[],'theta_center':[encode_num(x) for x in ROOT_UNIFORM]}
 for j,node in enumerate(nodes):
  Us=[]
  for U in node['U']:
   Y=inv_cayley(U);params=project(Y)
   assert np.linalg.norm(Y-sum(a*G for a,G in zip(params,L)))<3e-13
   Uagain=cayley(sum(a*G for a,G in zip(params,L)))
   assert np.max(abs(Uagain-U))<2e-13
   Us.append([encode_num(a) for a in params])
  info['nodes'].append({'e':[[encode_num(x) for x in row] for row in node['e']],
         'lie_params':Us,
         'v':[[encode_num(x) for x in row] for row in node['v']]})
 path=OUT/'rational_root_center.json';path.write_text(json.dumps(info,indent=2)+'\n')
 print('saved',path,'h',h,'original_residual',np.max(abs(euler(ROOT_UNIFORM))))

def newproblem():
 with open(OUT/'rational_root_center.json') as f: info=json.load(f)
 h=float(info['h']);nodes=[]
 for nd in info['nodes']:
  co=np.array(nd['e'],float)
  uu=np.array([cayley(sum(float(a)*G for a,G in zip(par,L))) for par in nd['lie_params']])
  vv=np.array(nd['v'],float)
  nodes.append(dict(e=co,U=uu,v=vv))
 def fields(z):
  q=[dict(e=nd['e'].copy(),U=nd['U'].copy(),v=nd['v'].copy()) for nd in nodes]
  q[1]['e']+=np.reshape(z[:16],(4,4))
  for r in range(4):
   Y=sum(z[16+6*r+k]*L[k] for k in range(6))
   q[1]['U'][r]=cayley(Y)@q[1]['U'][r]
  for A in range(2):
   q[0]['v'][A,0]+=z[40+A]/h
   q[1]['v'][A,0]-=z[40+A]/h
  return q
 def euler(z):
  src=full_source(fields(z),h,[1.,1.],.05)
  return np.r_[src['e'][1].ravel(),(h*src['U'][1]).ravel(),h*src['psi'][1]]
 return h,fields,euler

if __name__=='__main__':
 write()
 h,f,e=newproblem();z=np.zeros(42)
 x=e(z);print('new rational collar residual',np.linalg.norm(x,np.inf),'e range',np.min(np.linalg.svd(f(z)[1]['e'])[1]));
 from scipy.optimize._numdiff import approx_derivative
 J=approx_derivative(e,z,method='3-point',abs_step=1e-6)
 print('J min',np.linalg.svd(J)[1][-1], 'inv',np.linalg.norm(np.linalg.inv(J),np.inf));
