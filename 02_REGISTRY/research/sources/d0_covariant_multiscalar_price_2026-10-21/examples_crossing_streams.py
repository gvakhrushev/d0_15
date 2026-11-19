#!/usr/bin/env python3
"""Exact non-VSI two-scalar witness for the specified continuum price.

Derive curvature from the metric, then check the covariant equations and
the actual volume-gauge pullback. This is not a native lattice replay.
Requires SymPy. No assertions are disabled by python -O.
"""

import json
import sympy as sp


def main():
    checks = []

    def zero(name, expression):
        entries = list(expression) if isinstance(expression, sp.MatrixBase) else [expression]
        reduced = [sp.simplify(entry) for entry in entries]
        if any(entry != 0 for entry in reduced):
            raise RuntimeError(f"{name}: {reduced}")
        checks.append(name)

    b, x, y, z = sp.symbols("b x y z", positive=True)
    d, k0, eta = sp.symbols("d k0 eta", positive=True)
    coords = (b, x, y, z)
    f = sp.exp(d * b**2 / 2)
    metric = sp.diag(b * f, -f / b, -b**2, -b**2)
    inverse = metric.inv()
    volume = b**2 * f
    zero("positive_volume_squared", -metric.det() - volume**2)

    gamma = {}
    for a in range(4):
        for j in range(4):
            for k in range(4):
                entry = sp.simplify(sum(
                    inverse[a, l] * (
                        sp.diff(metric[l, k], coords[j])
                        + sp.diff(metric[l, j], coords[k])
                        - sp.diff(metric[j, k], coords[l])
                    ) for l in range(4)
                ) / 2)
                if entry != 0:
                    gamma[a, j, k] = entry

    def connection(a, j, k):
        return gamma.get((a, j, k), sp.S.Zero)

    riemann = {}
    for a in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    entry = sp.simplify(
                        sp.diff(connection(a, l, j), coords[k])
                        - sp.diff(connection(a, k, j), coords[l])
                        + sum(
                            connection(a, k, m) * connection(m, l, j)
                            - connection(a, l, m) * connection(m, k, j)
                            for m in range(4)
                        )
                    )
                    if entry != 0:
                        riemann[a, j, k, l] = entry

    ricci = sp.Matrix(4, 4, lambda j, l: sp.simplify(sum(
        riemann.get((a, j, a, l), sp.S.Zero) for a in range(4)
    )))
    scalar = sp.simplify(sp.trace(inverse * ricci))
    einstein = sp.simplify(ricci - metric * scalar / 2)
    zero("all_ricci_components", ricci - sp.diag(d, d / b**2, 0, 0))
    zero("scalar_curvature", scalar)

    fields = (b**2 / 2, x)
    gradients = [sp.Matrix([sp.diff(field, coord) for coord in coords]) for field in fields]
    kinetic_tensor = sum((v * v.T for v in gradients), sp.zeros(4))
    multiplier = d / b**2
    q_parts = [sp.simplify((v.T * inverse * v)[0]) for v in gradients]
    q = sp.simplify(sum(q_parts))
    zero("individual_kinetic_terms_opposite", sp.Matrix(q_parts) - sp.Matrix([b / f, -b / f]))
    zero("total_kinetic_constraint", q)
    zero("all_einstein_components", einstein - multiplier * kinetic_tensor)
    currents = []
    for a, gradient in enumerate(gradients, start=1):
        current_density = sp.simplify(volume * multiplier * inverse * gradient)
        currents.append(current_density)
        zero(f"covariant_scalar_{a}", sum(
            sp.diff(current_density[i], coords[i]) for i in range(4)
        ))
    zero("first_current_constant", currents[0] - sp.Matrix([d, 0, 0, 0]))
    zero("second_current_density", currents[1] - sp.Matrix([0, -d*b, 0, 0]))

    ricci_squared = sp.simplify(sp.trace((inverse * ricci)**2))
    riemann_squared = sp.simplify(sum(
        metric[a, a]**2 * inverse[a, a] * inverse[j, j]
        * inverse[k, k] * inverse[l, l] * entry**2
        for (a, j, k, l), entry in riemann.items()
    ))
    weyl_squared = sp.simplify(riemann_squared - 2 * ricci_squared + scalar**2/3)
    zero("nonzero_ricci_invariant_formula", ricci_squared - 2*d**2*sp.exp(-d*b**2)/b**2)
    zero("riemann_invariant_formula", riemann_squared - 4*(d**2*b**4+3)*sp.exp(-d*b**2)/b**6)
    zero("nonzero_weyl_invariant_formula", weyl_squared - 12*sp.exp(-d*b**2)/b**6)
    zero("rank_two_source_minor", ricci[:2, :2].det() - d**2/b**2)

    # d tau / d b = J > 0. All native-coordinate expressions remain functions
    # of the monotone parameter b; differentiation in tau is J^{-1} d/db.
    jacobian = d * f / k0
    new_volume = sp.simplify(volume / jacobian)
    new_metric = sp.diag(metric[0, 0] / jacobian**2, *[metric[i, i] for i in range(1, 4)])
    new_inverse = new_metric.inv()
    new_gradients = [sp.Matrix([v[0]/jacobian, v[1], v[2], v[3]]) for v in gradients]
    coordinate_pullback = sp.diag(1 / jacobian, 1, 1, 1)
    new_einstein = sp.simplify(coordinate_pullback * einstein * coordinate_pullback)
    new_kinetic = sum((v*v.T for v in new_gradients), sp.zeros(4))
    zero("volume_gauge", new_volume * multiplier - k0)
    zero("native_volume_formula", new_volume - k0*b**2/d)
    zero("all_native_metric_rows", new_volume * new_einstein - k0 * new_kinetic)
    for a, gradient in enumerate(new_gradients, start=1):
        current = sp.simplify(new_inverse * gradient)
        divergence = sp.diff(current[0], b) / jacobian + sum(
            sp.diff(current[i], coords[i]) for i in range(1, 4)
        )
        zero(f"native_undensitized_scalar_{a}", divergence)
    zero("native_two_queries", sp.Matrix([eta**2 * new_volume * scalar, -eta**2*q]))

    # Null-gradient decomposition is rank two, not the earlier rank-one wave.
    null_plus = (gradients[0] + gradients[1]) / sp.sqrt(2)
    null_minus = (gradients[0] - gradients[1]) / sp.sqrt(2)
    zero("crossing_null_covector_plus", (null_plus.T * inverse * null_plus)[0])
    zero("crossing_null_covector_minus", (null_minus.T * inverse * null_minus)[0])
    zero("crossing_null_tensor_identity", null_plus*null_plus.T + null_minus*null_minus.T - kinetic_tensor)

    # Two negative controls prevent losing the volume gauge or a real field.
    ungauged_defect = sp.simplify((volume*einstein-k0*kinetic_tensor)[0, 0])
    if sp.simplify(ungauged_defect.subs({b: 1, d: 1, k0: 1})) == 0:
        raise RuntimeError("omitting the volume gauge was not rejected")
    checks.append("reject_ungauged_native_equations")
    one_field_defect = sp.simplify((einstein - multiplier*gradients[0]*gradients[0].T)[1, 1])
    zero("retained_second_field_is_required", one_field_defect - d/b**2)
    if sp.simplify(one_field_defect.subs({b: 1, d: 1})) != 1:
        raise RuntimeError("dropping the second field was not detected")
    checks.append("reject_one_field_substitution")

    print(json.dumps({
        "status": "PASS",
        "scope": "exact conditional continuum witness; no finite native lattice or Book admission claim",
        "parameters": "b>0,d>0,k0>0,eta>0",
        "checks": checks,
        "check_groups": len(checks),
        "ricci": str(ricci),
        "scalar_curvature": str(scalar),
        "ricci_squared": str(ricci_squared),
        "weyl_squared": str(weyl_squared),
        "native_volume": str(new_volume),
        "GR_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
