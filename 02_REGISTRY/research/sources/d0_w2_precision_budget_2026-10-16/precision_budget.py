#!/usr/bin/env python3
"""Sufficient h^{-2} raw-l1 error budget on one declared interface.

Candidate arithmetic only. A passing budget is not a native refining
solution and does not derive general relativity. Physical scales
beta, alpha, t, z, M stay inputs. The program chooses only a return
depth and auxiliary tolerances.

The v8 price and the central-terminal AF price are different programs.
Their bounds are never added.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import subprocess
from pathlib import Path


INTERFACE = "unweighted_raw_l1_h_minus_2"
PARENT_SLOTS = 10
HISTORICAL_WITNESS_SLOTS = 6
V8_PROGRAM = "v8"
CENTRAL_PROGRAM = "central_terminal_af"
N08_TASK = "WRK-A4D-WEIGHTED-SITE-SOURCE-TRANSFER"
N08_PATH = "02_REGISTRY/research/sources/d0_w2_weighted_source_2026-10-16/"
N05_PATH = "02_REGISTRY/research/sources/d0_w2_stored_tangent_2026-10-16/stored_tangent.py"
N06_PATH = "02_REGISTRY/research/sources/d0_w2_matter_response_2026-10-16/matter_response.py"
N07_PATH = "02_REGISTRY/research/sources/d0_w2_hessian_apply_2026-10-16/hessian_apply.py"
PAIRING = "real_fourier_pairing_plus_traceless_hermitian_shell"
HISTORICAL_SOURCE = "74e62cdc716e10883accba9d34ccf0e21d58eb65"
JOINT_SOURCE = "33267713b2e6d3e78af7789547b00f50cdceb43d"

REPO = Path(__file__).resolve().parents[4]


class BudgetRefusal(Exception):
    def __init__(self, map_name, detail=""):
        self.map_name = map_name
        self.detail = detail
        super().__init__("%s: %s" % (map_name, detail))

    def payload(self):
        body = {
            "verdict": "REFUSE",
            "map": self.map_name,
            "detail": self.detail,
            "interface": INTERFACE,
            "native_refining_solutions_proved": False,
            "gr_derived": False,
            "programs_added": False,
        }
        return body


def F(value):
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, str):
        return Fraction(value)
    raise BudgetRefusal("non_rational_scale", "scale %r is not an exact rational" % (value,))


def show(value):
    if isinstance(value, Fraction):
        return "%s/%s" % (value.numerator, value.denominator)
    return str(value)


def integer_sqrt(n):
    if n < 0:
        raise BudgetRefusal("negative_square", "integer square root of a negative")
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 1) // 2)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def perfect_sqrt(n):
    root = integer_sqrt(n)
    if root * root == n:
        return root
    return None


def rational_sqrt(value):
    value = F(value)
    if value < 0:
        raise BudgetRefusal("negative_square", "rational square root of a negative")
    if value == 0:
        return Fraction(0)
    num = perfect_sqrt(value.numerator)
    den = perfect_sqrt(value.denominator)
    if num is None or den is None:
        raise BudgetRefusal(
            "hs_conversion_not_exact",
            "square root of %s is not rational; the budget does not drop it" % show(value),
        )
    return Fraction(num, den)


def sqrt5_bounds(denominator=10**6):
    """Rational bounds n/d <= sqrt(5) < (n+1)/d proved by integer squares."""
    den = int(denominator)
    target = 5 * den * den
    n = integer_sqrt(target)
    if n * n > target or (n + 1) * (n + 1) <= target:
        raise BudgetRefusal("sqrt5_enclosure_failed", "integer square root missed sqrt(5)")
    return Fraction(n, den), Fraction(n + 1, den)


def v8_calibration_enclosure(denominator=10**6):
    """Sufficient rational enclosure of the fixed v8 constants.

    beta = 2 p^2 = 3 - sqrt(5), b0 = p^3 = sqrt(5) - 2, z = 2^{-20}, M = 128.
    beta_upper uses the smaller square-root bound because beta subtracts sqrt(5).
    b0_lower uses the same smaller bound. Neither quantity is a function of h.
    """
    lower, upper = sqrt5_bounds(denominator)
    beta_upper = 3 - lower
    b0_lower = lower - 2
    if b0_lower <= 0 or beta_upper <= 0:
        raise BudgetRefusal("v8_enclosure_not_positive", "denominator too coarse")
    return {
        "sqrt5_lower": lower,
        "sqrt5_upper": upper,
        "beta_upper": beta_upper,
        "b0_lower": b0_lower,
        "z": Fraction(1, 2**20),
        "M": 128,
        "workspace_C": 128,
        "fock_multiplicity": 16,
        "length_ell": Fraction(1, 8),
        "length_ell_is_field": False,
        "rounds": 8192,
    }


class Golden:
    """Element a + b p of Z[p], p = (sqrt(5)-1)/2, p^2 = 1 - p."""

    __slots__ = ("a", "b")

    def __init__(self, a, b):
        self.a = F(a)
        self.b = F(b)

    def __mul__(self, other):
        if not isinstance(other, Golden):
            other = Golden(other, 0)
        a, b, c, d = self.a, self.b, other.a, other.b
        return Golden(a * c + b * d, a * d + b * c - b * d)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if not isinstance(other, Golden):
            other = Golden(other, 0)
        return Golden(self.a + other.a, self.b + other.b)

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        return "Golden(%s, %s)" % (show(self.a), show(self.b))

    def inverse(self):
        norm = self.a * self.a - self.a * self.b - self.b * self.b
        if norm == 0:
            raise BudgetRefusal("golden_zero_inverse", "zero element in Q(p)")
        return Golden((self.a - self.b) / norm, (-self.b) / norm)

    def to_sqrt5(self):
        """Return (u, v) with value = u + v sqrt(5)."""
        return (2 * self.a - self.b) / 2, self.b / 2

    def rational_upper(self, sqrt5_lower, sqrt5_upper):
        u, v = self.to_sqrt5()
        if v >= 0:
            return u + v * sqrt5_upper
        return u + v * sqrt5_lower


def p_pow(n):
    if n == 0:
        return Golden(1, 0)
    if n < 0:
        return p_pow(-n).inverse()
    result = Golden(1, 0)
    base = Golden(0, 1)
    exp = n
    while exp:
        if exp & 1:
            result = result * base
        base = base * base
        exp >>= 1
    return result


def artanh_upper(u, terms):
    """Upper bound of artanh(u) for rational u in (0, 1).

    The positive-term remainder after ``terms`` summands is
    < u^{2 terms + 1} / ((2 terms + 1) (1 - u^2)).
    """
    u = F(u)
    if not (0 < u < 1):
        raise BudgetRefusal("artanh_domain", "u must lie in (0, 1)")
    total = Fraction(0)
    power = u
    for n in range(terms):
        total += power / (2 * n + 1)
        power *= u * u
    remainder = power / ((2 * terms + 1) * (1 - u * u))
    return total + remainder


def artanh_lower(u, terms):
    u = F(u)
    total = Fraction(0)
    power = u
    for n in range(terms):
        total += power / (2 * n + 1)
        power *= u * u
    return total


def af_ell_bounds():
    """Certified rational bounds of ell = log(phi), distinct from v8 length 1/8.

    u = sqrt(5) - 2 = (phi - 1)/(phi + 1), and log(phi) = 2 artanh(u).
    682/305 < sqrt(5) < 161/72, hence 72/305 < u < 17/72.
    """
    if 682 * 682 >= 5 * 305 * 305:
        raise BudgetRefusal("sqrt5_enclosure_failed", "682/305 is not a lower bound")
    if 161 * 161 <= 5 * 72 * 72:
        raise BudgetRefusal("sqrt5_enclosure_failed", "161/72 is not an upper bound")
    u_lower = Fraction(72, 305)
    u_upper = Fraction(17, 72)
    lower = 2 * artanh_lower(u_lower, 8)
    upper = 2 * artanh_upper(u_upper, 8)
    if not (Fraction(1, 8) < lower < upper < Fraction(1, 2)):
        raise BudgetRefusal("af_ell_enclosure_failed", "log(phi) enclosure left its known range")
    return {"lower": lower, "upper": upper, "v8_length_ell": Fraction(1, 8)}


def raw_l1_from_pointwise(h, slots, pointwise):
    """h^{-2} * L^4 * slots * pointwise, with L = 1/h.

    The identity h^{-2} * h^{-4} = h^{-6} is exact. It is not a volume norm.
    """
    h = F(h)
    pointwise = F(pointwise)
    if h <= 0:
        raise BudgetRefusal("mesh_step_not_positive", "h must be positive")
    return slots * pointwise / (h ** 6)


def historical_boundary_value(h, slots=HISTORICAL_WITNESS_SLOTS, coefficient=1):
    """Pointwise coefficient * h^6 sums to a constant after h^{-2} raw l1.

    The published six-slot witness gives exactly 6, for every h = 1/L.
    That constant is O(1), not o(1). The volume norm of the same data is
    slots * coefficient * h^4 and is a different program.
    """
    h = F(h)
    pointwise = F(coefficient) * (h ** 6)
    return raw_l1_from_pointwise(h, slots, pointwise)


def volume_normalized_reading(h, slots, pointwise):
    """Cell-volume multiple of the raw target: raw_l1 * h^4.

    The certificate at 74e62cdc sets this reading to h^4 times the raw gap.
    For six slots of size h^6 the raw gap is 6, so the reading is 6 h^4.
    It tends to 0 and is not the parent raw target.
    """
    return raw_l1_from_pointwise(h, slots, pointwise) * (F(h) ** 4)


def mesh_length(h):
    h = F(h)
    if h <= 0 or h > 1 or h.numerator != 1:
        raise BudgetRefusal(
            "mesh_step_not_reciprocal_integer",
            "parent carrier requires h = 1/L for a positive integer L",
        )
    return h.denominator


def _rate(coefficient, exponent):
    return {"coefficient": F(coefficient), "exponent": int(exponent)}


def _rate_at(rate, h):
    return F(rate["coefficient"]) * (F(h) ** int(rate["exponent"]))


def choose_eps_h(allowance, beta, b0, d_op):
    """Largest exact eps_H whose H-channel equals ``allowance`` at these scales.

    eps_H is a computational tolerance. beta and b0 are not changed.
    """
    allowance = F(allowance)
    beta = F(beta)
    b0 = F(b0)
    d_op = F(d_op)
    if allowance < 0:
        raise BudgetRefusal("negative_allowance", "gap allowance is negative")
    if allowance == 0 or d_op == 0:
        return Fraction(0)
    if beta <= 0 or b0 <= 0:
        raise BudgetRefusal(
            "fixed_alpha_lambda_bound",
            "fixed-alpha bound (13) needs beta > 0 and b0 > 0",
        )
    return allowance ** 2 * b0 ** 2 / (2 * beta * d_op ** 2)


def choose_eps_j(allowance, q, M, z, beta, d_hs):
    allowance = F(allowance)
    q = F(q)
    z = F(z)
    beta = F(beta)
    d_hs = F(d_hs)
    if allowance < 0:
        raise BudgetRefusal("negative_allowance", "gap allowance is negative")
    if allowance == 0 or z == 0 or d_hs == 0:
        return Fraction(0)
    if q <= 0 or M <= 0 or beta <= 0 or not (0 <= z < 1):
        raise BudgetRefusal(
            "auxiliary_gap_domain",
            "J-channel needs q > 0, M > 0, beta > 0 and 0 <= z < 1",
        )
    return (
        allowance ** 2
        * (1 - z) ** 2
        / (q ** 2 * 2 * M * z ** 2 * beta ** 2 * d_hs ** 2)
    )


def gap_channels(eps_h, eps_j, beta, b0, d_op, q, M, z, d_hs):
    """Scalar (12)+(13) split into the two auxiliary channels.

    The returned values equal the allowances when eps was chosen from them.
    Squared comparisons avoid an extra radical: the identity
    2 beta eps_H D_op^2 = allowance_H^2 b0^2 is the H-channel.
    """
    eps_h = F(eps_h)
    eps_j = F(eps_j)
    beta = F(beta)
    b0 = F(b0)
    d_op = F(d_op)
    q = F(q)
    z = F(z)
    d_hs = F(d_hs)
    if eps_h == 0 or d_op == 0:
        channel_h = Fraction(0)
    else:
        channel_h = d_op * rational_sqrt(2 * beta * eps_h) / b0
    if eps_j == 0 or z == 0 or d_hs == 0:
        channel_j = Fraction(0)
    else:
        channel_j = q * rational_sqrt(2 * M * eps_j) * (z * beta / (1 - z)) * d_hs
    return channel_h, channel_j


def choose_return_depth(allowance, M, beta, z, delta_1, max_depth=100000):
    """Smallest k >= 0 with the trace-norm feedback (15) at most ``allowance``.

    z is not replaced by a function of h. If no such k exists inside the
    guard, the depth is unreachable.
    """
    allowance = F(allowance)
    z = F(z)
    beta = F(beta)
    delta_1 = F(delta_1)
    if not (0 <= z < 1):
        raise BudgetRefusal("return_tail_domain", "return tail requires 0 <= z < 1")
    if allowance < 0:
        raise BudgetRefusal("negative_allowance", "tail allowance is negative")
    if delta_1 == 0 or M == 0 or beta == 0 or z == 0:
        return 0
    factor = M * beta * delta_1 / (1 - z)
    power = z ** 2
    k = 0
    while factor * power > allowance:
        k += 1
        if k > max_depth:
            raise BudgetRefusal(
                "return_depth_unreachable",
                "fixed z does not meet the tail allowance",
            )
        power *= z
    return k


def tail_scalar(k, M, beta, z, delta_1):
    z = F(z)
    if not (0 <= z < 1):
        raise BudgetRefusal("return_tail_domain", "return tail requires 0 <= z < 1")
    if k < 0:
        raise BudgetRefusal("return_tail_domain", "depth k is negative")
    return M * F(beta) * (z ** (k + 2)) * F(delta_1) / (1 - z)


def euler_to_target(h, slots, c_w, scalar):
    """Right-inverse l1 lift of one slotwise scalar, then h^{-2} raw sum.

    ||e||_raw,1 <= C_W * (sites * slots * scalar), sites = h^{-4}.
    """
    return F(c_w) * raw_l1_from_pointwise(h, slots, scalar)


def source_to_target(h, slots, pointwise):
    """Defect already in the reconstructed packed slots. No second C_W."""
    return raw_l1_from_pointwise(h, slots, pointwise)


def effective_power(rate_exponent, dimension_exponent=0):
    """Numerator of the raw-target power of h, in halves.

    Slot size carries h^{rate + dimension/2}. The raw target multiplies by
    h^{-6}. Vanishing needs the resulting exponent to be positive.
    The integer returned is twice that exponent.
    """
    return 2 * (int(rate_exponent) - 6) + int(dimension_exponent)


def tends_to_zero(power_twice, coefficient):
    if F(coefficient) == 0:
        return True
    return power_twice > 0


def refusal_power_map(power_twice):
    if power_twice == 0:
        return "pointwise_h6_after_raw_sum"
    if power_twice < 0:
        return "pointwise_coarser_than_h6_raw_sum"
    return None


def schatten_scales(d_op, dimension, dimension_exponent, drop_dimension):
    """HS and trace-norm lifts. The dimension factor is part of the predicate."""
    if drop_dimension:
        raise BudgetRefusal(
            "hs_bound_independent_of_dimension",
            "an HS or trace bound of a field perturbation keeps its dimension",
        )
    dimension = int(dimension)
    if dimension <= 0:
        raise BudgetRefusal("hs_dimension_missing", "fibre dimension must be positive")
    if int(dimension_exponent) % 2 != 0:
        raise BudgetRefusal(
            "hs_conversion_not_exact",
            "dimension exponent must be even so the square root stays exact",
        )
    root = rational_sqrt(dimension)
    # ||A||_HS <= sqrt(dim) ||A||_op, ||A||_1 <= dim ||A||_op.
    return {
        "D_op": F(d_op),
        "D_hs": root * F(d_op),
        "Delta_1": dimension * F(d_op),
        "sqrt_dimension": root,
        "dimension": dimension,
        "dimension_exponent": int(dimension_exponent),
        "hs_factor": "sqrt(dimension)",
        "trace_factor": "dimension",
    }


def right_inverse_constant(spec):
    kind = spec.get("inverse_kind")
    if not spec.get("right_inverse_supplied"):
        raise BudgetRefusal(
            "missing_right_inverse",
            "source reflection needs an actual right inverse; none was supplied",
        )
    if kind == "left":
        raise BudgetRefusal(
            "left_inverse_is_not_right_inverse",
            "a left inverse does not reflect the covector",
        )
    if kind != "right":
        raise BudgetRefusal("missing_right_inverse", "inverse kind must be right")
    source = spec.get("constant_source", "input")
    if source == "28/s":
        if spec.get("neumann_ball") is not True:
            raise BudgetRefusal(
                "twenty_eight_over_s_without_neumann_ball",
                "28/s is only the Neumann bound inside ||F_Y-F0||_inf <= s/28",
            )
        price_s = F(spec.get("price_s"))
        if price_s <= 0:
            raise BudgetRefusal("neumann_scale_not_positive", "price scale s must be positive")
        return Fraction(28) / price_s
    if source != "input":
        raise BudgetRefusal("unknown_right_inverse_constant", source)
    constant = F(spec.get("C_W"))
    if constant < 0:
        raise BudgetRefusal("negative_right_inverse_constant", "C_W must be nonnegative")
    return constant


def _base_guards(spec, program):
    if spec.get("rescue") == "beta(h)":
        raise BudgetRefusal("beta_of_h_rescue", "beta(h) is not chosen to meet the target")
    if spec.get("rescue") == "alpha(h)":
        raise BudgetRefusal("alpha_of_h_rescue", "alpha(h) is not chosen to meet the target")
    if spec.get("rescue") == "t(h)":
        raise BudgetRefusal("t_of_h_rescue", "t(h) is not chosen to meet the target")
    if spec.get("compose_with_other_price"):
        raise BudgetRefusal(
            "v8_plus_central_price",
            "v8 and central-terminal AF bounds are not summands",
        )
    if spec.get("source_fitted_to_solution"):
        raise BudgetRefusal("fitted_source_rejected", "the comparator source is an input")
    if spec.get("weight_law") == "endogenous_moving":
        raise BudgetRefusal(
            "n08_endogenous_weight_conditional",
            "moving site weights stay the conditional input %s at %s; this budget does not wait for it"
            % (N08_TASK, N08_PATH),
        )
    if spec.get("weight_law") != "fixed_counting":
        raise BudgetRefusal("unknown_weight_law", "weight law must be fixed_counting or endogenous_moving")
    if program == V8_PROGRAM and spec.get("operator_family") not in (None, "v8"):
        raise BudgetRefusal("operator_family_is_not_v8", "this budget does not absorb another price")
    if spec.get("invert_lower_block"):
        raise BudgetRefusal(
            "lower_block_is_not_inverted",
            "the shell block of [H_red, T*; T, 0] is zero",
        )


def _fixed_calibration_guards(spec):
    if spec.get("beta_depends_on_h"):
        raise BudgetRefusal(
            "fixed_beta_bound_versus_beta_of_h",
            "the unfolding tail and gap use one input beta, not beta(h)",
        )
    if spec.get("alpha_depends_on_h"):
        raise BudgetRefusal(
            "fixed_alpha_unfolding_versus_alpha_of_h",
            "fixed-alpha bound (13) does not accept alpha(h)",
        )
    if spec.get("t_depends_on_h") or spec.get("z_depends_on_h"):
        raise BudgetRefusal(
            "fixed_z_tail_versus_t_of_h",
            "the return tail uses one input z, not t(h) or z(h)",
        )
    if int(spec.get("declared_multiplicity")) != int(spec.get("M")):
        raise BudgetRefusal(
            "multiplicity_mismatch",
            "declared multiplicity %s is not the M=%s used in the formula"
            % (spec.get("declared_multiplicity"), spec.get("M")),
        )
    if "feedback_multiplicity" in spec and int(spec["feedback_multiplicity"]) != int(spec["M"]):
        raise BudgetRefusal(
            "multiplicity_mismatch",
            "feedback multiplicity is M, not a substitute fock or shell rank",
        )


def _gq_contribution(spec, h, slots, c_w):
    if not spec.get("include_gq"):
        return None
    if spec.get("use_gq_as_hessian_inverse"):
        raise BudgetRefusal(
            "gq_is_not_field_shell_hessian_inverse",
            "||G_Q||<4 is not invertibility of the field/shell Hessian",
        )
    if spec.get("use_gq_as_spatial_refinement"):
        raise BudgetRefusal(
            "gq_does_not_give_spatial_refinement",
            "the constant 4 does not give spatial refinement",
        )
    record, tail = _owned_gq(
        spec.get("delta_op_norm", 0),
        spec.get("epsilon_shift", 0),
        spec.get("gap_exceeds_certified"),
        spec.get("gq_order", 0),
        spec.get("gq_contraction", Fraction(1, 3)),
    )
    if record.get("gq_strict_upper") is None or not record.get("window_open"):
        raise BudgetRefusal(
            "gq_outside_declared_window",
            "||G_Q||<4 is not claimed outside the open window",
        )
    if "gq_to_slot" not in spec:
        raise BudgetRefusal(
            "gq_slot_lipschitz_missing",
            "an operator-norm tail is not yet a raw slot",
        )
    # The constant 4 stays inside the owned Neumann comparison. The slot
    # defect uses the exact tail, not 4 as a Hessian norm.
    pointwise = F(spec["gq_to_slot"]) * tail["exact_tail"]
    target = euler_to_target(h, slots, c_w, pointwise)
    return {
        "name": "gq_neumann_tail",
        "domain": "||Delta-Delta0||<1/8, |epsilon-epsilon0|<1/8, certified gap > 1/2, t<1/2",
        "norm": "operator norm of the complement resolvent, then packed-slot l1",
        "add_predicate": "window_open and gq_to_slot supplied; not a Hessian inverse; not spatial refinement",
        "field_inverse_estimated": False,
        "spatial_refinement": False,
        "gq_strict_upper": record["gq_strict_upper"],
        "exact_tail": show(tail["exact_tail"]),
        "uniform_tail": show(tail["uniform_tail"]),
        "contribution": target,
        "added": True,
        "power_twice": effective_power(0) if pointwise != 0 else 1,
        "coefficient": pointwise,
    }


def _owned_gq(delta_op, epsilon_shift, gap_certified, order, contraction):
    matter = _load_matter()
    record = matter.uniform_shell_complement_bound(
        delta_op, epsilon_shift, gap_exceeds_certified=gap_certified
    )
    if record.get("gq_strict_upper") is None:
        return record, None
    tail = matter.neumann_tail_bound(int(order), F(contraction))
    if not tail["strict"]:
        raise BudgetRefusal("gq_tail_not_strict", "owned tail comparison failed")
    return record, tail


def _load_module(module_name, path):
    import importlib.util
    import sys

    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    # Python 3.9 dataclasses read the module from sys.modules during exec.
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def _load_matter():
    return _load_module("matter_response_budget", REPO / N06_PATH)


def _load_tangent():
    return _load_module("stored_tangent_budget", REPO / N05_PATH)


def _load_hessian():
    return _load_module("hessian_apply_budget", REPO / N07_PATH)


def native_chart_gate():
    """N05 regular chart versus the flat control. Not an Euler kernel."""
    import sympy as s

    tangent = _load_tangent()
    frame = tangent.homogeneous_frame(s.Rational(1, 4), s.Rational(1, 125))
    rho2 = s.simplify(frame.rho2[0])
    if rho2 != s.Rational(3, 15625):
        raise BudgetRefusal("n05_chart_value_changed", "rational frame rho_0^2 is not 3/15625")
    flat_rejected = False
    try:
        tangent.homogeneous_frame(1, 0)
    except tangent.ChartSingular:
        flat_rejected = True
    if not flat_rejected:
        raise BudgetRefusal("n05_chart_singular", "flat frame was accepted")
    return {
        "chart": "n05_stored_tangent",
        "rational_frame": "a=1/4, b=1/125",
        "rho0_squared": "3/15625",
        "flat_frame_rejected": True,
        "return_group": "SO(3)",
        "so4_return_admitted": False,
        "physical_native_admission": False,
    }


def native_calibration_gate():
    """N07 fixed v8 calibrations. ell = 1/8 is not a field and not AF log(phi)."""
    import sympy as s

    hessian = _load_hessian()
    cal = hessian.v8_calibrations()
    beta = s.simplify(cal["beta"] - (3 - s.sqrt(5)))
    b0 = s.simplify(cal["b0"] - (s.sqrt(5) - 2))
    if beta != 0 or b0 != 0:
        raise BudgetRefusal("v8_calibration_identity_failed", "beta or b0 left the fixed v8 value")
    if cal["fugacity"] != s.Rational(1, 2**20):
        raise BudgetRefusal("v8_calibration_identity_failed", "z is not 2^{-20}")
    if cal["feedback_multiplicity"] != 128 or cal["ell"] != s.Rational(1, 8):
        raise BudgetRefusal("v8_calibration_identity_failed", "M or length ell moved")
    if cal["ell_is_field"] or cal["af_preparation_second_variation_added"]:
        raise BudgetRefusal("v8_calibration_identity_failed", "calibration flags changed")
    return {
        "beta": "3-sqrt(5)",
        "b0": "sqrt(5)-2",
        "z": "1/1048576",
        "M": 128,
        "length_ell": "1/8",
        "af_preparation_added": False,
        "lower_block_inverted": False,
        "pairing": PAIRING,
    }


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_blob(sha, path):
    return subprocess.check_output(
        ["git", "rev-parse", "%s:%s" % (sha, path)],
        cwd=REPO,
        text=True,
    ).strip()


def provenance():
    return {
        "historical_source": HISTORICAL_SOURCE,
        "joint_source": JOINT_SOURCE,
        "blobs": {
            "unfolding": git_blob(
                HISTORICAL_SOURCE,
                "02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md",
            ),
            "central": git_blob(
                HISTORICAL_SOURCE,
                "02_REGISTRY/research/A4D_CENTRAL_RECORD_VARIATIONAL_EQUIVALENCE.md",
            ),
            "transport": git_blob(
                HISTORICAL_SOURCE,
                "02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md",
            ),
            "price_metric": git_blob(
                HISTORICAL_SOURCE,
                "02_REGISTRY/research/A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md",
            ),
            "joint": git_blob(
                JOINT_SOURCE,
                "02_REGISTRY/research/A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md",
            ),
        },
        "sha256": {
            "n05": file_sha256(REPO / N05_PATH),
            "n06": file_sha256(REPO / N06_PATH),
            "n07": file_sha256(REPO / N07_PATH),
        },
        "n08_conditional": {"task": N08_TASK, "path": N08_PATH, "merged": False},
    }


def _term(name, domain, norm, predicate, contribution, added, power_twice, coefficient, extra=None):
    record = {
        "name": name,
        "domain": domain,
        "norm": norm,
        "add_predicate": predicate,
        "contribution": show(contribution) if isinstance(contribution, Fraction) else contribution,
        "added": added,
        "power_twice": power_twice,
        "coefficient": show(coefficient) if isinstance(coefficient, Fraction) else coefficient,
    }
    if extra:
        record.update(extra)
    return record


def evaluate_v8(spec):
    """One v8 budget in the parent raw target, or a named refusal.

    ``spec`` carries input scales and assumed rates. Depth k and the
    auxiliary tolerances are chosen. A PASS verdict means the sufficient
    bound tends to 0. It does not assert that a refining solution exists.
    """
    _base_guards(spec, V8_PROGRAM)
    _fixed_calibration_guards(spec)
    if spec.get("norm") == "volume":
        raise BudgetRefusal(
            "volume_norm_is_not_raw_l1",
            "the volume reading of the six-slot witness tends to 0 while the raw target stays constant",
        )
    if int(spec.get("slots", PARENT_SLOTS)) != PARENT_SLOTS:
        raise BudgetRefusal(
            "slot_count_is_not_parent_packed_rows",
            "the parent raw target has 10 packed metric rows",
        )
    if spec.get("return_group", "SO(3)") != "SO(3)":
        raise BudgetRefusal("n05_so4_return_rejected", "the stored-adjoint return is SO(3), not SO(4)")
    if spec.get("rho_positive") is False or spec.get("chart_regular") is False:
        raise BudgetRefusal("n05_chart_singular", "the N05 chart rejects rho = 0")
    q = F(spec.get("q", 1))
    if q < 1:
        raise BudgetRefusal("auxiliary_gap_domain", "q must be at least max(1, ||Y||_op)")

    h = F(spec["h"])
    length = mesh_length(h)
    slots = PARENT_SLOTS
    c_w = right_inverse_constant(spec)
    beta = F(spec["beta"])
    b0 = F(spec["b0"])
    z = F(spec["z"])
    M = int(spec["M"])
    if beta <= 0 or b0 <= 0 or not (0 <= z < 1) or M <= 0:
        raise BudgetRefusal("auxiliary_gap_domain", "beta, b0, z, M left the fixed-calibration domain")

    scales = schatten_scales(
        spec.get("D_op", 1),
        spec.get("hs_dimension", 16),
        spec.get("dimension_exponent", 0),
        spec.get("drop_dimension_factor", False),
    )
    # A growing fibre changes the slot power. The factor is kept, not cancelled.
    dim_power = int(scales["dimension_exponent"])

    if "lambda_min_hx" not in spec or "lambda_max_hx" not in spec:
        raise BudgetRefusal("observer_bounds_missing", "conditioning of h_x needs both eigenvalues")
    lambda_min = F(spec["lambda_min_hx"])
    lambda_max = F(spec["lambda_max_hx"])
    if lambda_min <= 0 or lambda_max < lambda_min:
        raise BudgetRefusal("observer_eigenvalue_order", "h_x must be positive definite")
    sqrt_min = rational_sqrt(lambda_min)
    kappa = lambda_max / lambda_min
    if "observer_to_slot" not in spec:
        raise BudgetRefusal(
            "observer_slot_lipschitz_missing",
            "kappa(h_x) is exposed and is not silently a raw slot",
        )

    operator = spec["operator_rate"]
    quadrature = spec["quadrature_rate"]
    observer = spec["observer_rate"]
    if operator.get("stage") != "reconstructed_source":
        raise BudgetRefusal(
            "operator_stage_undeclared",
            "operator rate must name its stage; euler residuals are not source slots",
        )
    if quadrature.get("stage") != "reconstructed_source":
        raise BudgetRefusal(
            "quadrature_stage_undeclared",
            "quadrature must already be in the packed slots, not a volume norm",
        )
    if observer.get("stage") != "euler_residual":
        raise BudgetRefusal(
            "observer_stage_undeclared",
            "the whitened observer defect is still an Euler residual",
        )

    # Chosen tolerances track the slowest positive assumed rate. They are
    # not the obstruction: eps and k can always be tightened at fixed beta.
    op_dim = dim_power if operator.get("uses_growing_dimension") else 0
    assumed_powers = []
    for rate, extra in (
        (operator, op_dim),
        (quadrature, 0),
        (observer, 0),
    ):
        if F(rate["coefficient"]) != 0:
            assumed_powers.append(effective_power(rate["exponent"], extra))
    if F(spec.get("remainder_pointwise", 0)) != 0:
        assumed_powers.append(effective_power(0))
    guide = min(assumed_powers) if assumed_powers else 2
    guide_power = guide // 2 if guide > 0 else 0
    allowance_target = h ** guide_power if guide > 0 else Fraction(1)
    if c_w == 0:
        raise BudgetRefusal(
            "missing_right_inverse",
            "C_W = 0 on a positive slot count is not an admitted right inverse here",
        )
    scalar_allowance = allowance_target * (h ** 6) / (c_w * slots)
    half = scalar_allowance / 2
    eps_h = choose_eps_h(half, beta, b0, scales["D_op"])
    eps_j = choose_eps_j(half, q, M, z, beta, scales["D_hs"])
    channel_h, channel_j = gap_channels(
        eps_h, eps_j, beta, b0, scales["D_op"], q, M, z, scales["D_hs"]
    )
    gap_one = channel_h + channel_j
    k = choose_return_depth(scalar_allowance, M, beta, z, scales["Delta_1"])
    tail_one = tail_scalar(k, M, beta, z, scales["Delta_1"])
    if tail_one > scalar_allowance:
        raise BudgetRefusal("return_depth_unreachable", "chosen depth missed its allowance")

    growth = h ** (op_dim // 2) if operator.get("uses_growing_dimension") else Fraction(1)
    op_pointwise = _rate_at(operator, h) * growth
    quad_pointwise = _rate_at(quadrature, h)
    obs_pointwise = (
        F(spec["observer_to_slot"])
        * _rate_at(observer, h)
        / (2 * sqrt_min)
    )
    remainder = F(spec.get("remainder_pointwise", 0))

    t_gap = euler_to_target(h, slots, c_w, gap_one)
    t_tail = euler_to_target(h, slots, c_w, tail_one)
    t_obs = euler_to_target(h, slots, c_w, obs_pointwise)
    t_rem = euler_to_target(h, slots, c_w, remainder)
    t_op = source_to_target(h, slots, op_pointwise)
    t_quad = source_to_target(h, slots, quad_pointwise)
    gq = _gq_contribution(spec, h, slots, c_w)

    common = (
        "program v8; unweighted (Z/LZ)^4; 10 packed rows; fixed counting weight; "
        "fixed beta, alpha, z, M; actual right inverse; N05 chart regular and SO(3); "
        "N06 window respected; lower saddle block not inverted"
    )
    terms = [
        _term(
            "auxiliary_gap",
            "interior unfolding: sigma trace 1, X>0, q>=max(1,||Y||_op), fixed alpha, b0>0, 0<=z<1",
            "scalar |dS[v]-partial_x L[v]| from (12)+(13), op on dLambda and HS on sandwiched dA",
            common + "; slot variations separate the packed rows; HS dimension factor retained",
            t_gap,
            True,
            effective_power(guide_power + 6) if guide > 0 else guide,
            gap_one,
            {"eps_H": show(eps_h), "eps_J": show(eps_j), "channel_H": show(channel_h), "channel_J": show(channel_j)},
        ),
        _term(
            "return_tail",
            "0<=z<1 fixed, X_k = sum_{j=0}^k z^j F^j, k chosen",
            "trace norm ||dDelta||_1 in feedback (15); operator norm (14) is not added raw",
            common + "; trace-norm factor dimension kept; z not replaced by t(h)",
            t_tail,
            True,
            effective_power(guide_power + 6) if guide > 0 else guide,
            tail_one,
            {"k": k, "op_tail_not_added": show(z ** (k + 1) / (1 - z))},
        ),
        _term(
            "operator_approximation",
            "assumed rate on the reconstructed packed source, N07 pairing %s" % PAIRING,
            "slotwise sup already after the right inverse",
            common + "; stage=reconstructed_source; coefficient is assumed, not fitted",
            t_op,
            True,
            effective_power(operator["exponent"], op_dim),
            op_pointwise,
            {"assumed_exponent": operator["exponent"], "assumed_coefficient": show(F(operator["coefficient"]))},
        ),
        _term(
            "coframe_observer",
            "h_x positive definite, lambda_min=%s, kappa=%s; N05 whitening" % (show(lambda_min), show(kappa)),
            "||d sqrt(h)[S]||_op <= ||S||_op / (2 sqrt(lambda_min)), then Euler residual",
            common + "; observer_to_slot supplied; kappa does not cancel h^{-6}",
            t_obs,
            True,
            effective_power(observer["exponent"]),
            obs_pointwise,
            {"kappa_hx": show(kappa), "sqrt_lambda_min": show(sqrt_min)},
        ),
        _term(
            "spatial_quadrature",
            "exact unweighted 4D raw sum; quadrature defect is an assumed slot rate, not an integral",
            "packed-slot sup, then h^{-2} raw l1",
            common + "; not the volume norm; not the central AF address quadrature",
            t_quad,
            True,
            effective_power(quadrature["exponent"]),
            quad_pointwise,
            {"assumed_exponent": quadrature["exponent"], "assumed_coefficient": show(F(quadrature["coefficient"]))},
        ),
        _term(
            "source_after_right_inverse",
            "IsRightInverse: L W = I, C_W=%s, constant source %s" % (show(c_w), spec.get("constant_source", "input")),
            "l1(e) <= C_W l1(a-r); the factor multiplies Euler residuals, the additive term is only r",
            common + "; left inverse rejected; 28/s only inside its Neumann ball",
            t_rem,
            True,
            effective_power(0) if remainder != 0 else 1,
            remainder,
            {"C_W": show(c_w), "factor_applied_to_euler_terms": True},
        ),
    ]
    if operator.get("uses_growing_dimension"):
        terms[2]["add_predicate"] += "; growing HS dimension retained"
    total = t_gap + t_tail + t_op + t_obs + t_quad + t_rem
    if gq is not None:
        terms.append(
            {key: (show(val) if isinstance(val, Fraction) else val) for key, val in gq.items()}
        )
        total += gq["contribution"]
        if F(gq["coefficient"]) != 0:
            assumed_powers.append(gq["power_twice"])

    vanishing = all(power > 0 for power in assumed_powers) if assumed_powers else True
    blocking = None
    for power in assumed_powers:
        if power <= 0:
            blocking = refusal_power_map(power)
            break
    if spec.get("require_vanishing", True) and not vanishing:
        payload = BudgetRefusal(
            blocking or "pointwise_h6_after_raw_sum",
            "converted pointwise rate is not o(h^6); the raw target does not tend to 0",
        ).payload()
        payload["bound_at_h"] = show(total)
        payload["vanishing"] = False
        payload["h"] = show(h)
        payload["program"] = V8_PROGRAM
        payload["pieces"] = {
            "gap": show(t_gap),
            "tail": show(t_tail),
            "operator": show(t_op),
            "observer": show(t_obs),
            "quadrature": show(t_quad),
            "remainder": show(t_rem),
        }
        return payload

    return {
        "verdict": "PASS",
        "map": None,
        "program": V8_PROGRAM,
        "interface": INTERFACE,
        "target_norm": "h^{-2} raw l1",
        "h": show(h),
        "L": length,
        "slots": slots,
        "bound": show(total),
        "vanishing": vanishing,
        "native_refining_solutions_proved": False,
        "gr_derived": False,
        "field_shell_hessian_inverted": False,
        "gq_spatial_refinement": False,
        "programs_added": False,
        "lower_block_inverted": False,
        "chosen": {"k": k, "eps_H": show(eps_h), "eps_J": show(eps_j)},
        "scales": {
            "beta": show(beta),
            "b0": show(b0),
            "z": show(z),
            "M": M,
            "q": show(q),
            "C_W": show(c_w),
            "D_op": show(scales["D_op"]),
            "D_hs": show(scales["D_hs"]),
            "Delta_1": show(scales["Delta_1"]),
            "hs_dimension": scales["dimension"],
            "kappa_hx": show(kappa),
            "sqrt_dimension": show(scales["sqrt_dimension"]),
        },
        "assumed_rates": {
            "operator": {"coefficient": show(F(operator["coefficient"])), "exponent": operator["exponent"], "stage": "reconstructed_source"},
            "quadrature": {"coefficient": show(F(quadrature["coefficient"])), "exponent": quadrature["exponent"], "stage": "reconstructed_source"},
            "observer": {"coefficient": show(F(observer["coefficient"])), "exponent": observer["exponent"], "stage": "euler_residual"},
            "remainder_pointwise": show(remainder),
            "D_op": show(scales["D_op"]),
        },
        "parametrized": (
            "T(h) <= C_W * slots * h^{-6} * (gap_one + tail_one + observer_pointwise + remainder)"
            " + slots * h^{-6} * (operator_pointwise + quadrature_pointwise)"
            " [+ C_W * slots * h^{-6} * gq_to_slot * exact_neumann_tail if the window predicate holds]"
        ),
        "terms": [
            {key: (show(val) if isinstance(val, Fraction) else val) for key, val in item.items()}
            for item in terms
        ],
        "pieces": {
            "gap": show(t_gap),
            "tail": show(t_tail),
            "operator": show(t_op),
            "observer": show(t_obs),
            "quadrature": show(t_quad),
            "remainder": show(t_rem),
        },
    }


def central_reading_majorant(c, lip, f_inf, sqrt5_lower, sqrt5_upper):
    k = (16 * c) // 17
    gap = c - k
    cell = 4 * F(lip) * p_pow(k // 8)
    address = 2 * F(f_inf) * p_pow(2 * gap - 4)
    total = cell + address
    return k, total.rational_upper(sqrt5_lower, sqrt5_upper)


def central_address_majorant(c, sqrt5_lower, sqrt5_upper):
    k = (16 * c) // 17
    value = 2 * p_pow(2 * (c - k) - 4)
    return value.rational_upper(sqrt5_lower, sqrt5_upper)


def central_source_majorant(c, db_inf, sqrt5_lower, sqrt5_upper):
    k = (16 * c) // 17
    gap = c - k
    value = (4 * p_pow(2 * gap - 4) + 2 * p_pow(2 * gap - 8)) * F(db_inf)
    return value.rational_upper(sqrt5_lower, sqrt5_upper)


def choose_central_depth(lip, f_inf, tolerance, sqrt5_lower, sqrt5_upper, max_depth=4000):
    tolerance = F(tolerance)
    if tolerance <= 0:
        raise BudgetRefusal("negative_allowance", "central tolerance must be positive")
    for c in range(1, max_depth + 1):
        _k, bound = central_reading_majorant(c, lip, f_inf, sqrt5_lower, sqrt5_upper)
        if bound <= tolerance:
            return c, bound
    raise BudgetRefusal("central_depth_unreachable", "declared central tolerance was not met at fixed lambda")


def lambda_formula_upper(B, R, s_gate, residual, sqrt5_lower, sqrt5_upper):
    """Upper bound of (5/(2 lambda)) ||r|| with lambda = 4 p^{12} / (B R s^4).

    1/lambda grows when B, R, s grow. Those scales stay inputs.
    """
    B, R, s_gate, residual = F(B), F(R), F(s_gate), F(residual)
    if B <= 0 or R <= 0 or s_gate <= 0:
        raise BudgetRefusal("central_lambda_not_positive", "B, R, s must be positive inputs")
    # lambda = 4 p^{12} / (B R s^4), so 5/(2 lambda) = 5 B R s^4 / (8 p^{12}).
    factor = 5 * B * R * (s_gate ** 4) / 8 * p_pow(-12)
    upper = factor.rational_upper(sqrt5_lower, sqrt5_upper)
    return upper * residual


def evaluate_central(spec):
    """Separate central-terminal AF budget. Not a raw-l1 transfer."""
    if spec.get("compose_with_v8") or spec.get("compose_with_other_price"):
        raise BudgetRefusal("v8_plus_central_price", "central and v8 bounds are not summands")
    if spec.get("rescue") in {"beta(h)", "alpha(h)", "t(h)", "lambda(h)"}:
        raise BudgetRefusal("lambda_of_h_rescue", "lambda, beta, t and alpha are not tuned to the target")
    if spec.get("transfer_to_raw_l1") and not spec.get("lead_link_proved"):
        raise BudgetRefusal(
            "central_to_raw_without_lead_link",
            "the prepared-address rate is not a v8 raw bound until the lead proves the link",
        )
    if spec.get("ell") == Fraction(1, 8) or spec.get("ell") == "1/8":
        raise BudgetRefusal(
            "v8_length_ell_is_not_af_log_phi",
            "AF ell is log(phi); v8 length ell = 1/8 is a different constant",
        )
    ell = af_ell_bounds()
    if "ell_upper" in spec and F(spec["ell_upper"]) <= ell["lower"]:
        raise BudgetRefusal("af_ell_upper_too_small", "declared ell upper is below log(phi)")
    if spec.get("apply_to_v8"):
        raise BudgetRefusal(
            "central_rate_on_v8_without_same_program",
            "the central rate is not applied to v8 without a same-program hypothesis",
        )
    lam = F(spec["lambda"])
    residual = F(spec["residual_dual"])
    if lam <= 0:
        raise BudgetRefusal("central_lambda_not_positive", "lambda must be a positive input")
    compiler = Fraction(5, 2) / lam * residual
    lower, upper = sqrt5_bounds(spec.get("sqrt5_denominator", 10**6))
    depth, reading = choose_central_depth(
        spec.get("Lip", 1),
        spec.get("f_inf", 1),
        spec["tolerance"],
        lower,
        upper,
    )
    k = (16 * depth) // 17
    address = central_address_majorant(depth, lower, upper)
    source = central_source_majorant(depth, spec.get("db_inf", 1), lower, upper)
    formula = None
    if spec.get("lambda_route"):
        formula = lambda_formula_upper(
            spec.get("B", 1),
            spec.get("R", 1),
            spec.get("s_gate", 1),
            residual,
            lower,
            upper,
        )
    return {
        "verdict": "PASS",
        "map": None,
        "program": CENTRAL_PROGRAM,
        "interface": "central_dual_and_address_l1",
        "target_norm": "dual norm of dQ, address l1, and Lipschitz reading; not h^{-2} raw l1",
        "transferred_to_raw_l1": False,
        "native_refining_solutions_proved": False,
        "gr_derived": False,
        "programs_added": False,
        "bound": {
            "compiler_dual": show(compiler),
            "address_l1": show(address),
            "source_l1": show(source),
            "reading": show(reading),
            "lambda_route_alternative": None if formula is None else show(formula),
        },
        "chosen": {"c": depth, "k": k},
        "assumed_rates": {
            "lambda": show(lam),
            "residual_dual": show(residual),
            "Lip": show(F(spec.get("Lip", 1))),
            "f_inf": show(F(spec.get("f_inf", 1))),
            "db_inf": show(F(spec.get("db_inf", 1))),
            "tolerance": show(F(spec["tolerance"])),
            "B": show(F(spec.get("B", 1))) if spec.get("lambda_route") else None,
            "R": show(F(spec.get("R", 1))) if spec.get("lambda_route") else None,
            "s_gate": show(F(spec.get("s_gate", 1))) if spec.get("lambda_route") else None,
        },
        "ell_af": {"lower": show(ell["lower"]), "upper": show(ell["upper"])},
        "parametrized": (
            "||dQ|| <= (5/(2 lambda)) ||r||; "
            "||Prob-mu||_1 <= 2 p^{2(c-k)-4}; "
            "reading <= 4 Lip p^{floor(k/8)} + 2 ||f||_inf p^{2(c-k)-4}; "
            "k=floor(16c/17)"
        ),
        "terms": [
            {
                "name": "lambda_compiler",
                "domain": "dA = lambda a dQ + r, dA=0, lambda>0 fixed on the declared domain",
                "norm": "the dual norm of that identity",
                "add_predicate": "same central program; not added to a v8 raw sum",
                "contribution": show(compiler),
                "added": True,
            },
            {
                "name": "prepared_address",
                "domain": "central faithful optimum, cost cut c, k=floor(16c/17), p the golden weight",
                "norm": "unnormalized address l1",
                "add_predicate": "central history readout only; not the v8 raw lattice sum",
                "contribution": show(address),
                "added": True,
            },
            {
                "name": "address_source_jet",
                "domain": "same cut, ||db||_inf an input, denominator kept",
                "norm": "address l1 of the first source jet",
                "add_predicate": "same central program and the same cut as the value error",
                "contribution": show(source),
                "added": True,
            },
            {
                "name": "lipschitz_reading",
                "domain": "child clocks of diameter <= 2 p^{floor(k/8)} on the address cube",
                "norm": "scalar test against Lebesgue on the address cube",
                "add_predicate": "Lip and ||f||_inf supplied; not a Lorentz volume and not raw l1",
                "contribution": show(reading),
                "added": True,
            },
        ],
    }


def compose_programs(left, right):
    programs = {left.get("program"), right.get("program")}
    if programs == {V8_PROGRAM, CENTRAL_PROGRAM} or left.get("compose_with_other_price") or right.get("compose_with_other_price"):
        raise BudgetRefusal("v8_plus_central_price", "no map adds a v8 bound to a central bound")
    raise BudgetRefusal("v8_plus_central_price", "composition of distinct price bounds is refused")


def replay_certificate(certificate, scales):
    """Recompute the tail at the frozen depth. A new multiplicity does not pass."""
    if int(scales["M"]) != int(certificate["M"]):
        raise BudgetRefusal(
            "multiplicity_mismatch",
            "frozen certificate M=%s does not match replay M=%s" % (certificate["M"], scales["M"]),
        )
    if scales.get("beta_depends_on_h"):
        raise BudgetRefusal(
            "fixed_beta_bound_versus_beta_of_h",
            "replaying a fixed-beta certificate against beta(h)",
        )
    value = tail_scalar(
        certificate["k"],
        scales["M"],
        scales["beta"],
        scales["z"],
        scales["Delta_1"],
    )
    if value != F(certificate["tail_scalar"]):
        raise BudgetRefusal("certificate_mismatch", "replayed tail does not match the frozen value")
    return {"verdict": "PASS", "map": None, "tail_scalar": show(value), "native_refining_solutions_proved": False, "gr_derived": False}


def v8_spec_from_enclosure(h, operator, quadrature, observer, **overrides):
    enc = v8_calibration_enclosure()
    spec = {
        "h": h,
        "slots": PARENT_SLOTS,
        "program": V8_PROGRAM,
        "weight_law": "fixed_counting",
        "operator_family": "v8",
        "return_group": "SO(3)",
        "chart_regular": True,
        "rho_positive": True,
        "right_inverse_supplied": True,
        "inverse_kind": "right",
        "constant_source": "input",
        "C_W": Fraction(3),
        "beta": enc["beta_upper"],
        "b0": enc["b0_lower"],
        "z": enc["z"],
        "M": enc["M"],
        "declared_multiplicity": enc["M"],
        "feedback_multiplicity": enc["M"],
        "q": 1,
        "D_op": 1,
        "hs_dimension": 16,
        "dimension_exponent": 0,
        "lambda_min_hx": 1,
        "lambda_max_hx": 4,
        "observer_to_slot": 1,
        "operator_rate": operator,
        "quadrature_rate": quadrature,
        "observer_rate": observer,
        "remainder_pointwise": 0,
        "require_vanishing": True,
        "include_gq": False,
        "beta_depends_on_h": False,
        "alpha_depends_on_h": False,
        "z_depends_on_h": False,
        "enclosure": {
            "beta_upper": show(enc["beta_upper"]),
            "b0_lower": show(enc["b0_lower"]),
            "note": "sufficient majorant of beta=3-sqrt(5) and b0=sqrt(5)-2; not a law beta(h)",
        },
    }
    spec.update(overrides)
    return spec


def published_v8_budget():
    """Numerical v8 budget at h=1/8. Rates below are ASSUMED."""
    spec = v8_spec_from_enclosure(
        Fraction(1, 8),
        _rate(1, 8),
        _rate(1, 8),
        _rate(1, 8),
    )
    spec["operator_rate"]["stage"] = "reconstructed_source"
    spec["quadrature_rate"]["stage"] = "reconstructed_source"
    spec["observer_rate"]["stage"] = "euler_residual"
    result = evaluate_v8(spec)
    result["assumed_rates_note"] = (
        "ASSUMED: operator and quadrature are 1 * h^8 on reconstructed slots; "
        "observer defect is 1 * h^8 in operator norm; D_op=1 on a fixed 16-dimensional fibre; "
        "C_W=3 is an input, not 28/s; beta and b0 are rational majorants of the fixed v8 constants"
    )
    return result


def published_v8_budget_second():
    """Second numerical v8 budget at h=1/16 with different ASSUMED rates."""
    spec = v8_spec_from_enclosure(
        Fraction(1, 16),
        _rate(Fraction(1, 2), 7),
        _rate(1, 8),
        _rate(Fraction(1, 2), 8),
        C_W=4,
        lambda_min_hx=1,
        lambda_max_hx=2,
        observer_to_slot=1,
    )
    spec["operator_rate"]["stage"] = "reconstructed_source"
    spec["quadrature_rate"]["stage"] = "reconstructed_source"
    spec["observer_rate"]["stage"] = "euler_residual"
    result = evaluate_v8(spec)
    result["assumed_rates_note"] = (
        "ASSUMED: operator (1/2) h^7 on reconstructed slots; quadrature 1 * h^8; "
        "observer (1/2) h^8; D_op=1; C_W=4; lambda_min(h_x)=1; same fixed v8 majorants"
    )
    return result


def published_central_budget():
    """Numerical central budget. Rates and lambda are ASSUMED. Not raw l1."""
    return evaluate_central(
        {
            "lambda": Fraction(1, 10),
            "residual_dual": Fraction(1, 100),
            "Lip": 1,
            "f_inf": 1,
            "db_inf": Fraction(1, 10),
            "tolerance": Fraction(1, 1000),
            "lambda_route": True,
            "B": 1,
            "R": 1,
            "s_gate": 1,
            "lead_link_proved": False,
            "transfer_to_raw_l1": False,
        }
    )


def main():
    v8_a = published_v8_budget()
    v8_b = published_v8_budget_second()
    central = published_central_budget()
    boundary = evaluate_v8(
        v8_spec_from_enclosure(
            Fraction(1, 8),
            {**_rate(1, 6), "stage": "reconstructed_source"},
            {**_rate(0, 8), "stage": "reconstructed_source"},
            {**_rate(0, 8), "stage": "euler_residual"},
        )
    )
    report = {
        "v8_h_1_over_8": v8_a,
        "v8_h_1_over_16": v8_b,
        "central": central,
        "boundary_h6": boundary,
        "historical_six_slot": show(historical_boundary_value(Fraction(1, 8))),
        "native_refining_solutions_proved": False,
        "gr_derived": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if v8_a["verdict"] != "PASS" or v8_b["verdict"] != "PASS" or central["verdict"] != "PASS":
        return 1
    if boundary["verdict"] == "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
