# CASCADE-FLOOR-SHELL-CLOSURE — the floor closure ⇒ shell (POST-SKEPTIC v2)

**Status:** POST-SKEPTIC v2 (2026-08-09). Skeptic #1: MINT-AFTER-REPAIRS, no kill; R1-R2 +
advisories applied (wording only, no Lean changes). Pre-flight: `shellReflection` nowhere in
D0/; no SHELL-CLOSURE row; the prose step `circulation needs closure ⇒ shell` has NO floor in
the scaffold; the owned reading is BOOK_03 §03.23.5 (FORCED status, `[^b03-45]`), which the
defect-closure row (D0-CASCADE-FLOOR-DEFECT-CLOSURE-001, minted this session) already names as
"the still-open closure⇒shell half". The owned geometry: `D0.Geometry.TorusShellAttachment`
(minted; radii inner = 1 = R−r, core = (a+1)/2 = R, outer = a = R+r, for every rational
parameter 1 < a; strict monotonicity owned). Target: umbrella
`D0-CASCADE-INSUFFICIENCY-CHAIN-001` (#2 of the attack queue, value 56.9).

## Claim X (DEF-0.2.2 form)

X (Lean `D0.Foundation.CascadeFloorShellClosure`, clean axioms, standalone 3035 GREEN +
D0.All GREEN): the cascade step `closure ⇒ shell` is carried as a genuine `CascadeStep`
(`stepShellClosure`) + the FOURTH interlock link (`chain_linked_closure_to_shell`):

1. BRIDGING PROXY (scoped, this module's own definition): closure is read as closure of the
   radius set under the radial REFLECTION around the circulation core, `ρ(x) = 2·core − x` —
   the canonical completion move of the three-term radial progression;
2. `insufficient`: the INTERIOR pair {inner, core} — §03.23.5's OWN identification, verbatim:
   "An interior defect (03.23.4) plus a memory-circulation zone (03.23.3) leaves the global
   topology open" — is NOT reflection-closed: ρ(inner) = outer escapes, for EVERY admissible
   parameter (`interior_not_reflection_closed`);
3. `control`: the three-shell set IS reflection-closed for every admissible parameter
   (`shells_reflection_closed`: ρ(inner) = outer, ρ(core) = core, ρ(outer) = inner) — the
   outer shell is exactly what the completion demands ("closing it requires an outer shell",
   §03.23.5 verbatim);
4. M1 leg: the shell's scale carries no free parameter — `x = 1 + 1/x` has EXACTLY ONE
   positive solution and it is φ (`shell_scale_forced`, real level, golden quadratic;
   §03.23.5: "The only self-consistent parameter-free scale is the positive root of
   r² − r − 1 = 0 ⇒ r = φ");
5. the forced scale is the SCALE FLOOR'S OWN SURVIVOR: φ satisfies NonCaptured
   (`shell_scale_is_scale_survivor` = `phi_non_captured`, cited) — the cascade's φ reappears
   at the shell, linking the shell floor back to the scale floor's control;
6. floor genuine via the scaffold's `step_discriminates` (`shell_closure_floor_genuine`).

Grade: NEW FLOOR + FOURTH LINK; the umbrella stays OPEN (terminal step
three-insufficiencies⇒three-zones unformalized). With this floor the §01.6.1c segment
`order ⇒ defect ⇒ closure ⇒ shell` is carried end-to-end in the CascadeStep shape.

## Owned pre-facts (verbatim, file:line)

- BOOK_03 §03.23.5 (BOOK_03:996-1018, status FORCED): "An interior defect (03.23.4) plus a
  memory-circulation zone (03.23.3) leaves the global topology open; closing it requires an
  outer shell (the Closure role D of 03.23.1). The shell's scaling cannot carry a free
  parameter (M1). The only self-consistent parameter-free scale is the positive root of
  r^2 - r - 1 = 0 => r = phi" — the owned reading of the step, including the two-interior-
  layer identification this floor's `insufficient` instantiates.
- BOOK_03 shell table (:888-891): "D=9 puncture/interface shell = R−r; D=11 memory torus
  core shell = R; D=13 outer shell = R+r".
- `TorusShellAttachment.lean`: `torusShell_radius_inner/core/outer` (= T.inner/T.core/T.outer
  = 1, (a+1)/2, a), `torusShell_radius_strictMono`, `torusShell_inner_unit` — the owned
  radius geometry the floor computes on.
- `CascadeFloorScaleRatio.lean:44-46,64-70`: `NonCaptured = Irrational`; `phi_non_captured` —
  the scale floor's survivor, re-cited as the forced shell scale.
- D0-CASCADE-FLOOR-DEFECT-CLOSURE-001 note (this session): "§03.23.5's outer-shell/global
  closure is the still-open closure⇒shell half — two named, non-competing closures" — the
  named opening this floor fills.

## The forcing / construction

All legs are short exact proofs on the owned objects: the reflection identities are `ring`
on the owned radius values; the insufficiency uses the owned strict monotonicity (core ≠
inner) with the witness T = ⟨2⟩ inhabiting the parameter type; the fixed-point uniqueness is
the golden quadratic (`goldenRatio_sq`, factorization, positivity kills the conjugate). No
`decide` beyond kernel-free proofs; axioms propext/Classical.choice/Quot.sound on all
exported theorems; no `native_decide`. Standalone 3035 GREEN; D0.All GREEN. No python cert
(kernel content only; sibling-floor precedent).

## Named risks & PRE-REGISTERED attack surface (strongest first)

- **ATT-A (strongest: the proxy).** "Global topology open/closed" is genus/boundary talk;
  the floor formalizes reflection-closure of the radius set. A skeptic can demand the
  topological statement. Defense, pre-registered: the proxy is stated as the module's own
  bridging definition (the `carrierRealizedRatio` discipline, twice minted this session);
  the radius values and their completion structure are the OWNED content of the shell table;
  "global topology" stays at §03.23.5's own prose grade — the row must say "reflection-
  closure proxy, topological reading at prose grade". A kill must name an owned FORMAL
  topology reading this proxy contradicts.
- **ATT-B (obligations quantify over ALL parameters).** Below/Above quantify `∀ T`. The
  Below universal is FALSE (good: insufficient = its negation, witnessed at T = ⟨2⟩ but the
  failure is for every T — the witness only inhabits the type). Check: is
  `interior_not_reflection_closed` the negation of ObligationBelow verbatim? Yes by
  construction. No unexhausted-class shape: the quantified class is the module's own
  parameter type.
- **ATT-C (φ⁵ / spectrum non-claims).** The φ⁵ aspect (§03.23.6) and the {9,11,13} spectrum
  forcing are NOT claimed; the zone sizes enter only through the owned attachment; the
  orientation-parity floor is separate. Stated in-module.
- **ATT-D (rational/real split).** The geometry parameter is rational; φ is real. The module
  keeps the reflection legs (ℚ, ∀ T) and the scale leg (ℝ, fixed point) in SEPARATE theorems
  meeting only through §03.23.5's prose — no rational-φ conflation. Stated in-module.
- **ATT-E (link grammar).** The fourth link connects the defect-closure floor's carrier to
  the shell geometry through §03.23.5's own two-layer identification (owned prose, FORCED
  status). Unlike links 1-3, the identification step is prose-anchored rather than
  type-level; the row must carry this grade honestly ("prose-anchored link on a FORCED owned
  reading" vs the type-level links).

## What this does NOT show

The topological (genus/boundary) closure statement; the φ⁵ aspect; the {9,11,13} spectrum
forcing; the terminal three-zones step; the full cascade theorem (umbrella stays
PROOF-TARGET). What it adds: the `order ⇒ defect ⇒ closure ⇒ shell` prose segment carried
end-to-end in the registered floor shape, with the shell scale forced parameter-free to the
scale floor's own survivor φ.

## Repairs (accepted in full)

- R1 (the strongest finding): chain_linked_closure_to_shell does NOT have the shared-object
  interlock shape of links 1-3 (no defect-floor object occurs in the theorem; the formal
  cross-floor tie is to the SCALE floor's control). Repaired: 'prose-anchored fourth link'
  grade in the module docstring, the row section and the row note; the adjacency is carried
  by 03.23.5's own FORCED identification.
- R2: the umbrella update must not silently retire the registered topological/2-cell-
  attachment reading of closure=>shell. Repaired: 'end-to-end AT REFLECTION-PROXY GRADE',
  with the topological reading listed as still open.
- Advisories adopted: rival proxy named (reflection around inner completes the pair with an
  INTERIOR shell (3-a)/2 — 'closure => OUTER shell' is proxy-relative) + canonicity anchor
  (core = owned major radius = tube center); the phi-leg framed as forcing 03.23.5's OWN
  equation with 'equation = scaling' at prose grade; rational-never-attains-phi via the
  non-capture frame of D0-CASCADE-INTERLOCK-SCALE-001; load-bearing definitions listed;
  classifier token hygiene.
