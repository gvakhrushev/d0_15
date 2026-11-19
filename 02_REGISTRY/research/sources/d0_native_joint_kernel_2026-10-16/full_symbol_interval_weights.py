"""Rigorous scalar weights for the complete q3300 native symbol.

Every scalar is enclosed over the published d/o root rectangle, not merely
evaluated at its center. Exact feature grouping retains all 4096 momenta,
all sixteen exterior states in Z, and all 128 occupied shell states. Signed
complement resolvents retain the negative ground-state denominator.

The divided difference is the fixed-Z local spectral derivative in the
nonzero-q symbol, matching full_symbol_diagnostic._spectral_data. The full
normalizer Z is recomputed and propagated as an interval on the rectangle;
its separate trace-rank-one Hessian term vanishes at nonzero Fourier q.
Feature equality is exact integer Q(sqrt(2)) data. Unequal feature pairs
must have an interval-separated energy gap; no tolerance selects a branch.

spectral_intervals(repo) returns reusable live interval arrays plus exact
mode/feature indices. run(repo) exports a compact outward-rounded summary.
No old run(), root solve, receipt writer, operator/Hessian assembly or inertia
claim occurs here. This file writes nothing.
"""
from __future__ import annotations

import ast
from collections import Counter
from decimal import Decimal, localcontext, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import time

import mpmath
from mpmath.ctx_iv import MPIntervalContext


ROOT = Path(__file__).resolve().parents[4]
WAVE = "02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py"
RECEIPT = "02_REGISTRY/research/sources/d0_record_generated_heat_v8_2026-10-14/receipt.json"
PINS = {
    WAVE: "2b12f26d814a57cc99084e904deeac69a8f64a8d9a0eb9ee765e8104ef50bc37",
    RECEIPT: "da44c7393b1164ce4babcab2ea13707958364d273d2c3fa1d86d514a9ac83ae9",
}
Q = (3, 3, 0, 0)
L, FOCK, REFERENCE, ROUNDS = 8, 16, 128, 8192
DPS = 80


def require(condition, name):
    if not bool(condition):
        raise ArithmeticError("full_symbol_interval_weights:" + name)


def _fraction(binary):
    """Exact rational value of a finite mpmath binary endpoint."""
    sign, mantissa, exponent, bits = binary
    require(bits >= 0 and sign in (0, 1), "finite_real_binary_interval_endpoint")
    numerator = -mantissa if sign else mantissa
    return (Fraction(numerator * (1 << exponent)) if exponent >= 0
            else Fraction(numerator, 1 << (-exponent)))


def bounds(value):
    """Return exact Fraction lower/upper endpoints, with no float conversion."""
    return tuple(_fraction(endpoint) for endpoint in value._mpi_)


def _decimal(value, rounding, digits=68):
    with localcontext() as context:
        context.prec = digits
        context.rounding = rounding
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def interval_record(value):
    lower, upper = bounds(value)
    return {"lower": _decimal(lower, ROUND_FLOOR),
            "upper": _decimal(upper, ROUND_CEILING),
            "width_upper": _decimal(upper-lower, ROUND_CEILING)}


def float_bounds(value):
    """Binary64 export expanded one ulp outward from exact binary endpoints."""
    lower, upper = bounds(value)
    return math.nextafter(float(lower), -math.inf), math.nextafter(float(upper), math.inf)


def _owned_features(repo):
    for path, digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest, "pin:"+path)
    tree = ast.parse((repo/WAVE).read_bytes())
    names = {"qadd", "qsub", "qmul", "qsum", "_z", "_real_inner", "_feature"}
    nodes = [node for node in tree.body
             if (isinstance(node, ast.FunctionDef) and node.name in names)
             or (isinstance(node, ast.Assign)
                 and any(isinstance(target, ast.Name) and target.id in {"RE", "IM"}
                         for target in node.targets))]
    require(len(nodes) == 9, "only_owned_exact_feature_nodes")
    scope = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), WAVE, "exec"), scope)
    return lambda mode: scope["_feature"](scope["_z"](mode))


def _root_box(center, radius):
    with localcontext() as context:
        context.prec = 100
        c, r = Decimal(center), Decimal(radius)
        return str(c-r), str(c+r)


