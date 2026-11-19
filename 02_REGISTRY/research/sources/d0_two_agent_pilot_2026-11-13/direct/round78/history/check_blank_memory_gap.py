"""True blank likelihood, conditional RIGHT entropy and the lost spectral information."""
import hashlib
import json
import os
import sys
from fractions import Fraction as Q
from math import comb
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.dont_write_bytecode = True
import numpy as np

direct = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(direct / "round75/work"))
sys.path.insert(0, str(direct / "round75/curvature"))
import check_pointer_weyl as W
import check_local_coframe_source as coframe

I, O, spectral = W.I, W.O, W.spectral
d = 128


def tr(a):
    return O.reduce_sum(I(np.diag(a.lo), np.diag(a.hi)))


def widen(value, error):
    return value + I(-float(error.hi), float(error.hi))


def compressed_log(E, DE, j):
    # H=I-E, f(H)=H log H. Tr d(E^m)=m Tr(E^(m-1) dE) even for moving eigenvectors.
    order = 10
    power = E
    static, tangent = -tr(E)/d, -tr(DE)/d
    for m in range(2, order + 1):
        tangent += tr(spectral.matmul(power, DE)) / (d*(m-1))
        power = spectral.matmul(power, E)
        static += tr(power) / (d*m*(m-1))
    radius = I.rational(Q(j,100))
    tail_size = I(1.)
    for _ in range(order):
        tail_size *= radius
    summed = tail_size/(I(1.)-radius)
    return (widen(static, summed*radius/(order*(order+1))),
            widen(tangent, summed*(16*j)/order))


