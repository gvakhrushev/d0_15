"""Numerical exploration only: actual metric coupling to full Bloch Hessian."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json
from pathlib import Path
import numpy as np
from itertools import combinations
from linear import UPSTREAM
UP=UPSTREAM.parent
sys.path.insert(0,str(UP))
from interval_check import ET as eta,GN as GEN,neighbor
from symbol import STAR,G2,PAIR
GS=np.array((G2*STAR).tolist(),float)
PACK=list(combinations(range(4),2));MP=[(i,j) for i in range(4) for j in range(i,4)]

def frame(L):
 t=np.arange(L)*2*np.pi/L;f=1+np.cos(t)[:,None]/100+np.cos(t)[None,:]/1000
 E=np.tile(np.eye(4),(L*L,1,1));E[:,2,2]=f.ravel();E[:,3,3]=f.ravel();return E

def setup(A):
 ans={};eye=np.eye(4)
 for ix in range(len(A)):
  for r in range(4):
   X=np.einsum('k,kab->ab',A[ix,6*r:6*r+6],GEN);S=np.linalg.inv(eye-X/2);U=S@(eye+X/2)
   d=S@GEN@S;dd=(d[:,None]@GEN[None]@S+d[None]@GEN[:,None]@S)/2
   ans[ix,r,1]=(U,d,dd);ans[ix,r,-1]=(eta@U.T@eta,eta@d.swapaxes(-1,-2)@eta,eta@dd.swapaxes(-1,-2)@eta)
 return ans

def matrices(A,E):
 L=int(round(np.sqrt(len(A))));n=len(A);vc=n*24;gc=n*10
 H={};C={};UU=setup(A);eye=np.eye(4)
 def addH(i,j,dg,ex):
  if ex not in H:H[ex]=np.zeros((vc,vc))
  H[ex][i:i+6,j:j+6]+=dg
 def addC(i,j,dg,ex):
  if ex not in C:C[ex]=np.zeros((vc,gc))
  C[ex][i:i+6,j:j+10]+=dg
 def weight(E,r,s):
  u,v=[a for a in range(4) if a not in (r,s)];seq=[r,s,u,v];sg=(-1)**sum(seq[i]>seq[j] for i,j in combinations(range(4),2))
  w=np.array([E[a,u]*E[b,v]-E[b,u]*E[a,v] for a,b in PAIR])
  wt=sg*w@GS;KK=np.zeros((4,4))
  for t,(a,b) in enumerate(PAIR):KK[a,b]=wt[t]*eta[b,b]
  return KK
 for m in range(n):
  invg=np.linalg.inv(E[m].T@eta@E[m]);dEE=[]
  for a,b in MP:
   V=np.zeros((4,4));V[a,b]=V[b,a]=1.;dEE.append(E[m]@invg@V/2)
  for r,s in PAIR:
   K=weight(E[m],r,s)/2
   dK=np.array([(weight(E[m]+dE,r,s)-weight(E[m]-dE,r,s))/4 for dE in dEE]) # /2 for central diff, /2 for odd part
   ids=[(m,r,1),(neighbor(m,r,L),s,1),(neighbor(m,s,L),r,-1),(m,s,-1)]
   offsets=[(0,0),(int(r==0),int(r==3)),(int(s==0),int(s==3)),(0,0)]
   for sg,ls,off in [(1,ids,offsets),(-1,[(k,a,-z) for k,a,z in ids[::-1]],offsets[::-1])]:
    ff=[UU[k][0] for k in ls];pre=[eye]
    for z in ff:pre.append(pre[-1]@z)
    suf=[None]*5;suf[4]=eye
    for i in range(3,-1,-1):suf[i]=ff[i]@suf[i+1]
    for i,(ix,rr,zz) in enumerate(ls):
     U,d,dd=UU[ix,rr,zz]
     dj=pre[i]@d@suf[i+1];dg=np.einsum('jab,kab->kj',dK,dj)*sg
     addC(ix*24+rr*6,m*10,dg,(-off[i][0],-off[i][1]))
     dg=np.einsum('ab,klab->kl',K,pre[i]@dd@suf[i+1])*sg
     addH(ix*24+rr*6,ix*24+rr*6,dg,(0,0))
    for i in range(4):
     mid=eye;di=UU[ls[i]][1]
     for j in range(i+1,4):
      if j>i+1:mid=mid@ff[j-1]
      dj=UU[ls[j]][1];prod=pre[i]@di[:,None]@mid@dj[None]@suf[j+1]
      dg=np.einsum('ab,klab->kl',K,prod)*sg
      ii=24*ls[i][0]+6*ls[i][1];jj=24*ls[j][0]+6*ls[j][1];ex=(off[j][0]-off[i][0],off[j][1]-off[i][1])
      addH(ii,jj,dg,ex);addH(jj,ii,dg.T,(-ex[0],-ex[1]))
 return H,C

def bloch(dic,k0,k3,L=4):return sum(np.exp(2j*np.pi/L*(k0*i+k3*j))*B for (i,j),B in dic.items())

def main():
 A=np.array(json.loads((UP/'center.json').read_text())).reshape(16,24);E=frame(4);H,C=matrices(A,E)
 out=[]
 for i in range(4):
  for j in range(4):
   M=bloch(H,i,j);D=bloch(C,i,j);ev,V=np.linalg.eigh(M);ind=np.argsort(abs(ev));weak=ind[0]
   X=np.linalg.solve(M,D);Sch=D.conj().T@X
   row=dict(q0=i,q3=j,H_hermitian_error=float(np.max(abs(M-M.conj().T))),smallest_eigenvalues=ev[ind[:4]].tolist(),metric_norm=float(np.linalg.norm(D)),weak_metric_coupling=float(np.linalg.norm(D.conj().T@V[:,weak])),Hinv_inf=float(np.linalg.norm(np.linalg.inv(M),np.inf)),Hinv_C_inf=float(np.linalg.norm(X,np.inf)),Schur_inf=float(np.linalg.norm(Sch,np.inf)))
   print(json.dumps(row),flush=True);out.append(row)
 Path(__file__).with_name('curved_metric_scout.json').write_text(json.dumps({'status':'FLOATING_EXPLORATION_NOT_A_BOUND','blocks':out},indent=2)+'\n')
if __name__=='__main__':main()
