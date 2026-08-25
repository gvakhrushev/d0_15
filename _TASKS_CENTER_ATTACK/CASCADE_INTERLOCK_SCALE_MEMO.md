# CASCADE-INTERLOCK-SCALE — the second interlock link: the order-memory repair fails the scale floor (POST-SKEPTIC v2)

**Status:** POST-SKEPTIC v2 (2026-08-09). Skeptic #1: WOUNDED-FIXABLE, no kill on the new
content; R1-R5 applied, errors of record below. Pre-flight, CORRECTED: `chain_linked` appears
only in `CascadeChain.lean` (the single 4→5→5→6 link) and its row; `carrierRealizedRatio`
nowhere. ERROR OF RECORD (accepted): the draft claimed '`QuaternionGroup` nowhere in D0/' —
FALSE: `CascadeFloorOrderMemory.lean:71-73` already carries `control_quaternion_orderEncoded :
OrderEncoded (QuaternionGroup 2)` with the identical witness and proof, minted at
`D0-CASCADE-FLOOR-ORDER-MEMORY-001` ('witnessed twice — S₃ and, notably, Q₈') — 8 lines below
the draft's own trap-(l) citation. The draft's `q8_orderEncoded` was a verbatim duplicate:
DELETED (R1); both controls are cited from the floor row, not re-proved. Target: the umbrella row
`D0-CASCADE-INSUFFICIENCY-CHAIN-001` (the corpus's central thesis; value 37.2, attack queue),
whose own note asks for exactly this shape: "the unifying 'each floor forced by the
insufficiency of the previous' statement is the open obligation".

## Claim X (DEF-0.2.2 form)

X (Lean `D0.Foundation.CascadeInterlockScale`, clean axioms, D0.All GREEN): in the scaffold's
carried floor order (`CascadeChain` table: order memory 5→6, scale ratio 6→7), the SECOND
interlock link holds —

1. the 5→6 obligation is met on the repair carriers: `OrderEncoded (Equiv.Perm (Fin 3))`
   (`control_orderEncoded`) and `OrderEncoded (QuaternionGroup 2)`
   (`control_quaternion_orderEncoded`) — BOTH owned at `D0-CASCADE-FLOOR-ORDER-MEMORY-001`
   and cited, not re-proved (R1/R3);
2. EVERY scale ratio either carrier realizes is CAPTURED — fails the 6→7 obligation
   (`finite_carrier_ratio_captured`, fully generic over any carrier: quotients of finite-stage
   cardinalities are rational; `NonCaptured = Irrational` is the floor's own reading);
3. non-collapse: the 6→7 obligation is satisfiable (`phi_non_captured`, cited) while no
   carrier-realized ratio satisfies it (`scale_floor_forces_out`).

Net: the object that repaired order memory is one the scale floor rejects — the cascade is
forced past the finite non-commutative stage toward an irrational scale. Second link of the
chain property, matching `chain_linked_four_five_to_five_six` in shape MODULO the module's
scoped bridging definition, which the sibling did not need (its repair object literally IS
the next floor's registered failing carrier).

## Owned pre-facts (verbatim, file:line)

- `D0-CASCADE-INSUFFICIENCY-CHAIN-001` note: "the unifying 'each floor forced by the
  insufficiency of the previous' statement is the open obligation and is the corpus's headline
  target." + SCAFFOLD REGISTERED note (2026-08-09): interlock carried "at ONE link, not across
  the chain."
- `CascadeChain.lean` table: "| 5→6 | order memory … | `π₁(T²) = ℤ×ℤ` (abelian) | any
  non-commutative carrier (`S₃`, `Q₈`) |" and "| 6→7 | non-capture — no finite stage matches
  the scale ratio | any rational ratio | an irrational one; `φ` after the owned canonization |".
- `CascadeChain.lean` (chain-linked section): "The repair does not anticipate the next
  obligation; it creates the object on which the next obligation is asked, and fails it."
  — the exact shape this module instantiates at the next link.
- `CascadeFloorOrderMemory.lean:43,63`: `OrderEncoded (G) [Mul G] : Prop := ∃ a b : G,
  a * b ≠ b * a`; `control_orderEncoded : OrderEncoded (Equiv.Perm (Fin 3))`.
- `CascadeFloorScaleRatio.lean:44-46`: "`def NonCaptured (r : ℝ) : Prop := Irrational r`";
  `:64-70` `phi_non_captured`; the floor module's own `floor_does_not_select_phi` (the φ
  narrowing is the separate owned canonization — NOT claimed here).
- Umbrella prose order caveat (§01.6.1c, umbrella row note): the prose places the scale-ratio
  step before the torus/order steps; the scaffold's registered numbering (5→6 then 6→7) is
  the adjacency owner cited (pre-registered as ATT-A).

## The forcing / construction

All content is definitional + two-line proofs over owned objects; the only new definition is
`carrierRealizedRatio G r := ∃ s t : Finset G, t.Nonempty ∧ r = s.card / t.card` (the
finite-stage values available inside a carrier), scoped as the module's own bridging reading.
Lean: builds standalone 3030 jobs GREEN (post-R1 rebuild confirmed); axioms
propext/Classical.choice/Quot.sound on all exported theorems (skeptic verified four,
pre-R1); no `native_decide`. Robustness recorded: `finite_carrier_ratio_captured` holds even
without the `t.Nonempty` conjunct (`s.card/0 = 0` is rational) — the conjunct lives in the
definiens to keep `carrierRealizedRatio` a faithful ratio notion. Distinction recorded: the
quantum dimension d = φ of the Fibonacci fusion structure (BOOK_01) is a Perron/asymptotic
limit of stage ratios, never stage-attained — it instantiates non-capture, not a
counterexample to the captured-lemma. No python cert: no numeric content beyond card-arithmetic already carried
by the Lean kernel (precedent: the sibling floor rows carry no certs).

## Named risks & PRE-REGISTERED attack surface (strongest first)

- **ATT-A (strongest: adjacency).** The §01.6.1c PROSE order places scale-ratio BEFORE
  torus/order; the scaffold's carried order places it after (6→7). If an owner re-orders, is
  the link dead? Defense, pre-registered: the link is claimed AT THE SCAFFOLD'S REGISTERED
  ORDER (its table is minted, `D0-CASCADE-CHAIN-SCAFFOLD-001`), and the semantic content —
  the finite non-commutative repair realizes only rational scales — is numbering-independent:
  under ANY ordering in which the scale floor sits above the order floor's repair, the same
  theorem carries the link; under the prose order it becomes a link from a different
  predecessor, and the theorem text survives as "the order repair is scale-rejected". The row
  text must state the adjacency owner explicitly.
- **ATT-B (the bridging definition).** "Scale ratios realized by a carrier = cardinality
  quotients" is this module's reading, not an owned prior. A skeptic can ask why scale must be
  realized as cardinality quotients. Defense: for a FINITE carrier these are the only
  finite-stage values it owns (any stage is a finite subset; its size is the only scale datum);
  the definition is stated in-module as the bridging reading with its own name, and the row
  carries it as scoped. A kill must name a DIFFERENT owned reading of "the scale a finite
  carrier realizes" under which some finite carrier realizes an irrational ratio.
- **ATT-C (carrier mismatch: Q₈).** The corpus's `Q8`-typed role objects (zone-9 labeling,
  role algebra) are a DIFFERENT carrier from Mathlib's `QuaternionGroup 2`. No binding is
  claimed: the link cites `control_quaternion_orderEncoded` (the floor row's own control) — the
  CascadeChain table's "(S₃, Q₈)" repair entry at the group level only.
- **ATT-D (vacuity / triviality).** "Finite ⇒ rational ratios" is elementary. Defense: the
  content is the INTERLOCK (the repair object fails the next obligation — the chain property
  the umbrella row names as its open unifying statement), not the arithmetic; the sibling
  link `chain_linked_four_five_to_five_six` is of exactly the same elementary grade and is
  minted. Non-collapse (`scale_floor_forces_out`) shows the floors are independent
  requirements, so the link is not a restatement.
- **ATT-E (umbrella inflation).** Two links ≠ the chain. The umbrella row stays OPEN; the row
  note must say "second link; floors defect⇒closure⇒shell and three-insufficiencies⇒three-zones
  remain unformalized".

## What this does NOT show

The full cascade theorem (umbrella stays PROOF-TARGET); the missing floors; any φ selection
(the 6→7 floor reaches "irrational" only — `floor_does_not_select_phi` cited); any binding of
`QuaternionGroup 2` to the corpus's Q8-typed role objects; any claim about the prose-order
question beyond the scaffold's registered numbering.

## Repairs (errors of record, accepted in full)

- R1: q8_orderEncoded deleted — verbatim duplicate of the minted
  control_quaternion_orderEncoded (identical witness pair and proof); the link theorem now
  cites the owned control.
- R2: row theorem list drops q8_orderEncoded; Q8 control credited to
  D0-CASCADE-FLOOR-ORDER-MEMORY-001.
- R3: false pre-flight sentence struck; all NEW/newly-carried language removed (both controls
  were carried in 2026-07).
- R4: adjacency owner named explicitly in row + umbrella notes (scaffold table,
  D0-CASCADE-CHAIN-SCAFFOLD-001, reproduced in 01.6.1c) + prose-order caveat (in the 01.6.1c
  one-liner, order-memory's successor is defect and the scale step precedes torus/order).
- R5: module header 'intrinsic to FINITENESS' replaced by 'intrinsic to finite-STAGE
  realization (for a finite carrier the finite stages exhaust it)'.
- Advisories adopted: theorem-count fix; shape-matching qualifier; Nonempty-robustness and
  quantum-dimension-distinction sentences; classifier guardrails (no continuum/smooth tokens).
