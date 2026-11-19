"""Exact Fourier overlap and a physical Golden readout of null CAR-wave energy."""
from fractions import Fraction as F
from itertools import product
import json
import math


def require(ok, label):
    if not ok:
        raise ArithmeticError(label)


SITES = list(product(range(4), repeat=4))
P = (math.sqrt(5)-1)/2
A = math.sqrt(P)
GAP = 5/512
C = F(5,16)
H = F(1,4)
PHASE = ((1,0), (0,1), (-1,0), (0,-1))
WAVES = ((0,1,2,0), (0,2,1,0))


def add(x, y):
    return (x[0]+y[0], x[1]+y[1])


def scale(k, x):
    return (k*x[0], k*x[1])


def mul(x, y):
    a,b = x
    c,d = y
    return (a*c+b*d, a*d+b*c-b*d)


def positive(x):
    v,b = 2*x[0]-x[1], x[1]
    if b > 0:
        return v >= 0 or 5*b*b > v*v
    if b < 0:
        return v > 0 and v*v > 5*b*b
    return v > 0


def amplitude():
    # cos(2 theta)=p^3=2p-1, p^2=1-p. All recurrences in Z[p].
    c = (-1,2)
    prev, cur = (1,0), c
    for n in range(2,449):
        prev, cur = cur, add(scale(2,mul(c,cur)), scale(-1,prev))
        if n == 224:
            require(positive(scale(-1,cur)), "positive canonical filler")
    twice_b = mul((1,-1),add((1,0),scale(-1,cur)))
    for times, low, high in [(16,".00701775",".00701776"),(32,".01403550",".01403551")]:
        energy = scale(times,twice_b)
        require(positive(add(energy,(-F(low),0))) and positive(add((F(high),0),scale(-1,energy))),
                "exact native energy bracket")
    # Multiply the actual 448 G rotations on their active two-level plane.
    x,y = 1.0,0.0
    for _ in range(448):
        x,y = A*x-P*y,P*x+A*y
    amp, filler = P*y,-P*x
    require(filler > 0 and abs(P+amp*amp+filler*filler-1) < 2e-13, "actual CAR state")
    require(32*amp*amp < GAP < 64*amp*amp, "A88 midpoint")
    return amp, filler


def fourier():
    unit = [tuple(int(i==j) for i in range(4)) for j in range(4)]
    stencil = unit+[tuple(a-b for a,b in zip(x,y)) for i,x in enumerate(unit) for y in unit[:i]]
    def dot(k,x):
        return sum(a*b for a,b in zip(k,x)) % 4
    modes = [k for k in SITES if k<tuple(-v%4 for v in k)]
    modes.sort(key=lambda k:(-sum((1,0,-1,0)[dot(k,x)] for x in stencil),k))
    chosen = modes[:64]
    chi = {}
    for x in SITES:
        vec = [0]*128
        for j,k in enumerate(chosen):
            n = dot(k,x)
            vec[2*j+n%2] = 1 if n<2 else -1
        chi[x] = vec
    for x in SITES:
        nxt = ((x[0]+1)%4,)+x[1:]
        require(sum(u*v for u,v in zip(chi[x],chi[nxt])) == 20, "20/64 adjacent kernel")
    # True original Fourier128 column Gram, not a pointwise copy of SITE.
    columns = list(zip(*(chi[x] for x in SITES)))
    for i,col in enumerate(columns):
        for j,other in enumerate(columns[:i+1]):
            require(sum(u*v for u,v in zip(col,other)) == (128 if i==j else 0), "Fourier Gram")
    return chi


