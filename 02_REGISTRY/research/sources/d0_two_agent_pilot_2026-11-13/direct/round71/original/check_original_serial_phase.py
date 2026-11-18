"""Original rank-four SER writer: two native central words, same branch maps, different full clock price."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from hashlib import sha256
import sys
import sympy as s
import mpmath as mp


def need(flag, why):
    if not flag:
        raise ArithmeticError(why)


def main():
    root=Path(__file__).resolve().parents[7]
    gatefile=root/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
    need(sha256(gatefile.read_bytes()).hexdigest()=='222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c','native alphabet')
    sys.path.insert(0,str(gatefile.parent))
    import native_execution as n

    src=n.Gate('SourceI',(0,2,3))
    cx=n.Gate('CX',(0,1))
    def literal(gates):
        e=n.Execution(4,(),(),gates,n.G_CX_SOURCE_I,0,(2,3))
        return n.word_matrix(e,max_qubits=4,max_expanded_stages=2)
    signed,plain=literal((src,src)),literal((cx,cx))
    z=s.diag(1,-1)
    need(signed==s.kronecker_product(z,s.eye(8)) and plain==s.eye(16),'two equal-stage literal alternatives')
    for i in (0,1):
        pi=s.zeros(2)
        pi[i,i]=1
        Pi=s.kronecker_product(pi,s.eye(8))
        need(signed*Pi==(-1)**i*plain*Pi,'all live old columns have equal conditioned maps up to scalar phase')
    q,a,p=s.symbols('q a p', positive=True)
    c_signed=p*(a*(1-q)-p*q)
    c_plain=p*(a*(1-q)+p*q)
    gap=4*p**3*a*q*(1-q)
    need(s.expand(c_plain**2-c_signed**2-gap)==0,'cold squared gap')
    need(s.expand(1-(1-2*q)**2-4*q*(1-q))==0,'coherent old comparison gap')
    cos_delta=s.symbols('cos_delta',real=True)
    fidelity=1-2*q*(1-q)*(1-cos_delta)
    w=p**2*(a**2*(1-q)**2+p**2*q**2-2*a*p*q*(1-q)*cos_delta)
    need(s.expand(w-c_signed**2-a*p**3*(1-fidelity))==0,'one observable measures the entire hidden phase contribution')
    l0,l1=s.symbols('l0 l1',positive=True)
    N=(1-q)*l0**2+q*l1**2
    qq=q*l1**2/N
    squared=((1-q)*l0)**2+(q*l1)**2+2*(1-q)*q*l0*l1*cos_delta
    need(s.expand(N-squared-q*(1-q)*(l0**2+l1**2-2*l0*l1*cos_delta))==0,'one physical absolute weight and coherent defect')
    need(s.cancel(N*(1-qq)/(1-q)-l0**2)==0 and s.cancel(N*qq/q-l1**2)==0,'recover both absolute outcome weights')
    vx=s.Matrix([n.A,n.P]); pick=s.Matrix([[1,0]])
    for i,wanted in ((0,n.A),(1,n.P)):
        old=s.eye(2)[:,i]
        selected=s.kronecker_product(old.T,pick,s.eye(4))*literal((cx,))*s.kronecker_product(old,vx,s.eye(4))
        need(selected==wanted*s.eye(4),'charged Golden length from one native CX on the old record')
    alpha=p*(a-p)/2
    brec=p*(a+p)/2
    need(s.expand(alpha+brec*(1-2*q)-c_signed)==0,'actual SER10 in both original sectors')
    s_free=p*p*q/(a*a*(1-q)+p*p*q)
    need(s.simplify((q-s_free)*(a*a*(1-q)+p*p*q)-(a*a-p*p)*q*(1-q))==0,'free optimum changes the reverse mark')

    iv=mp.iv
    iv.dps=65
    truep=(iv.sqrt(5)-1)/2
    ac=iv.sqrt(truep)
    # Repeated squaring with outward rounding for kappa9 from original SC6.
    cc,ss=ac,truep
    for _ in range(9):
        cc,ss=cc*cc-ss*ss,2*cc*ss
    qref=4*ss**2*truep**7
    need(iv.mpf('0.12')<qref and qref<iv.mpf('.14'),'actual original H.1 anchor in the declared collar')
    # Applies to each actual source 1/10<=q<=1/5 and R_< = I; no r-fold bonus needed.
    # beta in (3/4,4/5), p>3/5, a>3/4, q(1-q)>=9/100.
    zeta=F(1,2**20)
    feedback_lower=zeta*4*F(3,5)**3*F(3,4)*F(9,100)
    heat_upper=F(132,359)/F(3,4)*F(4,5)**11/factorial(11)
    need(heat_upper<F(11,10**10) and feedback_lower-heat_upper>F(5,10**8),'growing H+J strict ranking, ten real CX slots')
    need(s.simplify((c_plain**2-c_signed**2).diff(q,2)+8*a*p**3)==0,'feedback curvature numerator')
    need(2*F(5,8)**2*(F(4,5)+F(5,8))*F(4,5)<1,'literal cold probability derivative bound')
    need(8*F(3,4)*F(3,5)**3-zeta/(1-zeta)**2>1,'curvature remains strictly below minus zeta')
    need(F(64,100)**11<F(1,100)<=F(64,100)**10,'actual one-sided test in eleven independent preparations')
    print('PASS: native signed/identity interiors, every branch operator, true SER10, SC6 anchor, coherent verification and strict growing H+J gap exceeding 5e-8.')


if __name__=='__main__':
    main()
