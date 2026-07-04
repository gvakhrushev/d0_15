# T2′ MATCHING FORCING v2 — the 13-leg (representation-home) argument (DRAFT, submitted to skeptic)

**Author:** chief researcher. Status: DRAFT; replaces the KILLED v1 (`T2_PRIME_TYPE_FORCING.md`;
kill accepted in `T2_PRIME_REVIEW_VERDICT.md`). v2 must in particular kill the reviewer's named
survivor **m′ = (9↔E₀, 11↔E₃, 13↔E₄)**. No registry row edited. Computational leg:
`w8_holomorph_check.py` (18 checks, RESULT: PASS).

## What v2 does differently

v1 argued through the "memory necessity" of zone 11 and died by its own citation. v2 never mentions
memory, order, or necessity-typing. It decides the bit at the **13-leg**, on a definitional identity
of the corpus's own objects, and takes the 11-leg by elimination.

## Owned pre-facts

- **P1 (verbatim §01.20, cert `vp_v1141_abcd_omega8_v9_phi_capacity.py`):**
  `V₁₃ = V₉ ⊔ {four terminal roles A,B,C,D}` — the 13-extension IS the role square, as a set,
  by the corpus's own construction. (`V₁₁ = V₉ ⊔ D₂`, the direct/return dyad.)
- **P2 (§01.7.1B, `D0-OMEGA8-CENTER-001`, CORE-FORMALIZED):** the abelianization
  `Q₈/[Q₈,Q₈]` is the Klein four-group whose classes are the role pairs `{±1},{±i},{±j},{±k}`
  — i.e. the ABCD square is the class set of Q₈ mod the structural ℤ₂.
- **P3 (definitional + verified):** functions on the role classes embed in ℂ[Q₈] exactly as the
  ±-pair symmetrizer, and that projector IS `E₀+E₃` by the corpus's own definitions
  (`Q8Terminal.lean`: E₃ := ½(I+L₋₁) − E₀, hence E₀+E₃ = ½(I+L₋₁)); its trace is 4 = |ABCD|;
  it is orthogonal to E₄ (`(E₀+E₃)E₄ = 0`); and on E₄ the role classes are ill-defined
  (`L₋₁ = −1` there: a class function must satisfy f(−g)=f(g), while E₄ forces f(−g)=−f(g),
  so the only class function in E₄ is 0). All four facts machine-checked.
- **P4 (base leg, agreed):** 9 ↔ E₀ — accepted by both the proposed matching and the reviewer's m′.

## The forcing (DEF-0.2.2 instantiation)

Assume ¬X at the remaining bit: `13 ↔ E₄` (this is m′, since E₀ is taken by P4). Zone 13's own
defining content — the capacity it adds to the scene — is the role square (P1). Inside the branch
algebra ℂ[Q₈], everything the role square can express lives in `E₀ ⊕ E₃` and **nothing** of it
lives in E₄: the home is orthogonal (P3) and the classes are ill-defined there (P3). So under
`13 ↔ E₄` the identification must still register the 13-extension's owned content somewhere, and the
assigned block structurally refuses it; a supplementary structure θ — a translation reconciling
±-collapsed role classes with a block on which ± acts as −1 — is required. θ affects distinguishable
outcomes (role-class readouts exist and differ from their absence), is not derivable from prior
DEF/THE (it contradicts the block's own algebra), and is not part of the distinguishability
protocol: θ is exogenous (DEF 0.3.1), ⊥M1. Hence `13 ↔ E₃`, and `11 ↔ E₄` **by elimination** —
no property of zone 11 is consumed. ∎ (draft, pending skeptic)

## The licensing dichotomy (pre-empting the "why must blocks represent extensions?" attack)

Either the zone↔block identification is required to respect owned structure, or it is not.
- If **yes**: the representation-home obstruction above forces `13 ↔ E₃` (m′ dies).
- If **no**: the identification is pure naming; a naming carries no physical content, is fixed by
  M1+ canonicalization for free, and the bit is empty of physics either way.
The only escape is a *named third position*: a specific owned structure the identification must
respect that discriminates differently from the representation home. Producing that named structure
is exactly what §05.8.R requires of a refusal; absent it, the bit closes.

## Bonus (not load-bearing): ID₂ resolves positively under one stated hypothesis

Q₈ has a **unique** involution (−1; machine-checked), hence a unique 2-element subgroup = Z(Q₈).
If the V₁₁-extension dyad embeds in the role group as a subgroup at all, it is forced to be the
structural ℤ₂, and its nontrivial (direct-vs-return, antisymmetric) character is representable
exactly where `L₋₁ = −1` — in E₄. This gives the 11-leg a positive weld consistent with the
elimination result; the *embeds-as-subgroup* hypothesis is stated, not owned, and the forcing above
does not use it.

## Anti-trap note

`|ABCD| = 4 = rank E₄` is a cardinality coincidence and is NOT the key; a "faithfulness/cardinality"
key welding the square to E₄ is exactly the pairing P3 forbids. Cardinality agreement of the home is
`4 = 1 + 3 = rank(E₀⊕E₃)` — trace-checked.

## If the skeptic passes v2

The matching closes as (9↔E₀, 11↔E₄, 13↔E₃) with the load on P1–P4. Remaining named gaps of the T2′
programme (unchanged by v2): the structural scene attachment (`TorusShell → Shell3/radius` map absent
in Lean — `T2_PRIME_REVIEW_VERDICT.md` §2) and the λ=1-slice conditionality inherited from
`TerminalReturn.lean`. Minting per `VERIFIED_CLOSURE_PROTOCOL.md` stays obligatory before any status
motion.
