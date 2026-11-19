"""Native Fourier128 on retained SITE, or a full independent pure source."""
import itertools
import json
import math
from fractions import Fraction as F

import mpmath as mp


def require(value, label):
    if not value:
        raise ArithmeticError(label)


def original_fourier():
    sites = list(itertools.product(range(4), repeat=4))
    unit = [tuple(int(i==j) for i in range(4)) for j in range(4)]
    stencil = unit + [tuple(a-b for a,b in zip(unit[i],unit[j]))
                      for i in range(4) for j in range(i)]
    cosine = (1,0,-1,0)
    def phase(k,y):
        return sum(a*b for a,b in zip(k,y)) % 4
    candidates = [k for k in sites if k<tuple(-j%4 for j in k)]
    ordered = sorted(candidates,
                     key=lambda k: (-sum(cosine[phase(k,d)] for d in stencil), k))
    chosen = ordered[:64]
    require(len(candidates)==120 and len(stencil)==10, 'native 64 Fourier pairs')
    # Reduced common binary table, same lowest-bit output and input order as W.
    bdd = {}
    def compile_table(values, depth=0):
        if len(values)==1:
            return values[0]
        half = len(values)//2
        low = compile_table(values[:half], depth+1)
        high = compile_table(values[half:], depth+1)
        if low==high:
            return low
        return bdd.setdefault((depth,low,high),2+len(bdd))
    for i in range(4):
        for bit in (0,1):
            compile_table([(k[i]>>bit)&1 for k in chosen])
    require(len(bdd)==105, '105 nodes for original ordered table')
    coeffs = []
    for x in sites:
        tx = (x[0],(x[1]+2)%4,x[2],x[3])
        left = [0]*128
        right = [0]*128
        for j,k in enumerate(chosen):
            for y, target in ((x,left),(tx,right)):
                s = phase(k,y)
                flag = s%2
                sign = 1 if s<2 else -1
                target[2*j+flag] = sign
                for old in (0,1):
                    require((old^flag)^flag==old and sign**2==1,'W is its own inverse')
        require(sum(a*a for a in left)==64,'unit norm for each x')
        coeffs.append(F(sum(a*b for a,b in zip(left,right)),64))
    require(set(coeffs)=={F(-1,16)},'all 256 true half-period Grams')
    # For uniform freshly made Y, every Fourier column has its true Choi norm.
    # Signs in both type quadratures are the original real cosine/sine basis.
    columns = []
    for k in chosen:
        for bit in (0,1):
            columns.append(tuple((1 if phase(k,x)<2 else -1) if phase(k,x)%2==bit
                                 else 0 for x in sites))
    for j,col in enumerate(columns):
        for i in range(j+1):
            require(sum(a*b for a,b in zip(col,columns[i]))==128*(i==j),
                    'fresh pure state has Fourier marginal I/128')
    return 4*len(bdd)+36


