"""Record count and race with paid golden decisions. Standard library, deterministic."""
from collections import Counter
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial
from typing import NamedTuple
import json


def need(condition, label):
    if not condition:
        raise ArithmeticError(label)


class Gold(NamedTuple):
    a: F
    b: F

    def __add__(self, other):
        other = gold(other)
        return Gold(self.a+other.a, self.b+other.b)

    __radd__ = __add__

    def __neg__(self):
        return Gold(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-gold(other))

    def __rsub__(self, other):
        return gold(other) + (-self)

    def __mul__(self, other):
        other = gold(other)
        bd = self.b*other.b
        return Gold(self.a*other.a+bd, self.a*other.b+self.b*other.a-bd)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a*self.a-self.a*self.b-self.b*self.b
        return Gold((self.a-self.b)/norm, -self.b/norm)

    def __truediv__(self, other):
        return self*gold(other).inverse()

    def __pow__(self, n):
        value = gold(1)
        for _ in range(n):
            value *= self
        return value

    def strings(self):
        return [str(self.a), str(self.b)]


def gold(x):
    return x if isinstance(x, Gold) else Gold(F(x), F(0))


p = Gold(F(0), F(1))
beta = 2*p**2
need(p+p**2 == gold(1) and 1-beta == p**3, "golden calibration")


def records(perm):
    high, count = -1, 0
    for x in perm:
        if x > high:
            high, count = x, count+1
    return count


def record_polynomials():
    # Enumerating all strict orders is exact for independent atomless keys.
    coefficients = [1]
    rows = []
    for n in range(9):
        observed = Counter(records(pi) for pi in permutations(range(n)))
        need(coefficients == [observed[k] for k in range(n+1)], "record PGF numerator")
        need(sum(coefficients) == factorial(n), "permutations")
        # Independent thinning: evaluate survival of all records and two PGF probes
        # both from the binomial outcome law and from the rising-factorial identity.
        for u in (gold(0), gold(F(1, 3)), gold(1)):
            direct = gold(0)
            for k, count in observed.items():
                for j in range(k+1):
                    direct += count*comb(k,j)*beta**j*(1-beta)**(k-j)*u**j
            thinned = 1-beta+beta*u
            rising = gold(1)
            for j in range(n):
                rising *= thinned+j
            need(direct == rising, "thinning actual beta")
        rows.append(coefficients)
        nxt = [0]*(n+2)
        for k,c in enumerate(coefficients):
            nxt[k] += n*c
            nxt[k+1] += c
        coefficients = nxt
    return rows


def parse_closed_race(bits):
    # Every primitive is a golden binary birth/read. Equal selector pairs,
    # failed races and the final accepted attempt are all charged and retained.
    offset = equal_pairs = failed = 0
    while offset < len(bits):
        while True:
            pair = bits[offset:offset+2]
            need(len(pair)==2, "complete fair selector")
            offset += 2
            if pair in ("01", "10"):
                break
            equal_pairs += 1
        need(offset < len(bits), "missing terminal probe")
        bit = bits[offset]
        offset += 1
        sign = "+" if pair == "01" else "-"
        if (sign,bit) in (("+","0"),("-","1")):
            need(offset == len(bits), "non-prefix-free test word")
            return {"bits":bits,"sign":sign,"equal_pair_rejections":equal_pairs,
                    "losing_rounds":failed,"paid_golden_length":len(bits)+bits.count("1")}
        failed += 1
    raise ArithmeticError("stopping rule unfinished")


