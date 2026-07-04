# SEAM LOCATION THEOREM — the α-realization cannot live on the vertex algebra (VERIFIED DRAFT)

**Status:** candidate theorem, machine-verified (`seam_location_check.py`, 5/5 PASS, reachable
negative control); registry grep clean (no owned row states this). Pre-skeptic self-audit applied:
objects built independently, check can fail (control), no conclusion inserted. No registry edit.

## Statement

For the owned active(rank-3)/archive(dim-30) split of the α-chain (`AlphaFeshbachDixmierOwner.lean`:
kernel structure 8⊕10⊕12; archive fingerprint {24×8, 22×10, 20×12} — ROOT R2's owned spectrum):

**Every operator in the scene vertex algebra ⟨A, D_deg⟩ preserves the split.** Proof in two lines:
A annihilates the kernel (zone-wise sum-zero vectors); D_deg is zone-scalar and preserves them;
hence every word maps kernel → kernel (verified for all words of length ≤ 4, and the closure is
algebraic: the generators do, so the algebra does). Consequently the Feshbach off-diagonal blocks
vanish identically — **B = C = 0 for any W_eff built from the vertex algebra** — and the depth-2
moment μ₂u² + μ₁u with μ₂, μ₁ ≠ 0 is **unrealizable at the vertex level**.

## Why this is progress on the last external edge (not a defeat)

The missing artifact of the C1-α triple ("Res_D0(W_eff) = Δα via the 2¹¹ active–archive pairing")
has been searched for, implicitly, at the wrong address: the Lean owner carries the split's
*dimensions* (3, 30) with no concrete blocks, and this theorem shows no concrete vertex-level
blocks can exist. The seam's operator home is therefore forced to a **carrier extension**, and the
owned candidates are exactly the objects the blocker's own wording names:

- the **359-edge carrier** — where the unified chain's contact machinery lives, where active↔bulk
  coupling is nontrivial (rank K = 7, cert-verified), and where a single-edge operator already
  produces a nonzero seam (this check's negative control);
- the **V₁₁ Fock capacity 2¹¹** — an edge/mode-side object with no vertex-level meaning, which is
  precisely why it appears in the pairing and cannot be derived from the vertex split.

The "external" status of the Dixmier edge thus acquires a structural explanation: the vertex
algebra is seam-free, so any realization must import the edge/Fock extension — and the pairing's
2¹¹ is the fingerprint of that import. The next construction site is precise: build W_eff on the
edge carrier (P_term/Q_bulk split of the unified chain), compute its depth-2 archive moment
exactly, and compare with μ₂ = 12288/5, μ₁ = 1/3. Landing = the realization derived; mismatch =
an exact witness that the external assumption is irreducible. Either outcome closes the question's
location for good.

## Honest scope

This does not close any blocker; it relocates the search space by exclusion, with proof. The edge-
level computation is the genuinely hard remaining step (the Q_bulk resolvent is 351-dim and the
depth-grading u = φ⁻³ must be typed from owned tick data, not chosen). Obligations: skeptic pass;
the word-closure argument should be stated algebraically in the minted version (generators
preserve ⇒ algebra preserves), with the length-≤4 sweep as its finite witness.
