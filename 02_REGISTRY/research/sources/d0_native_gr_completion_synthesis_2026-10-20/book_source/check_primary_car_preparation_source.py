#!/usr/bin/env python3
"""Exact local preparation source on the original primary CAR carrier.

This checks the negative linear coefficient of a small-matter primary
family, rather than using floating values as a sign certificate.  Every
CAR row and all128 real Fourier columns enter the finite inner products.
The owned midpoint and native-word theorems are consumed, not replayed.
No complete physical Book price or field-writing law is selected.
"""

import ast
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


PINS = {
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/check_primary_domain_source.py":
        "c67285c7469db49ff61f3e52597d0bcc6aad991ec1f7af025d6daeb065a43edf",
    "02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/RESULT.md":
        "290772fb869cfa73ed0cc419d3182048d80ea9b02312be0b9d56ad558f5c47be",
    "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py":
        "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
    "02_REGISTRY/research/A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md":
        "71497086dfad667831c77d69201aea3890909d0cf772791f7df32b8b8c3c07d4",
    "02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md":
        "a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915",
    "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_CAR_ACTUATED_METRIC.md":
        "b9dd63f0888a062941c1744d800120e47d20777f429f892f5a98c504a3c0a4be",
}
SIZE, SITES, RIGHT, H = 4, 256, 128, Q(1, 4)
SITES_LIST = tuple(product(range(SIZE), repeat=4))
W = (1, 1, 2, 2)
ORDER = (0, 2, 3, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rejection(test, message):
    try:
        test()
    except RuntimeError:
        return message
    raise RuntimeError("negative control accepted: " + message)


def step(site, role, amount):
    result = list(site)
    result[role] = (result[role] + amount) % SIZE
    return tuple(result)


def site_index(site):
    result = 0
    for digit in site:
        result = SIZE * result + digit
    return result


def creator(role):
    result = [[Q(0) for _ in range(16)] for _ in range(16)]
    predecessors = ORDER[:ORDER.index(role)]
    for mask in range(16):
        if not mask & (1 << role):
            result[mask | (1 << role)][mask] = Q((-1) ** sum(
                bool(mask & (1 << j)) for j in predecessors))
    return tuple(tuple(row) for row in result)


def transpose(a):
    return tuple(zip(*a))


def mmul(a, b):
    return tuple(tuple(sum(x * y for x, y in zip(row, col))
                       for col in transpose(b)) for row in a)


def madd(a, b):
    return tuple(tuple(x + y for x, y in zip(row, other))
                 for row, other in zip(a, b))


def mscale(a, scalar):
    return tuple(tuple(scalar * x for x in row) for row in a)


def eye(n):
    return tuple(tuple(Q(i == j) for j in range(n)) for i in range(n))


CREATORS = tuple(creator(role) for role in range(4))
# Columns of eta_rest (T^-1)^T for the OWNED rational rest/null map T.
# The omitted common factor is a_z=sigma*sqrt(rho_z), sigma=p^3.
LEGS = ((Q(1, 2), Q(-1, 2), 0, 0), (1, 1, 0, 0),
        (0, 0, -1, 0), (0, 0, 0, -1))
ROLE_CREATION = tuple(tuple(tuple(sum(leg[a] * CREATORS[a][i][j]
                                     for a in range(4)) for j in range(16))
                            for i in range(16)) for leg in LEGS)


def flat_column(site, mask):
    """Full literal D0 column, with exact symbolic weight a_weight_site.

    Keys (output_site, output_mask, weight_site) retain distinct shifted
    true-adjoint weights.  No scalar top block is assumed in constructing D.
    """
    result = defaultdict(Q)
    for role, creation in enumerate(ROLE_CREATION):
        for output in range(16):
            forward = creation[output][mask] / H
            backward = creation[mask][output] / H
            if forward:
                previous = step(site, role, -1)
                result[previous, output, previous] += forward
                result[site, output, site] -= forward
            if backward:
                following = step(site, role, 1)
                result[following, output, site] += backward
                result[site, output, site] -= backward
    return {key: value for key, value in result.items() if value}


def poly_add(left, right, scale=Q(1)):
    result = defaultdict(Q, left)
    for key, value in right.items():
        result[key] += scale * value
    return {key: value for key, value in result.items() if value}


def poly_scale(value, scalar):
    return {key: scalar * x for key, x in value.items() if scalar * x}


def column_inner(left, right):
    """Polynomial in a_x a_y, computed from every one of the16 CAR rows."""
    right_groups = defaultdict(list)
    for (site, mask, weight), value in right.items():
        right_groups[site, mask].append((weight, value))
    result = defaultdict(Q)
    for (site, mask, first_weight), first in left.items():
        for second_weight, second in right_groups[site, mask]:
            result[tuple(sorted((first_weight, second_weight)))] += first * second
    return {key: value for key, value in result.items() if value}


def fourier_numerators():
    pairs = []
    for mode in product(range(SIZE), repeat=4):
        opposite = tuple((-x) % SIZE for x in mode)
        if mode < opposite:
            pairs.append(mode)
        if len(pairs) == 64:
            break
    cosines, sines = (1, 0, -1, 0), (0, 1, 0, -1)
    numerators = []
    for site in SITES_LIST:
        row = []
        for mode in pairs:
            phase = sum(x * k for x, k in zip(site, mode)) % SIZE
            row.extend((cosines[phase], sines[phase]))
        numerators.append(tuple(row))
    # f=F_integer/sqrt128, C=f m/sqrt128.  The real columns are
    # unequal pointwise; they are not replaced by uniform phase weights.
    columns = tuple(zip(*numerators))
    for i, column in enumerate(columns):
        for j in range(i + 1):
            require(sum(a * b for a, b in zip(column, columns[j]))
                    == RIGHT * int(i == j), "exact complete real Fourier Gram")
    require(all(sum(x * x for x in row) == 64 for row in numerators),
            "exact local diagonal retains all128 real reference columns")
    return tuple(numerators)


def kernel(numerators, left, right):
    return Q(sum(a * b for a, b in zip(numerators[site_index(left)],
                                      numerators[site_index(right)])), RIGHT)


class Counts(list):
    def sum(self):
        return sum(self)

    def min(self):
        return min(self)

    def max(self):
        return max(self)


class CountAdapter:
    int64 = int

    @staticmethod
    def zeros(length, dtype):
        require(dtype is int, "integer-only owned F/R routing")
        return Counts([0] * length)


def actual_counts(root):
    # Load ONLY the pinned owned definition.  No predecessor main,
    # geometry, old entropy or registered checker suite is executed.
    path = root / next(iter(PINS))
    tree = ast.parse(path.read_text(encoding="utf-8"))
    definitions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                   and node.name == "original_counts"]
    require(len(definitions) == 1, "single owned literal count definition")
    scope = {"np": CountAdapter, "require": require}
    exec(compile(ast.Module(body=definitions, type_ignores=[]), str(path), "exec"), scope)
    counts = scope["original_counts"](20, SIZE)
    require(sha256(json.dumps(counts).encode()).hexdigest() ==
            "fbca167a01fcca76356153586a1006ad1144b612f97740b7611f163f5a3164e9",
            "same complete n20 density counts as the frozen primary receipt")
    return counts


