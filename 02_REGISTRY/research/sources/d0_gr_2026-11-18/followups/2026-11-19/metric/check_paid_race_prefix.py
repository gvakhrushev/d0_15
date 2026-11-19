"""Exact finite stopped signs, full recorded prefixes, and final work covariance."""
from itertools import product
import json

from check_golden_record_race import gold, need, p


class Poly(tuple):
    """Polynomial over Q(p) in the moving second-probe probability y."""
    def __new__(cls, coefficients):
        c = list(coefficients)
        while c and c[-1] == gold(0):
            c.pop()
        return tuple.__new__(cls, c)

    def __add__(self, other):
        rhs = polynomial(other)
        n = max(len(self), len(rhs))
        return Poly((self[i] if i < len(self) else gold(0)) +
                    (rhs[i] if i < len(rhs) else gold(0)) for i in range(n))

    __radd__ = __add__

    def __neg__(self):
        return Poly(-v for v in self)

    def __sub__(self, other):
        return self+(-polynomial(other))

    def __rsub__(self, other):
        return polynomial(other)+(-self)

    def __mul__(self, other):
        rhs = polynomial(other)
        if not self or not rhs:
            return Poly(())
        c = [gold(0)]*(len(self)+len(rhs)-1)
        for i, a in enumerate(self):
            for j, b in enumerate(rhs):
                c[i+j] = c[i+j]+a*b
        return Poly(c)

    __rmul__ = __mul__

    def at(self, y):
        v = gold(0)
        for x in reversed(self):
            v = v*y+x
        return v

    def deriv(self):
        return Poly(i*x for i,x in enumerate(self) if i)


def polynomial(value):
    return value if isinstance(value, Poly) else Poly((gold(value),))


ZERO, ONE = polynomial(0), polynomial(1)
Y = Poly((gold(0), gold(1)))
NATIVE = p**2
DZ = Y-NATIVE
BITS = tuple(product((0, 1), repeat=5))


def true_length(bits):
    return len(bits)+sum(bits)


def prob(bits):
    # Full five-bit leaf: first probe x, second probe d, guard, a raw fair-pair slot.
    x, d, gate, left, right = bits
    mass = p**true_length((x, gate, left, right))
    return (Y if d else ONE-Y)*mass


def permits(h, gate):
    if h is None:
        return gate == 0
    if h[0]:
        return True
    return gate == 1


def result(h, bits):
    x, d, gate, left, right = bits
    if not permits(h, gate):
        return "continue"
    if (left,right)==(0,1) and x==0:
        return "+"
    if (left,right)==(1,0) and x==0 and d==1:
        return "-"
    return "continue"


def prefix_fee(h):
    if h is None:
        return ZERO
    # Equals the actual paid prefix length at y=p². The old fee can move arbitrarily.
    return polynomial(true_length(h))+DZ*(3+sum(h))**2+DZ*DZ*(1+h[0])


def final_fee(bits):
    x, d, _, _, _ = bits
    # Common pre-orientation work of the probes, plus the actual guard and selector
    # length. At a successful slot either raw selector orientation costs exactly 3.
    return polynomial(true_length(bits))+5*DZ*int(x==0 and d==1)


def coefficients(f):
    return [g.strings() for g in f]


