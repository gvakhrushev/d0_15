"""Exact moving-projector/orthogonal-innovation source checks, independent
of the earlier Gram-determinant tests. No native operation admission claimed.
"""
import json
import sympy as S

def require(c, name):
    if not bool(c):
        raise RuntimeError(name)

def same(a,b,name):
    require(S.simplify(a-b)==0,name)

def run():
    C=S.Matrix([[S.Rational(1,2),S.Rational(1,6),0],
                [0,S.Rational(1,3),S.Rational(1,7)],
                [S.Rational(1,8),0,S.Rational(1,4)]])
    M=S.Matrix([[0,1,0],[1,0,1],[0,1,0]])/10
    t=S.symbols("t")
    Ct=C+t*M
    A=C.T*C
    A_t=Ct.T*Ct
    I=S.eye(3)
    n=0
    q_values=[]
    true_scores=[]
    frozen_scores=[]
    innovations=[]
    for j in range(3):
        V=Ct[:,:j]
        c=Ct[:,j]
        if j:
            G=V.T*V
            P=V*G.inv()*V.T
            G0=G.subs(t,0)
        else:
            P=S.zeros(3)
            G0=None
        P0=P.subs(t,0)
        dP=S.diff(P,t).subs(t,0)
        require(P0.T==P0 and P0*P0==P0, "orthogonal projector");n+=1
        require((I-P0).T==(I-P0) and (I-P0)*(I-P0)==I-P0,
                "complete two-outcome projector");n+=1
        cj=c.subs(t,0)
        dc=S.diff(c,t).subs(t,0)
        q_t=(c.T*(I-P)*c)[0]
        q0=S.factor(q_t.subs(t,0))
        q_values.append(q0)
        Aprev=A[:j,:j].det() if j else S.Integer(1)
        same(q0,A[:j+1,:j+1].det()/Aprev,"Gram Schur innovation");n+=1
        require(0<q0<1,"Born probability range");n+=1
        if j:
            dV=S.diff(V,t).subs(t,0)
            V0=V.subs(t,0)
            dP_formula=(I-P0)*dV*G0.inv()*V0.T+V0*G0.inv()*dV.T*(I-P0)
            require(dP==dP_formula,"moving projector derivative");n+=1
        actual=S.diff(q_t,t).subs(t,0)
        frozen=2*(dc.T*(I-P0)*cj)[0]
        projector=-(cj.T*dP*cj)[0]
        same(actual,frozen+projector,"moving innovation chain rule");n+=1
        true_scores.append(S.factor(actual/q0))
        frozen_scores.append(S.factor(frozen/q0))
        innovations.append([str(actual),str(frozen),str(projector)])
    require(S.prod(q_values)==A.det(),"all success Gram determinant");n+=1
    actual_total=S.factor(sum(true_scores))
    frozen_total=S.factor(sum(frozen_scores))
    same(actual_total,S.diff(S.log(A_t.det()),t).subs(t,0),
         "determinant and whole-record first source");n+=1
    same(actual_total,S.Rational(-1,3),"exact all-success source");n+=1
    same(frozen_total,S.Rational(71,1725),"frozen score hostile control");n+=1
    require(actual_total!=frozen_total and actual_total*frozen_total<0,
            "source sign defect invisible");n+=1
    require(all((I-C*C.T)[:i,:i].det()>0 for i in (1,2,3)),
            "full Julia lower completion unavailable");n+=1
    require(all((I-C.T*C)[:i,:i].det()>0 for i in (1,2,3)),
            "full Julia upper completion unavailable");n+=1
    return {"status":"PASS","exact_controls":n,
            "q":[str(v) for v in q_values],
            "innovations_actual_frozen_projector":innovations,
            "true_log_score":str(actual_total),
            "frozen_log_score":str(frozen_total),
            "native_projector_admitted":False,
            "original_GR_closed":False}

if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True))
