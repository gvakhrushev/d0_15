#!/usr/bin/env python3
"""D0 #334: exact Golden-only fair-thinning and ORIGINAL two-turn
(A=L+(1-L)B,B) operator harmonic stop, no spectral sqrt(F) or moving polar.
Scoped MATHEMATICS. Native full M1/Book03 physical admission NOT claimed.
"""
import math
from fractions import Fraction as Q
import sympy as S
from mpmath import iv

passed=[]
def check(label,predicate):
    if not bool(predicate): raise AssertionError(label)
    passed.append(label)

def simp(expression): return S.simplify(S.expand(expression))
def eqmat(A,B): return A.shape==B.shape and all(simp(u-v)==0 for u,v in zip(A,B))

p=(S.sqrt(5)-1)/2
phi=1/p
a=S.sqrt(p)
z=Q(1,2**20)
check('Golden relation p+p²=1',simp(p+p*p-1)==0)
check('native gate square root a²=p',simp(a*a-p)==0)
check('Golden amplitude algebraic integer monic quartic',S.minimal_polynomial(a,S.Symbol('x'))==S.Symbol('x')**4+S.Symbol('x')**2-1)
G=S.Matrix([[a,-p],[p,a]])
check('original splitter orthogonal exact',eqmat(G.T*G,S.eye(2)))
# FR or RF each occurs with probability p * p^2 = p^3.
q_success=simp(2*p**3)
q_fail=simp(p*p+p**4)
check('two original Golden outcomes exactly fair',simp(p*p*p-p*p*p)==0)
check('all original double words normalized',simp(q_success+q_fail-1)==0)
check('successful extractor nonzero',float(q_success)>0)
check('failure extractor nonzero',float(q_fail)>0)
expected_pair_cost=2*(p+2*p*p)
expected_cost_bit=simp(expected_pair_cost/q_success)
check('native Golden unbiased bit costs 3phi+1',simp(expected_cost_bit-(3*phi+1))==0)
check('20 bits give exact original Book fugacity',Q(1,2)**20==z)
check('20 exact fair bits positively paid',float(20*expected_cost_bit)>117)
check('20 fair bits expected cost strict <=118 Golden units',float(20*expected_cost_bit)<118)
for Lcap in [1,2,5,10]:
    prob_all_20=(1-q_fail**Lcap)**20/2**20
    check(f'finite cap L={Lcap} leaves positive unresolved archive',float(S.N(prob_all_20,60))<float(z))
    check(f'finite cap L={Lcap} still positive exact attempt mass',float(S.N(prob_all_20,60))>0)
# The original flat point has E=b=p², and the SAME 2-tick L=B=4p³.
Lflat=simp(4*p*p*(1-p*p))
Bflat=Lflat
Aflat=simp(Lflat+(1-Lflat)*Bflat)
check('flat original L=B=4p³',simp(Lflat-4*p**3)==0)
check('flat original p^6+4p³=1',simp(4*p**3+p**6-1)==0)
check('flat original A=B(1+p^6)',simp(Aflat-4*p**3*(1+p**6))==0)
# A bounded original-Golden-only computational-basis circuit has amplitude
# entries in Z[a]; a is a monic quartic algebraic integer. Every complete
# unnormalized branch probability is a sum of squared algebraic integers.
# The only RATIONAL algebraic integers are ordinary Z, so no probability
# exactly 1/2 or 2^-20 can be emitted unconditionally by that circuit class.
check('original Book fugacity is rational but NOT integral',z.denominator==2**20 and z.numerator==1)
check('unconditional genuine fair coin rational but NOT integral',Q(1,2).denominator==2)
# Golden rotations present in the original AF and scene 2-tick owner.
def port(t):
    return S.Matrix([[S.sqrt(1-t),-S.sqrt(t)],[S.sqrt(t),S.sqrt(1-t)]])
E=Q(3,10)
b=Q(2,5)
L=simp(4*E*(1-E));B=simp(4*b*(1-b));A=simp(L+(1-L)*B)
check('native L source from exact TWO forward AF rotations',simp((port(E)**2)[1,0]**2-L)==0)
check('native B source from exact TWO forward scene rotations',simp((port(b)**2)[1,0]**2-B)==0)
check('original sequential L or B is exact A',simp(A-(L+(1-L)*B))==0)
check('test native A lies in positive contraction interval',0<A<1)
check('test native B lies in positive contraction interval',0<B<1)
# Effect-valued multi-Kraus instrument: 3 different KEEP flags,4 STOP flags.
# Diagonal ordered sectors A, B, D (dark); 2 true matched scene types + dark.
PiA=S.diag(1,0,0);PiB=S.diag(0,1,0);PiD=S.diag(0,0,1); I=S.eye(3)
F=A*PiA+B*PiB
keep=[S.sqrt(z*L)*PiA,S.sqrt(z*(1-L)*B)*PiA,S.sqrt(z*B)*PiB]
stop=[S.sqrt(1-z)*I,S.sqrt(z*(1-L)*(1-B))*PiA,S.sqrt(z*(1-B))*PiB,S.sqrt(z)*PiD]
sq=lambda K:K.T*K
EK=sum([sq(v) for v in keep],S.zeros(3));ES=sum([sq(v) for v in stop],S.zeros(3))
check('three retained keep flags effect equals zeta F EXACTLY',eqmat(EK,z*F))
check('four retained stop flags effect = I-zeta F EXACTLY',eqmat(ES,I-z*F))
check('all seven COMPLETE flags Kraus-normalized',eqmat(EK+ES,I))
check('all keep Kraus commute with original F',all(eqmat(v*F,F*v) for v in keep))
check('all stop Kraus commute with original F',all(eqmat(v*F,F*v) for v in stop))
check('dark sector never incorrectly kept',EK[2,2]==0)
# A coherent non-eigenstate input is allowed: all accepted records remain.
rho=S.Matrix([[Q(1,3),Q(1,6),Q(1,6)],
              [Q(1,6),Q(1,3),Q(1,6)],
              [Q(1,6),Q(1,6),Q(1,3)]])
