"""Full growing-clock causal bound, neutral suffix, and the physical F2--F6 gain."""
import json
import sys
from fractions import Fraction as F
from math import factorial, comb
from pathlib import Path

import numpy as np

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"round75/work"))
from check_pointer_weyl import I,O


def power(x,n):
    out=I(1.)
    while n:
        if n%2:
            out=out*x
        x=x.square()
        n//=2
    return out


def growing_test():
    # Exact modular G5 with passive births |0>, a pair of inverse native
    # CX circuits on each new pair, and a genuine field-changing early letter.
    # A basis change of the fresh birth identifies the two cold vectors;
    # modular test uses |0> to check age/support rather than the Golden Born law.
    identity=np.eye(2,dtype=int)
    flip=identity[::-1]
    cx=np.eye(4,dtype=int)[[0,1,3,2]]
    assert np.array_equal(cx@cx,np.eye(4))
    def shift(old,m):
        stages=list(old)
        dims=[old[0].shape[1]]
        for _ in range(m):
            size=dims[-1]
            for d in (size,2*size):
                born=np.kron(np.eye(d,dtype=int),[[1],[0]])
                stages.append(born)
                dims.append(2*d)
            controlled=np.kron(np.eye(size,dtype=int),cx)
            stages.extend([controlled,controlled])
        # Build using true pre-edge stage dimensions, terminal g included.
        bases=[dims[0]]
        for stage in stages[:-1]:
            bases.append(stage.shape[0])
        offsets=np.cumsum([0]+bases)
        mapping=np.full(offsets[-1],-1,dtype=int)
        for j,f in enumerate(stages[:-1]):
            mapping[offsets[j]:offsets[j+1]]=offsets[j+1]+np.argmax(f,axis=0)
        final=bases[-1]
        for raw,mid in enumerate(np.argmax(stages[-1],axis=0)):
            pos=int(mid)
            for j in range(len(bases)-1,0,-1):
                if bases[j]!=bases[j-1]:
                    if pos%2:
                        break
                    pos//=2
            else:
                j=0
            mapping[offsets[-2]+raw]=offsets[j]+pos
        assert len(set(mapping))==len(mapping)
        return mapping,bases
    for m in (1,2,3):
        a,bases=shift([identity],m)
        b,_=shift([flip],m)
        assert len(a)==2+22*(4**m-1)//3
        ia,ib=np.arange(len(a)),np.arange(len(a))
        first=None
        for n in range(1,4*m+3):
            ia,ib=a[ia],b[ib]
            if np.count_nonzero(ia==np.arange(len(a)))!=np.count_nonzero(ib==np.arange(len(b))):
                first=n
                break
        assert first==4*m+1 # insensitive for k<=4m; the next moment can distinguish
    other=np.eye(4,dtype=int)[[0,3,2,1]]
    for m in (1,2):
        a,_=shift([cx,cx],m)
        b,_=shift([cx,other],m)
        ia,ib=np.arange(len(a)),np.arange(len(a))
        age=2+4*m
        for n in range(1,4*age+1):
            ia,ib=a[ia],b[ib]
            diff=np.count_nonzero(ia==np.arange(len(a)))-np.count_nonzero(ib==np.arange(len(b)))
            assert diff==(3*age if n%age==0 and (n//age)%3 else 0)


def main():
    growing_test()
    p=(I(5.).sqrt()-1)/2
    one=I(1.)
    a=p.sqrt()
    z=I.rational(F(1,2**20))
    p2,p3=p.square(),power(p,3)
    qmax=I.rational(F(38,100))
    k=1+2*a*p
    O.require((2*p*k*(one-k*qmax)).lo>.6 and (4*(one-2*qmax)).lo>.6,
              "lower gain for either the matched NPS2 or signed phase return")
    beta=2*p2
    O.require(beta.lo>.75 and (beta/22).hi<.035,"actual Hodge normalization")
    assert F(132,359)*F(4,3)*F(104,100)*F(7,200)<F(1,50)
    # For x<.035, exp(x) <= 1/(1-x) < 1.04.
    assert 1/(1-F(7,200))<F(104,100)
    H=F(1,4)
    chi=F(1)
    t,v=H/2,H*chi/20
    ca,sa=(1+t*t)/(1-t*t),2*t/(1-t*t)
    cb,sb=(1-v*v)/(1+v*v),2*v/(1+v*v)
    field=sa*sb*(2+(ca-1)*(1-cb))/(2*H*H)
    assert field==F(16517734400,162621047169) and F(160,1601)*chi<field<chi/8
    base=4*p3
    rf=4*p2*(one-2*p2)*z*(one-z*base)*(one-base)
    rq=8*p3*(one-2*p2)*(z*(I(2.)-base)-z.square()*(base+2*(one-base)*base))
    k0=rq/rf
    b=I.rational(field/16)/k0
    h=I.rational(F(1,8*4096))
    phase=one-2*p2
    for _ in range(9):
        phase=2*phase.square()-1
    visibility=(one-phase)*power(p,7)/2
    # Original geometric amplitude divided by the unreported *actual* alpha_H^2.
    gain=power(p,36)*705600*2*p3*visibility*rf*rq*h.square()*b
    O.require(gain.lo>0,"full geometric tariff coefficient per actual readiness squared")
    def heat_ratio(m):
        return F(1,50)*F(7,200)**(4*m)/(4**m*factorial(4*m))
    examples=[]
    for length in (0,64,256):
        gamma=F(3,5)*F(1,2**20)*F.from_float(float(gain.lo))*F.from_float(float(p.lo))**(3*length)
        def coefficient(m):
            return heat_ratio(m)/gamma
        m=0
        while coefficient(m)>F(1,10**6):
            m+=1
        examples.append({"archive_bits":length,"neutral_blocks":m,
                         "relative_bound_per_S_over_rank_alpha2":float(coefficient(m)),
                         "previous_bound":float(coefficient(m-1))})
    print(json.dumps({"F_grid":str(field),"true_b_ref":O.bounds(b),
                      "g_H_per_alpha_H_squared":O.bounds(gain),
                      "neutral_prefix_moments_exact_cases":3,"fixture_bounds":examples},indent=2))


if __name__=="__main__":
    main()
