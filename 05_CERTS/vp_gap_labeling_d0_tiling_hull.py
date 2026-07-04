#!/usr/bin/env python3
"""D0 gap labeling certificate — REAL-SPECTRUM EDITION.

[2026-07-04 RETIREMENT of the fabricated-IDS placeholder] The previous body of this file
computed a spectrum but then FABRICATED the IDS as (idx+1)/30 with a float (n,m) fit at
tolerance 0.05 (the flag on D0-KTHEORY-001 records this). This edition keeps the filename,
STATUS string and d0_gap_labels.json output contract (same keys) so all existing references
stay valid, but every number is now real:

  - operator: periodic Fibonacci-word tridiagonal H at |w| = F_16 = 987 (lambda = 1);
  - IDS at a gap = k/987 with k the exact eigenvalue count below the gap (REAL, not idx/30);
  - label: the exact congruence k = m * 610 (mod 987) (610/987 = approximant slope) and the
    module element n + m*phi^-1 in [0,1) with REAL tolerance 2/987 (was 0.05);
  - failure is possible: any dominant gap without a small-|m| label fails the cert.

Full owner-edge cert (saturation at two couplings, silver/Pell double control, T=A^-1,
Fricke-Vogt): 05_CERTS/vp_fibonacci_gap_labeling_owner_edge.py (D0-GAP-LABELING-OWNER-EDGE-001).
"""

import json
import numpy as np
from pathlib import Path

STATUS = "PASS_D0_GAP_LABELING_TILING_HULL"
PHI_INV = (5**0.5 - 1) / 2


def fibonacci_word(n_target: int) -> str:
    w = "a"
    while len(w) < n_target:
        w = "".join({"a": "ab", "b": "a"}[c] for c in w)
    return w[:n_target]


def run_certificate() -> None:
    print("--- D0 GAP LABELING TILING HULL CERTIFICATE (real-spectrum edition) ---")

    # 1. Real finite approximant: periodic Fibonacci tridiagonal, |w| = F_16 = 987
    N, SLOPE_NUM = 987, 610          # F_16, F_15
    word = fibonacci_word(N)
    assert word.count("a") == SLOPE_NUM
    lam = 1.0
    v = np.array([lam if c == "b" else 0.0 for c in word])
    H = np.diag(v) + np.diag(np.ones(N - 1), 1) + np.diag(np.ones(N - 1), -1)
    H[0, -1] = H[-1, 0] = 1.0        # periodic BC: no edge states inside gaps
    evals = np.linalg.eigvalsh(H)
    print(f"    Computed real spectrum of the F_16={N} Fibonacci approximant: PASS")

    # 2. Dominant gaps by rank (top 25 widest)
    spacings = np.diff(evals)
    top = sorted(int(i) + 1 for i in np.argsort(spacings)[::-1][:25])   # k = states below gap
    print(f"    Selected top {len(top)} widest gaps: PASS")

    # 3. Exact labels: the SAME m must both satisfy the congruence k = m*610 mod 987 AND land
    #    within tolerance of the golden fraction n + m*phi^-1 (single witness, not two tracks).
    labels = []
    failures = 0
    for idx, k in enumerate(top):
        ids = k / N
        m_int = None
        for m in range(-34, 35):
            if (m * SLOPE_NUM - k) % N == 0 and (m_int is None or abs(m) < abs(m_int)):
                m_int = m
        if m_int is None:
            ok, m_mod, n_mod, dist = False, 0, 0, float("inf")
        else:
            m_mod = m_int
            n_mod = round(ids - m_mod * PHI_INV)
            dist = abs(ids - (n_mod + m_mod * PHI_INV))
            ok = dist < 2.0 / N
        failures += 0 if ok else 1
        labels.append({
            "gap_idx": idx,
            "lower_bound": round(float(evals[k - 1]), 4),
            "upper_bound": round(float(evals[k]), 4),
            "ids": round(ids, 6),
            "k0_label": {"n": int(n_mod), "m": int(m_mod)},
            "trace_val": round(n_mod + m_mod * PHI_INV, 6),
        })
    assert failures == 0, f"{failures} dominant gaps failed exact golden labeling"
    worst = max(abs(l["ids"] - l["trace_val"]) for l in labels)
    print(f"    Exact K0 labels on all {len(labels)} gaps, worst |IDS - (n+m*phi^-1)| = {worst:.2e} (tol {2/N:.2e}): PASS")

    # 4. Save d0_gap_labels.json (same contract as before, real content)
    Path("d0_gap_labels.json").write_text(json.dumps(labels, indent=2), encoding="utf-8")
    print("    Saved d0_gap_labels.json: PASS")

    print(f"\n[CERT-CLOSED] {STATUS}")


if __name__ == "__main__":
    run_certificate()
