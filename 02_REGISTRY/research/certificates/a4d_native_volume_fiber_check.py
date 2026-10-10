#!/usr/bin/env python3
"""Exact curved volume-fiber and actual auxiliary-elimination controls.

See A4D_NATIVE_VOLUME_FIBER_OBSTRUCTION.md for the general proof.
Default replay compares an immutable ledger; --output explicitly creates it.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

INPUT_HEAD = "ff5baf86642fca81714843b8ab48bed50939fe54"
INPUTS = [
    "03_FORMALIZATION/D0/Geometry/A4DRawSolderFrameAction.lean",
    "03_FORMALIZATION/D0/Geometry/A4DStarFiniteLorentzQuotient.lean",
    "03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean",
    "03_FORMALIZATION/D0/Geometry/ConformalLaplacianTrace.lean",
    "03_FORMALIZATION/D0/Geometry/HeatTraceEHProxy.lean",
    "03_FORMALIZATION/D0/Cosmology/EntropyArchiveFlow.lean",
    "03_FORMALIZATION/D0/Gravity/A2CompensatorNoether.lean",
    "02_REGISTRY/research/A4D_NATIVE_QUADRATIC_GRAM_FLUX_BOUNDARY.md",
    "02_REGISTRY/research/A4D_NATIVE_WEIGHTED_TRACE_LIFT_BOUNDARY.md",
]
PROBE_INPUT = {
    "source_head": "af221e2fed92821c52afc88a5500774de8cd9a93",
    "path": "02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md",
    "consumption": "Constructively nonempty smooth midpoint endpoint preparations; all 24 finite Euler rows O(h^2), and the uniform action/contrast theorem. These are not exact joint roots.",
}


def entries(m):
    return [[str(v) for v in row] for row in m.tolist()]


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

    receipt_path = Path(__file__).with_name("a4d_native_volume_fiber_results.json")
    receipt = json.loads(receipt_path.read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0
    assert not receipt["sorryAx"] and receipt["printed_axiom_dependencies"] == 6
    pinned = {
        **receipt["transitive_d0_source_sha256"], **receipt["toolchain_input_sha256"],
        receipt["capsule"]: receipt["capsule_sha256"], receipt["output"]: receipt["output_sha256"],
    }
    for path, digest in pinned.items():
        assert hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest, "LEAN_INPUT_CHANGED: " + path

    s, eps, t, p, q = sp.symbols("s eps t p q", real=True)
    w = sp.symbols("w", positive=True)
    eta = sp.diag(1, -1, -1, -1)
    n = sp.Matrix([1, 0, 1, 0])
    P = n*n.T
    theta = w*eta+s*w*P/2
    E = theta*eta
    g = sp.simplify(theta*eta*theta.T)
    inv = sp.simplify(g.inv())
    volume = sp.sqrt(-sp.factor(g.det()))
    check("LITERAL_NULL_GRAM_HYPOTHESES", P.T == P and P*eta*P == sp.zeros(4))
    check("LITERAL_RAW_GRAM_PENCIL", sp.expand(g-w*w*(eta+s*P)) == sp.zeros(4))
    check("BOTH_RAW_COFRAME_AND_METRIC_ARE_AFFINE", theta.diff(s, 2) == sp.zeros(4) and g.diff(s, 2) == sp.zeros(4))
    check("EXACT_STRAIGHT_METRIC_ENDPOINTS", sp.expand(g.subs(s, s+eps)-g.subs(s, s-eps)-2*eps*w*w*P) == sp.zeros(4))
    check("POSITIVE_ORIENTATION_SOLDER", sp.factor(E.det()) == w**4 and sp.expand(E*eta*E.T-g) == sp.zeros(4))
    check("EXACT_POINTWISE_VOLUME_FIBER", volume == w**4 and sp.diff(volume, s) == 0)
    check("NONDEGENERATE_METRIC_INVERSE", sp.simplify(inv-(eta-s*eta*P*eta)/w**2) == sp.zeros(4))
    check("METRIC_SHAPE_REALLY_CHANGES", g.diff(s) == w*w*P and P != sp.zeros(4))

    slots = [(i, j) for i in range(4) for j in range(i, 4)]
    volume_row = []
    for i, j in slots:
        H = sp.zeros(4)
        H[i, j] = H[j, i] = 1
        derivative = sp.factor(-sp.diff((g+t*H).det(), t).subs(t, 0)/(2*volume))
        packed = (1 if i == j else 2)*volume*inv[i, j]/2
        volume_row.append(derivative)
        check(f"ALL_VOLUME_METRIC_SLOTS_AND_PACKING_{i}{j}", sp.factor(derivative-packed) == 0)
    covector = sp.Matrix([volume_row])
    probe = g.diff(s)
    probe_packed = sp.Matrix([probe[i, j] for i, j in slots])
    check("VOLUME_KERNEL_HAS_NINE_SHAPE_DIRECTIONS", covector.rank() == 1 and len(covector.nullspace()) == 9)
    check("PROBE_LIES_IN_FULL_VOLUME_KERNEL", sp.simplify(covector*probe_packed) == sp.zeros(1, 1))

    # Direct Levi-Civita computation, only y_2 varies.
    dg = g.diff(w)*p
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
    R = sp.factor(sum(inv[i, j]*ricci[i, j] for i in range(4) for j in range(4)))
    check("ALL_RICCI_ENTRIES_SYMMETRIC", ricci == ricci.T)
    check("EXACT_STANDARD_RICCI_SCALAR", R == 6*q*(1+s)/w**3)
    einstein = sp.simplify(ricci-g*R/2)
    raised = sp.simplify(inv*einstein*inv)
    density = sp.factor(-volume*R/2)
    check("LITERAL_OWNER_ACTION_SIGN_AND_NORMALIZATION", density == -3*w*q*(1+s))
    qcoeff = sp.diff(density, q)
    ibp = sp.factor((density-qcoeff*q)/p**2-sp.diff(qcoeff, w))
    check("PERIODIC_ACTION_COEFFICIENT", sp.expand(ibp-3*(1+s)) == 0)
    pairing = sp.factor(volume*sum(raised[i, j]*probe[i, j] for i in range(4) for j in range(4))/2)
    check("INDEPENDENT_EINSTEIN_FIRST_VARIATION", pairing == 2*p*p-w*q)
    packed_pairing = sp.factor(volume*sum((1 if i == j else 2)*raised[i, j]*probe[i, j] for i, j in slots)/2)
    check("EINSTEIN_TEN_SLOT_PACKED_RESPONSE", packed_pairing == pairing)
    check("EINSTEIN_DENSITY_DIFFERS_BY_TOTAL_DERIVATIVE", sp.factor(pairing-sp.diff(density, s)-2*(p*p+w*q)) == 0)
    check("VOLUME_SOURCE_IS_INVISIBLE_TO_THE_PROBE", sp.factor(sum(inv[i, j]*probe[i, j] for i in range(4) for j in range(4))) == 0)

    # These are the 24 continuum torsion equations, not 24 exact finite E_K equations.
    spin = []
    for i in range(4):
        Gi = sp.Matrix(4, 4, lambda a, b: Gamma[a][i][b])
        dEi = E.diff(w)*p if i == 2 else sp.zeros(4)
        omega = sp.simplify((E.inv()*(Gi.T*E-dEi)).T)
        spin.append(omega)
        check(f"PHYSICAL_SPIN_CONNECTION_LORENTZ_{i}", sp.simplify(omega.T*eta+eta*omega) == sp.zeros(4))
    for i in range(4):
        for j in range(i+1, 4):
            for a in range(4):
                torsion = (E[j, a].diff(w)*p if i == 2 else 0)-(E[i, a].diff(w)*p if j == 2 else 0)
                torsion += sum(spin[i][a, b]*E[j, b]-spin[j][a, b]*E[i, b] for b in range(4))
                check(f"CONTINUUM_TORSION_ROW_{i}{j}_{a}", sp.factor(torsion) == 0)

    y = sp.symbols("y", real=True)
    Omega = 1+sp.cos(2*sp.pi*y)/10
    integral = sp.integrate(sp.diff(Omega, y)**2, (y, 0, 1))
    action = 3*(1+s)*integral
    derivative = sp.diff(action, s)
    check("FIXED_CURVED_FACTOR_GRADIENT_INTEGRAL", integral == sp.pi**2/50)
    check("STRICT_FIXED_VOLUME_EINSTEIN_CONTRAST", sp.expand((action.subs(s, s+eps)-action.subs(s, s-eps))/2) == 3*sp.pi**2*eps/50)
    check("CURVED_BASE_OWNER_SCALAR", -R.subs({s: 0, w: sp.Rational(11, 10), p: 0, q: -2*sp.pi**2/5}) == 2400*sp.pi**2/1331)
    check("FLAT_FACTOR_CONTROL", density.subs({p: 0, q: 0}) == 0 and pairing.subs({p: 0, q: 0}) == 0)
    check("TRACEFREE_EINSTEIN_RESPONSE_IS_NONZERO", pairing.subs({w: 1, p: 1, q: 0}) == 2)

    # Literal rational compensator with density-dependent weights and all kernel roots.
    B = sp.Matrix(4, 4, lambda i, j: int(i == j)+int(i == (j+1) % 4))
    a = 1+s
    mu = [a, sp.Integer(1), sp.Integer(1), sp.Integer(1)]
    W = sp.diag(*[mu[i]*mu[(i+1) % 4] for i in range(4)])
    h = sp.Matrix([1, 0, 0, 0])
    tt = a/(2*(a+1))
    phi = sp.Matrix([tt/a, 2*tt, -tt, 0])
    kernel = sp.Matrix([1, -1, 1, -1])
    z = sp.symbols("z", real=True)
    residual = sp.simplify(h-B.T*(phi+z*kernel))
    normal = B*W*B.T
    check("LITERAL_RHO_PRODUCT_WEIGHTS", W == sp.diag(1+s, 1, 1, 1+s))
    check("ALL_FOUR_AUXILIARY_NORMAL_ROWS", sp.simplify(normal*(phi+z*kernel)-B*W*h) == sp.zeros(4, 1))
    check("AUXILIARY_KERNEL_IS_RETAINED", normal*kernel == sp.zeros(4, 1) and normal.rank() == 3)
    check("ACTUAL_RESIDUAL_UNIQUE_ALONG_KERNEL", sp.simplify(residual-tt*W.inv()*kernel) == sp.zeros(4, 1))
    Aeff = sp.factor(2*(residual.T*W*residual)[0])
    check("GENUINELY_NONPOLYNOMIAL_AUXILIARY_PROFILE", Aeff == (1+s)/(2+s) and sp.diff(Aeff, s, 3).subs(s, 0) == sp.Rational(3, 8))
    check("AUXILIARY_GATE_NOT_FULL_EDGE_GATE", sp.simplify(4*W*residual-4*tt*kernel) == sp.zeros(4, 1) and tt.subs(s, 0) != 0)

    # Negative controls: boundaries that must not be lost in a completeness claim.
    total_mu = [1+s, 1-s]
    check("TOTAL_VOLUME_IS_NOT_POINTWISE_DENSITY", sum(total_mu) == 2 and sp.diff(total_mu[0]+2*total_mu[1], s) == -1)
    check("SHAPE_DEPENDENT_OPERATOR_IS_OUTSIDE_CLASS", sp.diff(g[0, 0]/w**2, s) == 1)
    double_well = (z*z-1)**2
    check("GENERAL_CRITICAL_VALUES_NEED_NOT_BE_UNIQUE", sp.diff(double_well, z).subs(z, 0) == 0
          and sp.diff(double_well, z).subs(z, 1) == 0 and double_well.subs(z, 0) != double_well.subs(z, 1))
    mesh = sp.symbols("mesh", positive=True)
    check("SMALL_INPUT_ERROR_MAY_HAVE_ORDER_ONE_VALUE", sp.cancel((mesh-0)/mesh) == 1)
    check("RECORDING_ERROR_SCALE_CANNOT_REPAIR_CONSTANT", sp.limit(mesh/mesh**sp.Rational(1, 3), mesh, 0, dir='+') == 0 and derivative > 0)

    payload = {
        "status": "PASS", "input_head": INPUT_HEAD,
        "input_sha256": {path: hashlib.sha256((repo/path).read_bytes()).hexdigest() for path in INPUTS},
        "consumed_physical_probe": PROBE_INPUT,
        "lean_capsule_receipt_sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        "checks": checks,
        "gram": entries(g), "inverse": entries(inv), "pointwise_volume": str(volume),
        "ricci": entries(ricci), "standard_scalar": str(R), "owner_action_density": str(density),
        "periodic_action": str(action), "Einstein_probe_density": str(pairing),
        "strict_contrast_limit": str(derivative), "packed_metric_slots": len(slots), "volume_kernel_dimension": 9,
        "continuum_spin": [entries(om) for om in spin], "continuum_torsion_rows": 24,
        "finite_connection_status": "Consumed published all-24-row O(h^2) preparation theorem; no exact finite joint solution asserted.",
        "auxiliary_elimination": {"weights": entries(W), "phi": entries(phi), "residual": entries(residual),
            "kernel": entries(kernel), "profile": str(Aeff), "third_derivative": "3/8", "full_edge_gate": False},
        "scope": "All volume-factorized values and actual unique-value auxiliary preparations on the admitted curved pencil. No full-core completeness or exclusion of native metric-shape data.",
    }
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    expected = args.expect or (Path(__file__).with_name("a4d_native_volume_fiber_certificate.json") if not args.output else None)
    if expected:
        assert json.loads(expected.read_text()) == payload, "PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER", flush=True)
    print("PASS_NATIVE_VOLUME_FIBER_OBSTRUCTION", len(checks), flush=True)


if __name__ == "__main__":
    main()
