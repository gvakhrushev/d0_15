"""Checks for the one-report H.1 code minimum. Standard library, Python 3.9+."""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from math import comb, log
from typing import NamedTuple


PHI_LO = Q(1618033, 1000000)
PHI_HI = Q(1618034, 1000000)
F, R = "0", "10"


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def golden_prefix_trees(leaves):
    if leaves == 1:
        return [("",)]
    trees = []
    for left_count in range(1, leaves):
        for left in golden_prefix_trees(left_count):
            for right in golden_prefix_trees(leaves-left_count):
                trees.append(tuple(F+s for s in left)+tuple(R+s for s in right))
    return trees


def valid(words):
    return all(not b.startswith(a) for a, b in permutations(words, 2))


def gamma_report(m, b):
    """Known decoder reads a self-delimiting positive count, then a branch."""
    digits = bin(m)[2:]
    bits = "0"*(len(digits)-1)+digits+str(b)
    return "".join((F,R)[int(bit)] for bit in bits)


def read_report(word):
    pos = 0

    def bit():
        nonlocal pos
        if pos < len(word) and word[pos] == "0":
            pos += 1
            return 0
        if word.startswith("10", pos):
            pos += 2
            return 1
        raise ValueError("Truncated or invalid Golden token")

    zeros = 0
    while bit() == 0:
        zeros += 1
    count = 1
    for _ in range(zeros):
        count = 2*count+bit()
    report = bit()
    check(pos == len(word), "extra payload")
    return count, report


def minimum_tests():
    weights = [840*Q((-1)**(j-1)*comb(8,j), j) for j in range(1,9)]
    bound = 2*sum(abs(w) for w in weights)
    check(bound == 126506, "eight-scale flag bound")
    check(PHI_LO**2-PHI_LO < 1 < PHI_HI**2-PHI_HI, "enclose phi")
    k = 2**20
    lo, hi = Q(3,4)-bound/k, Q(3,4)+bound/k
    check(lo/(1-lo)> PHI_HI and hi<1, "twenty-bit entropy gap over one")
    check((2/PHI_LO**3)**20<Q(1,2), "actual address success below one half")
    trees = golden_prefix_trees(3)
    profiles = {tuple(sorted(map(len,words))) for words in trees}
    check(profiles == {(1,3,4),(2,2,3)}, "all three-leaf profiles")
    check((F,R+F,R+R) in trees and all(valid(t) for t in trees), "explicit code")

    # Independent exact envelope values at interior and outer probabilities.
    for lam, u in product((Q(1,10**7),Q(1,4),Q(499,1000)),(lo,Q(3,4),hi)):
        probs = (1-lam,lam*u,lam*(1-u))
        expected = min(sum(a*len(b) for a,b in zip(probs,codes))
                       for tree in trees for codes in permutations(tree))
        check(expected == 1+3*lam-lam*u,"optimal ternary expected wire length")
        check(2+lam*(1-u)-expected == 1-2*lam,"competing tree gap")

    k = 2**23
    lo, hi = Q(3,4)-bound/k, Q(3,4)+bound/k
    check((lo/(1-lo))**10 > PHI_HI**21, "lower log odds exceeds 21/10")
    check((hi/(1-hi))**2 < PHI_LO**5, "upper log odds below 5/2")
    return float(lo),float(hi)


def repeat_test():
    words = []
    for m in range(1,257):
        for b in (0,1):
            word = gamma_report(m,b)
            words.append(word)
            check(read_report(word) == (m,b),"self-delimiting repetition block")
            check(len(word) <= 4*(m.bit_length()-1)+4,"compact code for semantic output")
        check(len(gamma_report(m,1))-len(gamma_report(m,0)) == 1, "report delta")
    check(valid(words), "joint prefix condition")
    check(len(gamma_report(2**30,1)) < 128, "explicit large-block witness")


def parity_test():
    lo, hi = Q(7,10), Q(4,5)
    for n in range(2,8):
        words = list(product((0,1),repeat=n))
        even = {w for w in words if sum(w)%2 == 0}
        delta = {w: ((lo-hi) if w in even else (hi-lo))/2**(n-1)
                 for w in words}
        for size in range(n):
            for coords in combinations(range(n),size):
                marginals = {}
                for w in words:
                    cell = tuple(w[i] for i in coords)
                    marginals[cell] = marginals.get(cell,0)+delta[w]
                check(all(v==0 for v in marginals.values()),"all proper marginals fixed")
        arbitrary = {w: Q(sum((j+1)*(i+2)*b for i,b in enumerate(w)),13)
                     + Q(5,7)*(w not in even) for j,w in enumerate(words)}
        walsh = (sum(arbitrary[w] for w in words if w not in even)
                 - sum(arbitrary[w] for w in even))/2**(n-1)
        check(sum(delta[w]*arbitrary[w] for w in words) == (hi-lo)*walsh,
              "only full parity price remains")
        def final_cost(word):
            memory = 0
            for bit in word:
                memory ^= bit
            return memory
        check(sum(delta[w]*final_cost(w) for w in words) == hi-lo,
              "one memory bit plus a final paid write sees all reports")


