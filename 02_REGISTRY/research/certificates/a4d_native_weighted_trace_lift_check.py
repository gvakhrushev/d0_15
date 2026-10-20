#!/usr/bin/env python3
"""Exact controls for the weighted-trace, moving-lift and compensator boundaries.

General proofs: A4D_NATIVE_WEIGHTED_TRACE_LIFT_BOUNDARY.md.
Default replay is immutable; --output explicitly writes a new result ledger.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

INPUT_HEAD = "0af401558deca37468c077c40b53ac670a7ccaf3"
INPUTS = [
    "03_FORMALIZATION/D0/Geometry/ConformalLaplacianTrace.lean",
    "03_FORMALIZATION/D0/Geometry/HeatTraceEHProxy.lean",
    "03_FORMALIZATION/D0/Geometry/HeatTraceA2Decomposition.lean",
    "03_FORMALIZATION/D0/Cosmology/EntropyArchiveFlow.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCanonicalLaplacian.lean",
    "03_FORMALIZATION/D0/Geometry/ArchivePhaseDistance.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveSeamCurvature.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveLaplacianRG.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveHeatTrace.lean",
    "03_FORMALIZATION/D0/Gravity/A2CompensatorNoether.lean",
    "02_REGISTRY/research/A4D_NATIVE_QUADRATIC_GRAM_FLUX_BOUNDARY.md",
    "02_REGISTRY/research/certificates/a4d_native_quadratic_gram_flux_check.py",
    "02_REGISTRY/research/certificates/a4d_native_quadratic_gram_flux_results.json",
]


def entries(m):
    return [[str(x) for x in row] for row in m.tolist()]


def cycle(m):
    L = sp.zeros(m)
    for i in range(m):
        L[i, i] = 2
        L[i, (i-1) % m] -= 1
        L[i, (i+1) % m] -= 1
    return L


def norm2(m):
    return sp.expand(sum(x*x for x in m))


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

    receipt_path = Path(__file__).with_name("a4d_native_weighted_gate_results.json")
    receipt = json.loads(receipt_path.read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0
    assert not receipt["sorryAx"] and receipt["printed_axiom_dependencies"] == 7
    for path, digest in {
        **receipt["transitive_d0_source_sha256"], **receipt["toolchain_input_sha256"],
        receipt["capsule"]: receipt["capsule_sha256"],
        receipt["output"]: receipt["output_sha256"],
    }.items():
        assert hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest, "LEAN_INPUT_CHANGED: " + path

    s, eps, t = sp.symbols("s eps t", real=True)
    w = sp.symbols("w", positive=True)
    eta = sp.diag(1, -1, -1, -1)
    u, n = sp.Matrix([1, 0, 0, 0]), sp.Matrix([1, 1, 0, 0])
    theta = w*eta+s*u*n.T
    g = theta*eta*theta.T
    mu = w**3*(w+s)
    check("LITERAL_GRAM_VOLUME_SQUARE", sp.factor(g.det()) == -mu**2)
    check("VOLUME_PENCIL_AFFINE_AND_DENSITY_NONLINEAR", sp.diff(mu, s, 2) == 0
          and sp.diff(1/mu, s, 2) != 0)

    rho = sp.symbols("rho0:3", positive=True)
    L = cycle(3)
    proxy = sum(L[i, j]**2/(rho[i]*rho[j]) for i in range(3) for j in range(3) if i != j)
    inv_proxy = sum(L[i, j]**2*(1/rho[i])*(1/rho[j]) for i in range(3) for j in range(3) if i != j)
    check("PROXY_LITERAL_INVERSE_VOLUME", sp.cancel(proxy-inv_proxy) == 0)
    archive_volume = sum(1/r for r in rho)/3
    check("REGULAR_TRACE_VOLUME_NORMALIZATION", sp.cancel(sum(L[i, i]/rho[i] for i in range(3))/6-archive_volume) == 0)
    W = sp.diag(*[1/sp.sqrt(r) for r in rho])
    weighted = W*L*W
    diagonal = sum(L[i, i]**2/rho[i]**2 for i in range(3))
    check("ALL_TRACE_SQUARE_TERMS_AND_HALF_PROXY_FACTOR", sp.simplify(sp.trace(weighted**2)-diagonal-2*(proxy/2)) == 0)
    check("FREE_DENSITY_SCALING_EULER", sp.cancel(sum(rho[i]*sp.diff(proxy, rho[i]) for i in range(3))+2*proxy) == 0)
    check("FREE_DENSITY_GATE_NOT_CANONICAL_ROOT", proxy.subs(dict(zip(rho, [1]*3))) == 6)
    check("MASS_CONSTRAINT_EXCLUDES_UNIFORM_METRIC_SCALE",
          sp.diff(sum(rho)/(1+t)**2, t).subs(t, 0) == -2*sum(rho))

    # No symmetry hypothesis for the trace cyclicity identity.
    sqrt_mu = sp.diag(*sp.symbols("r0:3", positive=True))
    fixed_L = sp.Matrix([[2, -1, 0], [-2, 3, -1], [1, -2, 4]])
    for p in range(1, 5):
        check(f"CYCLIC_MOMENT_IDENTITY_{p}", sp.expand(sp.trace((sqrt_mu*fixed_L*sqrt_mu)**p)
              -sp.trace((sqrt_mu**2*fixed_L)**p)) == 0)
    wi = [sp.Rational(9, 10), sp.Integer(1), sp.Rational(11, 10)]
    site_mu = [a**3*(a+s) for a in wi]
    polynomial_moments = []
    for p in range(1, 7):
        moment = sp.expand(sp.trace((sp.diag(*site_mu)*fixed_L)**p))
        polynomial_moments.append(moment)
        check(f"MOVING_WEIGHT_MOMENT_DEGREE_{p}", sp.Poly(moment, s).degree() == p)
    pencil_proxy = sp.cancel(proxy.subs(dict(zip(rho, [1/a for a in site_mu]))))
    check("ACTUAL_PROXY_IS_QUADRATIC_ON_CURVED_VOLUME_PENCIL", sp.Poly(pencil_proxy, s).degree() == 2)
    product = polynomial_moments[0]*polynomial_moments[1]-7*polynomial_moments[2]
    check("SIGNED_PRODUCTS_KEEP_WEIGHTED_DEGREE", sp.Poly(product, s).degree() <= 3)

    for D in range(1, 7):
        a = sp.symbols(f"a0:{D+1}")
        F = sum(a[i]*s**i for i in range(D+1))
        secant = sp.cancel((F.subs(s, s+eps)-F.subs(s, s-eps))/(2*eps))
        anchors = [sp.Rational(j, 8*D)-sp.Rational(1, 16) for j in range(D)]
        interpolated = sum(secant.subs(s, x)*sp.prod((s-y)/(x-y) for y in anchors if y != x) for x in anchors)
        check(f"FINITE_ANCHOR_SECANT_IDENTITY_DEGREE_{D}", sp.Poly(secant, s).degree() <= D-1
              and sp.expand(secant-interpolated) == 0)
    C = (s+2*w)*(5*s+6*w)/(4*w*(s+w))
    check("EINSTEIN_COEFFICIENT_EXACT_RECIPROCAL", sp.cancel(C-5*s/(4*w)-sp.Rational(11, 4)-w/(4*(w+s))) == 0)
    check("CONSTANT_ACTION_FAILS_FIRST_VARIATION", sp.diff(C, s).subs(s, 0) == 1/w)
    for k in range(2, 11):
        check(f"NONZERO_EINSTEIN_DERIVATIVE_{k}", sp.factor(sp.diff(C, s, k).subs(s, 0)) == (-1)**k*sp.factorial(k)/(4*w**k))
    y = sp.symbols("y", real=True)
    omega = 1+sp.cos(2*sp.pi*y)/10
    check("STRICT_ALL_ORDER_INTEGRAL_BOUND_INPUT", sp.integrate(sp.diff(omega, y)**2, (y, 0, 1)) == sp.pi**2/50)
    for D in (2, 4, 8):
        trunc = sp.series(C, s, 0, D+1).removeO()
        check(f"GROWING_DEGREE_EXCEPTION_{D}", sp.cancel(C-trunc) == sp.cancel((-s/w)**(D+1)/(4*(1+s/w))))
    check("NONLINEAR_VOLUME_MAP_OUTSIDE_CLASS", sp.diff(sp.exp(s), s, 3) != 0)
    check("MOVING_OPERATOR_OUTSIDE_CLASS", sp.denom(sp.cancel(1/(1+s))) != 1)
    check("NONPOLYNOMIAL_SPECTRAL_CUTOFF_OUTSIDE_CLASS", sp.diff(sp.exp(-s), s, 3) != 0)

    lam = sp.Symbol("lam")
    z, zz = sp.symbols("z zz", nonzero=True)
    check("EIGENVALUE_COINCIDENCE_FACTOR", sp.expand((z-zz)*(z-1/zz)-(z*z-(zz+1/zz)*z+1)) == 0)
    gcds = {}
    for m in range(3, 19):
        cm = cycle(m).charpoly(lam).as_expr()
        cf = cycle(m+1).charpoly(lam).as_expr()
        gcd = sp.Poly(sp.gcd(cm, cf), lam).monic().as_expr()
        gcds[str(m)] = str(gcd)
        check(f"ADJACENT_CYCLE_CHARPOLY_GCD_{m}", gcd == lam)
    kernels = {}
    for m in range(3, 7):
        Lc, Lf = cycle(m), cycle(m+1)
        K = sp.kronecker_product(sp.eye(m), Lf)-sp.kronecker_product(Lc.T, sp.eye(m+1))
        kernel = K.nullspace()
        kernels[str(m)] = len(kernel)
        check(f"ALL_LINEAR_LIFT_KERNEL_{m}", len(kernel) == 1 and kernel[0] == sp.ones(m*(m+1), 1))
        P = sp.ones(m+1, m)/m
        J0 = sp.Matrix(m+1, m, lambda i, j: int(j == i % m))
        Jt = (1-t)*J0+t*P
        check(f"UNCONSTRAINED_LIFT_DESCENT_{m}", norm2(Lf*Jt-Jt*Lc) == sp.expand(4*(1-t)**2)
              and Lf*P-P*Lc == sp.zeros(m+1, m))
        delta = sp.symbols("delta", positive=True)
        Jdelta = P+delta*(J0-P)
        check(f"SMALL_RESIDUAL_INJECTIVE_EXCEPTION_{m}", norm2(Lf*Jdelta-Jdelta*Lc) == 4*delta**2
              and sp.factor(Jdelta[:m, :].det()) == delta**(m-1))

    x = sp.symbols("x0:4", real=True)
    Jlocal = sp.zeros(4, 3)
    for i in range(4):
        Jlocal[i, i % 3] = 1-x[i]
        Jlocal[i, (i+1) % 3] = x[i]
    Sloc = norm2(cycle(4)*Jlocal-Jlocal*cycle(3))
    stationary = dict(zip(x, [sp.Rational(1, 2), sp.Rational(5, 8), sp.Rational(3, 8), sp.Rational(1, 2)]))
    root = Jlocal.subs(stationary)
    Hess = sp.hessian(Sloc, x)
    check("LOCAL_LIFT_ALL_ADMITTED_ROWS_STATIONARY", all(sp.diff(Sloc, xx).subs(stationary) == 0 for xx in x))
    check("LOCAL_LIFT_STRICT_MINIMUM", all(Hess[:k, :k].det() > 0 for k in range(1, 5)))
    check("LOCAL_LIFT_NONEMPTY_INJECTIVE_POSITIVE_ACTION", root.rank() == 3 and Sloc.subs(stationary) == sp.Rational(3, 4)
          and all(0 < xx < 1 for xx in stationary.values()))
    check("DENSE_DESCENT_VIOLATES_LOCAL_SUPPORT", root[0, 2] == 0 and (sp.ones(4, 3)/3-root)[0, 2] != 0)
    Jcover = sp.Matrix(6, 3, lambda i, j: int(i % 3 == j))
    check("NONADJACENT_CYCLE_INJECTIVE_EXCEPTION", Jcover.rank() == 3 and cycle(6)*Jcover-Jcover*cycle(3) == sp.zeros(6, 3))

    # Every edge and vertex row of the literal rational compensator action.
    B = sp.Matrix(4, 4, lambda i, j: int(i == j)+int(i == (j+1) % 4))
    hs = sp.Matrix(sp.symbols("h0:4"))
    etas = sp.Matrix(sp.symbols("eta0:4"))
    weights = sp.symbols("W0:4", positive=True)
    Wdiag = sp.diag(*weights)
    residual = hs-B.T*etas/2
    A = sp.expand(2*(residual.T*Wdiag*residual)[0])
    Eh = sp.Matrix([sp.diff(A, xx) for xx in hs])
    Eeta = sp.Matrix([sp.diff(A, xx) for xx in etas])
    check("ALL_COMPENSATOR_EDGE_EULER_ROWS", sp.expand(Eh-4*Wdiag*residual) == sp.zeros(4, 1))
    check("ALL_COMPENSATOR_VERTEX_EULER_ROWS", sp.expand(Eeta+2*B*Wdiag*residual) == sp.zeros(4, 1))
    check("LITERAL_DIAGONAL_NORMALIZATION_AND_WARD", sp.expand(2*Eeta+B*Eh) == sp.zeros(4, 1))
    substitution = dict(zip(hs, B.T*etas/2))
    check("FULL_EDGE_GATE_VALUE_AND_SOURCE_ZERO", sp.expand(A.subs(substitution, simultaneous=True)) == 0
          and sp.expand(Eeta.subs(substitution, simultaneous=True)) == sp.zeros(4, 1))
    check("FULL_GATE_ALL_WEIGHT_VARIATIONS_ZERO", all(sp.expand(sp.diff(A, ww).subs(substitution, simultaneous=True)) == 0 for ww in weights))
    Wnum = sp.diag(sp.Rational(1, 2), sp.Rational(1, 6), sp.Rational(1, 12), sp.Rational(1, 4))
    k = sp.Matrix([1, -1, 1, -1])
    hedge = Wnum.inv()*k
    check("AUXILIARY_ONLY_GATE_IS_NONEMPTY", B*Wnum*hedge == sp.zeros(4, 1))
    check("AUXILIARY_ONLY_GATE_NOT_FULL_GATE", 4*Wnum*hedge == 4*k and 2*(hedge.T*Wnum*hedge)[0] == 48)
    # A singular weight invalidates the positive-weight gate implication.
    check("DEGENERATE_WEIGHT_EXCEPTION", sp.diag(1, 0)*sp.Matrix([0, 1]) == sp.zeros(2, 1))

    payload = {
        "status": "PASS", "input_head": INPUT_HEAD,
        "input_sha256": {p: hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in INPUTS},
        "lean_capsule_receipt_sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        "checks": checks,
        "weighted_trace": {"physical_volume_pencil": str(mu), "proxy_profile": str(pencil_proxy),
            "Einstein_coefficient": str(sp.factor(C)), "all_order_derivative": "(-1)^k k!/4 * integral(Omega'^2/Omega^k), k>=2",
            "hypotheses": "uniformly bounded degree, fixed L, admitted pencil and literal sitewise volume map; no variable-coefficient auxiliary elimination"},
        "moving_lift": {"adjacent_characteristic_gcd": gcds, "finite_full_intertwiner_nullities": kernels,
            "local_constrained_root": entries(root), "local_action": "3/4", "local_rank": 3,
            "local_Hessian": entries(Hess), "all_size_full_gate": "unique unital root is the rank-one constant projector",
            "approximate_exception": "rank m, seam action 4 delta^2; inverse degenerates"},
        "compensator": {"full_gate": "residual zero", "auxiliary_only_root": entries(hedge),
            "auxiliary_only_action": "48", "auxiliary_only_edge_response": entries(4*k)},
        "scope": "Scoped general analytic classifications with exact finite controls and literal Lean owner identities; no complete-core or positive-GR assertion.",
    }
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    expected = args.expect or (Path(__file__).with_name("a4d_native_weighted_trace_lift_results.json") if not args.output else None)
    if expected:
        assert json.loads(expected.read_text()) == payload, "PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER", flush=True)
    print("PASS_NATIVE_WEIGHTED_TRACE_LIFT_BOUNDARY", len(checks), flush=True)


if __name__ == "__main__":
    main()
