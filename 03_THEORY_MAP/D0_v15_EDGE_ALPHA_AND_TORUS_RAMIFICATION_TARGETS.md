# D0 v15 Edge Alpha and Torus Ramification Targets

## Title
Theorem targets for edge-sector electromagnetic normalization and lepton ramification indices

## 1. Status
These remain **theorem targets**, not closed proofs or CORE-CLOSED claims.

- EDGE-TRACE-COEFFICIENT-TARGET (open target)
- TORUS-RAMIFICATION-TARGET (open target)

External QED / lepton mass comparisons remain passport layers.

## 2. Edge-Sector Electromagnetic Normalization Target

On the 1-skeleton of the shell torus K(9,11,13) the coefficient-origin trace is reduced to an edge-sector invariant:

Target form (guardrail):

Tr(F_E) ~ phi^{-2} * 359 - phi^{-5}  (with seam corrections)

## 3. Lepton Ramification Indices Target

Charged-lepton hierarchy is expressed as branch indices of the finite Green function over the shell torus (Puiseux exponents).

Target indices (guardrail):

p_mu = 1/4 , p_tau = 1/3

## 4. Guardrails / Negative Controls

- PASS_EDGE_ALPHA_TRACE_TARGET_DECLARED
- PASS_EDGE_SECTOR_359_CHANNELS_DECLARED
- PASS_PHI_MINUS_FIVE_SEAM_CORRECTION_DECLARED
- PASS_NO_ALPHA_NUMEROLOGY_CLAIM
- PASS_TORUS_RAMIFICATION_TARGET_DECLARED
- PASS_PUISEUX_INDEX_REQUIREMENT_DECLARED
- PASS_NO_LEPTON_FRACTION_FIT_CLAIM

No claim is made that these targets are proved or that they reproduce PDG numbers inside the finite theory. They are synthesis targets for subsequent layers.

## 5. Cert Skeletons
See the lightweight target certs:

- 05_CERTS/vp_edge_sector_alpha_trace_target.py
- 05_CERTS/vp_torus_ramification_indices_target.py

These print the declared target/guardrail tokens above and explicitly reject numerology or fit claims.

## 6. Relation to Grand Synthesis
These targets appear in the Grand Synthesis as open items under "edge-sector alpha" and "mass hierarchy as ramification". They are not part of the closed sector-law core.

## 7. Book Patch Requirements
- Book 04: list as theorem targets (not closure).
- Book 05: register the two TARGET closure classes (not CERT-CLOSED).
- No overclaim in publication documents.
