"""One untrained golden code for a full binary-report classical archive."""
from fractions import Fraction as Q
from itertools import product
from math import comb, log, sqrt
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"coding"))
from check_trained_golden_code import add, sub, mul, field, sign, emit, ONE, P


def golden_index(index, size):
    """A prefix word for a uniform finite index, without allocating size entries."""
    lo,hi=field(Q(index,size)),field(Q(index+1,size))
    mid=field(Q(2*index+1,2*size))
    pos,span=(0,0),ONE
    result=[]
    while sign(sub(pos,lo))<0 or sign(sub(add(pos,span),hi))>0:
        left=mul(span,P)
        cut=add(pos,left)
        if sign(sub(mid,cut))<0:
            result.append(0)
            span=left
        else:
            result.append(1)
            pos,span=cut,sub(span,left)
    assert sign(sub(span,mul(mul(P,P),field(Q(1,2*size)))))>0
    return emit(result)


def type_ranks(group, d):
    counts=[0]*d
    for x in group:
        counts[x]+=1
    n=len(group)
    size=comb(n+d-1,d-1)
    rank=0
    remaining=n
    for i,x in enumerate(counts[:-1]):
        k=d-i-1
        rank+=comb(remaining+k,k)-comb(remaining-x+k,k)
        remaining-=x
    multiplicity=1
    remaining=n
    for x in counts:
        multiplicity*=comb(remaining,x)
        remaining-=x
    # Lexicographic rank among all distinct permutations of this multiset.
    arrangement=0
    ways=multiplicity
    remaining=n
    for x in group:
        arrangement+=ways*sum(counts[:x])//remaining
        ways=ways*counts[x]//remaining
        counts[x]-=1
        remaining-=1
    assert 0<=rank<size and 0<=arrangement<multiplicity
    return rank,size,arrangement,multiplicity


def encode(block,dims):
    groups=[[],[]]
    tag=[]
    for t,x in block:
        if t not in (0,1) or not 0<=x<dims[t]:
            raise ValueError("event not in the declared finite archive")
        tag.append(("0","1010")[t])
        groups[t].append(x)
    h0,M0,v0,A0=type_ranks(groups[0],dims[0])
    h1,M1,v1,A1=type_ranks(groups[1],dims[1])
    header=golden_index(h0*M1+h1,M0*M1)
    body=golden_index(v0*A1+v1,A0*A1)
    return "".join(tag),header,body,M0*M1,A0*A1


def test():
    phi=(sqrt(5)+1)/2
    lp=log(phi)
    # One field with changing binary event and both changing conditional laws.
    weights=[Q(1,8),Q(3,8),Q(1,4),Q(1,4)]
    tangent=[Q(1,7),-Q(2,7),Q(3,7),-Q(2,7)]
    options=[(0,0),(0,1),(1,0),(1,1)]
    m=4
    actual={}
    lengths=[Q(),Q()]
    entropy=jet=score_check=0.
    for j,p in enumerate(weights):
        entropy-=float(p)*log(float(p))/lp
        jet-=float(tangent[j])*log(float(p))/lp
    for outcomes in product(range(4),repeat=m):
        block=tuple(options[j] for j in outcomes)
        tag,header,body,M,A=encode(block,(2,2))
        code=tag+header+body
        assert code not in actual
        actual[code]=outcomes
        probability=Q(1); score=Q()
        for j in outcomes:
            probability*=weights[j]
            score+=tangent[j]/weights[j]
        lengths[0]+=probability*len(code)/m
        lengths[1]+=probability*score*len(code)/m
        assert 0<=len(header+body)-log(M*A)/lp<2*(2+log(2)/lp)
        score_check+=float(probability*score)
    ordered=sorted(actual)
    assert all(not y.startswith(x) for x,y in zip(ordered,ordered[1:]))
    q=float(weights[2]+weights[3]);dq=float(tangent[2]+tangent[3])
    h=(-q*log(q)-(1-q)*log(1-q))/lp
    F=1+3*q-h
    dF=(3-log((1-q)/q)/lp)*dq
    lnM=2*log(m+1)
    constant=2*(2+log(2)/lp)
    fisher=float(sum(y*y/p for p,y in zip(weights,tangent)))
    error=float(lengths[0])-entropy-F
    derivative=float(lengths[1])-jet-dF
    assert abs(score_check)<1e-14 and 0<=error<=(lnM/lp+constant)/m
    assert abs(derivative)<=(sqrt(lnM**2+2)/lp+constant)*sqrt(fisher/m)
    print("all",len(actual),"archives injective and prefix-free; mean length, derivative:",*lengths)
    print("finite excess above target and derivative of excess",error,derivative)
    sample=encode(((1,0),(0,1),(1,1)),(2,2))
    print("example: binary tags, type header, arrangement",sample[:3])


if __name__=="__main__":
    test()
