"""Exact controls for the marked-range source; no physical price inferred."""
from pathlib import Path
import hashlib
import json
import sympy as S


def run():
    checks = []

    def need(condition, label):
        if not bool(condition):
            raise AssertionError(label)
        checks.append(label)

    def eq(a,b,label):
        d=a-b
        good=all(S.simplify(v)==0 for v in d) if isinstance(d,S.MatrixBase) else S.simplify(d)==0
        need(good,label)

    p=(S.sqrt(5)-1)/2
    q,z,t,e,u=S.symbols('q z t e u',positive=True)
    a=S.sqrt(p)
    eq(p+p**2,1,'Golden normalization')
    eq(p+p**3+p**4,1,'original noisy cold legal and invalid masses')
    f=a*S.sqrt(1-q)+a*p*S.sqrt(q)
    qstar=S.simplify(p**2/(1+p**2))
    eq(S.diff(f,q).subs(q,qstar),0,'original cold stationary probability')
    need(S.simplify(p**2-qstar)>0,'original informative collar lies above cold stationary point')
    # Finite strict sign controls are additional checks; the general proof is the displayed inequality.
    for x in (p**2,S.Rational(2,5),S.Rational(1,2)):
        need(S.N(S.diff(f,q).subs(q,x),40)<0,'negative coherent cold slope at '+str(x))

    P0=S.diag(1,0,0)
    P1=S.diag(0,1,0)
    B=S.Matrix([a,a*p,p**2])
    eq((B.T*B)[0],1,'reference retains invalid born complement')
    K0=S.sqrt(1-q)*S.Matrix([1,0,0])
    K1=S.sqrt(q)*S.Matrix([0,1,0])
    eq(K0*K0.T/(1-q),P0,'first normalized range independent of probability')
    eq(K1*K1.T/q,P1,'second normalized range independent of probability')
    h=(B.T*(P0+P1)*B)[0]
    eq(h,p+p**3,'marked root compression uses sum of legal masses')
    eq(S.diff(h,q),0,'marked root q source vanishes')
    coherent=(B.T*(K0+K1))[0]
    eq(coherent,f,'coherent root adds amplitude overlaps')
    Jmarked=-S.log(1-z)-S.log(1-z+z*h)
    eq(S.diff(Jmarked,q),0,'entire marked determinant includes rank term and has zero q source')
    Jcoherent=-S.log(1-z+z*coherent**2)
    eq(S.diff(Jcoherent,q),-2*z*f*S.diff(f,q)/(1-z+z*f**2),'coherent source formula')

    # General exact-effect rotated isometry, including the changing branch weight.
    theta=S.Function('theta')(t)
    prob=S.Function('prob')(t)
    V=S.Matrix([S.cos(theta),S.sin(theta)])
    K=S.sqrt(prob)*V
    eq((K.T*K)[0],prob,'rotated native-error model retains exact scalar effect')
    P=K*K.T/prob
    eq(P,V*V.T,'normalized range cancels actual scalar weight')
    eq(S.diff(P,t),S.diff(V,t)*V.T+V*S.diff(V.T,t),'projector first derivative keeps orientation source')
    Vbase=S.Matrix([1,0])
    E=K-S.sqrt(prob)*Vbase
    R=E/S.sqrt(prob)
    eq(S.diff(P,t),S.diff(R,t)*V.T+V*S.diff(R.T,t),'exact compiler-error range derivative')
    eq(S.diff(R,t),S.diff(E,t)/S.sqrt(prob)-E*S.diff(prob,t)/(2*prob**S.Rational(3,2)),
       'small-probability normalization derivative retained')

    spike=e*S.sin(t/e)
    Vs=V.subs(theta,spike)
    Bs=S.Matrix([1,1])/S.sqrt(2)
    hs=(Bs.T*Vs*Vs.T*Bs)[0]
    eq(hs.subs(t,0),S.Rational(1,2),'small endpoint error control has fixed root value')
    eq(S.diff(hs,t).subs(t,0),1,'small endpoint error hides unit root first jet')
    Js=-S.log(1-z+z*hs)
    eq(S.diff(Js,t).subs(t,0),-z/(1-z/2),'small endpoint error does not suppress source')

    # Rank jump keeps the rank contribution: take a fixed rational valid (u,z).
    birth=S.Matrix([S.sqrt(u),S.sqrt(1-u)])
    eq((birth.T*birth)[0],1,'rank-jump reference is an isometry')
    eq((birth.T*S.eye(2)*birth)[0],1,'two occupied leaves have h equal one')
    eq((birth.T*S.diag(1,0)*birth)[0],u,'zero branch removes its range')
    jump=-S.log(1-z)+S.log(1-z+z*u)
    need(jump.subs({z:S.Rational(1,4),u:S.Rational(1,3)})>0,'rank jump changes full determinant despite continuous Kraus map')

    # Check M4 on explicit moving range fixtures, with the exact reference and source.
    for zz in (S.Rational(1,4),S.Rational(1,10)):
        source=abs((-z/(1-z/2)).subs(z,zz))
        nu=1
        need(source<=2*zz/(1-zz)*nu,'M4 bounds complete root source at z='+str(zz))

    # Exact finite projector contrast identity, needed for discrete native words.
    w=S.Matrix([S.Rational(3,5),S.Rational(4,5)])
    v=S.Matrix([1,0])
    eq(w.T*w,S.ones(1,1),'finite comparator preserves exact scalar effect after normalization')
    eq(w*w.T-v*v.T,(w-v)*w.T+v*(w-v).T,'finite projector error decomposition')
    eq(((w*w.T-v*v.T)**2),S.Rational(16,25)*S.eye(2),'exact comparator projector norm squared')
    need(S.Rational(4,5)<=2*S.sqrt(((w-v).T*(w-v))[0]),'finite comparator obeys twice-isometry-error bound')

    here=Path(__file__).resolve().parent
    owner=here.parents[3]/'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
    return {'status':'PASS','checks':len(checks),'numeric_sign_diagnostics':3,'check_names':checks,
            'baseline':'dc411daf01f697ec85dd22f28bfe124171796645',
            'owner_sha256':hashlib.sha256(owner.read_bytes()).hexdigest(),
            'proof_sha256':hashlib.sha256((here/'MARKED_SOURCE_RU.md').read_bytes()).hexdigest(),
            'scope':{'RC3_assumed_from_owner':True,'full_H1_executed':False,
                     'native_compiler_C1_bound_proved':False,'physical_C_closed':False,'GR_closed':False}}


if __name__=='__main__':
    result=run()
    out=Path(__file__).with_name('CHECK_RESULT.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'checks':result['checks'],'output':str(out)},ensure_ascii=False))
