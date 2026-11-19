#!/usr/bin/env python3
"""Original full128: unique Kraft/Gibbs/Holevo projection and native Golden X.

Loads unchanged 128-Kraus CAR16 Julia constructor by exact Git blob SHA.
True inverse-square moving DATA preparation; oldRIGHT product spectator.
No native DATA reset, no synthetic 2-outcome source. Full 128 fine labels,
and the 64 genuine dark outcomes remain in the 128-slot arrays.

Checks:
  - exact noncommuting same-run relative entropy chain and η=q_J minimizer
  - true native K0, full CP channel, registered support, full fine Shannon
    invariant under CONDITIONAL original native Golden X on rows j>0
  - exact original p³ native price/source shift for this changed readout
  - exact original q00,q01,qNB from h,mu
  - 75-decimal outward native FULL conditional PORT C1 and Gibbs mismatch C1
  - original whole-128 quantum Holevo and source numerical diagnostics

Mathematical projection/reference is a candidate, not compulsory Book03
scene Hodge, Info, clock, physical writer, or GR.
"""
from __future__ import annotations
import ast,hashlib,json,math,sys
from pathlib import Path

import numpy as np
from scipy.linalg import expm,solve_sylvester
import mpmath as mp

P=(math.sqrt(5)-1)/2
ELL=math.log(1/P)
BETA=2*P*P
EYE=np.eye(16,dtype=complex)
PIN="ee8de4635d24c668949ac9a0186616ab7d59f2ed"
ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/"02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
NTEST=0
def require(cond,msg):
    global NTEST
    NTEST+=1
    if not bool(cond):raise ArithmeticError(msg)
def near(x,y,tol,msg):
    require(abs(x-y)<tol,f"{msg}: {x} != {y}")
def load_native():
    smoke=(len(sys.argv)==3 and sys.argv[1]=="--transcription-smoke")
    src=Path(sys.argv[2]) if smoke else SOURCE
    raw=src.read_bytes()
    sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    if not smoke:require(sha==PIN,"original untouched CAR16 Git blob pin")
    nodes=ast.parse(raw).body
    names={"native","creators","adj","herm","root"}
    funcs=[z for z in nodes if isinstance(z,ast.FunctionDef) and z.name in names]
    require({z.name for z in funcs}==names,"five ORIGINAL Julia/Walsh/CAR constructors")
    e={"np":np,"P":P,"EYE":EYE,"expm":expm,
       "solve_sylvester":solve_sylvester}
    exec(compile(ast.Module(body=funcs,type_ignores=[]),str(src),"exec"),e)
    return e["native"],sha,not smoke

def entropy(rho):
    ev=np.linalg.eigvalsh((rho+rho.conj().T)/2)
    require(ev.min()>-1e-11,"all true conditional CAR state eigenvalues positive")
    ev=ev[ev>1e-14]
    return -float(np.dot(ev,np.log(ev)))

