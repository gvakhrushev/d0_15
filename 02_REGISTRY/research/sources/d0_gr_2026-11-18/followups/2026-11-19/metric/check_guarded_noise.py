"""Guarded noisy bits: exact Golden masses and a full retained quantum audit."""
from fractions import Fraction as F
from itertools import product
import json
import math

from check_golden_record_race import gold, p
from check_source_price import load_control, need


def geometry(kind,t,d):
    if kind=="paired":
        n=(d!=t)+t
        return 3+n,4+n
    zeros=(2*t+(kind=="cold"))*(1-d)
    return 1+d+zeros,1+2*d+zeros


def powp(n):
    return p**n if n>=0 else gold(1)/(p**(-n))


def exact_check():
    rows={}
    for kind in ("code","cold","paired"):
        for t in (0,1):
            lens,exps=zip(*(geometry(kind,t,d) for d in (0,1)))
            k=sum((p**i for i in lens),gold(0))
            m=sum((p**i for i in exps),gold(0))
            law=(p,p**2) if t==0 else (p**2,p)
            for d in (0,1):
                need((p**lens[d]/k==law[d])==(kind in ("code","paired")),"Kraft match")
                need((p**exps[d]/m==law[d])==(kind in ("cold","paired")),"Born match")
            if kind=="code":
                need(k==p**t,"conditional net price t")
            if kind=="cold":
                need(m==p**(1+t),"true physical reference branch mass")
            if kind=="paired":
                need(k==p**(2+t) and m==p**(3+t),"two roots, same conditional law")
            for size in (1,2,4):
                totalK=totalM=totalP=gold(0)
                for ds in product((0,1),repeat=size):
                    probability=gold(1)
                    for d in ds:
                        probability*=law[d]
                    totalP+=probability
                    km=p**sum(lens[d] for d in ds)
                    bm=p**sum(exps[d] for d in ds)
                    totalK+=km
                    totalM+=bm
                    if kind!="cold":
                        need(km==k**size*probability,"all retained word masses, Kraft")
                    if kind!="code":
                        need(bm==m**size*probability,"all retained word masses, rooted Born")
                need(totalP==gold(1) and totalK==k**size and totalM==m**size,"all leaf checks")
                tilted=gold(0)
                for ds in product((0,1),repeat=size):
                    # Deliberately change the law while keeping full support.
                    mass=gold(F(1,3))**sum(ds)*gold(F(2,3))**(size-sum(ds))
                    tilted+=mass*(p**sum(lens[d] for d in ds)/mass)
                need(tilted==k**size,"conditional Born-averaged exponential and full Kraft mass")
            rows[f"{kind}_{t}"]={"lengths":lens,"born_exponents":exps,
                    "kraft_mass_basis_1_p":k.strings(),"born_mass_basis_1_p":m.strings()}
    for n0,n1 in product(range(5),repeat=2):
        need(powp(2+n1-n0)/powp(1+n1-n0)==p,"zero-only odds invariant")
    need(F(16)*(F(3,5)**3)>1,"two encoded outputs already dominate corrected attenuation")
    return rows


def native_preparation():
    import sympy as sp
    ne,digest=load_control()
    g=ne.Gate
    token=(g("SourceI",(2,0,1)),)*2
    encoder=(g("CX",(2,3)),g("G",(3,)),g("CX",(2,3)))
    def unit(word):
        ex=ne.Execution(4,(),(),word,profile=ne.G_CX_SOURCE_I,
                        source_port=2,source_spin=(0,1),report_bits=(2,3))
        obj=ne.execution_from_json(ne.canonical_json(ex),max_qubits=4,max_expanded_stages=len(word))
        return ne.word_matrix(obj,max_qubits=4,max_expanded_stages=len(word))
    v=sp.Matrix([ne.A,ne.P])
    inp=sp.kronecker_product(sp.eye(4),v,v)
    known=unit(token+(g("G",(2,)),)+token+encoder)
    ideal=sp.kronecker_product(sp.eye(4),sp.Matrix([1,0]),ne.G_LOCAL*v)
    need(ne.exact_matrix_equal(known*inp,ideal),"paid zero outcome on every unknown Spin column")
    w=ne.Execution(3,(),(),(g("CX",(0,2)),g("CX",(1,2))),report_bits=(2,))
    obj=ne.execution_from_json(ne.canonical_json(w),max_qubits=3,max_expanded_stages=2)
    xor=ne.word_matrix(obj,max_qubits=3,max_expanded_stages=2)
    for h,d,b in product(range(2),repeat=3):
        i=4*h+2*d+b
        need(xor[4*h+2*d+(b^h^d),i]==1,"all eight complemented-port columns")
    return digest


def cq_numeric():
    import numpy as np
    def entropy(a):
        vals=np.linalg.eigvalsh(a)
        return -sum(v*math.log(v) for v in vals if v>1e-15)
    phi=(1+math.sqrt(5))/2
    ell=math.log(phi)
    t=1
    lens=[sum(geometry("paired",t,d)[0] for d in ds) for ds in product(range(2),repeat=2)]
    tau=np.array([phi**(-l) for l in lens])
    c=-math.log(tau.sum())/ell
    tau/=tau.sum()
    I=np.eye(3)
    x=np.array([[0,1,0],[1,0,0],[0,0,0]],float)/128
    zz=np.diag([1,-1,0])/128
    rho=np.array([[.6,.15,0],[.15,.4,0],[0,0,0]],float)
    ev,U=np.linalg.eigh(rho)
    root=(U*np.sqrt(ev))@U.T
    def inspect(s):
        dev=(x,-x,zz,-zz)
        effects=[prob*I+s*e for prob,e in zip(tau,dev)]
        need(min(np.linalg.eigvalsh(e).min() for e in effects)>0,"positive effects")
        need(np.linalg.norm(sum(effects)-I)<1e-14,"full conditional instrument")
        omega=[root@e@root for e in effects]
        total=sum(entropy(block) for block in omega)
        work=sum(l*np.trace(block) for l,block in zip(lens,omega))
        divergence=-total+entropy(rho)-sum(np.trace(block)*math.log(prob) for prob,block in zip(tau,omega))
        bound=sum(np.linalg.norm(s*e,2)**2/prob for e,prob in zip(dev,tau))
        need(abs(work-(total-entropy(rho))/ell-c-divergence/ell)<1e-12,"full quantum KL identity")
        need(-1e-12<=divergence<=bound+1e-12,"singular-archive uniform bound")
        return divergence
    need(np.linalg.norm(x@zz-zz@x)>1e-6,"genuine noncommuting changes")
    return {"scope":"floating-point diagnostic; identity and bound proved analytically",
            "rank_old":2,"old_dimension":3,"KL_at_0_half_1":[inspect(s) for s in (0,.5,1)]}


if __name__=="__main__":
    print(json.dumps({"status":"PASS","rows":exact_check(),"native_owner_sha256":native_preparation(),
                      "CQ":cq_numeric(),"full_microprice_binding":False},indent=2))
