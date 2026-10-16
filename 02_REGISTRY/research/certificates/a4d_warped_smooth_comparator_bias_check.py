#!/usr/bin/env python3
"""Literal all-24-row first smooth source correction on the fixed cosine warp.

This verifies a finite formal jet; it constructs no exact prescribed-source
root. The exact designated rescue is a separate analytic owner. The portable
owner-directory option allows independent replay outside the repository.
"""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,importlib.util,json,sys,time
import numpy as np
import sympy as sp

PARSER=argparse.ArgumentParser(description=__doc__)
PARSER.add_argument('--owner-directory',type=Path,default=Path(__file__).resolve().parent)
PARSER.add_argument('--output',type=Path,default=Path(__file__).with_name('a4d_warped_smooth_comparator_bias_results.json'))
PARSER.add_argument('--write-json',action='store_true')
ARGS=PARSER.parse_args()
sys.path.insert(0,str(ARGS.owner_directory))
import a4d_identity_quarter_nonlinear_response_check as N

f=sp.Symbol('f',positive=True);p,q,r,s,t=sp.symbols('p q r s t',real=True)
J=(f,p,q,r,s,t)
I=N.I;G=N.G;Z=np.zeros((4,4),dtype=object)

def simplify(a):
 a=np.asarray(a,dtype=object)
 return np.array([sp.cancel(sp.expand(x)) for x in a.flat],dtype=object).reshape(a.shape)

def derivative(a):
 a=np.asarray(a,dtype=object)
 return np.array([sum(sp.diff(x,J[k])*J[k+1] for k in range(len(J)-1)) for x in a.flat],dtype=object).reshape(a.shape)

def mm(a,b):return simplify(N.jmul(a,b))

def weight_base(face,ss):
 rr,ss0=N.PAIRS[face];u,v=[j for j in range(4) if j not in (rr,ss0)]
 solder=np.diag([1,1,ss,ss]).astype(object)
 return N.orient(rr,ss0)*N.weight(N.wedge(solder[:,u],solder[:,v]))

W=np.array([weight_base(face,f) for face in range(6)])
DW=[]
S=np.diag([1,1,f,f]).astype(object)
QINV=np.diag([1,-1,-f**-2,-f**-2]).astype(object)
ETA=np.diag(N.SIG).astype(object)
for face,(rr,ss) in enumerate(N.PAIRS):
 u,v=[j for j in range(4) if j not in (rr,ss)]
 row=[]
 for a,b in N.SYM:
  dq=np.zeros((4,4),dtype=object);dq[a,b]=dq[b,a]=1
  ds=S@QINV@dq*sp.Rational(1,2)
  assert not np.any(simplify(ds.T@ETA@S+S.T@ETA@ds-dq))
  row.append(N.orient(rr,ss)*N.weight(N.wedge(ds[:,u],S[:,v])+N.wedge(S[:,u],ds[:,v])))
 DW.append(row)
DW=np.array(DW)
# For any matrix P, W:P^dagger=(eta W^T eta):P. Consequently the
# complete naked odd curvature readout equals W:P, including its 1/2.
for aa in list(W)+list(DW.reshape(60,4,4)):
 assert not np.any(simplify(ETA@aa.T@ETA+aa))

H=np.zeros((24,24),dtype=object)
for face,(rr,ss) in enumerate(N.PAIRS):
 for a in range(6):
  for b in range(6):
   vv=sp.expand(np.sum(W[face]*(G[a]@G[b]-G[b]@G[a])))
   H[6*rr+a,6*ss+b]+=vv;H[6*ss+b,6*rr+a]+=vv
HI=sp.Matrix(H).inv()
assert sp.simplify(sp.Matrix(H)*HI)==sp.eye(24)
A1=np.zeros((4,4,4),dtype=object);A1[2]=-p*G[3];A1[3]=-p*G[4]

def jets(alist,degree):
 out={}
 for role in range(4):
  for offset in (-1,0,1):
   log=N.jconst(Z,degree)
   for k,aa in enumerate(alist,start=1):
    cur=aa[role]
    for dd in range(degree-k+1):
     log[k+dd]+=cur*sp.Rational(offset**dd,sp.factorial(dd))
     cur=derivative(cur)
   out[(role,offset)]=simplify(N.jexp(log))
 return out

def plaquette(jet,face,base,degree,swapped=False):
 rr,ss=N.PAIRS[face]
 er,es=(int(ss==1),int(rr==1)) if swapped else (int(rr==1),int(ss==1))
 loc=[(rr,base),(ss,base+er),(rr,base+es),(ss,base)]
 fac=[jet[xy] if i<2 else N.jinv(jet[xy]) for i,xy in enumerate(loc)]
 pre=[N.jconst(I,degree)]
 for ff in fac:pre.append(mm(pre[-1],ff))
 suff=[None]*5;suff[4]=N.jconst(I,degree)
 for i in range(3,-1,-1):suff[i]=mm(fac[i],suff[i+1])
 return fac,pre,suff

