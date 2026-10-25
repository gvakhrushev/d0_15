#!/usr/bin/env python3
"""Check the changed exact native return adapter only; no old suite replay."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import mpmath as mp
import sympy as sp
import native_echo as en

SOURCES = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SOURCES/"d0_query_feedback_first_book_2026-10-25"))
import query_book as qb
ne = en.native
from check_native_execution_domain import Quadratic
CHECKS = []


def check(name, assertion):
    if not assertion:
        raise AssertionError(name)
    CHECKS.append(name)


def numeric(a):
    return mp.matrix([[mp.mpf(str(sp.N(a[i, j], 80)))
                       for j in range(a.cols)] for i in range(a.rows)])


def trace(a):
    return mp.fsum(a[i, i] for i in range(a.rows))


def price(E, b, zeta):
    a, bb = en.feedback_bands(E, b)
    return -4*(mp.log1p(-zeta*a)+mp.log1p(-zeta*bb))


def run():
    mp.mp.dps = 70
    tol = mp.mpf("1e-50")
    zeta, beta, stages = mp.mpf(2)**-20, mp.mpf(1), 51
    middle = en.layout(en.middle_word())
    v = ne.word_matrix(middle)
    signed = sp.zeros(32)
    for col in range(32):
        e, b = (col >> 4) & 1, (col >> 3) & 1
        signed[col ^ (e << 2), col] = (-1)**(e+b)
    iv = ne.inventory(middle, **en.BOUNDS)
    check("actual eleven-letter middle is Z0 Z1 CX0,2 on ALL32 dirty-spin columns",
          ne.exact_matrix_equal(v, signed) and iv.gate_count == 11
          and iv.source_i_count == 4 and iv.cx_count == 7 and iv.g_count == 0)
    check("full native middle is an involution with sixteen plus and sixteen minus modes",
          ne.exact_matrix_equal(v*v, sp.eye(32)) and sp.trace(v) == 0)
    rows = []
    heat_reference = mp.log(32*(qb.character(0, stages, beta)
                                    +qb.character(mp.pi, stages, beta)))/beta
    for kE, kB in ((1, 1), (2, 1), (1, 2), (2, 2)):
        execution = en.echo(kE, kB, stages)
        w = ne.word_matrix(execution)
        inv = ne.inventory(execution, **en.BOUNDS)
        expected_body = 6*kE+12*kB+11
        check(f"actual full raw inverse counts and real common padding agree kE{kE} kB{kB}",
              len(en.echo(kE, kB).gates) == expected_body and inv.gate_count == stages
              and inv.g_count == 2*(kE+kB) and inv.source_i_count == 4*(kE+kB)+4
              and inv.cx_count == 6*kB+7+stages-expected_body
              and inv.full_dimension == 32 and inv.cut_rank == 8)
        a = sp.kronecker_product(ne.G_LOCAL**kE, ne.G_LOCAL**kB, sp.eye(8))
        check(f"completed echo equals A transpose V A on ALL32 input columns kE{kE} kB{kB}",
              ne.exact_matrix_equal(w, a.T*signed*a))
        small = w.extract(range(0, 32, 4), range(0, 32, 4))
        check(f"completed endpoint restores exact identity on the whole dirty source-spin kE{kE} kB{kB}",
              ne.exact_matrix_equal(w, sp.kronecker_product(small, sp.eye(4))))
        i = ne.input_isometry(execution)
        E, b = en.exact_bias(kE), en.exact_bias(kB)
        c = i.T*w*i
        c_expected = sp.kronecker_product(en.corner(E, b), sp.eye(4))
        f = sp.eye(8)-c.T*c
        aa, bb = en.feedback_bands(E, b)
        check(f"literal rank8 return corner and BOTH original defect bands are exact kE{kE} kB{kB}",
              ne.exact_matrix_equal(c, c_expected)
              and ne.exact_matrix_equal(f, i.T*w.T*(sp.eye(32)-i*i.T)*w*i)
              and ne.exact_matrix_equal((f-aa*sp.eye(8))*(f-bb*sp.eye(8)), sp.zeros(8)))
        # Numerical phases come from the actual exact full32 endpoint, not
        # a selected prepared column or an assumed initialized spin block.
        eigenvalues = mp.eigsy(numeric(w), eigvals_only=True)
        phases = [mp.mpf(0) if t > 0 else mp.pi for t in eigenvalues]
        partition = 2*mp.fsum(mp.exp(-beta*(1-mp.cos((angle+2*mp.pi*k)/stages)))
                             for angle in phases for k in range(stages))
        check(f"all matrix phases and ALL3264 paired clock modes give the same absolute heat kE{kE} kB{kB}",
              max(abs(abs(t)-1) for t in eigenvalues) < tol
              and sum(t > 0 for t in eigenvalues) == 16 and len(phases)*2*stages == 3264
              and abs(mp.log(partition)/beta-heat_reference) < tol)
        enu, bnu = numeric(sp.Matrix([[E, b]]))[0, 0], numeric(sp.Matrix([[E, b]]))[0, 1]
        j = -mp.log(mp.det(mp.eye(8)-zeta*numeric(f)))
        check(f"actual full-cut logdet equals four original rank2 feedback copies kE{kE} kB{kB}",
              abs(j-price(enu, bnu, zeta)) < tol)
        rows.append({"kE": kE, "kB": kB, "E": mp.nstr(enu, 30), "b": mp.nstr(bnu, 30),
                     "body_stages": expected_body, "padding_CX": stages-expected_body,
                     "actual_N": stages, "J": mp.nstr(j, 30), "heat": mp.nstr(heat_reference, 30),
                     "full_B": mp.nstr(j+heat_reference, 30)})
    check("actual native finite configuration contrasts survive the equal real clock",
          all(mp.mpf(rows[j]["J"]) > mp.mpf(rows[j+1]["J"]) for j in range(3)))
    # Nearby native E-only edits: exact Q(p) ordering plus literal inventories.
    # No long32 matrix or 6993-stage clock is constructed or diagonalized.
    qp, base = Quadratic(0, 1), Quadratic(-1, 2)
    tt = [Quadratic(1), base]
    for _ in range(2, 1162):
        tt.append(2*base*tt[-1]-tt[-2])
    es = {k: (1-tt[k])*Fraction(1, 2) for k in (1, 67, 1161)}
    check("exact nearby native E-only settings satisfy E67 less than E1 less than E1161",
          (es[1]-es[67]).sign() > 0 and (es[1161]-es[1]).sign() > 0
          and all((e-Fraction(37, 100)).sign() > 0 and (Fraction(2, 5)-e).sign() > 0
                  for e in es.values()))
    near_b = qp**2
    near_B = 4*near_b*(1-near_b)
    near_A = {k: 1-(1-4*e*(1-e))*(1-near_B) for k, e in es.items()}
    check("exact original feedback bands prove strict J67 less than J1 less than J1161",
          (1-near_B).sign() > 0 and (1-2*near_b).sign() > 0
          and (near_A[1]-near_A[67]).sign() > 0
          and (near_A[1161]-near_A[1]).sign() > 0)
    near_rows = []
    for kE in (1, 67, 1161):
        execution = en.echo(kE, 1, 6993)
        inv = ne.inventory(execution, **en.BOUNDS)
        body = 6*kE+23
        check(f"nearby native catalogue pays every actual stage and common N6993 kE{kE}",
              inv.gate_count == 6993 and inv.g_count == 2*(kE+1)
              and inv.source_i_count == 4*(kE+1)+4 and inv.cx_count == 13+6993-body
              and inv.cut_rank == 8 and inv.full_dimension == 32)
        near_rows.append({"kE": kE, "kB": 1, "body_stages": body, "padding_CX": 6993-body,
                          "actual_N": 6993, "E_Qp_sha256": es[kE].digest()})
    p = qb.golden()
    correlated = en.correlated_echo(stages)
    ci = ne.inventory(correlated, **en.BOUNDS)
    wc = ne.word_matrix(correlated)
    ac = ne.word_matrix(en.layout((ne.Gate("G", (0,)), ne.Gate("CX", (0, 1)))))
    ap = sp.kronecker_product(ne.G_LOCAL, ne.G_LOCAL, sp.eye(8))
    probabilities = lambda a: sp.Matrix([[sum(a[8*k+j, 0]**2 for j in range(8)) for k in range(4)]])
    pc, pp = probabilities(ac), probabilities(ap)
    check("actual correlated programme preserves BOTH native base marginals but changes the joint law",
          ne.exact_matrix_equal(pc, sp.Matrix([[ne.P, 0, 0, ne.P**2]]))
          and ne.exact_matrix_equal(sp.Matrix([[pc[0, 2]+pc[0, 3], pc[0, 1]+pc[0, 3]]]),
                                    sp.Matrix([[pp[0, 2]+pp[0, 3], pp[0, 1]+pp[0, 3]]]))
          and not ne.exact_matrix_equal(pc, pp))
    check("correlated echo has actual19stage body plus32CX at the same full carrier and clock",
          len(en.correlated_echo(19).gates) == 19 and ci.gate_count == 51
          and ci.g_count == 2 and ci.source_i_count == 8 and ci.cx_count == 41
          and ci.cut_rank == 8 and ci.full_dimension == 32)
    check("actual correlated echo is A transpose V A on ALL32 columns with identical full heat",
          ne.exact_matrix_equal(wc, ac.T*signed*ac)
          and ne.exact_matrix_equal(wc*wc, sp.eye(32)) and sp.trace(wc) == 0)
    ic = ne.input_isometry(correlated)
    cc = ic.T*wc*ic
    x2 = sp.Matrix([[0, 1], [1, 0]])
    check("same-marginal correlated native input gives pI plus p squared X and bands zero L",
          ne.exact_matrix_equal(cc, sp.kronecker_product(ne.P*sp.eye(2)+ne.P**2*x2, sp.eye(4)))
          and ne.exact_matrix_equal((sp.eye(8)-cc.T*cc)*(cc.T*cc-ne.P**6*sp.eye(8)), sp.zeros(8)))
    jc = -mp.log(mp.det(mp.eye(8)-zeta*(mp.eye(8)-numeric(cc.T*cc))))
    correlation_gap = -4*mp.log1p(-zeta*(1-p**12))
    check("actual same-marginal native controller edit has the exact strictly lower full Book price",
          (1-qp**12).sign() > 0 and (1-Fraction(1, 2**20)*(1-qp**12)).sign() > 0
          and correlation_gap > 0 and abs(price(p*p, p*p, zeta)-jc-correlation_gap) < tol)
    v8 = numeric(signed.extract(range(0, 32, 4), range(0, 32, 4)))
    def matrix_price(E, b):
        a = qb.kron(qb.kron(qb.rotation(mp.asin(mp.sqrt(E))),
                           qb.rotation(mp.asin(mp.sqrt(b)))), mp.eye(2))
        w = a.T*v8*a
        c = w[:2, :2]
        return -4*mp.log(mp.det((1-zeta)*mp.eye(2)+zeta*c.T*c))
    source = lambda x, y: matrix_price(p*p*(1+x), (p-p*p*y)**2)
    jx = 4*zeta*p**11/(1-zeta+zeta*p**12)
    jy = -8*zeta*p**6*(p**6/(1-zeta+zeta*p**12)+1/(1-zeta+zeta*p**6))
    check("real comparison source retains original x y chain and spin multiplicity",
          abs(matrix_price(p*p, p*p)-price(p*p, p*p, zeta)) < tol
          and abs(mp.diff(lambda x: source(x, 0), 0)-4*jx) < tol
          and abs(mp.diff(lambda y: source(0, y), 0)-4*jy) < tol)
    e_source = mp.diff(lambda E: matrix_price(E, p*p), p*p)
    b_source = mp.diff(lambda b: matrix_price(p*p, b), p*p)
    check("independent programme E and b biases have strictly nonzero positive source at native base",
          e_source > 0 and b_source > 0)
    c2 = numeric(en.corner(p*p, p*p))
    gram = (1-zeta)*mp.eye(2)+zeta*c2.T*c2
    branches = (mp.eye(2), -mp.eye(2), -mp.matrix([[0, 1], [1, 0]]), mp.matrix([[0, 1], [1, 0]]))
    obs = [-8*zeta*mp.re(trace(gram**-1*c2.T*k)) for k in branches]
    chi = mp.matrix([p, p**mp.mpf("1.5"), p**mp.mpf("1.5"), p*p])
    mean = mp.fsum(obs[k]*abs(chi[k])**2 for k in range(4))
    grad = [2*(obs[k]-mean)*chi[k] for k in range(4)]
    grad_norm = mp.sqrt(mp.fsum(abs(t)**2 for t in grad))
    check("actual full CP3 preparation normal fails despite the correct field-source corner",
          min(mp.eigsy(c2, eigvals_only=True)) > 0 and obs[0] < 0 < obs[1]
          and abs(obs[0]+obs[1]) < tol and grad_norm > mp.mpf("1e-8"))
    def correlation_price(t):
        c = c2+2*t*(mp.eye(2)+mp.matrix([[0, 1], [1, 0]]))
        return -4*mp.log(mp.det((1-zeta)*mp.eye(2)+zeta*c.T*c))
    correlation_source = -32*zeta*p**6/(1-zeta+zeta*p**12)
    check("fixed-marginal correlation normal has the exact nonzero full feedback source",
          correlation_source < 0 and abs(mp.diff(correlation_price, 0)-correlation_source) < tol)
    return {"checks": CHECKS, "checks_passed": len(CHECKS), "rows": rows, "nearby_native_catalogue": near_rows,
            "same_marginal_correlated_edit": {"body_stages": 19, "padding_CX": 32,
                "actual_N": 51, "J": mp.nstr(jc, 30), "strict_price_drop": mp.nstr(correlation_gap, 30),
                "correlation_source": mp.nstr(correlation_source, 30), "same_marginals_imply_same_task_claimed": False},
            "N": stages, "full_dimension": 32, "input_cut_rank": 8, "paired_clock_modes": 3264,
            "matrix_scope": "actual complete native ALL32 endpoints and literal full primitive stage lists",
            "numeric_arithmetic": "70-digit mpmath non-interval; exact Q(sqrt(p)) native matrix equalities separate",
            "base_sources": {"D_E": mp.nstr(e_source, 30), "D_b": mp.nstr(b_source, 30),
                             "D_x": mp.nstr(4*jx, 30), "D_y": mp.nstr(4*jy, 30),
                             "full_CP3_gradient_norm": mp.nstr(grad_norm, 30)},
            "original_return_corner_realized": True, "original_full8_logical_query_realized": False,
            "readiness_herald_or_SK_used": False, "continuous_native_word_family_proved": False,
            "long_word_matrix_or_clock_replayed": False,
            "independent_preparation_Euler_closed": False, "physical_all_variation_admission_proved": False,
            "native_geometry_writer_proved": False, "GR_closed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    result.update(schema="d0.native-bilinear-return-echo-check/1", status="PASS")
    paths = [Path(__file__).resolve(), Path(en.__file__).resolve(), Path(__file__).with_name("PROOF.md"),
             en.DOMAIN/"native_execution.py", en.DOMAIN/"check_native_execution_domain.py", Path(qb.__file__).resolve(),
             SOURCES/"d0_query_feedback_first_book_2026-10-25"/"PROOF.md",
             SOURCES/"d0_native_gr_completion_synthesis_2026-10-20"/"book_source"/"TWO_NATIVE_8D_DETERMINANT_SOURCE.md",
             SOURCES/"d0_physical_cap1_execution_composition_2026-10-21"/"moving_query"/"PROOF.md"]
    result["inputs_sha256"] = {str(p.relative_to(SOURCES)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    result["runtime"] = {"python": sys.version.split()[0], "mpmath": mp.__version__, "sympy": sp.__version__}
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
