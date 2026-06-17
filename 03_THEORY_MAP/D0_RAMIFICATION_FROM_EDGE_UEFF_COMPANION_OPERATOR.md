# D0 Ramification from Edge UEFF Companion Operator

## Statuses (hardened)

- EDGE-ALPHA-TRACE-CERT-CLOSED (explicit unitary dilation + seam in vp_edge_alpha_trace_constructive.py)
- RAMIFICATION-COMPANION-COVER-CERT-CLOSED (SymPy-exact C4/R3 blocks + det factorization in vp_ramification_edge_ueff_companion.py)
- RAMIFICATION-FROM-PHYSICAL-EDGE-UEFF-THEOREM-TARGET (stronger derivation from physical edge U_eff remains target)

## Companion Cover Construction

The companion cover is a finite spectral-cover extension attached to the edge resolvent.

Explicit blocks (from SymPy construction):

- C4: 4-cycle terminal capacity operator block (characteristic x^4 - λ)
- R3: 3-cycle scene-rank holonomy block (x^3 - λ)

These encode terminal role capacity and scene-rank holonomy sheets.

**Important clarification (per integration):**

The companion cover is a finite spectral-cover extension attached to the edge resolvent. It is not a claim that the 359-edge Hilbert space itself has dimension 359+4+3. The 4-cycle and 3-cycle blocks encode terminal role capacity and scene-rank holonomy sheets.

The physical edge dimension remains 359; the companion blocks are auxiliary for the ramification cover attached to the resolvent.

## Negative Controls

Diagonal holonomy (λ placed on diagonal instead of return edge) shifts the pole but does not create an m-sheet branch (verified in cert).

## Cert Support

See vp_edge_alpha_trace_constructive.py and vp_ramification_edge_ueff_companion.py (the latter uses SymPy for exact polynomials/dets).

## Book Relation

See Book 04 patch for the clarification on companion vs physical edge.

(Integrated with full executable evidence from the certs; statuses reflect that.)
