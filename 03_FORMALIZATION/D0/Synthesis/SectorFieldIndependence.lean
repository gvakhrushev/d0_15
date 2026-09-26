import Mathlib.Tactic
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.QuadraticAlgebra.Basic
import D0.Synthesis.TransportSplittingFieldObstruction

/-!
# Sector field-independence: the D0 sectors share only the integer `359`

**Target.** `D0-SECTOR-FIELD-INDEPENDENCE-001`. `D0-EDGE-INVARIANT-CROSS-SECTOR-001` (T13)
proved that the single integer `359 = |E|` is the identical object consumed by five sectors.
This module answers the dual question it left open — *do the sectors also share irrational
structure?* — in the negative, and strictly extends `D0-TRANSPORT-SPLITTING-FIELD-NOGO-001`
(T19, which established only `√5 ∉ K`).

Each sector's characteristic quadratic irrational is an owned object:
* α / golden dressing : `α_top⁻¹ = 359φ⁻² − φ⁻⁵ = 544 − 182√5 ∈ ℚ(√5)` (T17);
* dark-energy S_DE window: active eigenvalues `3/2 ± √10/40 ∈ ℚ(√10)`
  (`D0-SCENE-ACTIVE-EIGENVALUES-001`), radicand `10` from the window discriminant `640 = 2⁷·5`;
* transport / metric cubic: splitting field `K` of `λ³ − 359λ − 2574`, quadratic subfield
  `ℚ(√Δ)`, `Δ = 6185264 = 2⁴·193·2003`, squarefree kernel `386579 = 193·2003` (T19).

**Constructive content proved here (clean axioms, no `native_decide`).**

* `radicand_alpha/de/tr_not_square` — the three radicands `5, 10, 386579` are non-squares
  (each discharged by a mod-p certificate);
* `alpha_de_distinct` (`50` non-square), `alpha_tr_distinct` (`5·386579` non-square),
  `de_tr_distinct` (`10·386579` non-square), followed by a direct construction-level theorem:
  the concrete algebras `QuadraticAlgebra ℚ 5 0`, `QuadraticAlgebra ℚ 10 0`,
  `QuadraticAlgebra ℚ 386579 0` admit NO pairwise `ℚ`-algebra equivalence;
* `triple_independent` (`5·10·386579` non-square) — together with the above, NO nonempty
  subset product of `{5,10,386579}` is a square;
* `SectorCharacterAlgebra` — three successive quadratic adjunctions form a concrete
  eight-dimensional **field** over `ℚ` (no zero divisors, degree 8, fully internal);
  three explicit commuting involutions have a diagonal
  character table `(-1,+1,+1)`, `(+1,-1,+1)`, `(+1,+1,-1)`, giving the constructive
  three-bit sign architecture internally;
* `ten_disc_not_square` (`10·Δ` non-square) — the exact criterion `ℚ(√Δ) ≠ ℚ(√10)`, the new
  leg beyond T19; combined with T19's `five_disc_not_square` (`ℚ(√Δ) ≠ ℚ(√5)`).

**The owner-edge reading (external theorem, hypotheses proved here).** For the irreducible
transport cubic with non-square discriminant `Gal(K/ℚ) = S₃`, so `K` has a UNIQUE quadratic
subfield `ℚ(√Δ)` (standard Galois theory of cubics — external owner edge, as in T19). Given
`five_disc_not_square` and `ten_disc_not_square`, BOTH `√5 ∉ K` and `√10 ∉ K`: the
transport/metric sector is field-disjoint from the α sector AND the dark-energy sector.
Consequence: the entire
structure the sectors share is the rational integer `359`; no field automorphism carries one
sector's characteristic irrational to another's — the field-theoretic sharpening of
"one invariant, five sectors".

**Honest scope.** Pairwise non-isomorphism, fieldness, dimension 8, the commuting involutions
and their character table are fully internal. The remaining EXTERNAL owner edge is the `S₃`
unique-quadratic-subfield theorem placing neither `√5` nor `√10` in the *full transport
splitting field* (and, separately, packaging the three sign involutions as the complete Galois
group rather than the explicit subgroup already constructed). The original
`sector_field_independence` theorem is the arithmetic conjunction; `sector_character_assembly`
and `sector_compositum_degree_eight_field` are the constructive algebraic capstones. Deterministic mirror:
`04_CERTIFICATES/vp_sector_field_independence.py` (can-FAIL, with dependent-triple controls).
-/

namespace D0.Synthesis.SectorFieldIndependence

open D0.Synthesis.TransportSplittingFieldObstruction

/-! ## Fully internal quadratic-field separation

Unlike the later `S₃`/compositum conclusions, pairwise sector-field distinction can be proved
inside Lean without any external field-theory owner edge. Represent `ℚ(√d)` concretely by
`QuadraticAlgebra ℚ d 0`, whose generator `ι = ⟨0,1⟩` satisfies `ι²=d`. If an
`ℚ`-algebra equivalence sent this generator to `x+y√b`, then

`(x+y√b)² = a` gives `x²+b y²=a` and `2xy=0`.

If `y=0`, then `a` is a rational square; otherwise `x=0` and `ab=(by)²` is a rational square.
Thus `a` and `ab` both non-square rule out the equivalence. This is the exact constructive
criterion consumed below for the three D0 sector pairs. -/

