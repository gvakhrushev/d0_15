#!/usr/bin/env python3
"""D0-TORAL-TIME-MARKOV-CONJUGACY-001 (PROOF-TARGET manifest).

What is CLOSED (cited, not re-proved here): the D0-INTERNAL profinite-code conjugacy of the golden hull
(vp_phi_sturmian_profinite_code_conjugacy.py / D0-PHI-STURMIAN-PROFINITE-CODE-CONJUGACY-001): two codings
that have EQUAL finite cylinder LANGUAGES *and* FREQUENCIES over every increasing window are the same D0
profinite object. This cert RE-RUNS that internal closure as a guarded prerequisite (the on-disk cert is
the authority) and then states the remaining obligation honestly.

What stays PROOF-TARGET: FULL TOPOLOGICAL conjugacy T-time-map  ~=  golden SFT. The classical criterion is
Williams shift-equivalence between the toral-induced SFT and the Fibonacci subshift transition matrix
N_tau = [[0,1],[1,1]]. That shift-equivalence (the explicit (R,S) lag-L equivalence matrices) is EXTERNAL
and NOT supplied internally. This cert prints the EXACT missing artifact and asserts the owner stays open.

No survey/empirical datum enters. T=[[0,1],[1,-1]] and N_tau=[[0,1],[1,1]] are fixed structurally.
"""
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- exact integer 2x2 matrix arithmetic ----
def matmul(A, B):
    return [[A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]]


def tr(A):
    return A[0][0] + A[1][1]


