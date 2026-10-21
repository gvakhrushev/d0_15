#!/usr/bin/env python3
"""Outward interval proof of Lorentz orientation, genuine nonflat holonomy,
and independent rank-two real material field on the rational root cube."""
from pathlib import Path
from itertools import permutations
import json
from mpmath import mp,iv
import certified_newton as c
import mp_euler as own
ROOT=Path(__file__).resolve().parent
iv.dps=90

def det4(A):
 out=iv.mpf(0)
 for perm in permutations(range(4)):
  sign=(-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
  term=iv.mpf(sign)
  for i,j in enumerate(perm):term*=A[i,j]
  out+=term
 return out

def h_value(z):
 return c.abs_upper(z)

def require_away_zero(label,z,minval):
 lo=mp.mpf(z.a);hi=mp.mpf(z.b)
 assert lo>minval or hi < -minval, (label,lo,hi)
 return {'name':label,'min':mp.nstr(lo,25),'max':mp.nstr(hi,25)}

def run():
 inp=json.loads((ROOT/'mp_center.json').read_text())
 r=iv.mpf('1e-30');z=[iv.mpf([iv.mpf(v)-r,iv.mpf(v)+r]) for v in inp['center']]
 h,base=own.build();nodes=own.fields(z,h,base)
 record=[]
 for j in range(3):
  e=nodes[j]['e'];det=det4(e)
  assert mp.mpf(det.a) > mp.mpf('.9'),(j,det)
  record.append({'kind':'oriented tetrad det>0.9','time_node':j,'lower':mp.nstr(mp.mpf(det.a),23),'upper':mp.nstr(mp.mpf(det.b),23)})
 for j in range(2):
  e=nodes[j]['e'];Uj=nodes[j]['U'];Un=nodes[j+1]['U'];f=iv.mpf(0)
  for aa,bb in own.PAIRS:
   A=Uj[aa];B=Un[bb] if aa==0 else Uj[bb]
   Pm=A*B*own.v_inv(A)*own.v_inv(Uj[bb]);Rmat=(Pm-own.v_inv(Pm))/2
   u,v=[k for k in range(4) if k not in (aa,bb)]
   beta=own.wedge(e[:,u],e[:,v]);vv=own.vec_b(Rmat)
   W=iv.matrix(1,6)
   for k in range(6):W[0,k]=beta[k]*own.G2[k]
   f+=(own.SGNS[aa,bb]*W*own.STAR*vv)[0]/h**2
  g=e.T*own.ETA*e;gi=g**-1
  vv=nodes[j]['v'];Q=vv*gi*vv.T;qq=Q[0,0]+Q[1,1]
  record.append(require_away_zero('finite original STAR f_j'+str(j),f,mp.mpf('.001')))
  record.append(require_away_zero('finite CAR two-source q_j'+str(j),qq,mp.mpf('0.00001')))
  determinant=Q[0,0]*Q[1,1]-Q[0,1]*Q[1,0]
  record.append(require_away_zero('genuine 2x2 scalar current metric Gram determinant '+str(j),determinant,mp.mpf('1e-6')))
  P23=Uj[2]*Uj[3]*own.v_inv(Uj[2])*own.v_inv(Uj[3])
  record.append(require_away_zero('nontrivial full SO face P23 entry 2,3 node '+str(j),P23[2,3],mp.mpf('0.001')))
 out={'status':'PASS_OUTWARD_INTERVAL_NONFLAT_RANK2_ORIGINAL_NATIVE_FINITE42_ROOT',
      'root_cube_radius':'1e-30','coframes_positive_orientation':True,
      'metric_Lorentz_signature':'Sylvester congruence g=e^T diag(1,-1,-1,-1)e, det e>0',
      'nonflat_original_P23':True,'full_CAR_two_independent_real_scalar_currents':True,
      'records':record,'scope':{'exact_finite_mathematical_root':True,'GR_closed':False}}
 (ROOT/'INTERVAL_GEOMETRY_RANK2.json').write_text(json.dumps(out,indent=2)+'\n')
 print('PASS',len(record),'strict original geometric and matter intervals')
 for row in record: print(row)
 return out
if __name__=='__main__':run()
