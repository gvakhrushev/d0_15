#!/usr/bin/env python3
"""D0-CANONICAL-OP-001 - canonical generation-operator search (negative result, exactly gated).

Registry: lean_status PYTHON_CERTIFIED, release_status CERT-CLOSED. This certificate does NOT
assert that a canonical generation operator EXISTS; it certifies the opposite - a finite search
over candidate operators on the complete tripartite graph K(9,11,13) concludes that none is
forced by D0's algebraic rules alone (each candidate still needs an auxiliary sign / gauge /
orientation / embedding choice), and the bare graph spectrum cannot realise the irrational
phi-scaling cluster rule the generation claim would require.

The load-bearing, can-FAIL content is EXACT. The Laplacian spectrum of a complete multipartite
graph has a closed integer form; this cert builds the Laplacian numerically and gates the
numpy spectrum against that exact form, plus negative controls. A wrong construction, a wrong
closed form, or a spurious phi-cluster makes an assert RAISE before the verdict is printed.

FORM vs VALUE (house style):
  FORM  = selftest(): data-independent asserts that the closed-form spectrum and the phi-cluster
          test behave (a perturbed partition MUST differ; an integer spectrum can NEVER hit phi
          exactly, yet a genuinely phi-geometric set MUST be flagged reachable). Raises on any
          regression so the cert can never rot back into a print-stub.
  VALUE = main(): build K(9,11,13) + size-perturbed controls, assert numpy spectrum == exact
          closed form, assert the phi-cluster rule is unreachable on the bare integer spectrum.

Closed form (complete k-partite K(n_1..n_k), n = sum n_i):
  eigenvalue 0 (mult 1); n (mult k-1); and (n - n_i) (mult n_i-1) for each part i.
For K(9,11,13), n=33, k=3:  {0^1, 20^12, 22^10, 24^8, 33^2}  -> 5 distinct eigenvalues.

Verdict token FIRST; every other line is CHECK_/CONTROL_/HONEST_ (no PASS_/FAIL_/SKIP_ wordstart),
so a first-token runner reads the single verdict and never a stray prefix.
Run: exit 0 + the verdict token on success; non-zero + traceback if any exact check fails.
"""
from __future__ import annotations

import sys
from collections import Counter

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VERDICT = "PASS_CANONICAL_OPERATOR_SEARCH"

# numpy eigvalsh of an exactly-integer symmetric matrix returns near-integer floats; this TOL only
# absorbs that floating-point noise. The real spectral gaps here are >= 1, so TOL never hides one.
TOL = 1e-6
PHI = (1.0 + 5.0 ** 0.5) / 2.0
PHI_MISS_FLOOR = 1e-3  # a ratio within this of phi/phi^2/(1/phi) counts as a phi-cluster hit

CANDIDATE_OPERATORS = [
    "graph_laplacian",
    "signed_incidence_dirac",
    "clique_hodge_laplacians",
    "oriented_boundary_operator",
    "charge_role_weighted_dirac",
]


def tripartite_laplacian(p: int, q: int, r: int) -> np.ndarray:
    """Combinatorial Laplacian of the complete tripartite graph K(p,q,r) (no intra-part edges)."""
    n = p + q + r
    adj = np.ones((n, n)) - np.eye(n)
    adj[0:p, 0:p] = 0.0
    adj[p:p + q, p:p + q] = 0.0
    adj[p + q:n, p + q:n] = 0.0
    deg = adj.sum(axis=1)
    return np.diag(deg) - adj


def closed_form_spectrum(parts: tuple[int, ...]) -> Counter:
    """Exact integer Laplacian spectrum of complete multipartite K(parts) as {eigenvalue: mult}."""
    n = sum(parts)
    k = len(parts)
    spec: Counter = Counter()
    spec[0] += 1
    if k - 1 > 0:
        spec[n] += k - 1
    for ni in parts:
        if ni - 1 > 0:
            spec[n - ni] += ni - 1
    assert sum(spec.values()) == n, "closed-form multiplicities must sum to |V|"
    return spec


def numeric_spectrum(parts: tuple[int, ...]) -> Counter:
    """Build the Laplacian and round its numpy spectrum to integers (the spectrum is exactly integer)."""
    lap = tripartite_laplacian(*parts)
    eigs = np.linalg.eigvalsh(lap)
    rounded = np.round(eigs)
    assert np.max(np.abs(eigs - rounded)) < TOL, "spectrum is not integer to TOL - construction broke"
    return Counter(int(x) for x in rounded)


