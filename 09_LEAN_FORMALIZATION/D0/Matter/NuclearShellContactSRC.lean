namespace D0.Matter

/-!
D0-SRC-001: finite nuclear shell-contact SRC operator.

The core object is not an A-only or N/Z-only scalar.  Short-range contact is
read through occupied proton/neutron shell projectors and an angular-momentum
contact selector.  The concrete Ca/Fe witness uses only finite shell occupancy.
-/

/-- Nuclear orbital, storing `2j` as a natural number. -/
structure NuclearOrbital where
  n : Nat
  l : Nat
  j2 : Nat
  deriving DecidableEq, Repr

/-- Degeneracy `2j+1`, represented as `j2+1`. -/
def degeneracy (o : NuclearOrbital) : Nat :=
  o.j2 + 1

/-- Occupied proton and neutron shell projectors in diagonal form. -/
structure ShellOccupancy where
  proton_occ : NuclearOrbital -> Nat
  neutron_occ : NuclearOrbital -> Nat

/-- Angular-momentum/contact selector fields. -/
structure ShellContactSelector where
  same_l : Prop
  same_j : Prop
  contact_channel : Prop

/-- Diagonal same-shell contact term `p_alpha n_alpha / g_alpha`. -/
def sameShellContact (O : ShellOccupancy) (o : NuclearOrbital) : Nat :=
  O.proton_occ o * O.neutron_occ o / degeneracy o

/-- The `f_{7/2}`-type shell used by the Ca/Fe finite witness. -/
def f7_2 : NuclearOrbital where
  n := 0
  l := 3
  j2 := 7

theorem f7_2_degeneracy_eq_eight :
    degeneracy f7_2 = 8 := by
  rfl

/-- Closed-core valence witness: no active `f_{7/2}` protons or neutrons. -/
def ca40Valence : ShellOccupancy where
  proton_occ o := if o = f7_2 then 0 else 0
  neutron_occ o := if o = f7_2 then 0 else 0

/-- Ca-48 witness: eight unmatched valence neutrons in `f_{7/2}`. -/
def ca48Valence : ShellOccupancy where
  proton_occ o := if o = f7_2 then 0 else 0
  neutron_occ o := if o = f7_2 then 8 else 0

/-- Fe-54 witness: six valence protons matched to eight neutrons in `f_{7/2}`. -/
def fe54Valence : ShellOccupancy where
  proton_occ o := if o = f7_2 then 6 else 0
  neutron_occ o := if o = f7_2 then 8 else 0

/-- No proton projector overlap means no same-shell contact readout. -/
theorem src_contact_requires_shell_projector_overlap
    (O : ShellOccupancy) (o : NuclearOrbital)
    (h : O.proton_occ o = 0) :
    sameShellContact O o = 0 := by
  simp [sameShellContact, h]

/-- Extra unmatched Ca-48 neutrons do not turn on the same-shell contact term. -/
theorem same_shell_contact_index_zero_for_unmatched_valence_protons :
    sameShellContact ca48Valence f7_2 = 0 := by
  native_decide

/-- Matched Fe-54 proton/neutron occupancy turns on a finite contact term. -/
theorem same_shell_contact_turns_on_for_matched_valence_pn :
    sameShellContact fe54Valence f7_2 = 6 := by
  native_decide

def massDeltaCa48Ca40 : Nat := 8
def massDeltaFe54Ca48 : Nat := 6
def neutronExcessCa48 : Nat := 8
def neutronExcessFe54 : Nat := 2

/--
Mass increment alone gives the wrong ordering for the Ca/Fe witness:
`Ca48-Ca40` has larger mass increment, while the shell-contact jump is smaller.
-/
theorem mass_number_alone_cannot_determine_src_contact :
    massDeltaFe54Ca48 < massDeltaCa48Ca40 /\
      sameShellContact ca48Valence f7_2 <
        sameShellContact fe54Valence f7_2 := by
  native_decide

/--
Neutron-excess alone also gives the wrong ordering: Fe-54 has lower neutron
excess than Ca-48 but higher matched shell contact.
-/
theorem neutron_excess_alone_cannot_determine_src_contact :
    neutronExcessFe54 < neutronExcessCa48 /\
      sameShellContact ca48Valence f7_2 <
        sameShellContact fe54Valence f7_2 := by
  native_decide

/--
D0-SRC closure package: the finite SRC readout is a shell-contact selector
statement, and the Ca/Fe witness rejects A-only and N/Z-only scalar promotion.
-/
theorem nuclear_shell_contact_src_closure :
    degeneracy f7_2 = 8 /\
      sameShellContact ca48Valence f7_2 = 0 /\
      sameShellContact fe54Valence f7_2 = 6 /\
      massDeltaFe54Ca48 < massDeltaCa48Ca40 /\
      neutronExcessFe54 < neutronExcessCa48 := by
  native_decide

end D0.Matter
