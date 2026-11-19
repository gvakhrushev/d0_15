"""One observed output; certify interval gain, disjoint selector and both native columns."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import sys

from mpmath import iv

file = Path(__file__).resolve()
sys.path.insert(0,str(file.parents[2]/"round80"/"price"))
sys.path.insert(0,str(file.parents[4]/"d0_native_readiness_amplification_2026-10-24"))
from check_parity_price import a, p, one, Golden, action, ne
from native_phase import phase_word, native_rotation_intervals

iv.dps = 55
phi = (1+iv.sqrt(5))/2
pp = 1/phi
ell = iv.log(phi)


def small_native_projector():
    width=6
    r=5
    layout=ne.Execution(width,(r,),(),(),ne.G_CX_SOURCE_I,2,(0,1))
    gates=tuple(gate for bits in ((0,0),(1,1))
                for gate in phase_word(layout,(3,4),bits,r,1,
                                       max_qubits=6,max_expanded_stages=500))
    co,si=one,Golden()
    for _ in range(4):
        co,si=a*co-p*si,p*co+a*si
    for index in range(1<<width):
        output={index:one}
        for g in gates:
            output=action(output,g,width)
        control_pair=(index>>1)&3
        expected={index:one} if control_pair in (1,2) else {
            index:co,index^1:(-si if index&1 else si)}
        assert expected==output
    return len(gates)


def leaf_count(L):
    counts=[1,1]
    for _ in range(2,L+1):
        counts.append(counts[-1]+counts[-2])
    return counts[L]


def eta_interval(K,k):
    _,s=native_rotation_intervals((1<<K)*k,bits=212)
    lo,hi=(F(int(t.p),int(t.q)) for t in s)
    assert lo*hi>0
    return min(lo**2,hi**2),max(lo**2,hi**2)


def interval(x):
    return iv.mpf(x.numerator)/x.denominator


def rank_cut_check(L, bins):
    # For small price 24, visit every exact-price cylinder in lexicographic order,
    # retaining overshoots separately. For 36 the same recursion gives the counts.
    occupied=[0]*len(bins); exact=skip=0
    from bisect import bisect_right
    from itertools import accumulate
    ends=list(accumulate(bins))
    def walk(price):
        nonlocal exact,skip
        if price>=L:
            if price>L:
                skip+=1
            else:
                j=bisect_right(ends,exact)
                if j<len(occupied):
                    occupied[j]+=1
                exact+=1
            return
        walk(price+1)
        walk(price+2)
    walk(0)
    assert exact==leaf_count(L) and skip==leaf_count(L-1) and occupied==bins
    return exact,skip


def collect_parity_rotations(owner):
    # Compile exactly on the whole register. The accepted indicator is affine
    # in the eight signed live head Z's, so nine integer transforms suffice.
    import numpy as np
    def transform(values):
        out=values.copy()
        step=1
        while step<len(out):
            view=out.reshape(-1,2*step)
            left=view[:,:step].copy()
            right=view[:,step:].copy()
            view[:,:step]=left+right
            view[:,step:]=left-right
            step*=2
        return out
    labels=np.array([-1 if v is None else v for v in owner])
    indicators=[(labels==j).astype(np.int64) for j in range(8)]
    inputs=[sum(indicators)]+[(-1 if j%2==0 else 1)*b for j,b in enumerate(indicators)]
    words=negative=rotations=routes=previous=0
    for group,values in enumerate(inputs):
        coeff=transform(values)
        assert np.array_equal(transform(coeff),len(values)*values)
        head=0 if group==0 else 1<<(15+group)
        for index in range(len(values)):
            key=index^(index>>1)
            count=int(coeff[key])
            if not count:
                continue
            mask=head|key
            routes+=bin(mask^previous).count("1")
            previous=mask
            rotations+=abs(count)
            words+=1
            negative+=int(count<0)
    routes+=bin(previous).count("1")
    # One direct native sign conjugation Z G^m Z for a negative block if
    # the target is the SourceI port; otherwise actual port routing is extra.
    return dict(nonzero_parity_blocks=words,negative_blocks=negative,
                logical_G=rotations,parity_CX=routes)



def heralded_selector(bins):
    # Disjoint dyadic cover; inspect every uniform 16-bit address and both signs.
    width=16
    owner=[None]*(1<<width)
    chunks=[]
    start=0
    for j,count in enumerate(bins):
        stop=start+count
        while start<stop:
            alignment=(start & -start) if start else 1<<width
            size=min(alignment,1<<((stop-start).bit_length()-1))
            length=width-(size.bit_length()-1)
            chunks.append((length,start//size,j))
            for x in range(start,start+size):
                assert owner[x] is None and (x>>(width-length))==start//size
                owner[x]=j
            start+=size
    assert [owner.count(j) for j in range(8)]==bins
    assert owner.count(None)==(1<<width)-sum(bins)
    maximum=1+max(b for b,_,_ in chunks)
    assert maximum==17 and len(chunks)==74
    alo,ahi=eta_interval(maximum,1)
    blo,bhi=eta_interval(1,4)
    mass=iv.mpf(sum(bins))/(1<<width)
    low=mass*pp**2*interval(alo*blo)
    high=mass*pp*interval(ahi*bhi)
    assert iv.mpf(".2")<low and high<iv.mpf(".4")
    attempts=8
    born=(1-(1-2*pp**3)**attempts)**width
    econ=(1-pp**attempts)**width
    posterior=1/(1+(1-econ)/econ*pp**17)
    assert born>iv.mpf(".9") and posterior>iv.mpf(".999")
    return dict(registered_preparation_bits=width*attempts,dyadic_blocks=len(chunks),
                combined_first_pointer=collect_parity_rotations(owner),
                logical_unit_rotations=len(chunks)*(1<<maximum)+8,
                probability_success=round(float(born.mid),12),
                economic_success_lower_bound=round(float(posterior.mid),12),
                observable_min=round(float(low.mid),12),observable_max=round(float(high.mid),12))



def verify_header_prices():
    # Coefficient k counts physical 128-bit headers with k successes and all positions ready.
    import math
    active=[1]
    for _ in range(16):
        nxt=[0]*(len(active)+8)
        for j,count in enumerate(active):
            for k in range(1,9):
                nxt[j+k]+=count*comb(8,k)
        active=nxt
    assert sum(active)==255**16
    full=[comb(128,k) for k in range(129)]
    assert all(a<=b for a,b in zip(active,full)) and sum(full)==2**128
    pnum=(5**.5-1)/2; logphi=-math.log(pnum)
    u=2*pnum**3
    c=(1-(1-u)**8)**16
    ent=lambda b: -(b*math.log(b)+(1-b)*math.log(1-b))/logphi
    for s in (.24433,.28,.34,.39533):
        for a0 in (0,.25,.5,.75,1):
            t=1-a0
            gain=a0*(128*ent(u)+c*ent(s))
            groups=[]
            for k,success in enumerate(active):
                for count,cond,extra,score,label in (
                        (success,1-s,6,-1/(1-s),"ready zero"),
                        (success,s,12,1/s,"ready one"),
                        (full[k]-success,1,23,0,"failed")):
                    if not count:
                        continue
                    logpr=k*math.log(u)+(128-k)*math.log(1-u)+math.log(cond)
                    price=128+k+extra-gain+t*logpr/logphi
                    grad=-a0*c*math.log((1-s)/s)/logphi+t*score/logphi
                    groups.append((count,price,grad,label))
            z=sum(count*pnum**price for count,price,_,_ in groups)
            slope=sum(count*pnum**price*grad for count,price,grad,_ in groups)/z
            lo=min(price for _,price,_,_ in groups)
            assert all(label=="ready zero" for _,price,_,label in groups if price==lo)
            d=pnum*(1-u)**(-t); v=pnum**2*u**(-t)
            ct=(1-(d/(d+v))**8)**16
            tail=pnum**6*((1-s)**(-t)+pnum**6*s**(-t))
            checked=pnum**(-gain)*(d+v)**128*(ct*tail+(1-ct)*pnum**23)
            assert abs(z/checked-1)<8e-13
            assert slope<-.18 and c*(6-2*math.log((1-s)/s)/logphi)>.20



def main():
    verify_header_prices()
    examples={}
    for L,D,power,k in [(24,840,1,1),(36,705600,2,4)]:
        nn=[F(D*comb(8,j),j**power) for j in range(1,9)]
        assert all(x.denominator==1 for x in nn)
        bins=[int(x) for x in nn]
        if L==24:
            rank_cut_check(L,bins)
            compact=heralded_selector(bins)
        assert sum(bins)<=leaf_count(L)
        eta_lo,eta_hi=eta_interval(L+1,k)
        active=sum(bins)*pp**L
        lower=interval(eta_lo)*active*pp**2
        upper=interval(eta_hi)*active*pp
        assert lower>iv.mpf("0.2") and upper<iv.mpf("0.4")
        examples[L]={"active_cylinders":sum(bins),"K":L+1,"k":k,
                     "read_efficiency":round(float(eta_lo),12),
                     "s_min":round(float(lower.mid),12),"s_max":round(float(upper.mid),12),
                     "target_unit_rotations":sum(bins)*k*(1<<(L+1))}
    # A uniform derivative margin on the entire rectangle 0.2<=s<=0.4, 0<=a<=1.
    ratio=pp**6
    event_margin=(1-16*ratio)/((1+4*ratio)*ell)
    drop_margin=iv.log(iv.mpf(3)/2)/ell
    bell_margin=6-2*iv.log(4)/ell
    assert event_margin>iv.mpf(".18") and drop_margin>iv.mpf(".84")
    assert bell_margin>iv.mpf(".23") and 4*ratio<1
    # Explicit equality of slopes at finite parameter values as independent sanity checks.
    import math
    pnum=(5**.5-1)/2; lnum=-math.log(pnum)
    for s in (.22,.3,.378):
        for alpha in (0,.25,.5,.75,1):
            t=1-alpha
            def action_fs(u):
                ent=-(u*math.log(u)+(1-u)*math.log(1-u))/lnum
                return -alpha*ent-math.log((1-u)**(-t)+pnum**6*u**(-t))/lnum
            ratio0=(1-s)/s
            slope=-alpha*math.log(ratio0)/lnum-t*(1-pnum**6*ratio0**(t+1))/(
                lnum*(1-s)*(1+pnum**6*ratio0**t))
            delta=1e-6
            assert abs((action_fs(s+delta)-action_fs(s-delta))/(2*delta)-slope)<2e-8
    print(json.dumps(dict(smaller_native_word_gates=small_native_projector(),
                          exact_columns_checked=64,
                          selector=examples,
                          header_words_via_exact_multiplicities=str(2**128),
                          compact_geometric_selector=compact,
                          absolute_logsum_slope_magnitude_lower_bound=.18,
                          bell_slope_lower_bound=.23,
                          full_large_words_executed=False,
                          GR_closed=False),indent=2))


if __name__=="__main__":
    main()
