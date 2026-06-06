import D0.Geometry.TorusCore13GeometryOrigin
import Mathlib.Tactic

namespace D0.Matter

/-- Three D0 baryon-role labels. -/
abbrev BaryonRole : Type := Fin 3

/-- Tensor carrier for the finite baryon decuplet construction. -/
abbrev BaryonTripleCarrier : Type :=
  Prod BaryonRole (Prod BaryonRole BaryonRole)

/-- Triple carrier over the three torus shell roles. -/
abbrev BaryonTripleShellCarrier : Type :=
  Prod D0.Geometry.TorusShell
    (Prod D0.Geometry.TorusShell D0.Geometry.TorusShell)

/-- The shell-role baryon triple carrier has the same ordered dimension, 27. -/
theorem baryon_triple_shell_card_eq_27 :
    Fintype.card BaryonTripleShellCarrier = 27 := by
  decide

/-- Read one of the three tensor positions. -/
def baryonTripleAt (t : BaryonTripleCarrier) (i : Fin 3) : BaryonRole :=
  if i.val = 0 then t.1 else if i.val = 1 then t.2.1 else t.2.2

/-- S3 acts by permuting the positions of the triple, not by acting on one vertex. -/
def permuteTriple (g : Equiv.Perm (Fin 3)) :
    BaryonTripleCarrier -> BaryonTripleCarrier :=
  fun t =>
    (baryonTripleAt t (g.symm 0),
      (baryonTripleAt t (g.symm 1), baryonTripleAt t (g.symm 2)))

/-- Orbit relation under position permutations. -/
def SameS3Orbit (x y : BaryonTripleCarrier) : Prop :=
  exists g : Equiv.Perm (Fin 3), permuteTriple g x = y

/-- The transposition of the first two tensor positions. -/
def swap01Triple (t : BaryonTripleCarrier) : BaryonTripleCarrier :=
  (t.2.1, (t.1, t.2.2))

/-- The ordered triple carrier has dimension 27. -/
theorem baryon_triple_carrier_card :
    Fintype.card BaryonTripleCarrier = 27 := by
  simp [BaryonTripleCarrier, BaryonRole]

/--
Canonical sorted representatives for S3 orbits of triples over three labels.
These ten constructors are the finite D0 decuplet carrier; they are not PDG or
QCD labels.
-/
inductive SortedTriple where
  | t000
  | t001
  | t002
  | t011
  | t012
  | t022
  | t111
  | t112
  | t122
  | t222
  deriving DecidableEq, Repr, Fintype

namespace SortedTriple

def toCarrier : SortedTriple -> BaryonTripleCarrier
  | .t000 => (0, (0, 0))
  | .t001 => (0, (0, 1))
  | .t002 => (0, (0, 2))
  | .t011 => (0, (1, 1))
  | .t012 => (0, (1, 2))
  | .t022 => (0, (2, 2))
  | .t111 => (1, (1, 1))
  | .t112 => (1, (1, 2))
  | .t122 => (1, (2, 2))
  | .t222 => (2, (2, 2))

theorem toCarrier_sorted (s : SortedTriple) :
    (toCarrier s).1.val <= (toCarrier s).2.1.val /\
      (toCarrier s).2.1.val <= (toCarrier s).2.2.val := by
  cases s <;> decide

end SortedTriple

/-- The fully symmetric S3 sector over three labels has decuplet dimension 10. -/
theorem sorted_triple_card_eq_ten :
    Fintype.card SortedTriple = 10 := by
  decide

/-- A pair-average over the transposition used in the nucleon-line no-go. -/
def transpositionPairAverage (a : BaryonTripleCarrier -> Int)
    (x : BaryonTripleCarrier) : Int :=
  a x + a (swap01Triple x)

/--
Any line sector changing sign under a transposition is annihilated by the
corresponding symmetric transposition average.
-/
theorem antisymmetric_line_annihilated_by_s3_symmetrizer
    (a : BaryonTripleCarrier -> Int)
    (hanti : forall x, a (swap01Triple x) = -a x)
    (x : BaryonTripleCarrier) :
    transpositionPairAverage a x = 0 := by
  unfold transpositionPairAverage
  rw [hanti x]
  simp

/-- Constructive finite baryon decuplet carrier closure. -/
structure BaryonS3SymmetrizerClosure where
  carrier_witness : BaryonTripleCarrier
  carrier_dim : Fintype.card BaryonTripleCarrier = 27
  decuplet_dim : Fintype.card SortedTriple = 10
  sorted_representatives :
    forall s : SortedTriple,
      (SortedTriple.toCarrier s).1.val <= (SortedTriple.toCarrier s).2.1.val /\
        (SortedTriple.toCarrier s).2.1.val <= (SortedTriple.toCarrier s).2.2.val
  antisymmetric_line_no_go :
    forall (a : BaryonTripleCarrier -> Int),
      (forall x, a (swap01Triple x) = -a x) ->
        forall x, transpositionPairAverage a x = 0

/-- Concrete owner for the finite S3 baryon decuplet carrier. -/
def baryon_s3_symmetrizer_closure : BaryonS3SymmetrizerClosure where
  carrier_witness := (0, (0, 0))
  carrier_dim := baryon_triple_carrier_card
  decuplet_dim := sorted_triple_card_eq_ten
  sorted_representatives := SortedTriple.toCarrier_sorted
  antisymmetric_line_no_go := by
    intro a hanti x
    exact antisymmetric_line_annihilated_by_s3_symmetrizer a hanti x

end D0.Matter
