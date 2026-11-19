#!/usr/bin/env python3
"""Exploratory full frequency matrix for the OLD full128-rank v8 root.
Floating-point diagnostic, NOT a rigorous eigenvalue or physical-kernel certificate.
It does not implement the new rank8 branch. All 4096 heat momenta are retained.
Only q=(3,3,0,0), outside Omega-Omega, is used here.
No files are written. numpy/scipy required. Root centre is not the exact root.
"""
import time
import numpy as np, scipy.linalg as la, itertools, math, json, hashlib
from pathlib import Path
p=(math.sqrt(5)-1)/2
d=.0636351915943445350; o=.0040167350432317253
F0=math.sqrt(d-o)*np.eye(4)+(math.sqrt(d+3*o)-math.sqrt(d-o))*np.ones((4,4))/4
cc=np.zeros((4,16,16),complex)
for i in range(4):
 for msk in range(16):
  if not(msk&(1<<i)):
   cc[i,msk|(1<<i),msk]=(-1)**((msk&((1<<i)-1)).bit_count())
aa=cc.conj().transpose(0,2,1)
gg=np.einsum('iab,jbc->ijac',cc,aa)
def create(v): return np.einsum('i,iab->ab',v,cc)
def annih(v): return np.einsum('i,iab->ab',v,aa)
def ext(W): return np.einsum('ij,ijab->ab',W,gg)
def cross(v):
 x,y,z=v
 return np.array([[0,-z,y],[z,0,-x],[-y,x,0]],dtype=complex)
modes=np.array(list(itertools.product(range(8),repeat=4)),int)
ph=np.exp(2j*np.pi*modes/8)
zs=8*(ph-1)
u=np.einsum('nr,ri->ni',zs,F0)
D0=np.einsum('ni,iab->nab',u,cc)+np.einsum('ni,iab->nab',u.conj(),aa)
energies=np.einsum('ni,ni->n',u.conj(),u).real
assert np.max(abs(D0@D0-energies[:,None,None]*np.eye(16)))<1e-12
al=p*p/8192; beta=2*p*p; m=16384; fug=2**-20
B=1-al*energies; power=np.exp(m*np.log1p(-al*energies)); Z=16*sum(power)
den=1-fug+fug*power
kap=-power/(B*Z)+128*beta*fug*power/(B*den)
kprime=(m-1)*al*power/(Z*B**2) +128*beta*fug*al*power/(den*B**2)*(-(m-1)+m*fug*power/den)
shell=(np.sum((modes==1)|(modes==7),axis=1)==1)&(np.sum(modes!=0,axis=1)==1)
eps=(128-64*math.sqrt(2))*d
R=np.where(shell,0,1/np.where(shell,1,energies-eps))
w=kap+shell/128

def field_basis(q):
    q=np.array(q,int)
    Qphase=np.exp(2j*np.pi*q/8)
    pars=[]
    for r in range(4):
        wr=F0[r,1:]; rad=np.linalg.norm(wr); zr=wr/rad
        tangent=la.null_space(zr.reshape(1,3))
        for a in range(2):
            pars.append((r,'tangent',a,tangent[:,a]))
        pars.append((r,'angle',0,None))
        if q[r]==0:
            pars.extend([(r,'time',0,None),(r,'radial',0,None)])
    P=len(pars)
    du=np.zeros((P,4,4),complex)
    bz=np.zeros((P,4,3),complex)
    dr=np.zeros((P,4),complex)
    th=np.zeros((P,4),complex)
    Wp=np.zeros((P,4,4,4),complex)
    for A,(r,kind,a,vec) in enumerate(pars):
        wr=F0[r,1:]; rad=np.linalg.norm(wr); zr=wr/rad
        if kind=='tangent':
            du[A,r,1:]=vec; bz[A,r]=vec/rad
        if kind=='time':du[A,r,0]=1
        if kind=='radial':
            du[A,r,1:]=zr; dr[A,r]=1
        if kind=='angle':th[A,r]=1
        Wp[A,r,1:,1:]=(1-Qphase[r])*(np.outer(du[A,r,1:],wr)-np.outer(wr,du[A,r,1:]))/rad**2+th[A,r]*cross(zr)
    return pars,du,bz,dr,th,Wp

def first_D(q,du,Wp):
    N=len(modes); P=len(du)
    inds=np.ravel_multi_index(tuple(((modes+np.array(q))%8).T),(8,)*4)
    out=np.zeros((N,P,16,16),complex)
    for A in range(P):
        for r in range(4):
            V=create(du[A,r]); Vt=annih(du[A,r])
            G=ext(Wp[A,r]); Cu=create(F0[r]); Au=Cu.conj().T
            out[:,A]+=8*((ph[:,r]-1)[:,None,None]*V+
                          (ph[inds,r].conj()-1)[:,None,None]*Vt+
                          ph[:,r,None,None]*(Cu@G)-
                          ph[inds,r].conj()[:,None,None]*(G@Au))
    return out,inds

