#!/usr/bin/env python3
"""One exact physical phase source consumer, not a new rank census.

At q=eta, U=I, phase (1,1,i,i), variables (a,q), the geometric
linearized Euler equation is K (delta a,delta q) = (f_a,f_q).
All 24 link and ten independent symmetric metric coordinates are retained.
If I_total=A_geometry+epsilon*B_native, the *conditional* first variation
at an actual joint zero of A_geometry has f=-dB_native, in the same chart.
No epsilon family, B_native binding, physical Ward or refinement is derived.

The conjugate phase is compulsory for a real field: forcing amplitudes there
are the complex conjugates of these. Off-diagonal metric source slots are
already packed: f_q=(00,01,02,03,11,12,13,22,23,33) pairs with independent
symmetric q_{rs}, so an ambient symmetric tensor has packed slot 2*T_rs.

This is the geometric column-coframe convention q=E.T*eta*E, E=I,
delta E=eta*delta q/2. A native row frame F with q=F*eta*F.T may use
E=F.T only after identifying the actual common frame and link chart.
Raw, transported and off-constraint ambient partials are not interchanged.
"""
from __future__ import annotations

import argparse
import ast
from fractions import Fraction
from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys
import types

import sympy as sp
from sympy.polys.matrices import DomainMatrix