def main():
    probabilities = {bits:prob(bits) for bits in BITS}
    need(sum(probabilities.values(), ZERO)==ONE, "all raw outcomes at every round")
    for bits, mass in probabilities.items():
        need(mass.at(NATIVE)==p**true_length(bits), "actual canonical golden cylinder")
    history_mass = {None:ONE}
    for row, mass in probabilities.items():
        if result(None,row)=="continue":
            history_mass[row] = mass
    signs = ("+", "-")
    accepted = {s:ZERO for s in signs}
    past = {s:ZERO for s in signs}
    current = {s:ZERO for s in signs}
    true_work = {s:ZERO for s in signs}
    selector_fee = {s:ZERO for s in signs}
    terminal_hist = {}
    native_entropy_rows = []
    timeout = ZERO
    a, b = polynomial(p), Y*p
    two_probe_expected = (ONE-Y)*(ONE+5*DZ)
    hazards = set()
    for h, incoming in history_mass.items():
        # Measure the two tests before consulting either selector orientation, even on losses.
        # A={x=0}, B={x=0,d=1}; these actually executed events overlap fully on B.
        local = {s:ZERO for s in signs}
        local_current = {s:ZERO for s in signs}
        guard_prob = sum((p**(1+g) for g in (0,1) if permits(h,g)), gold(0))
        eligible = polynomial(guard_prob*p**3)
        common_w = common_a = common_b = ZERO
        for bits, mass in probabilities.items():
            x,d,gate,left,right = bits
            s = result(h, bits)
            if s == "continue":
                if h is not None:
                    timeout += incoming*mass
            else:
                local[s] += mass
                local_current[s] += mass*final_fee(bits)
                leaf = incoming*mass
                true_work[s] += leaf*(true_length(bits)+(true_length(h) if h else 0))
                selector_fee[s] += leaf*int((left,right)==(0,1))
                native_entropy_rows.append((h,s,bits,incoming.at(NATIVE)*mass.at(NATIVE)))
            # Use one concrete eligible orientation to integrate the common W law;
            # both orientations have the same length and the two G probes are independent of it.
            if permits(h,gate) and (left,right)==(0,1):
                w = mass*final_fee(bits)
                common_w += w
                if x==0:
                    common_a += w
                    if d:
                        common_b += w
        need(local["+"]==eligible*a and local["-"]==eligible*b, "constant conditional sign odds")
        terminal_hist[h] = {s:incoming*local[s] for s in signs}
        hazards.add(tuple((local["+"]+local["-"]).at(NATIVE).strings()))
        for s in signs:
            accepted[s] += terminal_hist[h][s]
            past[s] += terminal_hist[h][s]*prefix_fee(h)
            current[s] += incoming*local_current[s]
        # Cov(W,B)/b−Cov(W,A)/a, conditional on the common eligible slot:
        # common_w, common_a, common_b are unnormalized by the same eligible mass.
        cov_a = common_a-a*common_w
        cov_b = common_b-b*common_w
        need(local_current["+"]==common_a and local_current["-"]==common_b,
             "paid successful final means use the common W")
        need(a*cov_b-b*cov_a==eligible*a*b*two_probe_expected, "final covariance contrast")
    plus, minus = accepted["+"], accepted["-"]
    need(len(hazards)==3, "three different actual finishing hazards")
    need(plus+minus+timeout==ONE and timeout.at(NATIVE)!=gold(0), "complete finite mass")
    need(minus==Y*plus, "moving final odds")
    for term in terminal_hist.values():
        need(term["-"]==Y*term["+"], "identical conditional past law at every field value")
    need(past["-"]*plus==past["+"]*minus, "arbitrary moving past charge cancels identically")
    total = {s:past[s]+current[s] for s in signs}
    need(total["-"]*plus-total["+"]*minus==plus*minus*two_probe_expected,
         "complete moving-price contrast equals just the final covariance")
    need(current["-"]*plus-current["+"]*minus==plus*minus*two_probe_expected,
         "counterexample to discarding the final work covariance")
    need(two_probe_expected.at(NATIVE)==p and two_probe_expected.deriv().at(NATIVE)==5*p-1
         and two_probe_expected.deriv().deriv().at(NATIVE)==gold(-10),
         "first two true jets of the declared price continuation")
    # Conditional entropy chain rule certificate at native point:
    # proportional prefixes at all fields; exact product factorization on every complete cell.
    for h,s,bits,leaf_mass in native_entropy_rows:
        _,d,gate,_,_ = bits
        total_s = accepted[s].at(NATIVE)
        hist = terminal_hist[h][s].at(NATIVE)
        guard = sum((p**(1+g) for g in (0,1) if permits(h,g)), gold(0))
        # Once minus is selected both probes are fixed. Given plus, the second
        # probe still has its original law. The eligible guard has its own posterior.
        tested_probes = (p**(1+d) if s == "+" else gold(1))
        fresh_record = tested_probes*p**(1+gate)/guard
        need(leaf_mass/total_s == (hist/total_s)*fresh_record,
             "independent factorization of every entropy cell")
    native_contrast = true_work["-"].at(NATIVE)/minus.at(NATIVE)-true_work["+"].at(NATIVE)/plus.at(NATIVE)
    need(native_contrast==p and minus.at(NATIVE)/plus.at(NATIVE)==p**2,
         "conditional full entropy difference/log(phi) = p−2 on paid cylinders")
    # Independent sign and tests do not imply sign-neutral work if the controller
    # is charged asymmetrically. This artificial added fee is exactly 1 on successful +.
    need(selector_fee["+"]==plus and selector_fee["-"]==ZERO,
         "selector-dependent work adds minus one to the minus-vs-plus contrast")
    out = dict(status="PASS", basis="1,p; p²=1−p; field is y=Pr(second probe=1)",
               actual_raw_bits_per_round=5, maximum_rounds=2, completed_prefixes=len(terminal_hist),
               native_hazards_sorted_power_basis=sorted(hazards),
               golden_terminal_plus_minus_timeout=[s.at(NATIVE).strings() for s in (plus,minus,timeout)],
               terminal_sign_odds_minus_over_plus="y",
               prefix_law_and_old_price_identical="polynomial identities, hence all jets at 0<y<1",
               complete_current_contrast_polynomial_ascending=coefficients(two_probe_expected),
               native_completed_canonical_work_minus_plus=native_contrast.strings(),
               declared_moving_work_jets_native=[f.at(NATIVE).strings() for f in
                   (two_probe_expected,two_probe_expected.deriv(),two_probe_expected.deriv().deriv())],
               entropy_chain_rule_checked_positive_terminal_cells=len(native_entropy_rows),
               native_conditional_entropy_minus_plus_in_golden_units=(p-2).strings(),
               native_net_work_minus_entropy_diff_in_golden_units=2,
               selector_orientation_extra_fee_example_delta="-1",
               scope="canonical five-bit golden cylinders at y=p²; variable y and added price jets are declared comparisons; H.1 microscopic work not identified")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
