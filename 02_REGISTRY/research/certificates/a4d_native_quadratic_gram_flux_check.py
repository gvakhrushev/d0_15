#!/usr/bin/env python3
"""Exact controls for signed quadratic profiles, the Gram pencil and flux gates.

General proofs are in A4D_NATIVE_QUADRATIC_GRAM_FLUX_BOUNDARY.md.
Default replay is read-only; --output explicitly generates a ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

INPUT_HEAD = "a30408721a3804e3d0c97fe2a210a556dbff4b67"
INPUTS = [
    "03_FORMALIZATION/D0/Geometry/A4DDiscreteEnergyKernel.lean",
    "03_FORMALIZATION/D0/Geometry/A4DConstitutiveKernelClassification.lean",
    "03_FORMALIZATION/D0/Geometry/A4DStarFiniteLorentzQuotient.lean",
    "03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean",
    "03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCARDegreePreserving.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean",
    "03_FORMALIZATION/D0/Gravity/A4DLinearizedMetricResponse.lean",
]
PUBLISHED_PROBE = {
    "source_head": "af221e2fed92821c52afc88a5500774de8cd9a93",
    "path": "02_REGISTRY/research/certificates/a4d_finite_probe_palatini_check.py",
    "sha256": "7f2d1c58fa4d4a8c52b2b3c76b9ca1369297f3c169d4216cbc5b7434ac787d6d",
}


def entries(matrix):
    return [[str(a) for a in row] for row in matrix.tolist()]


def scalar(expr):
    return sp.factor(expr[0] if isinstance(expr, sp.MatrixBase) else expr)


def annihilate(role):
    result = sp.zeros(16)
    for ket in range(16):
        if ket & (1 << role):
            bra = ket ^ (1 << role)
            sign = (-1) ** sum(bool(ket & (1 << r)) for r in range(role))
            result[bra, ket] = sign
    return result


def exterior_lift(matrix):
    masks = [[i for i in range(4) if mask & (1 << i)] for mask in range(16)]
    return sp.Matrix(16, 16, lambda i, j:
        matrix.extract(masks[i], masks[j]).det() if len(masks[i]) == len(masks[j]) else 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    checks = []

    def check(name, result):
        assert bool(result), name
        checks.append(name)
        print("PASS_" + name, flush=True)

    receipt_path = Path(__file__).with_name("a4d_native_flux_gate_results.json")
    receipt = json.loads(receipt_path.read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0
    assert not receipt["sorryAx"] and receipt["printed_axiom_dependencies"] == 6
    pinned = {**receipt["transitive_d0_source_sha256"], **receipt["toolchain_input_sha256"],
              receipt["capsule"]: receipt["capsule_sha256"], receipt["output"]: receipt["output_sha256"]}
    for path, digest in pinned.items():
        assert hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest, "LEAN_INPUT_CHANGED: "+path

    s, eps, z, a, b, c = sp.symbols("s eps z a b c", real=True)
    v = sp.Matrix(sp.symbols("v0:3", real=True))
    K = sp.diag(2, -3, 0)
    r = sp.Matrix([1 + 2*s, 3 - s, 0])
    S = scalar(v.T*K*v/2 + v.T*r) + 7*s*s + 5*s + 11
    root = sp.Matrix([-(1 + 2*s)/2, (3 - s)/3, z])
    subs = dict(zip(v, root))
    profile = sp.factor(S.subs(subs, simultaneous=True))
    check("INDEFINITE_FULL_AUXILIARY_GATE", K.det() == 0 and K[0, 0] > 0 and K[1, 1] < 0
          and K*root+r == sp.zeros(3, 1))
    check("ALL_KERNEL_PREPARATIONS_SHARE_PROFILE", sp.diff(profile, z) == 0)
    check("SIGNED_PROFILE_IS_QUADRATIC", sp.diff(profile, s, 3) == 0)
    secant = sp.cancel((profile.subs(s, s+eps)-profile.subs(s, s-eps))/(2*eps))
    check("CENTERED_SECANT_EXACTLY_AFFINE", sp.diff(secant, s, 2) == 0
          and sp.expand(secant-((1-s)*secant.subs(s, 0)+s*secant.subs(s, 1))) == 0)
    wv = sp.Matrix(sp.symbols("w0:3", real=True))
    shifted = S.subs(dict(zip(v, v+wv)), simultaneous=True)
    check("GENERIC_STATIONARY_VALUE_DIFFERENCE_IDENTITY",
          sp.expand(shifted-S-scalar(wv.T*(K*v+r))-scalar(wv.T*K*wv)/2) == 0)
    offshell = S.subs(dict(zip(v, [s*s, 0, 0])), simultaneous=True)
    check("MISSING_AUXILIARY_GATE_IS_NOT_COVERED", sp.diff(offshell, s, 3) != 0)
    check("NONQUADRATIC_NATIVE_ACTION_IS_NOT_COVERED", sp.diff(s**4, s, 3) != 0)

    # The nonlinear Gram map, including its full ten-component derivative.
    eta = sp.diag(1, -1, -1, -1)
    theta0 = sp.Matrix([[1, sp.Rational(1, 3), 0, 0], [0, -2, sp.Rational(1, 5), 0],
                        [0, 0, -1, sp.Rational(1, 7)], [0, 0, 0, -sp.Rational(3, 2)]])
    variables = sp.symbols("d0:16", real=True)
    dtheta = sp.Matrix(4, 4, variables)
    dgram = dtheta*eta*theta0.T+theta0*eta*dtheta.T
    slots = [(i, j) for i in range(4) for j in range(i, 4)]
    jac = sp.Matrix([dgram[i, j] for i, j in slots]).jacobian(variables)
    check("GRAM_ALL_TEN_SLOTS_RANK", jac.rank() == 10 and len(jac.nullspace()) == 6)
    gauge = []
    for i in range(4):
        for j in range(i+1, 4):
            B = sp.zeros(4)
            B[i, j] = 1
            B[j, i] = -eta[j, j]/eta[i, i]
            assert B*eta+eta*B.T == sp.zeros(4)
            gauge.append(sp.Matrix(list(theta0*B)))
    check("SIX_LORENTZ_FRAME_DIRECTIONS_ARE_EXACT_KERNEL",
          sp.Matrix.hstack(*gauge).rank() == 6
          and jac*sp.Matrix.hstack(*gauge) == sp.zeros(10, 6))
    metric_covector = sp.Matrix(4, 4, lambda i, j: sp.Rational(1+i+j, 7))
    for i, j in slots:
        V = sp.zeros(4)
        V[i, j] = V[j, i] = 1
        lift = V*theta0.T.inv()*eta/2
        actual = lift*eta*theta0.T+theta0*eta*lift.T
        check(f"GRAM_RIGHT_INVERSE_AND_PACKED_WEIGHT_{i}{j}", actual == V
              and sum(metric_covector[r, k]*V[r, k] for r in range(4) for k in range(4))
              == (1 if i == j else 2)*metric_covector[i, j])

    w, p, q = sp.symbols("w p q", real=True, nonzero=True)
    u = sp.Matrix([1, 0, 0, 0])
    n = sp.Matrix([1, 1, 0, 0])
    D = u*n.T
    theta = w*eta+s*D
    gram = sp.simplify(theta*eta*theta.T)
    check("NULL_RANK_ONE_GRAM_TERM_VANISHES", D*eta*D.T == sp.zeros(4))
    check("COFRAME_AND_METRIC_PENCIL_BOTH_AFFINE", theta.diff(s, 2) == sp.zeros(4)
          and gram.diff(s, 2) == sp.zeros(4)
          and sp.expand(gram-w*w*eta-s*w*(u*n.T+n*u.T)) == sp.zeros(4))
    check("ACTUAL_STRAIGHT_METRIC_ENDPOINTS",
          sp.simplify(gram.subs(s, s+eps)-gram.subs(s, s-eps)-2*eps*gram.diff(s)) == sp.zeros(4))
    check("GRAM_PENCIL_DETERMINANT", sp.factor(gram.det()) == -w**6*(w+s)**2)
    physical_solder = theta*eta
    check("PHYSICAL_SOLDER_FIXED_ORIENTATION_CONVERSION",
          sp.factor(physical_solder.det()) == w**3*(w+s)
          and sp.simplify(physical_solder*eta*physical_solder.T-gram) == sp.zeros(4))
    check("NON_NULL_GRAM_DIRECTION_HAS_QUADRATIC_TERM",
          ((w*eta+s*sp.eye(4))*eta*(w*eta+s*sp.eye(4)).T).diff(s, 2) != sp.zeros(4))

    # Reconstruct every Christoffel and Ricci component, with only y_2 varying.
    inv = sp.simplify(gram.inv())
    dg = gram.diff(w)*p
    Gamma = [[[sp.factor(sum(inv[i, d]*(
        (dg[d, k] if j == 2 else 0)+(dg[d, j] if k == 2 else 0)
        -(dg[j, k] if d == 2 else 0)) for d in range(4))/2)
        for k in range(4)] for j in range(4)] for i in range(4)]

    def dy(f):
        return sp.diff(f, w)*p+sp.diff(f, p)*q

    ricci = sp.Matrix(4, 4, lambda j, k: sp.factor(sum(
        (dy(Gamma[i][j][k]) if i == 2 else 0)
        -(dy(Gamma[i][i][j]) if k == 2 else 0)
        +sum(Gamma[i][i][d]*Gamma[d][j][k]-Gamma[i][k][d]*Gamma[d][i][j]
             for d in range(4)) for i in range(4))))
    check("ALL_RICCI_COMPONENTS_SYMMETRIC", ricci == ricci.T)
    R = sp.factor(sum(inv[j, k]*ricci[j, k] for j in range(4) for k in range(4)))
    target_R = -(5*p*p*s*s+4*p*p*s*w-8*q*s*s*w-20*q*s*w*w-12*q*w**3)/(2*w**4*(s+w)**2)
    check("GRAM_PENCIL_LITERAL_RICCI_SCALAR", sp.factor(R-target_R) == 0)
    check("INDEPENDENT_CONFORMAL_SIGN_AT_BASE", sp.factor(R.subs(s, 0)-6*q/w**3) == 0)
    density = sp.factor(-sp.Rational(1, 2)*w**3*(w+s)*R)
    coeff_q = sp.diff(density, q)
    ibp = sp.factor((density-coeff_q*q)/p**2-sp.diff(coeff_q, w))
    target_ibp = (s+2*w)*(5*s+6*w)/(4*w*(s+w))
    check("PERIODIC_INTEGRATION_BY_PARTS_ALL_COEFFICIENTS", sp.factor(ibp-target_ibp) == 0)
    third = sp.factor(sp.diff(ibp, s, 3).subs(s, 0))
    check("NONZERO_THIRD_VARIATION", third == -sp.Rational(3, 2)/w**3)
    y = sp.symbols("y", real=True)
    omega = 1+sp.cos(2*sp.pi*y)/10
    dp_energy = sp.integrate(sp.diff(omega, y)**2, (y, 0, 1))
    check("CURVED_PENCIL_STRICT_THIRD_BOUND", dp_energy == sp.pi**2/50
          and sp.factor(-sp.Rational(3, 2)*dp_energy/sp.Rational(11, 10)**3)
          == -30*sp.pi**2/1331)
    R_owner_peak = -R.subs({s: 0, w: sp.Rational(11, 10), p: 0, q: -2*sp.pi**2/5})
    check("CURVED_BASE_IS_NONFLAT", R_owner_peak == 2400*sp.pi**2/1331)
    conformal_action = 6*sp.pi**2*(sp.Rational(1, 10)+s)**2
    check("ZERO_FIELD_CURVED_GATE_HAS_NONZERO_EINSTEIN_VARIATION",
          sp.diff(conformal_action, s).subs(s, 0) == 6*sp.pi**2/5)
    check("FIXED_AFFINE_METRIC_SOURCE_CANNOT_REPAIR_THIRD_VARIATION",
          sp.diff(a+b*s, s, 3) == 0)

    # Arbitrary symmetric linear H(e): the generic full-gate identity.
    evars = sp.symbols("e0:6", real=True)
    H = sp.Matrix([[evars[0], evars[1], evars[2]],
                   [evars[1], evars[3], evars[4]], [evars[2], evars[4], evars[5]]])
    psi = sp.Matrix(sp.symbols("psi0:3", real=True))
    E = scalar(psi.T*(sp.eye(3)+H)*psi)/2
    Epsi = sp.Matrix([sp.diff(E, x) for x in psi])
    Je = sp.Matrix([sp.diff(E, x) for x in evars])
    check("GENERIC_FIELD_EULER_ALL_COMPONENTS", sp.expand(Epsi-(sp.eye(3)+H)*psi) == sp.zeros(3, 1))
    check("GENERIC_LOCAL_GEOMETRY_EULER_ALL_COMPONENTS",
          all(sp.factor(Je[i]-scalar(psi.T*H.diff(evars[i])*psi)/2) == 0 for i in range(6)))
    check("GENERIC_FULL_JOINT_ZERO_FIELD_IDENTITY",
          sp.expand(scalar(psi.T*Epsi)-2*sum(evars[i]*Je[i] for i in range(6))-scalar(psi.T*psi)) == 0)
    zero = dict(zip(psi, [0]*3))
    check("ZERO_FIELD_SOLVES_EVERY_FIELD_AND_GEOMETRY_ROW",
          Epsi.subs(zero) == sp.zeros(3, 1) and Je.subs(zero) == sp.zeros(6, 1))
    delta = sp.Matrix(sp.symbols("j0:3", real=True))
    dv = sp.symbols("v0:6", real=True)
    joint_curve = E.subs(dict(zip(evars, [evars[i]+s*dv[i] for i in range(6)])), simultaneous=True)
    joint_curve = sp.expand(joint_curve.subs(dict(zip(psi, s*delta)), simultaneous=True))
    check("ZERO_FIELD_FULL_JOINT_FIRST_VARIATION_VANISHES", sp.diff(joint_curve, s).subs(s, 0) == 0)

    alpha = sp.symbols("alpha", real=True, nonzero=True)
    Q = sp.eye(3)+H+alpha*H*H
    square = alpha*(H+sp.eye(3)/(2*alpha))**2+(1-1/(4*alpha))*sp.eye(3)
    check("POLYNOMIAL_KERNEL_EXACT_COERCIVE_SQUARE", sp.simplify(Q-square) == sp.zeros(3))
    check("QUARTER_KERNEL_IS_A_SQUARE", sp.simplify(Q.subs(alpha, sp.Rational(1, 4))
          -(sp.eye(3)+H/2)**2) == sp.zeros(3))
    Hroot = sp.diag(-2, 1, 3)
    rootpsi = sp.Matrix([1, 0, 0])
    for i, evar in enumerate(evars):
        dH = H.diff(evar)
        dQ = dH+(dH*Hroot+Hroot*dH)/4
        check(f"QUARTER_NONZERO_KERNEL_SOURCE_ZERO_{i}", scalar(rootpsi.T*dQ*rootpsi) == 0)
    check("NONZERO_FIXED_FORCING_CHANGES_GATE",
          [sp.diff((1+s)*z*z/2-s/2-z, x).subs({s: 0, z: 1}) for x in (s, z)] == [0, 0])
    check("NORMALIZED_FIELD_VARIATIONS_DO_NOT_INCLUDE_RADIAL_DIRECTION",
          sp.diff((z+s*z)**2-1, s).subs({s: 0, z: 1}) == 2)

    # Actual 16-state CAR sector, all four roles in owner order A,B,C,D.
    ann = [annihilate(r) for r in range(4)]
    car = [[ann[r].T*ann[k] for k in range(4)] for r in range(4)]
    vacuum = sp.zeros(16, 1)
    vacuum[0] = 1
    check("ACTUAL_16_STATE_CAR_ALL_RELATIONS", all(
        ann[r]*ann[k].T+ann[k].T*ann[r] == (sp.eye(16) if r == k else sp.zeros(16))
        for r in range(4) for k in range(4)))
    check("ALL_SIXTEEN_CAR_BILINEARS_KILL_VACUUM", all(
        car[r][k]*vacuum == sp.zeros(16, 1) for r in range(4) for k in range(4)))
    ev = sp.Matrix(4, 4, sp.symbols("c0:16", real=True))
    Hconstant = sp.trace(ev)*sp.eye(16)
    for r in range(4):
        for k in range(4):
            Hconstant -= ev[r, k]*(car[r][k]+car[k][r])
    Econstant = scalar(vacuum.T*(sp.eye(16)+Hconstant)*vacuum)/2
    check("LITERAL_CONSTANT_FOCK_SCALAR_ACTION", sp.expand(Econstant-(1+sp.trace(ev))/2) == 0)
    Jeconstant = sp.Matrix(4, 4, [sp.diff(Econstant, x) for x in ev])
    check("LITERAL_LOCAL_SIXTEEN_SLOT_SOURCE", Jeconstant == sp.eye(4)/2)

    Troot = sp.diag(1, -2, -1, -1)
    eroot = Troot-eta
    root_sub = dict(zip(ev, eroot))
    check("NONDEGENERATE_ACTUAL_FIELD_ONLY_ROOT", Troot.det() == -2
          and Econstant.subs(root_sub) == 0
          and (sp.eye(16)+Hconstant.subs(root_sub))*vacuum == sp.zeros(16, 1)
          and Jeconstant != sp.zeros(4))
    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.Rational(5, 4)
    boost[0, 1] = boost[1, 0] = sp.Rational(3, 4)
    boosted = Troot*boost
    boost_sub = dict(zip(ev, boosted-eta))
    check("PROPER_TIME_ORIENTED_RATIONAL_BOOST", boost*eta*boost.T == eta
          and boost.det() == 1 and boost[0, 0] > 0)
    check("BOOST_PRESERVES_ACTUAL_RAW_GRAM", boosted*eta*boosted.T == Troot*eta*Troot.T
          and boosted.det() == Troot.det())
    check("OWNED_EXTERIOR_LIFT_FIXES_SCALAR_SECTOR", exterior_lift(boost)*vacuum == vacuum)
    boosted_energy = Econstant.subs(boost_sub)
    boosted_residual = (sp.eye(16)+Hconstant.subs(boost_sub))*vacuum
    check("FLUX_ACTION_FAILS_NONLINEAR_LORENTZ_DESCENT", boosted_energy == -sp.Rational(1, 8))
    check("FIELD_GATE_FAILS_NONLINEAR_LORENTZ_DESCENT", boosted_residual == -vacuum/4)
    metric_source = sp.diag(sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 4), sp.Rational(1, 4))
    check("FIELD_ONLY_ROOT_METRIC_SOURCE_NONZERO", 2*metric_source*Troot*eta == Jeconstant)

    payload = {
        "status": "PASS", "input_head": INPUT_HEAD,
        "input_sha256": {p: hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in INPUTS},
        "consumed_published_probe": PUBLISHED_PROBE,
        "lean_capsule_receipt_sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        "checks": checks,
        "signed_profile": {"value": str(profile), "secant": str(secant), "auxiliary_kernel_dimension": 1},
        "gram_pencil": {"gram": entries(gram), "ricci": entries(ricci), "standard_scalar": str(R),
            "owner_density": str(density), "periodic_coefficient": str(ibp),
            "third_integrand_coefficient_at_zero": str(third),
            "strict_third_upper_bound": "-30*pi**2/1331", "curved_base_owner_scalar_at_peak": str(R_owner_peak),
            "full_metric_differential_rank": 10, "frame_kernel_dimension": 6},
        "flux_gate": {"joint_solution_set": "psi=0; coframe arbitrary",
            "zero_field_curved_Einstein_derivative": "6*pi**2/5",
            "constant_root_gram": entries(Troot*eta*Troot.T),
            "constant_root_local_coframe_source": entries(Jeconstant),
            "boosted_energy_per_site": str(boosted_energy), "boosted_field_residual": entries(boosted_residual),
            "polynomial_positive_regime": "alpha>1/4: only psi=0; no coefficient selected"},
        "scope": "Analytic arbitrary-stage signed-quadratic profile and literal standalone flux-gate obstructions; no full-core completeness, combined-action or native-refinement closure assertion.",
    }
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    expected = args.expect or (Path(__file__).with_name("a4d_native_quadratic_gram_flux_results.json") if not args.output else None)
    if expected:
        assert json.loads(expected.read_text()) == payload, "PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER", flush=True)
    print("PASS_NATIVE_QUADRATIC_GRAM_FLUX_BOUNDARY", len(checks), flush=True)


if __name__ == "__main__":
    main()