def trial(nw, fresh):
    mp.mp.dps=70
    p=(mp.sqrt(5)-1)/2
    a=mp.sqrt(p)
    z=mp.mpf(2)**-20
    u=2*p**3
    b=(p*mp.sin(712*mp.asin(p)))**2
    iv=mp.iv
    iv.dps=60
    pi=(iv.sqrt(5)-1)/2
    ai=iv.sqrt(pi)
    c,s=iv.mpf(1),iv.mpf(0)
    ca,sa=ai,pi
    pow_=712
    while pow_:
        if pow_%2:
            c,s=c*ca-s*sa,s*ca+c*sa
        ca,sa=ca*ca-sa*sa,2*ca*sa
        pow_//=2
    require((pi*s)**2>iv.mpf(1)/10000 and (pi*s)**2<iv.mpf(1)/1000,
            'actual 712-G amplitude')
    gamma=-mp.mpf(1)/16
    tof=2*(43+nw)
    count_h=2*tof+12+16*fresh
    phases=count_h+tof+6
    f=p**2*(a*p+p**3)**2/(p**2+p**4)
    early=f**16
    def sums(q,n):
        return (1-q**n)/(1-q)
    weight=((p**3*sums(f,16))**count_h * (p**3*sums(p**2,32))**phases
            * (p**5*sums(p**4,32))**count_h)
    cold_exp=9*count_h+3*phases
    require(weight > mp.mpf(2)**(-cold_exp),'one all-first-plus physical leaf')
    beta=2*p**2
    x=beta/11
    tail=2112
    bound=264/(359*beta)*x**tail/mp.factorial(tail)/(1-x/(tail+1))
    b_rat=(F(528,359)*F(1,11)**tail/math.factorial(tail)
           /(1-F(1,11*(tail+1))))
    require(b_rat<F(1,2**27500),'integer full-heat bound')
    cc=1-2*b
    base=1-z+z*early
    t=z*weight*p
    if fresh:
        e0=u*(1-gamma)
        e1=u*(1-gamma*cc)
        v0=p-p**3*e0
        v1=p-p**3*e1
        delta=-mp.log1p(t*p**3*(e0-e1)*(v0+v1)/(base+t*v0**2))
        lower=(e0-e1)*2*z*weight*p**4*(p-p**3)
        rational_exp=cold_exp+44
        require(delta<0,'negative scalar return on one actual fresh address')
    else:
        vscale=p**3*u*gamma
        offset=p-p**3*u
        last=(base+t*(offset-vscale*cc)**2)*(base+t*(offset+vscale*cc)**2)
        contrast=((1-cc**2)*t*vscale**2
                  *(2*(base-t*offset**2)+t*vscale**2*(1+cc**2)))
        delta=128*mp.log1p(contrast/last)
        lower=128*2*z*weight*p**7*(1-z*(1+p**3))*u**2*gamma**2*(1-cc**2)
        rational_exp=cold_exp+45
        require(delta>0,'positive all-column unweighted spectral response')
    require(bound < mp.mpf(2)**-27500 < mp.mpf(2)**-rational_exp < lower < abs(delta),
            'full-heat and cold bounds')
    # Direct log-determinant subtraction, independent of the stable factorizations.
    # 4700 digits resolve both tiny differences without subtracting rounded doubles.
    with mp.workdps(4700):
        zz=mp.mpf(2)**-20
        def price(c):
            eig=[u*(1-gamma*c)] if fresh else [u*(1-gamma*c),u*(1+gamma*c)]
            return -(1 if fresh else 128)*sum(mp.log1p(zz*(early+weight*p*(p-p**3*e)**2-1))
                                               for e in eig)
        check=price(cc)-price(1)
        require(abs(check/delta-1)<mp.mpf('1e-60'),'direct high-precision trace')
    return dict(root='fresh_uniform_Y' if fresh else 'retained_full_SITE',
                full_RC3_rank_before_external_spectators=1 if fresh else 256,
                logical_Toffoli_both_legs=tof, true_Hadamard_transfers=count_h,
                phase_factories=phases, full_success_cold_weight=mp.nstr(weight,14),
                full_J_F6_minus_F5=mp.nstr(delta,14), full_heat_bound=mp.nstr(bound,14),
                rigorous_abs_DeltaJ_above_2pow=-rational_exp,
                rigorous_abs_DeltaH_below_2pow=-27500)


def main():
    nw=original_fourier()
    require(nw==456,'literal primary BDD schedule')
    return dict(native_W_toffoli=nw,clean_W_scratch=112,full_SITE_Gram='-1/16',
                final_CX_each_leaf=2112, service_caps=[16,32],
                retained=trial(nw,False), fresh=trial(nw,True),
                unknown_old_RIGHT_untouched=True, original_old_F_used_as_fresh=False,
                full_Book_Cost_minus_Info=False, GR_closed=False)


if __name__=='__main__':
    print(json.dumps(main(),indent=2,ensure_ascii=False))
