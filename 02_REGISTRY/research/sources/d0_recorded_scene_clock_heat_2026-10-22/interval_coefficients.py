"""Positive Laurent-series coefficients, with outward interval arithmetic.

No FFT cancellation is used to resolve the tiny winding terms. The entire
33-mode scene (three collective modes and 8+10+12 within-part modes) is kept.
"""
from mpmath import mp, iv
import json
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING

def upper(x):return mp.mpf(x.b._mpi_[1])
def lower(x):return mp.mpf(x.a._mpi_[0])
def directed(x,upward):
    sign,man,expo,_=mp.mpf(x)._mpf_
    num=(-1 if sign else 1)*man
    den=1
    if expo>=0:num <<= expo
    else:den <<= -expo
    with localcontext() as ctx:
        ctx.prec=50;ctx.rounding=ROUND_CEILING if upward else ROUND_FLOOR
        return format(Decimal(num)/Decimal(den),'E')
def su(x):return directed(x,True)
def sl(x):return directed(x,False)

def coefficients(K=64,dps=90):
    mp.dps=dps;iv.dps=dps
    p=(iv.sqrt(5)-1)/2;beta=2*p*p
    sizes=(9,11,13);degrees=(26,24,22)
    B=iv.matrix(3);C=iv.diag([iv.mpf(1)/x for x in degrees])
    for i in range(3):
        for j in range(3):
            B[i,j]=0 if i==j else iv.sqrt(iv.mpf(sizes[i]*sizes[j])/(degrees[i]*degrees[j]))
    pol=[iv.eye(3)];coef=[iv.mpf(0) for _ in range(K+1)]
    w=iv.mpf(1)
    for k in range(K+1):
        for n in range(k+1):coef[n]+=w*sum(pol[n][i,i] for i in range(3))
        if k==K:break
        nxt=[];zero=iv.zeros(3)
        for n in range(k+2):
            a=B*pol[n] if n<=k else zero.copy()
            a+=C*pol[abs(n-1)] if abs(n-1)<=k else zero
            if n+1<=k:a+=C*pol[n+1]
            nxt.append(a)
        pol=nxt;w*=beta/(k+1)
    # Silent scene modes contribute their exact Bessel positive series.
    for n in range(K+1):
        for size,degree in zip(sizes,degrees):
            x=beta/degree
            term=x**n/iv.factorial(n);total=iv.mpf(0)
            for j in range(K+1):
                if n+2*j>K:break
                total+=term
                term*=x*x/((j+1)*(n+j+1))
            coef[n]+=(size-1)*total
    # For the entire normalized adjacency at theta=0, spectral norm <=1.
    # The coefficient remainder of each scalar scene trace is bounded by
    # 33 sum_{k>K} beta^k/k!, with a geometric majorant for the positive tail.
    tail=33*beta**(K+1)/iv.factorial(K+1)/(1-beta/(K+2))
    return beta,coef,tail

def bessel_bound(n,x):
    # I_n(x) <= (x/2)^n/n! * exp(x^2/(4(n+1))).
    return (x/2)**n/iv.factorial(n)*iv.exp(x*x/(4*(n+1)))

def source_bounds(m,beta,with_scene=True):
    a=iv.mpf(12)/13 if with_scene else iv.mpf(0)
    c=iv.mpf(1)/22 if with_scene else iv.mpf(1)/2
    x=2*beta*c
    # Majorize all winding orders by a geometric factorial-ratio bound.
    b0=bessel_bound(m,x)
    ratio=(x/2)**m/iv.mpf(1)
    for k in range(m+1,2*m+1):ratio/=k
    if not bool(ratio.b<1):raise RuntimeError('tail ratio >=1')
    B1=b0/(1-ratio)**2
    B2=2*b0*ratio/(1-ratio)**3
    c1=2*iv.exp(beta*(1+a))/beta*B1
    c2mix=2*iv.exp(beta*(1+a))/beta*B2+4*iv.exp(2*beta*(1+a))/beta*B1*B1
    return {'m':m,'first_source_constant_upper':su(upper(c1)),
            'second_source_D2V_constant_upper':su(upper(c1)),
            'second_source_DV_DV_constant_upper':su(upper(c2mix)),
            'B1_upper':su(upper(B1)),'B2_upper':su(upper(B2)),
            'successive_winding_majorant_ratio_upper':su(upper(ratio))}

def main():
    beta,coef,tail=coefficients()
    out={'precision':90,'Taylor_degree':64,'beta_bounds':[sl(lower(beta)),su(upper(beta))],
         'coefficient_common_tail_upper':su(upper(tail)),
         'coefficient_bounds':[[sl(lower(c)),su(upper(c+tail))] for c in coef],
         'source_bounds_scene':[source_bounds(m,beta,True) for m in [3,8,11,15,16,32]],
         'source_bounds_cycle':[source_bounds(m,beta,False) for m in [3,8,11,15,16,32]],
         'scope':'explicit fixed-scene homogeneous-fibre connection graph; not compulsory native scene choice'}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
