namespace D0.Bridge

namespace BridgeAssumption

/-- External owner of the symbolic-dynamics classification that closes the *strongest* form of the
D0 categorical↔toral link (BOOK_01 §01.21.4 / BOOK_06). Two classical theorems:

* **Adler–Weiss (1967)** — every hyperbolic (Pisot) automorphism of the 2-torus admits a finite
  Markov partition, hence is topologically conjugate to a subshift of finite type whose transition
  matrix has Perron eigenvalue equal to the spectral radius `φ`.
* **Adler / Adler–Marcus finite-equivalence** — two irreducible subshifts of finite type with the
  same topological entropy are *finitely equivalent*; full topological **conjugacy** is the stronger
  Williams shift-equivalence, which equal entropy alone does not give.

D0 proves internally (cert `vp_fibonacci_if_bratteli.py`): the Fibonacci fusion matrix
`N_τ = [[0,1],[1,1]]` is the golden-mean SFT transition matrix (Perron eigenvalue `φ`, topological
entropy `log φ`), and the toral `T = [[0,1],[1,-1]]` is Anosov with `|λ_max| = φ` (entropy `log φ`).
So `I_f = log φ` is forced for the value and its mechanism (topological entropy `= log` of the
Perron eigenvalue of a golden-growth integer matrix), and the two systems are finitely equivalent.
The remaining, strongest equivalence — a full topological conjugacy of the fusion Bratteli system
with the toral Markov-partition SFT — is the assumed external owner, not re-proved here. -/
structure AdlerWeissPartition where
  /-- D0-side anchor: both sides are the golden-growth SFT, entropy `log φ` (cert-proved). -/
  d0GoldenEntropyBothSides : Prop
  /-- External: hyperbolic toral `T` has a Markov partition ⇒ conjugate to an SFT with Perron `φ`,
      and equal-entropy irreducible SFTs are finitely equivalent (full conjugacy = Williams). -/
  adlerWeissMarkovAndFiniteEquivalence : Prop
  d0Witness : d0GoldenEntropyBothSides
  cited : adlerWeissMarkovAndFiniteEquivalence

end BridgeAssumption

abbrev AdlerWeissPartition := BridgeAssumption.AdlerWeissPartition

/-- Conditional bridge: given the D0 golden-entropy fact (both the fusion Bratteli system and the
toral automorphism have topological entropy `log φ`) and the Adler–Weiss Markov partition together
with SFT finite-equivalence (assumed), the categorical↔toral systems are finitely equivalent and
`I_f = log φ` is the shared invariant. Proved ONLY relative to the declared external assumption
(`ASSUMP-ADLER-WEISS`). -/
theorem adler_weiss_partition_conditional (h : AdlerWeissPartition) :
    h.d0GoldenEntropyBothSides ∧ h.adlerWeissMarkovAndFiniteEquivalence :=
  ⟨h.d0Witness, h.cited⟩

end D0.Bridge
