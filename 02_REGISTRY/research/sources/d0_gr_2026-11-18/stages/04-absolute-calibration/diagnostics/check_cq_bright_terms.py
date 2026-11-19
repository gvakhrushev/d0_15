"""Exact verification of all 400/8000 two/three-letter spectra and entropy-jet bounds.
Requires sibling check_cq_tail.py, NumPy, SymPy, mpmath. Outputs JSON to stdout.
"""
from collections import defaultdict, Counter
import contextlib, io, json, math, runpy
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 85
with contextlib.redirect_stdout(io.StringIO()):
    base = runpy.run_path(str(Path(__file__).with_name("check_cq_tail.py")))
N,DN,den = base['M'],base['DM'],F(base['den'])
D=432
I=np.eye(32,dtype=np.int64)
def realify(X):
    R=np.array(X.applyfunc(sp.re).tolist(),dtype=np.int64)
    J=np.array(X.applyfunc(sp.im).tolist(),dtype=np.int64)
    return np.block([[R,-J],[J,R]])
def mx(A): return int(np.max(np.abs(A)))
def mm(A,B):
    if 32*mx(A)*mx(B)>=2**59: return A.astype(object)@B.astype(object)
    return np.asarray(A,dtype=np.int64)@np.asarray(B,dtype=np.int64)
def primitive(A):
    m=mx(A)
    if not m: return np.zeros((32,32),dtype=np.int64)
    if m<2**62:
        A=np.asarray(A,dtype=np.int64); g=int(np.gcd.reduce(np.abs(A).ravel()))
    else: g=math.gcd(*[int(v) for v in A.flat])
    out=A//g
    return np.asarray(out,dtype=np.int64) if mx(out)<2**59 else out
def inner(A,B):
    if 1024*mx(A)*mx(B)>=2**60: return int(np.sum(A.astype(object)*B.astype(object)))
    return int(np.sum(np.asarray(A,dtype=np.int64)*np.asarray(B,dtype=np.int64)))
def gersafe(A): return np.asarray(A,dtype=float)

