"""Exact controls for absolute positive-loop inversion and its GR error budget."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sympy as S


def run():
    root = Path(__file__).resolve()
    while not (root / "AGENTS.md").is_file():
        if root.parent == root:
            raise RuntimeError("repository root not found")
        root = root.parent
    pins = {
        "02_REGISTRY/research/A4D_BOOK03_SOURCE_IDENTIFIABILITY_THEOREM_2026_10_21.md":
            "ff50fe0d65cb2b3965affcfc528b5e7ef0a2bfe3b50682e4e4800319a8e7dc33",
        "02_REGISTRY/research/A4D_PRIMARY_NORMAL_SOURCE_RECOVERY_SYNTHESIS_2026_10_21.md":
            "d6ca03b9a16a352c7741eb9cb8657f34cd84c6a0a3c6f16e5b58c0b8574a3a22",
        "02_REGISTRY/research/A4D_CAUSAL_CLOCK_MINIMUM_AND_STATIONARY_SOURCE_DESCENT_2026_10_21.md":
            "b2715a08183fe1d4a58ea2d747ba45ef73e22071a73f671370a1b8f8c41546cc",
    }
    checks = []

    def ok(condition, label):
        if not condition:
            raise RuntimeError(label)
        checks.append(label)

    def eq(left, right, label):
        diff = left-right
        good = (all(S.simplify(v) == 0 for v in diff)
                if isinstance(diff, S.MatrixBase) else S.simplify(diff) == 0)
        ok(good, label)

    for p, sha in pins.items():
        ok(hashlib.sha256((root/p).read_bytes()).hexdigest() == sha, "pin "+p)
    f = S.Matrix([[S.Rational(1, 3), S.Rational(1, 10)],
                  [S.Rational(1, 10), S.Rational(1, 4)]])
    d = S.Matrix([[S.Rational(1, 5), S.Rational(1, 7)],
                  [S.Rational(1, 7), -S.Rational(1, 6)]])
    ok(f.det() > 0 and f[0, 0] > 0, "full relative operator is strictly positive")
    ok(f*d != d*f, "relative operator and its jet do not commute")
    a, b = S.Rational(2, 3), S.Rational(3, 5)
    s, t, dz, r = S.Rational(2, 11), S.Rational(3, 17), S.Rational(1, 13), 128
    direction = S.Symbol("direction", real=True)
    summaries = []
    for z in (S.Rational(1, 7), S.Rational(1, 2**20)):
        ra, rb = (S.eye(2)-z*a*f).inv(), (S.eye(2)-z*b*f).inv()
        margin = 1-z*a*S.trace(f)
        ok(margin > 0, f"positive resolvent margin at {z}")
        eq(a*ra-b*rb, (a-b)*ra*rb, f"weighted resolvent identity at {z}")
        eq(ra-rb, z*(a-b)*ra*f*rb, f"ordinary resolvent identity at {z}")
        chi = r*z*S.trace(ra*f)
        ok(chi >= r*z*S.trace(f) > 0, f"strict inverse conditioning at {z}")
        source = r*z*S.trace(ra*(a*d+f*s))
        recovered = (source-r*z*S.trace(ra*a*d))/chi
        eq(recovered, s, f"absolute jet recovers common scalar derivative at {z}")
        explicit = -r*S.log((S.eye(2)-z*(a+s*direction)*(f+direction*d)).det())
        eq(S.diff(explicit, direction).subs(direction, 0), source,
           f"independent determinant differentiation at {z}")
        moving = source+r*a*dz*S.trace(ra*f)
        eq((moving-r*S.trace(ra*(z*a*d+a*f*dz)))/chi, s,
           f"moving regulator retained at {z}")
        ok(S.simplify((moving-r*z*S.trace(ra*a*d))/chi-s) != 0,
           f"freezing actual moving regulator fails at {z}")
        ok((S.eye(2)-z*a*f).det() < (S.eye(2)-z*b*f).det(),
           f"absolute feedback value is strictly monotone at {z}")
        other = r*z*S.trace(rb*(b*d+f*t))
        bound = r*z*(abs(a-b)*sum(abs(v) for v in d)/margin**2
                     +S.trace(f)*abs(s-t)/margin
                     +z*S.trace(f*f)*abs(a-b)*abs(t)/margin**2)
        ok(abs(source-other) <= bound, f"full source error bound at {z}")
        summaries.append({"z":str(z),"chi":str(chi),"source_error":str(abs(source-other)),
                          "certified_bound":str(bound)})
    h = S.Symbol("h", positive=True)
    eq(h*h**5/(4*h**4), h**2/4, "h^5 residual gives h^2 profile with actual h^4 gain")
    eq(h*h**2/(4*h**4), 1/(4*h), "ignoring gain can turn h^2 source into divergent bound")
    return {"status":"PASS","input_snapshot":"2bbe9af6f3ce875898a28395c7c3ac2087a40277",
            "source_pins":pins,"checks":checks,"check_count":len(checks),"examples":summaries,
            "environment":{"python":platform.python_version(),"sympy":S.__version__},
            "scope":{"absolute_readout_and_binding_assumed":True,
                     "other_rows_must_vanish_for_normal_recovery":True,
                     "native_Info_derived":False,"GR_closed":False}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), ensure_ascii=False, indent=2)+"\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8", newline="\n")
    print(text, end="")
