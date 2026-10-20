#!/usr/bin/env python3
"""Immutable exact controls for the owned finite commutator action and source.

General all-size first variations, Fredholm alternative and Ward identity are
compiled in the companion Lean capsule. No physical D(g), source or new action
is selected. The four-dimensional spectrum is an exact illustrative family,
not the A4D connection symbol or its complex resonance divisor.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as sp

INPUT_HEAD = "a4a0ee1ce0a48fe07da0da036e122262e8cc7d44"
INPUTS = [
    "03_FORMALIZATION/D0/Algebra/ArchiveCommutatorOperators.lean",
    "03_FORMALIZATION/D0/Algebra/GaugeKineticPositivity.lean",
    "03_FORMALIZATION/D0/Matter/GaugeCurvatureOrigin.lean",
    "03_FORMALIZATION/D0/Matter/VectorOperatorOrigin.lean",
    "03_FORMALIZATION/D0/Matter/VectorFieldEquation.lean",
    "03_FORMALIZATION/D0/Gauge/MatrixRepGaugeTransform.lean",
    "03_FORMALIZATION/D0/Gauge/NonAbelianDiscreteCurvature.lean",
    "03_FORMALIZATION/D0/Gauge/NonAbelianSeamObstructionGap.lean",
    "03_FORMALIZATION/D0/Matter/ArchiveStressCoupling.lean",
    "03_FORMALIZATION/D0/Matter/GenerationAnomalyPreservation.lean",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    checks = []

    def check(name, value):
        assert bool(value), name
        checks.append(name)
        print("PASS_" + name, flush=True)

    def sha(path):
        return hashlib.sha256((repo / path).read_bytes()).hexdigest()

    def equal(X, Y):
        if isinstance(X, sp.MatrixBase):
            return X.shape == Y.shape and all(sp.expand(z) == 0 for z in X-Y)
        return sp.expand(X-Y) == 0

    def entries(X):
        return [[str(z) for z in row] for row in X.tolist()]

    comm = lambda X, Y: X*Y-Y*X
    inner = lambda X, Y: sp.trace(X.T*Y)
    lap = lambda D, A: -comm(D, comm(D, A))
    response = lambda D, A: comm(A, comm(D, A))
    energy = lambda D, A: -sp.trace(comm(D, A)**2)/2
    receipt_path = "02_REGISTRY/research/certificates/a4d_native_vector_source_results.json"
    receipt = json.loads((repo/receipt_path).read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0
    assert receipt["printed_axiom_dependencies"] == 20 and not receipt["sorryAx"]
    for path, digest in {
        **receipt["transitive_d0_source_sha256"], **receipt["toolchain_input_sha256"],
        receipt["capsule"]: receipt["capsule_sha256"],
        receipt["output"]: receipt["output_sha256"],
    }.items():
        assert sha(path) == digest, "LEAN_INPUT_CHANGED: " + path
    check("COMPILED_ALL_SIZE_VARIATION_RANGE_AND_WARD_BINDINGS", True)

    pairs = [(i, j) for i in range(4) for j in range(i+1, 4)]
    basis = []
    for i, j in pairs:
        E = sp.zeros(4); E[i, j] = 1; E[j, i] = -1; basis.append(E)
    coordinates = lambda M: sp.Matrix([M[i, j] for i, j in pairs])
    combine = lambda v: sum((z*E for z, E in zip(v, basis)), sp.zeros(4))
    d = sp.symbols("d0:6", real=True)
    a = sp.symbols("u0:6", real=True)
    v = sp.symbols("v0:6", real=True)
    D, A, B = [combine(xs) for xs in (d, a, v)]
    K = comm(D, A); LA = lap(D, A); P = response(D, A)
    t, c = sp.symbols("t c", real=True)
    check("ALL_SIX_SKEW_COORDINATES_AND_FROBENIUS_WEIGHTS",
          len(pairs) == 6 and equal(inner(A, A), 2*sum(z*z for z in a)))
    check("LITERAL_CURVATURE_AND_NEGATIVE_DOUBLE_COMMUTATOR",
          K.T == -K and equal(LA.T, -LA) and equal(inner(A, LA), inner(K, K)))
    check("ALL_SIX_FIELD_DERIVATIVES_WITH_OWNER_NORMALIZATION",
          all(equal(sp.diff(energy(D, A), z), inner(LA, E)) for z, E in zip(a, basis)))
    check("ALL_SIX_BACKGROUND_DERIVATIVES_WITH_OWNER_NORMALIZATION",
          all(equal(sp.diff(energy(D, A), z), inner(P, E)) for z, E in zip(d, basis)))
    check("ARBITRARY_COEFFICIENT_FIELD_POLARIZATION", equal(2*c*energy(D, A+t*B),
          2*c*energy(D, A)+2*c*t*inner(LA, B)+c*t*t*inner(comm(D, B), comm(D, B))))
    check("JOINT_SIMULTANEOUS_VARIATION", equal(
          sp.diff(energy(D+t*B, A+t*B), t).subs(t, 0), inner(P, B)+inner(LA, B)))
    check("ACTUAL_JOINT_COMMUTATOR_WARD_ALL_ENTRIES", equal(comm(D, P)+comm(A, LA), sp.zeros(4)))
    check("HOMOGENEITY_IN_EACH_INDEPENDENT_FIELD", equal(inner(P, D), 2*energy(D, A))
          and equal(inner(LA, A), 2*energy(D, A)))
    check("SELF_COMMUTATOR_INTERACTION_IS_IDENTICALLY_ZERO", comm(A, A) == sp.zeros(4))

    # Complete six-dimensional spectrum for every displayed alpha,beta.
    alpha, beta = sp.symbols("alpha beta", real=True)
    D0 = alpha*basis[0]+beta*basis[5]
    L0 = sp.Matrix.hstack(*[coordinates(lap(D0, E)) for E in basis])
    modes = [basis[0], basis[5], basis[1]+basis[4], basis[2]-basis[3],
             basis[1]-basis[4], basis[2]+basis[3]]
    V = sp.Matrix.hstack(*[coordinates(M) for M in modes])
    lam = [0, 0, (alpha-beta)**2, (alpha-beta)**2, (alpha+beta)**2, (alpha+beta)**2]
    norms = [inner(M, M) for M in modes]
    check("COMPLETE_SIX_DIMENSIONAL_EIGENBASIS", V.det() != 0 and equal(L0*V, V*sp.diag(*lam)))
    check("EXACT_ORTHOGONAL_EIGENBASIS_NORMALIZATION",
          sp.Matrix([[inner(M, N) for N in modes] for M in modes]) == sp.diag(*norms)
          and norms == [2, 2, 4, 4, 4, 4])
    rank_data = {}
    for label, av, bv, rank in [
        ("regular", 1, 2, 4), ("equal", 1, 1, 2), ("opposite", 1, -1, 2),
        ("zero", 0, 0, 0), ("singular_D_positive_range_gap", 0, 2, 4),
    ]:
        DD = D0.subs({alpha: av, beta: bv})
        LL = L0.subs({alpha: av, beta: bv})
        rank_data[label] = {"D_determinant": str(DD.det()), "rank": LL.rank(),
                            "nullity": 6-LL.rank(), "spectrum": [str(z.subs({alpha: av, beta: bv})) if hasattr(z, "subs") else str(z) for z in lam]}
        check("EXACT_RANK_AND_COMMUTANT_"+label, LL.rank() == rank and all(
              equal(comm(DD, combine(w)), sp.zeros(4)) for w in LL.nullspace()))

    # Construct the inverse on the actual range without deleting its kernel.
    js = sp.symbols("j0:6", real=True)
    J = combine(js)
    inv_lam = [0, 0, 1/(alpha-beta)**2, 1/(alpha-beta)**2,
               1/(alpha+beta)**2, 1/(alpha+beta)**2]
    Lplus = V*sp.diag(*inv_lam)*V.inv()
    Prange = sp.diag(0, 1, 1, 1, 1, 0)
    check("REGULAR_RANGE_PROJECTOR_AND_PSEUDOINVERSE", sp.simplify(L0*Lplus) == Prange
          and sp.simplify(Lplus*L0) == Prange and sp.simplify(Lplus.T-Lplus) == sp.zeros(6))
    Aplus = combine(Lplus*sp.Matrix(js))
    check("SOURCE_COMPATIBILITY_EXACTLY_TWO_COMMUTANT_COMPONENTS",
          sp.simplify(lap(D0, Aplus)-J+js[0]*basis[0]+js[5]*basis[5]) == sp.zeros(4))
    incompatible = basis[0]
    check("NEGATIVE_EMPTY_SOURCE_FIBER", inner(incompatible, basis[0]) == 2
          and comm(D0, basis[0]) == sp.zeros(4)
          and sp.simplify(L0*(Lplus*coordinates(incompatible))) == sp.zeros(6, 1))
    check("SOURCE_MUST_NOT_BE_FITTED_AFTER_CHOOSING_FIELD",
          equal(lap(D, A), LA) and inner(incompatible, basis[0]) != 0)

    # Source-only solution fibers may share an action value but not a full
    # background derivative. All displayed fields really solve one fixed J.
    D1 = basis[0]+2*basis[5]; A1 = basis[1]; Z = basis[0]; J1 = lap(D1, A1)
    K1 = comm(D1, A1); dP = response(D1, A1+Z)-response(D1, A1)
    check("FIXED_SOURCE_NONEMPTY_FIBER_AND_KERNEL_SHIFT",
          lap(D1, A1+Z) == J1 and comm(D1, Z) == sp.zeros(4) and J1 != sp.zeros(4))
    check("REDUCED_WORK_VALUE_UNIQUE_ON_THIS_FIBER",
          energy(D1, A1+Z)-inner(J1, A1+Z) == energy(D1, A1)-inner(J1, A1)
          and energy(D1, A1)-inner(J1, A1) == -inner(J1, A1)/2)
    check("BACKGROUND_RESPONSE_CAN_DIFFER_ALONG_SOURCED_KERNEL",
          dP == comm(Z, K1) and dP != sp.zeros(4))
    check("SOURCED_KERNEL_SHIFT_IS_NOT_EVEN_ORTHOGONALLY_CONJUGATE",
          inner(A1, A1) == 2 and inner(A1+Z, A1+Z) == 4)
    check("FULL_SOURCED_WARD_RETAINS_KERNEL_DEPENDENCE",
          comm(D1, response(D1, A1))+comm(A1, J1) == sp.zeros(4)
          and comm(D1, dP)+comm(Z, J1) == sp.zeros(4))
    Btransverse = dP
    check("RESPONSE_DIFFERENCE_DETECTED_BY_VALID_SKEW_VARIATION",
          Btransverse.T == -Btransverse and inner(dP, Btransverse) > 0)
    # Differentiate [D(t), Z(t)]=0 and source compatibility on the kernel.
    # For a fixed source the exact identity yields <dP,deltaD>=-<J,deltaZ>.
    X = basis[2]; deltaD = comm(X, D1); deltaZ = comm(X, Z)
    check("KERNEL_TRANSPORT_DERIVATIVE", comm(deltaD, Z)+comm(D1, deltaZ) == sp.zeros(4))
    check("COMPATIBILITY_TANGENT_CONTROLS_PROFILE_DERIVATIVE",
          inner(dP, deltaD) == -inner(J1, deltaZ))

    # Constant-rank regular backgrounds, uniformly nonsingular and bounded,
    # but no uniform inverse. A fixed, independently declared source is used.
    delta = sp.symbols("delta", positive=True)
    Ddelta = basis[0]+(1+delta)*basis[5]
    T = basis[1]+basis[4]  # declared before A_delta; Frobenius norm is 2.
    Adelta = T/delta**2; Kdelta = comm(Ddelta, Adelta); Pdelta = response(Ddelta, Adelta)
    check("FIXED_SOURCE_EXACT_REFINING_SOLUTIONS", sp.simplify(lap(Ddelta, Adelta)-T) == sp.zeros(4))
    check("UNIFORM_D_NONSINGULARITY_IS_INSUFFICIENT", equal(Ddelta.det(), (1+delta)**2)
          and sp.expand(inner(Ddelta, Ddelta)) == 4+4*delta+2*delta**2
          and equal(Ddelta.T*Ddelta, sp.diag(1, 1, (1+delta)**2, (1+delta)**2)))
    check("SHARP_RANGE_INVERSE_IS_DELTA_MINUS_TWO",
          equal(lap(Ddelta, T), delta*delta*T)
          and sp.simplify(inner(Adelta, Adelta)) == 4/delta**4)
    check("SHARP_ENERGY_AND_BACKGROUND_RESPONSE_BLOWUP",
          sp.simplify(energy(Ddelta, Adelta)) == 2/delta**2
          and sp.simplify(Pdelta-2*(basis[5]-basis[0])/delta**3) == sp.zeros(4)
          and sp.simplify(inner(Pdelta, Pdelta)) == 16/delta**6)
    check("JOINT_WARD_DOES_NOT_BOUND_THE_RESPONSE",
          sp.simplify(comm(Ddelta, Pdelta)) == sp.zeros(4) and comm(Adelta, T) == sp.zeros(4))
    check("SMALL_RESIDUAL_IS_NOT_SMALL_STATE_ERROR",
          sp.simplify(lap(Ddelta, Adelta+T/delta)-T-delta*T) == sp.zeros(4)
          and sp.simplify(inner(T/delta, T/delta)) == 4/delta**2)
    for k in [1, 2, 4, 8, 16]:
        dd = sp.Rational(1, k); DL = Ddelta.subs(delta, dd); AL = Adelta.subs(delta, dd)
        LL = sp.Matrix.hstack(*[coordinates(lap(DL, E)) for E in basis])
        check("CONSTANT_RANK_FIXED_SOURCE_SEQUENCE_"+str(k), LL.rank() == 4
              and lap(DL, AL) == T and inner(AL, AL) == 4*k**4 and DL.det() >= 1
              and inner(DL, DL) <= 10)
    check("LIMIT_SOURCE_FIBER_IS_EMPTY", comm(Ddelta.subs(delta, 0), T) == sp.zeros(4)
          and inner(T, T) == 4)
    check("SOURCED_ROOT_IS_NOT_JOINT_BACKGROUND_STATIONARY",
          sp.simplify(inner(Pdelta, Ddelta)) == 4/delta**2)

    # Actual matrix conjugation, not an assumed local spacetime symmetry.
    U = sp.eye(4); U[0, 0] = U[2, 2] = sp.Rational(3, 5)
    U[0, 2] = sp.Rational(4, 5); U[2, 0] = -sp.Rational(4, 5)
    check("PROPER_ORTHOGONAL_CONJUGATION", U.T*U == sp.eye(4) and U.det() == 1)
    check("SIMULTANEOUS_CONJUGATION_IS_ACTUAL_ACTION_SYMMETRY",
          energy(U*D1*U.T, U*A1*U.T) == energy(D1, A1)
          and lap(U*D1*U.T, U*A1*U.T) == U*J1*U.T)
    check("FIXED_D_ARBITRARY_CONJUGATION_IS_NOT_GAUGE",
          comm(U, D1) != sp.zeros(4) and energy(D1, U*Z*U.T) != energy(D1, Z))
    check("KERNEL_AT_ZERO_IS_NOT_A_GAUGE_TANGENT",
          lap(D1, D1) == sp.zeros(4) and comm(X, sp.zeros(4)) == sp.zeros(4)
          and inner(D1, D1) > 0)

    # Hostile exceptions: both positivity and unconstrained variations matter.
    # so(1,2) has an indefinite trace form; nonzero curvature may be null and
    # even unsourced stationary for an admitted different Lie algebra.
    metric = sp.diag(1, -1, -1)
    N = sp.Matrix([[0, 1, 0], [1, 0, 1], [0, -1, 0]])
    H = sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]])
    KN = comm(N, H)
    check("INDEFINITE_LIE_ALGEBRA_IS_OUTSIDE_SKEW_OWNER",
          N.T*metric+metric*N == sp.zeros(3) and H.T*metric+metric*H == sp.zeros(3)
          and N.T != -N and H.T != -H)
    check("INDEFINITE_NULL_CURVATURE_PROTECTS_SCOPE",
          KN != sp.zeros(3) and sp.trace(KN*KN) == 0 and comm(N, KN) == sp.zeros(3))
    # A normalized sphere admits a nonzero eigenvector constrained critical
    # point; the native full free variation theorem does not include it.
    tangents = [basis[0], basis[5], basis[2], basis[3], basis[1]-basis[4]]
    check("NORMALIZED_CONSTRAINT_PROTECTS_NONZERO_CURVATURE",
          lap(D1, T) == T and comm(D1, T) != sp.zeros(4)
          and sp.Matrix.hstack(*[coordinates(M) for M in tangents]).rank() == 5
          and all(inner(T, M) == 0 and inner(lap(D1, T), M) == 0 for M in tangents))
    check("DELETING_BACKGROUND_VARIATIONS_PROTECTS_SOURCED_SOLUTIONS", J1 != sp.zeros(4)
          and lap(D1, A1) == J1 and response(D1, A1) != sp.zeros(4))
    check("ZERO_COEFFICIENT_IS_A_SEPARATE_DEGENERATE_ACTION", sp.expand((2*c*energy(D1, A1)).subs(c, 0)) == 0
          and comm(D1, A1) != sp.zeros(4))

    payload = {
        "status": "PASS", "input_head": INPUT_HEAD,
        "scope": "Existing finite real-skew commutator kinetic action; full free field variation, supplied-source range, independent background response. No selected physical D(g), source, metric Ward or refinement.",
        "inputs_sha256": {p: sha(p) for p in INPUTS},
        "lean_receipt_sha256": sha(receipt_path), "checks": checks,
        "basis_upper_slots": [list(p) for p in pairs], "normal_form_laplacian": entries(L0),
        "normal_form_spectrum": [str(z) for z in lam], "rank_strata": rank_data,
        "fixed_source": entries(T), "fixed_source_solution": entries(Adelta),
        "range_inverse_norm": "delta^(-2)", "fixed_source_field_norm": "2/delta^2",
        "fixed_source_energy": "2/delta^2", "background_response_norm": "4/delta^3",
        "kernel_shift_response": entries(dP), "indefinite_exception_curvature": entries(KN),
        "protected_exceptions": ["Constrained field variations", "Indefinite Lie algebra trace form",
            "Fixed background with compatible external source", "Additional independently owned action terms",
            "Nonlinear or shape-dependent physical state maps requiring separate owners"],
    }
    output = json.dumps(payload, sort_keys=True, indent=2)+"\n"
    if args.output:
        args.output.write_text(output)
    else:
        ledger = args.expect or Path(__file__).with_name("a4d_native_vector_source_certificate.json")
        assert ledger.read_text() == output, "PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER")
    print("PASS_NATIVE_VECTOR_SOURCE", len(checks))


if __name__ == "__main__":
    main()