class Line(NamedTuple):
    intercept: Q
    slope: Q


def adaptive_example():
    # A field-blind factory with public abort of weight 3/7, two success types.
    abort, s, t = Q(3,7), Q(1,7), Q(3,7)
    gain = s+t
    candidates = [(1,2,4,1,2),(1,4,1,3,1),(2,0,3,0,1),(1,4,3,1,1)]
    lines = set()
    for fail, s0, s1, t0, t1 in candidates:
        lines.add(Line(abort*fail+s*s0+t*t0, s*(s1-s0)+t*(t1-t0)))
    cuts = {(b.intercept-a.intercept)/(a.slope-b.slope)
            for a,b in permutations(lines,2) if a.slope != b.slope}
    check(Q(3,4) in cuts, "default bias really has a candidate crossing")
    left, right = Q(76,100),Q(77,100)
    for cut in cuts:
        check(not left<=cut<=right, "no affine crossing on example interval")
    check(min(lines,key=lambda l:l.intercept+left*l.slope)
          == min(lines,key=lambda l:l.intercept+right*l.slope),"one minimizing line")
    for line in lines:
        exponent = -line.slope/gain
        a, b = exponent.numerator, exponent.denominator
        check((left/(1-left))**b > max(PHI_HI**a, PHI_LO**a)
              or (right/(1-right))**b < min(PHI_HI**a, PHI_LO**a),
              "no entropy cancellation for any candidate")

    # A lexicographic cut for n independent *unconditioned* Golden bits can be
    # found without storing 2**n words. Squared probabilities exploit p+p^2=1.
    # Rational interval for p certifies the mass bracket of the selected cut.
    n, m = 18, 16
    p_lo,p_hi = 1/PHI_HI,1/PHI_LO
    # Binary lexical rank j. Split fractions p and 1-p; interval evaluation
    # uses the first differing bit in the disjoint lexical cylinders below j.
    def cut_mass(j):
        prefix = successes = 0
        low = high = Q(0)
        for pos in range(n-1,-1,-1):
            digit = (j >> pos)&1
            if digit:
                low += p_lo**(prefix+1)*(1-p_hi)**successes
                high += p_hi**(prefix+1)*(1-p_lo)**successes
                successes += 1
            else:
                prefix += 1
        return low, high

    target = Q(153,200)
    a,b = 0,2**n-1
    while a+1<b:
        mid = (a+b)//2
        if cut_mass(mid)[1] < target:
            a=mid
        else:
            b=mid
    rlo,rhi = cut_mass(a)
    check(rlo <= rhi < target and rlo > target-Q(1,200),"internal cut")
    # P = (1-p^m)r + p^m q, q in [0,1] including all old H.1 reports.
    wmax = p_hi**m
    check(left < (1-wmax)*rlo and rhi+wmax*(1-rhi)<right,"whole-chart interval")
    return a,n,m


def rare_report_test():
    phi = (1+5**0.5)/2
    p = 1/phi
    gamma = Q(4,7)
    # At ordinary probabilities and near one these fixed implementations win
    # on different branches. Add truly dominated exceptional two-branch prices.
    costs = [(4,2),(7,1),(1,6),(8,8),(20,2),(5,7)]
    frontier = [c for c in costs if not any(a<=c[0] and b<=c[1] and (a,b)!=c
                                          for a,b in costs)]
    check(sorted(frontier) == [(1,6),(4,2),(7,1)], "integer Pareto minima")
    # Exact cost comparison in the rare-failure region including both endpoints.
    for u in (Q(9,10),Q(99,100),Q(99999,100000)):
        check(min(costs,key=lambda c:(1-u)*c[0]+u*c[1]) == (7,1), "stable winner")
    for u in (0.63,0.75,0.87):
        for m in (16,40,100,200):
            failure = p**m*(1-u)
            # Work with the failure directly, including when 1-failure rounds to 1.
            score = (log(1-failure)-log(failure))/log(phi)
            check(abs(score-(m-log(1-u,phi)+log(1-failure,phi))) < 1e-10,
                  "exact rare-report log odds formula")
            normalized = float(gamma)*(score-6)/m
            check(normalized>0 and abs(normalized-float(gamma))<4/m,
                  "positive full minimized information source")


if __name__ == "__main__":
    low,high = minimum_tests()
    repeat_test()
    parity_test()
    rare_report_test()
    cut,nbits,trigger = adaptive_example()
    print("PASS: exact three-leaf minimum, full-range integer separation, semantic repetition code")
    print(f"23-bit probabilities in [{low:.8f}, {high:.8f}], absolute multiplier > 0.1")
    print(f"Finite-factory example: {nbits} unobserved Golden bits, cut rank {cut}, trigger depth {trigger}")
    print("PASS: parity-price identity, every proper output marginal, two-state counterexample")
    print("PASS: fixed minimum under a rare Golden trigger and normalized entropy slope")
