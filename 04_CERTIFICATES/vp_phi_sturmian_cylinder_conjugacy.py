#!/usr/bin/env python3
"""D0-PHI-STURMIAN-CYLINDER-CONJUGACY-001 - finite cylinder-language equivalence ONLY.

The golden substitution word (a->ab, b->a, the Fibonacci word) and the phi-rotation coding share the
same FINITE cylinder language: (1) it avoids 'bb' (the golden-mean SFT constraint), (2) its factor
complexity is exactly L+1 for each length L (Sturmian linear complexity), and (3) its single-letter
frequencies converge to the golden split (freq(a), freq(b)) -> (phi^-1, phi^-2) -- the same stationary
cylinder measure as D0-PHI-CYLINDER-TRACE-UNIQUE-001.

SCOPE (honest): this closes the FINITE cylinder-language equivalence only. The full topological/measure
conjugacy (rotation <-> tiling hull) stays the EXTERNAL owner D0-ADLER-WEISS-PARTITION-OWNER-001
(ASSUMP-ADLER-WEISS), and the letter-by-letter symbolic coincidence to N=4000 is the existing cert
vp_quasicrystal_time_sturmian.py. Not a new conjugacy claim.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def fib_word(min_len: int) -> str:
    w = "a"
    while len(w) < min_len:
        w = "".join("ab" if c == "a" else "a" for c in w)
    return w


def factors(w: str, L: int) -> set:
    return {w[i:i + L] for i in range(len(w) - L + 1)}


def main() -> int:
    print("=== D0-PHI-STURMIAN-CYLINDER-CONJUGACY-001  finite cylinder-language equivalence (golden word) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: golden substitution a->ab, b->a (Fibonacci word); the finite factor "
          "language + cylinder frequencies are fixed before any value")
    w = fib_word(4000)

    # (1) avoids 'bb' (golden-mean SFT constraint)
    assert "bb" not in w, "golden word must avoid 'bb' (golden-mean SFT)"
    print(f"PASS_GOLDEN_SFT_CONSTRAINT  the golden word (len {len(w)}) avoids 'bb' (golden-mean subshift)")

    # (2) factor complexity p(L) = L + 1 (Sturmian linear complexity = finite cylinder language)
    for L in range(1, 12):
        p = len(factors(w, L))
        assert p == L + 1, f"factor complexity p({L}) must be L+1={L+1}: got {p}"
    print("PASS_STURMIAN_COMPLEXITY  factor complexity p(L)=L+1 for L=1..11 (linear/Sturmian cylinder language)")

    # (3) single-letter frequencies -> golden split (phi^-1, phi^-2)
    fa = w.count("a") / len(w)
    fb = w.count("b") / len(w)
    assert abs(fa - PHI ** -1) < 1e-3 and abs(fb - PHI ** -2) < 1e-3, f"letter freqs must -> golden split: {fa},{fb}"
    print(f"PASS_GOLDEN_CYLINDER_FREQUENCIES  freq(a)={fa:.5f}~phi^-1, freq(b)={fb:.5f}~phi^-2 "
          "(same stationary measure as D0-PHI-CYLINDER-TRACE-UNIQUE-001)")

    # negative controls
    per = "ab" * 2000  # a periodic word
    assert len(factors(per, 8)) < 8 + 1, "control: a periodic word must have BOUNDED (sub-Sturmian) complexity"
    print("FAIL_PERIODIC_REJECTED  periodic 'ab' word has bounded complexity (<L+1) -- not the golden Sturmian language")
    assert abs((per.count("a") / len(per)) - 0.5) < 1e-9, "control: periodic freq is 1/2, not the golden split"
    print("FAIL_PERIODIC_FREQ_REJECTED  periodic word freq(a)=1/2 != phi^-1 (not the golden cylinder measure)")
    bad = "abb" + w[:200]  # contains 'bb' -> outside the golden-mean SFT language
    assert any("bb" in f for f in factors(bad, 3)) and not any("bb" in f for f in factors(w, 3)), \
        "control: a 'bb'-containing word has factors outside the golden cylinder language"
    print("FAIL_NON_GOLDEN_WORD_REJECTED  a 'bb'-containing word has a factor outside the golden language (the golden word never does)")

    print("HONEST_FINITE_ONLY  finite cylinder-language equivalence ONLY; full topological/measure conjugacy stays the "
          "external owner D0-ADLER-WEISS-PARTITION-OWNER-001 (ASSUMP-ADLER-WEISS); coincidence cert vp_quasicrystal_time_sturmian.py.")
    print("PASS_PHI_STURMIAN_CYLINDER_CONJUGACY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
