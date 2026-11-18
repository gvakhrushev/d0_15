"""Exact signed-winding scene walk on two native D=11 growing clocks.

Run with Python 3 next to the pinned check_heat_history.py. Probability and
moment checks use rational arithmetic in Q(a), a^4+a^2=1. This is a replay
with known addresses and known gate matrices, not an experimental oracle.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb, factorial, lcm
from pathlib import Path
import json
import runpy


def need(value, label):
    if not value:
        raise ArithmeticError(label)


owner = Path(__file__).with_name("check_heat_history.py")
need(sha256(owner.read_bytes()).hexdigest() ==
     "577ad99d9c25ae20d097e2841304ca2f2887cb10b5adc28d37b914734458b783",
     "pinned complete-clock fixtures")
g = runpy.run_path(str(owner))
zero, one, const, p = (g[k] for k in ("ZERO", "ONE", "const", "P"))
bounds = g["algebraic_bounds"]
decimal = g["decimal_enclosure"]
D = g["D"]
SIZES = (9, 11, 13)
PART = tuple(part for part, n in enumerate(SIZES) for _ in range(n))
ROWS = tuple(35 - SIZES[part] for part in PART)
SCALE = lcm(*ROWS)
ORDER = 19
BETA = const(2) * p**2


def windings():
    """Explicit Markov recursion on every vertex and every signed temporal winding.

    For each initial part one fixed vertex suffices by permutation symmetry.
    The initial average is uniform on vertices, so these weights are 9,11,13.
    Each literal outgoing spatial edge gets 1/d_x and each ± step gets 1/d_x.
    """
    closed = [defaultdict(int) for _ in range(ORDER+1)]
    abs_all = [0]*(ORDER+1)
    neighbors = [[y for y in range(33) if PART[x] != PART[y]] for x in range(33)]
    for size, origin in zip(SIZES, (0, 9, 20)):
        state = {(origin, 0): 1}
        for k in range(ORDER+1):
            total = SCALE**k
            need(sum(state.values()) == total, "full rooted probability")
            for (vertex, winding), mass in state.items():
                abs_all[k] += size*abs(winding)*mass
                if vertex == origin:
                    closed[k][winding] += size*mass
            if k == ORDER:
                break
            nxt = defaultdict(int)
            for (x, w), mass in state.items():
                routed = mass*(SCALE//ROWS[x])
                for y in neighbors[x]:
                    nxt[y, w] += routed
                nxt[x, w-1] += routed
                nxt[x, w+1] += routed
            state = nxt
    for k, row in enumerate(closed):
        need(all(row[w] == row[-w] for w in tuple(row)), "symmetric winding law")
        need(F(abs_all[k], 33*SCALE**k) <= F(k, 11), "time-letter winding bound")
    return closed


def compare_scene_polynomial(closed):
    """Separate 3x3 scene quotient + all 30 intrapart modes; no path states."""
    coefficients, other_scale = g["scene_moment_coefficients"](ORDER)
    need(other_scale == SCALE, "independent denominator")
    for k, (row, polynomial) in enumerate(zip(closed, coefficients)):
        for w in range(-k, k+1):
            from_power = sum(c*comb(n, (n+w)//2) for n, c in enumerate(polynomial)
                             if abs(w) <= n and (n+w)%2 == 0)
            need(row.get(w, 0) == from_power, "full Laurent trace coefficient")
    # Test the exact symmetric similarity locally on every spatial edge:
    # Bxy=(dx dy)^(-1/2); row walk weight=(dy/dx)^1/2 Bxy=1/dx.
    for x, y in product(range(33), repeat=2):
        if PART[x] != PART[y]:
            need(F(ROWS[y], ROWS[x])*F(1, ROWS[x]*ROWS[y]) == F(1, ROWS[x]**2),
                 "positive square-root similarity")


def divided(x, n):
    return const(F(1, n))*x


def dyadic_floor(x, bits):
    low, high = bounds(x)
    multiplier = 2**bits
    left, right = (t*multiplier//1 for t in (low, high))
    need(left == right, "certified dyadic bucket")
    return F(left, multiplier)


def word_values(name, first, second, closed):
    report, _, tr2, time = g["fixture"](name, first, second)
    powers = [g["eye"](D)]
    for _ in range(ORDER):
        powers.append(g["mul"](powers[-1], time))
    traces = [g["trace"](m) for m in powers]
    need(traces[0] == const(D) and traces[2] == tr2, "actual time moments")
    t2_diagonal = [powers[2][i][i] for i in range(D)]
    t2_intervals = [bounds(x) for x in t2_diagonal]
    positive = next(i for i, (lo, _) in enumerate(t2_intervals) if lo > 0)
    negative = next(i for i, (_, hi) in enumerate(t2_intervals) if hi < 0)
    for i in (positive, negative):
        click = divided(one+t2_diagonal[i], 2)
        dyadic = dyadic_floor(click, 32)
        low, high = bounds(click)
        need(dyadic <= low <= high <= dyadic+F(1, 2**32), "frozen capped threshold")
    # Compare a literal frozen uniform string for the two results:
    # mismatches occupy precisely the interval of thresholds between them.
    c1, c2 = [dyadic_floor(divided(one+t2_diagonal[i], 2), 32)
              for i in (positive, negative)]
    need(c1 > c2 and ((c1-c2)*2**32).denominator == 1, "frozen disagreement mass")
    seq = []
    scaled_mark = zero
    for k, row in enumerate(closed):
        moment = sum((const(count)*traces[abs(w)] for w, count in row.items()), zero)
        normalized = divided(moment, 33*D*SCALE**k)
        full = divided(const(359)+const(66)*normalized, 425)
        mixed = divided(const(293), 425) + divided(const(132), 425)*divided(one+normalized, 2)
        need(full == mixed, "full heat multiplicity vs binary mixture")
        seq.append(normalized)
        scaled_mark = scaled_mark + divided(BETA**k, factorial(k))*full
    # |33D-normalized trace moment|<=1 and beta<1: e^beta times
    # entire normalized heat differs by at most 3/(ORDER+1)!.
    error = F(3, factorial(ORDER+1))
    low, high = bounds(scaled_mark)
    sign_rows = {str(i): [str(t) for t in t2_diagonal[i].c] for i in (positive, negative)}
    return report, seq, (low-error, high+error), sign_rows


def trial(read, max_k, prefix_bits):
    """One complete literal geometric proposal with retained prefix/cap status."""
    k = 0
    while read():
        k += 1
        if k > max_k:
            return "length_timeout", k
    if k < 2:
        return "accept", k
    words = [0]*k
    for _ in range(prefix_bits):
        for i in range(k):
            words[i] = 2*words[i]+read()
        if len(set(words)) == k:
            return ("accept" if words == sorted(words) else "reject"), k
    return "sorting_timeout", k


def golden_clock():
    # The trial's read() records each consumed bit, including ties and failures.
    cases = (
        ([0], ("accept", 0)), ([1, 0], ("accept", 1)),
        ([1, 1, 0, 0, 1], ("accept", 2)),
        ([1, 1, 0, 1, 0], ("reject", 2)),
        ([1, 1, 0, 0, 0, 0, 0], ("sorting_timeout", 2)),
        ([1, 1, 1, 1], ("length_timeout", 4)),
    )
    for bits, target in cases:
        consumed = []
        def read():
            bit = bits[len(consumed)]
            consumed.append(bit)
            return bit
        need(trial(read, 3, 2) == target and consumed == bits, "golden transcript")
    # Exact finite prefix ranks for biased i.i.d. bits. Infinite streams tie
    # with probability zero since a fixed pair ties on b bits with rho^b, rho<1.
    prefixes = list(product(range(2), repeat=3))
    distinct, increasing = zero, zero
    for words in product(prefixes, repeat=3):
        if len(set(words)) != 3:
            continue
        term = p**(9+sum(sum(w) for w in words))
        distinct = distinct+term
        if tuple(sorted(words)) == words:
            increasing = increasing+term
    need(const(6)*increasing == distinct and distinct != zero, "biased iid rank")
    need(p+p**2 == one and p**2+p**4 == one-const(2)*p**3, "golden die")
    for k in range(13):
        need(sum((F(1, factorial(i)*factorial(k-i)) for i in range(k+1)), F(0))
             == F(2**k, factorial(k)), "convolution of the two accepted counts")
    # For each group L transactions until success, A=p exp(p²).
    # Analytic outward bounds using exact series and beta<1.
    small = p**2
    series = sum((divided(small**k, factorial(k)) for k in range(17)), zero)
    lo, hi = bounds(p*series)
    acceptance_interval = (lo, hi+F(3, factorial(17)))
    groups = (2/acceptance_interval[1], 2/acceptance_interval[0])
    return {"one_group_acceptance":"p exp(p^2)", "two_group_proposals_mean":decimal(groups, 13),
            "accepted_two_group_count":"Poisson(2p^2)", "explicit_transcript_cases":len(cases),
            "exchangeable_sort_test":"3 independent, nonuniform three-bit prefixes",
            "finite_service_control":"per group with R trials, length limit G and b prefix bits: (1-p exp(p^2))^R + R[(p^2)^(G+1) + p^2(p^2+p^4)^b] (union bound)"}


def tail_bound():
    # E[k 1_{k>c}]=beta P(Pois(beta)>=c); max_x 2/d_x=1/11.
    # |d ReTr(T^w)| <= |w| ||dT||_1, including negative powers, by
    # unitarity and the actual tangent on this fixed-dimensional clock.
    cap = 12
    lo, hi = bounds(BETA)
    need(0 < lo < hi < 1 and max(F(2, d) for d in ROWS) == F(1, 11),
         "genuine beta and worst scene degree")
    beta_up = F(764, 1000)
    need(hi < beta_up, "short rational beta majorant")
    # Bound e^-beta by 1; the ratios after the cap are <=beta/(cap+1).
    pois = beta_up**cap / (factorial(cap)*(1-beta_up/(cap+1)))
    source = F(66, 425*D)*beta_up/11*pois
    need(source < F(1, 10**12), "signed tail of marked source at cap 12")
    return {"omit":"k>Kcap; tail is replaced by a field-independent outcome law",
            "exact_source_majorant":"(66/(425 D)) (beta/11) Pr{Pois(beta)>=Kcap} ||dT||_1",
            "Kcap_example":cap,"upper_bound_for_D11_per_unit_trace_norm":str(source),
            "fixed_transcript_secants":"under common uniform U, E|1[U<x]-1[U<y]|=|x-y|; compare means before differentiating; field-independent service error must be o(actual secant step) after normalization"}


def main():
    closed = windings()
    compare_scene_polynomial(closed)
    a = word_values("G1;CX01", g["G1"], g["CX"], closed)
    b = word_values("CX01;G1", g["CX"], g["G1"], closed)
    ratio = (a[2][0]/b[2][1], a[2][1]/b[2][0])
    scene = sum((F(n, (35-n)**2) for n in SIZES), F())
    # E Tr(T^2) contrast is negative on the exact stored same-budget pair.
    need(a[1][2]-b[1][2] == const(-F(8, 33*D)*scene)*p**4,
         "signed second normalized scene-clock moment")
    need(0 < ratio[0] < ratio[1] < 1, "strict sign of full heat on swapped native calls")
    return {"schema":"d0.scene-winding-heat/1","status":"PASS","clock_dimension":D,
            "degrees":[33*D,392*D],"harmonic_background":359*D,
            "uniform_initial":"33 scene vertices and all D clock basis states",
            "checked_spatial_full_laurent_polynomials":ORDER+1,"scale_per_step":SCALE,
            "order_two_closed_prob_by_winding":{str(w):str(F(c,33*SCALE**2))
                                                   for w,c in sorted(closed[2].items()) if c},
            "full_binary_mixture":"293/425 sure acceptance + 132/425 signed-clock test",
            "full_heat_ratio_G1_CX_to_CX_G1":decimal(ratio, 18),
            "signed_diagonal_T2_indices_and_power_basis_1_a_a2_a3":
                    {a[0]["word"]:a[3], b[0]["word"]:b[3]},
            "native_count":golden_clock(),"derivative_tail":tail_bound(),
            "scope":"known finite word and normalized full heat; measuring an unknown clock, old-register access, and identification with full microscopic Cost-Info require their own physical transport",
            "original_cost_info_identified":False}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
