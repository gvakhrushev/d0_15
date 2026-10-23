#!/usr/bin/env python3
"""Complete ordinary/rare second jets, pinned full16 definitions only."""
from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[4]
CREATORS='02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS={CREATORS:'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
 '02_REGISTRY/research/sources/d0_retained_history_causal_source_2026-10-16/check_retained_history.py':'6be5d31fc2b5a2d2f75b54071720b03c6bbebc30356260b5c823c3ef8ef88d92',
 '02_REGISTRY/research/sources/d0_full_contrast_gauge_span_2026-10-17/check_gauge_span.py':'6ce1983a9b437dba3d49c30f290d934f9b0caa3a6cac54f758fb11fd33cfd8c5'}

def run(repo=None):
    repo=ROOT if repo is None else Path(repo).resolve()
    checks=[]
    def require(condition,name):
        if not bool(condition): raise ArithmeticError('complete_exit:'+name)
        checks.append(name)
    def eq(actual,expected,name,reduce=s.expand):
        entries=list(actual-expected) if isinstance(actual,s.MatrixBase) else [actual-expected]
        require(all(reduce(x)==0 for x in entries),name)
    for path,digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'source_pin_'+Path(path).name)
    tree=ast.parse((repo/CREATORS).read_text())
    nodes=[n for n in tree.body if (isinstance(n,ast.FunctionDef) and n.name=='creator') or
      (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXTERIOR_ORDER' for t in n.targets))]
    require(len(nodes)==2,'creator_definition_nodes_only')
    scope={'s':s,'lru_cache':lru_cache}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),CREATORS,'exec'),scope)
    C=[scope['creator'](r) for r in range(4)]
    I,O=s.eye(16),s.zeros(16)
    nu,defect=s.Rational(3,5),s.Rational(4,5)
    # Jets mean value, first derivative, second derivative, not coefficients.
    def mul(X,Y):
        return [X[0]*Y[0],X[1]*Y[0]+X[0]*Y[1],X[2]*Y[0]+2*X[1]*Y[1]+X[0]*Y[2]]
    def adj(X): return [x.T for x in X]
    def add(X,Y): return [x+y for x,y in zip(X,Y)]
    def scale(k,X): return [k*x for x in X]
    def const(x): return [x,s.zeros(x.rows,x.cols),s.zeros(x.rows,x.cols)]
    def jeq(X,Y,name):
        for j in range(3): eq(X[j],Y[j],name+'_jet'+str(j))
    def lift(M):
        return sum((M[i,j]*C[i]*C[j].T for i in range(4) for j in range(4)),O.copy())
    def generator(i,j):
        M=s.zeros(4); M[i,j],M[j,i]=1,-1
        return lift(M)
    def rotation(K): return I+s.Rational(4,5)*K+s.Rational(2,5)*K*K
    k12,k23,k13=generator(1,2),generator(2,3),generator(1,3)
    bases=[rotation(k12)*rotation(k23),rotation(k23),rotation(k13),I]
    tangents=[k23,k13,k12,k12+k23]
    P,L,R,Lbare,Rbare=[],[],[],[],[]
    for r in range(4):
        ret=[bases[r],bases[r]*tangents[r],bases[r]*tangents[r]*tangents[r]]
        jeq(mul(adj(ret),ret),const(I),'proper_SO3_return_'+str(r))
        nr=C[r]*C[r].T
        l0,r0=I+(defect-1)*nr,I+(defect-1)*(I-nr)
        pr=[nu*C[r]*x for x in ret]; lr=const(l0); rr=mul(mul(adj(ret),const(r0)),ret)
        P.append(pr); L.append(lr); R.append(rr); Lbare.append(l0); Rbare.append(r0)
        jeq(add(mul(pr,adj(pr)),mul(lr,lr)),const(I),'full16_Julia_top_'+str(r))
        jeq(add(mul(rr,rr),mul(adj(pr),pr)),const(I),'full16_Julia_bottom_'+str(r))
        jeq(mul(pr,rr),mul(lr,pr),'full16_Julia_cross_'+str(r))
    # The literal32 word order, each word duplicated; retain both coefficients.
    words=[]
    for r in range(4):
        pc,lc,rc=const(nu*C[r]),const(Lbare[r]),const(Rbare[r])
        for top,upper in ((P[r],L[r]),(adj(P[r]),R[r]),(scale(-1,pc),scale(-1,lc)),
                          (scale(-1,adj(pc)),scale(-1,rc))):
            words.extend([(top,upper),(top,upper)])
    require(len(words)==32,'actual32_signed_Julia_words')
    rows={}
    for label in range(32):
        for coefficient in range(2):
            jet=[O.copy() for _ in range(3)]
            for j,word in enumerate(words):
                jet=add(jet,scale(s.Rational((-1)**bin(label&j).count('1'),32),word[coefficient]))
            rows[(label,coefficient)]=jet
    require(all(x==O for key,jet in rows.items() if key[0]%2 for x in jet),'odd_duplicate_rows_zero')
    total=[O.copy() for _ in range(3)]
    for jet in rows.values(): total=add(total,mul(jet,adj(jet)))
    jeq(total,const(I),'full64_row_completeness')
    A=rows[(0,0)]
    jeq(A,adj(A),'actual_blank_D_selfadjoint')
    ordinary,rare=[],[]
    for chi,role in enumerate((0,16,8,24)):
        for u in range(2):
            for v in range(2):
                for coefficient in range(2):
                    key=(role+2*u+4*v,coefficient)
                    zero=v==0 or (u==0 and coefficient==1 and chi!=0)
                    if key!=(0,0): (rare if zero else ordinary).append(key)
    require(len(ordinary)==13 and len(rare)==18,'all13_ordinary18_rare_rows_retained')
    def row_effect(keys):
        result=[O.copy() for _ in range(3)]
        for key in keys: result=add(result,mul(rows[key],adj(rows[key])))
        return result
    Ro,Rr=row_effect(ordinary),row_effect(rare)
    jeq(add(add(Ro,Rr),mul(A,A)),const(I),'ordinary_rare_and_blank_row_jet_balance')

    # Matrix pairs X0+pX1 keep Q(p) exact without expression swell.
    def f(x): return (x,s.zeros(x.rows,x.cols))
    def fa(X,Y): return (X[0]+Y[0],X[1]+Y[1])
    def fn(X): return (-X[0],-X[1])
    def fm(X,Y):
        bd=X[1]*Y[1]
        return (X[0]*Y[0]+bd,X[0]*Y[1]+X[1]*Y[0]-bd)
    def fs(k,X):
        a,b=k
        return (a*X[0]+b*X[1],a*X[1]+b*X[0]-b*X[1])
    def fj(X): return [f(x) for x in X]
    def ja(X,Y): return [fa(x,y) for x,y in zip(X,Y)]
    def jn(X): return [fn(x) for x in X]
    def js(k,X): return [fs(k,x) for x in X]
    def jm(X,Y):
        return [fm(X[0],Y[0]),fa(fm(X[1],Y[0]),fm(X[0],Y[1])),
          fa(fa(fm(X[2],Y[0]),fs((2,0),fm(X[1],Y[1]))),fm(X[0],Y[2]))]
    def feq(X,Y,name):
        for j in range(3):
            for k in range(2): eq(X[j][k],Y[j][k],name+'_jet'+str(j)+'_p'+str(k))
    ident,Af=fj(const(I)),fj(A)
    A2=jm(Af,Af)
    B=ja(ident,js((-2,2),A2))
    Eo=js((4,-4),jm(jm(Af,fj(Ro)),Af))
    Er=ja(js((4,-4),jm(jm(Af,fj(Rr)),Af)),js((-4,8),jm(A2,A2)))
    # The last summand is blank/port1=4p^3 A^4; blank/port0 is survival.
    feq(ja(Eo,Er),ja(ident,jn(jm(B,B))),'all128_outcome_exit_balance')
    commutator=fa(fm(B[0],Er[0]),fn(fm(Er[0],B[0])))
    require(any(x!=O for x in commutator),'full16_B_rare_effect_noncommuting')
    Fo,Fr=ja(Eo,jm(jm(B,Eo),B)),ja(Er,jm(jm(B,Er),B))
    survival=jm(jm(jm(B,B),B),B)
    feq(ja(Fo,Fr),ja(ident,jn(survival)),'n2_ordered_first_exit_balance')
    wrong=ja(Er,jm(Er,jm(B,B)))
    require(any(x!=y for x,y in zip(Fr[0],wrong[0])),'hostile_commuted_first_exit_rejected')
    require(any(x!=y for x,y in zip(Fr[0],js((2,0),Er)[0])),'hostile_reset_rejected')

    rho0=I+(C[0]+C[0].T)/5
    H=I/10+(C[3]+C[3].T)/9+(C[0]*C[0].T)/7
    G=I/11+(C[1]+C[1].T)/13
    rho=[rho0,H*rho0+rho0*H,G*rho0+rho0*G+2*H*rho0*H]
    normalizer=[s.trace(x) for x in rho]
    require(normalizer[1]!=0 and normalizer[2]!=0,'first_and_second_preparation_normalizer_move')
    p=s.Symbol('p',real=True)
    def normalized(F):
        numerator=[s.trace(x[0])+p*s.trace(x[1]) for x in jm(fj(rho),F)]
        q0=numerator[0]/normalizer[0]
        q1=(numerator[1]-q0*normalizer[1])/normalizer[0]
        q2=(numerator[2]-q0*normalizer[2]-2*q1*normalizer[1])/normalizer[0]
        return [q0,q1,q2],numerator
    qo,numerator=normalized(Fo); qr,_=normalized(Fr); qs,_=normalized(survival)
    for j in range(3):
        eq(qo[j]+qr[j]+qs[j],1 if j==0 else 0,'normalized_source_completeness_jet'+str(j))
    require(s.expand(qo[1]-numerator[1]/normalizer[0])!=0,'hostile_frozen_normalizer_rejected')
    require(s.expand(qo[2]-(numerator[2]-qo[0]*normalizer[2])/normalizer[0])!=0,
            'hostile_omitted_second_normalizer_cross_term_rejected')
    t=s.Symbol('t',real=True)
    direct=(numerator[0]+t*numerator[1]+t*t*numerator[2]/2)/(
             normalizer[0]+t*normalizer[1]+t*t*normalizer[2]/2)
    for j in (1,2):
        eq(s.diff(direct,t,j).subs(t,0),qo[j],'independent_quotient_source_'+str(j),s.cancel)

    # Separate2x2 noncommuting SAME-price/calibration control, not a root.
    I2=s.eye(2)
    Delta=[s.Matrix([[1,s.Rational(1,5)],[s.Rational(1,5),2]]),
      s.Matrix([[s.Rational(1,7),s.Rational(1,9)],[s.Rational(1,9),-s.Rational(1,8)]]),
      s.Matrix([[s.Rational(1,11),-s.Rational(1,13)],[-s.Rational(1,13),s.Rational(1,17)]])]
    beta=[s.Rational(3,2),s.Rational(1,7),-s.Rational(1,11)]
    alpha=[x/4 for x in beta]
    B2=[I2-alpha[0]*Delta[0],-alpha[1]*Delta[0]-alpha[0]*Delta[1],
        -alpha[2]*Delta[0]-2*alpha[1]*Delta[1]-alpha[0]*Delta[2]]
    S=mul(mul(B2,B2),mul(B2,B2))
    require(Delta[0]*Delta[1]!=Delta[1]*Delta[0] and S[0]*S[1]!=S[1]*S[0],
            'actual_price_operator_jets_noncommuting')
    require(B2[0][0,0]>0 and s.det(B2[0])>0,'small_price_B_positive')
    z=[s.Rational(1,8),s.Rational(1,29),s.Rational(1,31)]
    M=[s.Integer(2),s.Rational(1,19),-s.Rational(1,23)]
    logC=[s.log(7),s.Rational(1,13),-s.Rational(1,17)]
    Z=[s.trace(x) for x in S]
    U=[logC[0]+s.log(Z[0]),logC[1]+Z[1]/Z[0],
       logC[2]+Z[2]/Z[0]-Z[1]**2/Z[0]**2]
    Hj=[U[0]/beta[0],U[1]/beta[0]-U[0]*beta[1]/beta[0]**2,
        U[2]/beta[0]-(2*U[1]*beta[1]+U[0]*beta[2])/beta[0]**2
        +2*U[0]*beta[1]**2/beta[0]**3]
    F=[(1-z[0])*I2+z[0]*S[0],z[0]*S[1]+z[1]*(S[0]-I2),
       z[0]*S[2]+2*z[1]*S[1]+z[2]*(S[0]-I2)]
    inv=F[0].inv()
    V=[s.log(s.det(F[0])),s.trace(inv*F[1]),
       s.trace(inv*F[2])-s.trace(inv*F[1]*inv*F[1])]
    Jj=[-M[0]*V[0],-M[1]*V[0]-M[0]*V[1],-M[2]*V[0]-2*M[1]*V[1]-M[0]*V[2]]
    poly=lambda x:x[0]+t*x[1]+t*t*x[2]/2
    Hd=(poly(logC)+s.log(poly(Z)))/poly(beta)
    Fpoly=F[0]+t*F[1]+t*t*F[2]/2
    Jd=-poly(M)*s.log(s.det(Fpoly))
    for j in (1,2):
        eq(s.diff(Hd,t,j).subs(t,0),Hj[j],'fullZ_clock_calibration_heat_source_'+str(j),s.simplify)
        eq(s.diff(Jd,t,j).subs(t,0),Jj[j],'feedback_noncommuting_calibration_source_'+str(j),s.simplify)
    rho2=[s.Matrix([[2,1],[1,3]]),s.Matrix([[1,2],[2,0]]),s.Matrix([[0,1],[1,2]])]
    N2=[s.trace(x) for x in rho2]
    rnum=[s.trace(x) for x in mul(rho2,Delta)]
    Rj=[rnum[0]/N2[0]]
    Rj.append((rnum[1]-Rj[0]*N2[1])/N2[0])
    Rj.append((rnum[2]-2*Rj[1]*N2[1]-Rj[0]*N2[2])/N2[0])
    Rd=poly(rnum)/poly(N2)
    for j in (1,2):
        eq(s.diff(Hd+Jd+Rd,t,j).subs(t,0),Hj[j]+Jj[j]+Rj[j],
           'same_total_HJR_second_source_'+str(j),s.simplify)
    require(s.trace(rho2[0]*S[0])/N2[0]!=Z[0],'hostile_prepared_probability_not_thermal_Z')
    without_C=Hj[1]+Jj[1]-logC[1]/beta[0]
    eq(s.expand(Hj[1]+Jj[1]-without_C),s.Rational(2,39),
       'hostile_omitted_logC_source_has_exact_nonzero_residual')
    # Positivity certifies the omitted beta term is nonzero, avoiding a
    # log-combination simplifier that would form gigantic integer powers.
    require(7*Z[0]>1 and beta[1]>0,'hostile_omitted_beta_prefactor_source_is_strictly_nonzero')

    # Finite blank logarithm throughh^2, without a continuum error claim.
    h,d,a1,a2,clock,c0=s.symbols('h d a1 a2 beta c0',positive=True)
    log_survival=clock/(c0*h*h)*s.log(1-c0*h*h*(d+h*a1+h*h*a2))
    eq(s.series(log_survival,h,0,3).removeO(),
       -clock*d-clock*h*a1-h*h*(clock*a2+clock*c0*d*d/2),
       'finite_blank_clock_second_term_retained')
    return {'status':'PASS','exact_checks':len(checks),'checks':checks,'source_pins':PINS,
      'carrier':{'Fock':16,'Julia_words':32,'data_outputs':64,'golden_outcomes':128,
                 'reference_kept_in_parent':128},
      'fixture':'nu3/5,defect4/5; literal SO3 exterior R0 exp(tK), exact0/1/2jets',
      'ordinary_nonzero_flat_N0_rows':13,'rare_zero_flat_N0_nonblank_rows':18,
      'rare_port_outcomes_including_distinct_blank_port1':37,
      'chronology':'n=2,m=4; Fo+Fr=I-B^4; [B,Er]nonzero; allsecondjetsordered',
      'normalizer_jets':[str(x) for x in normalizer],
      'price_control':'separate2x2 S=(I-alpha Delta)^4,beta4alpha,fulltraceZ,formalactualcalibrationjets',
      'scope':{'old_run_roots_or_spectra_executed':False,'physical_root_or_native_clock_law_proved':False,
       'full16_truncated':False,'ordinary_secondsource_inferred_from_positiveGram':False,
       'continuum_or_UV_error_estimate_tested':False,'new_eventprice_or_preparation_selected':False}}

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
