"""Check the same-CAR cap comparison and its entropy first source."""

from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "round129"))
from check_car_stop_price import COMMIT, PIN, primary, require

F = sp.QQ_I
RARE = (13, 29, 45, 61)


def gaussian(matrix):
    expanded = matrix.applyfunc(sp.expand)
    return DomainMatrix.from_Matrix(expanded).convert_to(F).to_sparse()


def scale(matrix, scalar):
    return matrix.scalarmul(F.convert(scalar))


def trace_product(left, right):
    right_entries = right.to_dok()
    return sum((v * right_entries.get((j, i), F.zero)
                for (i, j), v in left.to_dok().items()), F.zero)


def trace(matrix):
    return F.to_sympy(sum((v for (i, j), v in matrix.to_dok().items() if i == j), F.zero))


def density(matrix, derivative):
    mass, rate = trace(matrix), trace(derivative)
    rho = scale(matrix, 1 / mass)
    return rho, scale(derivative - scale(rho, rate), 1 / mass)


def transfer(b, adj, db, dadj, rho, drho):
    state = b.matmul(rho).matmul(adj)
    rate = db.matmul(rho).matmul(adj) + b.matmul(drho).matmul(adj) + b.matmul(rho).matmul(dadj)
    return state, rate


def coefficients():
    data = primary()
    ns, dns, a, da = (data[name] for name in ("ns", "dns", "a", "da"))
    lam = data["kappa"]
    normalizer = lam * (1-lam)
    identity, zero = gaussian(data["I"]), gaussian(data["O"])
    prefix = [
        tuple(map(gaussian, (n.H*a, a.H*n, dn.H*a + n.H*da, da.H*n + a.H*dn)))
        for n, dn in zip(ns, dns)
    ]
    effects, effect_jets, output, output_jets = [], [], [], []
    for b, adj, db, dadj in prefix:
        effects.append(adj.matmul(b))
        effect_jets.append(dadj.matmul(b) + adj.matmul(db))
        output.append(b.matmul(adj))
        output_jets.append(db.matmul(adj) + b.matmul(dadj))
    require(effects[0] == scale(identity, lam**2) and effect_jets[0] == zero and output_jets[0] == zero,
            "Quiet state or its jet changed")
    quiet = scale(identity, sp.Rational(1, 16))
    require([j for j, effect in enumerate(effects)
             if effect != scale(identity, trace(effect)/16)] == list(RARE),
            "The nonscalar support changed")
    for tensors, jets in ((output, output_jets), (effects, effect_jets)):
        states = [density(tensors[j], jets[j]) for j in RARE]
        require(len({trace(tensors[j]) for j in RARE}) == len({trace(jets[j]) for j in RARE}) == 1,
                "The rare first-prefix weights or their jets are nonuniform")
        require(sum((rho for rho, _ in states), zero) == scale(quiet, 4),
                "The rare mixture differs from the quiet marginal")
        require(sum((drho for _, drho in states), zero) == zero,
                "The rare mixture moves relative to the quiet marginal")

    active = [j for j in range(1, 64) if trace(effects[j]) != 0]
    require(len(active) == 20, "Unexpected active nonquiet support")
    poles = {}
    log_coeff = defaultdict(lambda: sp.S.Zero)
    log_value = defaultdict(lambda: sp.S.Zero)
    for j in RARE:
        rho, drho = density(output[j], output_jets[j])
        poles[j] = {}
        for m in active:
            state, rate = transfer(*prefix[m], rho, drho)
            reference = prefix[m][0].matmul(quiet).matmul(prefix[m][1])
            require(trace(state) == trace(reference), "One extra visit distinguishes the inputs")
            poles[j][m] = {}
            for k in RARE:
                mass = F.to_sympy(trace_product(effects[k], state))
                baseline = F.to_sympy(trace_product(effects[k], reference))
                derivative = trace_product(effect_jets[k], state) + trace_product(effects[k], rate)
                require(mass.is_positive and baseline.is_positive, "A used addressed pair vanished")
                ratio = mass / baseline
                poles[j][m][k] = ratio
                if ratio != 1:
                    log_value[ratio] += mass/(4*normalizer**2)
                    log_coeff[ratio] += F.to_sympy(derivative)/(4*normalizer**2)

    require(all(poles[j][9][k] == sp.Rational(5 if j == k else 1, 2)
                for j in RARE for k in RARE), "The z19 path witness changed")
    changed = [m for m in active if any(poles[j][m][k] != 1 for j in RARE for k in RARE)]
    require(changed == [9, *RARE], "The informative two-visit support changed")
    t9, trare = (trace(effects[j])/(16*normalizer) for j in (9, RARE[0]))
    require(t9 == sp.Rational(2592, 3155) and trare == sp.Rational(8, 3155),
            "The exact two-visit lower bound changed")
    return dict(sorted(log_value.items())), dict(sorted(log_coeff.items())), lam


def logarithm_bounds(x, steps=24):
    z = (x-1)/(x+1)
    prefix = 2*sum((z**(2*i+1)/(2*i+1) for i in range(steps)), Fraction())
    remainder = 2*abs(z)**(2*steps+1)/((2*steps+1)*(1-z*z))
    return (prefix, prefix+remainder) if z >= 0 else (prefix-remainder, prefix)


def critical_interval(log_coeff, lam):
    p_lo = Fraction(61803398874989, 10**14)
    p_hi = Fraction(61803398874990, 10**14)
    require(p_lo*p_lo+p_lo < 1 < p_hi*p_hi+p_hi, "The Golden bracket failed")
    lam = Fraction(lam)
    v_lo, v_hi = (4*p**3*lam*(1-lam) for p in (p_lo, p_hi))
    two_visits = (v_lo*v_lo*(1+p_lo), v_hi*v_hi*(1+p_hi))
    witness_factor = Fraction(2592, 3155)*Fraction(8, 3155)
    lower_divergence = (Fraction(5, 2)*logarithm_bounds(Fraction(5, 2))[0]
                        + Fraction(3, 2)*logarithm_bounds(Fraction(1, 2))[0])
    require(two_visits[0]*witness_factor*lower_divergence > Fraction(7, 10**7),
            "The known contribution is not larger than the claimed entropy bound")
    lower, upper = Fraction(), Fraction()
    for k, v in log_coeff.items():
        left, right = sorted(Fraction(v)*b for b in logarithm_bounds(Fraction(k)))
        lower += left
        upper += right
    interval = [x*y for x in two_visits for y in (lower, upper)]
    return min(interval), max(interval)


def main():
    log_value, log_coeff, lam = coefficients()
    expected = {
        "gap": (727353, 727354, log_value),
        "gap_jet": (1221385, 1221386, log_coeff),
    }
    receipt = {}
    for key, (left, right, coefficients_in_logs) in expected.items():
        lower, upper = critical_interval(coefficients_in_logs, lam)
        low_bound, high_bound = Fraction(left, 10**12), Fraction(right, 10**12)
        require(low_bound < lower <= upper < high_bound, f"Could not isolate {key}")
        receipt[key] = [str(low_bound), str(high_bound)]
    print(json.dumps({
        "status": "PASS",
        "primary_commit": COMMIT,
        "primary_checker_sha256": PIN,
        "quiet_and_rare_mixture_both_marginals_same_value_and_jet": True,
        "one_extra_visit_same_center_law": True,
        "two_visit_gap_log_coefficients": {str(k): str(v) for k, v in log_value.items()},
        "two_visit_jet_log_coefficients": {str(k): str(v) for k, v in log_coeff.items()},
        "stopped_jensen_strict_intervals_nats": receipt,
        "physical_C_closed": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
