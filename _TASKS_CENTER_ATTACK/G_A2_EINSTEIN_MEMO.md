# G_A2 finite Einstein tensor: BUILD-or-OBSTRUCT memo (DRAFT, center-attack)

**Claim-ID:** D0-SPECTRAL-EINSTEIN-001 (jointly D0-HODGE-LINKS-001)
**Date:** 2026-07-05 · **Status of this memo:** DRAFT / candidate — pre-skeptic
**Outcome (candidate):** OBSTRUCTION PROVED — the a2/EH-proxy variational Einstein
tensor `G_A2 = dS_A2/dh` is NOT archiveDivergence-free on the frozen scene K(9,11,13).
**Deliverables:** `g_a2_einstein_check.py` (exact-ℚ, can-fail) + this memo.

---

## 0. DEF-0.2.2 claim under test

> On the frozen scene K(9,11,13), lift the heat-trace a₂ coefficient S_A2 onto a
> symmetric metric-perturbation field h, define the rank-2 tensor
> `G_A2^{ij} := ∂S_A2/∂h_ij`, and test whether it is simultaneously (i) SYMMETRIC and
> (ii) discrete-contracted-Bianchi / divergence-free, `∂_i G_A2^{ij} = 0`, as an EXACT
> ℚ computation. BUILD if it holds; PROVE THE OBSTRUCTION if it fails.

This is the load-bearing finite→GR cement link. The registry currently marks it
CERT-CLOSED, but (per the row-175 note) the genuine rank-2 tensor does not exist and the
cert was a print-only stub; a colliding internal NO-GO says the canonical stress
divergence ≠ 0.

---

## 1. Owned pre-facts (verbatim, file:line)

**F1 — the registry note demands a rank-2 tensor that does not exist.**
`09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv:175` (D0-SPECTRAL-EINSTEIN-001), verbatim:
> "What is OPEN here is the rank-2 Einstein tensor G_ij = dS_A2/dh proved simultaneously
> SYMMETRIC and DIVERGENCE-FREE -- that object does NOT exist anywhere in D0/ (no
> G_A2/EinsteinTensor). The block is two-fold: a CARRIER MISMATCH (HeatTraceEHProxy.lean
> over R Matrix N N + W_rho vs FiniteSpin2WaveOperator.lean over Q SymPert4 + pairing4)
> and a MISSING variational-derivative operator (dS_A2/dh as a closed-form matrix on a
> single carrier was never written)."

**F2 — the genuine a₂/EH proxy S_A2 (the object to differentiate).**
`09_LEAN_FORMALIZATION/D0/Geometry/HeatTraceEHProxy.lean:12-13`, verbatim:
> `noncomputable def discreteEHActionProxy {N : Type} [Fintype N] [DecidableEq N] (L : Matrix N N ℝ) (ρ : N → ℝ) : ℝ :=`
> `  ∑ i, ∑ j, if i ≠ j then (L i j)^2 / (ρ i * ρ j) else 0`

and its identification as the a₂ coefficient, `SpectralActionLadder.lean:34-38`, verbatim:
> `theorem spectral_action_a2_is_eh_proxy ... : spectralTracePower L ρ 2 =`
> `  HeatTraceA2Decomposition.diagonalSquareTerm L ρ + 2 * HeatTraceA2Decomposition.discreteEHActionProxy L ρ`

So **S_A2 = 2·(EH-proxy) = 2·Σ_{i≠j} L_ij²/(ρ_i ρ_j)** (up to the diagonal "volume" term,
which is h-independent under an off-diagonal metric perturbation). This is the scalar the
memo differentiates — NOT `Tr(L²)`.

**F3 — the corpus divergence operator (what "∂_i G^{ij}=0" means natively).**
`09_LEAN_FORMALIZATION/D0/Geometry/ArchiveFieldEquation.lean:25-28`, verbatim:
> `def archiveDivergence {n : Nat} (A : Matrix ... ℝ) : archivePhaseIndex n → ℝ :=`
> `  fun i => ∑ j : archivePhaseIndex n, A i j`

The discrete contracted-Bianchi identity is stated against THIS operator,
`ArchiveBianchiIdentity.lean:55-56`, verbatim:
> `theorem curvature_gradient_conserved (n : Nat) :`
> `    archiveDivergence (archiveCurvatureGradient n) = 0`