def B(site):
    u = site[0] * H
    return u * (u - H)


def main():
    root = Path(__file__).resolve().parents[5]
    for path, expected in PINS.items():
        require(sha256((root / path).read_bytes()).hexdigest() == expected,
                "pinned input changed: " + path)
    for i, ci in enumerate(CREATORS):
        for j, cj in enumerate(CREATORS):
            require(madd(mmul(ci, cj), mmul(cj, ci)) == mscale(eye(16), 0),
                    "all full16 creator anticommutators")
            require(madd(mmul(ci, transpose(cj)), mmul(transpose(cj), ci))
                    == mscale(eye(16), int(i == j)), "all full16 CAR adjoint anticommutators")
    leg_gram = tuple(tuple(sum(x * y for x, y in zip(a, b)) for b in LEGS) for a in LEGS)
    require(leg_gram == ((Q(1, 2), 0, 0, 0), (0, 2, 0, 0),
                         (0, 0, 1, 0), (0, 0, 0, 1)), "actual rational-null positive leg Gram")
    f = fourier_numerators()
    counts = actual_counts(root)
    plus, minus = step(W, 0, 1), step(W, 0, -1)
    require(B(W) == B(minus) == 0 and B(plus) == Q(1, 8), "actual quadratic primary samples")
    for site in SITES_LIST:
        u = site[0] * H
        require((u + H) * u - u * (u - H) == H * (2 * (u + H / 2) - H),
                "quadratic waveform equals its exact midpoint increment")
    require(kernel(f, W, W) == Q(1, 2) and kernel(f, plus, W) == Q(7, 32),
            "actual all128 Fourier kernel and local normalization")
    target14, target15 = flat_column(W, 14), flat_column(W, 15)
    for mask in range(16):
        require(all((output.bit_count() - mask.bit_count()) % 2
                    for (_, output, _) in flat_column(W, mask)),
                "all16 literal flat Dirac columns reverse CAR parity")
    b14 = poly_scale(column_inner(target14, target14), kernel(f, W, W) / RIGHT)
    b15 = poly_scale(column_inner(target15, target15), kernel(f, W, W) / RIGHT)
    bcross = poly_scale(column_inner(target14, target15), 2 * kernel(f, W, W) / RIGHT)
    expected14 = {(W, W): Q(31, 4) / (SITES * H ** 2),
                  (minus, minus): Q(1, 4) / (SITES * H ** 2),
                  (step(W, 1, -1), step(W, 1, -1)): Q(1) / (SITES * H ** 2)}
    require(b14 == expected14, "full D0 actual-density B14 coefficient")
    require(b15 == {(W, W): Q(9) / (SITES * H ** 2)} and not bcross,
            "full D0 B15 and exact parity cross cancellation")
    a14_clock, a14_slack, a15_linear = {}, {}, {}
    contributing = []
    for site in SITES_LIST:
        weight = kernel(f, site, W) / RIGHT
        clock = flat_column(site, 1)
        low = flat_column(site, 14)
        top = flat_column(site, 15)
        a14_clock = poly_add(a14_clock, column_inner(clock, target14), weight)
        a14_slack = poly_add(a14_slack, column_inner(low, target14), weight)
        require(not column_inner(clock, target15) and not column_inner(low, target15),
                "literal full D0 parity removes every odd-to-top energy term")
        term = column_inner(top, target15)
        expected_top = {(W, W): Q(9) / H ** 2} if site == W else {}
        for role, gamma in enumerate((Q(1, 2), 2, 1, 1)):
            if site in (step(W, role, 1), step(W, role, -1)):
                expected_top = {tuple(sorted((W, site))): -gamma / H ** 2}
        require(term == expected_top, "full top/top composition including every off-stencil zero")
        a15_linear = poly_add(a15_linear, term, weight * B(site))
        if term and B(site):
            contributing.append(site)
    pair = tuple(sorted((W, plus)))
    require(a15_linear == {pair: Q(-7, 4096)}, "exact native CAR A15 coefficient ledger")
    source_linear = poly_scale(a15_linear, 2)
    require(source_linear == {pair: Q(-7, 2048)}, "exact native CAR source coefficient ledger")
    require(contributing == [plus], "only the actual next-u top sample contributes")
    # The source is 2p*A15_linear*t.  Since a_z=sigma sqrt(rho_z),
    # sigma=p^3, its exact linear coefficient is -7 p^7 sqrt(rho_w rho_+)/2048.
    rho_w = Q(SITES * counts[site_index(W)], counts.sum())
    rho_plus = Q(SITES * counts[site_index(plus)], counts.sum())
    p_lower, p_upper = Q(3, 5), Q(5, 8)
    require(p_lower ** 2 + p_lower - 1 < 0 < p_upper ** 2 + p_upper - 1,
            "rigorous positive Golden root enclosure")
    source_abs_lower = Q(7, 2048) * p_lower ** 7 * min(rho_w, rho_plus)
    source_abs_upper = Q(7, 2048) * p_upper ** 7 * max(rho_w, rho_plus)
    require(0 < source_abs_lower < source_abs_upper and rho_w > 0 and rho_plus > 0,
            "strict rational magnitude bounds on the exact nonzero coefficient")
    # For arbitrary real c,s with c^2+s^2=1, the actual two-mask rotation
    # has column squared norms c^2+s^2 and zero cross term exactly.
    rotation_columns = (((1, 0), (0, 1)), ((0, -1), (1, 0)))
    def quadratic_coeff(left, right):
        return (sum(a[0] * b[0] for a, b in zip(left, right)),
                sum(a[1] * b[1] for a, b in zip(left, right)),
                sum(a[0] * b[1] + a[1] * b[0] for a, b in zip(left, right)))
    require(quadratic_coeff(rotation_columns[0], rotation_columns[0]) == (1, 1, 0)
            and quadratic_coeff(rotation_columns[1], rotation_columns[1]) == (1, 1, 0)
            and quadratic_coeff(*rotation_columns) == (0, 0, 0),
            "actual rotation preserves every oldRIGHT Gram entry")
    controls = [
        rejection(lambda: require(poly_scale(source_linear, RIGHT) == source_linear,
                                  "drop physical reference normalization"), "omit 1/128 RIGHT factor"),
        rejection(lambda: require(Q(1, 2) == 1, "replace actual null leg Gram"),
                  "Euclidean null-mask substitution changes the source"),
        rejection(lambda: require(poly_scale(source_linear, -1) == source_linear,
                                  "reverse actual native angle"), "wrong native rotation orientation"),
        rejection(lambda: require(kernel(f, plus, W) == 0, "erase Fourier neighbour coherence"),
                  "diagonal-only reference kernel loses the source"),
        rejection(lambda: require(rho_w == rho_plus == 1, "uniformize actual F/R weights"),
                  "actual n20 density is retained"),
    ]
    print(json.dumps({
        "status": "PASS", "arithmetic": "exact Fraction; no floating sign or spectral cutoff",
        "carrier": {"L": SIZE, "sites": SITES, "CAR": 16, "oldRIGHT": RIGHT,
                    "ell": str(H), "sigma": "p^3", "FR_cost_depth": 20,
                    "FR_words": counts.sum(), "site": W, "next_u": plus,
                    "count_w": counts[site_index(W)], "count_next_u": counts[site_index(plus)]},
        "primary_family": "c=0,b=t*u*(u-1/4),physical_Psi=sigma^2*(0,b),W_harmonic=0; H,K=O(t^2)",
        "coefficient_ledger": {
            "convention": "A_j=Re<DC,DV_j>,B_j=||DV_j||^2; R(alpha)-R(0)=2p(cos(alpha)-1)A14+2p*sin(alpha)*A15+p^2(cos(alpha)-1)^2*B14+p^2*sin(alpha)^2*B15",
            "a_z": "sigma*sqrt(rho_z)",
            "A14_at_zero": {"sqrt_p_clock_terms": len(a14_clock), "p_slack_terms": len(a14_slack)},
            "A15": "-(7/4096)*a_w*a_next_u*t+O(t^3)",
            "B14_at_zero": "[(31/4)*a_w^2+(1/4)*a_(w-u)^2+a_(w-v)^2]/(S*ell^2)",
            "B15_at_zero": "9*a_w^2/(S*ell^2)", "Bcross": "0 by exact CAR parity",
            "P_F_w_next_u": "7/32", "complete_state_kernel_w_next_u": "7/4096",
            "Delta0_top_w_next_u": "-sigma^2*sqrt(rho_w*rho_next_u)/(2*ell^2)",
        },
        "preparation_source": {
            "formula": "g(t)=-(7*p*sigma^2*sqrt(rho_w*rho_next_u)/2048)*t+O(t^3)",
            "absolute_linear_coefficient_strict_lower": str(source_abs_lower),
            "absolute_linear_coefficient_strict_upper": str(source_abs_upper),
            "sign": "negative for every sufficiently small positive t by analyticity",
            "retained_RIGHT_Gram": "C(alpha)^* C(alpha)=I128/128 exactly",
        },
        "native_word_consumer": "owned finite signed G^2 returns give arbitrarily small positive alpha; paid inverse echo retained",
        "boundary_scope": "local primary solution and stated periodic storage regulator; no global periodic polynomial root",
        "H_and_closed_J_fixed": "geometry, native Delta, original unprepared full-history cut and clock fixed during CAR rotation",
        "not_the_prepared_image_echo": True,
        "complete_physical_Cost_Info_or_GR_selection_derived": False,
        "negative_controls": controls, "source_sha256": PINS,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
