import D0.Foundation.FutureMemoryQuotientBound
import D0.Foundation.VerificationTransferApplication

/-!
# Finite capacity for future class plus registered line

A lossless packing of the existing coded archive entries needs a distinct memory
value for every future-class/line pair. The representative choice is classical.
This counts values of a supplied memory, not physical costs or independent
causality of line labels. It does not claim that one detector verdict retains a
line. The round trip is required only on the actual encoded archive entries.
-/

namespace D0.Foundation.ArchivePairCapacity

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.VerificationCore
open D0.Foundation.FutureMemoryQuotientBound
open D0.Foundation.VerificationTransferApplication
open D0.Foundation.TheoryTransfer

variable {F : FutureExecution} {E : TheoryVerification F.futureEmpiricalTheory}

/-- Choose a representative for the future class solely to count distinct
archive entries after the supplied packing. -/
noncomputable def packedArchivePair (W : SigmaWitness E) {Memory : Type}
    (pack : List W.Symbol → Memory) : F.FutureClass × E.protocol.Line → Memory :=
  fun p => pack (W.archiveCode (Quotient.out p.1, p.2))

/-- Source archive identity and round-trip preservation separate every
future-class/line pair. No preservation of invalid words is required. -/
theorem packedArchivePair_injective (W : SigmaWitness E) {Memory : Type}
    (pack : List W.Symbol → Memory) (unpack : Memory → List W.Symbol)
    (correct : ∀ s l, unpack (pack (W.archiveCode (s, l))) = W.archiveCode (s, l)) :
    Function.Injective (packedArchivePair W pack) := by
  rintro ⟨q, l⟩ ⟨r, k⟩ h
  have hcodes : W.archiveCode (Quotient.out q, l) = W.archiveCode (Quotient.out r, k) := by
    calc
      W.archiveCode (Quotient.out q, l) = unpack (pack (W.archiveCode (Quotient.out q, l))) :=
        (correct _ _).symm
      _ = unpack (pack (W.archiveCode (Quotient.out r, k))) := congrArg unpack h
      _ = W.archiveCode (Quotient.out r, k) := correct _ _
  obtain ⟨hprofile, hline⟩ := (W.archiveCode_eq_iff _ _ _ _).mp hcodes
  apply Prod.ext
  · have hclasses : (Quotient.mk F.futureSetoid (Quotient.out q) : F.FutureClass) =
        Quotient.mk F.futureSetoid (Quotient.out r) := Quotient.sound hprofile
    simpa using hclasses
  · exact hline

/-- A finite lossless archive packing needs at least one memory value for
each future class and each registered line. -/
theorem archivePair_card_le_memory (W : SigmaWitness E)
    [Fintype F.FutureClass] [Fintype E.protocol.Line] {Memory : Type} [Fintype Memory]
    (pack : List W.Symbol → Memory) (unpack : Memory → List W.Symbol)
    (correct : ∀ s l, unpack (pack (W.archiveCode (s, l))) = W.archiveCode (s, l)) :
    Fintype.card F.FutureClass * Fintype.card E.protocol.Line ≤ Fintype.card Memory := by
  have h := Fintype.card_le_of_injective (packedArchivePair W pack)
    (packedArchivePair_injective W pack unpack correct)
  simpa only [Fintype.card_prod] using h

/-! ## A concrete existing finite verification witness -/

/-- The existing finite construction on the actual visible-bit verification. -/
noncomputable def visibleArchiveWitness : SigmaWitness visibleBitVerification := by
  letI : Fintype visibleBitVerification.protocol.State := inferInstanceAs (Fintype Bool)
  letI : Fintype visibleBitVerification.protocol.Line := inferInstanceAs (Fintype Bool)
  exact finiteSigmaWitness visibleBitVerification

/-- Four memory values are required to recover all valid visible-bit archive
entries, including the identity of their registered Boolean line. -/
theorem visibleArchive_memory_lower_bound {Memory : Type} [Fintype Memory]
    (pack : List visibleArchiveWitness.Symbol → Memory)
    (unpack : Memory → List visibleArchiveWitness.Symbol)
    (correct : ∀ s l, unpack (pack (visibleArchiveWitness.archiveCode (s, l))) =
      visibleArchiveWitness.archiveCode (s, l)) :
    4 ≤ Fintype.card Memory := by
  letI : Fintype visibleBitVerification.protocol.Line := inferInstanceAs (Fintype Bool)
  have h := archivePair_card_le_memory visibleArchiveWitness pack unpack correct
  simpa [visible_future_class_card] using h

/-- On valid archive entries, retain precisely the verified state and line.
For other code words the default is arbitrary and no round trip is claimed. -/
noncomputable def visibleArchivePack (c : List visibleArchiveWitness.Symbol) : Bool × Bool :=
  match visibleArchiveWitness.coding.decode c with
  | some (Sum.inr pair) => pair
  | _ => (false, false)

noncomputable def visibleArchiveUnpack (p : Bool × Bool) : List visibleArchiveWitness.Symbol :=
  visibleArchiveWitness.coding.encode (Sum.inr p)

/-- The four-value memory reaches the bound on every actual archive entry. -/
theorem visibleArchive_roundtrip (s : visibleBitSystem.State)
    (l : visibleBitVerification.protocol.Line) :
    visibleArchiveUnpack (visibleArchivePack (visibleArchiveWitness.archiveCode (s, l))) =
      visibleArchiveWitness.archiveCode (s, l) := by
  simp [visibleArchiveUnpack, visibleArchivePack, SigmaWitness.archiveCode,
    CodePresentation.decode_encode]

theorem visibleArchive_bound_attained :
    (∀ s l, visibleArchiveUnpack (visibleArchivePack (visibleArchiveWitness.archiveCode (s, l))) =
      visibleArchiveWitness.archiveCode (s, l)) ∧ Fintype.card (Bool × Bool) = 4 :=
  ⟨visibleArchive_roundtrip, by decide⟩

end D0.Foundation.ArchivePairCapacity
