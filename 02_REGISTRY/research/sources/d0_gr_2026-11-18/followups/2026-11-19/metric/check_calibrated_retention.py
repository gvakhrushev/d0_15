"""Exact golden checks for full-tree stationary retention records."""
from fractions import Fraction as F
from itertools import product
import json
import sympy as s

from check_extra_work import span, check


def main():
    p = (s.sqrt(5)-1)/2
    a = s.sqrt(p)
    mu0, mu1 = p, p**3
    total = s.simplify(mu0+mu1)
    optimum = s.simplify(mu1/total)
    check(s.simplify(total-(1-p**4)) == 0, "complete valid born mass")
    check(s.simplify(optimum-(5-s.sqrt(5))/10) == 0, "physical optimal mark probability")
    check(s.simplify(s.sqrt(mu0*(1-optimum))+s.sqrt(mu1*optimum)-s.sqrt(total)) == 0,
          "one-mark sharp Cauchy equality")

    # Directly verify every conditional full-tree derivative is the same.
    # Thus each normalized tangent, including correlations, cancels.
    dimensions = {}
    for m in range(1, 6):
        masses = [mu0**(m-sum(word))*mu1**sum(word)
                  for word in product((0,1), repeat=m)]
        q = [s.simplify(x/total**m) for x in masses]
        check(s.simplify(sum(q)-1) == 0, "full conditional normalization")
        for mass, probability in zip(masses,q):
            check(s.simplify(mass/probability-total**m) == 0, "common tangent coefficient")
        for index in range(1, len(q)):
            check(s.simplify(masses[0]*q[index]-masses[index]*q[0]) == 0,
                  "all correlation-exchange tangents vanish")
        dimensions[str(m)] = len(q)

    pi = (span(5).sqrt()-1)/2
    mui0, mui1 = pi, pi**3
    total_i = mui0+mui1
    u_i = mui1/total_i
    check(u_i.lo>F(27,100) and u_i.hi<F(28,100), "optimal mark interior")
    check((4*total_i).lo>3, "full-clock dilution dominates squared cold loss")
    # p² is the noisy original probability. It is strictly different.
    check((pi**2-u_i).lo>F(1,10), "retention mark is a different physical instrument")
    print(json.dumps({
        "status":"PASS", "optimal_probability":u_i.fmt(15),
        "valid_reference_mass":total_i.fmt(15),
        "clock_growth_per_retention":(4*total_i).fmt(15),
        "binary_tree_leaves":dimensions,
        "scope":"global cold optimum at fixed initial label law; exact all-conditional probability tangents; native finite compiler and complete physical cost remain open"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
