"""Full DATA terminal, true RIGHT retained, on the fixed-portal geometric ray."""
import json
from pathlib import Path
from fractions import Fraction as Q
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "round75/work"))
import check_pointer_weyl as source

O, I = source.O, source.I
LOG2 = O.logarithm(I(2))


def sum_right(a):
    # Exact interval addition over the 128 Fourier columns.
    while a.lo.shape[-1] != 1:
        a = a[..., ::2] + a[..., 1::2]
    return a[..., 0]


def log_point(x):
    """Vector logarithm with directed atanh series and a rational uniform tail."""
    m, exponent = np.frexp(x)
    m = I(2*m)
    t = (m-1)/(m+1)
    total, power = I(0), t
    for j in range(20):
        total = total+power*Q(2, 2*j+1)
        power = power*t*t
    error = I.rational(Q(2, 3**41)*Q(9, 8*41))
    return total+I(0., error.hi)+I(exponent-1)*LOG2


def stats(z, dz):
    mass = sum_right(z.square())
    jet = 2*sum_right(z*dz)
    pos = mass.lo > 0
    logs = I(log_point(mass.lo[pos]).lo, log_point(mass.hi[pos]).hi)
    entropy = -O.reduce_sum(jet[pos]*logs)
    # At a vanishing row -dP log(P) extends continuously to zero. For an
    # unresolved positive row, bound the exact score using its amplitude.
    unresolved = (~pos) & (mass.hi > 0)
    if np.any(unresolved):
        O.require(np.max(mass.hi[unresolved]) < 2**-80, "Unresolved sizable data mass")
        squared_norm = O.reduce_sum(dz[unresolved].square())
        dz_norm = I(0., squared_norm.hi).sqrt()
        bound = I(2)*I.rational(Q(1,2**40))*80*LOG2*I(int(unresolved.sum())).sqrt()*dz_norm
        entropy = entropy+I(-bound.hi,bound.hi)
    return mass, jet, entropy


def main():
    p, state, w, dw, fw, bw, u, du, _ = source.site_vector()
    # SITE is lexicographically encoded on eight bits; the four CAR bits
    # follow. A different fixed order of these twelve bits has the same length.
    hamming = I(np.array([[bin(site).count("1")+bin(mask).count("1")
                           for mask in range(16)] for site in range(256)]))
    entropy, length, normal, tip, tv = (I(0.) for _ in range(5))
    log_p = O.logarithm(p)
    for coeff in range(2):
        values, derivatives = source.actions(coeff,w,dw,fw,bw,u,du)
        for j,(v,dv) in enumerate(zip(values,derivatives)):
            blank = j == 0 and coeff == 0
            for port in ((0,1) if blank else (1,)):
                fac = -2*(p*p if port == 0 else p*p.sqrt())
                z, dz = (v*fac+state if blank and port == 0 else v*fac), dv*fac
                mass, jet, h = stats(z,dz)
                scale = I(1.) if blank else 1+p
                normal = normal+scale*O.reduce_sum(mass)
                dprob = O.reduce_sum(jet)
                tip = tip+scale*dprob
                tv = tv+scale*O.reduce_sum(I(np.maximum(0,np.maximum(jet.lo,-jet.hi)),
                                               np.maximum(np.abs(jet.lo),np.abs(jet.hi))))*Q(1,2)
                length = length+scale*O.reduce_sum(hamming*jet)
                entropy = entropy+scale*h
                if not blank:
                    # The other port has mass p times the recorded row.
                    entropy = entropy-p*dprob*log_p
    entropy = entropy/(-log_p)
    O.require(normal.contains(1) and tip.contains(0), "Incomplete DATA record")
    O.require(entropy.lo > -0.000320942 and entropy.hi < -0.000320940, "Full data entropy source")
    O.require(length.lo > 0.0000396593 and length.hi < 0.0000396595, "Literal twelve-symbol source")
    O.require(tv.lo > 0.0007771326 and tv.hi < 0.0007771328, "Total variation of data")
    heat_lower = Q(220465,10**7)
    required_spread = (I.rational(heat_lower)-entropy)/tv
    O.require(required_spread.lo > 28.78, "Range needed from the complete data tariff")
    O.require((I.rational(heat_lower)-Q(434416,10**8)+length-entropy).lo > 0.01806,
              "Best possible old pointer code plus literal data")
    result = {"necessary_spread_lower": float(required_spread.lo),
              "dH_fine_mark_DATA_RIGHT":O.bounds(entropy),
              "d_literal_DATA_length":O.bounds(length),"d_length_minus_H":O.bounds(length-entropy),
              "total_variation_of_jet":O.bounds(tv)}
    print(json.dumps(result))


if __name__ == "__main__":
    main()
