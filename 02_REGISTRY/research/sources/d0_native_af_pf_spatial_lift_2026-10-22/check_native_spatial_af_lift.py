#!/usr/bin/env python3
"""Original A4D six-face + two-CAR native N1 CQ spatial lifting control.

Independent 42-direction local derivatives, two translated ORIGINAL based
stencils, uniform-geometry reduction and nonaveraged site-PF perturbations.
This is a NONSTATIONARY local formula check. The original certified h=1/4
42-root and Golden integer-count convergence are CONSUMED existing theorems;
no full spatial Hessian inverse or exact unequal-PF full4D root is claimed.
"""
from itertools import combinations, product
from decimal import Decimal, localcontext
from pathlib import Path
import argparse, hashlib, json
import numpy as np
from scipy.linalg import expm

PIN={
 "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/RIGOROUS_EXACT42_CERTIFICATE.json":"9f4bdef4c367660539c588db01819330ff0d55b3",
 "02_REGISTRY/gr_assembly/sources/d0_original_golden_moving_mean_j2_2026-10-19/theorem.md":"1eb92875e745bed2b72319ea9de64a3c41a9cc46",
 "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/native42.py":"2ca022e87e18de591fd681645e0d7d18e83183a3",
}
def checkpins(root):
    for name,expect in PIN.items():
        b=(root/name).read_bytes()
        actual=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
        assert actual==expect,("OWNED_INPUT_CHANGED",name,actual)

