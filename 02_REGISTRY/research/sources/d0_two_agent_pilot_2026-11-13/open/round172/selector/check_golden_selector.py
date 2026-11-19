"""Exact adaptive Golden selectors, optimal interval order, and a depth-25 certificate."""

from fractions import Fraction
from hashlib import sha256
from math import ceil, comb, floor, isqrt
from pathlib import Path
import json
import subprocess


ROOT = Path(__file__).resolve().parents[7]
PRIMARY = (
    "02_REGISTRY/research/sources/d0_gr_2026-11-18/"
    "followups/2026-11-19/metric/"
)
ALLOCATIONS = (5644800, 4939200, 4390400, 3087000, 1580544, 548800, 115200, 11025)
EARLY = {
    "00": 0,
    "01000001": 1, "0100001": 1, "010001": 1, "01001": 1,
    "0101": 1, "011000": 1, "0110010": 1, "01100110": 1,
    "0111": 2, "1000": 2,
    "10010001": 3, "1001001": 3, "100101": 3, "10011": 3,
    "1010": 3, "101100": 3, "1011010": 3, "10110110": 3,
    "1100": 4, "11010": 4, "1110": 5,
}
RESIDUAL = (
    {7:5033, 9:18540, 12:17, 13:1683, 15:210284, 17:233573},
    {7:22014, 9:6, 10:63293, 11:43522, 12:563058, 13:346591,
     19:80813, 21:8599, 23:252},
    {12:96577, 13:528403, 17:143912, 19:12365},
    {1:1, 10:32376, 11:405849, 15:394094},
    {2:18, 8:27585, 10:170821, 11:50, 15:246944},
    {4:839, 6:10316, 8:36234, 9:97250, 11:24, 12:23, 15:55,
     17:32599, 18:2248, 21:9},
    {5:3312, 9:21139, 13:251, 17:5923},
    {7:125, 11:10167, 12:2, 25:1},
)
ZERO, ONE, P, PHI = (0, 0), (1, 0), (0, 1), (1, 1)


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def add(x, y):
    return x[0]+y[0], x[1]+y[1]


def scale(x, n):
    return x[0]*n, x[1]*n


def subtract(x, y):
    return add(x, scale(y, -1))


def multiply(x, y):
    a, b = x
    c, d = y
    return a*c+b*d, a*d+b*c-b*d


def power(x, n):
    value = ONE
    for _ in range(n):
        value = multiply(value, x)
    return value


def total(values):
    value = ZERO
    for element in values:
        value = add(value, element)
    return value


def sign(x):
    a, b = 2*x[0]-x[1], x[1]
    sa, sb = (a>0)-(a<0), (b>0)-(b<0)
    if sa == sb or not sa or not sb:
        return sa or sb
    difference = a*a-5*b*b
    return sa*((difference>0)-(difference<0))


def enclosure(x, digits=12):
    resolution = 10**80
    low = Fraction(isqrt(5*resolution**2)-resolution, 2*resolution)
    high = low+Fraction(1, 2*resolution)
    endpoints = [x[0]+x[1]*bound for bound in (low, high)]
    denominator = 10**digits
    scaled = [floor(min(endpoints)*denominator), ceil(max(endpoints)*denominator)]

    def decimal(value):
        integer, fractional = divmod(value, denominator)
        return f"{integer}.{fractional:0{digits}d}"

    return [decimal(value) for value in scaled]


def cost(word):
    return len(word)+word.count("1")


def complete_stats(expected, depths, costs):
    h_g = add(ONE, power(P, 2))
    return {
        "raw_leaf_count": sum(depths.values()),
        "raw_leaf_count_by_reads": depths,
        "minimum_birth_reads": min(depths),
        "maximum_birth_reads": max(depths),
        "minimum_Golden_cost": min(costs),
        "maximum_Golden_cost": max(costs),
        "expected_birth_reads_Qp": expected,
        "expected_birth_reads_interval": enclosure(expected),
        "expected_LC1_births_with_one_tail_per_read_interval": enclosure(scale(expected, 2)),
        "expected_Golden_tape_cost_interval": enclosure(multiply(expected, h_g)),
    }


def path(threshold):
    current = threshold
    word, internal = "", []
    while current not in (ZERO, ONE):
        require(len(word)<200, "exact Golden threshold did not terminate")
        internal.append(word)
        if sign(subtract(current,P)) < 0:
            current = multiply(current,PHI)
            word += "0"
        else:
            current = multiply(subtract(current,P),power(PHI,2))
            word += "1"
    return frozenset(internal)