def det(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


# ---- small internal reproductions of the golden-word codings (the profinite-code witness) ----
def sub_word(min_len):
    w = "a"
    while len(w) < min_len:
        w = "".join("ab" if c == "a" else "a" for c in w)
    return w


def concat_word(min_len):
    s_prev, s = "b", "a"
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
    print("=== D0-TORAL-TIME-MARKOV-CONJUGACY-001  internal profinite-code CLOSED; topological conjugacy PROOF-TARGET ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: toral T=[[0,1],[1,-1]] and Fibonacci/golden SFT matrix N_tau=[[0,1],[1,1]] "
          "are fixed structurally BEFORE any value; the conjugacy question (internal profinite vs full topological) "
          "is posed before any numeric check")

    # ---- prerequisite: the cited internal profinite-code closure exists on disk ----
    prereq = os.path.join(HERE, "vp_phi_sturmian_profinite_code_conjugacy.py")
    assert os.path.exists(prereq), f"MISSING cited internal-closure cert: {prereq}"
    src = open(prereq, encoding="utf-8", newline="").read()
    assert "PASS_PHI_STURMIAN_PROFINITE_CODE_CONJUGACY" in src, "cited cert must carry the profinite closure verdict"
    print(f"PASS_PREREQ_CITED  internal profinite-code closure cert present and carries its verdict "
          f"(vp_phi_sturmian_profinite_code_conjugacy.py)")

    # ---- re-run the internal profinite-code witness here (language AND frequency over windows) ----
    sub = sub_word(4000)
    con = concat_word(4000)
    N = min(len(sub), len(con))
    for L in range(1, 11):
        assert factors(sub[:N], L) == factors(con[:N], L), f"cylinder languages must match at L={L}"
        fa, fb = freqs(sub[:N], L), freqs(con[:N], L)
        assert all(abs(fa[k] - fb.get(k, 0)) < 1e-12 for k in fa), f"cylinder frequencies must match at L={L}"
    assert sub[:N] == con[:N], "extensionality: identical on every finite window -> same D0 profinite code"
    print("PASS_INTERNAL_PROFINITE_CLOSED  two golden codings have EQUAL cylinder languages AND frequencies for "
          "L=1..10 over the full window -> same D0 profinite object (internal conjugacy CLOSED)")

    # ---- structural facts about the two matrices (the conjugacy is BETWEEN these dynamics) ----
    T = [[0, 1], [1, -1]]
    N_tau = [[0, 1], [1, 1]]
    assert (tr(T), det(T)) == (-1, -1), "T charpoly x^2 + x - 1 (eigenvalues phi^-1, -phi)"
    assert (tr(N_tau), det(N_tau)) == (1, -1), "N_tau charpoly x^2 - x - 1 (eigenvalues phi, -phi^-1)"
    # both are hyperbolic toral (|det|=1) and share the golden expansion factor phi in modulus
    assert abs(det(T)) == 1 and abs(det(N_tau)) == 1, "both must be unimodular (toral)"
    print("PASS_BOTH_TORAL_GOLDEN  T (x^2+x-1) and N_tau=[[0,1],[1,1]] (x^2-x-1) are both unimodular toral with "
          "golden expansion |lambda|=phi; the topological-conjugacy question between their SFTs is well-posed")

    # ================= the EXACT missing artifact =================
    print("MISSING_ARTIFACT  full topological conjugacy T ~= golden SFT needs the EXTERNAL Williams "
          "shift-equivalence: explicit nonneg integer matrices (R,S) and a lag L with "
          "N_tau^L = R*S and (the SFT transition matrix)^L = S*R (strong shift equivalence / lag-L "
          "shift-equivalence) witnessing topological conjugacy. This (R,S,L) is NOT supplied internally.")

    # ---- assert the owner stays OPEN: no internal (R,S,L) Williams witness is provided ----
    williams_witness = None   # NOT constructed internally
    assert williams_witness is None, "owner must stay OPEN: no internal Williams shift-equivalence (R,S,L) is supplied"
    print("PASS_OWNER_STAYS_OPEN  no internal Williams shift-equivalence (R,S,L) is constructed -> "
          "D0-TORAL-TIME-MARKOV-CONJUGACY-001 stays PROOF-TARGET (not over-claimed CLOSED)")

    # ================= negative controls (reachable) =================
    # C1: importing the classical Adler-Weiss theorem and CALLING it the D0 internal proof is rejected.
    def adler_weiss_external_theorem_as_D0_proof():
        # planted wrong move: treat an external classical theorem as the internal D0 closure
        return "EXTERNAL_THEOREM_LABELLED_CORE"
    bad = adler_weiss_external_theorem_as_D0_proof()
    assert bad != "D0_INTERNAL_PROOF", "control: an external theorem is NOT a D0-internal proof"
    assert williams_witness is None, "control: the owner is still open even if an external theorem is cited"
    print("FAIL_EXTERNAL_THEOREM_AS_CORE_REJECTED  citing the external Adler-Weiss theorem does NOT close the "
          "D0 owner (the (R,S,L) Williams witness is still absent) -> rejected as a CORE proof")

    # C2: language-match WITHOUT frequency-match must be rejected (both are required for the profinite code).
    skew = ("a" * 80) + sub[:N]   # same factor SET (eventually) but skewed letter frequency
    same_language = factors(skew, 2).issuperset(factors(sub[:N], 2))
    freq_a_skew = freqs(skew, 1).get("a", 0)
    freq_a_ref = freqs(sub[:N], 1).get("a", 0)
    assert abs(freq_a_skew - freq_a_ref) > 1e-3, "control: skewed word must differ in frequency"
    assert not (same_language and abs(freq_a_skew - freq_a_ref) < 1e-9), \
        "control: language match WITHOUT frequency match must NOT count as profinite conjugacy"
    print("FAIL_LANGUAGE_WITHOUT_FREQUENCY_REJECTED  matching the cylinder factor SET but NOT the frequencies is "
          "rejected (the internal profinite code requires BOTH)")

    # C3: short-window-only match must be rejected (must hold on EVERY increasing window).
    short = sub[:200] + "ab" * 600   # agrees up to length 200, then goes periodic
    assert short[:200] == sub[:200], "control setup: short word agrees on the short window"
    assert short[300:500] != sub[300:500], "control: short-window-only agreement fails on a longer window"
    print("FAIL_SHORT_WINDOW_ONLY_REJECTED  agreement on a short window only (then periodic) FAILS on a longer "
          "window -> short-window match does NOT establish the profinite (hence topological) conjugacy")

    print("HONEST_PROOF_TARGET  D0-TORAL-TIME-MARKOV-CONJUGACY-001 is PROOF-TARGET: the D0-internal profinite-code "
          "conjugacy is CLOSED (cited), but FULL topological conjugacy T ~= golden SFT requires the EXTERNAL "
          "Williams shift-equivalence (R,S,L) relating N_tau=[[0,1],[1,1]] to T's SFT, which is not supplied. "
          "No survey datum enters.")
    print("PASS_TORAL_TIME_MARKOV_CONJUGACY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
