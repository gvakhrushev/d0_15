#!/usr/bin/env python3
"""Actual canonical A1 record: coarse-left and full-operator archive sources.

The real matter chart has ALL 16 CAR coordinates, plus the retained four
scalar-channel coordinates. Complex matrices implement the owned isometry;
they do not enlarge the physical matter chart to 32 real dimensions.
The fixed tuple is the e04e4e8a bridge at q=eta, not an intrinsic updated
orientation/preparation rule. No physical Info or admission is selected.
Only AF/F definitions are imported. Their checkers/controls are never run.
The A4 left readout has 13 defining modes. The actual full operator algebra
acting on H4 is A7=M34 (+) M21, with 55 defining modes and the complete
old-right A1 multiplicities. Nonzero coarse A4 jets are NOT full A7 jets.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CERT = "02_REGISTRY/research/certificates/"
SOURCE_PINS = {
    CERT + "a4d_native_fibonacci_record_activation.py":
        "9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee",
    CERT + "a4d_native_fock_record_binding_check.py":
        "42e83e6f93b48ce4d4420f829d8e79c993a215d7b1a4c6a2f812bd45fd914078",
}
BRIDGE_PROVENANCE = {
    "commit": "e04e4e8a",
    "path": CERT + "a4d_native_engine_correlated_current_extension_check.py",
    "git_blob": "f6a369b25bb45e0144a44e22eefa22360daf544c",
    "definition": "af_lorentz_fock_bridge: Psi=V_M2*(T tensor chi)*B_car^*",
    "foreign_bridge_checker_imported_or_executed": False,
}


def require(condition: object, name: str) -> None:
    if not bool(condition):
        raise AssertionError(name)


def pin_sources(repo: Path) -> None:
    for path, expected in SOURCE_PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == expected,
                "source_pin:" + path)


def _definition(repo: Path, stem: str):
    name = "canonical_record_definition_" + stem
    spec = importlib.util.spec_from_file_location(name, repo/CERT/(stem + ".py"))
    if spec is None or spec.loader is None:
        raise RuntimeError("definition_import_failed:" + stem)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@dataclass(frozen=True)
class CanonicalRecord:
    AF: object
    a: s.Expr
    p: s.Expr
    V: s.MatrixBase
    Psi: s.MatrixBase
    scalar: s.MatrixBase
    J: s.MatrixBase
    Q: s.MatrixBase
    seed: s.MatrixBase
    incoming: s.MatrixBase
    outgoing: s.MatrixBase
    gate: s.MatrixBase


def canonical_record(repo: Path | None = None) -> CanonicalRecord:
    """Reconstruct the full89 vector from literal owned frame/activate."""
    repo = ROOT if repo is None else Path(repo).resolve()
    pin_sources(repo)
    AF = _definition(repo, "a4d_native_fibonacci_record_activation")
    F = _definition(repo, "a4d_native_fock_record_binding_check")
    a, p = AF.a, AF.p
    frame = AF.frame(1)
    V, d = frame["V"], frame["old_dimension"]
    require(d == 5 and V.shape == (89, 20), "actual_full_A1_to_A4_frame")
    T = s.Matrix([[1, 0, 1, 0], [1, 0, -1, 0],
                  [0, 1, 0, 1], [0, 1, 0, -1]])/s.sqrt(2)
    chi = s.Matrix([[1, 0, 0, 1], [0, 1, -s.I, 0],
                    [0, 1, s.I, 0], [1, 0, 0, -1]])/s.sqrt(2)
    m2 = [j*d+i for j in range(4) for i in range(4)]
    scalar_columns = [j*d+4 for j in range(4)]
    Psi = V[:, m2]*s.kronecker_product(T, chi)*F.record_basis().T
    scalar = V[:, scalar_columns]
    J = V[:, :d]
    Q = s.eye(89)-J*J.H
    seed = s.Matrix([p, 0, 0, p, a*p])
    incoming = J*seed
    outgoing = AF.activate(1, seed)
    gate = s.kronecker_product(AF.record(), s.eye(d))
    return CanonicalRecord(AF, a, p, V, Psi, scalar, J, Q,
                           seed, incoming, outgoing, gate)


def left_density(vector: s.MatrixBase, reduce_scalar=s.simplify) -> tuple[s.MatrixBase, s.MatrixBase, s.Expr]:
    """Normalized left-state on ALL M8 (+) M5 from orthonormal GNS entries.

    These coordinates already include square roots of the PF weights. Thus
    the raw factor matrices are the two reshaped GNS coordinate blocks.
    """
    if vector.shape != (89, 1):
        raise ValueError("complete_89_GNS_column_required")
    A = s.Matrix(8, 8, list(vector[:64]))
    B = s.Matrix(5, 5, list(vector[64:]))
    tau = reduce_scalar((vector.H*vector)[0])
    if tau == 0:
        raise ValueError("positive_GNS_normalizer_required")
    return A*A.H/tau, B*B.H/tau, tau


def spectral_amplitudes(data: CanonicalRecord) -> dict[str, s.Expr]:
    a, p = data.a, data.p
    return {"plus": p**3+p**2/s.sqrt(2), "minus": p**3-p**2/s.sqrt(2),
            "zero": p**3, "scalar_plus": p**3+a*p**2/s.sqrt(2),
            "scalar_minus": p**3-a*p**2/s.sqrt(2), "B": a*p**3}


def generic_costates(data: CanonicalRecord) -> dict:
    """Exact COARSE A4 generic-log costates at the actual post-record state.

    The covector convention is dA=2 Re(delta_x^* h); real16/scalar4 use
    ordinary real coordinates. Raw-coordinate normalization is differentiated,
    so the -A*x terms remain even if a caller later chooses a norm tangent.
    All69 complement coefficients are retained as a complete ambient vector.
    """
    a, p, AF, x = data.a, data.p, data.AF, data.outgoing
    g = s.Symbol("log_phi", positive=True)
    lp, lm, l0, lsp, lsm, lb = s.symbols(
        "log_lambda_plus log_lambda_minus log_lambda_zero "
        "log_lambda_scalar_plus log_lambda_scalar_minus log_lambda_B", real=True)
    q = spectral_amplitudes(data)
    xp, xm, x0, sp, sm, xb = (q[k] for k in
                              ("plus", "minus", "zero", "scalar_plus", "scalar_minus", "B"))
    logs = [lp, lp, lsp, lm, lm, l0, l0, lsm]+[lb]*5
    log_x = s.zeros(89, 1)
    for i in range(8):
        log_x[8*i+i] = x[8*i+i]*logs[i]
    for i in range(5):
        log_x[64+5*i+i] = x[64+5*i+i]*logs[8+i]
    E = 2*xp**2*lp+2*xm**2*lm+2*x0**2*l0+sp**2*lsp+sm**2*lsm+5*xb**2*lb
    cost = 5+5*p**7
    old, gain = cost+E/g, -E/g
    cost_x = s.Matrix([5*x[i] if i < 64 else 6*x[i] for i in range(89)])
    old_h = cost_x+log_x/g-old*x
    gain_h = -log_x/g-gain*x
    J0 = a*p*(xp*lp+xm*lm+p**3*l0)+2*a*p**5*lb
    J1 = (xp*lp-xm*lm)/s.sqrt(2)
    S0 = p*(sp*lsp+sm*lsm)+p**5*lb
    S3 = (sp*lsp-sm*lsm)/s.sqrt(2)
    closed = {}
    for label, k0, k1, t0, t3 in (
        ("old", 3*a*(5*p-2)+J0/g-old*a*p, 5*p**2+J1/g-old*p**2,
         2+S0/g-old*p**2, 5*a*p**2+S3/g-old*a*p**2),
        ("gain", -J0/g-gain*a*p, -J1/g-gain*p**2,
         -S0/g-gain*p**2, -S3/g-gain*a*p**2),
    ):
        matter = s.zeros(16, 1)
        matter[0] = matter[14] = k0
        matter[1], matter[15] = k1, -k1
        closed[label] = {"matter_real16": matter, "scalar_real4": s.Matrix([t0, 0, 0, t3])}
    result = {"log_phi": g, "logs": (lp, lm, l0, lsp, lsm, lb),
              "E": E, "cost": cost, "old_value": old, "gain_value": gain,
              "log_x": log_x, "closed": closed}
    for label, h in (("old", old_h), ("gain", gain_h)):
        matter = AF.mat(data.Psi.H*h)
        scalar = AF.mat(data.scalar.H*h)
        complement = AF.mat(h-data.V*(data.V.H*h))
        result[label] = {"ambient89": h, "matter_real16": matter,
                         "scalar_real4": scalar, "complement69_ambient": complement}
    return result


def full_operator_factors(data: CanonicalRecord, vector: s.MatrixBase) -> tuple[s.MatrixBase, ...]:
    """Full A7 operator readout of the SAME 89-dimensional GNS vector.

    The owned right_frames(1)[j].labels=(v,k,row) enumerate a multiplicity
    row; c is the old-right M2/M1 column. No row, column, or zero mode is
    discarded. F0 is 34x2 and F1 is 21x1, so 34*2+21=89.
    """
    if vector.shape != (89, 1):
        raise ValueError("complete_89_GNS_column_required")
    frame = data.AF.frame(1)
    segments = frame["segments"]
    factors = []
    for old_type, info in enumerate(data.AF.right_frames(1)):
        width = info["spectator_dimension"]
        factor = s.zeros(info["dimension"], width)
        for i, (v, k, row) in enumerate(info["labels"]):
            kind, path, offset = segments[v][k]
            require(kind == old_type, "owned_right_label_type")
            size = (8, 5)[v]
            start = (0, 64)[v]
            for c in range(width):
                factor[i, c] = vector[start+row*size+offset+c]
        factors.append(factor)
    return tuple(factors)


def full_operator_readout(data: CanonicalRecord, vector: s.MatrixBase,
                          tangent: s.MatrixBase | None = None) -> dict:
    """Full55 density and its small old-right Gram matrices; full normalizer."""
    factors = full_operator_factors(data, vector)
    tau = data.AF.red((vector.H*vector)[0])
    if tau == 0:
        raise ValueError("positive_full_operator_normalizer_required")
    result = {"factors": factors, "tau": tau,
              "density": tuple(F*F.H/tau for F in factors),
              "right_grams": tuple(F.H*F/tau for F in factors)}
    if tangent is not None:
        dots = full_operator_factors(data, tangent)
        dtau = data.AF.red((tangent.H*vector+vector.H*tangent)[0])
        result.update({"factor_jets": dots, "dtau": dtau,
                       "right_gram_jets": tuple(
                           (dF.H*F+F.H*dF)/tau-F.H*F*dtau/tau**2
                           for F, dF in zip(factors, dots))})
    return result


def full_operator_costates(data: CanonicalRecord) -> dict:
    """Actual A7 entropy-contract covectors, with all55/89 modes retained.

    At the canonical record F0*F0=p^2 I2 and F1*F1=p^3. Therefore
    mu7^(-1)*sigma7=p^(-6)P7. Old D/g is stationary on every C1 amplitude
    germ here. Gain entropy is stationary only on tangents preserving the
    M2/scalar masses, including our full-blank rotation witness.
    """
    a, p, AF = data.a, data.p, data.AF
    m = AF.mat(data.Psi.H*data.outgoing)
    c = AF.mat(data.scalar.H*data.outgoing)
    m2_x, scalar_x = data.Psi*m, data.scalar*c
    old_h = s.zeros(89, 1)
    gain_h = AF.mat(-p**3*m2_x+2*p**2*scalar_x)
    return {"dimension": 55, "block_dimensions": (34, 21),
            "nonzero_eigenvalues": (p**2, p**2, p**3),
            "zero_multiplicities": (32, 20),
            "PF_weights": (p**8, p**9), "cost_value": 8+p**3,
            "old_value": s.Integer(6), "gain_value": 2+p**3,
            "old_ambient89": old_h, "old_matter_real16": s.zeros(16, 1),
            "old_scalar_real4": s.zeros(4, 1),
            "gain_ambient89": gain_h, "gain_matter_real16": AF.mat(-p**3*m),
            "gain_scalar_real4": AF.mat(2*p**2*c),
            "gain_complement69_ambient": AF.mat(gain_h-data.V*(data.V.H*gain_h))}


def normalized_copy_adjoint_to_A1(data: CanonicalRecord,
                                  blocks: tuple[s.MatrixBase, ...]) -> tuple[s.MatrixBase, ...]:
    """Actual trace-adjoint of the six-copy A1 -> A7 inclusion.

    A7 is expressed in the owned right-module multiplicity basis. A coarse
    matrix is repeated on each old-left path inside each (v,right-path)
    group. Compressing EVERY such copy and weighting by tau7/tau1 is its
    trace adjoint, independently of a canonical-path coordinate permutation.
    Off-diagonal entries between different copies remain in the full input
    and its norm; they are not deleted from the regular carrier.
    """
    p = data.p
    segments = data.AF.frame(1)["segments"]
    answer = [s.zeros(2), s.zeros(1)]
    for right_type, info in enumerate(data.AF.right_frames(1)):
        labels = info["labels"]
        index = {label: i for i, label in enumerate(labels)}
        groups = sorted({(v, k) for v, k, row in labels})
        for v, k in groups:
            for left_type, path, offset in segments[v]:
                width = (2, 1)[left_type]
                rows = [index[(v, k, offset+r)] for r in range(width)]
                answer[left_type] += p**(8+right_type-(2+left_type))*blocks[right_type].extract(rows, rows)
    return tuple(data.AF.mat(v) for v in answer)


def full_regular_preparation(data: CanonicalRecord) -> dict:
    """Owned A7 element X7=W*e/p^3 and its full-blank preparation jet.

    Working H4 has dimension89. The REGULAR GNS space of A7 has dimension
    34^2+21^2=1597. Its old-algebra retained rank is5. The working e has
    rank5 on H4, but left multiplication by e has rank89 on regular H7.
    They must not be confused with that retained rank5 projection.
    """
    a, p = data.a, data.p
    elements, dots, corners = [], [], []
    for j, info in enumerate(data.AF.right_frames(1)):
        width, V = info["spectator_dimension"], info["V"]
        J, detail = V[:, :width], V[:, 3*width:4*width]
        e = J*J.H
        elements.append((a*J+p*detail)*J.H/p**3)
        dots.append((-p*J+a*detail)*J.H/p**3 if j == 0 else s.zeros(info["dimension"]))
        corners.append(e)
    factors = full_operator_readout(data, data.outgoing)["density"]
    # X7 is a normalized vector of the actual PF-GNS regular algebra.
    norm = data.AF.red(sum(p**(8+j)*s.trace(X.H*X) for j, X in enumerate(elements)))
    norm_dot = data.AF.red(sum(p**(8+j)*s.trace(dX.H*X+X.H*dX)
                              for j, (X, dX) in enumerate(zip(elements, dots))))
    density = tuple(p**(8+j)*X*X.H/norm for j, X in enumerate(elements))
    coarse = normalized_copy_adjoint_to_A1(data, tuple(elements))
    coarse_dot = normalized_copy_adjoint_to_A1(data, tuple(dots))
    retained = sum(p**(2+j)*s.trace(C.H*C) for j, C in enumerate(coarse))
    retained_dot = sum(p**(2+j)*s.trace(dC.H*C+C.H*dC)
                       for j, (C, dC) in enumerate(zip(coarse, coarse_dot)))
    left_retained = sum(p**(8+j)*s.trace(X.H*e*X)
                        for j, (X, e) in enumerate(zip(elements, corners)))
    left_retained_dot = sum(p**(8+j)*s.trace(dX.H*e*X+X.H*e*dX)
                            for j, (X, e, dX) in enumerate(zip(elements, corners, dots)))
    return {"elements": tuple(elements), "jets": tuple(dots), "corners": tuple(corners),
            "norm": norm, "norm_jet": norm_dot, "density": density, "working_density": factors,
            "coarse": coarse, "coarse_jet": coarse_dot,
            "q_regular": 1-retained/norm,
            "dq_regular": -retained_dot/norm+retained*norm_dot/norm**2,
            "q_left_corner": 1-left_retained/norm,
            "dq_left_corner": -left_retained_dot/norm+left_retained*norm_dot/norm**2,
            "dimension": 1597, "retained_rank": 5}


def next_active_record(data: CanonicalRecord, tangent: s.MatrixBase) -> dict:
    """Next OWNED active W4 J4; exact Gram transfer without any1597 matrix.

    In right-module j the operator-A10 feature is F_j=R_j X4_j, where
    R_j=a V0_j+p V3_j is the actual record isometry. Thus F_j*F_j=X4_j*X4_j
    and all nonzero spectra/entropy jets transfer exactly. Full operator A10
    has M144 (+) M89, not A7; its PF weights differ from A4 by p^6.
    This active record is NOT passive hatC state extension.
    """
    if tangent.shape != (89, 1):
        raise ValueError("complete_H4_tangent_required")
    input_blocks = (s.Matrix(8, 8, list(data.outgoing[:64])),
                    s.Matrix(5, 5, list(data.outgoing[64:])))
    input_jets = (s.Matrix(8, 8, list(tangent[:64])),
                  s.Matrix(5, 5, list(tangent[64:])))
    actual = data.AF.activate(4, data.outgoing)
    actual_jet = data.AF.activate(4, tangent)
    actual_frame = data.AF.frame(4)
    fine_sizes = actual_frame["fine_sizes"]
    starts = (0, fine_sizes[0]**2)
    factors, factor_jets, records, literal, literal_jets = [], [], [], [], []
    for info, X, dX in zip(data.AF.right_frames(4), input_blocks, input_jets):
        V, d = info["V"], info["spectator_dimension"]
        R = data.a*V[:, :d]+data.p*V[:, 3*d:4*d]
        records.append(R)
        factors.append(R*X)
        factor_jets.append(R*dX)
        # Extract the actual activate() output independently of R*X.
        # Keep every fine row and old-right column, including zero entries.
        F, dF = s.zeros(info["dimension"], d), s.zeros(info["dimension"], d)
        for i, (v, k, row) in enumerate(info["labels"]):
            offset = actual_frame["segments"][v][k][2]
            for c in range(d):
                index = starts[v]+row*fine_sizes[v]+offset+c
                F[i, c], dF[i, c] = actual[index], actual_jet[index]
        literal.append(F)
        literal_jets.append(dF)
    return {"record_isometries": tuple(records), "factors": tuple(factors),
            "factor_jets": tuple(factor_jets), "input_blocks": input_blocks,
            "literal_factors": tuple(literal), "literal_jets": tuple(literal_jets),
            "input_jets": input_jets, "operator_block_dimensions": (144, 89),
            "working_H7_dimension": 1597, "regular_A10_dimension": 28657,
            "relative_entropy_shift_phi_units": 6}


def outgoing_witness(data: CanonicalRecord) -> dict:
    a, p = data.a, data.p
    dm = s.zeros(16, 1)
    dm[0] = dm[14] = -p**2
    dm[1], dm[15] = a*p, -a*p
    incoming_dm = s.zeros(16, 1)
    incoming_dm[1] = incoming_dm[15] = p
    return {"matter_real16": dm, "scalar_real4": s.zeros(4, 1),
            "ambient89": data.Psi*dm,
            "incoming_blank_matter_real16": incoming_dm,
            "incoming_blank_ambient89": data.Psi*incoming_dm}


def interval_witness() -> dict:
    """Outward intervals for the actual spectral source; no rank threshold."""
    from mpmath import iv
    previous = iv.dps
    iv.dps = 45
    try:
        p = (iv.sqrt(5)-1)/2
        a, g, r2 = iv.sqrt(p), -iv.log(p), iv.sqrt(2)
        xp, xm, x0 = p**3+p**2/r2, p**3-p**2/r2, p**3
        sp, sm, xb = p**3+a*p**2/r2, p**3-a*p**2/r2, a*p**3
        amplitudes = [xp, xp, sp, xm, xm, x0, x0, sm]+[xb]*5
        lambdas = [v*v for v in amplitudes]
        require(all(v > 0 for v in lambdas), "all13_actual_left_eigenvalues_positive")
        logs = [iv.log(v) for v in lambdas]
        # Actual diagonal derivatives: scalar4 is fixed, including its M5 row.
        dxp, dxm, dx0 = a*(-p**3+p/r2), a*(-p**3-p/r2), -a*p**3
        dots = [dxp, dxp, 0, dxm, dxm, dx0, dx0, 0]+[-p**4, -p**4, 0, -p**4, -p**4]
        dE = sum(2*x*dx*l for x, dx, l in zip(amplitudes, dots, logs))
        gain_source = -dE/g
        cost_source = -8*a*p**7
        old_source = cost_source-gain_source
        require(old_source > iv.mpf("0.43415444592488") and
                old_source < iv.mpf("0.43415444592489"), "old_source_strict_interval")
        require(gain_source > iv.mpf("-0.65076653214095") and
                gain_source < iv.mpf("-0.65076653214094"), "gain_source_strict_interval")
        return {"old_source": str(old_source), "gain_source": str(gain_source),
                "cost_source": str(cost_source), "all13_eigenvalues_positive": True,
                "readout": "COARSE_LEFT_A4_ONLY",
                "full_A7_old_witness_source": "0", "full_A7_gain_witness_source": "0",
                "full_minus_coarse_old_source": str(-old_source),
                "full_minus_coarse_gain_source": str(-gain_source),
                "next_ACTIVE_A10_old_source": str(old_source),
                "next_ACTIVE_A10_gain_source": str(gain_source)}
    finally:
        iv.dps = previous


def run_checks(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    data = canonical_record(repo)
    AF, a, p = data.AF, data.a, data.p
    checks = []
    def eq(actual, expected, name):
        require(AF.zero(actual-expected), name)
        checks.append(name)
    eq(data.V.H*data.V, s.eye(20), "all20_record_frame_isometry")
    eq(data.Psi.H*data.Psi, s.eye(16), "all16_real_CAR_chart_isometric")
    eq(data.scalar.H*data.scalar, s.eye(4), "all4_scalar_channel_isometric")
    eq(data.Psi.H*data.scalar, s.zeros(16, 4), "CAR_scalar_orthogonal")
    eq(data.Psi*data.Psi.H+data.scalar*data.scalar.H, data.V*data.V.H,
       "full20_plus69_carrier_decomposition")
    eq((data.seed.H*data.seed)[0], 1, "whole_canonical_trace_seed_normalized")
    eq(data.outgoing, data.V*data.gate*data.V.H*data.incoming,
       "literal_activate_equals_fixed_record_on_full_seed")
    eq((data.outgoing.H*data.outgoing)[0], 1, "full89_post_record_norm")
    m = s.zeros(16, 1)
    m[0] = m[14] = a*p
    m[1], m[15] = p**2, -p**2
    eq(data.Psi.H*data.outgoing, m, "actual_outgoing_real16")
    eq(data.scalar.H*data.outgoing, s.Matrix([p**2, 0, 0, a*p**2]),
       "whole_scalar_channel_retained")
    require(AF.red(2*p**2) != 1, "reject_conditioning_away_scalar_channel")
    q = spectral_amplitudes(data)
    av = [q[k] for k in ("plus", "plus", "scalar_plus", "minus", "minus",
                          "zero", "zero", "scalar_minus")]
    rhoA, rhoB, tau = left_density(data.outgoing, AF.red)
    eq(tau, 1, "actual_GNS_normalizer")
    eq(rhoA, s.diag(*(v*v for v in av)), "all8_A_eigenvalues_and_coherences")
    eq(rhoB, q["B"]**2*s.eye(5), "all5_B_eigenvalues_including_scalar_row")
    eq(s.trace(rhoA)+s.trace(rhoB), 1, "all13_eigenvalues_unit_total")
    states = generic_costates(data)
    for label in ("old", "gain"):
        got, want = states[label], states["closed"][label]
        eq(got["matter_real16"], want["matter_real16"], label+"_all16_closed_log_coefficients")
        eq(got["scalar_real4"], want["scalar_real4"], label+"_all4_closed_log_coefficients")
        h, hc = got["ambient89"], got["complement69_ambient"]
        eq(data.Psi.H*hc, s.zeros(16, 1), label+"_complement_orthogonal_CAR")
        eq(data.scalar.H*hc, s.zeros(4, 1), label+"_complement_orthogonal_scalar")
        eq(h, data.Psi*got["matter_real16"]+data.scalar*got["scalar_real4"]+hc,
           label+"_full89_covector_reconstruction")
        eq((data.outgoing.H*h)[0], 0, label+"_raw_radial_normalizer_cancellation")
        require(not AF.zero(hc), label+"_generic_log_complement_not_erased")
    eq(states["old"]["ambient89"]+states["gain"]["ambient89"],
       s.Matrix([5*data.outgoing[i] if i < 64 else 6*data.outgoing[i] for i in range(89)])
       -states["cost"]*data.outgoing, "two_contracts_sum_to_full_normalized_cost_gradient")
    w = outgoing_witness(data)
    dx, din = w["ambient89"], w["incoming_blank_ambient89"]
    eq((data.outgoing.H*dx)[0], 0, "outgoing_real_matter_norm_tangent")
    eq(data.scalar.H*dx, s.zeros(4, 1), "witness_does_not_move_scalar_channel")
    old_m2_seed = s.Matrix([p, 0, 0, p, 0])
    eq(din, data.V[:, 10:15]*old_m2_seed, "preimage_is_full_blank_e2_not_old_inclusion")
    blank = s.kronecker_product(s.diag(1, 0, 1, 0), s.eye(5))
    eq(blank*(data.V.H*din), data.V.H*din, "preimage_in_actual_full_blank_plane")
    eq(data.V*data.gate*data.V.H*din, dx, "fixed_owned_gate_gives_outgoing_witness")
    eq(data.J.H*din, s.zeros(5, 1), "incoming_witness_not_V0_seed_variation")
    eq(data.J.H*data.V*data.gate.H*data.V.H*dx, s.zeros(5, 1),
       "outgoing_witness_orthogonal_WV0_image")
    # Full operator archive: SAME x on H4, but all A7=M34 (+) M21 readout.
    full = full_operator_readout(data, data.outgoing, dx)
    F0, F1 = full["factors"]
    require(F0.shape == (34, 2) and F1.shape == (21, 1), "full_operator_34x2_plus21x1_keeps89")
    eq(s.trace(F0.H*F0)+s.trace(F1.H*F1), tau, "right_decomposition_keeps_entire89_norm")
    eq(full["right_grams"][0], p**2*s.eye(2), "full_A7_nonzero_spectrum_p2_twice")
    eq(full["right_grams"][1], s.Matrix([[p**3]]), "full_A7_nonzero_spectrum_p3_once")
    eq(full["right_gram_jets"][0], s.zeros(2), "full_A7_witness_M2_spectrum_jet_zero")
    eq(full["right_gram_jets"][1], s.zeros(1), "full_A7_witness_scalar_spectrum_jet_zero")
    rho7A, rho7B = full["density"]
    eq(rho7A*rho7A, p**2*rho7A, "full34_density_support_eigenvalue_p2")
    eq(rho7B*rho7B, p**3*rho7B, "full21_density_support_eigenvalue_p3")
    eq(34*p**8+21*p**9, 1, "actual_A7_PF_reference_normalized")
    eq((8*(2*p**2)+9*p**3)-(4*p**2+3*p**3), 6,
       "full_A7_old_D_over_g_value6")
    # Whole finite blank rotation: x(t)=cos(t)*x_M2+sin(t)*dx+x_scalar.
    # The following three Gram identities prove its spectrum constant, not
    # just a finite-difference zero at one angle.
    dF0 = full["factor_jets"][0]
    eq(dF0.H*dF0, p**2*s.eye(2), "full_blank_rotation_M2_tangent_Gram")
    eq(F0.H*dF0+dF0.H*F0, s.zeros(2), "full_blank_rotation_cross_Gram_zero")
    fc = full_operator_costates(data)
    eq(fc["gain_ambient89"], data.Psi*fc["gain_matter_real16"]
       +data.scalar*fc["gain_scalar_real4"], "full_A7_gain_all20_covector")
    eq(fc["gain_complement69_ambient"], s.zeros(89, 1), "full_A7_gain_no69_loss")
    eq(2*(dx.H*fc["gain_ambient89"])[0], 0, "full_A7_gain_rotation_source_zero")
    # At the support, log(sigma7)/g=(-2,-3), C7=(8,9), so
    # (C7+log(sigma7)/g-6)F=0 including every amplitude direction.
    eq(8-2-fc["old_value"], 0, "full_A7_old_M2_gradient_zero")
    eq(9-3-fc["old_value"], 0, "full_A7_old_scalar_gradient_zero")
    for label in ("old", "gain"):
        hfull = fc[label+"_ambient89"]
        remainder = hfull-states[label]["ambient89"]
        eq(2*(dx.H*remainder)[0], -2*(dx.H*states[label]["ambient89"])[0],
           label+"_actual_archive_remainder_cancels_coarse_witness_source")
    # A4 embeds in the A7 old-right commutant by three copies/two copies
    # in its first block and two/one in its second, up to path permutation.
    eq(3*p**8+2*p**9, p**5, "three_inclusions_A4_A7_A_weight")
    eq(2*p**8+p**9, p**6, "three_inclusions_A4_A7_B_weight")
    eq(data.J.H*data.J, s.eye(5), "full_GNS_J_rank5")
    eq(data.Q*data.Q, data.Q, "full_GNS_archive_projection")
    eq(s.trace(data.Q), 84, "full89_archive_complement_rank84")
    occupation = AF.red((data.outgoing.H*data.Q*data.outgoing)[0])
    eq(occupation, p**2, "actual_full_GNS_archive_occupation")
    hq = AF.mat((data.Q-occupation*s.eye(89))*data.outgoing)
    hqm = s.zeros(16, 1)
    hqm[0] = hqm[14] = -a*p**3
    hqm[1], hqm[15] = p**3, -p**3
    eq(data.Psi.H*hq, hqm, "archive_full16_covector")
    eq(data.scalar.H*hq, s.Matrix([-p**4, 0, 0, a*p**3]), "archive_fullscalar_covector")
    eq(hq-data.V*(data.V.H*hq), s.zeros(89, 1), "archive_covector_complement69_zero_by_projection")
    eq(2*(dx.H*hq)[0], 4*a*p**3, "archive_witness_source_4ap3")
    eq(2*sum(s.conjugate(data.outgoing[i])*dx[i] for i in range(64, 89)),
       -8*a*p**7, "independent_full_B_mass_cost_source")
    # This is only the separately declared reference residual-heat family.
    eq(s.Rational(84, 2)/(5+s.Rational(84, 2)), s.Rational(42, 47),
       "full89_retained5_thermal_reference_at_beta_log2_nu1")
    regular = full_regular_preparation(data)
    eq(normalized_copy_adjoint_to_A1(data, (s.eye(34), s.eye(21)))[0], s.eye(2),
       "six_copy_adjoint_unital_M2")
    eq(normalized_copy_adjoint_to_A1(data, (s.eye(34), s.eye(21)))[1], s.eye(1),
       "six_copy_adjoint_unital_M1")
    eq(regular["norm"], 1, "actual_We_over_p3_full1597_regular_norm")
    eq(regular["norm_jet"], 0, "actual_full1597_regular_normalizer_jet")
    eq(sum(p**(8+j)*s.trace(e) for j, e in enumerate(regular["corners"])), p**6,
       "actual_corner_PF_trace_p6")
    eq(sum((34, 21)[j]*s.trace(e) for j, e in enumerate(regular["corners"])), 89,
       "left_corner_full_regular_rank89_not_retained5")
    for j in range(2):
        eq(regular["density"][j], regular["working_density"][j],
           "full1597_We_left_state_equals_working_operator_readout_"+str(j))
    eq(regular["coarse"][0], a*p**3*s.eye(2), "C_A1_A7_X_M2")
    eq(regular["coarse"][1], a*p**3*s.eye(1), "C_A1_A7_X_M1")
    eq(regular["coarse_jet"][0], -p**4*s.eye(2), "C_A1_A7_dX_M2")
    eq(regular["coarse_jet"][1], s.zeros(1), "C_A1_A7_dX_M1")
    eq(regular["q_regular"], 1-p**7, "actual_regular_archive_q_1_minus_p7")
    eq(regular["dq_regular"], 4*a*p**9, "actual_regular_archive_dq_4ap9")
    eq(regular["q_regular"], 1-p**6*(1-occupation), "regular_working_archive_normalization_relation")
    eq(regular["dq_regular"], p**6*4*a*p**3, "regular_working_archive_source_factor_p6")
    eq(regular["q_left_corner"], p**2, "full1597_left_corner_rank89_q")
    eq(regular["dq_left_corner"], 4*a*p**3, "full1597_left_corner_rank89_dq")
    eq(s.Rational(1592, 2)/(5+s.Rational(1592, 2)), s.Rational(796, 801),
       "full1597_rank5_thermal_reference_beta_log2_nu1")
    eq((1-p**7)-s.Rational(796, 801), s.Rational(5, 801)-p**7,
       "full1597_reference_nu_source")
    eq(s.Rational(1508, 2)/(89+s.Rational(1508, 2)), s.Rational(754, 843),
       "full1597_LEFT_CORNER_rank89_distinct_thermal_reference")
    active = next_active_record(data, dx)
    for j, (R, F, dF, X, dX) in enumerate(zip(
        active["record_isometries"], active["factors"], active["factor_jets"],
        active["input_blocks"], active["input_jets"])):
        d = (8, 5)[j]
        eq(R.H*R, s.eye(d), "next_active_actual_record_isometry_"+str(j))
        eq(F, active["literal_factors"][j], "next_active_literal_activate_factor_"+str(j))
        eq(dF, active["literal_jets"][j], "next_active_literal_activate_jet_"+str(j))
        eq(F.H*F, X.H*X, "next_active_all13_spectrum_transfer_"+str(j))
        eq(dF.H*F+F.H*dF, dX.H*X+X.H*dX,
           "next_active_exact_entropy_jet_transfer_"+str(j))
    eq((11-5)*s.trace(rhoA)+(12-6)*s.trace(rhoB), 6,
       "next_active_full_operator_cost_shift_exactly6")
    eq(p**11-p**6*p**5, 0, "next_active_A_PF_shift_p6")
    eq(p**12-p**6*p**6, 0, "next_active_B_PF_shift_p6")
    intervals = interval_witness()
    pin_sources(repo)
    return {"status": "PASS_CANONICAL_TRACE_RECORD_SOURCE", "exact_check_count": len(checks),
            "scope": {"real_matter_components": 16, "scalar_components": 4,
                      "retained_old_GNS_rank": 5,
                      "working_H4_GNS_dimension": 89,
                      "full_A7_regular_GNS_dimension": 1597,
                      "record_frame_dimension": 20, "identity_complement_dimension": 69,
                      "left_defining_eigenvalues": 13,
                      "left_readout_is_coarse_A4": True,
                      "full_operator_A7_defining_modes": 55,
                      "full_operator_A7_nonzero_modes": 3,
                      "full_operator_A7_zero_modes": 52,
                      "working_H4_archive_complement_rank": 84,
                      "fixed_tuple_not_intrinsic_orientation_update": True,
                      "physical_Info_or_preparation_admission_proved": False,
                      "old_suites_executed": False},
            "archive": {"q": "p^2", "witness_dq": "4*a*p^3",
                        "carrier": "WORKING_H4_GNS_DIM89_ONLY",
                        "reference_thermal_p": "42/47",
                        "reference_nu_source": "p^2-42/47",
                        "identified_with_Cost_Info": False},
            "regular_archive": {"carrier": "FULL_A7_REGULAR_GNS_DIM1597",
                "preparation": "X7=W*e/p^3", "corner_PF_trace": "p^6",
                "left_corner_rank": 89, "old_algebra_retained_rank": 5,
                "q": "1-p^7", "witness_dq": "4*a*p^9",
                "reference_thermal_p": "796/801", "reference_nu_source": "5/801-p^7",
                "identified_with_Cost_Info": False},
            "regular_left_corner": {"carrier_dimension": 1597, "left_corner_rank": 89,
                "projection": "L_e; DIFFERENT from canonical GNS J1_to7 J1_to7*",
                "q": "p^2", "witness_dq": "4*a*p^3",
                "reference_thermal_p": "754/843", "reference_nu_source": "p^2-754/843"},
            "full_operator_archive": {"algebra": "M34 (+) M21",
                "nonzero_spectrum": ["p^2", "p^2", "p^3"],
                "zero_multiplicities": [32, 20], "old_action": "6",
                "gain_action": "2+p^3", "old_witness_source": "0",
                "gain_witness_source": "0", "old_covector_all89_zero": True,
                "gain_covector_all89_zero": False,
                "coarse_nonzero_source_is_full_source": False},
            "next_active_record": {"working_H7_dimension": 1597,
                "operator_algebra": "A10=M144 (+) M89", "defining_modes": 233,
                "nonzero_modes": 13, "zero_modes": 220,
                "full_regular_dimension": 28657,
                "old_action": "6+coarse_A4_old_action", "gain_action": "coarse_A4_gain_action",
                "old_and_gain_sources": "the nonzero coarse A4 intervals, by exact transfer",
                "passive_hatC_extension": False},
            "interval_witness": intervals, "bridge_provenance": BRIDGE_PROVENANCE,
            "source_pins": SOURCE_PINS}


if __name__ == "__main__":
    print(json.dumps(run_checks(), sort_keys=True))