def interval_selectors(masses):
    full = (1<<len(masses))-1
    subset_mass = [ZERO]
    for mask in range(1, full+1):
        bit = mask & -mask
        subset_mass.append(add(subset_mass[mask^bit],masses[bit.bit_length()-1]))
    require(subset_mass[full] == ONE, "wrong total address mass")
    paths = [path(mass) for mass in subset_mass]
    depths = [len(words) for words in paths]
    maximum = max(depths)
    powers = [power(P,k) for k in range(2*maximum+2)]

    best_depth = [0]*(full+1)
    for mask in range(1, full+1):
        best_depth[mask] = max(
            depths[mask], min(best_depth[mask^(1<<j)] for j in range(len(masses))
                              if mask & (1<<j)),
        )
    require(best_depth[full] == 49 and maximum == 58, "interval depth bound changed")

    def cheapest(cap):
        best = [(ZERO, ())] + [None]*full
        for mask in range(1,full+1):
            if depths[mask] > cap:
                continue
            for j in range(len(masses)):
                bit = 1<<j
                if not mask & bit or best[mask^bit] is None:
                    continue
                before = mask^bit
                increment = total(powers[cost(s)] for s in paths[mask]-paths[before])
                prior, order = best[before]
                candidate = add(prior,increment)
                if best[mask] is None or sign(subtract(candidate,best[mask][0])) < 0:
                    best[mask] = (candidate,order+(j,))
        return best[full]

    def assess(order, minimum=None):
        cuts, internal = [ZERO], set()
        mask = 0
        for j in order:
            mask |= 1<<j
            cuts.append(subset_mass[mask])
            internal.update(paths[mask])
        received = [ZERO]*len(masses)
        leaf_depths, leaf_costs = {}, set()
        stack = [("",ZERO,ONE)]
        while stack:
            word, lower, mass = stack.pop()
            if word in internal:
                left = multiply(mass,P)
                stack.append((word+"0",lower,left))
                stack.append((word+"1",add(lower,left),multiply(mass,powers[2])))
                continue
            upper = add(lower,mass)
            labels = [j for k,j in enumerate(order)
                      if sign(subtract(lower,cuts[k]))>=0
                      and sign(subtract(cuts[k+1],upper))>=0]
            require(len(labels)==1, "a stopped cylinder crosses a colour boundary")
            j = labels[0]
            received[j] = add(received[j],mass)
            leaf_depths[len(word)] = leaf_depths.get(len(word),0)+1
            leaf_costs.add(cost(word))
        require(received==list(masses), "interval colour law changed")
        require(sum(leaf_depths.values())==len(internal)+1, "interval tree support lost a leaf")
        expected = total(powers[cost(word)] for word in internal)
        if minimum is not None:
            require(expected==minimum, "adjacent-boundary shortcut missed a prefix")
        return dict(complete_stats(expected,leaf_depths,leaf_costs), order=order)

    expected, order = cheapest(maximum)
    capped_expected, capped_order = cheapest(best_depth[full])
    return {
        "subset_boundaries_tested": len(paths),
        "minimum_possible_maximum_reads": best_depth[full],
        "largest_maximum_reads_over_orders": maximum,
        "original_colour_order": assess((1,2,3,4,5,6,7,8,0)),
        "best_expected_at_minimum_maximum_depth": assess(capped_order,capped_expected),
        "best_expected_over_all_orders": assess(order,expected),
    }


def choose(n, k):
    return comb(n,k) if 0<=k<=n else 0


