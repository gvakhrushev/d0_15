"""Short-winding full Hodge heat localized on the physical NPS2 register."""
from fractions import Fraction as F
import json
import math
import numpy as np
from check_clock_coherence import mm
from check_shared_site_union import curvature
from check_source_price import load_control, need


def halo(x, n):
    return x**n/math.factorial(n)/(1-x/(n+1))


def scene():
    groups=np.repeat(np.arange(3),(9,11,13))
    A=(groups[:,None]!=groups[None,:]).astype(float)
    d=A.sum(1)+2
    r=1/np.sqrt(d)
    B=r[:,None]*A*r[None,:]
    C=np.diag(1/d)
    return B,C


def scene_heat(B,C,lam,beta):
    v,U=np.linalg.eigh(np.eye(33)-B-lam*C)
    return mm(U*np.exp(-beta*v)[None,:],U.T)


def build(ne,m):
    gt=ne.Gate
    t=gt("CX",(0,1)); enc=gt("CX",(1,2))
    gates=(t,enc,gt("G",(2,)))+(t,t)*m+(enc,)
    spec=ne.Execution(3,(),(),gates,report_bits=(1,2))
    raw=ne.execution_from_json(ne.canonical_json(spec),max_qubits=3,max_expanded_stages=len(gates))
    gates=[np.array(ne.gate_matrix(raw,g,max_qubits=3,max_expanded_stages=len(raw.gates)),dtype=float)
           for g in raw.gates]
    v=np.array([[float(ne.A)],[float(ne.P)]])
    births=[np.kron(np.eye(2),v),np.kron(np.eye(4),v)]
    stages=births+gates[:-1]
    passive=births+[np.eye(8) for _ in gates[:-1]]
    dims=[2]+[x.shape[0] for x in stages]
    at=np.cumsum([0]+dims)
    cuts=[slice(at[j],at[j+1]) for j in range(len(dims))]
    D=int(at[-1]); T=np.zeros((D,D))
    for j,f in enumerate(stages):
        T[cuts[j+1],cuts[j]]=f
    for j,d in enumerate(dims):
        emb=np.eye(d)
        for b in passive[j:]:
            emb=mm(b,emb)
        extra=np.eye(d) if j==0 else np.eye(d)-mm(passive[j-1],passive[j-1].T)
        T[cuts[j],cuts[-1]]+=mm(extra,emb.T,gates[-1])
    V=mm(births[1],births[0])
    bare=V.copy()
    for g in gates:
        V=mm(g,V)
    cold=mm(bare.T,V)
    z=2**-20
    J=-np.linalg.slogdet((1-z)*np.eye(2)+z*mm(cold.T,cold))[1]
    need(np.linalg.norm(mm(T.T,T)-np.eye(D))<1e-12,"genuine unitary including terminal complement")
    return T,cuts,gates[-1],V,float(J)


def main():
    ne,digest=load_control()
    B,C=scene(); p=float(ne.P); beta=2*p*p; x=beta/11
    # Trapezoid aliasing only for temporal displacement of magnitude >=128.
    # Its uniform operator error is bounded by 2*halo(x,128).
    quadrature=128
    Sinf=sum(scene_heat(B,C,2*math.cos(2*math.pi*j/quadrature),beta)
             for j in range(quadrature))/quadrature
    need(np.ptp(Sinf.diagonal())>1e-5 and np.linalg.eigvalsh(Sinf).min()>math.exp(-2*beta),
         "actual positive nonscalar spatial average")
    s=float(Sinf[32,32]); zinf=359+2*float(Sinf.trace())
    rows={}
    for m in (0,1,2):
        T,cuts,g,V,J=build(ne,m)
        D=len(T); L=4+2*m
        power=np.eye(D)
        for k in range(1,L+1):
            power=mm(power,T)
            norms=[np.linalg.norm(power[c,c]) for c in cuts]
            need((max(norms)<1e-12) if k<L else (max(norms)>1e-3),"shortest physical return at each stage")
        eigen,W=np.linalg.eigh(T+T.T)
        heat_modes=[scene_heat(B,C,q,beta) for q in eigen]
        Z=359*D+2*sum(h.trace() for h in heat_modes)
        local=mm(W*np.array([h[32,32] for h in heat_modes])[None,:],W.T)
        c=cuts[-1]
        K=mm(g,local[c,c],g.T)
        err=2*halo(x,L)
        need(np.linalg.norm(K-s*np.eye(8),ord=2)<err+5e-14,"true post-final coordinate compression")
        need(abs(Z/D-zinf)<=66*err+1e-12,"complete two-grade trace oracle")
        # Full old T and an untouched reference are entangled, no supplied value for economic work.
        old=np.array([1,0,0,1])/np.sqrt(2)
        out=mm(np.kron(V,np.eye(2)),old)
        gram=np.outer(out,out)
        marks=[np.diag(v) for v in ((1,1,0,0),(0,0,1,0),(0,0,0,1))]
        raw=[]; lifted=[]
        for idx,mask in enumerate(marks):
            proj=np.kron(np.eye(2),np.kron(mask,np.eye(2)))
            block=mm(proj,gram,proj)
            native=float(block.trace())
            observed=float(np.trace(mm(np.kron(K,np.eye(2)),block)))
            need(abs(observed-s*native)<=err*native+5e-14,"all true fine marks and reference")
            if idx==2:
                need(native<1e-26 and abs(observed)<1e-26,"actual forbidden code retained")
            raw.append(native);lifted.append(observed)
        full=math.exp(J)*Z
        push=math.exp(J)*(D*zinf/s)*sum(lifted)
        need(abs(push/full-1)<=err/s+66*err/(359)+1e-12,"full partition with its actual determinant")
        rows[str(m)]={"clock_dimension":D,"shortest_return":L,"declared_heat_modes":425*D,
          "absolute_local_error_analytic_upper":f"{err:.9e}",
          "normalized_terminal_probabilities":[round(v,11) for v in raw]}
    f0,f1=curvature(F(1,5)),curvature(F(1,4))
    need(f1>f0>0,"genuine off-shell CAR curvature values")
    print(json.dumps({"status":"PASS","native_source_sha256":digest,"spectral_fixtures":rows,
        "true_geometric_CAR_curvatures":[str(f0),str(f1)],
        "full_eight_bank_compilation_replayed":False,
        "nonconstant_spatial_factor":True,
        "actual_scene_vertex_32_weight":round(s,10),
        "all_mode_density_including_grade_one":round(zinf,10),
        "role":"graphical Born-mark disintegration with controlled source; no microscopic price assignment"},
        sort_keys=True,indent=2))


if __name__=="__main__":
    main()
