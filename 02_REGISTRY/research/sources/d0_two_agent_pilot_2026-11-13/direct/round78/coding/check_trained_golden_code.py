"""A deterministic golden code from training counts, with an exhaustive small test."""
from fractions import Fraction as Q
from itertools import product
from math import comb, log, sqrt
import argparse

# a+b*p with p=(sqrt(5)-1)/2 and p*p=1-p. All encoder comparisons are exact.
def add(x,y):
    return x[0]+y[0], x[1]+y[1]


def sub(x,y):
    return x[0]-y[0], x[1]-y[1]


def mul(x,y):
    a,b=x
    c,d=y
    return a*c+b*d,a*d+b*c-b*d


def sign(x):
    a,b=x
    k=2*a-b
    if b==0:
        return (k>0)-(k<0)
    if k*b>=0:
        return 1 if b>0 else -1
    if k*k>5*b*b:
        return 1 if k>0 else -1
    return 1 if b>0 else -1


def field(q):
    return q,0


P=(0,1)
ONE=(1,0)


def interval_for(counts, word):
    total=sum(counts)+len(counts)
    weights=[Q(x+1,total) for x in counts]
    cdf=[sum(weights[:i],Q(0)) for i in range(len(counts))]
    lo,width=Q(0),Q(1)
    for x in word:
        lo+=width*cdf[x]
        width*=weights[x]
    return lo,width


def encode(counts,word):
    """Return the physical decision symbols; 0 prints 0, 1 prints 10."""
    lo,width=interval_for(counts,word)
    hi,mid=field(lo+width),field(lo+width/2)
    low=field(lo)
    pos,mass=(0,0),ONE
    bits=[]
    while sign(sub(pos,low))<0 or sign(sub(add(pos,mass),hi))>0:
        left=mul(mass,P)
        cut=add(pos,left)
        if sign(sub(mid,cut))<0:
            bits.append(0)
            mass=left
        else:
            bits.append(1)
            pos,mass=cut,sub(mass,left)
    assert sign(sub(mass,mul(mul(P,P),field(width/2))))>0
    assert sign(sub(field(width),mass))>=0
    return tuple(bits)


def emit(symbols):
    return ''.join(('0','10')[x] for x in symbols)


def finite_test():
    p=(sqrt(5)-1)/2
    lp=-log(p)
    natural=lambda q:log(q)/lp
    # Genuine tilt P(pass|L)=p^L on L=0,2. Differentiate in the live prior u=P(L=2).
    u=0.4
    survival=1-u+u*p*p
    v=u*p*p/survival
    du=1.
    dv=p*p/survival**2
    n,m=4,4
    average=code_jet=cross=plugin_jet=0.
    widths=[]
    for hits in range(n+1):
        training=comb(n,hits)*u**hits*(1-u)**(n-hits)
        train_score=hits/u-(n-hits)/(1-u)
        counts=(n-hits,hits)
        words=list(product(range(2),repeat=m))
        codes=[emit(encode(counts,w)) for w in words]
        assert len(set(codes))==len(codes)
        assert all(not b.startswith(a) for a in codes for b in codes if a!=b)
        for w,code in zip(words,codes):
            ones=sum(w)
            chance=v**ones*(1-v)**(m-ones)
            score=train_score+dv*(ones/v-(m-ones)/(1-v))
            _,mass=interval_for(counts,w)
            ideal=-natural(float(mass))
            width=len(code)-ideal
            widths.append(width)
            average+=training*chance*len(code)/m
            code_jet+=training*chance*score*len(code)/m
            cross+=training*chance*ideal/m
            plugin_jet+=training*chance*score*ideal/m
    redundancy=2+natural(2)
    fisher_mu=du**2/(u*(1-u))
    fisher_v=dv**2/(v*(1-v))
    round_jet=redundancy*sqrt(n*fisher_mu+m*fisher_v)/(2*m)
    assert min(widths)>0 and max(widths)<redundancy
    assert 0<=average-cross<redundancy/m
    assert abs(code_jet-plugin_jet) < round_jet
    entropy=-v*natural(v)-(1-v)*natural(1-v)
    entropy_jet=dv*natural((1-v)/v)
    ce=-v*natural(u)-(1-v)*natural(1-u)
    ce_jet=dv*natural((1-u)/u)+((1-v)/(1-u)-v/u)/lp
    target=-natural(survival)
    target_jet=(1-p*p)/(survival*lp)
    assert abs(2*v+ce-entropy-target)<4e-15
    assert abs(2*dv+ce_jet-entropy_jet-target_jet)<1e-14
    large_n=10_000
    large_m=large_n**2
    a=min(u,1-u)
    e0=max(log((large_n+2)/(large_n+1)),log(1+1/(large_n*a)))
    e1=(1-a)**large_n/a+1/((large_n+1)*a*a)
    error=e0/lp+redundancy/large_m
    jet_error=(2*abs(dv)*e0+e1)/lp+redundancy*sqrt(large_n*fisher_mu+large_m*fisher_v)/(2*large_m)
    assert error<.000520 and jet_error<.00229
    print("bounds at n=10000, m=n^2",error,jet_error)
    print("finite example: code, derivative on tilted blocks",average,code_jet)
    print("exact target and derivative",target,target_jet,"training and selected score both included")


def check_learning_bounds():
    # Exact binomial identity for the two bounds on n E[log(1+1/(K+1))].
    for n in (1,2,7,20):
        for u in (Q(1,12),Q(2,5),Q(9,10)):
            PM=[comb(n-1,k)*u**k*(1-u)**(n-1-k) for k in range(n)]
            upper=n*sum(a/(k+1) for k,a in enumerate(PM))
            lower=n*sum(a/(k+2) for k,a in enumerate(PM))
            assert upper==(1-(1-u)**n)/u
            assert upper-lower<=1/((n+1)*u*u)
            assert lower<=upper and upper<=1/u


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--counts",nargs="+",type=int)
    parser.add_argument("--word",nargs="+",type=int)
    args=parser.parse_args()
    if args.counts is not None or args.word is not None:
        if not args.counts or args.word is None or any(x<0 for x in args.counts):
            parser.error("provide nonnegative --counts and --word")
        if any(x<0 or x>=len(args.counts) for x in args.word):
            parser.error("word outside the declared alphabet")
        print(emit(encode(args.counts,args.word)))
        return
    check_learning_bounds()
    finite_test()


if __name__=="__main__":
    main()
