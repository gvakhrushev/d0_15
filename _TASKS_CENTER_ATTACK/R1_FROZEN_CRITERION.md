# R1 — frozen criterion (pre-registered BEFORE data contact)

**Committed before any read of `d0_gap_labels.json` values.** Schema knowledge only (from
`05_CERTS/vp_gap_label_genericity_nogo.py`): 25 plateaux, each with IDS value in [0,1] and
integer label `(n, m)`, IDS ≡ (n + m/φ) mod 1. The rewind question (matrix R1): does the
move-5 dataset (gap labels) carry the move-4 closure structure (the terminal-count shape:
two interior elements generate the forced third)?

## R1a (primary): three-gap closure shape on the SPARSE plateau set

Sort the 25 IDS values; form the 24 circular gaps (mod 1). PASS-a iff BOTH:
1. the gap multiset takes EXACTLY 3 distinct values {S₁ < S₂ < L} at tolerance
   `tol = 1e-9` (labels are exact integers, so gaps are exact in ℤ + ℤ/φ — compare gaps by
   their exact (n, m) differences, not floats, whenever labels permit);
2. `L = S₁ + S₂` exactly in the module (the closure shape: the two interior lengths
   generate the third — the same 2-generate-the-3rd shape as
   `D0-CASCADE-TERMINAL-COUNT-001`).

Why non-trivial: the three-distance theorem guarantees this for {kα mod 1, k ≤ N}
(consecutive orbits), NOT for a sparse 25-element subset of the module ℤ + ℤ/φ chosen by
physics (gap-opening). For a sparse subset the generic outcome is MANY distinct gap values.

**Null control N-a (must fire):** 10 000 random 25-element label sets, (n, m) drawn
uniformly from the data's own (n, m) bounding box, distinct IDS required, seed = 20260814.
Record the fraction of null sets passing R1a. The control FIRES iff that fraction < 0.01.
If the control does not fire, R1a is uninformative regardless of the data outcome, and this
is recorded as CONTROL-FAIL (not PASS, not FAIL).

## R1b (secondary): exact reflection triples in adjacency

Adjacency = consecutive in sorted IDS. A reflection triple at position i:
`n_{i+1} = 2n_i − n_{i−1}` AND `m_{i+1} = 2m_i − m_{i−1}` (exact integer arithmetic — the
label-module analogue of the shell reflection `x ↦ 2R − x`). Count T = number of reflection
triples among the 23 interior consecutive triples. PASS-b iff T strictly exceeds the 99th
percentile of the null distribution (same null as N-a, same seed).

## Adjudication (frozen)

- R1a PASS + control fires → the closure shape is PRESENT in the move-5 data (retrodiction
  holds); campaign proceeds to memo → skeptic → mint as a rewind result.
- R1a FAIL (control fires) → retrodiction FAILS on this dataset; recorded as a negative
  with the same prominence (the matrix cell gets the FAIL grade).
- CONTROL-FAIL → criterion void; a new criterion may be frozen only in a NEW file, this one
  stays as the record.
- R1b is secondary either way: reported, never promoted to headline on its own.
- N6's cap stands in every branch: this is retrodiction inside D0's own program, NOT an
  experimental discriminator between D0 and generic Fibonacci hulls.

Freeze date: 2026-08-14. Data file untouched at freeze time.