def _separated(value):
    lower, upper = bounds(value)
    return lower > 0 or upper < 0


def _absolute_lower(value):
    lower, upper = bounds(value)
    require(lower > 0 or upper < 0, "absolute_lower_requires_separation")
    return min(abs(lower), abs(upper))


def spectral_intervals(repo=None):
    """All mode arrays are live 80-dps outward-rounded real intervals.

    feature_data keys are exact ((A0,A1),(C0,C1)) integer pairs. pair_data
    uses canonical unordered feature pairs, while outgoing preserves the
    directed k -> k+q mode index. Repeated arrays share cached intervals.
    """
    start = time.perf_counter()
    repo = ROOT if repo is None else Path(repo).resolve()
    feature = _owned_features(repo)
    receipt = json.loads((repo/RECEIPT).read_bytes())
    owned = receipt["interval"]
    require(owned["L"] == L and owned["rounds"] == ROUNDS
            and owned["Fock_dimension"] == FOCK
            and owned["purifying_reference_dimension"] == REFERENCE,
            "owned_full_experiment_dimensions")
    require(owned["workspace_thermal_multiplicity_retained"] is True
            and owned["matter_operator"] == "Delta, not log generator",
            "owned_full_trace_and_matter_convention")
    iv = MPIntervalContext()
    iv.dps = DPS
    dbox, obox = [_root_box(center, owned["root_radius"]) for center in owned["root_center"]]
    d, o = iv.mpf(dbox), iv.mpf(obox)
    require(bounds(o)[0] > 0 and bounds(d-o)[0] > 0, "whole_rectangle_regular_d_greater_o_positive")
    sqrt2, sqrt5 = iv.sqrt(2), iv.sqrt(5)
    p = (sqrt5-1)/2
    alpha, beta, fugacity = p*p/ROUNDS, 2*p*p, iv.mpf(1)/(2**20)
    m = 2*ROUNDS
    modes = tuple(itertools.product(range(L), repeat=4))
    mode_index = {mode: index for index, mode in enumerate(modes)}
    features = tuple(feature(mode) for mode in modes)
    counts = Counter(features)
    outgoing = tuple(mode_index[tuple((mode[r]+Q[r]) % L for r in range(4))]
                     for mode in modes)
    require(all(index != other for index, other in enumerate(outgoing)),
            "nonzero_q_has_no_diagonal_momentum_block_for_trace_rank_one_term")
    shell_modes = {tuple(sign if r == axis else 0 for r in range(4))
                   for axis in range(4) for sign in (1, 7)}
    shell_feature = features[mode_index[(0, 0, 0, 1)]]
    require({mode for mode, f in zip(modes, features) if f == shell_feature} == shell_modes,
            "exactly_all_eight_shell_momenta_not_tolerance_selection")
    require(len(modes) == 4096 and len(counts) == 119 and sum(counts.values()) == len(modes),
            "complete_4096_modes_and_119_feature_groups")
    require(counts[shell_feature]*FOCK == REFERENCE, "all_128_occupied_shell_states")

    def real_pair(pair):
        return pair[0]+pair[1]*sqrt2

    def energy(f):
        return d*real_pair(f[0])+o*real_pair(f[1])

    def gap(left, right):
        # Subtract exact feature coefficients BEFORE interval arithmetic.
        delta_a = tuple(right[0][j]-left[0][j] for j in range(2))
        delta_c = tuple(right[1][j]-left[1][j] for j in range(2))
        return d*real_pair(delta_a)+o*real_pair(delta_c)

    data = {}
    for f in sorted(counts):
        lam = energy(f)
        require(bounds(lam)[0] >= 0, "nonnegative_actual_energy_feature")
        survival = 1-alpha*lam
        require(bounds(survival)[0] > 0, "all_survival_intervals_strictly_positive")
        power = survival**m  # exact integer-power interval; no rounded exponential input.
        data[f] = {"lambda": lam, "sqrt_lambda": iv.sqrt(lam),
                   "survival": survival, "power": power, "count": counts[f]}
    partition = FOCK*sum((counts[f]*data[f]["power"] for f in sorted(counts)), iv.mpf(0))
    require(bounds(partition)[0] > 0, "full_Z_strictly_positive")
    shell_epsilon = data[shell_feature]["lambda"]
    resolvent_gaps = []
    for f in sorted(counts):
        row = data[f]
        b, e = row["survival"], row["power"]
        h = 1-fugacity+fugacity*e
        require(bounds(h)[0] > 0, "all_feedback_denominators_positive")
        kappa = -e/(partition*b)+REFERENCE*beta*fugacity*e/(h*b)
        # B'= -alpha, e=B^m, h=1-z+z*e. Differentiate
        # -B^(m-1)/Z + M*beta*z*B^(m-1)/h at fixed Z analytically.
        derivative = ((m-1)*alpha*e/(partition*b*b)
                      +REFERENCE*beta*fugacity*alpha*e/(h*b*b)
                       *(-(m-1)+m*fugacity*e/h))
        rho = iv.mpf(1)/REFERENCE if f == shell_feature else iv.mpf(0)
        if f == shell_feature:
            resolvent = iv.mpf(0)
        else:
            denominator = gap(shell_feature, f)
            require(_separated(denominator), "every_complement_shell_gap_interval_separated")
            resolvent_gaps.append(_absolute_lower(denominator))
            resolvent = 1/denominator
        row.update(kappa=kappa, derivative=derivative, rho=rho,
                   chi=rho+kappa, resolvent=resolvent)
    ground_feature = features[0]
    require(bounds(data[ground_feature]["resolvent"])[1] < 0,
            "signed_negative_ground_resolvent_retained")
    require(bounds(data[ground_feature]["lambda"]) == (Fraction(0), Fraction(0)),
            "exact_ground_zero_mode_retained_in_partition")

    pairs = {}
    edge_keys = []
    distinct_gaps = []
    equal_edges = 0
    for index, other in enumerate(outgoing):
        fk, fl = features[index], features[other]
        key = tuple(sorted((fk, fl)))
        edge_keys.append(key)
        if fk == fl:
            equal_edges += 1
        if key in pairs:
            continue
        left, right = key
        dl, dr = data[left], data[right]
        if left == right:
            dd = dl["derivative"]
            difference = iv.mpf(0)
        else:
            difference = gap(left, right)
            require(_separated(difference), "distinct_exact_features_have_interval_separated_gap")
            distinct_gaps.append(_absolute_lower(difference))
            dd = (dr["kappa"]-dl["kappa"])/difference
        gamma_j = dl["chi"]+dr["chi"]
        weight_x = dd-dl["rho"]*dr["resolvent"]-dr["rho"]*dl["resolvent"]
        pairs[key] = {"dd": dd, "gamma_J": gamma_j, "weight_X": weight_x,
                      "energy_gap": difference, "equal_exact_features": left == right}
    require(equal_edges == 624 and len(pairs) == 472,
            "complete_exact_equal_branch_and_pair_cache_counts")
    f = (iv.sqrt(d+3*o)+3*iv.sqrt(d-o))/4
    g = (iv.sqrt(d+3*o)-iv.sqrt(d-o))/4
    require(bounds(g)[0] > 0 and bounds(f-g)[0] > 0, "whole_rectangle_frame_a_greater_b_positive")
    result = {"iv": iv, "iv_ctx": iv, "d": d, "o": o, "a": f, "b": g,
              "alpha": alpha, "beta": beta, "fugacity": fugacity,
              "Z": partition, "epsilon": shell_epsilon, "modes": modes,
              "outgoing": outgoing, "features": features, "feature_counts": counts,
              "feature_data": data, "pair_data": pairs, "edge_keys": tuple(edge_keys),
              "shell_feature": shell_feature, "shell_modes": tuple(sorted(shell_modes)),
              "minimum_distinct_gap_lower": min(distinct_gaps),
              "minimum_complement_shell_gap_lower": min(resolvent_gaps),
              "exact_equal_edges": equal_edges, "root_boxes": (dbox, obox),
              "root_box": {"d": dbox, "o": obox,
                           "center": owned["root_center"], "radius": owned["root_radius"]},
              "metadata": {"status": "rigorous_scalar_weights_only_not_inertia",
                           "interval_precision_decimal_digits": DPS,
                           "momenta": len(modes), "feature_groups": len(data),
                           "unordered_feature_pairs": len(pairs),
                           "exact_equal_feature_directed_edges": equal_edges,
                           "Fock_states_per_mode": FOCK, "occupied_shell_states": REFERENCE,
                           "minimum_distinct_gap_lower": _decimal(min(distinct_gaps), ROUND_FLOOR),
                           "all_Z_terms_and_signed_ground_retained": True},
              "source_pins": dict(PINS), "precision_decimal_digits": DPS,
              "seconds": time.perf_counter()-start}
    for name in ("lambda", "sqrt_lambda", "kappa", "derivative", "rho", "chi", "resolvent"):
        result[name] = tuple(data[f][name] for f in features)
    for name in ("dd", "gamma_J", "weight_X"):
        result[name] = tuple(pairs[key][name] for key in edge_keys)
    return result