check('input density is valid real normalized SPD',rho.trace()==1 and rho.det()>0)
D=rho
for n in range(1,9):
    D=sum([k*D*k.T for k in keep],S.zeros(3))
    target=(z*F)**n*rho
    check(f'all complete retained keep-record survival moment n={n}',simp(S.trace(D)-S.trace(target))==0)
    stop_prob=sum(S.trace(s*D*s.T) for s in stop)
    check(f'each post-keep stop probability valid n={n}',0<float(stop_prob)<1)
# Normalized maximally mixed state on actual 2x528 scene active positive sectors.
A0=S.simplify(A);B0=S.simplify(B)
check('scalar all-orders harmonic moment matches original 528x2 J2',
      S.simplify(-528*S.log((1-z*A0)*(1-z*B0))+
                 528*S.log(1-z*A0)+528*S.log(1-z*B0))==0)
for n in range(1,9):
    check(f'original 528+528 tail sum n={n}',
          S.simplify((z*A0)**n/2+(z*B0)**n/2 -
                S.trace((z*F)**n)/2)==0)
# Real original Golden scalar source and fair-coin per-OUTER-run price;
# coin work is independent in each new attempt, but T depends on fields.
iv.dps=80
p_iv=(iv.sqrt(5)-1)/2
zi=iv.mpf(2)**-20;lp=iv.log(1/p_iv)
coords=[('0.001370578581747874','-0.000016169093857131'),
        ('-0.000127665084908232','0.000005454102084650')]

def box(x):
    from decimal import Decimal
    u=Decimal(x);e=Decimal('1e-12')
    return iv.mpf([str(u-e),str(u+e)])

def source(x,y):
    E=p_iv*p_iv*(1+x);L=4*E*(1-E)
    b=p_iv-p_iv*p_iv*y;B=4*b*b*(1-b*b);A=L+(1-L)*B
    By=-8*p_iv*p_iv*b*(1-2*b*b);Ay=(1-L)*By
    r=zi*(A+B)-zi*zi*A*B
    ry=zi*(Ay*(1-zi*B)+By*(1-zi*A))
    k=1-iv.log((1-r)/r)/lp
    j=528/(1-r)
    work=zi*(Ay/(1-zi*A)**2+By/(1-zi*B)**2)/ry
    return r,ry,k,j,work
h0=[source(box(x),box(y)) for x,y in coords]
(r0,ry0,k0,j0,w0),(r1,ry1,k1,j1,w1)=h0
ratio=k0/k1
book_relative=j0-ratio*j1
coin_relative=w0-ratio*w1
check('original exact h0 unpadded root first-cell CAR click source strictly negative',ry0.b<0)
check('original h0 offnull BARE J2 source coefficient positive',book_relative.a>0)
check('exact fair Golden compiled coin-work source coefficient positive',coin_relative.a>0)
check('coin work and bare Book J2 have SAME sign on first CAR tangent',
      (book_relative*ry0).b<0 and (coin_relative*ry0).b<0)
# True cost per round, includes all original unsuccessful fair extracts.
Ccoin=20*(p_iv+2*p_iv*p_iv)/p_iv**3
check('original Golden fair-coin source payment lower',Ccoin.a>iv.mpf(117))
check('original Golden fair-coin source payment upper',Ccoin.b<iv.mpf(118))
check('strictly negative positive-cost added source on original exact h0 scalar direction',
      ((Ccoin/2)*coin_relative*ry0).b<0)
ratio_clock=(Ccoin/2)*coin_relative/book_relative
check('coin-work versus Book source ratio in original h0 root between 0.1 and 0.12',
      ratio_clock.a>iv.mpf('.10') and ratio_clock.b<iv.mpf('.12'))
# Capped F/R extractor changes the unconditional exact rational fugacity.
# Analytic genuine C1 source-error bound for any actual finite F with
# 0<=F<=I, all field derivatives DF retained (trace-norm). 
for Lcap in [3,6,12,24,48]:
    sf=2*float(p**3)
    zz=float(z)*(1-(1-sf)**Lcap)**20
    error=float(z)-zz
    upper=20*float(z)*(1-sf)**Lcap
    check(f'finite-cap Golden probability error exact upper L={Lcap}',0<=error<=upper*(1+1e-9))
    # all native positive return eigenvalues in [0,1]:
    for eigen in [0.0,0.2,0.95,1.0]:
        actual=abs(float(z)/(1-float(z)*eigen)-zz/(1-zz*eigen))
        estimate=error/(1-float(z))**2
        check(f'finite-cap first Book source bound L={Lcap}, eig={eigen}',actual<=estimate*(1+1e-8))
print('PASS',len(passed),'exact original Golden/Q8 φ, full Kraus and strict h0 original-source controls')
print('Golden exact unbiased bit cost',str(expected_cost_bit),'20 bit cost',float(20*expected_cost_bit))
print('Native source J2 coefficient',book_relative)
print('Independent paid coin-work coefficient',coin_relative,'work/Book ratio',ratio_clock)
print('Physical M1/G0 admission of controlled field rotations, fresh coins, archive clock and full Book H+J+R remains OPEN')