def euler(alist,degree,doF=True,swapped=False):
 jet=jets(alist,degree)
 F=np.zeros((degree+1,24),dtype=object);E=np.zeros((degree+1,10),dtype=object)
 cache={}
 for face,(rr,ss) in enumerate(N.PAIRS):
  for base in (-1,0):cache[(face,base)]=plaquette(jet,face,base,degree,swapped)
  for j in range(10):
   for k in range(degree+1):
    prod=cache[(face,0)][1][4]
    value=np.sum(DW[face,j]*prod[k])
    odd_value=np.sum(DW[face,j]*(prod[k]-N.jinv(prod)[k]))*Fraction(1,2)
    assert sp.cancel(value-odd_value)==0
    E[k,j]+=sp.expand(value)
  if not doF:continue
  er,es=(int(ss==1),int(rr==1)) if swapped else (int(rr==1),int(ss==1))
  roles=[rr,ss,rr,ss];offsets=[0,er,es,0]
  for i,(role,off) in enumerate(zip(roles,offsets)):
   base=-off;fac,pre,suff=cache[(face,base)]
   ww=N.jconst(W[face],degree);cur=W[face]
   for k in range(1,degree+1):
    cur=derivative(cur);ww[k]=cur*sp.Rational(base**k,sp.factorial(k))
   co=mm(suff[i+1],mm(ww.swapaxes(-1,-2),pre[i]))
   jet0=-mm(fac[i],co) if i>=2 else mm(co,fac[i])
   for g in range(6):
    for k in range(degree+1):F[k,6*role+g]+=np.sum(jet0[k].T*G[g])
 return simplify(F),simplify(E)

def mats(coeff):
 return np.array([sum((coeff[6*role+g]*G[g] for g in range(6)),Z.copy()) for role in range(4)],dtype=object)

def coords(m):return simplify([[aa[a,b] for a,b in N.PAIRS] for aa in m])
def nonzero(a):return [[i,str(x)] for i,x in enumerate(simplify(a).flat) if x!=0]

