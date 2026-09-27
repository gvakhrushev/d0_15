# WRK-A4D-SCHUR-EINSTEIN-DIRECT-IDENTIFICATION

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-schur-einstein-direct-identification`  
Primary artifact: `02_REGISTRY/research/A4D_SCHUR_EINSTEIN_DIRECT_IDENTIFICATION.md`  
Execution: `GitHub-first`

## Dependency

Consume the merged exact owner `A4D_METRIC_NULL_HESSIAN_COMPLEX.md` from PR #270. Do not rebuild a second owner for its null-line theorem.

## Objective

Independently identify the leading metric Schur complement of the accepted finite star joint symbol with the standard flat linearized Einstein operator.

The identification must not use `E_eta` as the final comparison object. Reconstruct the textbook tensor symbol directly on the repository's ten symmetric metric coordinates and compare coefficient-by-coefficient.

## Required gates

1. Rebuild the trivial-character connection block `A0=H_AA(1)` and the first character derivative `C1(k)` from the accepted polarized owner.
2. Form the leading eliminated metric symbol
   \[
   K_{\rm Schur}(k)=-C_1(k)^T A_0^{-1} C_1(k).
   \]
3. Independently construct the standard flat linearized Einstein tensor \(G^{(1)}_{\mu\nu}(h;k)\) for Minkowski \(\eta\), with the repository's input/output index and ten-coordinate conventions made explicit.
4. Prove or refute the exact polynomial identity
   \[
   K_{\rm Schur}(k)=-\frac12\,K_{G^{(1)}}(k).
   \]
5. Hostile convention controls:
   - lower-vs-raised Einstein output;
   - factor two on off-diagonal symmetric metric coordinates;
   - overall Schur sign.
   A convention mismatch must fail explicitly rather than be absorbed by renaming.
6. Prove the generic rank and gauge kernel:
   - \(\operatorname{rank}K_{\rm Schur}=6\) over the generic momentum field;
   - the four-dimensional leading forward-coframe metric image lies in its kernel;
   - use dimensions to identify equality of the generic kernel and coframe image.
7. Prove the linearized Bianchi identity directly in the same coordinate convention.
8. Record characteristic hostile controls, including a null covector where the rank drops to the owned characteristic value.
9. State the exact relation to #270/#201: this is an independent standard-Einstein cross-check, not a replacement owner and not a nonlinear continuum theorem.

## Preferred terminal

`J2-SCHUR-DIRECT-LINEAR-EINSTEIN-IDENTIFICATION-EXACT`

A negative terminal must identify the first convention-independent coefficient mismatch.

## Forbidden

No nonlinear Einstein claim, no finite diffeomorphism-gauge promotion, no new action term, no \(\varphi\), no observational claim, and no circular use of `E_eta=-2G` as the proof of the requested equality.

## GitHub execution contract

Open the Draft PR before substantive science commits. Produce an exact certificate under `02_REGISTRY/research/certificates/`. Self-retire only at an exact terminal and do not self-merge.

## Chat handoff

Return PR, head SHA, exact terminal, the direct Schur-vs-standard-Einstein identity, the Bianchi check, generic/null rank data, the four-dimensional gauge-kernel comparison, and the exact certificate command.
