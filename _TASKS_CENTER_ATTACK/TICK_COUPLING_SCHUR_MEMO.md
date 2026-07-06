# TICK-COUPLING-SCHUR — the Feshbach tick never fires on equivariant carriers; typed (unitary) carriers make the residual false-and-vacuous; a nilpotent tri-phase unitary is the typed firing candidate (DRAFT v2, post-skeptic-#1 repairs)

**Status:** DRAFT candidate; no registry row edited, no cert minted. Skeptic #1 verdict: NO KILL,
two FORCED repairs — both applied in full below (repair log at end). Pre-flight cross-refs now
include R1 and row 336 (missed in v1 — error of record).

## Claim (DEF-0.2.2 form)

Frozen scene K(9,11,13); frozen Feshbach split P = proj(range A_scene) (rank 3),
Q = proj(ker A_scene) (dim 30).

**(A) Coupling vacuity on the equivariant class — an R1-COROLLARY, not a fresh theorem.**
The corpus already owns the module structure: `05_CERTS/vp_root_r1_representation_reconstruction.py:2`
("Aut(K(9,11,13))=S9xS11xS13 perm rep on C^33: isotypes 3 trivial + std9/11/13 (8,10,12); commutant
dim=3^2+1+1+1=12") and `04_VERIFICATION/POST_CORE_NOGO_SCOPE_REPAIR.csv:3` ("commutant dim 12,
GL(3) freedom on the rank-3 trivial isotype"; owner row
D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001). COROLLARY (the NEW content = the tick-ladder
consequence): since the commutant is GL(3)⊕C⊕C⊕C with no trivial↔std cross-blocks, EVERY
Aut-equivariant U (directed or not) has P U Q = Q U P = 0; hence every Neumann delay term
P U Q (QUQ)^k Q U P is identically zero, W_eff = P U P, and the tick spine's named residual
rho(QUQ) < 1 is VACUOUS on the whole equivariant class. Directedness alone (zone-cyclic A_dir,
inside the commutant) does not fire the tick.

