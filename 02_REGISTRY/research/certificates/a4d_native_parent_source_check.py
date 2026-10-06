#!/usr/bin/env python3
"""Exact source controls for the existing mixed primal/dual parent action.

No physical star or new action is selected. Generic proofs and the quantitative
bound are stated in A4D_NATIVE_PARENT_SOURCE_BOUNDARY.md; immutable default replay.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as sp

INPUT_HEAD = "8b96338505395dabf509e13422089d89685483b8"
INPUTS = [
    "03_FORMALIZATION/D0/Geometry/FinitePrimalDualHodgeParent.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveMetricMeasureHodgeLift.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveWeightedHodgeDirac.lean",
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    ap.add_argument("--output", type=Path)
    ap.add_argument("--expect", type=Path)
    args = ap.parse_args(); repo = args.repo.resolve(); checks = []
    sha = lambda p: hashlib.sha256((repo/p).read_bytes()).hexdigest()

    def check(name, value):
        assert bool(value), name
        checks.append(name); print("PASS_"+name, flush=True)

    def zero(X):
        return all(sp.factor(z) == 0 for z in X) if isinstance(X, sp.MatrixBase) else sp.factor(X) == 0

    entries = lambda M: [[str(z) for z in row] for row in M.tolist()]
    dot = lambda x, y: (x.T*y)[0]
    form = lambda M, K, p, x, l: dot(x, M*x)/2+dot(l, M*x-K*p)
    equations = lambda M, K, p, x, l: (-K.T*l, M*(x+l), M*x-K*p)
    source = lambda U, V, p, x, l: dot(x, U*x)/2+dot(l, U*x-V*p)
    receipt_path = "02_REGISTRY/research/certificates/a4d_native_parent_source_results.json"
    receipt = json.loads((repo/receipt_path).read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0
    assert receipt["printed_axiom_dependencies"] == 16 and not receipt["sorryAx"]
    for path, digest in {**receipt["transitive_d0_source_sha256"], **receipt["toolchain_input_sha256"],
                         receipt["capsule"]: receipt["capsule_sha256"], receipt["output"]: receipt["output_sha256"]}.items():
        assert sha(path) == digest, "LEAN_INPUT_CHANGED: "+path
    check("COMPILED_ACTUAL_PARENT_VARIATION_AND_SOURCE_BINDINGS", True)

    m0, m1, m2, t = sp.symbols("m0 m1 m2 t", real=True)
    M = sp.Matrix([[m0, m1], [m1, m2]])
    K = sp.Matrix(2, 2, sp.symbols("k0:4", real=True))
    p, x, l, v = [sp.Matrix(sp.symbols(prefix+"0:2", real=True)) for prefix in ["p", "x", "l", "v"]]
    U = sp.Matrix(2, 2, sp.symbols("u0:4", real=True))
    V = sp.Matrix(2, 2, sp.symbols("vop0:4", real=True))
    F = form(M, K, p, x, l); r = equations(M, K, p, x, l)
    for label, fields, rhs in zip(["FIELD", "AUXILIARY", "MULTIPLIER"], [p, x, l], r):
        check("ALL_"+label+"_EULER_ROWS", zero(sp.Matrix([sp.diff(F, z) for z in fields])-rhs))
    check("FIELD_EXACT_AFFINE_VARIATION", zero(form(M, K, p+t*v, x, l)-F-t*dot(r[0], v)))
    check("AUXILIARY_EXACT_QUADRATIC_VARIATION", zero(form(M, K, p, x+t*v, l)-F-t*dot(r[1], v)-t*t*dot(v, M*v)/2))
    check("MULTIPLIER_EXACT_AFFINE_VARIATION", zero(form(M, K, p, x, l+t*v)-F-t*dot(r[2], v)))
    check("ALL_CONSTITUTIVE_DERIVATIVES_WITH_SIGNS", zero(form(M+t*U, K+t*V, p, x, l)-F-t*source(U, V, p, x, l)))
    check("COERCIVE_EULER_BALANCE_WITHOUT_RANGE_INVERSE", zero(dot(x, M*x)-dot(x, r[1])+dot(l, r[2])-dot(p, r[0])))
    check("ON_SHELL_CONSTITUTIVE_RELATION", zero(source(U, V, p, x, -x)+dot(x, U*x)/2-dot(x, V*p)))
    check("POSITIVE_ROOT_ZERO_SOURCE_FOR_EVERY_OPERATOR_VARIATION", source(U, V, p, sp.zeros(2, 1), sp.zeros(2, 1)) == 0)
    check("INDEPENDENT_IDENTITY_DIRECTION_DETECTS_AUXILIARY", zero(source(sp.eye(2), sp.zeros(2), p, x, -x)+dot(x, x)/2))

    # Bind an arbitrary supplied matrix pairing, including rectangular R,
    # to the actual four-slot operator composition before using normal form.
    R = sp.Matrix([[1, 0, 2], [0, 1, -1]])
    S0 = sp.Matrix([[2, 1], [1, 3], [1, -1]])
    dP = sp.Matrix([[1, 2], [-1, 0], [0, 1]])
    S1 = sp.Matrix([[1, 0, 1], [0, 2, -1], [2, 1, 0], [1, -1, 1]])
    dD = sp.Matrix([[1, 0, 2, 1], [0, 1, -1, 2], [1, 1, 0, -1]])
    raw = dot(x, R*S0*x)/2+dot(l, R*(S0*x-dD*S1*dP*p))
    check("RECTANGULAR_LITERAL_PAIRING_AND_OPERATOR_BINDING", zero(raw-form(R*S0, R*dD*S1*dP, p, x, l)))

    # Exact auxiliary elimination is a change of variables in the old action.
    Minv = M.inv(); Q = K.T*Minv*K
    eta, zeta = [sp.Matrix(sp.symbols(prefix+"0:2", real=True)) for prefix in ["eta", "zeta"]]
    xx = Minv*K*p
    check("EXACT_ELIMINATION_INTO_SQUARED_OPERATOR", zero(
          form(M, K, p, xx+eta, -xx+zeta)-dot(p, Q*p)/2-dot(eta, M*eta)/2-dot(zeta, M*eta)))
    check("ELIMINATED_FIELD_OPERATOR_IS_K_TRANSPOSE_M_INV_K", zero(equations(M, K, p, xx, -xx)[0]-Q*p)
          and zero(equations(M, K, p, xx, -xx)[1]) and zero(equations(M, K, p, xx, -xx)[2]))
    check("ELIMINATED_ACTION_VALUE_IS_POSITIVE_SQUARE_WHEN_M_POSITIVE", zero(form(M, K, p, xx, -xx)-dot(K*p, Minv*K*p)/2))
    check("SYMMETRIC_CONSTITUTIVE_PACKED_FACTOR_TWO", zero(sp.diff(F, m1)-(x[0]*x[1]+l[0]*x[1]+l[1]*x[0])))

    cases = [
        ("positive_full_rank", sp.diag(2, 3), sp.Matrix([[1, 2], [0, 1]])),
        ("positive_kernel", sp.diag(2, 3), sp.ones(2)),
        ("indefinite_regular", sp.diag(1, -1), sp.eye(2)),
        ("indefinite_radical", sp.diag(1, -1), sp.Matrix([[1, 0], [1, 0]])),
        ("indefinite_three", sp.diag(1, -1, 2), sp.Matrix([[1, 0, 0], [1, 0, 0], [0, 1, 0]])),
        ("positive_four", sp.diag(1, 2, 3, 4), sp.diag(0, 1, 2, 3)),
    ]
    strata = {}
    for name, MM, KK in cases:
        n = MM.rows; QQ = KK.T*MM.inv()*KK; Z = sp.zeros(n)
        HH = sp.BlockMatrix([[Z, Z, -KK.T], [Z, MM, MM], [-KK, MM, Z]]).as_explicit()
        kernel = QQ.nullspace(); reduced = sp.Matrix.hstack(*[sp.Matrix.vstack(z, MM.inv()*KK*z, -MM.inv()*KK*z) for z in kernel]) if kernel else sp.zeros(3*n, 0)
        check("COMPLETE_PARENT_HESSIAN_KERNEL_"+name, HH.rank() == 2*n+QQ.rank()
              and HH*reduced == sp.zeros(3*n, reduced.cols) and reduced.rank() == n-QQ.rank())
        # Image radical dimension = dim ker Q - dim ker K.
        Y = sp.Matrix.hstack(*KK.columnspace()) if KK.rank() else sp.zeros(n, 0)
        Gram = Y.T*MM.inv()*Y
        check("IMAGE_RADICAL_CLASSIFICATION_"+name, KK.rank()-QQ.rank() == Gram.cols-Gram.rank())
        strata[name] = {"M": entries(MM), "K": entries(KK), "Q": entries(QQ),
            "rank_parent_Hessian": HH.rank(), "rank_K": KK.rank(), "rank_Q": QQ.rank(),
            "source_visible_kernel_quotient_dimension": KK.rank()-QQ.rank()}

    # Reproduce, rather than erase, the earlier indefinite pointwise source.
    q = sp.symbols("q", real=True)
    Ms = sp.Matrix([[0, 1], [1, 0]]); Ks = sp.Matrix([[0, q], [q, 1]])
    ps = sp.Matrix([0, 1]); xs = sp.Matrix([1, 0]); ls = -xs
    rs = equations(Ms, Ks, ps, xs, ls); Qs = Ks.T*Ms.inv()*Ks
    check("INDEFINITE_NONZERO_POINTWISE_SOURCE_IS_REAL", all(zero(z.subs(q, 0)) for z in rs)
          and form(Ms, Ks, ps, xs, ls).subs(q, 0) == 0 and sp.diff(form(Ms, Ks, ps, xs, ls), q) == 1)
    check("INDEFINITE_SOURCE_ROOT_HAS_NO_NEIGHBORING_CONTINUATION", Qs.det() == -q**4
          and Qs.subs(q, 0) == sp.zeros(2))
    check("INDIVIDUAL_BACKGROUND_DIRECTION_MAY_MISS_SOURCE", source(Ms, sp.zeros(2), ps, xs, ls) == 0
          and source(sp.eye(2), sp.zeros(2), ps, xs, ls) == -sp.Rational(1, 2))
    # Tangential transport of an indefinite kernel can have zero pulled-back source.
    Kt = sp.diag(0, 1+q); pt = sp.Matrix([0, 1]); xt = Ms*Kt*pt
    lt = -xt
    check("CONTINUING_INDEFINITE_ROOT_HAS_ZERO_TANGENTIAL_RESPONSE",
          all(zero(z) for z in equations(Ms, Kt, pt, xt, lt))
          and zero(source(sp.zeros(2), sp.diff(Kt, q), pt, xt, lt)))

    # Quantitative near-gate source estimate and each of its real hypotheses.
    h = sp.symbols("h", positive=True)
    scalar = lambda z: sp.Matrix([[z]])
    pm = scalar(1); xm = scalar(h); lm = scalar(-h)
    rm = equations(scalar(1), scalar(h), pm, xm, lm)
    check("SHARP_SQUARE_ROOT_RESIDUAL_SOURCE", rm == (scalar(h*h), scalar(0), scalar(0))
          and source(scalar(0), scalar(1), pm, xm, lm) == h
          and form(scalar(1), scalar(h), pm, xm, lm) == h*h/2)
    check("VANISHING_COERCIVITY_BREAKS_SOURCE_BOUND", equations(scalar(h*h), scalar(h*h), scalar(1), scalar(1), scalar(-1)) ==
          (scalar(h*h), scalar(0), scalar(0))
          and source(scalar(0), scalar(1), scalar(1), scalar(1), scalar(-1)) == 1)
    check("UNBOUNDED_FIELD_BREAKS_SOURCE_BOUND", equations(scalar(1), scalar(h*h), scalar(h**-2), scalar(1), scalar(-1)) ==
          (scalar(h*h), scalar(0), scalar(0))
          and source(scalar(0), scalar(1), scalar(h**-2), scalar(1), scalar(-1)) == h**-2)
    check("UNBOUNDED_CONSTITUTIVE_VARIATION_BREAKS_SOURCE_BOUND", source(scalar(0), scalar(1/h), pm, xm, lm) == 1)
    # Check the exact residual identity on independent rational cases as well.
    for n in [1, 2, 3, 4]:
        MM = sp.diag(*range(1, n+1)); KK = sp.Matrix(n, n, lambda i,j: sp.Rational((i+1)*(j+2), n+1))
        pp = sp.Matrix(range(1, n+1)); xx = sp.Matrix([(-1)**i for i in range(n)]); ll = sp.Matrix([sp.Rational(i+1, 3) for i in range(n)])
        rr = equations(MM, KK, pp, xx, ll)
        Z2 = dot(pp, pp)+dot(xx, xx)+dot(ll, ll); R2 = sum(dot(z, z) for z in rr)
        balance = dot(xx, rr[1])-dot(ll, rr[2])+dot(pp, rr[0])
        check("DIMENSION_FREE_RESIDUAL_CONTROL_"+str(n), balance == dot(xx, MM*xx)
              and balance >= dot(xx, xx) and balance*balance <= Z2*R2)
    # Degenerate pairing does not enforce the hidden raw constraint.
    Rbad = sp.Matrix([[1, 0]]); Sbad = sp.Matrix([1, 0]); Kbad = sp.Matrix([0, 1])
    check("DEGENERATE_PAIRING_PROTECTS_RAW_CONSTRAINT_SCOPE", Rbad*Sbad == scalar(1) and Rbad*Kbad == scalar(0)
          and all(zero(z) for z in equations(Rbad*Sbad, Rbad*Kbad, scalar(1), scalar(0), scalar(0)))
          and Sbad*scalar(0)-Kbad*scalar(1) != sp.zeros(2, 1))
    check("SEMIDEFINITE_IS_NOT_STRICT_POSITIVE", all(zero(z) for z in equations(scalar(0), scalar(0), scalar(0), scalar(1), scalar(0)))
          and source(scalar(1), scalar(0), scalar(0), scalar(1), scalar(0)) == sp.Rational(1, 2))
    PP = sp.Matrix([1, 0]); XX = PP; LL = -PP; KK = sp.diag(1, 2)
    check("NORMALIZATION_CONSTRAINT_PRESERVES_NONZERO_SOURCE", equations(sp.eye(2), KK, PP, XX, LL) == (PP, sp.zeros(2, 1), sp.zeros(2, 1))
          and dot(PP, sp.Matrix([0, 1])) == 0 and source(sp.zeros(2), sp.diag(1, 0), PP, XX, LL) == 1)
    check("AUXILIARY_ONLY_GATE_IS_INSUFFICIENT", equations(sp.eye(2), KK, PP, XX, LL)[0] != sp.zeros(2, 1)
          and form(sp.eye(2), KK, PP, XX, LL) == sp.Rational(1, 2))

    payload = {"status": "PASS", "input_head": INPUT_HEAD,
        "scope": "Existing homogeneous mixed parent, actual supplied linear pairing, symmetric scalar form. Complete positive pointwise source classification; nondegenerate indefinite source relation and image radical; no selected metric or matter action.",
        "inputs_sha256": {p: sha(p) for p in INPUTS}, "lean_receipt_sha256": sha(receipt_path),
        "checks": checks, "finite_strata": strata, "indefinite_reduced_operator": entries(Qs),
        "positive_source": "0", "residual_source_exponent": "1/2",
        "quantitative_hypotheses": ["uniform positive scalar-form lower bound", "bounded full field norm", "bounded constitutive variation norms", "all three Euler residuals controlled in matching norms"],
        "indefinite_pointwise_source": "1", "indefinite_neighbor_determinant": "-q^4",
        "protected_exceptions": ["Indefinite or degenerate scalar form", "Missing field equation or normalized constraints", "Degenerate raw pairing", "Unbounded fields, inverse scalar form or variations", "Additional native action terms with their own owners"]}
    out = json.dumps(payload, sort_keys=True, indent=2)+"\n"
    if args.output: args.output.write_text(out)
    else:
        ledger = args.expect or Path(__file__).with_name("a4d_native_parent_source_certificate.json")
        assert ledger.read_text() == out, "PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER")
    print("PASS_NATIVE_PARENT_SOURCE", len(checks))


if __name__ == "__main__": main()
