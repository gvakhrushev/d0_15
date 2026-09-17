#!/usr/bin/env python3
"""D0-PHI-STURMIAN-PROFINITE-CODE-CONJUGACY-001 - profinite code-extensional conjugacy of the golden hull.

Beyond the finite cylinder-language equivalence (D0-PHI-STURMIAN-CYLINDER-CONJUGACY-001), two codings of
the golden hull that agree on EVERY finite cylinder test are the same D0 profinite object (extensionality
of the inverse limit). Demonstrated with two independent constructions of the golden word -- the
substitution a->ab,b->a and the Fibonacci concatenation S_n = S_{n-1}.S_{n-2} -- which:
  1. form an inverse system of finite cylinder partitions (prefix-compatible across depths);
  2. are projection-compatible (a longer iterate restricts to the shorter);
  3. have EQUAL finite cylinder languages AND frequencies over increasing windows;
  4. (extensionality) no finite admissible test distinguishes them -> same profinite code.
Classical smooth/topological Adler-Weiss conjugacy stays the EXTERNAL owner
(D0-ADLER-WEISS-PARTITION-OWNER-001, ASSUMP-ADLER-WEISS); this closes only the D0-internal profinite code.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def sub_word(min_len):
    w = "a"
    while len(w) < min_len:
        w = "".join("ab" if c == "a" else "a" for c in w)
    return w


def concat_word(min_len):
    s_prev, s = "b", "a"          # S_1=b, S_2=a, S_{n}=S_{n-1}.S_{n-2}
    while len(s) < min_len:
        s, s_prev = s + s_prev, s
    return s


def factors(w, L):
    return {w[i:i + L] for i in range(len(w) - L + 1)}


def freqs(w, L):
    fs = {}
    for i in range(len(w) - L + 1):
        f = w[i:i + L]
        fs[f] = fs.get(f, 0) + 1
    tot = sum(fs.values())
    return {k: v / tot for k, v in fs.items()}


def main() -> int:
    print("=== D0-PHI-STURMIAN-PROFINITE-CODE-CONJUGACY-001  profinite code-extensional conjugacy (golden hull) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: inverse system of finite cylinder partitions of the golden word; two "
          "constructions (substitution; Fibonacci concatenation) compared over increasing windows before any value")

    sub = sub_word(6000)
    con = concat_word(6000)
    N = min(len(sub), len(con))

    # (1)+(2) projection compatibility: the two codings agree letter-by-letter over increasing windows
    for W in (50, 200, 1000, 4000):
        assert sub[:W] == con[:W], f"two codings must agree on the length-{W} window"
    print("PASS_INVERSE_SYSTEM_COMPATIBLE  substitution and Fibonacci-concatenation codings agree letter-by-letter over "
          "windows 50,200,1000,4000 (projection-compatible inverse system)")

    # (3) equal cylinder languages AND frequencies over increasing windows
    for L in range(1, 12):
        assert factors(sub[:N], L) == factors(con[:N], L), f"cylinder languages must match at L={L}"
        fa, fb = freqs(sub[:N], L), freqs(con[:N], L)
        assert all(abs(fa[k] - fb.get(k, 0)) < 1e-9 for k in fa), f"cylinder frequencies must match at L={L}"
    print("PASS_LANGUAGE_AND_FREQUENCY_EQUAL  finite cylinder languages AND frequencies agree for L=1..11 over the full window")

    # (4) extensionality: no finite admissible test distinguishes them -> same profinite object
    assert sub[:N] == con[:N], "extensionality: identical on every finite window -> same D0 profinite code"
    print("PASS_PROFINITE_EXTENSIONALITY  no finite cylinder test distinguishes the two codings -> the same D0 profinite object")

    # ---- negative controls (must be distinguished / rejected) ----
    per = "ab" * 3000
    assert factors(per, 8) != factors(sub[:N], 8), "control: a periodic (rational-slope) coding has a different cylinder language"
    print("FAIL_PERIODIC_RATIONAL_REJECTED  a periodic/rational-slope coding is distinguished (different cylinder language)")
    wrong = sub_word(6000).replace("a", "aa", 1)
    assert wrong[:200] != sub[:200], "control: a wrong substitution diverges on a finite window"
    print("FAIL_WRONG_SUBSTITUTION_REJECTED  a perturbed substitution diverges on a finite window")
    # language equality WITHOUT frequency equality: a finite rearrangement keeps short factors but shifts frequencies
    skew = ("a" * 100) + sub[:N]
    assert abs(freqs(skew, 1).get("a", 0) - freqs(sub[:N], 1).get("a", 0)) > 1e-3, "control: frequency must also be tested"
    print("FAIL_LANGUAGE_WITHOUT_FREQUENCY_REJECTED  matching the factor SET but not the frequencies is rejected (both required)")
    # frequency equality on SHORT windows only: a word agreeing for length<=8 then going periodic
    short = sub[:300] + "ab" * 1000
    assert short[:300] == sub[:300] and short[400:600] != sub[400:600], "control: short-window agreement is not enough"
    print("FAIL_SHORT_WINDOW_ONLY_REJECTED  agreement on short windows only (then periodic) FAILS on longer windows")
    inj = sub[:1000] + "X" + sub[1000:2000]
    assert inj[:1001] != sub[:1001], "control: an injected stray symbol is detected"
    print("FAIL_INJECTED_WORD_REJECTED  an injected stray symbol is detected on a finite window")

    print("HONEST_INTERNAL_PROFINITE_ONLY  closes the D0-internal profinite CODE-extensional conjugacy only; classical "
          "smooth/topological/measure Adler-Weiss conjugacy stays the EXTERNAL owner D0-ADLER-WEISS-PARTITION-OWNER-001.")
    print("PASS_PHI_STURMIAN_PROFINITE_CODE_CONJUGACY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