def main():
    for rel, digest in O.PINS.items():
        O.require(hashlib.sha256((W.ROOT/rel).read_bytes()).hexdigest() == digest, rel)
    p,C,w,dw,fw,bw,_,_,_ = W.site_vector()
    logphi = -O.logarithm(p)
    O.require(max(abs(dw.lo).max(),abs(dw.hi).max())<10,"two-site leg norm bound")
    # The flat singular basis has a verified polar residual below 1.2e-8.
    singular, _ = coframe.numerical_basis()
    O.require(max(singular)+2e-8 < 5, "full native Dirac norm including the polar residual")
    amax = I.rational(Q(5,64))
    O.require((4*p*p*amax.square()).hi < .01, "I-X spectral radius")
    # Differentiate four role stencils, ||DA0|| <= max(dw)*sum(sqrt(g))/4 < 12.5.
    O.require((4*p*p*(2*amax+4*p*p*amax*amax.square())*Q(25,2)).hi < 16, "DX norm")

    def kernel(x, jet):
        # K=I-X=4p^2(A0^2-p^2 A0^4), A0=hD/16, on the whole live DATA carrier.
        for r in range(1,5):
            jet = W.dirac(jet,w,fw,bw) + W.dirac(x,dw,fw,bw)
            x = W.dirac(x,w,fw,bw)
            if r == 2:
                x2, d2 = x, jet
        return 4*p*p*(x2-p*p*x), 4*p*p*(d2-p*p*jet)

    vectors, jets = [C], [I(np.zeros_like(C.lo))]
    for _ in range(6):
        v, dv = kernel(vectors[-1], jets[-1])
        vectors.append(v)
        jets.append(dv)

    def inner(x,y):
        return O.reduce_sum(x*y)
    moments, dmoments = [I(1.)], [I(0.)]
    for m in range(1, 12):
        i, k = m//2, (m+1)//2
        moments.append(inner(vectors[i],vectors[k]))
        dmoments.append(inner(jets[i],vectors[k])+inner(vectors[i],jets[k]))

    def moment(fam, j, r=0):
        return sum(((-1)**i*comb(j,i)*fam[r+i] for i in range(j+1)), I(0.))
    def pwr(j):
        return sum(((-1)**i*comb(j,i)*vectors[i] for i in range(1,j+1)),
                   I(np.zeros_like(C.lo)))
    flat_c,Wct = W.flatten(C),spectral.transpose(W.flatten(C))
    O.require(spectral.matmul(Wct,flat_c).contains(np.eye(d)/d), "uniform prepared RIGHT")
    rows, calculations = {}, []
    for j in (1, 2, 3):
        # E=V*(I-X^j)V positive, V=sqrt(128)C. Use I-X^j directly to avoid leading cancellation.
        loss_vec = -pwr(j)
        dl_vec = sum(((-1)**(i+1)*comb(j,i)*jets[i] for i in range(1,j+1)),
                     I(np.zeros_like(C.lo)))
        E = d*spectral.matmul(Wct,W.flatten(loss_vec))
        DE = d*spectral.matmul(Wct,W.flatten(dl_vec))
        Pj, DPj = moment(moments,j), moment(dmoments,j)
        O.require((I(1.)-tr(E)/d-Pj).contains(0), "EA marginal and birth trace")
        h,dh = compressed_log(E,DE,j)
        # s=Tr rho X^j log(X^j)=-j sum_{r>=1} Tr rho X^j K^r/r.
        order=8
        s,ds = (sum((-j*moment(fam,j,r)/r for r in range(1,order+1)), I(0.))
                for fam in (moments,dmoments))
        rad = I.rational(Q(1,100))
        rem = I.rational(Q(1,100**order))/(I(1.)-rad)
        s = widen(s,j*rem*rad/(order+1))
        ds = widen(ds,16*j*rem*(1+j*rad/(order+1)))
        leak = inner(loss_vec,loss_vec)-tr(spectral.matmul(E,E))/d
        raw = -O.logarithm(Pj)/logphi
        draw = -DPj/Pj/logphi
        post = (h/Pj-O.logarithm(Pj))/logphi
        dpost = (dh/Pj - h*DPj/Pj.square() - DPj/Pj)/logphi
        gap = (s-h)/Pj/logphi
        if j == 1:
            after_count = gap - (Pj-moment(moments,2))/(2*65536*Pj*I.rational(Q(99,100))*logphi)
            O.require(after_count.lo > 7e-8, "positive additional discrimination with a finite counter")
        dgap = ((ds-dh)/Pj - (s-h)*DPj/Pj.square())/logphi
        energy = -s/Pj/logphi
        denergy = (-ds/Pj + s*DPj/Pj.square())/logphi
        O.require((energy+post+gap-raw).contains(0) and
                  (denergy+dpost+dgap-draw).contains(0),"all costs and field jets")
        O.require(leak.lo>0 and gap.lo>0,"native prepared subspace leaks spectral information")
        rows[j] = {name: O.bounds(v) for name,v in
                   (("raw",raw),("D_raw",draw),("right_gain",post),("D_right_gain",dpost),
                    ("spectral_price",energy),("D_spectral_price",denergy),
                    ("gap",gap),("D_gap",dgap),("escape_squared",leak))}
        calculations.append((draw,dpost,dgap,denergy))
    first_leak = rows[1]["escape_squared"]
    assert 1.09466362e-7 < first_leak[0] <= first_leak[1] < 1.09466364e-7
    curvature = [last-2*middle+first for first,middle,last in zip(*calculations)]
    assert 2.2169217e-6 < curvature[2].lo <= curvature[2].hi < 2.2169285e-6
    assert -4.145027e-6 < curvature[0].lo <= curvature[0].hi < -4.145021e-6
    assert 1.887337e-6 < curvature[1].lo <= curvature[1].hi < 1.887345e-6
    assert -8.249294e-6 < curvature[3].lo <= curvature[3].hi < -8.249288e-6
    print(json.dumps({"by_length":rows,"second_difference_D":
                      dict(zip(("raw","right_gain","gap","spectral_price"),map(O.bounds,curvature)))},
                     sort_keys=True,indent=2))


def verify_comparison_counter():
    from itertools import product
    import sympy as sp
    # Full two-branch projection tape in two exact nontrivial principal planes.
    for a, b in ((sp.Rational(3,5), sp.Rational(4,5)), (sp.Rational(5,13), sp.Rational(12,13))):
        u = sp.Matrix([[a,-b],[b,a]])
        ready, eye = sp.diag(1,0), sp.eye(2)
        counts = [sp.Integer(0)]*6
        for outcomes in product((0,1), repeat=5):
            state, previous, count = eye[:,0], 1, 0
            for i, y in enumerate(outcomes):
                state = (ready if y else eye-ready)*(u if i%2 == 0 else u.T)*state
                count += int(y == previous)
                previous = y
            mass = (state.T*state)[0]
            assert mass == (a*a)**count*(1-a*a)**(5-count)
            counts[count] += mass
        assert counts == [comb(5,k)*(a*a)**k*(1-a*a)**(5-k) for k in range(6)]


if __name__ == "__main__":
    verify_comparison_counter()
    main()
