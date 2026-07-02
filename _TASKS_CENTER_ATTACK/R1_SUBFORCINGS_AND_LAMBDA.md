# R1 SUB-FORCINGS + the λ-lattice finding (DRAFT, pre-skeptic)

**Author:** chief researcher. Status: DRAFT; two writable sub-forcings with computed bases, one
structural finding with an owned weld, one named clash. No registry row edited. Computational legs:
`r1_theta_port.py` (PASS, this folder), inline lattice arithmetic (recorded below).

## Sub-forcing A — the balanced port (the ½ of F_term = ½P_br)

**Computed base (`r1_theta_port.py`):** for the unitary port family R_θ = [[cosθ,−sinθ],[sinθ,cosθ]]⊗I₇:
`F_term(θ) = sin²θ · I` on the branch space; `F = ½·I ⇔ θ = π/4`, unique in (0, π/2); the
leaf-asymmetry parameter `|cos²θ − sin²θ|` vanishes iff balanced; and θ≠π/4 ports ARE unitary —
the existing cert's negative control (non-normalized matrix) is blind to this family. **Cert gap of
record for `verify_unified_feedback.py`: add the θ-family control.**

**Forcing draft (DEF-0.2.2):** the two-port couples two copies of U_br — the two leaves of the
double cover (UE = blockdiag(U_br, U_br)·R_θ; the ± leaf structure is the structural ℤ₂, §01.7.1B).
Assume θ ≠ π/4. Then the coupling carries the nonzero leaf-asymmetry |cos²θ − sin²θ| — a parameter
that distinguishes the two leaves. Distinguishing the leaves of the double cover requires a
which-leaf register not derivable from prior DEF/THE (the leaves are exchanged by the owned ℤ₂);
the parameter affects distinguishable outcomes (F_term = sin²θ scales every feedback readout):
exogenous θ, ⊥M1. Hence θ = π/4 and the ½ is forced. **Stated premise:** the two U_br copies are
the ℤ₂-exchanged leaves (to be welded to §01.7.1B by the reviewer; if the two copies have distinct
owned types instead, the forcing fails there — named risk).

## Sub-forcing B — λ must be a derived point, not a family parameter

The two contacts' K†K spectra and the dressed factors (1−λz⁴), (1−λz³) vary with λ: λ affects
distinguishable outcomes. A freely-ranging λ ∈ U(1) is a continuum label carried as required
structure — exactly what M1+ bans as CORE (BOOK_00 §00.1: ℝ-primitives are BRIDGE-only; an
uncountable label set is an external catalog). Hence the edge-cover *family* is FORMALISM;
the physical instance needs λ at a **derived point** (algebraic, owned-derivable). This does not
pick the point; it collapses U(1) to a finite/derived candidate set. Nearly-direct M1+ instance;
cheap to review.

## The λ-lattice finding (structural; one owned weld, one clash, one unowned flag)

§01.22 owns (CORE-FORCING) the discretization of the phase circle: the base-zone cycle must have
exactly N = 9 steps (fewer gluing addresses ⊥M1, more needing a significance catalog ⊥M1), step
40°. If the same argument runs per zone (address counts 11 and 13), branch-cycle holonomies
quantize on **zone lattices**: λ_μ ∈ μ₁₁, λ_τ ∈ μ₁₃ (roots of unity).

**The owned weld (verified arithmetic):** with λ_μ ∈ μ₁₁, the zeros of the μ-return factor
1 − λz⁴ live on the 2π/44 lattice — return modulus **44 = q_T**, the corpus's own first forced
return window (§01.22: q_T = lcm(|ABCD|, V₁₁) = 4·11, owned). The base-lattice reading (λ ∈ μ₉)
gives modulus 36 — unowned. So the zone-lattice reading reproduces an owned window exactly;
the base-lattice reading does not.

**The named clash:** zone lattices give **different** λ per cycle (μ₁₁ vs μ₁₃), contradicting the
certs' common-λ construction; my scout memo's "single-λ forced by single-section" candidate is
hereby downgraded to one side of an open fork: {common derived λ} vs {per-zone lattice λ}.
The certs' identities are λ-uniform, so both survive at cert level; the fork is physical.

**The unowned flag:** the τ-side zone-lattice modulus is 39 = 3·13; no owned window 39 exists.
Per §00.9 E-accounting, searching the corpus for a 39 *after* this derivation is forbidden as
post-hoc; a 39-window claim would need pre-registration. Recorded as a prediction-shaped item
ONLY: *if* the zone-lattice reading is forced, a 39-return structure should appear where the
τ-cycle meets zone 13 — to be tested against material that was not consulted in deriving it.

**Missing premise, precisely:** does the §01.22 N=D discretization argument apply to *branch-cycle
holonomies* (phases of return cycles through a zone), or only to the base-zone addressor cycle γ*?
The argument's two blades (address-gluing / significance-catalog) are stated for address positions;
extending them to holonomy phases needs: "a holonomy phase not resolvable by the zone's address
positions is either indistinguishable (⊥M1) or needs an external resolution catalog (⊥M1)."
That extension is the single load-bearing step for the lattice route — the next forcing to write
and the next thing a skeptic should attack.

## Consequences if the lattice route survives

λ collapses from U(1) to finite sets welded to owned windows; the dressed z⁴/z³ structure becomes
physical at specific roots of unity; the contact bit (m vs m′) may then be discriminated by which
assignment reproduces owned return moduli (44 at the μ/11 leg is already m-shaped: the 4-cycle is
welded to zone 11 by the owned q_T arithmetic itself — lcm(4, 11)). Note this is the THIRD
independent owned-material chain landing on m (after the return-order key and downstream
consumption) — still evidence, not forcing, until the missing premise is owned.

## Obligations

1. Skeptic pass on A and B (cheap; A's premise and B's "affects outcomes" step are the targets).
2. Write the N=D-for-holonomies extension (the missing premise) in DEF-0.2.2 form; skeptic it.
3. Add the θ-family control to the unified feedback cert (task-folder copy first).
4. Do NOT search for 39; pre-register the grammar first if route 2 survives.
