"""Exact B167 checks for the measured return, cold saturation, and early SITE."""

from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
import json
import subprocess

import sympy as sp


PILOT = Path(__file__).resolve().parents[2]
ROOT = PILOT.parents[3]
PRIMARY = (
    "02_REGISTRY/research/sources/d0_gr_2026-11-18/"
    "followups/2026-11-19/metric/"
)
GOLDEN = (sp.sqrt(5) - 1) / 2
FIELD = sp.QQ.algebraic_field(GOLDEN)
P = FIELD.from_sympy(GOLDEN)


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def source_pins():
    local = {
        "direct/round80/READOUT_RU.md":
            "84873c50d6fe2a05045c7b8735fcd7086e85450cbae8f95d288b7b89144e9fb4",
        "open/round165/B165_SERVICE_ABORT_RC3_RU.md":
            "55ebd2f164e55ea9297257ae44aa914e60fb354e2d83f27d5c3ae0292d9222ad",
    }
    archived = {
        ("04931a7a26a9741bba0584c8e1413613ff7a28d5", "EIGHT_READERS_RU.md"):
            "e6cf63011b94a10068d9545eb901c6f17c22024693d9ea21bc874dcd7f86fb0e",
        ("65753c972b4ad1e528a29b0343e30c3ecc9b9670", "FULL_SITE_SORT_RU.md"):
            "31f1bb57bd2066a26999565258bfb3238c8fb3a9c36fdf5cd7b11b0beee936a7",
    }
    for name, expected in local.items():
        require(sha256((PILOT / name).read_bytes()).hexdigest() == expected, name)
    for (revision, name), expected in archived.items():
        raw = subprocess.check_output(
            ["git", "show", f"{revision}:{PRIMARY}{name}"], cwd=ROOT,
        )
        require(sha256(raw).hexdigest() == expected, name)
    return len(local) + len(archived)


def check_tree(x, y, m, n):
    squared = x*x + y*y
    q = Fraction(x*x, squared)
    s = Fraction(x*y, squared)
    projectors = (((1-q, -s), (-s, q)), ((q, s), (s, 1-q)))
    report_weights = (P, P**2)
    eta = Fraction(16, 25)
    mu = Fraction(3, 5)
    nu = Fraction(4, 5)
    a = P**(2*n)
    ell = P**3 * sum(P**(2*j) for j in range(n))
    cold_sum = FIELD.zero
    born_sum = Fraction(0)
    service_sum = Fraction(0)
    overflow_sum = Fraction(0)
    leaves = 0

    def finish(state, passive, terminal):
        nonlocal born_sum, service_sum, overflow_sum, cold_sum, leaves
        mass = sum(value*value for value in state)
        require(mass > 0, "an enumerated terminal lost its occupied rank")
        born_sum += mass
        cold_sum += passive * FIELD.convert(state[0]**2 / mass)
        service_sum += mass if terminal == "service" else 0
        overflow_sum += mass if terminal == "overflow" else 0
        leaves += 1

    def visit(state, passive, depth):
        for label, projector in enumerate(projectors):
            first, second = (sum(row[j] * state[j] for j in range(2))
                             for row in projector)
            report_passive = passive * report_weights[label]
            finish((mu**n * first, mu**n * second), report_passive*a, "service")
            for attempt in range(n):
                factor = mu**attempt * nu
                child_passive = report_passive * P**(2*attempt+3)
                finish((factor*first, 0), child_passive, "return")
                failure = (0, factor*second)
                if depth == m:
                    finish(failure, child_passive, "overflow")
                else:
                    visit(failure, child_passive, depth+1)

    visit((Fraction(1), Fraction(0)), FIELD.one, 0)
    depth_sum = sum(ell**j for j in range(m+1))
    expected_cold = depth_sum * (
        ell + a * (P*FIELD.convert(1-q) + P**2*FIELD.convert(q))
    )
    beta = 2*q*(1-q)
    service = (1-eta)**n
    attempted = 1 + beta*(1-service) * sum(
        ((1-beta)*(1-service))**j for j in range(m)
    )
    expected_count = (
        sum((2*n)**j for j in range(1, m+2))
        + 2*sum((2*n)**j for j in range(m+1))
        + (2*n)**(m+1)
    )
    require(cold_sum == expected_cold, "wrong normalized cold sum")
    require(born_sum == 1 and leaves == expected_count, "incomplete stopping tree")
    require(service_sum == service*attempted <= 2*service, "wrong service mass")
    require(overflow_sum == (1-service)**(m+1)*beta*(1-beta)**m,
            "wrong overflow mass")


