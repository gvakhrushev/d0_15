"""Exact lower bound for the stopped full128 fine-CQ direct source at the §7gb CAR tangent."""
from fractions import Fraction as F
import json
import math
import sympy as s

I, O = s.eye(16), s.zeros(16)
lam = s.Rational(9,640)
order = (0,2,3,1)
word, jet, cs = [], [], []
for r in range(4):
    c = O.copy()
    for x in range(16):
        if not x & (1<<r):
            c[x | (1<<r), x] = (-1)**sum((x>>j)&1 for j in order[:order.index(r)])
    cs.append(c)
def rootjet(root, rhs):
    return s.Matrix(16,16,lambda i,j: rhs[i,j]/(root[i,i]+root[j,j]))
def expand(M):
    return M.applyfunc(s.expand)
for r,c in enumerate(cs):
    base = s.Rational(3,5)*c
    db = cs[0]-cs[1] if r==0 else O
    ph = (s.I,s.I,-1,-s.I)[r]
    l=I-c*c.H/5; h=4*I/5+c*c.H/5
    dl=rootjet(l,-db*base.H-base*db.H)
    dh=rootjet(h,-db.H*base-base.H*db)
    for w,v in zip(((ph*base,l),((ph*base).H,h),(-base,-l),(-base.H,-h)),
                   ((ph*db,dl),((ph*db).H,dh),(-db,-dl),(-db.H,-dh))):
        word.extend((w,w)); jet.extend((v,v))
def walsh(w):
    return [sum(((-1)**(bin(l&j).count("1")%2)*w[j][b] for j in range(32)), O.copy())/32
            for l in range(32) for b in (0,1)]
N,DN=walsh(word),walsh(jet)
a,da=N[0],DN[0]
assert a==a.H and da==da.H and expand(a*a)==lam*I and expand(a*da+da*a)==O
assert expand(sum((x*x.H for x in N),O.copy()))==I
assert expand(sum((dx*x.H+x*dx.H for x,dx in zip(N,DN)),O.copy()))==O
M=[expand(x.H*a) for x in N[1:]]
DM=[expand(dx.H*a+x.H*da) for x,dx in zip(N[1:],DN[1:])]
den=lam*(1-lam)
assert expand(sum((m.H*m for m in M),O.copy()))==den*I
assert expand(sum((dm.H*m+m.H*dm for m,dm in zip(M,DM)),O.copy()))==O
assert len([m for m in M if m!=O])==20
gram=expand(sum((dm.H*dm for dm in DM),O.copy()))/den
# Rational upper bound on the Hermitian operator norm by row sums. Each
# Gaussian-rational off-diagonal entry has modulus <= |Re|+|Im|.
k2=max(sum(abs(s.re(gram[i,j]))+abs(s.im(gram[i,j])) for j in range(16)) for i in range(16))
assert k2 < s.Rational(13,10)**2
# Exact recovery of the direct entropy coefficient, avoiding any spectral approximation.
from collections import defaultdict
coeff=defaultdict(lambda:s.S.Zero)
for x,dx in zip(N[1:],DN[1:]):
    H=expand(x*x.H); dH=expand(dx*x.H+x*dx.H)
    assert H==s.diag(*H.diagonal())
    for eig,der in zip(H.diagonal(),dH.diagonal()):
        if not eig: assert der==0
        else: coeff[eig]+=der
coeff={mu:v for mu,v in coeff.items() if v}
assert coeff=={s.Rational(81,100):-s.Rational(27,10),s.Rational(1,400):s.Rational(3,20),
               s.Rational(1,100):s.Rational(3,20),s.Rational(9,640):s.Rational(6,5),
               s.Rational(27,3200):s.Rational(6,5)}

def logbounds(x):
    y=F(x-1,x+1); n=90
    low=2*sum(y**(2*i+1)/(2*i+1) for i in range(n))
    return low, low+2*y**(2*n+1)/((2*n+1)*(1-y*y))

pl,pu=F(6180,10000),F(6181,10000)
assert pl*pl+pl<1<pu*pu+pu
ll=F(9,640); q_upper=4*pu**3*ll
rr=F(131,10000)
assert q_upper*(1-ll)/(1-q_upper*ll) < rr
assert logbounds(20)[1]<3 and F(142,100)**2>2
dlo=27*pl**2/F(25600)*(41*logbounds(2)[0]+16*logbounds(3)[0]-4*logbounds(5)[1])
dhi=27*pu**2/F(25600)*(41*logbounds(2)[1]+16*logbounds(3)[1]-4*logbounds(5)[0])
q0=4*pl**3*ll
rlo=q0*(1-ll)/(1-q0*ll)
firstlo=dlo*(1-rr)/(1-q0*ll)
firsthi=dhi*(1-rlo)/(1-q_upper*ll)
# S1=sum_{k>=2} k r^k, S2=sum_{k>=2} k^2 r^k.
s1=rr/(1-rr)**2-rr
s2=rr*(1+rr)/(1-rr)**3-rr
tail=2*F(13,10)*(1+pu)*(3*s2+F(142,100)*s1)
assert firstlo-tail>F(45,10000)
# Couple capped and uncapped category patterns. The entropy jet changes only
# if M continuations are followed by at least one additional bright letter.
future_mean=1/(1-rr)
future_second=(1+rr)/(1-rr)**2
def time_error(M):
    return q_upper**M*(1+pu)*rr*2*F(13,10)*(
        3*(2*M*M+2*M*future_mean+future_second)+F(142,100)*(2*M+future_mean))
assert dlo-time_error(1)>F(15,10000)
assert all(time_error(M)>time_error(M+1) for M in range(1,10))
p=(math.sqrt(5)-1)/2
q=4*p**3*float(ll); r=q*(1-float(ll))/(1-q*float(ll))
direct=27*p**2/25600*(41*math.log(2)+16*math.log(3)-4*math.log(5))
print(json.dumps(dict(status="PASS_EXACT_POSITIVE_STOPPED_CQ_SOURCE",
    nonquiet_nonzero_labels=20,one_round_derivative=direct,normalized_bright_stinespring_gram_row_bound=str(k2),
    amplitude_jet_norm_strict_upper="13/10",q=q,bright_continuation_after_quiet_loops=r,
    exact_one_bright_contribution_numerical=direct*(1-r)/(1-q*float(ll)),
    one_bright_term_rigorous_lower=float(firstlo),all_k_ge_2_absolute_upper=float(tail),
    signed_sum_lower=float(firstlo-tail),signed_sum_upper=float(firsthi+tail),
    genuine_time_cap_derivative_error_upper={M:float(time_error(M)) for M in [1,2,3,4,6]},
    direct_one_round_minus_time_error_lower=float(dlo-time_error(1)),
    certified_lower_rational="> 45/10000",natural_logs=True,physical_Book_Info_selected=False),indent=2))