**F4 — the colliding internal NO-GO (row-sum divergence of a stress is nonzero in general).**
`09_LEAN_FORMALIZATION/D0/Geometry/ArchiveStressRepresentative.lean:30-35`, verbatim:
> `def NO_GO_CANONICAL_STRESS_CONSERVATION_PROJECTION (n : Nat) : Prop :=`
> `  ∃ A : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ, archiveDivergence (symPart A) ≠ 0`
> `theorem canonical_stress_conservation_no_go (n : Nat) : NO_GO_CANONICAL_STRESS_CONSERVATION_PROJECTION n`

**F5 — the ℚ Sym⁴ perturbation carrier + its geometric divergence (the other carrier).**
`09_LEAN_FORMALIZATION/D0/Geometry/FiniteSpin2WaveOperator.lean:29-32,66-68`, verbatim:
> `structure SymPert4 where`  `  h : QMat4`  `  symm : h.transpose = h`
> `def finiteDivergence4 (h : SymPert4) : Role4 -> Rat := (h.h * eta4).mulVec k4`

---

## 2. Construction (the object is now DEFINED)

**Perturbation model.** The discrete metric perturbation on the scene is the symmetric
off-diagonal edge-weight field `h_ij = w_ij` (`i≠j`), with graph Laplacian
`L(h)_ij = -w_ij` off-diagonal, `L(h)_ii = Σ_j w_ij`. The frozen scene is the flat
background `w_ij = 1` on every K(9,11,13) edge (adjacency).

**S_A2 as an exact ℚ functional of h** (F2; `g_a2_einstein_check.py:S_A2`):
```
S_A2(h) = Σ_{i≠j} L_ij² / (ρ_i ρ_j) = 2 · Σ_{edges {i,j}} w_ij² / (ρ_i ρ_j).
```

**The rank-2 tensor G_A2 = ∂S_A2/∂h** (the missing operator of F1;
`g_a2_einstein_check.py:grad_S_A2`), closed-form over ℚ:
```
G_A2^{ij} = ∂S_A2/∂w_ij = 4 · w_ij / (ρ_i ρ_j)     (off-diagonal; diagonal ≡ 0).
```
It is (i) SYMMETRIC by construction (defined per unordered edge, so `G_A2^{ij}=G_A2^{ji}`),
and (0) a GENUINE gradient — it matches an independent exact-ℚ central difference of S_A2
at three probe edges (`PASS_VARIATIONAL_GRADIENT`), so it is not a fitted stand-in. This
answers the "MISSING variational-derivative operator" half of F1: **the operator now exists,
in closed form, on a single carrier (ℚ, the scene edge set).**

---

## 3. Result — the divergence test (exact ℚ, load-bearing)

Test: the corpus discrete contracted-Bianchi identity `(div G_A2)_j = Σ_i G_A2^{ij} = 0`
(F3), computed exactly over ℚ on K(9,11,13).

**FLAT measure ρ≡1** (the a₂ proxy at flat measure — the naive Einstein interface):
```
(div G_A2)_j = Σ_i 4·w_ij = 4·deg(j).
```
On K(9,11,13) every node has degree ≥ 20 (zone-0 node: 11+13=24, zone-1: 9+13=22,
zone-2: 9+11=20), so `(div G_A2)_j = {96, 88, 80} ≠ 0` for every node. **max|div| = 96.**
NOT conserved.

**PERRON / degree measure ρ_i = deg(i)** (the weighted a₂ the cert's own boundary clause
invokes): `max|div| = 23/120 ≠ 0`. Still NOT conserved.

**Verdict (candidate): OBSTRUCTION.** The finite a₂/EH-proxy variational Einstein tensor
`G_A2 = ∂S_A2/∂h` is SYMMETRIC but is NOT `archiveDivergence`-free on the frozen scene,
under either the flat or the Perron measure. The exact obstruction is
`(div G_A2)_j = 4·deg(j)/ρ… ≠ 0`, driven by the fact that the a₂ proxy is a sum of squared
edge weights whose gradient is the (weighted) adjacency, not a Laplacian — the adjacency has
NONZERO row sums (= the degree), which is exactly the discrete Bianchi failure that
`canonical_stress_conservation_no_go` (F4) predicts.

Reproduce: `python3 _TASKS_CENTER_ATTACK/g_a2_einstein_check.py` → `RESULT conclusion = OBSTRUCTION`.