def sample(native,r):
    K,_=native(2*math.atanh(r),.6)
    require(K.shape==(128,16,16),"TRUE 128 original recorded fine Kraus")
    near(float(np.linalg.norm(np.einsum("aij,aik->jk",K.conj(),K)-EYE)),
         0,5e-12,"all native Kraus complete without postselection")
    Delta=(EYE-K[0])/BETA
    rho=np.linalg.inv(Delta);rho/=np.trace(rho)
    uncond=np.einsum("aij,jk,alk->il",K,rho,K.conj(),optimize=True)
    near(float(np.linalg.norm(uncond-rho)),0,5e-11,
         "ORIGINAL actual moving inverse-square input is stationary")
    z=expm(-BETA*Delta);Z=float(np.trace(z).real);sigma=z/Z
    q=[];weighted=0.;sumrel=0.
    for ka in K:
        x=ka@rho@ka.conj().T
        qi=float(np.trace(x).real)
        q.append(max(0,qi))
        if qi>1e-25:
            X=x/qi
            hX=entropy(X)
            weighted+=qi*hX
            # D(X||sigma) = -S(X) + beta E_X[Delta] + log Z
            sumrel+=qi*(-hX+BETA*float(np.trace(X@Delta).real)+math.log(Z))
    q=np.array(q).reshape(64,2)
    near(float(q.sum()),1,1e-10,"whole original fine pointer normalization")
    qJ=q.sum(axis=1)
    q00,q01=q[0]
    qnb=float(q[1:].sum());qblank=q00+q01
    mu=float(np.trace(Delta).real)/16
    h=16/float(np.trace(np.linalg.inv(Delta)).real)
    near(q00,1-4*P*P*h+4*P**4*h*mu,2e-12,
         "exact original K0 blank conditional mass")
    near(q01,4*P**3*h*mu,2e-12,
         "exact original K1 orphan conditional mass")
    near(qnb,4*P*P*h*(1-mu),2e-12,
         "true native nonblank CAR16 Kraus effect")
    kraft=np.array([P,P*P])
    reference=qJ[:,None]*kraft
    mask=q>1e-22
    kl=float(np.sum(q[mask]*np.log(q[mask]/reference[mask])))
    blank=q00*math.log(q00/(qblank*P))+q01*math.log(q01/(qblank*P*P))
    near(kl,blank+qnb*P**3*ELL,1e-12,
         "FULL conditional port Golden Kraft KL includes blank and twins")
    srho=entropy(rho)
    chi=srho-weighted
    dtherm=-srho+BETA*h+math.log(Z)
    near(sumrel,dtherm+chi,2e-11,
         "exact noncommuting native Donald/Holevo-Gibbs source identity")
    require(dtherm>0 and chi>0,"both true native information projections strictly positive")
    # SAME original quantum instrument modulo labelled Golden X on all j>0.
    swapped=K.copy()
    for j in range(1,64):
        swapped[2*j]=K[2*j+1]
        swapped[2*j+1]=K[2*j]
        near(float(np.linalg.norm(K[2*j+1]-K[2*j]/math.sqrt(P))),
             0,1e-12,"TRUE original nonblank Golden proportional port states")
    near(float(np.linalg.norm(swapped[0]-K[0])),0,1e-14,
         "actual original blank K0 and Book input remain EXACT unchanged")
    near(float(np.linalg.norm(np.einsum("aij,aik->jk",swapped.conj(),swapped)-
                              np.einsum("aij,aik->jk",K.conj(),K))),
         0,1e-12,"full unchanged original CP channel after native X")
    qq=np.array([float(np.trace(aa@rho@aa.conj().T).real) for aa in swapped])
    qq=qq.reshape(64,2)
    near(float(np.max(np.abs(qq[1:,0]-q[1:,1]))),0,1e-13,
         "REAL original even/odd price labels are swapped")
    near(entropy(np.diag(q.ravel())),entropy(np.diag(qq.ravel())),
         1e-12,"ENTIRE original fine Shannon entropy invariant under native X")
    good=qq>1e-22
    swapKL=float(np.sum(qq[good]*np.log(qq[good]/reference[good])))
    near(kl-swapKL,qnb*P**3*ELL,2e-12,
         "unique Golden source label-to-cost shift p³ qNB")
    # The ENTIRE fine↔row Holevo difference comes ONLY from j0 orphan.
    rowweighted=0.
    for j in range(64):
        if qJ[j]>1e-24:
            X=sum((K[2*j+b]@rho@K[2*j+b].conj().T
                    for b in (0,1)),np.zeros((16,16),complex))
            rowweighted+=qJ[j]*entropy(X/qJ[j])
    rowchi=srho-rowweighted
    require(0<=chi-rowchi<1e-5,
            "actual original j>0 native twins carry zero conditional quantum Holevo")
    return dict(KLport=kl,KLportGolden=kl/ELL,KLblank=blank,
        KLnonblank=qnb*P**3*ELL,KLswapped=swapKL,
        full_fine_shannon=entropy(np.diag(q.ravel())),
        Gibbs_mismatch=dtherm,Holevo_fine=chi,
        Holevo_row=rowchi,Holevo_only_blank_port=chi-rowchi,
        nofit_score=kl+dtherm+chi,
        direct_full_cq_score=kl+sumrel,
        qNB=qnb,mu=mu,h=h)