p=(np.sqrt(5)-1)/2
z0=2**-20
lnphi=np.log(1/p)
eta=np.diag([1,-1,-1,-1])
PAIRS=list(combinations(range(4),2))
G2=np.array([eta[i,i]*eta[j,j] for i,j in PAIRS])
STAR=np.zeros((6,6))
ORIGINAL_STAR_MAP={
 (0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
 (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}
for a,(b,sgn) in ORIGINAL_STAR_MAP.items():
    STAR[PAIRS.index(b),PAIRS.index(a)]=sgn
SITES=list(product(range(3),repeat=3))
I=np.eye(4,dtype=complex)
L=[]
for k in range(1,4):
    X=np.zeros((4,4));X[0,k]=X[k,0]=1;L.append(X)
for i,j in ((1,2),(1,3),(2,3)):
    X=np.zeros((4,4));X[i,j]=1;X[j,i]=-1;L.append(X)

rng=np.random.default_rng(43)
E={};U={};psi={}
for t in range(3):
    e=np.array([[1,.01,0,0],[0,1.1,0,0],
                [0,0,1.02,0],[0,0,0,.93]],complex)
    e+=rng.normal(0,.003,(4,4))
    words=[]
    for r in range(4):
        X=sum(float(v)*b for v,b in zip(rng.normal(0,.06,6),L))
        words.append(expm(.25*X))
    for xyz in product(range(4),repeat=3):
        E[t,xyz]=e.copy()
        U[t,xyz]=np.asarray(words,dtype=complex).copy()
        psi[t,xyz]=np.array([.02*t+.002*t*t,
                              .014*t+.023*xyz[0]],complex)
h=.25; tau=.05

def shift(node,r):
    t,xyz=node
    if r==0:return t+1,xyz
    xyz=list(xyz);xyz[r-1]+=1
    return t,tuple(xyz)
def parity(seq):
    return -1 if sum(seq[i]>seq[j] for i in range(4)
                     for j in range(i+1,4))%2 else 1

def source_action(rho):
    total=0j
    for t in (0,1):
        for xyz in SITES:
            node=t,xyz
            e=E[node]
            words=U[node]
            f=0j
            for r,s in PAIRS:
                a=U[shift(node,r)][s]
                b=U[shift(node,s)][r]
                H=words[r]@a@np.linalg.inv(b)@np.linalg.inv(words[s])
                curv=(H-np.linalg.inv(H))/2
                T=curv@eta
                c=np.array([T[i,j] for i,j in PAIRS])
                ii,jj=[k for k in range(4) if k not in (r,s)]
                wedge=np.array([e[a,ii]*e[b,jj]-e[b,ii]*e[a,jj]
                                for a,b in PAIRS])
                f+=parity((r,s,ii,jj))*(wedge*G2)@(STAR@c)
            f/=h*h
            inv=np.linalg.inv(e.T@eta@e)
            q=0j
            for a in range(2):
                grad=np.array([(psi[shift(node,r)][a]-psi[node][a])/h
                               for r in range(4)])
                q+=grad@inv@grad
            rr=rho[t,*xyz]
            x=-tau*f/rr;y=tau*q/rr
            e0=p*p*(1+x);ell=4*e0*(1-e0)
            v=p-p*p*y;bb=4*v*v*(1-v*v)
            aa=ell+(1-ell)*bb
            click=1-(1-z0*aa)*(1-z0*bb)
            # Actual two-band N1 entropy, positive readiness factor omitted
            # ONLY as one global nonzero source multiplier.
            F=(click*np.log(click)+(1-click)*np.log(1-click))/lnphi
            total+=rr*F
    return total

def gradient_one(node,what,price,step=1e-20):
    typ,ij=what
    if typ=="e":
        i,j=ij
        old=E[node][i,j]
        E[node][i,j]=old+1j*step
        ans=source_action(price).imag/step
        E[node][i,j]=old
    elif typ=="U":
        i,j=ij
        old=U[node][i].copy()
        U[node][i]=expm(1j*step*L[j])@old
        ans=source_action(price).imag/step
        U[node][i]=old
    else:
        i=ij[0];old=psi[node][i]
        psi[node][i]=old+1j*step
        ans=source_action(price).imag/step
        psi[node][i]=old
    return float(ans)

def uniform_derivative(what,price,step=1e-20):
    typ,ij=what
    backups={}
    for xyz in product(range(4),repeat=3):
        node=1,xyz
        if typ=="e":
            backups[node]=E[node][ij]
            E[node][ij]+=1j*step
        elif typ=="U":
            i,j=ij
            backups[node]=U[node][i].copy()
            U[node][i]=expm(1j*step*L[j])@U[node][i]
        else:
            i=ij[0];backups[node]=psi[node][i]
            psi[node][i]+=1j*step
    ans=source_action(price).imag/(step*len(SITES))
    for node,old in backups.items():
        if typ=="e":E[node][ij]=old
        elif typ=="U":U[node][ij[0]]=old
        else:psi[node][ij[0]]=old
    return float(ans)

def af_bounds():
    out=[]
    with localcontext() as ctx:
        ctx.prec=95
        pd=(Decimal(5).sqrt()-1)/2
        ph=1/pd
        ainfty=ph/Decimal(5).sqrt()
        for n in (256,512,1024,1536,2048,2304):
            k=n//4
            an=ainfty+((-1) if n%2 else 1)*pd**(2*n+1)/Decimal(5).sqrt()
            eps=pd**(2*(n-2*k)+1)/Decimal(5).sqrt()
            diam=2*pd**(k//4)
            diff=(Decimal(4)**4*eps+128*Decimal(4)*diam+
                  abs(an-ainfty))/an
            ready=2*pd**3*an
            out.append({"original_cost_depth":n,
                        "all_4D_site_PF_delta_bound":format(diff,".9E"),
                        "real_ready_fraction":format(ready,".14f")})
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",type=Path)
    ap.add_argument("--json",type=Path)
    opts=ap.parse_args()
    if opts.repo:checkpins(opts.repo)
    coords=([("e",(a,b)) for a in range(4) for b in range(4)]+
            [("U",(axis,k)) for axis in range(4) for k in range(6)]+
            [("psi",(k,)) for k in range(2)])
    assert len(coords)==42
    rho=np.ones((2,3,3,3))
    at_a=np.array([gradient_one((1,(1,1,1)),c,rho) for c in coords])
    at_b=np.array([gradient_one((1,(2,2,2)),c,rho) for c in coords])
    err=float(np.max(abs(at_a-at_b)))
    assert err<1e-10,err
    uniform_checks=[]
    for k in (0,2,16,22,40,41):
        d=abs(uniform_derivative(coords[k],rho)-at_a[k])
        assert d<1e-10,(k,d)
        uniform_checks.append(float(d))
    controls=[]
    for delta in (.01,.001,.0001):
        uneven=np.ones_like(rho)
        for t in (0,1):
            for xyz in SITES:
                uneven[t,*xyz]=1+delta*(-1)**(t+sum(xyz))
        gs=np.array([gradient_one((1,(1,1,1)),c,uneven)
                     for c in coords])
        differ=float(np.max(abs(gs-at_a)))
        controls.append({"sup_PF_perturbation":delta,
                         "full42_local_source_change":differ,
                         "change_over_PF_delta":differ/delta})
    assert controls[0]["full42_local_source_change"]>5*controls[1]["full42_local_source_change"]
    assert controls[1]["full42_local_source_change"]>5*controls[2]["full42_local_source_change"]
    result={
      "status":"PASS_ORIGINAL_4D_LOCAL_42_EULER_SPATIAL_LIFT",
      "h":"1/4",
      "exact_h4_42_root":"CONSUMED_CERTIFIED_NOT_REPLAYED",
      "uniform_PF_two_free_site_42_source_match_error":err,
      "uniform_replication_source_checks":uniform_checks,
      "diagnostic_spatial_PF_perturbations":controls,
      "actual_integer_AF_depth_bound":af_bounds(),
      "scope":{
        "original_based_six_faces":True,
        "original_two_real_CAR_gradients":True,
        "original_N1_two_band_golden_function":True,
        "actual_integer_count_convergence_consumed":True,
        "synthetic_uneven_PF_used_in_derivative_test":True,
        "true_integer_counts_not_enumerated":True,
        "fully_nonuniform_four_dimensional_exact_root":False,
        "full_spatial_Euler_Hessian_inverse_proved":False,
        "actual_full_Book03_selected":False,
        "GR_closed":False}}
    resulttxt=json.dumps(result,indent=2)+"\n"
    print(resulttxt,end="")
    if opts.json:opts.json.write_text(resulttxt)

if __name__=="__main__":main()