---

## 4. Why the existing cert's "CLOSED" is an over-claim (the precise error)

`05_CERTS/vp_spectral_einstein_response.py` is NOT a print-only stub anymore — someone wrote
a can-fail cert. But it proves an EASIER statement than the registry note (F1) demands, by
two substitutions that the note explicitly forbids:

1. **Wrong scalar.** The cert sets `S = Tr(L²)` (its docstring: "S(L) = Tr(L^2)"), then
   `G := dS = 2L`. But the a₂/EH proxy is `S_A2 = Σ_{i≠j} L_ij²/(ρ_iρ_j)` (F2), **not**
   `Tr(L²)`. `Tr(L²)` includes the diagonal `Σ_i L_ii²` term (the "volume"/cosmological
   part), and its gradient w.r.t. the full matrix L is the Laplacian itself.

2. **Wrong derivative + wrong divergence.** The cert computes `dS/dL` (derivative w.r.t. the
   operator L itself), giving `2L`; then it calls `2L` "divergence-free" because a graph
   Laplacian has zero ROW SUMS. Both facts are TRUE, but neither is the target: (a) the
   target is `∂S_A2/∂h_ij` on a metric-PERTURBATION space, not `dS/dL`; (b) `2L` is
   row-sum-zero for the trivial reason that L annihilates constants — this is NOT the
   contracted-Bianchi identity for a stress tensor, it is the definition of a Laplacian.

The honest object `G_A2 = ∂S_A2/∂h` (this memo, §2) is the (weighted) adjacency `4w/(ρρ)`,
whose row sums are `4·deg/ρ… ≠ 0`. **The old cert's "divergence-free" is a property of the
Laplacian `2L`, silently substituted for the actual a₂ variational stress, which is NOT
divergence-free.** `g_a2_einstein_check.py` PASS_CONTROL_A / PASS_CONTROL_B pins this: the
divergence routine returns 0 for `2L` (non-degenerate) but nonzero for `G_A2` (a genuinely
different rank-2 object).

---

## 5. Pre-registered self-attack (strongest attack against this memo)

**SA1 — "the divergence operator is wrong; use finiteDivergence4 (F5), and it may vanish."**
The corpus has TWO divergence notions: `archiveDivergence` = row sum (F3, on the ℝ archive
carrier) and `finiteDivergence4 = (h·η)·k` (F5, on the ℚ Sym⁴ Lorentz carrier). This memo
tested `archiveDivergence`. Could `G_A2` be `finiteDivergence4`-free instead, rescuing BUILT?
— Two answers. (a) `archiveDivergence` is the operator the discrete contracted-Bianchi
identity is literally stated against in the corpus (`curvature_gradient_conserved`, F3), so
it is the *correct* target for THIS claim. (b) The carrier-mismatch (F1) is the deeper block:
`G_A2` lives on the scene edge set (33 nodes), `finiteDivergence4` on Fin 4 with a Lorentz η
and a fixed null covector k=(1,1,0,0) — there is no scene→Fin4 map that carries the a₂
gradient onto the k-contraction. Testing `finiteDivergence4` on `G_A2` is not even type-
correct without the missing cross-carrier binding (D0-HODGE-LINKS-001, still open). So SA1
does not rescue BUILT; it re-exposes the carrier mismatch as a second, independent block.

**SA2 — "you picked the wrong perturbation; the RIGHT h makes it conserved."** The
obstruction `(div G_A2)_j = 4·deg(j)` is structural: for ANY positive edge-weight field,
`∂S_A2/∂w_ij = 4w_ij/(ρ_iρ_j) > 0`, so the row sum is a sum of positive terms and cannot
vanish on a connected graph. Conservation would require signed weights (a signed/Laplacian-
like stress), which is exactly the substitution the old cert made and which is NOT the a₂
gradient. Pre-registered: `g_a2_einstein_check.py` CONTROL_B fails the CONCLUSION if flat
conservation is ever falsely asserted (mutation-tested: forcing `is_conserved_flat=True`
trips CONTROL_B, exit 1).