**(A') Typed sharpening (skeptic #1's construction, adopted with credit).** The tick owners' own
book section types the slot: BOOK_06 §06.8.F ("The global state of the finite holographic carrier
is static under the unitary U_N", BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md:425). On the
equivariant ∩ unitary class, U preserves ker A and U|ker is unitary, so rho(QUQ) = 1 exactly while
the coupling is 0: the residual is SIMULTANEOUSLY FALSE AND VACUOUS there. Convergence was never
the operative gap; symmetry breaking is.

**(B) Witnesses that the completion class is nonempty.**
- *Untyped (demoted per pre-registered S1, executed):* any rank-one vertex selector Pi_v fires and
  converges — for a vertex in the zone of size n: rho(Q Pi_v Q) = (n-1)/n < 1,
  ||P Pi_v Q||^2 = (n-1)/n^2, all exact in Q, no rescale. GENERIC in the vertex: the v1 claim that
  the T2 pedigree of omega0 selects the witness was an over-sell (error of record) — any vertex in
  any zone works (8/9; 10/11; 12/13). Pi_v is NOT unitary, so this leg shows nonemptiness only in
  the UNTYPED sense.
- *Typed candidate (new in v2, numerically verified, pre-minting):* the tri-phase diagonal unitary
  U3 = diag(mu9; mu11; mu13) (per-zone phase lattices of order = zone size) is UNITARY, breaks all
  three within-zone symmetries, and satisfies: (QUQ)^12 = 0 EXACTLY (nilpotent; true rho = 0), so
  the Neumann ladder is a FINITE SUM — no convergence hypothesis at all; ||P U3 Q||_F = sqrt(3) != 0
  and ladder-sum ||.||_F = sqrt(3) (FROBENIUS norms; both OPERATOR norms are exactly 1 — skeptic #2).
  Nilpotency index exactly 12 (||(QUQ)^11|| = 1). The tick fires with finite archive-circulation
  depth < 12; robust under within-zone phase permutation; destroyed by a single repeated phase
  (the full phase lattice is exactly load-bearing).
  Echoes the owned nilpotent seam-transport theme (N^2=0; here index <= 12).

**Consequence (carrier-selection reframing, candidate).** Block-II's residual is not convergence
but CARRIER SELECTION: on equivariant carriers the tick cannot fire (A, A'); it fires on
within-zone symmetry-broken carriers, and in the typed (unitary) class at least one candidate
(U3) fires with a nilpotent — hence convergence-free — ladder. Selection of THE canonical U is NOT
made here (selection ≠ forcing); the completion object is a within-zone symmetry-breaking UNITARY
with an ownership pedigree, which is exactly the shape of the known representation-selection
frontier (R1).

## Reconciliation with D0-HORIZON-FESHBACH-RADIATION-OWNER-001 (row 336, CERT-CLOSED "coupling exists (B != 0)")

Named by skeptic #1 as an unswept opposite-polarity row. Its cert plants a 3x3 free-rational toy
corner for B — it owns the radiation-channel SHAPE, not an equivariant scene-derived B. (A) says:
if the physical U is equivariant, row 336's channel is empty; a physical radiation channel
therefore ALSO requires a symmetry-broken carrier. The two rows are consistent exactly on the
symmetry-broken class; neither yields — but row 336's mechanism inherits the same completion
object (this memo makes that dependency explicit for the first time).

## Relation to D0-ARCHIVE-CONTRACTION-NOGO-001 (v1 wording repaired)

The legs are INCOMPARABLE (v1's "strictly weaker" was an overreach — error of record): R2 kills
U = L_scene by radius and owns the S_DE/w-underdetermination leg, which (A) does not touch; (A)
adds the coupling leg R2's Lean does not contain (verified: ArchiveContractionCriterion.lean has
no coupling statement). Both respect R2's SCOPE-REPAIR ("does NOT prove QUQ is non-contractive").

## Owned pre-facts (verbatim; all six v1 quotes verified verbatim by skeptic #1; two added)

1-6. As v1 (tick-owner scopes; R2 scope-repair; guard cert; T2 P1; Lean HONESTY BOUNDARY).
7. `05_CERTS/vp_root_r1_representation_reconstruction.py:2` (quoted in (A) above).
8. BOOK_06 §06.8.F unitary/staticity clause (quoted in (A') above).

## Verification

`_TASKS_CENTER_ATTACK/tick_coupling_schur_check.py` v2: adds (i) span-completeness control — the
equivariant sample provably covers all 12 commutant dimensions (skeptic: v1 could have passed on a
proper subspace); (ii) computed (not print-only) vacuity check — max delay-term norm over the
class; (iii) U3 nilpotency + unitarity + firing, exact; (iv) honest control descriptions (v1
control-1 description over-sold — error of record). Negative controls can fail the CONCLUSION.

## Named risks & PRE-REGISTERED attack surface (v2)

- **S1' (strongest): the staticity clause.** BOOK_06 §06.8.F also says the global state is STATIC
  under U_N. If "static" means U_N fixes the carrier STATE VECTOR, U3 fails it
  (||U3 u - u|| = sqrt(2) on the uniform vector); if it means the maximally-mixed global DENSITY
  is preserved, every unitary passes. The reading is NOT resolved here; U3 is a candidate, not a
  typed theorem, until the clause's binding force is adjudicated.
- **S2 (unchanged): phase-lattice operator ownership.** mu_n-as-diagonal-operator is not a
  greppable owned object; U3's pedigree is the same gap v1 pre-registered for Phi9.
- **S3 (narrowed): non-equivariant, non-unitary U built without external catalog** — not covered
  by (A) or (A'); the carrier-selection frame absorbs, does not refute, such candidates.
- **S4: does book-prose typing BIND the Lean-untyped slot?** The Lean owner leaves U untyped;
  §06.8.F types it in prose. This memo takes the conservative branch (prose binds ⇒ (B) untyped
  leg demoted). The liberal branch (prose does not bind) would re-promote Pi_v; adjudication
  belongs to the closure contract, not to this memo.

## What this does NOT show

- Does NOT select the canonical tick carrier (selection ≠ forcing).
- Does NOT edit or demote any CERT-CLOSED row; no live contradiction exists (v1 finding, upheld).
- Does NOT prove U3 is admissible under the staticity clause (S1') nor owned (S2).
- (A) is an owned-content corollary — its registry value is the tick-ladder consequence and the
  row-336 dependency, not the module decomposition (which is R1's).

## Repair log (skeptic #1, all accepted, no defense)

R-1: novelty preamble named the wrong closest row; R1 owns the proof engine → (A) re-scoped as
corollary, R1 + row 336 added to cross-refs. R-2: S1 demotion executed against BOOK_06 §06.8.F;
(B) split into untyped/typed legs; skeptic's rho=1-and-coupling-0 sharpening adopted as (A').
R-3: omega0-pedigree over-sell removed (any-vertex genericity stated). R-4: "strictly weaker"
→ incomparable. R-5: script controls repaired + span-completeness added + vacuity made computed.

Skeptic #2 (focused re-pass on v2 new text): NO KILL on all five items; (A') and row-336
reconciliation SURVIVE clean; U3 nilpotency verified EXACT at 60-digit precision (DFT ⇒ truncated
cyclic shift Jordan blocks, index exactly 12), permutation-robust, single-repeated-phase boundary
probe destroys it (full lattice load-bearing). Two forced repairs applied: R-6 verbatim-quote
misprint std9/11/12 → std9/11/13 (memo §(A)); R-7 U3 norms labelled Frobenius (operator norms = 1)
+ ladder-sum flagged as memo-level pending script addition. Residual known limitation: script's
ladder-sum value not yet computed in-script (skeptic verified independently, Frobenius
1.732050807569).
