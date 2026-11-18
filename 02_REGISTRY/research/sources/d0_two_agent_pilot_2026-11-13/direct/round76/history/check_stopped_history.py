"""Exact checks of the stopped Golden path sum, input queries and fair clock."""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product

import sympy as sp


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def identical(left, right):
    require(sp.factor(left - right) == 0, "Unequal expressions")


def root_and_clock():
    # z counts original input calls and t counts unbiased split coins.
    # Sum over the complete tree on both branches, even if the first son fails.
    a, z, t = sp.symbols("a z t", positive=True)
    x = a**2
    u = 1 - x
    total = sp.Function("M")(z, t)
    positive = sp.Function("S")(z, t)
    rec_total = t * (1 + z * (x + u * total**2)) / 2
    rec_positive = t * (1 + z * u * positive**2) / 2
    base = {total: 1, positive: 1 / (1 + a), z: 1, t: 1}
    identical(rec_total.xreplace(base), 1)
    identical(rec_positive.xreplace(base), 1 / (1 + a))

    # At the outer root an input is drawn before the subtree.
    mass = z * (x + u * total)
    accept = z * (x + u * (total - positive))
    identical(accept.xreplace(base), a)
    differences = []
    for variable in (z, t):
        derivatives = {}
        for term, recurrence in [(total, rec_total), (positive, rec_positive)]:
            symbol = sp.Symbol("slope")
            rule = {sp.diff(term, variable): symbol, **base}
            derivative = sp.solve(symbol - sp.diff(recurrence, variable).xreplace(rule), symbol)[0]
            derivatives[sp.diff(term, variable)] = derivative
        rule = {**derivatives, **base}
        covariance = (sp.diff(accept, variable) - a * sp.diff(mass, variable)).xreplace(rule)
        differences.append(sp.factor(covariance / (a * (1 - a))))
    identical(differences[0], (1 - a) / (2 * a**3))
    identical(differences[1], 1/a**3 - 1/a**2 - 1/a)

    # Independent Geom(a) readings, a new Bernoulli(a) and a fair bit are drawn
    # on every history, before deciding which non-negative integer pad to run.
    dummy_input_on_failure = (1 - a) / (2 * a**3)
    dummy_fair_on_failure = 1/a**3
    dummy_fair_on_success = 1/a**2 + 1/a
    identical(differences[0] - dummy_input_on_failure, 0)
    identical(differences[1] + dummy_fair_on_success - dummy_fair_on_failure, 0)
    # The likelihood score holds for every finite-mean, differentiable procedure.
    # After equalizing the total count, the conditional 0-count difference is -d.
    d = sp.Symbol("difference")
    score = a * (1-a) * (d/x + d/(1-x))
    identical(sp.solve(score - 1/(2*a), d)[0], (1+a)/2)
    print("Stopped root, both clock covariances, integer pads and the two outcome fees agree.")


def finite_prefix():
    # Independent exhaustive count by splitting finite-depth trees.
    x = Q(9, 25)
    u = 1 - x
    leaves = {(False, 0, 0): Q(1)}
    for depth in range(1, 4):
        result = defaultdict(Q)
        result[(True, 0, 1)] += Q(1, 2)
        result[(False, 1, 1)] += x/2
        for (a, b) in product(leaves, repeat=2):
            result[(a[0] and b[0], 1+a[1]+b[1], 1+a[2]+b[2])] += u*leaves[a]*leaves[b]/2
        leaves = result
        require(sum(leaves.values()) == 1, "Lost a retained leaf")
        root = 1-u*sum(prob for (good, _, _), prob in leaves.items() if good)
        require(0 < root-Q(3, 5) <= u**(depth+1), "Value tail not enclosed")
    r = Q(3, 4)
    true = Q(3, 5)
    value, slope = Q(0), Q(0)
    bound = 1 / (2*(1-r))
    # Denominators double in bit length at each exact iteration.
    for k in range(1, 10):
        slope, value = value**2/2 + u*value*slope, Q(1,2)+u*value**2/2
        root_slope_x = value+u*slope
        upper = r**k + r*(bound*r**k + k*(1+r*bound)*r**(k-1))
        require(abs(root_slope_x-1/(2*true)) <= upper, "Derivative tail not enclosed")
    print("Exhaustive marked clock trees and the first-source truncation bound agree.")


def actual_gate():
    p = (sp.sqrt(5)-1)/2
    a = sp.sqrt(p)
    j = sp.Matrix([[0,-1],[1,0]])
    g = a*sp.eye(2)+p*j
    # Two equally likely arms. A rejected leaf splits between +I and -I.
    signed_mean = (a*sp.eye(2)+p*j)/2
    cx01 = sp.eye(4)[:, [0,1,3,2]]
    cx10 = sp.eye(4)[:, [0,3,2,1]]
    w = cx10*cx01*sp.kronecker_product(sp.eye(2),g)
    lifted = cx10*cx01*sp.kronecker_product(sp.eye(2),signed_mean)
    owner = sp.Matrix([[a,-p,0,0],[0,0,a,-p],[0,0,p,a],[p,a,0,0]])
    require(w == owner and 2*lifted == w, "Wrong order at the original paid gate")
    require(sp.simplify(sp.trace(w*w)- (a-p)**2) == 0, "Native invariant changed")
    require(sp.minpoly(a).as_poly().degree() == 4, "Finite-state field example changed")
    require(sp.simplify(1/(1+2/p)-p**3) == 0, "Wrong noisy input threshold")
    print("The original four-address gate is recovered with constant scale 1/2.")


if __name__ == "__main__":
    root_and_clock()
    finite_prefix()
    actual_gate()
