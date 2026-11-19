"""Genuine growing clock, pinching of the noisy event, and the LIVE Bellman corner."""
from fractions import Fraction as F
import json
import numpy as np
from check_extra_work import span
from check_source_price import load_control, need


def mm(*terms):
    value=terms[0]
    for other in terms[1:]:
        contraction={(2,2):"ij,jk->ik",(2,1):"ij,j->i",(1,2):"i,ij->j",(1,1):"i,i->"}
        value=np.einsum(contraction[value.ndim,other.ndim],value,other,optimize=False)
    return value


def clock():
    ne,digest=load_control()
    gt=ne.Gate
    cx=gt("CX",(0,1)); enc=gt("CX",(1,2))
    gates=(cx,enc,gt("G",(2,)),enc)
    spec=ne.Execution(3,(),(),gates,report_bits=(1,2))
    raw=ne.execution_from_json(ne.canonical_json(spec),max_qubits=3,max_expanded_stages=4)
    gate=[np.array(ne.gate_matrix(raw,g,max_qubits=3,max_expanded_stages=4),dtype=np.longdouble) for g in raw.gates]
    p=float(ne.P); v=np.array([[float(ne.A)],[p]],dtype=np.longdouble)
    births=[np.kron(np.eye(2),v),np.kron(np.eye(4),v)]
    # F_j are the real active maps; B_j are the passive canonical stage inclusions.
    stages=births+gate[:-1]
    passive=births+[np.eye(8) for _ in gate[:-1]]
    dims=[2]+[f.shape[0] for f in stages]
    offsets=np.cumsum([0]+dims)
    def sl(j):
        return slice(offsets[j],offsets[j+1])
    total=offsets[-1]
    T=np.zeros((total,total),dtype=np.longdouble)
    for j,f in enumerate(stages):
        T[sl(j+1),sl(j)]=f
    for j,d in enumerate(dims):
        embedding=np.eye(d)
        for b in passive[j:]:
            embedding=mm(b,embedding)
        detail=np.eye(d) if j==0 else np.eye(d)-mm(passive[j-1],passive[j-1].T)
        T[sl(j),sl(len(dims)-1)]+=mm(detail,embedding.T,gate[-1])
    need(np.linalg.norm(mm(T.T,T)-np.eye(total))<1e-12,"all birth complements and final gate")
    adjacency=T+T.T
    need(np.linalg.norm(adjacency[sl(1),sl(0)]-births[0])<1e-12,"genuine undoubled birth block")
    Q=np.kron(np.eye(2),np.diag([0,1]))
    for P in (np.zeros((2,2)),np.eye(2),np.diag([0,1]),np.ones((2,2))/2):
        defect=mm(Q,births[0])-mm(births[0],P)
        need(np.linalg.norm(mm(defect.T,defect)-(p*p*(np.eye(2)-P)+(1-p*p)*P))<1e-12,
             "sharp birth-event intertwining defect")
    # On this interior ordinary edge the only two-stage coupling is the true CX.
    A=adjacency[sl(2),sl(3)]
    need(np.linalg.norm(A-gate[0].T)<1e-12,"true noisy CX block")
    E=np.diag([int(((k>>2)&1)^((k>>1)&1)) for k in range(8)])
    angle_samples=(0.27,p*p,0.49)
    for l in angle_samples:
        psi=np.kron(np.kron(np.array([1.,0.]),np.sqrt([1-l,l])),v[:,0])
        post=mm(gate[0],psi)
        need(abs(mm(post,E,post)-l)<1e-12,"true retained error D xor T")
        for sign in (1,-1):
            ket=np.zeros(total,dtype=np.longdouble); ket[sl(2)]=psi/np.sqrt(2); ket[sl(3)]=sign*post/np.sqrt(2)
            P=np.zeros_like(T); P[sl(3),sl(3)]=E
            rho=np.outer(ket,ket); perp=np.eye(total)-P; pin=mm(P,rho,P)+mm(perp,rho,perp)
            # Compression of G13 at one spatial vertex of degree 20: C_s=1/22.
            delta=np.eye(total)-adjacency/22
            need(abs(np.trace(mm(delta,rho-pin))+sign*l/22)<1e-12,"real local energy defect")
            need(abs(np.trace(mm(rho,P))-l/2)<1e-12,"same dephasing entropy for both trial phases")
    return digest,int(total)


def arithmetic():
    p=(span(5).sqrt()-1)/2
    ell=(1/p).log_positive()
    beta=2*p**2
    tc=2*p-1
    for _ in range(9):
        tc=2*tc**2-1
    q=p**2+2*p**10*(1-tc)
    def inf0(x,m):
        h=(x*(1/x).log_positive()+(1-x)*(1/(1-x)).log_positive())/ell
        return -(1/(1-x)).log_positive()/ell+2*h-(m+1)*x
    # At p^2 use the exact recurrence p^2=1-p and h_phi(p^2)=1+p^2.
    need((inf0(p**2,4)+p**4).lo<0<(inf0(p**2,4)+p**4).hi,"native -p^4")
    a,b=inf0(q,3),inf0(q,4)
    need(a.lo>0 and b.hi<0,"first four-copy LIVE negative on the actual PC13")
    return {"beta_p_over_22":(beta*p/22).fmt(15),
            "two_stage_thermal_source_separation":(2*beta/22).fmt(15),
            "pc13_q":q.fmt(15),"live_I0_M3":a.fmt(15),"live_I0_M4":b.fmt(15),
            "live_I0_M4_at_q_p_squared":"-p^4",
            "additional_zero_minus_one_mean_work_needed_at_M4":((-b)/q).fmt(13)}


if __name__=="__main__":
    digest,d=clock()
    print(json.dumps({"status":"PASS","primary_native_sha256":digest,"complete_clock_dimension":d,
        "local_hamiltonian_check":"numeric full clock with all complements; analytic proof in note",
        "price_binding":"single cut variational deficit only; no physical edge-value assignment",
        **arithmetic()},indent=2,sort_keys=True))
