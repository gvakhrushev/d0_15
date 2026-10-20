"""Rigorous K9 finite Fourier Hessian over the owned v8 root box; no root replay."""
import sys,time,json,itertools,math,ast,hashlib
from pathlib import Path
import numpy as np
from flint import arb,acb,arb_mat,acb_mat,ctx
ctx.prec=128
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(sys.argv[sys.argv.index('--output')+1]) if '--output' in sys.argv else Path(__file__).with_name('COLLAR_HESSIAN_ARB.json')
L=8;m=16384
C=np.zeros((4,16,16),dtype=np.int64)
for a in range(4):
 for mask in range(16):
  if not(mask>>a)&1:C[a,mask|(1<<a),mask]=(-1)**((mask&((1<<a)-1)).bit_count())
eta=np.diag([1,-1,-1,-1]).astype(np.int64)
U=[eta,eta@np.ones((4,4),dtype=np.int64)]
Cu=np.array([np.einsum('ar,aij->rij',v,C) for v in U])
S=[]
x=np.zeros((4,4),dtype=np.int64);x[0,0]=1;S.append(x)
x=np.zeros((4,4),dtype=np.int64);x[0,1:]=1;x[1:,0]=-1;S.append(x)
S.append(np.diag([0,1,1,1]).astype(np.int64))
x=np.zeros((4,4),dtype=np.int64);x[1:,1:]=1-np.eye(3,dtype=np.int64);S.append(x)
x=np.zeros((4,4),dtype=np.int64);x[0,1:]=1;x[1:,0]=1;S.append(x)
fam=np.zeros((4,4,4,4),dtype=np.int64)
boost=[]
for i in range(1,4):
 x=np.zeros((4,4),dtype=np.int64);x[0,i]=x[i,0]=1;boost.append(x)
fam[0,0]=sum(boost)
for i in range(1,4):
 fam[1,i]=boost[i-1]
 fam[2,i]=sum(boost[j-1] for j in range(1,4) if j!=i)
 for j in range(1,4):
  if i!=j:fam[3,i,i,j]+=1;fam[3,i,j,i]-=1
coefs=np.array([np.array([np.einsum('ar,aij->rij',X@v,C) for v in U]) for X in S])
links=[]
for f in fam:
 gam=np.einsum('rab,aik,bkj->rij',f,C,C.transpose(0,2,1))
 links.append(np.array([np.einsum('rij,rjk->rik',cv,gam) for cv in Cu]))
links=np.array(links)
# t_j=(a+b sqrt2 + i(c+d sqrt2))/2, exact eighth roots.
T=np.array([[2,0,0,0],[0,1,0,1],[0,0,2,0],[0,-1,0,1],[-2,0,0,0],[0,-1,0,-1],[0,0,-2,0],[0,1,0,-1]],dtype=np.int64)
ZT=T.copy();ZT[:,0]-=2
SQ=arb(2).sqrt();I=acb(0,1)
qball=lambda p:arb(int(p[0]))+arb(int(p[1]))*SQ

def spectrum_feature(k):
 z=ZT[list(k)]
 aa=np.array([sum(128-64*T[j,0] for j in k),sum(-64*T[j,1] for j in k)],dtype=np.int64)
 cc=np.zeros(2,dtype=np.int64)
 for r in range(4):
  for s in range(r):
   a,b,c,d=z[r];e,f,g,h=z[s]
   cc+=32*np.array([a*e+2*b*f+c*g+2*d*h,a*f+b*e+c*h+d*g],dtype=np.int64)
 return tuple(map(int,aa)),tuple(map(int,cc))

def mul(A,B):
 # Last three axes are (quadratic-field component, matrixrow,matrixcol).
 assert 16*8*int(np.max(np.abs(A)))*int(np.max(np.abs(B))) <2**63
 a,b,c,d=np.moveaxis(A,-3,0);e,f,g,h=np.moveaxis(B,-3,0)
 return np.stack([a@e+2*b@f-c@g-2*d@h,a@f+b@e-c@h-d@g,a@g+2*b@h+c@e+2*d@f,a@h+b@g+c@f+d@e],axis=-3)

def gram(A,B):
 assert 256*8*int(np.max(np.abs(A)))*int(np.max(np.abs(B)))<2**63
 a,b,c,d=A.reshape((A.shape[0],4,-1)).transpose(1,0,2)
 e,f,g,h=B.reshape((B.shape[0],4,-1)).transpose(1,0,2)
 return np.stack([a@e.T+2*b@f.T+c@g.T+2*d@h.T,a@f.T+b@e.T+c@h.T+d@g.T,a@g.T+2*b@h.T-c@e.T-2*d@f.T,a@h.T+b@g.T-c@f.T-d@e.T],axis=-1)

