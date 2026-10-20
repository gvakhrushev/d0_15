"""Exact checks for the heat/Einstein covector comparison. python -O safe."""
from __future__ import annotations

import json
import sympy as sp

from heat_covector import (
    PHI,
    PROFILE,
    X,
    anholonomy_quadratic,
    e00_frame,
    einstein_hilbert_density,
    euler,
    heat_coefficient,
    lorentz_metric,
    positive_metric,
    probe_g00,
    profile_frame,
    require_sphere,
    varied,
    wave_frame,
)


def require(condition, name: str, checks: list[str]) -> None:
    if not bool(condition):
        raise ArithmeticError(name)
    checks.append(name)


def only_zero_calibration(heat_el, volume_el, profile_heat) -> bool:
    c0, c2, c = sp.symbols("C0 C2 c")
    profile = sp.simplify(c2 * profile_heat)
    transverse = sp.expand(c0 * volume_el + c2 * heat_el + c)
    if profile != 0 and sp.simplify(sp.diff(transverse, X)) != 0:
        # Used only as a documented shape. The solver below is the check.
        pass
    poly = sp.Poly(sp.together(transverse), X)
    equations = [profile, *poly.coeffs()]
    solution = sp.solve(equations, [c0, c2, c], dict=True)
    return solution == [{c0: 0, c2: 0, c: 0}]