def orthogonal_projector(frame):
    return frame * (frame.T*frame).inv() * frame.T


def check_matrix_saturation():
    rotation = sp.Matrix([[3, -4], [4, 3]]) / 5
    e = rotation * sp.diag(sp.Rational(9, 25), sp.Rational(25, 169)) * rotation.T
    s = rotation * sp.diag(sp.Rational(12, 25), sp.Rational(60, 169)) * rotation.T
    eye = sp.eye(6)
    q1 = sp.diag(e.row_join(s).col_join(s.row_join(sp.eye(2)-e)), 1, 0)
    q0 = eye - q1
    require(q1*q1 == q1 and q1.T == q1 and e[0, 1] != 0, "invalid matrix fixture")
    initial = eye[:, :2]
    late = eye[:, 2:4]

    def skew(first, second):
        result = sp.zeros(6)
        result[first, second], result[second, first] = 1, -1
        return result

    axes = [skew(*number) for number in product(range(6), repeat=2)
            if number[0] < number[1]]
    nonzero_backward = 0
    strict_defects = 0
    for projector, incoming in product((q0, q1), (initial, late)):
        y = projector*initial
        x = projector*incoming
        supported = orthogonal_projector(x)
        require(supported*y == y, "failed simultaneous saturation")

        rotation_with_extra = eye.copy()
        extra = 4 if projector == q1 else 5
        source = 0 if incoming == initial else 2
        rotation_with_extra[source, source] = sp.Rational(3, 5)
        rotation_with_extra[extra, extra] = sp.Rational(3, 5)
        rotation_with_extra[source, extra] = sp.Rational(-4, 5)
        rotation_with_extra[extra, source] = sp.Rational(4, 5)
        moved = orthogonal_projector(projector*rotation_with_extra*incoming)
        residual = (eye-moved)*y
        defect = y.T*y - y.T*moved*y
        require(defect == residual.T*residual, "wrong operator saturation deficit")
        strict_defects += int(defect != sp.zeros(2))

        inverse_frame = (x.T*x).inv()*x.T
        for axis in axes:
            first = (eye-supported)*projector*axis*incoming*inverse_frame
            require(y.T*(first+first.T)*y == sp.zeros(2),
                    "an independent forward axis was detected")
            dy = projector*axis*initial
            derivative = dy.T*supported*y + y.T*supported*dy
            require(derivative == dy.T*y+y.T*dy, "lost backward derivative")
            if derivative != sp.zeros(2):
                nonzero_backward += 1
    require(strict_defects > 0 and nonzero_backward > 0, "vacuous saturation fixture")
    return {"independent_forward_axes": len(axes)*4,
            "nonzero_backward_axes": nonzero_backward,
            "strict_finite_defects": strict_defects}