def arrays(k,l):
 zk=ZT[list(k)];zl=ZT[list(l)];tk=T[list(k)];tl=T[list(l)]
 def op(z1,z2,cc):
  return np.stack([np.einsum('r,frij->fij',z1[:,i],cc)+(1 if i<2 else -1)*np.einsum('r,frji->fij',z2[:,i],cc) for i in range(4)],axis=1)
 Dk=op(zk,zk,Cu);Dl=op(zl,zl,Cu)
 V=np.stack([op(zk,zl,cf) for cf in coefs]+[op(tk,tl,lf) for lf in links])
 # Shape V:9,2,4,16,16; exact common denominator2, physical factorL.
 Q=np.empty((9,3,4,16,16),dtype=np.int64)
 Q[:,0]=mul(Dl[0],V[:,0])+mul(V[:,0],Dk[0])
 Q[:,1]=mul(Dl[0],V[:,1])+mul(V[:,1],Dk[0])+mul(Dl[1],V[:,0])+mul(V[:,0],Dk[1])
 Q[:,2]=mul(Dl[1],V[:,1])+mul(V[:,1],Dk[1])
 # Q has common denominator4, physical factorL².
 Gv=[gram(V[:,0],V[:,0]),gram(V[:,0],V[:,1])+gram(V[:,1],V[:,0]),gram(V[:,1],V[:,1])]
 Gq=[gram(Q[:,0],Q[:,0]),gram(Q[:,0],Q[:,1])+gram(Q[:,1],Q[:,0]),gram(Q[:,0],Q[:,2])+gram(Q[:,1],Q[:,1])+gram(Q[:,2],Q[:,0]),gram(Q[:,1],Q[:,2])+gram(Q[:,2],Q[:,1]),gram(Q[:,2],Q[:,2])]
 trQ=np.trace(Q,axis1=-2,axis2=-1)
 return Gv,Gq,trQ