**SA3 — "the a₂ gradient plus a Lagrange/gauge term IS conserved (the true Einstein tensor
is Ric − ½Rg, not just Ric)."** Correct in spirit and this is the honest bridge: the smooth
`G_μν = R_μν − ½R g_μν` is conserved precisely because of the `−½R g` trace-subtraction. The
finite analogue would subtract a trace term to enforce conservation — but that trace-adjusted
tensor is a NEW object that must be BUILT and shown to reduce to `∂S_A2/∂h` only in a limit;
it is not the bare `∂S_A2/∂h` this claim names. This is a valid FUTURE construction, not a
present closure. See §6 bridge.

**SA4 — "the divergence operator is degenerate / everything fails, so the obstruction is
vacuous."** REFUTED by the corpus's OWN conserved object. F3 (`curvature_gradient_conserved`,
`ArchiveBianchiIdentity.lean:55-56`, verbatim: `archiveDivergence (archiveCurvatureGradient n)
= 0`) proves that a DIFFERENT rank-2 tensor — the *seam curvature gradient* — IS exactly
`archiveDivergence`-free. So `archiveDivergence` is not vacuously-nonzero; it returns 0 for a
genuinely conserved tensor (mirrored by `PASS_CONTROL_A` on `2L` and `PASS_CONTROL_C` on the
zero tensor). The obstruction is therefore a *specific* property of the a₂/EH-proxy variational
response `G_A2`, not a defect of the divergence operator. This SHARPENS the diagnosis: the
corpus already owns a conserved discrete-Bianchi tensor (`archiveCurvatureGradient`); the
`D0-SPECTRAL-EINSTEIN-001` claim over-reached by asserting the *a₂/EH-proxy* gradient is that
conserved object, when it is a different, non-conserved one.

**SA5 (model-robustness) — "you rigged the obstruction by dropping the diagonal volume term;
the FULL Tr(L²) gradient is conserved."** REFUTED in-code (`PASS_CONTROL_D`). Differentiating
the FULL `Tr(L(w)²)` (diagonal `Σ_a deg_a²` volume term included) w.r.t. the *metric* `h=w`
via the chain rule (degree depends on `w`) gives `G_full^{ab} = 2(deg_a+deg_b) + 4w_ab` and
`(div G_full)_b = 4E + 2N·deg_b = {3020, 2888, 2756} ≠ 0` on the scene, cross-checked against
an independent exact-ℚ finite difference. The obstruction survives under BOTH the off-diagonal
EH-proxy `S_A2` (owned by F2) and the full `Tr(L²)`. It does not depend on the modeling choice.

---

## 6. Honest bridge — what a CONSERVED finite Einstein tensor would require (labelled IMPORT)

The bare a₂/EH-proxy variational stress `G_A2 = ∂S_A2/∂h` is not conserved (§3, model-robust
§5-SA5). A conserved finite Einstein tensor on the scene, if desired, is a SEPARATE construction
requiring one of the following EXPLICIT, minimal, honestly-labelled bridge assumptions — none of
which is presently owned; each is an IMPORT, not a derivation:

- **BRIDGE-A (trace-reversal counterterm).** Define `Ĝ := G_A2 − (½)·τ·g` with a discrete
  trace scalar `τ` and background metric `g`, chosen so `archiveDivergence Ĝ = 0`. This mirrors
  the smooth `R_μν − ½R g_μν`. STATUS: not built; must (i) exhibit `τ,g` on the scene carrier,
  (ii) prove conservation exactly over ℚ, (iii) show `Ĝ → G_A2` in a flat/decoupling limit so it
  is a genuine completion of THIS object and not an unrelated tensor. NOTE: no *multiple of the
  Laplacian* `cL` can serve — `L` is already `archiveDivergence`-free (F3-style), so `div(G_A2 +
  cL) = div(G_A2) ≠ 0` for every `c` (verified: the L-counterterm leaves the obstruction intact).
  The counterterm must be a genuinely non-Laplacian trace object.

- **BRIDGE-B (change the divergence pairing).** Adopt the ℚ Sym⁴ Lorentz divergence
  `finiteDivergence4 = (h·η)·k` (F5) instead of the row-sum `archiveDivergence`. STATUS: blocked
  by the carrier mismatch (F1) — there is no owned scene(33-node)→Fin4 map carrying the a₂
  gradient onto the null-covector contraction; building it is exactly the open
  `D0-HODGE-LINKS-001` cross-carrier binding, itself colliding with F4. Not a shortcut.

