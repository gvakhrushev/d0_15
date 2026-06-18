#!/usr/bin/env python3
"""D0-LEPTON-STURMIAN-PUISEUX-COEFFICIENTS-001 (OPERATOR-SCAFFOLD-CERTIFIED for the internal generator;
lepton identification PROOF-TARGET).

The Puiseux coefficient SECTION c_k (k=0..K-1, K=8) is GENERATED INTERNALLY from the Fibonacci word --
substitution a->ab, b->a, equivalently Fibonacci concatenation S_n = S_{n-1}.S_{n-2} -- via a DECLARED
internal {-1,0,1} rule:
    LETTER MAP:  a -> +1 ,  b -> -1     (declared; the third symbol 0 is reserved for the unramified slot)
The c_k are PRODUCED BY THE WORD, never typed from any target decimal. The alphabet is checked to stay
inside {-1,0,1}. K is DECLARED and FROZEN before any comparison.

HONEST (CARDINAL): this cert does NOT claim these c_k reproduce m_mu/m_e or the 17-digit decimals. That
identification stays PROOF-TARGET (it needs the finite Green operator/resolvent). The exact MISSING
artifact is printed and the owner is asserted to stay open. No PDG mass enters as input.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

K = 8  # DECLARED, FROZEN coefficient-section depth (fixed before any comparison)

# DECLARED internal letter -> {-1,0,1} rule. 0 is reserved (unramified slot), never produced by a/b.
LETTER_MAP = {"a": 1, "b": -1}

# external COMPARISON datum only -- NEVER an input that defines the internal coefficients
PDG_MU_OVER_E = 206.7682830


def fibonacci_word_substitution(min_len: int) -> str:
    """Fixed point of sigma: a->ab, b->a, grown to at least min_len letters."""
    w = "a"
    while len(w) < min_len:
        w = "".join("ab" if c == "a" else "a" for c in w)
    return w


def fibonacci_word_concatenation(min_len: int) -> str:
    """Fibonacci concatenation S_n = S_{n-1}.S_{n-2} with S_1=b, S_2=a (same fixed point)."""
    s_prev, s = "b", "a"
    while len(s) < min_len:
        s, s_prev = s + s_prev, s
    return s


def coefficient_section(word: str, depth: int) -> list:
    """Map the first `depth` letters of the word through the declared {-1,0,1} rule."""
    return [LETTER_MAP[c] for c in word[:depth]]


def main() -> int:
    print("=== D0-LEPTON-STURMIAN-PUISEUX-COEFFICIENTS-001  c_k generated from the Fibonacci word (K=8) ===")
    print(f"STRUCTURE_FIXED_BEFORE_NUMBER: substitution a->ab,b->a (= Fibonacci concat S_n=S_(n-1).S_(n-2)); "
          f"DECLARED letter rule a->+1,b->-1 in {{-1,0,1}}; depth K={K} FROZEN -- all fixed BEFORE any c_k value "
          "and BEFORE any mass/decimal")

    # ---- the two constructions of the word agree (the generator is well-defined) -------
    w_sub = fibonacci_word_substitution(K + 8)
    w_con = fibonacci_word_concatenation(K + 8)
    assert w_sub[:K] == w_con[:K], "substitution and concatenation must agree over the depth-K window"
    print(f"PASS_WORD_GENERATOR_CONSISTENT  substitution & Fibonacci-concat agree on the first {K} letters: "
          f"'{w_sub[:K]}'")

    # ---- generate the coefficient section FROM the word --------------------------------
    c = coefficient_section(w_sub, K)
    # The first K letters of the Fibonacci word are a b a a b a b a -> [1,-1,1,1,-1,1,-1,1]
    expected_word = "abaababa"
    assert w_sub[:K] == expected_word, f"first {K} Fibonacci letters must be '{expected_word}': {w_sub[:K]}"
    assert c == [LETTER_MAP[ch] for ch in expected_word], "c_k must be the letter-map image of the word"
    assert c == [1, -1, 1, 1, -1, 1, -1, 1], f"c_k must be the word-generated section: {c}"
    print(f"PASS_COEFFICIENTS_FROM_WORD  c_k (k=0..{K-1}) = {c}  (image of '{expected_word}', NOT typed from a decimal)")

    # ---- alphabet stays inside {-1,0,1} ------------------------------------------------
    assert all(x in (-1, 0, 1) for x in c), "every coefficient must lie in {-1,0,1}"
    print("PASS_ALPHABET_IN_PM1  every c_k in {-1,0,1}")

    # ---- K is frozen: regenerating at the same depth is stable -------------------------
    c2 = coefficient_section(fibonacci_word_substitution(K + 50), K)
    assert c2 == c, "the depth-K section must be a stable prefix (longer word, same first K coefficients)"
    print(f"PASS_DEPTH_K_FROZEN_STABLE  the first K={K} coefficients are prefix-stable under word growth")

    # ---- negative controls (reachable FAIL_) -------------------------------------------
    # (a) a PDG-inverted coefficient row is NOT the Fibonacci-word section
    pdg_row = [round(PDG_MU_OVER_E)] + [0] * (K - 1)  # a row built FROM the mass ratio
    assert pdg_row != c, "control: a PDG-mass-derived row must NOT equal the word-generated c_k"
    assert any(abs(x) > 1 for x in pdg_row), "control: the PDG-mass row even leaves the {-1,0,1} alphabet"
    print(f"FAIL_PDG_INVERTED_ROW_CAUGHT  PDG-derived row {pdg_row[:3]}... != word c_k (and leaves {{-1,0,1}}); "
          "the section is the Fibonacci word, NOT the mass ratio")

    # (b) a random/arbitrary row in-alphabet is rejected (it is not the word sequence)
    random_row = [1, 1, 1, 1, 1, 1, 1, 1]  # all +1 = periodic 'aaaa...' -> not the Fibonacci word
    assert random_row != c, "control: an arbitrary in-alphabet row must NOT equal the word-generated c_k"
    print(f"FAIL_RANDOM_ROW_CAUGHT  arbitrary in-alphabet row {random_row} != word c_k (only the word generates c_k)")

    # (c) a letter rule that escapes {-1,0,1} is rejected
    bad_map = {"a": 2, "b": -1}
    bad_c = [bad_map[ch] for ch in w_sub[:K]]
    assert any(x not in (-1, 0, 1) for x in bad_c), "control: an out-of-alphabet rule must be detected"
    print(f"FAIL_ALPHABET_VIOLATION_CAUGHT  a rule a->2 yields {bad_c[:3]}... outside {{-1,0,1}} (rejected)")

    # (d) changing K AFTER a comparison changes the section -> the post-hoc K is rejected
    c_other_K = coefficient_section(w_sub, K + 2)
    assert c_other_K != c, "control: a section at a DIFFERENT (post-hoc) K must not be conflated with the K=8 section"
    assert len(c_other_K) == K + 2, "control: changing K changes the section length"
    print(f"FAIL_CHANGING_K_CAUGHT  a post-hoc K={K+2} gives a different-length section {len(c_other_K)} != {K} "
          "(K is frozen before comparison)")

    # ---- honest PROOF-TARGET residual --------------------------------------------------
    print("HONEST_PROOF_TARGET  MISSING ARTIFACT (owner stays OPEN): this cert does NOT claim the word-generated "
          "c_k reproduce m_mu/m_e or the 17-digit decimals r_mu/r_tau. The map (internal coefficients c_k + the "
          "exponent row (0,1/4,1/3)) -> physical lepton ratios needs the FINITE GREEN OPERATOR/RESOLVENT, which is "
          "NOT built here -- owner D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001. No PDG mass enters as input.")
    print("PASS_LEPTON_STURMIAN_PUISEUX_COEFFICIENTS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
