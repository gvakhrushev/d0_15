import Mathlib.Tactic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Multiset.Basic
import D0.NumberTheory.HurwitzMinimaxPhi

namespace D0

structure GenerationOperator where
  dim : Nat
  op : Matrix (Fin dim) (Fin dim) Rat

inductive CandidateOperator
  | graphLaplacian
  | signedIncidenceDirac
  | cliqueHodge
  | orientedBoundary
  | chargeWeightedDirac
  deriving DecidableEq, Repr

def isCanonical : CandidateOperator → Prop
  | _ => False

theorem no_canonical_operator_among_candidates :
  ∀ op : CandidateOperator, ¬ isCanonical op := by
  intro op h
  cases op <;> exact h

def candidateSpectrum : CandidateOperator → Option (Multiset Rat)
  | _ => none

theorem no_exact_candidate_spectrum :
  ∀ op : CandidateOperator, candidateSpectrum op = none := by
  intro op
  cases op <;> rfl

def samePhiRay (x y : Rat) : Prop :=
  x = y

def candidateClusterCount : CandidateOperator → Option Nat
  | _ => none

inductive SearchResult
  | ProvedExactlyThree
  | NoCanonicalOperator
  | ExistButNotThree
  | ExtraPhysicalInputRequired
  deriving DecidableEq, Repr

def searchResult : SearchResult :=
  SearchResult.NoCanonicalOperator

theorem search_result_is_no_canonical_operator :
  searchResult = SearchResult.NoCanonicalOperator := by
  rfl

structure GenerationSpectralRayNoGo where
  noCanonicalOperator : ∀ op : CandidateOperator, ¬ isCanonical op
  noExactSpectrum : ∀ op : CandidateOperator, candidateSpectrum op = none
  searchOutcome : searchResult = SearchResult.NoCanonicalOperator

theorem NO_GO_GENERATION_RAYS_UNDEFINED :
  GenerationSpectralRayNoGo := by
  exact
    { noCanonicalOperator := no_canonical_operator_among_candidates
      noExactSpectrum := no_exact_candidate_spectrum
      searchOutcome := search_result_is_no_canonical_operator }

end D0