PINS = {
    "flat_symbols": "a843847c4c169da6dba98e9608fc265fac534d56",
    "literal_hessian": "f3a388d12737d8814f134f02eba4daa5c34c857d",
    "literal_face_algebra": "e96283c5761f395096080843de30d00ae5826f71",
}
PATHS = {
    "flat_symbols": "02_REGISTRY/research/certificates/a4d_designated_full_gap_check.py",
    "literal_hessian": "02_REGISTRY/research/certificates/a4d_identity_physical_resonance_circles_check.py",
    "literal_face_algebra": "02_REGISTRY/research/certificates/a4d_y_curved_joint_rational_stencil.py",
}
METRIC = ["00", "01", "02", "03", "11", "12", "13", "22", "23", "33"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_owner(repo: Path, key: str) -> str:
    data = (repo / PATHS[key]).read_bytes()
    blob = b"blob " + str(len(data)).encode() + b"\0" + data
    if hashlib.sha1(blob).hexdigest() != PINS[key]:
        raise RuntimeError("SOURCE_PIN_MISMATCH: " + PATHS[key])
    return data.decode()


def domain(matrix: sp.Matrix) -> DomainMatrix:
    return DomainMatrix.from_Matrix(matrix.applyfunc(sp.expand)).convert_to(sp.QQ_I)


def same(left: sp.Matrix, right: sp.Matrix) -> bool:
    return (domain(left) - domain(right)).is_zero_matrix


def build_context(repo: Path | None = None) -> dict:
    repo = Path(repo) if repo is not None else Path(__file__).resolve().parents[4]
    # Import definitions only. No owner checker/census is run or rewritten.
    owner = types.ModuleType("d0_source_compatibility_flat_owner")
    owner.__file__ = str(repo / "02_REGISTRY/research/certificates/a4d_designated_full_gap_check.py")
    sys.modules[owner.__name__] = owner
    exec(compile(read_owner(repo, "flat_symbols"), owner.__file__, "exec"), owner.__dict__)
    algebra = types.SimpleNamespace()
    algebra_text = read_owner(repo, "literal_face_algebra")
    # The archived module eagerly builds an unrelated curved stencil below
    # this line; only its shared exact 4x4 algebra definitions are needed.
    algebra_text = algebra_text.split("ATERMS,QTERMS=build_stencil()", 1)[0]
    exec(compile(algebra_text, "<pinned-literal-face-algebra>", "exec"), algebra.__dict__)
    audit_text = read_owner(repo, "literal_hessian")
    literal_node = next(x for x in ast.parse(audit_text).body if isinstance(x, ast.FunctionDef) and x.name == "literal_stencil")
    namespace = {"S": algebra, "F": Fraction, "combinations": combinations}
    exec(compile(ast.get_source_segment(audit_text, literal_node), "<pinned-literal-stencil>", "exec"), namespace)
    h_terms, c_terms = namespace["literal_stencil"]()

    phase = (sp.Integer(1), sp.Integer(1), sp.I, sp.I)
    qi_phase = [owner.QI(Fraction(0), Fraction(1)) if z == sp.I else owner.QI.of(1) for z in phase]
    polarized, metric = owner.flat_symbols(qi_phase)

    def convert(array):
        return sp.Matrix([[sp.Rational(x.re.numerator, x.re.denominator) + sp.I*sp.Rational(x.im.numerator, x.im.denominator) for x in row] for row in array])

    def evaluate(terms, rows, cols, reverse=False):
        out = sp.zeros(rows, cols)
        for shift, entries in terms.items():
            factor = sp.prod(z**(-power if reverse else power) for z, power in zip(phase, shift))
            for (row, col), value in entries.items():
                if reverse:
                    row, col = col, row
                out[row, col] += factor*sp.Rational(value.numerator, value.denominator)
        return out

    H = evaluate(h_terms, 24, 24)
    C = evaluate(c_terms, 10, 24)
    B = evaluate(c_terms, 24, 10, reverse=True)
    require(same(H, convert(polarized).T), "physical input/output placement")
    require(same(C, convert(metric)), "literal packed metric mixed derivative")
    require(same(H, H.conjugate().T), "connection Hessian reciprocity")
    require(same(B, C.conjugate().T), "mixed reciprocal placement from same face")

    # At U=I the odd plaquette curvature is identically zero for every q;
    # hence the geometric qq Hessian block is zero. This uses the actual
    # naked-star action, not the older auxiliary H+H.T convention.
    K = H.row_join(B).col_join(C.row_join(sp.zeros(10)))
    KD = domain(K)
    require(same(K, K.conjugate().T), 'Exact condition: same(K, K.conjugate().T)')
    require(KD.rank() == 28, 'Exact condition: KD.rank() == 28')
    raw_basis = KD.nullspace().to_Matrix()
    normalized = []
    for row in raw_basis.tolist():
        lead = next(x for x in row if x != 0)
        normalized.append([sp.cancel(x/lead) for x in row])
    N = sp.Matrix(normalized)  # six RIGHT kernel vectors, stored as rows
    require(N.shape == (6, 34), 'Exact condition: N.shape == (6, 34)')
    require(domain(N).rank() == 6, 'Exact condition: domain(N).rank() == 6')
    require(KD.matmul(domain(N.T)).is_zero_matrix, 'Exact condition: KD.matmul(domain(N.T)).is_zero_matrix')
    # Because K=K*, the actual left compatibility matrix is Nbar, not N.
    L = N.conjugate()
    require(domain(L).matmul(KD).is_zero_matrix, 'Exact condition: domain(L).matmul(KD).is_zero_matrix')

    # Metric-only forcing has no hidden link reaction: f_a=0. Verify that
    # its full six-row cokernel test is equivalent to these five conditions.
    T = sp.zeros(5, 10)
    T[0, 1] = 1
    T[1, 2] = T[1, 3] = 1
    T[2, 5] = T[2, 6] = 1
    T[3, 7], T[3, 8] = 2, 1
    T[4, 7], T[4, 9] = 1, -1
    Lq = L[:, 24:]
    require(domain(Lq).rank() == domain(T).rank() == 5, 'Exact condition: domain(Lq).rank() == domain(T).rank() == 5')
    require(domain(Lq.col_join(T)).rank() == 5, 'Exact condition: domain(Lq.col_join(T)).rank() == 5')

    return {"K": K, "H": H, "C": C, "N": N, "L": L, "T": T, "phase": phase}


def test_forcing(link_forcing, metric_forcing, context: dict | None = None) -> dict:
    """Exact finite source test; inputs are actual covectors, never fitted here."""
    ctx = build_context() if context is None else context
    fa, fq = sp.Matrix(link_forcing), sp.Matrix(metric_forcing)
    if fa.shape != (24, 1) or fq.shape != (10, 1):
        raise ValueError("Keep all 24 link and ten packed metric covector slots")
    forcing = fa.col_join(fq)
    residual = ctx["L"] * forcing
    residual_zero = domain(residual).is_zero_matrix
    augmented_rank = domain(ctx["K"].row_join(forcing)).rank()
    rank_compatible = augmented_rank == 28
    if residual_zero != rank_compatible:
        raise AssertionError("cokernel and independent augmented image rank disagree")
    return {"compatible": residual_zero, "augmented_rank": augmented_rank,
            "full_cokernel_residual": [str(sp.expand(x)) for x in residual],
            "metric_only_residual": [str(sp.expand(x)) for x in ctx["T"] * fq]}


def run_checks(repo: Path | None = None) -> dict:
    ctx = build_context(repo)
    K, H, C, N, L, T, phase = (ctx[key] for key in ("K", "H", "C", "N", "L", "T", "phase"))
    KD = domain(K)
    # Verify a complete basis of all compatible metric-only sources by the
    # independent augmented-rank image criterion, not only kernel tests.
    metric_image = sp.zeros(10, 5)
    metric_image[0, 0] = metric_image[4, 1] = 1
    metric_image[2, 2], metric_image[3, 2] = 1, -1
    metric_image[5, 3], metric_image[6, 3] = 1, -1
    metric_image[7, 4], metric_image[8, 4], metric_image[9, 4] = 1, -2, 1
    require(domain(metric_image).rank() == 5, 'Exact condition: domain(metric_image).rank() == 5')
    require(domain(T * metric_image).is_zero_matrix, 'Exact condition: domain(T * metric_image).is_zero_matrix')
    require(domain(K.row_join(sp.zeros(24, 5).col_join(metric_image))).rank() == 28, 'Exact condition: domain(K.row_join(sp.zeros(24, 5).col_join(metric_image))).rank() == 28')
    for column in range(5):
        require(test_forcing(sp.zeros(24, 1), metric_image[:, column], ctx)["compatible"], 'Exact condition: test_forcing(sp.zeros(24, 1), metric_image[:, column], ctx)["compatible"]')

    # Same nonzero metric source, different link forcing: all five reduced
    # metric tests agree, while only the pure-link sixth compatibility fails.
    fq = metric_image[:, 0]
    good = test_forcing(sp.zeros(24, 1), fq, ctx)
    bad_link = sp.zeros(24, 1)
    bad_link[16] = 1
    bad = test_forcing(bad_link, fq, ctx)
    require(good["compatible"] and not bad["compatible"], 'Exact condition: good["compatible"] and not bad["compatible"]')
    require(bad["full_cokernel_residual"] == ["-1", "0", "0", "0", "0", "0"], 'Exact condition: bad["full_cokernel_residual"] == ["-1", "0", "0", "0", "0", "0"]')
    require(good["metric_only_residual"] == bad["metric_only_residual"] == ["0"] * 5, 'Exact condition: good["metric_only_residual"] == bad["metric_only_residual"] == ["0"] * 5')

    bad_metric = sp.zeros(10, 1)
    bad_metric[1] = 1
    negative = test_forcing(sp.zeros(24, 1), bad_metric, ctx)
    require(not negative["compatible"] and negative["augmented_rank"] == 29, 'Exact condition: not negative["compatible"] and negative["augmented_rank"] == 29')

    # Conversely, an actual joint image can have a metric part which fails
    # the metric-only conditions: its genuine link reaction must be kept.
    column = next(j for j in range(24) if not domain(T*C[:, j]).is_zero_matrix)
    actual_image = K[:, column]
    reaction = test_forcing(actual_image[:24, :], actual_image[24:, :], ctx)
    require(reaction["compatible"] and any(x != "0" for x in reaction["metric_only_residual"]), 'Exact condition: reaction["compatible"] and any(x != "0" for x in reaction["metric_only_residual"])')

    fa_symbols = sp.symbols("f_a0:24")
    fq_symbols = sp.symbols("f_00 f_01 f_02 f_03 f_11 f_12 f_13 f_22 f_23 f_33")
    equations = [str(sp.expand(x)) for x in L * sp.Matrix(fa_symbols + fq_symbols)]
    metric_equations = [str(x) for x in T*sp.Matrix(fq_symbols)]
    report = {
        "scope": "single physical phase (1,1,i,i), finite exact geometric first source compatibility; not all torus, native source or GR",
        "source_pins": PINS,
        "source_paths": PATHS,
        "phase": [str(x) for x in phase],
        "connection_order": "6*role+generator; generators K1,K2,K3,J12,J13,J23",
        "metric_packed_order": METRIC,
        "matrix": "K=[[A.T,C.conjugate().T],[C,0]]; 24 connection + 10 metric variables",
        "fourier_convention": "u(x+delta)=phase^delta*u(x); reciprocal mixed block reverses input-minus-output shift",
        "metric_chart": "q=E.T*eta*E; E=I; deltaE=eta*deltaq/2; actual native chart identification required",
        "rank": KD.rank(), "nullity": N.rows,
        "right_kernel_sparse_rows": [{str(j): str(x) for j, x in enumerate(row) if x != 0} for row in N.tolist()],
        "full_left_compatibility": equations,
        "metric_only_equivalent_five_conditions": metric_equations,
        "metric_only_source_image_dimension_complex": 5,
        "sign": "E_geom+epsilon*dB=0 => K delta=-dB; compatibility Nbar*dB=0",
        "all_24_connection_and_10_metric_coordinates_retained_at_phase": True,
        "native_affine_matter_preparation_not_frozen_by_this_geometric_diagnostic": True,
        "full_native_action_source_binding_or_joint_root_derived": False,
    }
    report["complete_metric_only_image_basis_augmented_rank"] = 28
    report["same_metric_source_different_link_forcing"] = {
        "metric_source": "e_00", "good_link_source": "0", "bad_link_source": "e_16",
        "good": good, "bad": bad,
    }
    report["incompatible_metric_only_e01"] = negative
    report["actual_joint_image_needs_link_reaction"] = {
        "actual_image_column": column, "image_source": "K*e_" + str(column), "test": reaction,
    }
    return report


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    report = run_checks(args.repo)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("PASS_SINGLE_PHASE_LITERAL_JOINT_SOURCE_COMPATIBILITY")


if __name__ == "__main__":
    main()
