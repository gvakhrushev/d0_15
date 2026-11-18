"""Verify non-renewal and absolute count inversion for the original blank port."""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
DIRECT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(DIRECT/"round75/work"),str(DIRECT/"round75/curvature")]
import check_pointer_weyl as original
import check_local_coframe_source as trace_owner

I,O = original.I,original.O


def physical_master():
    p,C,w,dw,fw,bw,u,du,_ = original.site_vector()
    words,dwords = [C,u],[None,du]
    for k in range(2,5):
        words.append(original.dirac(words[k-1],w,fw,bw))
        dwords.append(original.dirac(dwords[k-1],w,fw,bw)
                      +original.dirac(words[k-1],dw,fw,bw))
    # E=(B^2-I)C. The subtraction of a multiple of C keeps all RIGHT columns.
    e = -4*p*p*(words[2]-p*p*words[4])
    de = -4*p*p*(dwords[2]-p*p*dwords[4])
    first = O.reduce_sum(C*e)
    dfirst = O.reduce_sum(C*de)
    centered = e-C*first
    variance = O.reduce_sum(centered.square())
    dvariance = 2*O.reduce_sum(centered*(de-C*dfirst))
    O.require(variance.lo>0,"complete original preparation is not regenerated")
    result={k:O.bounds(v) for k,v in (
        ("P1",1+first),("P2",1+2*first+O.reduce_sum(e.square())),
        ("P2_minus_P1_squared",variance),("D_P1",dfirst),
        ("D_P2_minus_P1_squared",dvariance))}
    def a(v,jet=False):
        return original.dirac(v,dw if jet else w,fw,bw)
    def k(v):
        a2=a(a(v))
        return 4*p*p*(a2-p*p*a(a(a2)))
    def dx(v):
        field=a(v)
        change=a(v,True)
        d2=None
        for degree in range(2,5):
            change=a(field,True)+a(change)
            field=a(field)
            if degree==2:
                d2=change
        return -4*p*p*(d2-p*p*change)
    # At n=1 use the actual geometric clock p and the Neumann series centered
    # at X=I. Trace owner's certified ||D||<5 gives ||I-X||<.01.
    t=p
    scale=I(1.)/(I(1.)-t)
    ratio=t*scale
    term=C
    ys=C
    zs=C
    for j in range(1,7):
        term=-ratio*k(term)
        ys=ys+term
        zs=zs+(j+1)*term
    Y,Z=scale*ys,scale.square()*zs
    rad=ratio*Q(1,100)
    power=rad
    for _ in range(6):
        power=power*rad
    ey=scale*power/(I(1)-rad)
    kernel=I(1.)/(I(1.)-rad)
    ez=scale.square()*power*(8*kernel+rad*kernel.square())
    O.require(ey.hi<1e-12 and ez.hi<2.1e-11 and
              max(abs(dw.lo).max(),abs(dw.hi).max())<10,"Neumann remainders and geometric leg bound")
    def widen(v,width):
        return v+I(-float(width),float(width))
    # ||dA0|| <= (sum sqrt(g_j))/4 * max|dw| < 12.5. Thus ||dX||<16.
    # ||Y_exact||<3, ||Z_exact||<7, ||Y_trunc||<4, ||Z_trunc||<8.
    DY=dx(Y)
    mu=widen(O.reduce_sum(C*Y),ey.hi)
    dma=t*widen(O.reduce_sum(Y*DY),float((16*7*ey).hi))
    dsecond=2*t*widen(O.reduce_sum(Z*DY),float((16*(3*ez+8*ey)).hi))
    vr=widen(O.reduce_sum((Y-C*mu).square()),float((20*ey).hi))
    dv=dsecond-2*mu*dma
    absolute=mu-1
    dbias=dv/absolute-vr*dma/absolute.square()
    O.require(dma.lo>1.55002e-5 and dma.hi<1.55005e-5 and
              dbias.lo>2.1558e-5 and dbias.hi<2.1562e-5,
              "actual full-state source and larger memory correction")
    result["Golden_p"]={k:O.bounds(v) for k,v in (
        ("absolute_mass",absolute),("D_absolute_mass",dma),
        ("excess_of_mean_N_minus_one",vr/absolute),("D_excess",dbias))}
    return result


def average(x):
    # Every singular value occurs twice in B on the complete 4096 DATA space.
    return O.reduce_sum(x)*Q(1,2048)


def gap(x):
    return average((x-average(x)).square())


def clock_results(x,t):
    # U/t is O(1) even for the small original clock.
    y=x/(I(1.)-t*x)
    return {"absolute_mass":O.bounds(t*average(y)),
            "excess_of_mean_N_minus_one":O.bounds(t*gap(y)/average(y))}


def trace_results():
    s,_=trace_owner.numerical_basis()
    # The primary polar residual is <1.2e-8 in operator norm. The extra
    # slack includes the rounded endpoint construction, even at a zero mode.
    singular=I(np.maximum(0.,s-2e-8),s+2e-8)
    p=I(trace_owner.P.lo,trace_owner.P.hi)
    b=I(1.)-p*p*Q(1,2048)*singular.square()
    results={}
    for n in (1,8192):
        native_b=trace_owner.I(b.lo,b.hi)
        native_x=trace_owner.power(native_b,2*n)
        x=I(native_x.lo,native_x.hi)
        p1,p2,variance=average(x),average(x.square()),gap(x)
        O.require(variance.lo>0 and (variance-(p2-p1.square())).contains(0),
                  "strict physical trace non-renewal")
        block={"P1":O.bounds(p1),"P2":O.bounds(p2),
               "P2_minus_P1_squared":O.bounds(variance),
               "Golden_p":clock_results(x,p),
               "fixed_2^-20":clock_results(x,I.rational(Q(1,2**20)))}
        if n==1:
            O.require(x.lo.min()>.99,"short record accuracy on this trace carrier")
            width=I(1.)-I(float(x.lo.min()))
            block["mass_error_relative_to_upper_three_bins"]=float((width.square()*width).hi)
        results[n]=block
    return results


def exact_normalized_hankel():
    # Test scale recovery with no regeneration on an independent rational example.
    nodes=(Q(1,4),Q(3,4))
    weights=(Q(1,3),Q(2,3))
    t=Q(2,3)
    a=sum(w*t*x/(1-t*x) for x,w in zip(nodes,weights))
    g=[sum(w*x**k for x,w in zip(nodes,weights))/a for k in range(5)]
    det=g[2]*g[4]-g[3]**2
    O.require(det>0 and (g[1]**2*g[4]-2*g[1]*g[2]*g[3]+g[2]**3)/det==1/a,
              "exact one-histogram Hankel inverse with distinct live modes")
    O.require(sum(w*(t*x/(1-t*x))**2 for x,w in zip(nodes,weights))/a>a,
              "normalized mean overcounts the absolute mass")


if __name__=="__main__":
    exact_normalized_hankel()
    print(json.dumps({"material_full_RIGHT":physical_master(),
                      "trace_4096":trace_results()},indent=2,sort_keys=True))