R=[];DR=[]; norm=[]; coeff=[]
for M,DM in zip(N,DN):
    if not any(M): continue
    assert all(sp.re(z).is_Integer and sp.im(z).is_Integer for z in 3200*M)
    G=realify(3200*M)
    g=int(np.gcd.reduce(np.abs(G).ravel()))
    R.append(G//g)
    X=DM*(3200*D)/g
    assert all(sp.re(z).is_Integer and sp.im(z).is_Integer for z in X)
    DR.append(realify(X))
    n=round(np.linalg.eigvalsh(gersafe(mm(R[-1].T,R[-1])))[-1])
    assert n in [10,15,25,40]
    norm.append(n); coeff.append(F(g*g,3200**2)/den)
assert len(R)==20
roots = {'Z':F(0),'S':F(1,100),'K':F(1,16),'Q':F(1,4),'I':F(1)}
root2=F(math.isqrt(2*10**90),10**45)
root_intervals={r:(v,v) for r,v in roots.items()}
root_intervals['A']=((3-2*(root2+F(1,10**45)))/25,(3-2*root2)/25)
root_intervals['B']=((3+2*root2)/25,(3+2*(root2+F(1,10**45)))/25)
def root_guess(A,d):
    vals=np.linalg.eigvalsh(np.asarray(A,dtype=float)/d)
    pts={name:float(v[0]) for name,v in root_intervals.items()}
    return tuple(sorted({min(pts,key=lambda n:abs(pts[n]-x)) for x in vals}))
def annihilator(A,deno,signature):
    P=I
    for name in signature:
        if name=='A':
            assert 'B' in signature
            B=25*A-3*deno*I
            Q=mm(B,B)-8*deno**2*I
        elif name=='B':
            assert 'A' in signature
            continue
        else:
            v=roots[name]; Q=v.denominator*A-(v.numerator*deno)*I
        P=primitive(mm(P,primitive(Q)))
    assert not np.any(P), 'failed exact annihilator'

@lru_cache(None)
def lnunit(x,steps=75):
    w=(x-1)/(x+1)
    low=2*sum(w**(2*j+1)/(2*j+1) for j in range(steps))
    return low, low+2*w**(2*steps+1)/((2*steps+1)*(1-w*w))
@lru_cache(None)
def logi(x):
    assert x>0
    k=0
    while x<1: k-=1; x*=2
    while x>=2: k+=1; x/=2
    lo,hi=lnunit(x); l2,h2=lnunit(F(2))
    return (lo+k*l2,hi+k*h2) if k>=0 else (lo+k*h2,hi+k*l2)
def interval_scale(a,T):
    return (a*T[0],a*T[1]) if a>=0 else (a*T[1],a*T[0])
def mpf(x): return mp.mpf(x.numerator)/x.denominator
@lru_cache(None)
def log_poly(signature):
    xs=[mpf(sum(root_intervals[n])/2) for n in signature]
    vals=mp.matrix([mp.log(x) if x else 0 for x in xs])
    cs=mp.lu_solve(mp.matrix([[x**j for j in range(len(xs))] for x in xs]),vals)
    coeffs=[F(int(mp.nint(c*10**15)),10**15) for c in cs]
    for n in signature:
        l,h=root_intervals[n]
        exact=(logi(l)[0],logi(h)[1]) if n!='Z' else (F(0),F(0))
        out=[F(0),F(0)]
        for j,c in enumerate(coeffs):
            term=interval_scale(c,(l**j,h**j));out[0]+=term[0];out[1]+=term[1]
        assert max(abs(exact[0]-out[1]),abs(exact[1]-out[0]))<F(1,10**12)
    return coeffs

def evaluate(k):
    gsum=defaultdict(F); moments=defaultdict(F); signatures=Counter()
    for ids in product(range(20),repeat=k):
        B=R[ids[0]]
        DB=DR[ids[0]]
        for j in ids[1:]:
            DB=mm(DR[j],B)+mm(R[j],DB)
            B=mm(R[j],B)
        deno=math.prod(norm[i] for i in ids)
        C=math.prod(coeff[i] for i in ids)/F(32*D)
        A=mm(B.T,B)
        jet=mm(DB.T,B); jet=jet+jet.T
        g=math.gcd(deno,int(np.gcd.reduce(np.abs(A).ravel())))
        A=A//g;deno//=g
        sig=root_guess(A,deno)
        annihilator(A,deno,sig)
        signatures[sig]+=1
        tr=int(np.trace(jet))
        for j in ids: gsum[coeff[j]*norm[j]]+=C*tr
        powerA=I
        for power in range(len(sig)):
            moments[sig,power]+=C*F(inner(jet,powerA),deno**power)
            if power+1<len(sig): powerA=mm(powerA,A)
    exact=sum(value*log_poly(sig)[j] for (sig,j),value in moments.items())
    lo=hi=exact
    for mu,value in gsum.items():
        l,h=interval_scale(value,logi(mu));lo+=l;hi+=h
    error=2*k*F(13,10)*F(1,10**12)
    ball=(-hi-error,-lo+error)
    # Independent exact spectral projectors, grouped AFTER the exact
    # operator polynomial proof. All possible roots belong to Q(sqrt(2)).
    alg={n:sp.Rational(v.numerator,v.denominator) for n,v in roots.items()}
    alg['A']=(3-2*sp.sqrt(2))/25; alg['B']=(3+2*sp.sqrt(2))/25
    weights=defaultdict(lambda:sp.S.Zero)
    def log_of_fraction(mu,scalar):
        for x,sgn in [(mu.numerator,1),(mu.denominator,-1)]:
            for prime,exponent in sp.factorint(int(x)).items():
                weights[str(prime)]-=sgn*scalar*exponent
    for mu,value in gsum.items(): log_of_fraction(mu,value)
    for sig in signatures:
        for label in sig:
            if label=='Z': continue
            basis=[sp.S.One]
            for other in sig:
                if other==label: continue
                old=basis; basis=[sp.S.Zero]*(len(old)+1)
                for j,c in enumerate(old):
                    cc=sp.radsimp(c/(alg[label]-alg[other]))
                    basis[j]-=cc*alg[other];basis[j+1]+=cc
            w=sp.simplify(sum(c*moments[sig,j] for j,c in enumerate(basis)))
            if label in ('A','B'):
                weights['5']+=2*w
                weights['1+sqrt(2)']+=2*w*(1 if label=='A' else -1)
            else: log_of_fraction(roots[label],w)
    weights={u:sp.simplify(v) for u,v in weights.items() if sp.simplify(v)!=0}
    return ball, {''.join(sig):v for sig,v in signatures.items()},weights

values={}; allsig={}; exact_log_coeff={}
for k in [1,2,3]:
    values[k],allsig[k],exact_log_coeff[k]=evaluate(k)
assert exact_log_coeff[2]=={u:2*w for u,w in exact_log_coeff[1].items()}
assert values[3][0]-3*values[1][1] > F(54,10**8)
diff3={u:sp.simplify(exact_log_coeff[3].get(u,0)-3*exact_log_coeff[1].get(u,0))
       for u in sorted(exact_log_coeff[3].keys()|exact_log_coeff[1].keys())}
assert allsig[2] and sum(allsig[3].values())==8000
# The closed-form one-step result and the independent trace computation agree.
def outward(I,digits=13):
    K=10**digits
    return [f"{F((I[0]*K).__floor__(),K)}",f"{F((I[1]*K).__ceil__(),K)}"]
pl=F(math.isqrt(5*10**80)-10**40,2*10**40);pu=pl+F(1,2*10**40)
assert pl**2+pl<1<pu**2+pu
lam=F(9,640)
def rrate(p):
    q=4*p**3*lam
    return q*(1-lam)/(1-q*lam)
rl,ru=rrate(pl),rrate(pu)
lo=hi=F(0);weighted={}
for k in values:
    weight=((1+pl)*(1-ru)*rl**k,(1+pu)*(1-rl)*ru**k)
    aa,bb=values[k]
    pts=[a*b for a in weight for b in (aa,bb)]
    weighted[k]=(min(pts),max(pts));lo+=min(pts);hi+=max(pts)
direct=(27*pl**2/F(25600))*(41*logi(F(2))[0]+16*logi(F(3))[0]-4*logi(F(5))[1])
t_actual=4*pl**2*lam*(1-lam)
assert values[1][0] < direct/t_actual < values[1][1]
s1=ru/(1-ru)**2-sum(j*ru**j for j in (1,2,3))
s2=ru*(1+ru)/(1-ru)**3-sum(j*j*ru**j for j in (1,2,3))
tail=2*F(13,10)*(1+pu)*(1-rl)*(logi(F(20))[1]*s2+F(142,100)*s1)
def imul(x,y):
    pts=[u*v for u in x for v in y]
    return min(pts),max(pts)
def iadd(x,y): return (x[0]+y[0],x[1]+y[1])
ql,qu=4*pl**3*lam,4*pu**3*lam
v=(ql*lam,qu*lam);o=(ql*(1-lam),qu*(1-lam));e=imul((pl,pu),o)
h=(1-v[1]-o[1]-e[1],1-v[0]-o[0]-e[0])
pc=[(F(1),F(1))];cap_jets={};zero=(F(0),F(0))
for M in range(1,4):
    pp=[h,e]+[zero]*(M-1)
    for j,x in enumerate(pc):
        pp[j]=iadd(pp[j],imul(x,v));pp[j+1]=iadd(pp[j+1],imul(x,o))
    pc=pp
    val=zero
    for j in range(1,len(pc)): val=iadd(val,imul(pc[j],values[j]))
    cap_jets[M]=outward(val)
print(json.dumps(dict(status="PASS_EXACT_HERMITIAN_ANNIHILATORS_AND_RATIONAL_INTERVALS",
    k=sorted(values),counts=allsig,normalized_jet_intervals={k:outward(x) for k,x in values.items()},
    exact_hk_log_coefficients={k:{u:str(w) for u,w in x.items()} for k,x in exact_log_coeff.items()},
    exact_h2_equals_twice_h1=True,
    exact_h3_minus_three_h1_log_coefficients={u:str(w) for u,w in diff3.items() if w},
    weighted_terms_outward_rational={k:outward(x) for k,x in weighted.items()},
    weighted_terms_midpoint={k:float(sum(x)/2) for k,x in weighted.items()},
    finite_sum_outward_rational=outward((lo,hi)),all_k_ge_4_absolute_upper_outward=outward((0,tail))[1],
    stopped_jet_outward_rational=outward((lo-tail,hi+tail)),
    finite_physical_caps_outward_rational=cap_jets,
    stopped_jet_diagnostic=[float(lo-tail),float(hi+tail)],log_uniform_error="1/10^12",
    physical_info_selected=False),indent=2))
