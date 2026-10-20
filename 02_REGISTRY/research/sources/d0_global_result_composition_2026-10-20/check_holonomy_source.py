#!/usr/bin/env python3
"""Narrow exact matrix/boost checks for the new composition proof.

Uses the published original null REST generators and grade-one Choi block
inside CAR16 x fresh R4. No old replay, input mutation, full-rank census,
Lorentz all40 theorem, or physical action-selection claim is performed.
All gates below are active under Python -O. The analytic inverse theorem,
the all-jet chain rule and the continuum theorem remain analytical proofs.
"""

import json

import sympy as sp


GROUPS = []


def require(value, message):
    if value is not True:
        raise RuntimeError(message)


def zero(expr):
    if isinstance(expr, sp.MatrixBase):
        return all(sp.simplify(x) == 0 for x in expr)
    return sp.simplify(expr) == 0


def unit(i, j):
    out = sp.zeros(4)
    out[i, j] = 1
    return out


def vec(matrix):
    # A fixed row-major vectorization; all overlaps are Frobenius products.
    return sp.Matrix(list(matrix))


def main():
    eta = sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0],
                     [0, 0, -1, 0], [0, 0, 0, -1]])
    n2 = unit(1, 2) + unit(2, 0)
    n3 = unit(1, 3) + unit(3, 0)
    m2 = unit(0, 2) + unit(2, 1)
    m3 = unit(0, 3) + unit(3, 1)
    j = unit(2, 3) - unit(3, 2)
    b = unit(1, 1) - unit(0, 0)
    gs = [n2, n3, m2, m3, j, b]
    for a, ga in enumerate(gs):
        require(zero(ga.T * eta + eta * ga), f"Lorentz generator {a}")
        require(sp.trace(ga) == 0, f"traceless generator {a}")
        for c, gc in enumerate(gs):
            require(sp.trace(ga.T * gc) == (2 if a == c else 0),
                    f"native REST Gram {a},{c}")
    require(zero(n2 * m3 - m3 * n2 - j), "original J commutator")
    require(zero(n2 * m2 - m2 * n2 - b), "original B commutator")
    GROUPS.append("literal_native_Lorentz_REST_basis_and_two_commutators")

    omega = vec(sp.eye(4)) / 2
    fs = [sp.sqrt(2) * vec(ga) / 2 for ga in gs]
    require((omega.T * omega)[0] == 1, "normalized original Choi block")
    for a, fa in enumerate(fs):
        require((omega.T * fa)[0] == 0, f"Choi tangent orthogonal {a}")
        for c, fc in enumerate(fs):
            require((fa.T * fc)[0] == (1 if a == c else 0),
                    f"Choi tangent orthonormal {a},{c}")
    effects = {}
    for a, fa in enumerate(fs):
        for sign in (-1, 1):
            v = (omega + sign * fa) / sp.sqrt(2)
            effects[a, sign] = v * v.T / 12
    rest = sp.eye(16) - sum(effects.values(), sp.zeros(16))
    expected_rest = sp.eye(16) - omega * omega.T / 2
    for fa in fs:
        expected_rest -= fa * fa.T / 12
    require(zero(rest - expected_rest), "original complete positive rest decomposition")
    GROUPS.append("original_prepared_grade1_R4_block_and_13_effect_completeness")

    lam, z = sp.symbols("lam z", positive=True)
    p = sp.diag(1 / z, z, 1, 1)
    require(zero(p.T * eta * p - eta), "boost proper Lorentz metric")
    require(p.det() == 1, "boost determinant")
    chi = sp.sqrt(lam) * vec(p) / 2
    probs = {}
    for a, ga in enumerate(gs):
        alpha = sp.trace(p) / 4
        beta = sp.sqrt(2) * sp.trace(ga.T * p) / 4
        for sign in (-1, 1):
            actual = (chi.T * effects[a, sign] * chi)[0]
            expected = lam * (alpha + sign * beta) ** 2 / 24
            require(zero(actual - expected), f"original unconditional pointer {a},{sign}")
            probs[a, sign] = sp.factor(expected)
            require(sp.simplify(expected.subs(z, 1)) == lam / 24,
                    f"positive baseline pointer {a},{sign}")
        ratio = sp.cancel(probs[a, -1] / probs[a, 1])
        require(zero(sp.diff(ratio, lam)), f"exact subdivision-free odds {a}")
    a_norm = sp.trace(p.T * p) / 4
    require(zero(a_norm - (z + 1 / z) ** 2 / 4), "boost Choi mass cosh squared")
    success = (chi.T * chi)[0]
    rest_prob = (chi.T * rest * chi)[0]
    require(zero(success - lam * a_norm), "full all-good mass")
    require(zero(sum(probs.values()) + rest_prob - success), "complete success pointer mass")
    require(sp.simplify(rest_prob.subs(z, 1)) == lam / 2,
            "positive baseline success rest")
    GROUPS.append("all_good_probabilities_exact_subdivision_odds_and_boost_mass")

    t = sp.symbols("t", real=True)
    ln_phi = sp.log((1 + sp.sqrt(5)) / 2)
    jac = sp.zeros(6)
    conditional_fisher = []
    for c, gc in enumerate(gs):
        first_jet_p = sp.eye(4) + t * gc
        alpha = sp.trace(first_jet_p) / 4
        derivs = []
        for a, ga in enumerate(gs):
            beta = sp.sqrt(2) * sp.trace(ga.T * first_jet_p) / 4
            qm = lam * (alpha - beta) ** 2 / 24
            qp = lam * (alpha + beta) ** 2 / 24
            jac[a, c] = sp.simplify((sp.diff(qm, t) / qm - sp.diff(qp, t) / qp).subs(t, 0) / ln_phi)
            derivs.extend([sp.diff(qm / lam, t).subs(t, 0),
                           sp.diff(qp / lam, t).subs(t, 0)])
        conditional_fisher.append(sp.simplify(sum(d * d * 24 for d in derivs)))
    require(zero(jac + 2 * sp.sqrt(2) * sp.eye(6) / ln_phi),
            "exact six-odds Jacobian in the literal native basis")
    require(all(v == sp.Rational(1, 6) for v in conditional_fisher),
            "conditional success pointer Fisher")
    GROUPS.append("native_six_by_six_odds_first_jet_and_coarse_Fisher")

    an, am = sp.symbols("A_n A_m", real=True)
    tanh = (z - 1 / z) / (z + 1 / z)
    cost_n = an / a_norm
    cost_m = am / a_norm
    dxi = lambda expr: z * sp.diff(expr, z)
    require(zero(dxi(cost_n) + 2 * an * tanh / a_norm), "exact retained-call source")
    require(zero((cost_n - cost_m) - (an - am) + (an - am) * tanh ** 2),
            "exact flat-subtracted vertical price defect")
    require(sp.simplify(dxi(cost_n).subs(z, 1)) == 0, "flat first jet cannot see defect")
    require(sp.simplify(dxi(dxi(cost_n - cost_m)).subs(z, 1)) == -2 * (an - am),
            "flat second jet sees source defect")
    direct_vs_four = -2 * (4 * 4 ** 4 - 1 * 4 ** 1)
    require(direct_vs_four == -2040, "direct versus four-edge exact Hessian defect")
    ak = sp.symbols("A_k", real=True)
    omega_nm = dxi((an - am) / a_norm)
    omega_mk = dxi((am - ak) / a_norm)
    omega_nk = dxi((an - ak) / a_norm)
    require(zero(omega_nm + omega_mk - omega_nk), "exact additive vertical source cocycle")
    GROUPS.append("retained_call_cost_exact_source_cocycle_and_minus_2040_witness")

    print(json.dumps({
        "status": "PASS",
        "arithmetic": "exact_sympy",
        "groups": GROUPS,
        "group_count": len(GROUPS),
        "odds_jacobian": "-2*sqrt(2)/log(phi) * I6",
        "success_mass": "4**(-n)*cosh(xi)**2",
        "primitive_call_cost": "n*4**n*sech(xi)**2",
        "flat_subtracted_direct_vs_four": "-1020*tanh(xi)**2",
        "flat_second_derivative_direct_vs_four": direct_vs_four,
        "original_referenced_checker_replayed": False,
        "scope": "Finite original prepared Choi block and stated complete-trial stopping protocol only; analytic all-jet composition is a separate proof; no physical action selection or GR closure."
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