def check_selector():
    denominator = 705600
    settings = range(1, 9)
    signed = [Fraction((-1)**(j-1)*denominator*comb(8, j), j*j)
              for j in settings]
    require(all(value.denominator == 1 for value in signed), "noninteger allocation")
    counts = [abs(int(value)) for value in signed]
    levels = [1, 1]
    for _ in range(2, 38):
        levels.append(levels[-1]+levels[-2])
    require(levels[36] == 24157817 and levels[35] == 14930352,
            "wrong counts of exact and overshooting Golden codes")
    require(sum(counts) == 20316969 and sum(counts) < levels[36],
            "wrong accepted Golden prefix mass")
    for degree in range(2, 10):
        require(sum(value*j**degree for value, j in zip(signed, settings))
                == (denominator if degree == 2 else 0), "wrong interpolation moment")
    require(sum(count*j*j for count, j in zip(counts, settings)) == 255*denominator,
            "wrong total variation multiplier")

    # A common affine cold sum must use the complemented read on negative settings.
    qref = Fraction(2, 5)
    ell, a, w = P**3, P**2, FIELD.one + P**3
    pi = [count * P**36 for count in counts]
    active = sum(pi)
    for signal in (Fraction(-1, 10), Fraction(0), Fraction(1, 10)):
        values = [qref + signal*Fraction(j*j, 64) + Fraction(j**3, 10**5)
                  for j in settings]
        reads = [q if sign > 0 else 1-q for q, sign in zip(values, signed)]
        require(all(0 < q < 1 for q in reads), "interpolation fixture lost support")
        reported = sum(weight*FIELD.convert(q) for weight, q in zip(pi, reads))
        offset = sum(weight*FIELD.convert(qref if sign > 0 else 1-qref)
                     for weight, sign in zip(pi, signed))
        require(reported == offset + denominator*P**36*FIELD.convert(signal/64),
                "wrong physically complemented aggregate")
        listed = 1-active+sum(
            weight*w*(ell+a*(P-P**3*FIELD.convert(q)))
            for weight, q in zip(pi, reads)
        )
        require(listed == 1-active+w*((ell+a*P)*active-a*P**3*reported),
                "cold blocks were not summed before log")
    return {"active_prefixes": sum(counts),
            "inactive_prefixes": levels[36]+levels[35]-sum(counts),
            "allocations": counts}


def check_early_site():
    low, high = Fraction("0.61803398874"), Fraction("0.61803398876")
    require(low**2+low < 1 < high**2+high, "bad Golden interval")
    zeta = Fraction(1, 2**20)
    k0_lower = 2*high**(-5)*(1-zeta*4*high**3*(1+high**6)+low**6)
    gamma_upper = 705600*high**36
    require(3*k0_lower/(16*gamma_upper) > 207 and 765*k0_lower/16 > 1119,
            "the actual early SITE lower margins failed")
    require((low-high**2/256)**2 > Fraction(1, 6) and high**2 < Fraction(1, 2),
            "SC1 material derivative interval lost monotonicity")

    e1 = sp.diag(sp.Rational(3, 10), sp.Rational(2, 5))
    e0 = sp.eye(2)-e1
    delta = e1[1, 1]-e1[0, 0]
    saturation = 0
    for effect in (e0, e1):
        mass = min(effect.diagonal())
        factor = sp.diag(*(sp.sqrt(mass/x) for x in effect.diagonal()))
        require(factor.T*effect*factor == mass*sp.eye(2), "wrong polar filter")
        require(all(x <= 1 for x in (factor.T*factor).diagonal()), "not a filter")
        saturation += mass
    require(saturation == 1-delta, "wrong exact SITE return threshold")
    return {"one_setting_lower_per_j_squared_b_h": 207,
            "joint_record_lower_per_b_h": 1119,
            "two_site_exact_return_fixture": str(saturation)}


def main():
    trees = list(product(((3, 4), (5, 12)), range(3), range(1, 4)))
    for (x, y), m, n in trees:
        check_tree(x, y, m, n)
    payload = {
        "source_pins": source_pins(),
        "exact_matched_stopping_trees": len(trees),
        "saturation": check_matrix_saturation(),
        "eight_setting": check_selector(),
        "early_protected_site": check_early_site(),
        "joint_H1_device_replayed": False,
        "full_physical_cost_minus_info_proved": False,
        "GR_closed": False,
        "status": "PASS",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