def hybrid(masses):
    d = 25
    for word in EARLY:
        require(not any(word[:k] in EARLY for k in range(len(word))),
                "an early stop is a descendant of another early stop")

    def capacity(prefix, ones):
        if any(prefix[:k] in EARLY for k in range(len(prefix)+1)):
            return 0
        all_words = choose(d-len(prefix),ones-prefix.count("1"))
        early_words = sum(choose(d-len(word),ones-word.count("1"))
                          for word in EARLY if word.startswith(prefix))
        return all_words-early_words

    available = [capacity("",k) for k in range(d+1)]
    reject = tuple(available[k]-sum(row.get(k,0) for row in RESIDUAL) for k in range(d+1))
    require(min(reject)>=0, "weight bucket capacity was overallocated")
    rows = ({k:v for k,v in enumerate(reject) if v},)+RESIDUAL
    result = [
        add(total(power(P,cost(word)) for word,label in EARLY.items() if label==j),
            total(scale(power(P,d+k),v) for k,v in row.items()))
        for j,row in enumerate(rows)
    ]
    require(result==list(masses), "hybrid selector altered true address masses")

    def unrank(rank, ones):
        prefix = ""
        while len(prefix)<d:
            left = capacity(prefix+"0",ones)
            if rank<left:
                prefix += "0"
            else:
                prefix += "1"
                rank -= left
        require(rank==0 and capacity(prefix,ones)==1, "unranking hit a stopped prefix")
        return prefix

    def rank(word, ones):
        require(capacity(word,ones)==1, "cannot rank a stopped prefix")
        return sum(capacity(word[:k]+"0",ones) for k,bit in enumerate(word) if bit=="1")

    def dispatch(read_symbol):
        word = ""
        while len(word)<d:
            bit = read_symbol()
            require(bit in ("0", "1"), "not a registered Golden digit")
            word += bit
            if word in EARLY:
                return word, EARLY[word]
        ones = word.count("1")
        remaining = rank(word,ones)
        for label, row in enumerate(rows):
            count = row.get(ones,0)
            if remaining<count:
                return word, label
            remaining -= count
        raise ArithmeticError("residual word escaped all labels")

    for word, label in EARLY.items():
        recorded = iter(word)
        require(dispatch(lambda: next(recorded))==(word,label),
                "early dispatch read beyond the real prefix")

    boundary_checks = 0
    for ones, size in enumerate(available):
        offset = 0
        for label, row in enumerate(rows):
            count = row.get(ones,0)
            if count:
                for k in (offset,offset+count-1):
                    word = unrank(k,ones)
                    require(rank(word,ones)==k, "residual rank interval mismatch")
                    recorder = iter(word)
                    require(dispatch(lambda: next(recorder))==(word,label),
                            "wrong recorded residual route")
                    boundary_checks += 1
            offset += count
        require(offset==size, "residual rank intervals did not exhaust a bucket")

    conjugate_total_variation = subtract(scale(power(PHI,36),2*sum(ALLOCATIONS)),ONE)
    require(sign(subtract(conjugate_total_variation,power(PHI,3*(d-1))))>0,
            "depth-24 impossibility lost its strict margin")

    depth_counts, costs = {d:sum(available)}, {d+k for k,num in enumerate(available) if num}
    for word in EARLY:
        depth_counts[len(word)] = depth_counts.get(len(word),0)+1
        costs.add(cost(word))
    expected = subtract((d,0),
                        total(scale(power(P,cost(word)),d-len(word)) for word in EARLY))
    terminal_cap_mass = total(scale(power(P,d+k),num) for k,num in enumerate(available))
    return dict(complete_stats(expected,depth_counts,costs),
                early_stopped_leaves=len(EARLY), rank_boundary_checks=boundary_checks,
                probability_of_reaching_cap_interval=enclosure(terminal_cap_mass),
                universal_minimum_maximum_reads=d)


def counterfactual():
    variable = [ZERO]
    for k in range(1,37):
        shorter = variable[k-2] if k>=2 else ZERO
        variable.append(add(ONE,add(multiply(P,variable[k-1]),
                                    multiply(power(P,2),shorter))))
    hits, overshoots = 1, 1
    for _ in range(35):
        hits, overshoots = hits+overshoots, hits
    require((hits,overshoots)==(24157817,14930352), "wrong cost-cut prefix counts")
    h_g = add(ONE,power(P,2))
    expected_cost = multiply(variable[36],h_g)
    require(expected_cost==add((36,0),scale(power(P,37),overshoots)),
            "wrong expected cost of first hit or overshoot")
    return {
        "original_cost_cut_36": {
            "maximum_reads": 36,
            "positive_raw_leaves": hits+overshoots,
            "expected_reads_interval": enclosure(variable[36]),
            "expected_Golden_tape_cost_interval": enclosure(expected_cost),
        },
        "mandatory_36_reads": {
            "reads": 36,
            "positive_raw_leaves": 2**36,
            "LC1_births_with_tails": 72,
            "expected_Golden_tape_cost_interval": enclosure(scale(h_g,36)),
        },
    }


def check_source_pins():
    pins = (
        ("a03c0e1f0", "SELECTOR36_NATIVE_RU.md",
         "e25530b6968a72740a9765584f3b93b23ca6f9c84897ca0ba81df3331621768d"),
        ("04931a7a26a9741bba0584c8e1413613ff7a28d5", "EIGHT_READERS_RU.md",
         "e6cf63011b94a10068d9545eb901c6f17c22024693d9ea21bc874dcd7f86fb0e"),
    )
    for revision,name,expected in pins:
        raw = subprocess.check_output(
            ["git","show",f"{revision}:{PRIMARY}{name}"], cwd=ROOT,
        )
        require(sha256(raw).hexdigest()==expected, name)
    return len(pins)


def main():
    active = tuple(scale(power(P,36),count) for count in ALLOCATIONS)
    masses = (subtract(ONE,total(active)),)+active
    result = {
        "source_pins": check_source_pins(),
        "address_probabilities_by_index_interval": [enclosure(mass) for mass in masses],
        "contiguous_intervals": interval_selectors(masses),
        "hybrid": hybrid(masses),
        "counterfactual": counterfactual(),
        "same_nine_address_probabilities": True,
        "same_raw_archive_or_clock_proved": False,
        "classical_dispatch_physical_tariff_proved": False,
        "GR_closed": False,
        "status": "PASS",
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