def run():
 F2,E2=euler([A1],2)
 assert not np.any(F2[:2])
 A2=simplify(mats(list(-HI*sp.Matrix(F2[2]))))
 expectedA2=np.zeros(24,dtype=object)
 expectedA2[0]=p**2/(2*f**2)
 expectedA2[9]=expectedA2[10]=p**2/(2*f)
 expectedA2[15]=expectedA2[22]=q/2+p**2/(2*f)
 assert not np.any(simplify(coords(A2).reshape(24)-expectedA2))
 F3,E3=euler([A1,A2],3)
 assert not np.any(F3[:3])
 A3=simplify(mats(list(-HI*sp.Matrix(F3[3]))))
 expectedA3=np.zeros(24,dtype=object)
 expectedA3[0]=p**3/(2*f)-p*q/(2*f**2)
 expectedA3[9]=expectedA3[10]=p*q/(2*f)-p**3/(2*f**2)
 expectedA3[15]=expectedA3[22]=-p**3/6-r/6-p*q/(2*f)
 expectedA3[17]=p**3/(2*f);expectedA3[23]=-p**3/(2*f)
 assert not np.any(simplify(coords(A3).reshape(24)-expectedA3))
 correctedF,correctedE=euler([A1,A2,A3],3)
 assert not np.any(correctedF)
 assert not np.any(simplify(correctedE-E3))
 # Hostile arbitrary 24-parameter third coefficient: the order-three
 # metric readout cannot depend on A3, and every connection row has
 # exactly the already owned constant-character Hessian coefficient.
 zz=sp.symbols('c0:24',real=True);arbitrary=mats(zz)
 arbitraryF,arbitraryE=euler([A1,A2,arbitrary],3)
 assert not np.any(simplify(arbitraryE-E3))
 assert not np.any(simplify(arbitraryF[3]-F3[3]-H@np.array(zz,dtype=object)))
 expected0=np.array([-f*q-p**2/2,0,0,0,p**2/2,0,0,q/(2*f),0,q/(2*f)],dtype=object)
 expected1=np.array([3*p*q/2,0,0,0,-p*q/2,p**3/(2*f),p**3/(2*f),0,0,0],dtype=object)
 assert not np.any(simplify(E3[2]-expected0))
 assert not np.any(simplify(E3[3]-expected1))
 assert not np.any(E3[:2])
 # The omission and shared-link swap both fail the pinned response.
 _,omitE=euler([A1],3,doF=False)
 _,swapE=euler([A1,A2],3,doF=False,swapped=True)
 omitDifference=simplify(omitE[3]-expected1)
 swapDifference=simplify(swapE[2:]-E3[2:])
 assert np.any(omitDifference) and np.any(swapDifference)
 rational_point={f:sp.Rational(51,50),p:sp.Rational(1,7),q:sp.Rational(-2,11)}
 rational_rho1=simplify([sp.sympify(value).subs(rational_point) for value in expected1])
 rational_expected=np.array([sp.Rational(-3,77),0,0,0,sp.Rational(1,77),sp.Rational(25,17493),sp.Rational(25,17493),0,0,0],dtype=object)
 assert np.array_equal(rational_rho1,rational_expected)
 assert np.any(rational_rho1)
 # Independent continuum Einstein calculation, without importing an
 # Einstein formula from the discrete response.
 metric=sp.diag(1,-1,-f**2,-f**2);inverse=metric.inv()
 dt=lambda value,i:derivative(np.array([value]))[0] if i==1 else sp.Integer(0)
 Gamma=[[[sp.cancel(sum(inverse[a,d]*(dt(metric[d,c],b)+dt(metric[d,b],c)-dt(metric[b,c],d))/2 for d in range(4))) for c in range(4)] for b in range(4)] for a in range(4)]
 Ricci=sp.Matrix(4,4,lambda b,c:sp.cancel(sum(dt(Gamma[a][b][c],a)-dt(Gamma[a][b][a],c)+sum(Gamma[a][a][d]*Gamma[d][b][c]-Gamma[a][c][d]*Gamma[d][b][a] for d in range(4)) for a in range(4))))
 scalar=sp.cancel(sp.trace(inverse*Ricci))
 einstein=Ricci-metric*scalar/2
 raised=inverse*einstein*inverse*f**2/2
 continuum=np.array([(1 if a==b else 2)*raised[a,b] for a,b in N.SYM],dtype=object)
 assert not np.any(simplify(continuum-expected0))
 qslots=np.array([metric[a,b] for a,b in N.SYM],dtype=object)
 trace=sp.cancel(qslots@expected0)
 assert trace==-2*f*q-p**2
 # cos(theta)^2 and sin(theta)^2 averages are 1/2 for every L>=3;
 # on allowed L in 4N, this exact polynomial is pi²/1250.
 cc=sp.Symbol('c',real=True)
 trace_scaled=sp.expand(trace.subs({f:(51-cc)/50,q:2*cc/25,p**2:(1-cc**2)/625}))
 assert trace_scaled==(-102*cc+3*cc**2-1)/625
 assert trace_scaled.subs(cc**2,sp.Rational(1,2)).subs(cc,0)==sp.Rational(1,1250)
 # This generic observation point proves rho1 is not identically zero
 # on the fixed warp; pi powers are explicit continuum data.
 rho1_point=simplify(expected1).reshape(10)
 theta=sp.pi/4
 point={f:(51-sp.cos(theta))/50,p:sp.sin(theta)*sp.pi/25,q:2*sp.cos(theta)*sp.pi**2/25}
 rho1_point=simplify([value.subs(point) for value in rho1_point])
 assert rho1_point[0]==3*sp.pi**3/1250
 report={
  'status':'PASS_EXACT_FORMAL_SMOOTH_SOURCE_JET; no exact prescribed-source existence claim',
  'owner_sha1':hashlib.sha1(Path(N.__file__).read_bytes()).hexdigest(),
  'generator_order':['K1','K2','K3','J12','J13','J23'],
  'metric_slot_order':[list(x) for x in N.SYM],
  'jet_variables':{'f':'f(y)','p':'f_prime(y)','q':'f_second(y)','r':'f_third(y)'},
  'all_24_connection_rows_through_order3':'zero after A1,A2,A3',
  'A1':nonzero(coords(A1)), 'A2':nonzero(coords(A2)), 'A3':nonzero(coords(A3)),
  'rho0':list(map(str,simplify(expected0))), 'rho1':list(map(str,simplify(expected1))),
  'arbitrary_24_A3_response_dependency':'zero at order3',
  'arbitrary_24_A3_connection_dependency':'H_s(1) times all24 coefficients',
  'curvature_and_readout_odd_projection':'all six W and all60 DW are eta-antisymmetric; full odd 1/2 readout equals W:P',
  'omitted_A2_negative_difference':nonzero(omitDifference),
  'swapped_shared_incidence_negative_difference_order2_and3':nonzero(swapDifference),
  'independent_continuum_match':'rho0=sqrt_abs_det_g * packed_raised_G_standard/2',
  'scalar_curvature':str(scalar),'trace_rho0':str(trace),
  'sampled_trace_pi_squared_coefficient_polynomial_in_cos':str(trace_scaled),
  'sampled_trace_mean_for_L_in_4N':'pi^2/1250',
  'rho1_at_y_1_8':list(map(str,rho1_point)),
  'rho1_at_generic_rational_jet_f_51_50_p_1_7_q_minus_2_11':list(map(str,rational_rho1)),
  'original_raw_norm_implication':'if exact fixed rho0 source roots existed, raw normalized gap would have first order h and grow like h^-3',
  'nonclaims':['no exact prescribed-source root','no source candidate assignment','no full transverse inverse','no universal source-image theorem']}
 return report

if __name__=='__main__':
 result=run()
 text=json.dumps(result,indent=2,sort_keys=True)+'\n'
 if ARGS.write_json:ARGS.output.write_text(text)
 else:
  if json.loads(ARGS.output.read_text())!=result:raise AssertionError('pinned result mismatch')
 print('PASS_ALL24_SMOOTH_WARP_SOURCE_JET_AND_HOSTILE_CONTROLS',flush=True)
 print(json.dumps({k:result[k] for k in ('rho0','rho1','sampled_trace_mean_for_L_in_4N','status')},sort_keys=True),flush=True)