def direct_second(q,du,bz,dr,th,Wp):
    P=len(du); qp=np.exp(2j*np.pi*np.array(q)/8)
    A0=8*np.einsum('n,nr,nij->rij',w,ph-1,D0)
    A1=8*np.einsum('n,nr,nij->rij',w,ph,D0)
    vals=np.zeros((P,P),complex)
    for a in range(P):
      for b in range(P):
        # plus a, minus b (basis vectors themselves real).
        for r in range(4):
          z0=F0[r,1:]/np.linalg.norm(F0[r,1:])
          rho=np.linalg.norm(F0[r,1:])
          bA=bz[a,r]; bB=bz[b,r].conj()
          thA=th[a,r];thB=th[b,r].conj()
          u2=np.r_[0,dr[a,r]*bB+dr[b,r].conj()*bA-rho*np.dot(bA,bB)*z0]
          VA=cross((1-qp[r])*np.cross(z0,bA))
          VB=cross((1-qp[r].conj())*np.cross(z0,bB))
          # mixed second derivative of canonical sphere transport then spin
          v2=(qp[r]-qp[r].conj())*np.cross(bA,bB)
          Z0=cross(z0)
          R2=thA*cross(bB)+thB*cross(bA)+thA*thB*(Z0@Z0)+thA*(Z0@VB)+thB*(Z0@VA)+cross(v2)+(VA@VB+VB@VA)/2
          matR2=np.zeros((4,4),complex); matR2[1:,1:]=R2
          WA=Wp[a,r]; WB=Wp[b,r].conj()
          GA=ext(WA); GB=ext(WB)
          ext2=ext(matR2-(WA@WB+WB@WA)/2)+(GA@GB+GB@GA)/2
          mat=create(du[a,r])@GB+create(du[b,r].conj())@GA+create(F0[r])@ext2
          vals[a,b]+=np.trace(A0[r]@create(u2))+np.trace(A1[r]@mat)
    return 2*(vals.T+vals.conj())

def field_H(q,keep=False):
    t=time.time()
    pars,du,bz,dr,th,Wp=field_basis(q)
    dv,inds=first_D(q,du,Wp)
    xv=D0[inds,None]@dv+dv@D0[:,None]
    gap=energies[inds]-energies
    same=np.abs(gap)<1e-10
    kapdiv=np.where(same,kprime,(kap[inds]-kap)/np.where(same,1,gap))
    # Full physical off-shell matter, not thermal auxiliary.
    coefficients=kapdiv-(shell[inds]*R+shell*R[inds])/128
    direct=np.einsum('naij,nbij,n->ab',dv.conj(),dv,w+w[inds],optimize=True)
    divided=np.einsum('naij,nbij,n->ab',xv.conj(),xv,coefficients,optimize=True)
    curv=direct_second(q,du,bz,dr,th,Wp)
    H=direct+divided+curv
    out=(H+H.conj().T)/2
    if keep: return out, (pars,du,bz,dr,th,Wp,dv,xv,inds,direct,divided,curv)
    return out

if __name__=='__main__':
    q=(3,3,0,0)
    H,data=field_H(q,True)
    pars,du,bz,dr,th,Wp,*_=data
    gauge=[]
    for j in range(3):
        axis=np.eye(3)[j]
        S=cross(axis)
        coeff=np.zeros(len(pars),complex)
        for k,(r,kind,a,vec) in enumerate(pars):
            wr=F0[r,1:]; zr=wr/np.linalg.norm(wr)
            if kind=='tangent':coeff[k]=np.dot(vec,S@wr)
            elif kind=='angle':coeff[k]=(1-np.exp(2j*np.pi*q[r]/8))*np.dot(axis,zr)
        gauge.append(coeff)
    gauge=np.array(gauge).T
    residual=float(la.norm(H@gauge))
    eigen=np.linalg.eigvalsh(H)
    print(json.dumps({
      'scope':'Floating diagnostic only; old full128-rank preparation, no certified inertia/root/nonflat branch',
      'source_ref':'0ff0a93f199a9411fbdf2470d557c6fd6c2ccc02',
      'frequency':q,
      'fixed_positive_frame_matrix_dimension':len(pars),
      'observer_representation_directions_not_numerically_assembled':3,
      'full_thermal_modes':len(modes),
      'exact_field_matrix_or_new_root_proved':False,
      'gauge_residual_float':residual,
      'eigenvalues_float':eigen.tolist()
    },indent=2,sort_keys=True))