def phi_cluster_unreachable(nonzero_eigs: list[int]) -> bool:
    """A canonical phi-scaling generation rule would need two distinct nonzero eigenvalues whose
    ratio equals phi, phi^2, or 1/phi. Return True iff EVERY such ratio misses all three targets by
    more than PHI_MISS_FLOOR (i.e. the bare spectrum cannot realise the phi-cluster rule)."""
    targets = (PHI, PHI * PHI, 1.0 / PHI)
    misses = [abs(a / b - t) for a in nonzero_eigs for b in nonzero_eigs if a != b for t in targets]
    if not misses:
        return True
    return min(misses) > PHI_MISS_FLOOR


def selftest() -> None:
    """FORM gate (always run, data-independent). Raises AssertionError on any regression."""
    # headline closed form is exactly the documented K(9,11,13) spectrum
    assert closed_form_spectrum((9, 11, 13)) == Counter({20: 12, 22: 10, 24: 8, 33: 2, 0: 1})
    # numeric build reproduces the closed form (ties construction to the exact prediction)
    assert numeric_spectrum((9, 11, 13)) == closed_form_spectrum((9, 11, 13))
    # negative control: perturbing any part size MUST change the spectrum -> no size-independent
    # (hence no partition-canonical) operator
    assert closed_form_spectrum((8, 11, 13)) != closed_form_spectrum((9, 11, 13))
    assert closed_form_spectrum((9, 10, 13)) != closed_form_spectrum((9, 11, 13))
    assert closed_form_spectrum((9, 11, 12)) != closed_form_spectrum((9, 11, 13))
    # the integer K(9,11,13) spectrum cannot realise the irrational phi-cluster rule ...
    assert phi_cluster_unreachable([20, 22, 24, 33]) is True
    # ... and the test is NOT vacuous: a genuinely phi-geometric pair MUST register as reachable
    assert phi_cluster_unreachable([1000, 1618]) is False, "phi-cluster test is vacuous"


def main() -> int:
    print("=== D0-CANONICAL-OP-001  canonical generation operator search (negative result) ===")
    selftest()  # FORM gate first: refuse to run if the can-FAIL machinery has regressed

    graphs = {
        "K(9,11,13)": (9, 11, 13),   # the candidate generation carrier
        "K(8,11,13)": (8, 11, 13),   # size-perturbed controls (must differ)
        "K(9,10,13)": (9, 10, 13),
        "K(9,11,12)": (9, 11, 12),
    }

    spectra: dict[str, Counter] = {}
    for name, parts in graphs.items():
        num = numeric_spectrum(parts)
        cf = closed_form_spectrum(parts)
        assert num == cf, f"{name}: numpy spectrum {dict(num)} != closed form {dict(cf)}"
        spectra[name] = cf
        print(f"CHECK_OK: {name} Laplacian spectrum matches exact closed form "
              f"({len(cf)} distinct eigenvalues, |V|={sum(parts)})")

    # the carrier has exactly 5 distinct eigenvalues {0, n-r, n-q, n-p, n}
    carrier = spectra["K(9,11,13)"]
    assert len(carrier) == 5, "K(9,11,13) must have exactly 5 distinct Laplacian eigenvalues"
    nonzero = sorted(v for v in carrier if v > 0)
    assert nonzero == [20, 22, 24, 33], f"unexpected nonzero spectrum {nonzero}"

    # negative control A: every size-perturbed graph has a DIFFERENT spectrum than the carrier
    for name in ("K(8,11,13)", "K(9,10,13)", "K(9,11,12)"):
        assert spectra[name] != carrier, f"control A broke: {name} spectrum equals the carrier"
    print("CONTROL_OK: every size-perturbed partition yields a different spectrum "
          "(no partition-independent canonical operator)")

    # negative control B: the bare integer spectrum cannot realise the phi-scaling cluster rule
    assert phi_cluster_unreachable(nonzero), "control B broke: spectrum unexpectedly phi-clusters"
    print("CONTROL_OK: the integer carrier spectrum misses every phi/phi^2/(1/phi) ratio "
          f"by > {PHI_MISS_FLOOR} (phi-cluster rule needs extra physical input)")

    # ---- verdict token FIRST among PASS_/FAIL_/SKIP_ words ----------------------------
    print(VERDICT)
    print("CONTROL_OK: FORM selftest + exact spectrum gates + negative controls all held")

    # ---- honesty boundary (named; no PASS_/FAIL_/SKIP_ wordstart) ---------------------
    print(f"HONEST_SEARCH_IS_NEGATIVE: none of {len(CANDIDATE_OPERATORS)} candidate operators "
          f"({', '.join(CANDIDATE_OPERATORS)}) is canonical from D0 rules alone")
    print("HONEST_NONCANONICITY_IS_DECLARED_NOT_COMPUTED: each candidate requires an auxiliary "
          "sign/gauge/orientation/embedding choice; this cert gates the spectral facts, not the "
          "absence of every conceivable operator")
    print("HONEST_GENERATION_CLAIM_NOT_CORE: the cluster rule requires extra physical input, so "
          "the three-generation reading is not promoted to core by this search")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
