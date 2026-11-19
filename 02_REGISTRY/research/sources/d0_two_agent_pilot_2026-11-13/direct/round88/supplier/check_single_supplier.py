"""Fourier signed transcript, actual repeated codes and economic support under failures."""
from fractions import Fraction
from itertools import product
import json
from mpmath import iv

iv.dps = 65
p = (iv.sqrt(5)-1)/2
h = p**3
eta = 4*h


def require(ok, msg):
    if not ok:
        raise ArithmeticError(msg)


def interval(value, lo, hi):
    require(value.a > iv.mpf(lo) and value.b < iv.mpf(hi), (value, lo, hi))
    return [lo, hi]


def fourier_transcript():
    sites = list(product(range(4), repeat=4))
    axes = [tuple(int(i == j) for j in range(4)) for i in range(4)]
    directions = axes + [tuple(u-v for u, v in zip(axes[i], axes[j]))
                         for i in range(4) for j in range(i)]
    co, si = (1,0,-1,0), (0,1,0,-1)
    def phase(x, k):
        return sum(a*b for a,b in zip(x,k)) % 4
    candidates = (k for k in sites if k < tuple((-a)%4 for a in k))
    modes = sorted(candidates, key=lambda k:(-sum(co[phase(d,k)] for d in directions), k))[:64]
    k = modes[0]
    require(k == (0,0,0,1), "wrong six-bit physical address")
    # Integer Fourier/CAR coefficients on the selected pair; two quadratures and
    # both occupied wave columns. Constant CAR columns have zero wrong projection.
    quads = lambda x: (co[phase(x,k)], si[phase(x,k)])
    energies = []
    for mu in range(2):
        energy = 0
        for x in sites:
            y = ((x[0]+2)%4, *x[1:])
            require(quads(x) == quads(y), "constant CAR leaked into selected sign")
            for q1,q2 in zip(quads(x),quads(y)):
                for trig in (co,si):
                    energy += (q1*trig[x[mu]] - q2*trig[y[mu]])**2
        energies.append(Fraction(energy,4*128**2))
    require(energies == [Fraction(1,64),0], "wrong full Fourier signed projection")
    A = p*iv.sin(712*iv.atan2(p,iv.sqrt(p)))
    probability = A**2 * eta*h**2/64
    bounds = interval(probability,"0.000000101912118290730","0.000000101912118290734")
    return {"index":list(k), "signed_wave_energy":[str(e) for e in energies],
            "axis0":[1,0],"axis1":[0,0],"F5_fine_probability":bounds,
            "F5_including_single_golden_unit":interval(p**2*probability,
                      "0.000000038926965321558","0.000000038926965321561"),
            "F6_fine_probability":0}


def check_latched_flags():
    # 6 measured j bits and both fine records for each axis. A materialized
    # Boolean chain has nine fresh AND targets on its successful gate records.
    wanted = (0,0,0,0,0,0,1,0,0,0)
    for raw in product((0,1),repeat=10):
        literals = tuple(x == y for x,y in zip(raw,wanted))
        acc = literals[0]
        for lit in literals[1:]:
            acc = (0 ^ (acc & lit))
        require(acc == (raw == wanted), "literal transcript tag")
        # Known-one H=1 creates the complement by actual CNOTs from H,T.
        bp, bm = 0^1^acc, 0^acc
        printed = (bp,bp,1-bm)
        length = sum(1+x for x in printed)
        require(length == (3 if acc else 6), "balanced B181 public heads")
    # Fresh zero prepared by raw ZGZ (Z is actual routed SourceI squared).
    a = iv.sqrt(p)
    g = iv.matrix([[a,-p],[p,a]])
    z = iv.matrix([[1,0],[0,-1]])
    inp = iv.matrix([a,p])
    zero = z*g*z*inp
    require(abs(zero[0]-1) < 1e-60 and abs(zero[1]) < 1e-60, "real refusal baseline")
    # If honest independent raw noise is desired, surprisal equals code length
    # at BOTH outcomes. Numerical checks validate instantiation, not a Book weight.
    for length, born in ((1,p),(2,p**2)):
        require(abs(iv.log(born)/iv.log(p)-length) < 1e-60, "conditional noise")
    return {"complete_register_columns":2**10,"conditional_public_lengths":{"tag":3,"common":6},
            "failure_zero_publications_per_block":6, "B181_passive_per_block":"p^15",
            "B181_square_movements_per_block":"18+12p+9p^3"}


def partition(n,w,rare,common,fail):
    f,c,t = w
    return t*rare**n+c*common**n+f*fail**n


def economic_test():
    # Weights need not be Born probabilities or normalized; compare an unequal
    # old supplier and include a nonzero fixed economic weight of factory failures.
    old5 = (iv.mpf(4),iv.mpf(19),iv.mpf(1)/70000000)
    old6 = (iv.mpf(7),iv.mpf(11),iv.mpf(0))
    a,b = p**6,p**3
    at = {}
    for n in (1,12,40):
        z5 = partition(n,old5,b,a,a)
        z6 = partition(n,old6,b,a,a)
        ratio = z5/z6
        require(abs(ratio-(23+old5[2]*(b/a)**n)/18) < 1e-37, "full finite sum")
        at[str(n)] = interval(ratio,*{"1":("1.27777","1.27779"),
                "12":("1.30","1.31"),"40":("9e15","1e17")}[str(n)])
        floor5 = partition(n,old5,b,a,iv.mpf(1))
        floor6 = partition(n,old6,b,a,iv.mpf(1))
        require(floor5/floor6 < 7,"unserviced refusal introduces positive floor")
    # Any positive leakage saturates. Exhibit an exact native readable false tag
    # with k independent heads all 1, mass p^(2k), conditional on an admitted flag.
    for k in (2,5,12,24):
        eps = p**(2*k)
        for n in (1,10,50):
            z5 = partition(n,old5,b,a,a)
            leaky = partition(n,(old6[0],old6[1]*(1-eps),old6[1]*eps),b,a,a)
            lim = old5[2]/(old6[1]*eps)
            ordinary = (old5[0]+old5[1])/(old6[0]+old6[1]*(1-eps))
            # The full ratio is a positive weighted mean of the two
            # sectorwise ratios, for arbitrary positive economic source.
            low = min(float(ordinary.mid),float(lim.mid))
            high = max(float(ordinary.mid),float(lim.mid))
            require(low*(1-1e-13) <= float((z5/leaky).mid) <= high*(1+1e-13),
                    "two supported rare sectors must saturate")
    return {"W5_failure_common_tag":["4","19","1/70000000"],
            "W6_failure_common_tag":["7","11","0"],
            "Z5_over_Z6_enclosures":at, "unit_factory_refusal_always_served":True,
            "leakage_at_k24":interval(p**48,"0.0000000000930","0.0000000000931"),
            "R_phys_identified":False,"GR_closed":False}


if __name__=="__main__":
    print(json.dumps({"fourier":fourier_transcript(),"flag_and_reader":check_latched_flags(),
                      "economic":economic_test()},indent=2,sort_keys=True))
