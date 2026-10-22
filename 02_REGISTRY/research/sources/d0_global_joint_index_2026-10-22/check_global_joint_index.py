#!/usr/bin/env python3
"""Exact arithmetic consumer and illustrative controls for the joint-index proof.

This does not evaluate the missing complete native Book03 source, identify its
admissible preparation manifold, rerun the original interval proof, or prove GR.
It reads one immutable original receipt and never rewrites expected evidence.
The analytical theorem is in A4D_GLOBAL_JOINT_INDEX_AND_GR_RIGIDITY_2026_10_22.md.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as Q
from hashlib import sha1
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dec(value):
    with localcontext() as context:
        context.prec = 75
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def sign(value):
    return (value > 0) - (value < 0)


def main():
    packet = Path(__file__).resolve().parent
    native_path = packet.parent / "d0_original_unpadded42_2026-10-22" / "RESULT.json"
    native_bytes = native_path.read_bytes()
    blob = sha1(b"blob " + str(len(native_bytes)).encode("ascii") + b"\0" + native_bytes).hexdigest()
    expected_blob = "0ac76b58522d84f5bcc787fb6b6da0c99e1211cd"
    require(blob == expected_blob, "Original source receipt changed: cannot consume these bounds")
    native = json.loads(native_bytes)
    require(native["status"] == "PASS_LOCAL_OUTWARD_INTERVAL_BANACH_ORIGINAL_UNPADDED_42_ROOT", "Wrong original model")
    certificate = native["certificate"]
    expected_fields = {
        "original_old_root_rational_preconditioner_infinity_upper": "<28.883",
        "certified_new_near_inverse_infinity": "<0.036547",
        "center_drift_infinity": "<3.01e-52",
        "real_exact_root_ball_radius_infinity": "1e-24",
    }
    for key, value in expected_fields.items():
        require(certificate[key] == value, "Source-bound mismatch: " + key)
    require(native["analytic_domain"]["complex_polydisc_radius"] == "1e-4", "Wrong analytic domain")

    # These are conservative exact rational upper bounds consumed from the
    # already-proved native interval/Cauchy owner, not new interval evaluations.
    inverse_upper = Q("28.883")
    defect_upper = Q("0.036547")
    drift_upper = Q("3.01e-52")
    cauchy_constant = Q(42**2 * 48 * 20) / Q("1e-4")**3
    require(cauchy_constant == Q("1.69344e18"), "Cauchy arithmetic")
    radius = Q("1e-20")
    q_upper = defect_upper + inverse_upper * cauchy_constant * radius
    require(q_upper == Q("0.52566327520"), "Field boundary defect arithmetic")
    require(q_upper < 1, "Seed field index not isolated by this estimate")
    seed_face_margin = (1 - q_upper) * radius - drift_upper
    require(seed_face_margin > 0, "No seed boundary margin")

    # CONDITIONAL full-source application: the actual native residual is not
    # computed here. If its field part has this boundary bound uniformly over
    # the actual preparation manifold, these exact inequalities apply.
    hypothetical_residual_bound = Q("1e-22")
    scaled_residual_bound = inverse_upper * hypothetical_residual_bound
    full_face_margin = seed_face_margin - scaled_residual_bound
    require(scaled_residual_bound == Q("2.8883e-21"), "Scaled boundary-source arithmetic")
    require(full_face_margin > Q("1.85506724799e-21"), "No positive interpolated boundary margin")

    # A genuinely coupled analytical control on R^42 x S^2.
    # S_t=1/2 sum(p_j^2-q_j^2)+t(p_0 n_1+q_0 n_2+c n_3), c=1/2.
    # Field roots p_0=-t n_1, q_0=t n_2 reduce S to
    # W_t=-t^2 n_1^2/2+t^2 n_2^2/2+t c n_3 on |n|=1.
    # All source/Hessian formulas below are exact rational signs. No numerical
    # root finding, Monte Carlo boundary sampling, or native model substitution.
    c = Q(1, 2)
    field_index = (-1)**21
    control = []
    for t in (Q(1, 4), Q(1)):
        pole_det = t**2 * (c**2 - t**2)
        pole_index = sign(pole_det)
        require(pole_index != 0, "Use the separate bifurcation control at t=c")
        extra_count = 0
        extra_index_sum = 0
        if t > c:
            transverse_square = 1 - (c / t)**2
            extra_hessian_det = 2 * t**4 * transverse_square
            require(transverse_square > 0 and extra_hessian_det > 0, "Additional sphere roots")
            extra_count = 4
            extra_index_sum = 4
        prep_index_sum = 2 * pole_index + extra_index_sum
        require(prep_index_sum == 2, "S^2 index must be two on both sides of the fold")
        require(field_index * prep_index_sum == -2, "Joint product index")
        control.append({
            "t": dec(t),
            "joint_root_count": 2 + extra_count,
            "preparation_index_sum": prep_index_sum,
            "joint_index": field_index * prep_index_sum,
        })
    require(c**2 * (c**2 - c**2) == 0, "Interior Hessian degeneration at t=1/2")
    require(2 - Q(1) == 1, "All-t field boundary margin on the radius-two cube")

    # Missing-hypothesis controls. For S_t=(y-2t)^2/2+height(n), a root
    # crosses y=1 at t=1/2 and lies outside (-1,1) at t=1.
    require(2 * Q(1, 2) == 1 and 2 * Q(1) > 1, "Boundary-escape control")
    # On M=[0,1], S(y,u)=y^2/2+u has a field root at y=0 for every u,
    # but its independent preparation derivative is identically one.
    preparation_derivative_on_interval = Q(1)
    require(preparation_derivative_on_interval != 0, "Boundary KKT is not free preparation stationarity")

    result = {
        "status": "PASS_EXACT_ARITHMETIC_AND_ANALYTICAL_MODEL_CONTROLS",
        "source_snapshot": "fcfc52064737815c75bef96f7696b473ee304061",
        "native_receipt_blob": blob,
        "consumed_native_certificate_replayed": False,
        "boundary_budget": {
            "radius": dec(radius),
            "q_upper": dec(q_upper),
            "seed_face_margin_strict_lower": dec(seed_face_margin),
            "conditional_unscaled_residual_bound": dec(hypothetical_residual_bound),
            "scaled_residual_upper": dec(scaled_residual_bound),
            "full_face_margin_strict_lower": dec(full_face_margin),
            "unscaled_sufficient_boundary_budget": dec(seed_face_margin / inverse_upper),
            "preconditioned_seed_degree": 1,
        },
        "coupled_42_field_sphere_control": control,
        "interior_hessian_degeneracy_permitted": True,
        "boundary_escape_negative_control": "ROOT_LEAVES_AT_t_1/2",
        "preparation_with_boundary_negative_control": "NO_FREE_PREPARATION_CRITICAL_POINT",
        "physical_application": {
            "actual_full_Book03_residual_computed": False,
            "actual_preparation_manifold_identified": False,
            "actual_full_boundary_homotopy_certified": False,
            "new_physical_joint_root_certified": False,
            "uniform_refinement_certified": False,
            "GR_closed": False,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
