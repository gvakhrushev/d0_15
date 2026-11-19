"""Inward dyadic preparation of full normalized Julia and original Fourier targets."""
import itertools
import json
import math
from fractions import Fraction as F

import mpmath as mp

mp.mp.dps=72
iv=mp.iv
iv.dps=65


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def rational(field, q):
    return field.mpf(q.numerator)/q.denominator


def enclosed(real, interval, M):
    # Supply rational endpoints of width <1/M. On the present algebraic
    # fixtures the interval calculation certifies the proposed endpoints.
    k=int(mp.floor(4*M*real))
    lo,hi=F(k-1,4*M),F(k+2,4*M)
    require(interval>rational(iv,lo) and interval<rational(iv,hi),'outward enclosure')
    return lo,hi


def inward(lo,hi,M):
    if lo>=0:
        return (M*lo).__floor__()
    if hi<=0:
        return -(M*(-hi)).__floor__()
    return 0


def four_squares(n):
    require(n>=0,'integer norm deficit')
    if not n:
        return (0,0,0,0)
    scale=1
    while not n%4:
        n//=4;scale*=2
    for a in range(math.isqrt(n),-1,-1):
        rest=n-a*a
        test=rest
        while test and not test%4:
            test//=4
        if test%8==7:
            continue
        for b in range(math.isqrt(rest),-1,-1):
            t=rest-b*b
            for c in range(math.isqrt(t),-1,-1):
                d=math.isqrt(t-c*c)
                if c*c+d*d==t:
                    result=tuple(scale*j for j in (a,b,c,d))
                    require(sum(j*j for j in result)==n*scale**2,'exact four square identity')
                    return result
    raise ArithmeticError('four-square witness')


def normalize(rows,M,S,N):
    # rows=(number of equal absolute coordinates, real, certified interval).
    m=[inward(*enclosed(val,box,M),M) for count,val,box in rows]
    total=sum(count*digit**2 for (count,val,box),digit in zip(rows,m))
    deficit=M*M-total
    d=four_squares(deficit)
    require(total+sum(i*i for i in d)==M*M,'complete vector is exactly unit')
    P=1<<(N+4*S*S-1).bit_length()
    work=F(sum(count*(S*digit)**2 for (count,val,box),digit in zip(rows,m))
           + S*S*sum(i*i for i in d),P*M*M)
    require(work==F(S*S,P),'actual full work-zero probability')
    for digit in [S*j for j in m]+list(d):
        for sign in (-1,1):
            cut=M-sign*digit
            require(0<=cut<=2*M and F(2*M-2*cut,2*M)==F(sign*digit,M),
                    'absolute threshold and its full-endpoint extension')
    physical_sq=sum(count*(val-mp.mpf(digit)/M)**2 for (count,val,box),digit in zip(rows,m))
    err=mp.sqrt(physical_sq)
    k=sum(count for count,_,_ in rows)
    require(err<=2*mp.sqrt(k)/M,'physical coordinate error')
    distance=mp.sqrt(physical_sq+mp.mpf(deficit)/(M*M))
    require(distance**2<=2*err+mp.mpf('1e-65'),'full amplitude error')
    return m, dict(physical_dimension=N, nonzero_coordinates=k,padded_addresses=P,
                   integer_denominator=M,common_address_scale=S,
                   work_zero_probability=str(work),four_squares=list(d),
                   physical_vector_error=float(err),full_vector_error=float(distance))