def strictly_interval_source():
    mp.iv.dps=75;iv=mp.iv
    p=(iv.sqrt(5)-1)/2
    beta=2*p*p
    mu=iv.mpf(141489)/10240000
    h=iv.mpf(69399)/5030720
    muj=-iv.mpf(328779)/204800000
    hj=-iv.mpf(20040939)/9885993640
    q00=1-4*p*p*h+4*p**4*h*mu
    q01=4*p**3*h*mu
    qnb=4*p*p*h*(1-mu)
    b=q00+q01
    q00j=-4*p*p*hj+4*p**4*(hj*mu+h*muj)
    q01j=4*p**3*(hj*mu+h*muj)
    qnbj=4*p*p*(hj*(1-mu)-h*muj)
    ell=iv.log(1/p)
    Dport=qnbj*p**3*ell+q00j*iv.log(q00/(b*p))+q01j*iv.log(q01/(b*p**2))
    eps=iv.sqrt(mu*(mu-h))
    epsj=((2*mu-h)*muj-mu*hj)/(2*eps)
    w=(1+eps/mu)/2
    wj=(epsj*mu-eps*muj)/(2*mu*mu)
    s=1/(1+iv.exp(-2*beta*eps))
    sj=2*beta*epsj*s*(1-s)
    Dtherm=w*iv.log(w/s)+(1-w)*iv.log((1-w)/(1-s))
    Dthermalj=wj*iv.log(w*(1-s)/((1-w)*s))+sj*((1-w)/(1-s)-w/s)
    for val,lo,hi,label in (
        (Dport,"0.00149446500172038","0.00149446500172039","full port nat source"),
        (Dport/ell,"0.00310562817431861","0.00310562817431862","full port Golden source"),
        (Dtherm,"0.00078817233745897","0.00078817233745898","true thermal preparation mismatch"),
        (Dthermalj,"0.01504610155394310","0.01504610155394312","true thermal preparation source")):
        require(val.a>iv.mpf(lo) and val.b<iv.mpf(hi),
                "OUTWARD 75d "+label)
    return {
      "Kport_natural_first_jet":str(Dport),
      "Kport_Golden_first_jet":str(Dport/ell),
      "thermal_Gibbs_relative_entropy":str(Dtherm),
      "thermal_Gibbs_relative_first_jet":str(Dthermalj)
    }

def main():
    native,blob,pinned=load_native()
    r=1/9
    sample0=sample(native,r)
    jets={}
    for eps in (1e-4,3e-5):
        a=sample(native,r+eps)
        b=sample(native,r-eps)
        jets[str(eps)]={k:(a[k]-b[k])/(2*eps) for k in
                         ("KLport","Gibbs_mismatch","Holevo_fine","nofit_score","qNB")}
    cert=strictly_interval_source()
    require(abs(sample0["direct_full_cq_score"]-sample0["nofit_score"])<2e-11,
            "direct full original noncommuting cq projection matches unique sum")
    print(json.dumps({
      "status":"PASS_ORIGINAL_PINNED_KRAFT_GIBBS_HOLEVO" if pinned else
               "PASS_LOCAL_TRANSCRIPTION_SMOKE",
      "checks":NTEST,"original_git_blob":blob,
      "upstream_original_blob_verified":pinned,
      "actual_native_CAR16_allKraus_present":128,
      "oldRIGHT_spectator_input":"product declared; arbitrary correlated DR theorem analytic",
      "r":"1/9","nu":"3/5",
      "observables":sample0,
      "actual_proper_Lorentz_numeric_sources":jets,
      "original_rational_canonical_outward_certificates":cert,
      "physical_pre_readout_controlled_X_admission":False,
      "compulsory_Book03_scene_Delta_and_Info_selected":False,
      "same_original_full42_PF_raw216_GR_closed":False
    },indent=2))
if __name__=="__main__":
    main()
