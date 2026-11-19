"""Exact identities and bounded stopped-sum controls; all-k results use the proof."""
import json
from decimal import Decimal as D, localcontext
import sympy as s

def require(value, label):
    if not bool(value):
        raise RuntimeError(label)

p=(s.sqrt(5)-1)/2
phi=1/p
q2=4*p**3
require(s.simplify(1-q2-p**6)==0,'q2 complementary weight')
require(q2>s.Rational(12,13),'q2>12/13')
require(p**2>s.Rational(1,3),'log lower bound endpoint')
require(phi<2,'Hgeo(q1)<4')
require(s.simplify(1+1/p**2-(phi+2))==0,'Hgeo(q1) exact value')
require(9*(1-q2)/q2<s.Rational(3,4),'Hgeo(q2) upper bound certificate')
require(phi+2-s.Rational(3,4)>2,'unit-cost winner strict gap')
q=s.symbols('q',positive=True)
L=s.symbols('L',positive=True)
h=(-q*s.log(q)-(1-q)*s.log(1-q))/L
require(s.simplify(s.diff(h/q,q)-s.log(1-q)/(L*q**2))==0,'geometric entropy derivative')
a=s.symbols('a',positive=True)
x=s.symbols('x',positive=True)
# x=p^(A+1), dx/dA=-log(phi)x: b(A)=A+2+log(1-x)/log(phi).
require(s.simplify(1+s.diff(s.log(1-x)/L,x)*(-L*x)-1/(1-x))==0,'b monotonic gap')
require(s.simplify((-6)*(8*p**s.Rational(9,2))/q2**2+3/p**s.Rational(3,2))==0,'k2 source')
require(s.simplify((-1)*(4*p**s.Rational(3,2))/(p**2)**2+4/p**s.Rational(5,2))==0,'k1 source')

with localcontext() as ctx:
    ctx.prec=75
    pp=(D(5).sqrt()-1)/2; lnphi=(1/pp).ln(); c=D(1); ss=D(0)
    probs={}
    for k in range(1,9):
        c,ss=pp.sqrt()*c-pp*ss,pp*c+pp.sqrt()*ss
        probs[k]=ss*ss
    def H(qv):
        return -(qv*qv.ln()+(1-qv)*(1-qv).ln())/lnphi/qv
    def zval(B,T,ell,k):
        A=T+D(k)*ell
        return (pp**(B+A+2))/(1-pp**(A+1))
    rows=[]
    for k in (1,2,3,7):
        B,T,ell=D(3),D(7),D(1)
        qv=probs[k];r=1-qv;A=T+D(k)*ell;N=512
        Z=zval(B,T,ell,k)
        mass=ecost=rawinfo=norminfo=entropy=D(0)
        for n in range(1,N+1):
            prob=qv*r**(n-1);cost=B+D(n)*(A+1)+1
            logmu=cost*pp.ln();logprob=prob.ln()
            mass+=prob;ecost+=prob*cost
            rawinfo+=prob*(logprob-logmu)/lnphi
            norminfo+=prob*(logprob-logmu+Z.ln())/lnphi
            entropy-=prob*logprob/lnphi
        tail=r**N
        # Complete capped experiment retains the all-dark unresolved record.
        tailcost=B+D(N)*(A+1)
        cap_entropy=entropy-tail*tail.ln()/lnphi
        cap_cost=ecost+tail*tailcost
        E=(1-r**N)/qv
        require(abs(mass+tail-1)<D('1e-68'),'complete stopped mass')
        require(abs(cap_entropy-E*qv*H(qv))<D('1e-65'),'capped entropy with unresolved leaf')
        require(abs(cap_cost-(B+(A+1)*E+(1-tail)))<D('1e-64'),'capped cost with unresolved leaf')
        require(abs(ecost-rawinfo-H(qv))<D('1e-60'),'raw binding complete sum')
        require(abs(ecost-norminfo-(H(qv)-Z.ln()/lnphi))<D('1e-60'),'normalized reference complete sum')
        Zcap=pp**(B+A+2)*(1-(pp**(A+1))**N)/(1-pp**(A+1))+pp**(B+D(N)*(A+1))
        require(abs(Zcap-Z)<D('1e-60'),'cap partition convergence')
        rows.append({'k':k,'q':str(qv),'raw':str(H(qv)),'normalized':str(H(qv)-Z.ln()/lnphi),'mean_cost':str(B+(A+1)/qv+1)})
    winners={}
    for ell in (D(1),D(4)):
        T=D(5)
        vals={k:H(v)-zval(D(0),T,ell,k).ln()/lnphi for k,v in probs.items()}
        winner=min(vals,key=vals.get)
        require(winner==(2 if ell==1 else 1),'declared normalization winner diagnostic')
        winners[str(ell)]=winner
print(json.dumps({'passed':True,'complete_sum_controls':rows,'finite_diagnostic_winners':winners,'scope':'Exact algebra and complete sums; infinite-family existence/nonattainment and all-k winner exclusions are analytical, not numerical scans.'},indent=2))