- **BRIDGE-C (import the smooth conservation).** Assert `∇^μ G_μν = 0` from the continuum
  Connes/Rieffel spectral-action limit as an EXTERNAL passport (D0-SMOOTH-MANIFOLD-PASSPORT).
  STATUS: this is an honest IMPORT of continuum GR, valid only as a labelled bridge assumption in
  a G2 gate — it does NOT make the finite object conserved; it declares conservation to hold only
  in the smooth limit, which is not the frozen-scene claim.

None of A/B/C is claimed here. The present result stands on its own as an OBSTRUCTION for the
bare finite object; the above are the only honest routes to a conserved successor, all deferred.

---

## 7. Registry motions (PROPOSALS ONLY — no CSV/ledger/.lean edits made)

1. **Demote `D0-SPECTRAL-EINSTEIN-001`: `CERT-CLOSED → PROOF-TARGET`.** The `release_status`
   column at `CLAIM_TO_LEAN_MAP.csv:175` currently reads `CERT-CLOSED`. The cert
   `vp_spectral_einstein_response.py` proves a substituted statement (`G = dS/dL = 2L`
   divergence-free), NOT the registry-note obligation (`G_A2 = ∂S_A2/∂h` symmetric AND
   divergence-free). The genuine object is DEFINED here and is NOT divergence-free; therefore the
   claim is not closed. Proposed note append:
   > "[Iter-CA G_A2 build] The rank-2 a₂/EH-proxy Einstein response G_A2 = ∂S_A2/∂h is now
   > DEFINED in closed form over ℚ on the scene (g_a2_einstein_check.py). It is symmetric but is
   > NOT archiveDivergence-free: (div G_A2)_j = 4·deg(j)/(ρ…) ≠ 0 (flat AND Perron), model-robust
   > to full Tr(L²) (div=4E+2N·deg). This is the discrete-Bianchi failure predicted by
   > canonical_stress_conservation_no_go. The old cert's 'divergence-free' is a property of 2L=dS/dL,
   > a different object. DEMOTE CERT-CLOSED → PROOF-TARGET; a conserved successor needs an explicit
   > trace-reversal counterterm / cross-carrier binding (BRIDGE-A/B/C), none owned. Jointly open
   > with D0-HODGE-LINKS-001."

2. **Replace the cert.** Swap `python_cert = vp_spectral_einstein_response.py` handling: the
   new can-fail computation is `_TASKS_CENTER_ATTACK/g_a2_einstein_check.py` (exact ℚ, 4 negative
   controls incl. model-robustness CONTROL_D; mutation-tested — forcing conserved trips CONTROL_B,
   exit 1). Recommend either repointing the cert or archiving the old one as `*_SUPERSEDED`.

3. **`D0-HODGE-LINKS-001` stays `PROOF-TARGET`** (unchanged). This memo confirms its block: the
   cross-carrier binding is what BRIDGE-B would need, and it collides with F4 (`canonical_stress_
   conservation_no_go`). No motion; cross-reference added.

4. **No LEAN_ASSUMPTION_LEDGER row.** Do NOT anchor an ASSUMP row to `a2_is_eh_proxy` (the
   scalar) — consistent with the row-175 standing instruction ("Do NOT anchor an ASSUMP row to
   the scalar a2_is_eh_proxy -- it supplies no tensor"). The obstruction is a theorem-grade
   negative result, not a bridge import; it needs no assumption row.

---

## 8. Summary (candidate, pre-skeptic-external)

The finite Einstein tensor `G_A2 = ∂S_A2/∂h` on K(9,11,13) **exists and is symmetric** — the
"MISSING variational-derivative operator" of F1 is now written in closed form over ℚ on a single
carrier. But it is **NOT `archiveDivergence`-free** (exact ℚ, flat + Perron, model-robust to full
Tr(L²)), so the conserved finite Einstein tensor is **NOT built**; the obstruction is
`(div G_A2)_j = 4·deg(j)/(ρ…) ≠ 0`, exactly the discrete-Bianchi failure predicted by the
colliding NO-GO F4. The registry's `CERT-CLOSED` is an over-claim (substituted `2L=dS/dL` for the
a₂ metric gradient) and is proposed for demotion to `PROOF-TARGET`. A conserved successor is a
deferred construction (BRIDGE-A/B/C, none owned). Outcome: **OBSTRUCTION-PROVED** — a real,
load-bearing negative result on the finite→GR cement link.