v8=ROOT/'02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/verify.py'
center=next(ast.literal_eval(n.value) for n in ast.parse(v8.read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CENTER' for t in n.targets))
d=arb(center[0],'1e-12');o=arb(center[1],'1e-12')
a=(d-o).sqrt();b=((d+3*o).sqrt()-a)/4
vpoly=[a*a,a*b,b*b];qpoly=[a**4,a**3*b,a*a*b*b,a*b**3,b**4];Qpoly=[a*a,a*b,b*b]
p=(arb(5).sqrt()-1)/2;alpha=p*p/(128*L*L);beta=m*alpha;z=arb(1)/(2**20);M=128
orbits=[]
for t in range(8):
 for kk in itertools.combinations_with_replacement(range(8),3):
  mult=6
  for val in set(kk):mult//=math.factorial(kk.count(val))
  orbits.append(((t,)+kk,mult))
assert sum(v for _,v in orbits)==4096
spec={}
for k in itertools.product(range(8),repeat=4):
 aa,cc=spectrum_feature(k);E=d*qball(aa)+o*qball(cc);B=1-alpha*E;ee=B**m
 ch=int(sum(j!=0 for j in k)==1 and any(j in(1,7) for j in k))
 spec[k]={'aa':aa,'cc':cc,'E':E,'B':B,'ee':ee,'a':ee/B,'chi':ch}
Z=16*sum(spec[k]['ee']*mult for k,mult in orbits)
for v in spec.values():
 F=1-z+z*v['ee'];v['F']=F
 v['kap']=-v['a']/Z+M*z*beta*v['a']/F
 v['w']=v['kap']+arb(v['chi'])/128
 ap=-alpha*(m-1)*v['ee']/(v['B']**2);fp=-z*beta*v['a']
 v['slope']=-ap/Z+M*z*beta*(ap/F-v['a']*fp/(F*F))

def evaluate(features,powers,scale):
 out=[]
 for i in range(9):
  for j in range(9):
   re=arb(0);im=arb(0)
   for arr,powr in zip(features,powers):
    v=arr[i,j]
    if v[0] or v[1]:re+=qball(v[:2])*powr
    if v[2] or v[3]:im+=qball(v[2:])*powr
   out.append(acb(re*scale,im*scale))
 return acb_mat(9,9,out)

def tr_eval(arr):
 out=[]
 for i in range(9):
  re=arb(0);im=arb(0)
  for j,powr in enumerate(Qpoly):
   v=arr[i,j];re+=qball(v[:2])*powr;im+=qball(v[2:])*powr
  out.append(acb(re*L*L/4,im*L*L/4))
 return out

cases=[];start=time.perf_counter()
for q in range(5):
 K=acb_mat(9,9);norm=[acb(0) for _ in range(9)];maxint=0
 for nn,(k,mult) in enumerate(orbits):
  l=((k[0]+q)%8,)+k[1:];vk=spec[k];vl=spec[l]
  if vk['aa']==vl['aa'] and vk['cc']==vl['cc']:
   assert vk['chi']==vl['chi'];dd=vk['slope']
  else:
   de=vl['E']-vk['E'];assert not de.contains(0),(q,k,str(de))
   dd=(vl['kap']-vk['kap']+arb(vl['chi']-vk['chi'])/128)/de
  Gv,Gq,trQ=arrays(k,l)
  K+=evaluate(Gv,vpoly,arb(L*L)/4)*(mult*(vk['w']+vl['w']))+evaluate(Gq,qpoly,arb(L**4)/16)*(mult*dd)
  if q==0:
   tr=tr_eval(trQ)
   for i in range(9):norm[i]+=tr[i]*(mult*vk['a'])
  if nn%240==0:print(json.dumps({'q':q,'orbits':nn,'elapsed':time.perf_counter()-start}),flush=True)
 if q==0:
  K-=acb_mat([[norm[i].conjugate()*norm[j]*beta/(Z*Z) for j in range(9)] for i in range(9)])
 cases.append(K)
 print(json.dumps({'q_done':q,'elapsed':time.perf_counter()-start,'K00':str(K[0,0])}),flush=True)
# Exact real Fourier reconstruction of site-fibre block matrix.
positions=[0]*9+[-1];components=list(range(9))+[5]
def H(diff,i,j):
 out=cases[0][i,j]+cases[4][i,j]*((-1)**diff)
 for q in range(1,4):
  tt=T[(q*diff)%8];phase=acb(qball(tt[:2])/2,qball(tt[2:])/2)
  out+=phase*cases[q][i,j]+phase.conjugate()*cases[q][i,j].conjugate()
 assert out.imag.contains(0),str(out)
 return out.real/8
A=arb_mat([[H(positions[i]-positions[j],components[i],components[j]) for j in range(10)] for i in range(10)])
Bv=arb_mat([[H(positions[i]-1,components[i],2)] for i in range(10)])
# arb interval inverse proves nonsingularity; ball solve encloses actual response.
Inv=A.inv();response=-(Inv*Bv)
# Independent rational-midpoint Neumann residual certificate.
import fractions
Rnum=np.linalg.inv(np.array([[float(A[i,j].mid()) for j in range(10)] for i in range(10)]))
R=arb_mat([[arb(str(float(Rnum[i,j]))) for j in range(10)] for i in range(10)])
res=arb_mat(10,10)-R*A
for i in range(10):res[i,i]+=1
row_bounds=[sum(abs(res[i,j]) for j in range(10)) for i in range(10)]
assert all(bound<arb('0.0001') for bound in row_bounds)
assert all(not response[j,0].contains(0) for j in (6,7,8))
out={'status':'RIGOROUS_ARB_PASS','python_flint':'0.9.0','precision_bits':ctx.prec,'root_box':{'d':str(d),'o':str(o),'radius':'1e-12'},'L':8,'all_momenta':4096,'spatial_S3_orbits':960,'fullCAR':16,'fixedRIGHT':128,'calibrations':{'m':m,'alpha':str(alpha),'beta':str(beta),'z':'2^-20'},'A':[[str(A[i,j]) for j in range(10)] for i in range(10)],'boundary_covector':[str(Bv[i,0]) for i in range(10)],'response':[str(response[i,0]) for i in range(10)],'neumann_residual_inf_upper_bound':'1/10000','neumann_row_bounds':[str(bound) for bound in row_bounds],'rational_preconditioner':[[str(float(Rnum[i,j])) for j in range(10)] for i in range(10)],'transverse_response_nonzero':[6,7,8],'K9':[[[str(K[i,j]) for j in range(9)] for i in range(9)] for K in cases],'elapsed_seconds':time.perf_counter()-start,'scope':'Exact integer Q(sqrt2,i) feature traces and Arb enclosures over owned rootbox; encloses the true Hessian at its exact stationary root using owned moment cancellation, not an off-root Hessian identity; full HJR finite Hessian plus Riesz preparation Schur; no native admission, root replay or GR claim.'}
OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','response','neumann_residual_inf_upper_bound','elapsed_seconds']},indent=2),flush=True)
