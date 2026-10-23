"""Exact finite controls for the positive polynomial Gram-innovation effect.
No native gate admission, no full source-to-Einstein conclusion.
"""
import itertools
import json
import sympy as S

def require(x,description):
    if not bool(x):
        raise RuntimeError(description)

def same(A,B,description):
    require(all(S.simplify(e)==0 for e in (A-B)),description)

def positive_semidefinite(A):
    n=A.rows
    return all(A.extract(q,q).det()>=0 for m in range(1,n+1)
               for q in itertools.combinations(range(n),m))

def run():
    eps=S.Rational(1,100)
    M=S.Matrix([[2,1,0],[1,2,1],[0,1,2]])/4
    p=S.Rational(9,16)
    C=S.Rational(3,4)*(S.eye(3)-eps*M)
    A=C.T*C
    alpha=p*(1-eps)**2
    delta=1-(1-eps)**2
    count=0
    require(positive_semidefinite(A-alpha*S.eye(3)), "positive Gram lower gap");count+=1
    require(positive_semidefinite(p*S.eye(3)-A), "positive Gram upper gap");count+=1
    tests=[]
    for j in (1,2):
        V=C[:,:j]
        cj=C[:,j]
        G=V.T*V
        D=S.eye(j)-G/p
        P=V*G.inv()*V.T
        require(positive_semidefinite(D), "Neumann matrix positivity");count+=1
        for m in (0,1,2):
            B=sum((D**k for k in range(m+1)),S.zeros(j))/p
            Pm=V*B*V.T
            difference=P-Pm
            Qbound=delta**(m+1)*S.eye(3)-difference
            same(difference,V*G.inv()*D**(m+1)*V.T,"exact projector remainder");count+=1
            require(positive_semidefinite(Pm) and positive_semidefinite(difference),
                    "Neumann effect not monotone positive");count+=1
            require(positive_semidefinite(Qbound),
                    "dimension-free positive operator remainder bound");count+=1
            require(positive_semidefinite(S.eye(3)-Pm),
                    "Incomplete success/failure POVM");count+=1
            q=(cj.T*(S.eye(3)-P)*cj)[0]
            qm=(cj.T*(S.eye(3)-Pm)*cj)[0]
            require(q>=alpha and qm>=q and qm<=p,
                    "Golden conditional probability band");count+=1
            require(0<=qm-q<=p*delta**(m+1),
                    "Conditional probability error bound");count+=1
            tests.append([j,m,str(S.factor(qm-q))])
    H=S.Matrix([[0,1,0],[1,0,1],[0,1,0]])/100
    t=S.symbols("t")
    Vt=(C+t*H)[:,:2]
    Gt=Vt.T*Vt
    Dt=S.eye(2)-Gt/p
    require(Dt.subs(t,0)*S.diff(Dt,t).subs(t,0) !=
            S.diff(Dt,t).subs(t,0)*Dt.subs(t,0),
            "moving Gram jet unexpectedly commuting");count+=1
    for m in (0,1,2):
        Pt=Vt*Gt.inv()*Vt.T
        Pmt=Vt*(sum((Dt**k for k in range(m+1)),S.zeros(2))/p)*Vt.T
        full=Pt-Pmt
        compact=Vt*Gt.inv()*Dt**(m+1)*Vt.T
        same(full.subs(t,0),compact.subs(t,0),"value formula");count+=1
        same(S.diff(full,t).subs(t,0),S.diff(compact,t).subs(t,0),
             "full moving noncommuting source formula");count+=1
    return {"status":"PASS","exact_controls":count,
            "rational_reference_p":str(p),
            "controlled_gap_delta":str(delta),
            "tested_mode_orderings":2,
            "tested_polynomial_degrees":[0,1,2],
            "positive_effect":True,
            "moving_first_source":True,
            "native_polynomial_actuation_selected":False,
            "original_raw_terminal_closed":False}

if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True))