/-- Concrete generator of `QuadraticAlgebra R d 0`, satisfying `sqrtGen d ^ 2 = d`. -/
def sqrtGen {R : Type*} [Zero R] [One R] (d : R) : QuadraticAlgebra R d 0 := ⟨0, 1⟩

@[simp]
theorem sqrtGen_re {R : Type*} [Zero R] [One R] (d : R) : (sqrtGen d).re = 0 := rfl

@[simp]
theorem sqrtGen_im {R : Type*} [Zero R] [One R] (d : R) : (sqrtGen d).im = 1 := rfl

theorem sqrtGen_sq {R : Type*} [CommRing R] (d : R) :
    sqrtGen d ^ 2 = algebraMap R (QuadraticAlgebra R d 0) d := by
  ext <;> simp [sqrtGen, pow_two, QuadraticAlgebra.algebraMap_eq]

/-- Internal separation criterion for concrete quadratic algebras:
if `a` and `a*b` are not rational squares, there is no `ℚ`-algebra equivalence
`ℚ[√a] ≃ ℚ[√b]`. -/
theorem no_quadraticAlgEquiv_of_not_squares (a b : ℚ)
    (ha : ¬ IsSquare a) (hab : ¬ IsSquare (a * b)) :
    ¬ Nonempty (QuadraticAlgebra ℚ a 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ b 0) := by
  rintro ⟨e⟩
  let z : QuadraticAlgebra ℚ b 0 := e (sqrtGen a)
  have hzsq : z ^ 2 = algebraMap ℚ (QuadraticAlgebra ℚ b 0) a := by
    calc
      z ^ 2 = e (sqrtGen a ^ 2) := by simp [z]
      _ = e (algebraMap ℚ (QuadraticAlgebra ℚ a 0) a) := by rw [sqrtGen_sq]
      _ = algebraMap ℚ (QuadraticAlgebra ℚ b 0) a := by simp
  have hre : z.re ^ 2 + b * z.im ^ 2 = a := by
    have := congrArg QuadraticAlgebra.re hzsq
    simp [pow_two, QuadraticAlgebra.algebraMap_eq] at this
    nlinarith
  have him : 2 * z.re * z.im = 0 := by
    have := congrArg QuadraticAlgebra.im hzsq
    simp [pow_two, QuadraticAlgebra.algebraMap_eq] at this
    nlinarith
  by_cases hy : z.im = 0
  · apply ha
    refine ⟨z.re, ?_⟩
    simpa [hy, pow_two] using hre.symm
  · have hx : z.re = 0 := by
      rcases mul_eq_zero.mp him with hleft | hy'
      · exact (mul_eq_zero.mp hleft).resolve_left (by norm_num)
      · exact (hy hy').elim
    have hre' : b * z.im ^ 2 = a := by
      simpa [hx] using hre
    apply hab
    refine ⟨b * z.im, ?_⟩
    calc
      a * b = (b * z.im ^ 2) * b := by rw [hre']
      _ = (b * z.im) * (b * z.im) := by ring

/-- The dark-energy S_DE window quadratic `160x² − 480x + 359` has discriminant
`b² − 4ac = 640 = 2⁶·10`, so its splitting radicand is the squarefree kernel `10`
(roots `3/2 ± √10/40`, owned at `D0-SCENE-ACTIVE-EIGENVALUES-001`). -/
theorem sde_window_disc :
    (480 : ℤ) ^ 2 - 4 * 160 * 359 = 640 ∧ (640 : ℤ) = 2 ^ 6 * 10 := by
  norm_num

/-- Generic non-square helper by a modulus certificate: if the image of `n` in `ZMod m` is not
a square, then `n` is not a square in `ℤ`. -/
private theorem not_square_of_mod {m : ℕ} (n : ℤ)
    (h : ¬ IsSquare ((n : ℤ) : ZMod m)) : ¬ IsSquare n := fun hs =>
  h (hs.map (Int.castRingHom (ZMod m)))

/-- Radicand of the α sector: `5` is not a square (mod-3: `5 ≡ 2`, squares mod 3 are `{0,1}`). -/
theorem radicand_alpha_not_square : ¬ IsSquare (5 : ℤ) := by
  apply not_square_of_mod (m := 3)
  have : ((5 : ℤ) : ZMod 3) = 2 := by decide
  rw [this]; decide

/-- Radicand of the dark-energy sector: `10` is not a square (mod-4: `10 ≡ 2`,
squares mod 4 are `{0,1}`). -/
theorem radicand_de_not_square : ¬ IsSquare (10 : ℤ) := by
  apply not_square_of_mod (m := 4)
  have : ((10 : ℤ) : ZMod 4) = 2 := by decide
  rw [this]; decide

/-- Radicand of the transport sector: `386579 = 193·2003` is not a square
(mod-3: `386579 ≡ 2`). -/
theorem radicand_tr_not_square : ¬ IsSquare (386579 : ℤ) := by
  apply not_square_of_mod (m := 3)
  have : ((386579 : ℤ) : ZMod 3) = 2 := by decide
  rw [this]; decide

/-- α ≠ DE: `5·10 = 50` is not a square (mod-3: `50 ≡ 2`) ⇒ `ℚ(√5) ≠ ℚ(√10)`. -/
theorem alpha_de_distinct : ¬ IsSquare (5 * 10 : ℤ) := by
  apply not_square_of_mod (m := 3)
  have : ((5 * 10 : ℤ) : ZMod 3) = 2 := by decide
  rw [this]; decide

/-- α ≠ transport at radicand level: `5·386579 = 1932895` is not a square (mod-4: `≡ 3`)
⇒ `ℚ(√5) ≠ ℚ(√386579)`. -/
theorem alpha_tr_distinct : ¬ IsSquare (5 * 386579 : ℤ) := by
  apply not_square_of_mod (m := 4)
  have : ((5 * 386579 : ℤ) : ZMod 4) = 3 := by decide
  rw [this]; decide

/-- DE ≠ transport at radicand level: `10·386579 = 3865790` is not a square (mod-3: `≡ 2`)
⇒ `ℚ(√10) ≠ ℚ(√386579)`. -/
theorem de_tr_distinct : ¬ IsSquare (10 * 386579 : ℤ) := by
  apply not_square_of_mod (m := 3)
  have : ((10 * 386579 : ℤ) : ZMod 3) = 2 := by decide
  rw [this]; decide

/-- Full independence: `5·10·386579 = 19328950` is not a square (mod-4: `≡ 2`). With the three
pairwise legs, NO nonempty subset product of `{5,10,386579}` is a square, so the compositum is
`(ℤ/2)³`. -/
theorem triple_independent : ¬ IsSquare (5 * 10 * 386579 : ℤ) := by
  apply not_square_of_mod (m := 4)
  have : ((5 * 10 * 386579 : ℤ) : ZMod 4) = 2 := by decide
  rw [this]; decide

/-- The α and dark-energy quadratic algebras are not `ℚ`-algebra isomorphic. This is the
field-distinction conclusion itself, fully internalized — not merely its radicand certificate. -/
theorem alpha_de_no_algEquiv :
    ¬ Nonempty
      (QuadraticAlgebra ℚ 5 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ 10 0) := by
  apply no_quadraticAlgEquiv_of_not_squares
  · norm_num
  · norm_num

/-- The α and transport-character quadratic algebras are not `ℚ`-algebra isomorphic. -/
theorem alpha_tr_no_algEquiv :
    ¬ Nonempty
      (QuadraticAlgebra ℚ 5 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ 386579 0) := by
  apply no_quadraticAlgEquiv_of_not_squares
  · norm_num
  · norm_num

/-- The dark-energy and transport-character quadratic algebras are not `ℚ`-algebra isomorphic. -/
theorem de_tr_no_algEquiv :
    ¬ Nonempty
      (QuadraticAlgebra ℚ 10 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ 386579 0) := by
  apply no_quadraticAlgEquiv_of_not_squares
  · norm_num
  · norm_num

/-- Fully internal pairwise separation of the three sector quadratic algebras. The only
remaining external owner edge in T26 concerns the degree-8 compositum and the placement of
these characters inside the full `S₃` transport splitting field — not pairwise distinction. -/
theorem sector_quadratic_algebras_pairwise_nonisomorphic :
    (¬ Nonempty (QuadraticAlgebra ℚ 5 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ 10 0))
      ∧ (¬ Nonempty (QuadraticAlgebra ℚ 5 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ 386579 0))
      ∧ (¬ Nonempty (QuadraticAlgebra ℚ 10 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ 386579 0)) :=
  ⟨alpha_de_no_algEquiv, alpha_tr_no_algEquiv, de_tr_no_algEquiv⟩

/-! ## The finite sector-character carrier

The three independent quadratic axes admit a single finite carrier obtained by three successive
quadratic adjunctions. Its algebra and module structure is completely concrete and its dimension
is forced to be `2·2·2 = 8`; the final block of this module then discharges the three conditional
non-squareness hypotheses and upgrades this carrier to a genuine field. -/

/-- α character layer: adjoin an element whose square is `5`. -/
abbrev AlphaCharacterAlgebra := QuadraticAlgebra ℚ 5 0

/-- α × DE character layer: adjoin a second element whose square is `10`. -/
abbrev AlphaDECharacterAlgebra :=
  QuadraticAlgebra AlphaCharacterAlgebra
    (algebraMap ℚ AlphaCharacterAlgebra 10) 0

/-- Full three-axis sector character carrier: adjoin the transport character
whose square is `386579 = 193·2003`. -/
abbrev SectorCharacterAlgebra :=
  QuadraticAlgebra AlphaDECharacterAlgebra
    (algebraMap ℚ AlphaDECharacterAlgebra 386579) 0

theorem alpha_character_finrank :
    Module.finrank ℚ AlphaCharacterAlgebra = 2 :=
  QuadraticAlgebra.finrank_eq_two (5 : ℚ) 0

theorem alpha_de_character_finrank :
    Module.finrank ℚ AlphaDECharacterAlgebra = 4 := by
  calc
    Module.finrank ℚ AlphaDECharacterAlgebra =
        Module.finrank ℚ AlphaCharacterAlgebra *
          Module.finrank AlphaCharacterAlgebra AlphaDECharacterAlgebra :=
      (Module.finrank_mul_finrank ℚ AlphaCharacterAlgebra AlphaDECharacterAlgebra).symm
    _ = 2 * 2 := by
      rw [alpha_character_finrank,
        QuadraticAlgebra.finrank_eq_two (algebraMap ℚ AlphaCharacterAlgebra 10) 0]
    _ = 4 := by norm_num

/-- The three sector characters have a concrete eight-dimensional finite carrier. This is the
internal rank statement underlying the external `(ℤ/2)³` compositum reading. -/
theorem sector_character_finrank :
    Module.finrank ℚ SectorCharacterAlgebra = 8 := by
  calc
    Module.finrank ℚ SectorCharacterAlgebra =
        Module.finrank ℚ AlphaDECharacterAlgebra *
          Module.finrank AlphaDECharacterAlgebra SectorCharacterAlgebra :=
      (Module.finrank_mul_finrank ℚ AlphaDECharacterAlgebra SectorCharacterAlgebra).symm
    _ = 4 * 2 := by
      rw [alpha_de_character_finrank,
        QuadraticAlgebra.finrank_eq_two (algebraMap ℚ AlphaDECharacterAlgebra 386579) 0]
    _ = 8 := by norm_num

/-- Sign conjugation on a pure quadratic algebra (`ι ↦ -ι`) as an algebra equivalence. -/
def quadraticSignAlgEquiv {R : Type*} [CommRing R] (a : R) :
    QuadraticAlgebra R a 0 ≃ₐ[R] QuadraticAlgebra R a 0 where
  toFun z := ⟨z.re, -z.im⟩
  invFun z := ⟨z.re, -z.im⟩
  left_inv z := by ext <;> simp
  right_inv z := by ext <;> simp
  map_add' x y := by
    ext
    · simp
    · simp [add_comm]
  map_mul' x y := by
    ext
    · simp
    · simp [add_comm]
  commutes' r := by ext <;> simp [QuadraticAlgebra.algebraMap_eq]

@[simp]
theorem quadraticSignAlgEquiv_re {R : Type*} [CommRing R] (a : R)
    (z : QuadraticAlgebra R a 0) :
    (quadraticSignAlgEquiv a z).re = z.re := rfl

@[simp]
theorem quadraticSignAlgEquiv_im {R : Type*} [CommRing R] (a : R)
    (z : QuadraticAlgebra R a 0) :
    (quadraticSignAlgEquiv a z).im = -z.im := rfl

/-- Lift a scalar algebra automorphism coefficientwise through a quadratic algebra when it fixes
the defining coefficients. This is the mechanism that separates the three sign axes by depth. -/
def liftCoeffAlgEquiv {S R : Type*} [CommSemiring S] [CommRing R] [Algebra S R]
    (a b : R) (e : R ≃ₐ[S] R) (ha : e a = a) (hb : e b = b) :
    QuadraticAlgebra R a b ≃ₐ[S] QuadraticAlgebra R a b where
  toFun z := ⟨e z.re, e z.im⟩
  invFun z := ⟨e.symm z.re, e.symm z.im⟩
  left_inv z := by ext <;> simp
  right_inv z := by ext <;> simp
  map_add' x y := by ext <;> simp
  map_mul' x y := by
    ext <;> simp [ha, hb]
  commutes' s := by
    ext
    · change e (algebraMap S R s) = algebraMap S R s
      exact e.commutes s
    · change e 0 = 0
      simp

@[simp]
theorem liftCoeffAlgEquiv_re {S R : Type*} [CommSemiring S] [CommRing R] [Algebra S R]
    (a b : R) (e : R ≃ₐ[S] R) (ha : e a = a) (hb : e b = b)
    (z : QuadraticAlgebra R a b) :
    (liftCoeffAlgEquiv a b e ha hb z).re = e z.re := rfl

@[simp]
theorem liftCoeffAlgEquiv_im {S R : Type*} [CommSemiring S] [CommRing R] [Algebra S R]
    (a b : R) (e : R ≃ₐ[S] R) (ha : e a = a) (hb : e b = b)
    (z : QuadraticAlgebra R a b) :
    (liftCoeffAlgEquiv a b e ha hb z).im = e z.im := rfl

/-- α-sign on the first quadratic layer. -/
def sigmaAlpha0 : AlphaCharacterAlgebra ≃ₐ[ℚ] AlphaCharacterAlgebra :=
  quadraticSignAlgEquiv 5

/-- α-sign lifted through the DE layer. -/
def sigmaAlpha1 : AlphaDECharacterAlgebra ≃ₐ[ℚ] AlphaDECharacterAlgebra :=
  liftCoeffAlgEquiv (algebraMap ℚ AlphaCharacterAlgebra 10) 0 sigmaAlpha0 (by simp) (by simp)

/-- α-sign lifted through all three layers. -/
def sigmaAlpha : SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra :=
  liftCoeffAlgEquiv (algebraMap ℚ AlphaDECharacterAlgebra 386579) 0 sigmaAlpha1
    (by simp) (by simp)

/-- DE-sign on the second layer, viewed as a `ℚ`-algebra equivalence. -/
def sigmaDE1 : AlphaDECharacterAlgebra ≃ₐ[ℚ] AlphaDECharacterAlgebra :=
  (quadraticSignAlgEquiv (algebraMap ℚ AlphaCharacterAlgebra 10)).restrictScalars ℚ

/-- DE-sign lifted through the transport-character layer. -/
def sigmaDE : SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra :=
  liftCoeffAlgEquiv (algebraMap ℚ AlphaDECharacterAlgebra 386579) 0 sigmaDE1
    (by simp) (by simp)

/-- Transport-character sign on the outer layer. -/
def sigmaTransport : SectorCharacterAlgebra ≃ₐ[ℚ] SectorCharacterAlgebra :=
  (quadraticSignAlgEquiv (algebraMap ℚ AlphaDECharacterAlgebra 386579)).restrictScalars ℚ

@[simp] theorem sigmaAlpha0_re (z : AlphaCharacterAlgebra) :
    (sigmaAlpha0 z).re = z.re := rfl
@[simp] theorem sigmaAlpha0_im (z : AlphaCharacterAlgebra) :
    (sigmaAlpha0 z).im = -z.im := rfl
@[simp] theorem sigmaAlpha1_re (z : AlphaDECharacterAlgebra) :
    (sigmaAlpha1 z).re = sigmaAlpha0 z.re := rfl
@[simp] theorem sigmaAlpha1_im (z : AlphaDECharacterAlgebra) :
    (sigmaAlpha1 z).im = sigmaAlpha0 z.im := rfl
@[simp] theorem sigmaAlpha_re (z : SectorCharacterAlgebra) :
    (sigmaAlpha z).re = sigmaAlpha1 z.re := rfl
@[simp] theorem sigmaAlpha_im (z : SectorCharacterAlgebra) :
    (sigmaAlpha z).im = sigmaAlpha1 z.im := rfl

@[simp] theorem sigmaDE1_re (z : AlphaDECharacterAlgebra) :
    (sigmaDE1 z).re = z.re := rfl
@[simp] theorem sigmaDE1_im (z : AlphaDECharacterAlgebra) :
    (sigmaDE1 z).im = -z.im := rfl
@[simp] theorem sigmaDE_re (z : SectorCharacterAlgebra) :
    (sigmaDE z).re = sigmaDE1 z.re := rfl
@[simp] theorem sigmaDE_im (z : SectorCharacterAlgebra) :
    (sigmaDE z).im = sigmaDE1 z.im := rfl

@[simp] theorem sigmaTransport_re (z : SectorCharacterAlgebra) :
    (sigmaTransport z).re = z.re := rfl
@[simp] theorem sigmaTransport_im (z : SectorCharacterAlgebra) :
    (sigmaTransport z).im = -z.im := rfl

/-- Each sector sign is an involution. -/
theorem sector_signs_involutive (z : SectorCharacterAlgebra) :
    sigmaAlpha (sigmaAlpha z) = z
      ∧ sigmaDE (sigmaDE z) = z
      ∧ sigmaTransport (sigmaTransport z) = z := by
  constructor
  · ext <;> simp [sigmaAlpha, sigmaAlpha1, sigmaAlpha0, liftCoeffAlgEquiv,
      quadraticSignAlgEquiv]
  constructor
  · ext <;> simp [sigmaDE, sigmaDE1, liftCoeffAlgEquiv, quadraticSignAlgEquiv]
  · ext <;> simp [sigmaTransport, quadraticSignAlgEquiv]

set_option maxHeartbeats 1000000 in
/-- The three sector signs commute pairwise: they are independent coordinate reflections on the
eight-dimensional character carrier. -/
theorem sector_signs_commute (z : SectorCharacterAlgebra) :
    sigmaAlpha (sigmaDE z) = sigmaDE (sigmaAlpha z)
      ∧ sigmaAlpha (sigmaTransport z) = sigmaTransport (sigmaAlpha z)
      ∧ sigmaDE (sigmaTransport z) = sigmaTransport (sigmaDE z) := by
  constructor
  · ext <;> simp [sigmaAlpha, sigmaAlpha1, sigmaAlpha0, sigmaDE, sigmaDE1,
      liftCoeffAlgEquiv, quadraticSignAlgEquiv]
  constructor
  · ext <;> simp [sigmaAlpha, sigmaAlpha1, sigmaAlpha0, sigmaTransport,
      liftCoeffAlgEquiv, quadraticSignAlgEquiv]
  · ext <;> simp [sigmaDE, sigmaDE1, sigmaTransport, liftCoeffAlgEquiv,
      quadraticSignAlgEquiv]

/-- α-character generator, embedded through the DE and transport layers. -/
def alphaAxis : SectorCharacterAlgebra :=
  algebraMap AlphaDECharacterAlgebra SectorCharacterAlgebra
    (algebraMap AlphaCharacterAlgebra AlphaDECharacterAlgebra (sqrtGen 5))

/-- DE-character generator, embedded through the transport layer. -/
def deAxis : SectorCharacterAlgebra :=
  algebraMap AlphaDECharacterAlgebra SectorCharacterAlgebra
    (sqrtGen (algebraMap ℚ AlphaCharacterAlgebra 10))

/-- Transport-character generator in the outer quadratic layer. -/
def transportAxis : SectorCharacterAlgebra :=
  sqrtGen (algebraMap ℚ AlphaDECharacterAlgebra 386579)

/-- Exact `3×3` character table, read on the three distinguished rational coordinates:

```
                 α-axis   DE-axis   transport-axis
σ_α                -1        +1          +1
σ_DE               +1        -1          +1
σ_transport        +1        +1          -1
```

Together with involutivity and pairwise commutation, this gives a faithful internal
three-bit sign system on the eight-dimensional carrier — the constructive `(ℤ/2)³`
architecture, without invoking the external Kummer degree theorem. -/
theorem sector_sign_character_table :
    (sigmaAlpha alphaAxis).re.re.im = -1
      ∧ (sigmaAlpha deAxis).re.im.re = 1
      ∧ (sigmaAlpha transportAxis).im.re.re = 1
      ∧ (sigmaDE alphaAxis).re.re.im = 1
      ∧ (sigmaDE deAxis).re.im.re = -1
      ∧ (sigmaDE transportAxis).im.re.re = 1
      ∧ (sigmaTransport alphaAxis).re.re.im = 1
      ∧ (sigmaTransport deAxis).re.im.re = 1
      ∧ (sigmaTransport transportAxis).im.re.re = -1 := by
  norm_num [sigmaAlpha, sigmaAlpha1, sigmaAlpha0, sigmaDE, sigmaDE1, sigmaTransport,
    alphaAxis, deAxis, transportAxis, liftCoeffAlgEquiv, quadraticSignAlgEquiv, sqrtGen,
    QuadraticAlgebra.algebraMap_eq, QuadraticAlgebra.re_one, QuadraticAlgebra.im_one]

/-- Constructive capstone: pairwise non-isomorphic sector quadratic algebras, a concrete
eight-dimensional joint carrier, three commuting involutions, and the diagonal `(-1,+1,+1)`,
`(+1,-1,+1)`, `(+1,+1,-1)` character table — all internal to Lean. -/
theorem sector_character_assembly :
    ((¬ Nonempty (QuadraticAlgebra ℚ 5 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ 10 0))
        ∧ (¬ Nonempty (QuadraticAlgebra ℚ 5 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ 386579 0))
        ∧ (¬ Nonempty (QuadraticAlgebra ℚ 10 0 ≃ₐ[ℚ] QuadraticAlgebra ℚ 386579 0)))
      ∧ Module.finrank ℚ SectorCharacterAlgebra = 8
      ∧ (∀ z : SectorCharacterAlgebra,
        sigmaAlpha (sigmaAlpha z) = z
          ∧ sigmaDE (sigmaDE z) = z
          ∧ sigmaTransport (sigmaTransport z) = z)
      ∧ (∀ z : SectorCharacterAlgebra,
        sigmaAlpha (sigmaDE z) = sigmaDE (sigmaAlpha z)
          ∧ sigmaAlpha (sigmaTransport z) = sigmaTransport (sigmaAlpha z)
          ∧ sigmaDE (sigmaTransport z) = sigmaTransport (sigmaDE z))
      ∧ ((sigmaAlpha alphaAxis).re.re.im = -1
          ∧ (sigmaAlpha deAxis).re.im.re = 1
          ∧ (sigmaAlpha transportAxis).im.re.re = 1
          ∧ (sigmaDE alphaAxis).re.re.im = 1
          ∧ (sigmaDE deAxis).re.im.re = -1
          ∧ (sigmaDE transportAxis).im.re.re = 1
          ∧ (sigmaTransport alphaAxis).re.re.im = 1
          ∧ (sigmaTransport deAxis).re.im.re = 1
          ∧ (sigmaTransport transportAxis).im.re.re = -1) :=
  ⟨sector_quadratic_algebras_pairwise_nonisomorphic, sector_character_finrank,
    sector_signs_involutive, sector_signs_commute, sector_sign_character_table⟩

/-- New leg beyond T19 (which owned only `√5 ∉ K`): `10·Δ` is not a square (mod-3: `≡ 2`),
the exact criterion `ℚ(√Δ) ≠ ℚ(√10)`, hence `√10 ∉ K`. -/
theorem ten_disc_not_square : ¬ IsSquare (10 * 6185264 : ℤ) := by
  apply not_square_of_mod (m := 3)
  have : ((10 * 6185264 : ℤ) : ZMod 3) = 2 := by decide
  rw [this]; decide

/-- Assembly: the arithmetic legs of sector field-independence. The `S₃`/unique-quadratic-
subfield classification and the multiquadratic-degree conclusion are the named external owner
edge (row text); everything below is Lean-clean. Combined with `five_disc_not_square` (T19),
the two `disc` legs give `√5 ∉ K` and `√10 ∉ K`; the seven radicand legs give a `(ℤ/2)³`
independence, so the three sector fields meet only in `ℚ` and the shared object is `359`. -/
theorem sector_field_independence :
    ((480 : ℤ) ^ 2 - 4 * 160 * 359 = 640)
      ∧ ¬ IsSquare (5 : ℤ)
      ∧ ¬ IsSquare (10 : ℤ)
      ∧ ¬ IsSquare (386579 : ℤ)
      ∧ ¬ IsSquare (5 * 10 : ℤ)
      ∧ ¬ IsSquare (5 * 386579 : ℤ)
      ∧ ¬ IsSquare (10 * 386579 : ℤ)
      ∧ ¬ IsSquare (5 * 10 * 386579 : ℤ)
      ∧ ¬ IsSquare (5 * 6185264 : ℤ)
      ∧ ¬ IsSquare (10 * 6185264 : ℤ) :=
  ⟨(sde_window_disc).1, radicand_alpha_not_square, radicand_de_not_square,
    radicand_tr_not_square, alpha_de_distinct, alpha_tr_distinct, de_tr_distinct,
    triple_independent, five_disc_not_square, ten_disc_not_square⟩

/-! ## Full closure: the eight-dimensional carrier is a field

The conditional mathlib field instance for `QuadraticAlgebra F d 0` requires exactly that `d`
is not a square in `F`. The coordinate lemma below propagates rational non-squareness through
successive quadratic layers. We then install each field explicitly and restore both the
immediate-base and rational algebra structures, avoiding the `HPow`/`Algebra` instance diamond
that otherwise appears for nested conditional field instances. -/

/-- In `F(√d)`, a scalar `c` can be a square only if `c` or `c*d` is already a square in `F`. -/
theorem not_isSquare_algebraMap {F : Type*} [Field F] (h2 : (2 : F) ≠ 0)
    (d c : F) (hc : ¬ IsSquare c) (hcd : ¬ IsSquare (c * d)) :
    ¬ IsSquare (algebraMap F (QuadraticAlgebra F d 0) c) := by
  rintro ⟨r, hr⟩
  have e1 : r.re * r.re + d * (r.im * r.im) = c := by
    have h := congrArg QuadraticAlgebra.re hr
    simpa [QuadraticAlgebra.algebraMap_eq, mul_assoc] using h.symm
  have e2 : r.re * r.im + r.im * r.re = 0 := by
    have h := congrArg QuadraticAlgebra.im hr
    simpa [QuadraticAlgebra.algebraMap_eq] using h.symm
  have e2' : r.re * r.im = 0 := by
    have h : 2 * (r.re * r.im) = 0 := by rw [two_mul]; linear_combination e2
    rcases mul_eq_zero.mp h with h | h
    · exact absurd h h2
    · exact h
  rcases mul_eq_zero.mp e2' with hre | him
  · apply hcd
    have hce : d * (r.im * r.im) = c := by simpa [hre] using e1
    exact ⟨d * r.im, by rw [← hce]; ring⟩
  · apply hc
    have hce : r.re * r.re = c := by simpa [him] using e1
    exact ⟨r.re, hce.symm⟩

-- Layer 1: `ℚ(√5)`.
instance alphaFieldFact : Fact (∀ r : ℚ, r ^ 2 ≠ (5 : ℚ) + (0 : ℚ) * r) :=
  ⟨fun r hr => (by norm_num : ¬ IsSquare (5 : ℚ)) ⟨r, by linear_combination -hr⟩⟩

noncomputable instance alphaCharacterField : Field AlphaCharacterAlgebra :=
  @QuadraticAlgebra.instField ℚ inferInstance 5 0 alphaFieldFact

local instance alphaCharZero : CharZero AlphaCharacterAlgebra :=
  algebraRat.charZero AlphaCharacterAlgebra

-- Layer 2: `ℚ(√5,√10)`. `10` and `10·5=50` are non-squares in `ℚ`.
theorem ten_not_square_in_alpha :
    ¬ IsSquare (algebraMap ℚ AlphaCharacterAlgebra 10) :=
  not_isSquare_algebraMap (by norm_num) 5 10 (by norm_num) (by norm_num)

instance alphaDEFieldFact : Fact (∀ r : AlphaCharacterAlgebra,
    r ^ 2 ≠ algebraMap ℚ AlphaCharacterAlgebra 10 + (0 : AlphaCharacterAlgebra) * r) :=
  ⟨fun r hr => ten_not_square_in_alpha ⟨r, by
    show algebraMap ℚ AlphaCharacterAlgebra 10 = r * r
    linear_combination -hr⟩⟩

noncomputable instance alphaDECharacterField : Field AlphaDECharacterAlgebra :=
  @QuadraticAlgebra.instField AlphaCharacterAlgebra alphaCharacterField
    (algebraMap ℚ AlphaCharacterAlgebra 10) 0 alphaDEFieldFact

local instance alphaDEImmediateAlgebra :
    Algebra AlphaCharacterAlgebra AlphaDECharacterAlgebra :=
  QuadraticAlgebra.instAlgebra

noncomputable local instance alphaDERationalAlgebra : Algebra ℚ AlphaDECharacterAlgebra :=
  QuadraticAlgebra.instAlgebra

local instance alphaDECharZero : CharZero AlphaDECharacterAlgebra :=
  algebraRat.charZero AlphaDECharacterAlgebra

-- Layer 3: `ℚ(√5,√10,√386579)`. The four rational square-class tests are
-- 386579, 5·386579, 10·386579, and 5·10·386579.
theorem kernel_not_square_in_alpha :
    ¬ IsSquare (algebraMap ℚ AlphaCharacterAlgebra 386579) :=
  not_isSquare_algebraMap (by norm_num) 5 386579 (by norm_num) (by norm_num)

theorem kernel_times_ten_not_square_in_alpha :
    ¬ IsSquare ((algebraMap ℚ AlphaCharacterAlgebra 386579)
      * (algebraMap ℚ AlphaCharacterAlgebra 10)) := by
  have hmul : (algebraMap ℚ AlphaCharacterAlgebra 386579)
      * (algebraMap ℚ AlphaCharacterAlgebra 10)
      = algebraMap ℚ AlphaCharacterAlgebra 3865790 := by rw [← map_mul]; norm_num
  rw [hmul]
  exact not_isSquare_algebraMap (by norm_num) 5 3865790 (by norm_num) (by norm_num)

theorem kernel_not_square_in_alphaDE :
    ¬ IsSquare (algebraMap ℚ AlphaDECharacterAlgebra 386579) := by
  have hmain := not_isSquare_algebraMap (F := AlphaCharacterAlgebra) (by norm_num)
    (algebraMap ℚ AlphaCharacterAlgebra 10)
    (algebraMap ℚ AlphaCharacterAlgebra 386579)
    kernel_not_square_in_alpha kernel_times_ten_not_square_in_alpha
  have hEq : algebraMap ℚ AlphaDECharacterAlgebra 386579 =
      algebraMap AlphaCharacterAlgebra AlphaDECharacterAlgebra
        (algebraMap ℚ AlphaCharacterAlgebra 386579) := by
    norm_num
    exact (map_natCast (algebraMap AlphaCharacterAlgebra AlphaDECharacterAlgebra) 386579).symm
  rw [hEq]
  exact hmain

instance sectorFieldFact : Fact (∀ r : AlphaDECharacterAlgebra,
    r ^ 2 ≠ algebraMap ℚ AlphaDECharacterAlgebra 386579
      + (0 : AlphaDECharacterAlgebra) * r) :=
  ⟨fun r hr => kernel_not_square_in_alphaDE ⟨r, by
    apply QuadraticAlgebra.ext
    · have h := congrArg QuadraticAlgebra.re hr
      simp [pow_two, QuadraticAlgebra.algebraMap_eq] at h ⊢
      exact h.symm
    · have h := congrArg QuadraticAlgebra.im hr
      simp [pow_two, QuadraticAlgebra.algebraMap_eq] at h ⊢
      convert h.symm using 1
      convert (QuadraticAlgebra.im_mul r r).symm using 1
      apply QuadraticAlgebra.ext <;> simp⟩⟩

noncomputable instance sectorCharacterField : Field SectorCharacterAlgebra :=
  @QuadraticAlgebra.instField AlphaDECharacterAlgebra alphaDECharacterField
    (algebraMap ℚ AlphaDECharacterAlgebra 386579) 0 sectorFieldFact

local instance sectorImmediateAlgebra :
    Algebra AlphaDECharacterAlgebra SectorCharacterAlgebra :=
  QuadraticAlgebra.instAlgebra

noncomputable local instance sectorRationalAlgebra : Algebra ℚ SectorCharacterAlgebra :=
  QuadraticAlgebra.instAlgebra

local instance sectorCharZero : CharZero SectorCharacterAlgebra :=
  algebraRat.charZero SectorCharacterAlgebra

/-- The character carrier is a genuine field: it has no zero divisors. -/
theorem sector_compositum_no_zero_divisors (x y : SectorCharacterAlgebra) :
    x * y = 0 → x = 0 ∨ y = 0 :=
  fun h => mul_eq_zero.mp h

/-- Full internal closure: the three independent sector square classes generate a genuine
degree-eight field over `ℚ`, not merely an eight-dimensional algebra. -/
theorem sector_compositum_degree_eight_field :
    (∀ x y : SectorCharacterAlgebra, x * y = 0 → x = 0 ∨ y = 0)
      ∧ Module.finrank ℚ SectorCharacterAlgebra = 8 :=
  ⟨sector_compositum_no_zero_divisors, sector_character_finrank⟩

/-! ## Element-level eigenvector character table

The coordinate character table above reads three specific rational entries. Here is the full
element-level form: each sign involution negates its own axis generator and fixes the other
two — i.e. the three axis generators are simultaneous eigenvectors of the three commuting
involutions with the diagonal `(-1,+1,+1)`, `(+1,-1,+1)`, `(+1,+1,-1)` eigenvalue pattern. Every
equation is definitional. -/
theorem sigmaAlpha_alphaAxis : sigmaAlpha alphaAxis = -alphaAxis := rfl
theorem sigmaAlpha_deAxis : sigmaAlpha deAxis = deAxis := rfl
theorem sigmaAlpha_transportAxis : sigmaAlpha transportAxis = transportAxis := rfl
theorem sigmaDE_alphaAxis : sigmaDE alphaAxis = alphaAxis := rfl
theorem sigmaDE_deAxis : sigmaDE deAxis = -deAxis := rfl
theorem sigmaDE_transportAxis : sigmaDE transportAxis = transportAxis := rfl
theorem sigmaTransport_alphaAxis : sigmaTransport alphaAxis = alphaAxis := rfl
theorem sigmaTransport_deAxis : sigmaTransport deAxis = deAxis := rfl
theorem sigmaTransport_transportAxis : sigmaTransport transportAxis = -transportAxis := rfl

/-- The full element-level eigenvector character table of the three sector sign involutions. -/
theorem sector_sign_eigen_table :
    sigmaAlpha alphaAxis = -alphaAxis
      ∧ sigmaAlpha deAxis = deAxis
      ∧ sigmaAlpha transportAxis = transportAxis
      ∧ sigmaDE alphaAxis = alphaAxis
      ∧ sigmaDE deAxis = -deAxis
      ∧ sigmaDE transportAxis = transportAxis
      ∧ sigmaTransport alphaAxis = alphaAxis
      ∧ sigmaTransport deAxis = deAxis
      ∧ sigmaTransport transportAxis = -transportAxis :=
  ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

end D0.Synthesis.SectorFieldIndependence