def _summary(values):
    endpoints = [bounds(value) for value in values]
    return {"minimum_lower": _decimal(min(lower for lower, _ in endpoints), ROUND_FLOOR),
            "maximum_upper": _decimal(max(upper for _, upper in endpoints), ROUND_CEILING),
            "maximum_width_upper": _decimal(max(upper-lower for lower, upper in endpoints), ROUND_CEILING)}


def run(repo=None):
    result = spectral_intervals(repo)
    serialized_features = [{"feature": f, "count": row["count"],
                            **{name: interval_record(row[name]) for name in
                               ("lambda", "sqrt_lambda", "kappa", "derivative", "rho", "chi", "resolvent")}}
                           for f, row in sorted(result["feature_data"].items())]
    serialized_pairs = [{"features": key, **{name: interval_record(row[name])
                                            for name in ("dd", "gamma_J", "weight_X", "energy_gap")}}
                       for key, row in sorted(result["pair_data"].items())]
    digest = hashlib.sha256(json.dumps({"features": serialized_features, "pairs": serialized_pairs},
                                      sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"schema": "d0-native-full-symbol-interval-scalar-weights/1",
            "status": "PASS_RIGOROUS_SCALAR_ENCLOSURES_NOT_INERTIA",
            "seconds": round(result["seconds"], 4), "mpmath_version": mpmath.__version__,
            "interval_precision_decimal_digits": DPS,
            "source_pins": PINS,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "root_d_o_boxes_exact_decimal": result["root_boxes"], "q": Q,
            "scalar_constants": {name: interval_record(result[name]) for name in
                                 ("d", "o", "a", "b", "alpha", "beta", "fugacity", "Z", "epsilon")},
            "momenta": len(result["modes"]), "feature_groups": len(result["feature_data"]),
            "unordered_feature_pairs": len(result["pair_data"]),
            "directed_exact_equal_feature_edges": result["exact_equal_edges"],
            "Fock_states_per_mode": FOCK, "occupied_shell_modes": len(result["shell_modes"]),
            "occupied_shell_states": len(result["shell_modes"])*FOCK,
            "signed_ground_resolvent": interval_record(result["resolvent"][0]),
            "minimum_distinct_energy_gap_lower": _decimal(result["minimum_distinct_gap_lower"], ROUND_FLOOR),
            "minimum_complement_shell_gap_lower": _decimal(result["minimum_complement_shell_gap_lower"], ROUND_FLOOR),
            "weight_and_energy_summary": {name: _summary(result[name]) for name in
                                          ("lambda", "sqrt_lambda", "kappa", "resolvent", "dd", "gamma_J", "weight_X")},
            "outward_decimal_interval_payload_sha256": digest,
            "binary64_export": "float_bounds expands exact Fraction endpoints one ulp outward",
            "equal_energy_branch": "exact feature equality only; analytic fixed-Z derivative",
            "distinct_energy_branch": "interval quotient only after exact-feature gap excludes zero",
            "nonzero_q_has_no_diagonal_momentum_block": True,
            "full_Z_all4096_times16_retained": True,
            "kernel_or_inertia_certified": False, "physical_admission_or_GR_claim": False,
            "old_run_root_solve_or_receipt_write": False}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