def committed_profiles(amp, filler):
    fields = [{x:(amp*PHASE[wave[x[0]]][0],amp*PHASE[wave[x[0]]][1])
               for x in SITES} for wave in WAVES]
    for x in SITES:
        if x[0] in (0,3):
            require(fields[0][x] == fields[1][x], "common time endpoints")
    # Direct short test on an unknown copy: least-significant CAR bit, masks 1 and 15.
    cheap = []
    for wave,field in zip(WAVES,fields):
        for x,psi in field.items():
            require(abs(sum(v*v for v in (A,filler,*psi))-1)<2e-13, "positive filler")
        cheap.append([sum(P + field[x][1]**2 for x in SITES if x[0]//2==j)/128 for j in (0,1)])
    require(cheap[0][0] > cheap[0][1] and cheap[1][0] < cheap[1][1], "local CAR contrast")
    # A non-null test with nonconstant filler, for the general energy meter.
    fields.append({x:((1+x[0]+x[2])/40,(x[0]-x[1])/35) for x in SITES})
    return fields


def energy_meter(field,chi,ends,condition):
    # A full unnormalized Fourier component (Y, physical CAR mask, j,type).
    # The D=1 amplitude after G^{-1} is a*p*(shifted-input minus input).
    left,right = ends
    all_sites = [x for x in SITES if not condition or x[0] in ends]
    active = [x for x in all_sites if x[0] in ends]
    diffs, masses = [], []
    for x in active:
        nx = (right if x[0]==left else left,) + x[1:]
        old, new = field[x], field[nx]
        masses.append(sum(z*z for z in old))
        for i in (0,1):
            diffs.append(sum((new[i]*b-old[i]*a)**2 for a,b in zip(chi[x],chi[nx]))/64)
    measured = P**3 * math.fsum(diffs)/len(all_sites)
    mass = math.fsum(masses)/len(all_sites)
    fallback = sum(1 for u,v in product(range(2),repeat=2) if u!=v)*P**3*F(11,16)
    # Measuring B=(D xor (outside & background)) is a genuine disjoint union.
    result = measured + float(fallback)*(1-mass)
    energy = math.fsum(sum((q-s)**2 for q,s in zip(field[x],field[(right,)+x[1:]]))
                       for x in SITES if x[0]==left) / (64*float(H)**2)
    expected = 2*P**3*(1-float(C)) + P**3*float(C)*float(H)**2*energy*len(active)/len(all_sites)
    require(abs(result-expected)<3e-14, "registered full Fourier energy")
    return energy, result


def mask_and_selector():
    # Paid 4-CAR mask computation, heralded Toffoli on its successful leaf.
    for digits in range(16):
        b0 = digits&1
        work = [((digits>>j)&1) ^ b0 ^ 1 for j in (1,2,3)]
        scratch = work[0]&work[1]
        out = scratch&work[2]
        scratch ^= work[0]&work[1]
        old = [v^1^b0 for v in work]
        require(not scratch and old == [(digits>>j)&1 for j in (1,2,3)], "CAR restore")
        require(out == (digits in (0,15)), "retained active masks")
    for y, d, at in product(range(4), (0,1), (0,1)):
        require((y ^ (d&at))//2 == y//2, "measured interval preserved")
        hi, low = divmod(y, 2)
        both = hi & low
        one, two = low ^ both, hi ^ both
        require((one, two) == (int(y == 1), int(y == 2)), "raw temporal predicates")
        for j in (0,1):
            active = d & at
            if not j:
                # Fredkin: CX, Toffoli, CX. When active this swaps only 01 and 10.
                a1, a0 = hi, low ^ hi
                a1 ^= active & a0
                a0 ^= a1
            else:
                a1, a0 = hi, low ^ (active & hi)
            pair = ((1,2),(2,3))[j]
            expected = sum(pair)-y if active and y in pair else y
            require(2*a1+a0 == expected, "interior pair selector")
    # Random registered switch samples an independently prepared calibration wave.
    for u,v,r in product((0,1), repeat=3):
        require(((r & u) ^ ((1-r) & v)) == (u if r else v), "literal mux")


if __name__ == "__main__":
    amp, filler = amplitude()
    chi = fourier()
    mask_and_selector()
    fields = committed_profiles(amp,filler)
    waves = []
    for n,field in enumerate(fields):
        values = [energy_meter(field,chi,e,True) for e in ((0,1),(2,3),(1,2))]
        unselected = [energy_meter(field,chi,e,False) for e in ((1,2),(2,3))]
        if n<2:
            waves.append(values)
        require(len(unselected) == 2, "two free base cells")
    require(waves[0][0][1] < waves[0][1][1] and waves[1][0][1] > waves[1][1][1],
            "two opposite material tags")
    require(waves[0][2][0] < GAP < waves[0][1][0], "two interior-origin responses")
    print(json.dumps({"a89":"owned H.1 null wave energy", "golden_G_rotations":448,
                      "native_energy_low_interval":["0.00701775","0.00701776"],
                      "native_energy_high_interval":["0.01403550","0.01403551"],
                      "a88_midpoint":"5/512","adjacent_fourier_inner_product":"20/64",
                      "original_fourier_column_gram":"I128/128 after physical 1/128 scale",
                      "wave_phases_quarter_turns":WAVES,"quadratic_energy_tests":15,
                      "direct_registered_probabilities":[[format(m,".12f") for _,m in row[:2]] for row in waves],
                      "common_temporal_boundary_slices":[0,3],
                      "universal_fixed_transverse_material_collar":False,
                      "h1_microscopic_total_price_derived":False,"GR_closed":False},
                     indent=2,sort_keys=True))
