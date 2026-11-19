"""Exact field obstruction for the specified blank/factory full32 writer."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import subprocess
import sympy as S


def run():
    root = Path(__file__).resolve()
    while not (root / "AGENTS.md").is_file():
        if root.parent == root:
            raise RuntimeError("repository root not found")
        root = root.parent
    pins = {
        "02_REGISTRY/research/sources/d0_common_execution_closure_2026-10-21/native_processor/FIXED_PROCESSOR_PROGRAM_SOURCE.md":
            "4a879a3bb986aca43f06cec760f882cec4e7c6446efd46d5add8a2f199e9381b",
        "02_REGISTRY/research/A4D_NATIVE_COMPILER_SOURCE_AND_RESOURCE_BOUNDARY.md":
            "7b2121fdaa2ebd4f98be494d6062034577971d334b00bddf9ef9da8969f8f817",
        "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/DETERMINANT_PREPARATION_BANK.md":
            "6cc9fc85ef8e238635ef24b78ddb3936f07d1a3f915558172eee8ff1c3602705",
    }
    historical_pins = {
        "02_REGISTRY/research/A4D_NEXT_COMMON_MAP_CONSTRUCTION_GATE_2026_10_21.md": {
            "ref": "43adff715186cdb9a4c8fc7fa04986600f7d24cc",
            "sha256": "0d407c28b4a2a4f969889120f01aa109d878468cb782c4019bfe68bc3a8133d5",
        },
    }
    checks = []

    def ok(condition, label):
        if not condition:
            raise RuntimeError(label)
        checks.append(label)

    def eq(left, right, label):
        diff = left-right
        good = (all(S.simplify(x) == 0 for x in diff)
                if isinstance(diff, S.MatrixBase) else S.simplify(diff) == 0)
        ok(good, label)

    for path, sha in pins.items():
        ok(hashlib.sha256((root/path).read_bytes()).hexdigest() == sha, "pin "+path)
    for path, pin in historical_pins.items():
        source = subprocess.check_output(["git", "show", pin["ref"]+":"+path], cwd=root)
        ok(hashlib.sha256(source).hexdigest() == pin["sha256"],
           "historical pin "+pin["ref"]+":"+path)
    x, t = S.symbols("x t")
    p = (S.sqrt(5)-1)/2
    a = S.sqrt(p)
    f = t**4+t**2-1
    ok(S.Poly(f, t).is_irreducible, "Golden amplitude has degree four over Q")
    eq(f.subs(t, a), 0, "actual positive Golden root satisfies the quartic")
    pconjugate = (-S.sqrt(5)-1)/2
    eq(p*pconjugate, -1, "Golden square has negative quadratic-field norm")
    eq((3/p)*(3/pconjugate), -9, "sqrt3 alternate-basis case has negative square norm")
    ok(not S.integer_nthroot(3, 2)[1], "3 is not a rational square")
    ok(not S.integer_nthroot(3, 2)[1] and not S.integer_nthroot(5, 2)[1],
       "3/5 is not a rational square in lowest terms")
    resultant = S.resultant(f, (x-t)**2-3, t)
    expected = x**8-10*x**6+47*x**4-170*x**2+121
    eq(resultant, expected, "exact Golden-plus-sqrt3 compositum resultant")
    ok(S.degree(resultant, x) == 8 and S.Poly(resultant, x).is_irreducible,
       "independent degree-eight compositum certificate excludes sqrt3 from K")
    g = S.Matrix([[a, -p], [p, a]])
    eq(g.T*g, S.eye(2), "literal Golden gate remains unitary")
    eq(a*(a**3+a), 1, "Golden inverse amplitude is still in K")
    half = S.Matrix([[S.Rational(1, 2), S.sqrt(3)/2],
                     [S.sqrt(3)/2, -S.Rational(1, 2)]])
    full = S.kronecker_product(half, S.eye(16))
    eq(full.T*full, S.eye(32), "actual flat half-Julia uses all32 coordinates")
    eq(full[16, 0]/full[0, 0], S.sqrt(3),
       "actual vacuum programme coordinates require the excluded relative amplitude")
    # Two-address fixture: one actual flat link, one padded identity address.
    raw = S.Matrix([block[row, col] for block in (full, S.eye(32))
                    for col in range(32) for row in range(32)])
    eq(raw.dot(raw), 64, "complete two-address Choi fixture has norm Ad")
    omega = raw/8
    eq(omega.dot(omega), 1, "complete normalized two-address programme fixture")
    eq(omega[16]/omega[0], S.sqrt(3),
       "address and Choi normalization cannot remove the actual relative witness")
    golden_julia = S.Matrix([[p, a], [a, -p]])
    eq(golden_julia.T*golden_julia, S.eye(2), "different p-Golden flat Julia is a valid positive control")
    eq(golden_julia[1, 0]/golden_julia[0, 0], a**3+a,
       "p-Golden flat Julia ratio lies inside K and is not excluded")
    fair_raw = S.Matrix([1, 1])
    eq(fair_raw[1]/fair_raw[0], 1, "supplied and heralded fair seeds are projectively K-valued")
    h_raw = S.Matrix([[1, 1], [1, -1]])
    eq(h_raw.T*h_raw, 2*S.eye(2), "paid logical H has only a common non-K normalization")
    # A non-K logical encoding really can evade the fixed computational-code hypothesis.
    s4 = S.ones(4, 1)/2
    reflection = S.eye(4)-2*s4*s4.T
    embedding = S.Matrix.hstack(S.eye(4)[:, 0], S.Matrix([0, 1, 1, 1])/S.sqrt(3))
    encoded = S.Matrix([[S.Rational(1, 2), -S.sqrt(3)/2],
                        [-S.sqrt(3)/2, -S.Rational(1, 2)]])
    eq(reflection.T*reflection, S.eye(4), "larger rational reflection is a full orthogonal operator")
    ok(all(v.is_Rational for v in reflection), "encoded escape uses a rational physical matrix")
    eq(embedding.T*embedding, S.eye(2), "non-K logical encoding is isometric")
    eq(reflection*embedding, embedding*encoded,
       "encoded escape has the stated non-K logical block with no leakage")
    eq(embedding.T*reflection*embedding, encoded,
       "fixed-code exclusion is not promoted to a basis-independent no-go")
    return {"status":"PASS","input_snapshot":"faa0064285c0f66627cac7382a341998033f9cde",
            "source_pins":pins,"historical_source_pins":historical_pins,
            "checks":checks,"check_count":len(checks),
            "quartic":str(f),"compositum_polynomial":str(resultant),
            "environment":{"python":platform.python_version(),"sympy":S.__version__},
            "scope":{"target":"supplied half-Julia programme in its specified computational code",
                     "seed_class":"projectively K-valued active inputs; passive RIGHT allowed",
                     "finite_postselection_and_factories_included":True,
                     "actual_full32_flat_block_checked":True,
                     "address_fixture":2,"full_spatial_programme_bank_replayed":False,
                     "encoded_escape_explicitly_preserved":True,
                     "approximation_excluded":False,"all_D0_writers_excluded":False,
                     "Book_Info_selected":False,"GR_closed":False}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), ensure_ascii=False, indent=2)+"\n"
    if args.output:
        args.output.write_text(result, encoding="utf-8", newline="\n")
    print(result, end="")
