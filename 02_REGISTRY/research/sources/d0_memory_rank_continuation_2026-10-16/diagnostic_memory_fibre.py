#!/usr/bin/env python3
"""Floating diagnostic ONLY: not a native kernel, inertia or bifurcation proof.
Recomputes all4096 heat modes. Approximate root midpoint; no files written.
Exact continuation theorem and its checker do not depend on these numbers.
"""
from pathlib import Path
import importlib.util,hashlib,json
import numpy as np, scipy.linalg as la
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[4]
OWNER=ROOT/'02_REGISTRY/research/sources/d0_native_memory_source_2026-10-16/diagnostic_old_frequency.py'
raw=OWNER.read_bytes()
if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!='82e179e9ae774e004530034ca5d89c85bd708509':
    raise ValueError('Changed diagnostic parent')
spec=importlib.util.spec_from_file_location('owned_full_frequency_diagnostic',OWNER)
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
def matter_matrix(q,data):
 pars,du,bz,dr,th,Wp,dv,xv,inds,*_=data
 n=len(pars); mm=np.zeros((n,n,16,16),complex)
 for k in np.where(d.shell)[0]:
  l=inds[k]
  left=dv[k]; X=xv[k]
  mm += (np.einsum('aji,bjk->abik',left.conj(),left)-d.R[l]*np.einsum('aji,bjk->abik',X.conj(),X))/8
 for k in np.where(d.shell[inds])[0]:
  left=dv[k];X=xv[k]
  mm += (np.einsum('bij,akj->abik',left,left.conj())-d.R[k]*np.einsum('bij,akj->abik',X,X.conj()))/8
 # second actual chart jet, computed as an operator coefficient of sigma
 qp=np.exp(2j*np.pi*np.array(q)/8)
 B0=4/8*np.einsum('nr,nij->rij',d.ph[d.shell]-1,d.D0[d.shell])
 B1=4/8*np.einsum('nr,nij->rij',d.ph[d.shell],d.D0[d.shell])
 vals=np.zeros_like(mm)
 for a in range(n):
  for b in range(n):
   for r in range(4):
    z0=d.F0[r,1:]/np.linalg.norm(d.F0[r,1:]);rho=np.linalg.norm(d.F0[r,1:])
    bA=bz[a,r];bB=bz[b,r].conj(); thA=th[a,r];thB=th[b,r].conj()
    u2=np.r_[0,dr[a,r]*bB+dr[b,r].conj()*bA-rho*np.dot(bA,bB)*z0]
    VA=d.cross((1-qp[r])*np.cross(z0,bA));VB=d.cross((1-qp[r].conj())*np.cross(z0,bB))
    v2=(qp[r]-qp[r].conj())*np.cross(bA,bB);Z0=d.cross(z0)
    R2=thA*d.cross(bB)+thB*d.cross(bA)+thA*thB*(Z0@Z0)+thA*(Z0@VB)+thB*(Z0@VA)+d.cross(v2)+(VA@VB+VB@VA)/2
    matR2=np.zeros((4,4),complex);matR2[1:,1:]=R2
    WA=Wp[a,r];WB=Wp[b,r].conj();GA=d.ext(WA);GB=d.ext(WB)
    ext2=d.ext(matR2-(WA@WB+WB@WA)/2)+(GA@GB+GB@GA)/2
    mat=d.create(du[a,r])@GB+d.create(du[b,r].conj())@GA+d.create(d.F0[r])@ext2
    C=d.create(u2)
    vals[a,b]+=B0[r]@C+C@B0[r]+B1[r]@mat+mat@B1[r]
 mm+=2*(vals.transpose(1,0,2,3)+vals.conj().transpose(0,1,3,2))
 mm=(mm+mm.conj().transpose(1,0,3,2))/2
 return mm

def run():
    q=(3,3,0,0)
    H,data=d.field_H(q,True);M=matter_matrix(q,data)
    thermal=H-np.trace(M,axis1=2,axis2=3)/16
    pars,du,bz,dr,th,Wp,*_=data
    gauge=[]
    for j in range(3):
        axis=np.eye(3)[j];S=d.cross(axis);coeff=np.zeros(len(pars),complex)
        for k,(r,kind,a,vec) in enumerate(pars):
            wr=d.F0[r,1:];zr=wr/np.linalg.norm(wr)
            if kind=='tangent':coeff[k]=np.dot(vec,S@wr)
            elif kind=='angle':coeff[k]=(1-np.exp(2j*np.pi*q[r]/8))*np.dot(axis,zr)
        gauge.append(coeff)
    gauge=np.array(gauge).T;P=la.null_space(gauge.conj().T)
    chi=np.zeros(16);chi[1]=1/np.sqrt(2);chi[15]=-1/np.sqrt(2)
    Hs=thermal+np.einsum('i,j,abji->ab',chi,chi,M)
    A=P.conj().T@H@P;B=P.conj().T@(Hs-H)@P
    t0=brentq(lambda t:la.eigvalsh(A+t*B)[1],0.,1.,xtol=1e-13)
    ev,U=la.eigh(A+t0*B);v=P@U[:,1]
    Mv=np.einsum('a,b,abij->ij',v.conj(),v,M);Mv=(Mv+Mv.conj().T)/2
    Js=[]
    for r in [1,2,3]:
        W=np.zeros((4,4),complex);W[1:,1:]=d.cross(d.F0[r,1:])
        g=W@np.sum(d.F0,axis=0);u=d.F0[r]
        Js.append((d.create(g)+d.annih(g))@(d.create(u)-d.annih(u)))
    G=np.array([[np.trace(j@k).real for k in Js] for j in Js])
    vec=np.array([np.trace(j@Mv).real for j in Js])
    proj=np.trace(Mv).real*np.eye(16)/16+sum((b*j for b,j in zip(la.solve(G,vec),Js)),np.zeros((16,16),complex))
    return {'schema':'d0-memory-fibre-flow-diagnostic/1','scope':'Floating exploration, no interval inertia, exact root or bifurcating solution certified',
      'frequency':list(q),'thermal_modes':4096,'Fock_dimension':16,
      'reference_dimension':128,'preparation':'(1-t)I16/16+t|whitened_seed><whitened_seed|',
      'candidate_t_float':float(t0),'transverse_slope_float':float(np.vdot(U[:,1],B@U[:,1]).real),
      'zero_eigen_residual_float':float(la.norm((A+t0*B)@U[:,1])),
      'fibre_obstruction_HS_norm_float':float(la.norm(Mv-proj)),
      'operator_HS_norm_float':float(la.norm(Mv)),
      'old_gauge_residual_float':float(la.norm(H@gauge)),
      'new_gauge_residual_float':float(la.norm(Hs@gauge)),
      'new_curved_native_root_proved':False,
      'diagnostic_used_by_exact_certificate':False}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