def main() -> dict:
    checks: list[str] = []
    require_sphere()
    checks.append("sphere_scalar_2_and_ricci_1")

    frame = wave_frame(PROFILE)
    metric = lorentz_metric(frame)
    require(sp.simplify(frame.det() - 1) == 0, "det_frame_1", checks)
    require(sp.simplify(metric.det() + 1) == 0, "det_metric_minus_1", checks)
    require(sp.simplify(einstein_hilbert_density(metric)) == 0, "lorentz_density_0", checks)
    g00 = sp.factor(probe_g00(metric))
    require(g00 == 1, "probe_G00_is_1", checks)
    require(sp.simplify(positive_metric(frame).det() - 1) == 0, "positive_det_1", checks)
    q = sp.factor(anholonomy_quadratic(frame))
    l2 = sp.factor(heat_coefficient(frame))
    hx2 = sp.diff(PROFILE, X) ** 2
    require(sp.simplify(q - 2 * hx2) == 0, "anholonomy_is_2_grad2", checks)
    require(sp.simplify(l2 - sp.Rational(8, 3) * hx2) == 0, "heat_is_8_over_3_grad2", checks)

    # Profile direction. det e stays 1, so the volume factor does not move.
    family = profile_frame()
    require(sp.simplify(family.det() - 1) == 0, "profile_det_frozen", checks)
    profile_eh, _ = euler(varied(einstein_hilbert_density(lorentz_metric(family))))
    profile_heat, _ = euler(varied(heat_coefficient(family)))
    require(sp.simplify(profile_eh) == 0, "profile_EH_EL_0", checks)
    require(sp.simplify(profile_heat + sp.Rational(32, 3)) == 0, "profile_heat_EL_minus_32_over_3", checks)

    # E_00 direction.
    from heat_covector import E00

    lifted, _ = e00_frame()
    lifted_metric = lorentz_metric(lifted)
    require(
        sp.simplify(varied(lifted_metric) - PHI * E00) == sp.zeros(4),
        "lift_reproduces_E00",
        checks,
    )
    eh_raw = varied(einstein_hilbert_density(lifted_metric))
    eh_el, eh_current = euler(eh_raw)
    published_current = -X * PHI - (4 * X**2 - 3) * sp.diff(PHI, X) / 4
    require(sp.simplify(eh_current - published_current) == 0, "E00_EH_current", checks)
    require(sp.simplify(eh_el + 1) == 0, "E00_EH_EL_minus_1", checks)
    require(sp.simplify(eh_el + g00) == 0, "E00_EH_EL_equals_minus_probe", checks)
    frozen = eh_raw.subs(sp.diff(PHI, X, 2), 0).subs(sp.diff(PHI, X), 0)
    require(sp.simplify(frozen.subs(X, 0) + 2 * PHI.subs(X, 0)) == 0, "raw_origin_constant_phi_is_minus_2", checks)

    heat_raw = varied(heat_coefficient(lifted))
    heat_el, _ = euler(heat_raw)
    heat_vol_raw = varied(heat_coefficient(lifted) * lifted.det())
    heat_vol_el, _ = euler(heat_vol_raw)
    expected_heat = -(4 * X**2 - 4 * X - 1) * (4 * X**2 + 4 * X - 1) / 6
    expected_vol = -(48 * X**4 - 48 * X**2 + 1) / 6
    require(sp.simplify(heat_el - expected_heat) == 0, "E00_heat_EL_without_volume", checks)
    require(sp.simplify(heat_vol_el - expected_vol) == 0, "E00_heat_EL_with_volume", checks)
    require(sp.simplify(heat_el.subs(X, 0) + sp.Rational(1, 6)) == 0, "heat_EL_at_0_is_minus_1_6", checks)
    require(sp.simplify(heat_vol_el.subs(X, 0) + sp.Rational(1, 6)) == 0, "heat_volume_EL_at_0_is_minus_1_6", checks)
    require(sp.simplify(sp.diff(heat_el, X)) != 0, "heat_EL_not_constant", checks)
    require(sp.simplify(sp.diff(heat_vol_el, X)) != 0, "heat_volume_EL_not_constant", checks)

    # Positive volume and Lorentz volume have the same first derivative here,
    # because sqrt(-det g) = |det e| and det e = 1 on the background.
    lorentz_volume = varied(sp.sqrt(-lifted_metric.det()))
    positive_volume = varied(lifted.det())
    require(sp.simplify(lorentz_volume - positive_volume) == 0, "volumes_agree_at_first_order", checks)
    volume_el, _ = euler(positive_volume)
    require(sp.simplify(volume_el - (-(4 * X**2 - 3) / 8)) == 0, "volume_EL", checks)
    require(sp.simplify(volume_el.subs(X, 0) - sp.Rational(3, 8)) == 0, "volume_EL_at_0_is_3_8", checks)
    require(sp.simplify(volume_el + 1) != 0, "volume_EL_is_not_einstein", checks)

    require(only_zero_calibration(heat_el, volume_el, profile_heat), "calibration_without_volume_only_zero", checks)
    require(only_zero_calibration(heat_vol_el, volume_el, profile_heat), "calibration_with_volume_only_zero", checks)

    # Second profile from the independent attack. Hxx=1, so the probe is 1/2.
    half = X**2 / 2
    half_frame = wave_frame(half)
    half_metric = lorentz_metric(half_frame)
    require(sp.simplify(probe_g00(half_metric) - sp.Rational(1, 2)) == 0, "half_profile_probe_1_2", checks)
    half_family = profile_frame(half)
    half_eh, _ = euler(varied(einstein_hilbert_density(lorentz_metric(half_family))))
    half_heat, _ = euler(varied(heat_coefficient(half_family)))
    require(sp.simplify(half_eh) == 0, "half_profile_EH_EL_0", checks)
    require(sp.simplify(half_heat + sp.Rational(16, 3)) == 0, "half_profile_heat_EL_minus_16_over_3", checks)
    half_lifted, _ = e00_frame(half)
    half_e00, _ = euler(varied(einstein_hilbert_density(lorentz_metric(half_lifted))))
    require(sp.simplify(half_e00 + sp.Rational(1, 2)) == 0, "half_E00_EH_EL_minus_1_2", checks)
    payload = {
        "schema": "d0-heat-e00-covector/1",
        "status": "PASS",
        "candidate": True,
        "gr_derived": False,
        "native_price_equals_geometric_action": False,
        "equation_20_closed": False,
        "background": "H=x^2+1/4",
        "probe_G00": "1",
        "profile_EH_EL": "0",
        "profile_heat_EL": "-32/3",
        "E00_EH_EL": "-1",
        "E00_heat_EL": str(sp.factor(heat_el)),
        "E00_heat_EL_with_volume": str(sp.factor(heat_vol_el)),
        "E00_heat_EL_at_0": "-1/6",
        "volume_EL": str(sp.factor(volume_el)),
        "constant_calibration_reproduces_einstein": False,
        "exact_check_count": len(checks),
        "checks": checks,
    }
    return payload


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