def julia(name,M):
    # J(t*c0†) and J(Lambda(R23(pi/2))/2); second exterior matrix is
    # a signed permutation. The 112 nonzero entries are in the original 2048 slots.
    u=F(1,2)+name*F(1,32)
    ul,ui=rational(mp,u),rational(iv,u)
    vals=[(16,ul/8,ui/8),
          (16,mp.sqrt(1-ul**2)/8,iv.sqrt(1-ui**2)/8),
          (16,mp.mpf(1)/8,iv.mpf(1)/8),
          (32,mp.mpf(1)/16,iv.mpf(1)/16),
          (32,mp.sqrt(3)/16,iv.sqrt(3)/16)]
    digits,stats=normalize(vals,M,8,2048)
    # Equal superposition of one physical defect-block slot and one link slot.
    original=(vals[1][1]+vals[3][1])**2/2
    realized=F((digits[1]+digits[3])**2,2*M*M)
    require(abs(original-rational(mp,realized))<=2*stats['physical_vector_error'],
            'projected original effect before the dummy')
    # Actual operator arrays can be reconstructed numerically from the classical
    # table. Each 32x32 block obeys the Frobenius upper bound without an input port.
    frob=[]
    for chunk in ((0,1,2),(3,4)):
        frob.append(8*mp.sqrt(sum(vals[i][0]*(vals[i][1]-mp.mpf(digits[i])/M)**2
                                  for i in chunk)))
    require(max(frob)<64*8/M,'each reconstructed operator: spectral <= Frobenius')
    stats.update(raw_projected_effect=float(original),approx_projected_effect=float(realized),
                 block_Frobenius_errors=list(map(float,frob)))
    return original,realized,stats


def fourier(M):
    # F5 or F6: original 64 real pair quadratures times material CAR.
    # Find actual kappa table, all SITE signs and counts at quarter-periods.
    sites=list(itertools.product(range(4),repeat=4))
    u=[tuple(int(i==j) for i in range(4)) for j in range(4)]
    ds=u+[tuple(a-b for a,b in zip(u[i],u[j])) for i in range(4) for j in range(i)]
    def dot(k,x):
        return sum(a*b for a,b in zip(k,x))%4
    cos=(1,0,-1,0)
    candidates=[k for k in sites if k<tuple((-j)%4 for j in k)]
    chosen=sorted(candidates,key=lambda k:(-sum(cos[dot(k,d)] for d in ds),k))[:64]
    signs=[sum(1 if dot(k,x)<2 else -1 for k in chosen) for x in sites]
    require(len(signs)==256 and signs[0]==64 and len(set(signs))>1,'real Fourier signs')
    def coords(field):
        p=(field.sqrt(5)-1)/2
        a=field.sqrt(p)
        cc,ss=field.mpf(1),field.mpf(0)
        co,si=a,p
        exponent=712
        while exponent:
            if exponent%2:
                cc,ss=cc*co-ss*si,cc*si+ss*co
            co,si=co*co-si*si,2*co*si
            exponent//=2
        return [a/128,-p*cc/128,p*ss/128]
    real,boxes=coords(mp),coords(iv)
    rows=[(256*64,x,y) for x,y in zip(real,boxes)]
    require(abs(sum(256*64*t*t for t in real)-1)<mp.mpf('1e-65'),'native full Fourier norm')
    _,stats=normalize(rows,M,128,256*16*128)
    return stats


def main():
    for n in range(1024):
        require(sum(j*j for j in four_squares(n))==n,'all small residuals')
    # At a dyadic boundary the selected lower or upper bin remains admissible.
    M=2**18
    require(inward(F(1,4)-F(1,2*M),F(1,4)+F(1,2*M),M)==M//4-1,
            'non-decidable equality is unnecessary')
    require(inward(-F(1,4)-F(1,2*M),-F(1,4)+F(1,2*M),M)==-M//4+1,'negative boundary')
    require(inward(-F(1,2*M),F(1,2*M),M)==0,'unknown sign near zero')
    minus,rm,ms=julia(-1,M)
    plus,rp,ps=julia(1,M)
    h=mp.mpf(1)/32
    true=(plus-minus)/(2*h)
    actual=rational(mp,rp-rm)/(2*h)
    require(abs(true-actual)<2*max(ms['physical_vector_error'],ps['physical_vector_error'])/h,
            'finite physical secant bound')
    fresh=fourier(M)
    require(ms['work_zero_probability']==ps['work_zero_probability']==fresh['work_zero_probability']=='1/64',
            'common scaled readiness on the original indexed alphabets')
    return dict(Julia_minus=ms,Julia_plus=ps,Fourier128_F5_or_F6=fresh,
                original_effect_central_secant=float(true),realized_effect_central_secant=float(actual),
                supplies_unknown_old_operator=False,consumes_old_purifier=False,GR_closed=False)


if __name__=='__main__':
    print(json.dumps(main(),indent=2))