def closed_golden_witness():
    # The first unequal pair is equally likely to be 01 or 10. Both pay
    # length 3. Its rejected initial pairs are independent of its orientation.
    eq = p**2+p**4
    fair_length = 2*(1+p**2)/(1-eq)
    fair_orientation = p**3/(1-eq)
    need(fair_orientation == gold(F(1, 2)), "fair selector with all rejected pairs")
    # Expected cost via a separate recursion on the first pair.
    reconstructed = p**2*(2+fair_length)+p**4*(4+fair_length)+2*p**3*3
    need(reconstructed == fair_length, "selector's real length")
    u,v = fair_orientation*p, fair_orientation*p**2
    fail = 1-u-v
    need(fail == gold(F(1,2)) and u/(1-fail) == p and v/(1-fail) == p**2,
         "race's exact terminal marks")
    examples = [parse_closed_race(x) for x in ("010","101","00"+"01"+"1"+"11"+"10"+"1",
                                                "11"+"10"+"0"+"00"+"01"+"0")]
    for record in examples:
        mass = gold(1)
        for b in record["bits"]:
            mass *= p if b == "0" else p**2
        need(mass == p**record["paid_golden_length"], "true paid cylinder")
    # In units of log(phi), the entropy left given the sign of one fair
    # selector is L_f - log(2)/ell. Derive it independently from the random
    # rejection words: their unconditioned weights times final 2*p^3.
    rejected_cost = (2*p**2+4*p**4)/(1-eq)
    need(rejected_cost+3 == fair_length, "conditional fair rejection entropy")
    # Given the ultimate sign, the geometric number of failed rounds has mean
    # 1 and entropy 2 log 2. In each failed round the orientation has weights
    # (p^2,p) and entropy (1+p^2)*ell. Track coefficients of log(2)/ell
    # separately to check cancellation rather than assume the desired identity.
    fail_mean = fail/(1-fail)
    h_fail_orientation = 2*p**2+p
    h_cond = (fail_mean+1)*(rejected_cost+3)+fail_mean*h_fail_orientation
    log2_coeff = 2-(1+fail_mean)
    need(log2_coeff == gold(0), "all conditional log2 terms retained")
    conditional_costs = []
    for final_length in (1,2):
        expected_cost = fail_mean*(fair_length+1+p**2)+fair_length+final_length
        need(expected_cost-h_cond == gold(final_length), "complete conditional price/entropy")
        conditional_costs.append(expected_cost.strings())
    return {"plus_probability":"p","minus_probability":"p^2","examples":examples,
            "basis":"1,p","fair_selector_mean_paid_length":fair_length.strings(),
            "conditional_mean_paid_length_plus_minus":conditional_costs,
            "conditional_entropy_over_log_phi_both_signs":h_cond.strings(),
            "conditional_net_golden_units_plus_minus":[1,2],
            "scope":"fully golden deterministic witness; its two test coins differ from the H.1 heat and determinant oracles"}


def field_bounds():
    # beta in (0,1); on Spin4, d=h_D^beta >= (1-z)^4. This lower bound
    # is rational, uniform in the actual cold corner and does not require knowing heat.
    r, z = 4, F(1,2**20)
    heat_min, d_min = F(359,425), (1-z)**r
    plus_min, minus_min = heat_min/(1+heat_min), d_min/(1+d_min)
    per_round = (heat_min+d_min)/2
    need(plus_min > F(45,100) and minus_min > F(49,100) and per_round > F(92,100),
         "uniform sign and stopping bounds")
    # For the variance use log(425/359)=2 atanh(33/392) and
    # -log(1-z) <= z/(1-z). Thus no transcendental numerical bound is needed.
    x=F(33,392)
    var_upper=2*x/(1-x*x)+r*z/(1-z)
    need(var_upper < F(17,100), "independent signed count variance")
    with localcontext() as ctx:
        ctx.prec=65
        p0=(D(5).sqrt()-1)/2
        a=p0.sqrt()
        c=p0**3
        for _ in range(9):
            c=2*c*c-1
        q=p0**2+2*p0**10*(1-c)
        # LC4 recovered branch with no extra old-return or retention factor.
        m=(a*(1-q).sqrt()+a*p0*q.sqrt())**2
        z0=D(z.numerator)/D(z.denominator)
        b0=2*p0**2
        det=(1-z0+z0*m)**r
        d=(b0*det.ln()).exp()
        need(D(".41246") < q < D(".41248") and 0<m<1 and 0<d<1, "actual LC4 collar")
        for t in (D(359)/425, D(1)):
            odds=t/d
            # beta B - log(425D) = log(P_H) - beta log(det H).
            reconstructed=t.ln()-b0*det.ln()
            need(abs(odds.ln()-reconstructed)<D("1e-60"), "log odds identity")
        summary={"q":str(round(q,16)), "m_LC4":str(round(m,16)), "h_D":str(round(det,16)),
                 "h_D_power_beta":str(round(d,16))}
    return {"rank":r,"z":str(z),"beta":"2*p^2; the disjoint golden decisions 1 or 00 give beta",
            "LC4_example_decimal":summary,"uniform_P_plus_lower":str(plus_min),
            "uniform_P_minus_lower":str(minus_min),"uniform_per_round_accept_lower":str(per_round),
            "uniform_signed_independent_Poisson_variance_upper":str(var_upper),
            "variance_identity":"-log(P_H)-beta*log(h_D)",
            "scope":"conditional heat and cold-test laws; full H.1 heat value and original physical path valuation not inferred"}


def main():
    print(json.dumps({"status":"PASS","unsigned_Stirling_counts_n_0_to_8":record_polynomials(),
                      "record_law":"P sum_n (1-P)^n (u)_n/n! = P^(1-u)",
                      "thinning_zero":"P^beta","closed_golden_transcript":closed_golden_witness(),
                      "actual_parameters":field_bounds(),"physical_Cost_Info_identified":False},indent=2))


if __name__ == "__main__":
    main()
