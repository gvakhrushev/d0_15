# D0 → GR: the original Lorentz Hodge insertion is the grade-two part of the OWNED CAR16 four-role word

**20 October 2026 | EXACT FINITE ALGEBRAIC CARRIER WELD | Research on existing scientific PR #334.**
No new fundamental action, CAR mode, arbitrary gamma representation, Role metric, Einstein tensor, Book-source selector or CORE claim. GR_closed=false.

## 0. The actual missing interface

The original finite six-based-face A4D Palatini action already has a *nonzero exact Einstein metric response* after solving its independent 24 Lorentz-link equations, e.g. the original owned mixed 40-row Cartan theorem. The still-unproved physical step is deriving that SAME geometric action/source as the selected complete native Book Cost−Info/ordered-memory execution. This memo does not assert that missing selection.

We can, however, remove an intermediate **carrier-level** ambiguity: where does the orientation-odd bivector/Hodge insertion inside the original finite Palatini action live relative to the D0 CAR16 record algebra?

Exact existing inputs:
- D0.Geometry.ArchiveCARRelations: four CAR modes in deterministic Role order (A,B,C,D), Jordan–Wigner signs; c_r and c_r† on the ORIGINAL 16-state Fock carrier.
- D0.Geometry.ArchiveCARDirac.fockGamma: gamma_r=c_r+c_r†, a self-adjoint real 16×16 OWNED matrix, not an introduced Dirac gamma.
- D0.Geometry.ArchiveCARFockCarrier: Fock states indexed by subsets of four Roles.
- Original Lorentz metric eta=diag(1,−1,−1,−1) and the EXACT CONTROL owner MEMO_A4D_AFFINE_CONJUGACY_ROLE_BIVECTOR_INSERTION_AUDIT, section 5: the explicit six-dimensional Role-bivector Hodge J with J²=−I and the 2D proper-Lorentz commutant span{I,J}.
- Original finite Palatini action and all40 source: A4D_DOUBLE_NULL_EXACT_FINITE_QUADRATIC_CARTAN_EINSTEIN_BOOTSTRAP_2026_10_19.

## 1. The canonical four-Majorana word selects degree 2

On the original 16-state Fock basis |S>, S⊂{A,B,C,D}, define

    gamma_r = c_r+c_r†,
    Gamma = gamma_A gamma_B gamma_C gamma_D.

The CAR relations imply gamma_r²=I, gamma_r gamma_s=−gamma_s gamma_r for r≠s, and Gamma²=I. More concretely, in the OWNED Jordan–Wigner representation,

    Gamma |S> = ± |{A,B,C,D}\S>.

Thus Gamma maps degree k to degree 4−k. **The only Fock sector individually preserved by this word at fixed number k is k=2**, the ORIGINAL 6D space Λ²Role. No extra six-dimensional matter/vector space is selected; the two-particle sector is singled out by the same four-role word and preservation of degree. This does NOT say that the original physical apparatus is compelled to insert Gamma.

Let P₂ be the projector onto that degree-two sector, with the ordered basis (AB,AC,AD,BC,BD,CD). Let M_eta be the *already given Lorentz metric* on the same bivectors:

    M_eta = diag(eta_A eta_B, eta_A eta_C, eta_A eta_D,
                 eta_B eta_C, eta_B eta_D, eta_C eta_D)
          = diag(−1,−1,−1,+1,+1,+1).

Define B=P₂ Gamma P₂ and J_CAR=B M_eta.

**NEW exact original-owner identity (all 36 entries):**

    J_CAR =
      [0 0 0 0 0 −1;
       0 0 0 0 1  0;
       0 0 0 −1 0 0;
       0 0 1 0 0 0;
       0 −1 0 0 0 0;
       1 0 0 0 0 0]
      = J_owned(Role bivector).

Moreover B²=I, J_CAR²=−I and J_CAR^T=−J_CAR, **exact integer arithmetic**.

Negative control: using B alone gives B²=+I, hence the *Euclidean*, not Lorentzian, Hodge character. The eta raising matrix is load-bearing, not decoration or a freely chosen phase.

## 2. Orientation-odd Role control and uniqueness on the owned 6D carrier

Let U₂ be the SIGNED exterior/Fock lift of the odd spacelike Role transposition B↔C. Its fermionic occupied-basis sign is essential. Direct exact computation gives

    U₂ J_CAR U₂^T = −J_CAR.

CONTROL had independently certified that the commutant of the proper Lorentz action on Λ²Role is precisely span{I,J_owned}, with dimension TWO, while an odd Role swap reverses J. Consequently, **conditional on selecting a nonzero proper-Lorentz-equivariant, orientation-odd linear bivector insertion**, the insertion is uniquely proportional to this J. The normalization and exact matrix are supplied by the existing CAR word and eta; a global orientation sign remains a convention. Nothing here proves Book03 chooses orientation-odd rather than orientation-even insertion, or that the requisite signed detector is physically executed.

## 3. Independent 256-entry chirality trace equals the oriented Palatini epsilon

For the same ORIGINAL real CAR generators and Gamma, for EVERY a,b,c,d ∈ {A,B,C,D}, including repeated roles,

    (1/16) Tr_CAR16(Gamma gamma_a gamma_b gamma_c gamma_d)
      = epsilon_abcd,

where epsilon_ABCD=+1, sign under permutations and zero on repeated indices. This is an EXACT 256-case integer result, not a fit or normal-chart limit. Proof: gamma product toggles precisely its letters; a Fock basis state contributes to the trace only when each of the four modes is toggled once. The product sign is then the parity of its permutation, and all sixteen Fock basis states contribute identically.

For proper Lorentz signature, form the complex Clifford basis **within the complexification of the same CAR16**:

    tilde_gamma_A=gamma_A, tilde_gamma_(B,C,D)=i gamma_(B,C,D),
    Gamma_5=i tilde_gamma_A tilde_gamma_B tilde_gamma_C tilde_gamma_D
           =Gamma.

Then the invariant oriented contraction in the declared Lorentz coframe is

    (i/16) Tr_CAR16(
       Gamma_5 tilde_gamma_a tilde_gamma_b
               tilde_gamma_c tilde_gamma_d)
        = epsilon_abcd.

Consequently, for any coframe legs e_r,e_s and antisymmetric proper-Lorentz bivector curvature F_rs^{cd},

    epsilon_abcd e_r^a e_s^b F_rs^{cd}
    =
    (i/16) Tr_CAR16 [
       Gamma_5 gammaL(e_r) gammaL(e_s)
       (sum_cd F_rs^{cd} tilde_gamma_c tilde_gamma_d)
    ].

The right-hand side uses no externally postulated Levi-Civita tensor: its orientation comes from the ordered four native CAR modes. The numerical normalization 1/16 is fixed by the original Fock dimension. Index-lowering and the factor 1/2 of the usual antisymmetric spin representation must be kept when translating this identity into a particular component convention; the displayed formula deliberately uses the FULL ordered sum over c,d.

This is an oriented *algebraic contraction identity*, not a statement that a trace by itself is the physically selected scalar Book action. Ordinary unweighted scalar trace does not reproduce the epsilon insertion.

## 4. Exact reuse of the ALREADY-OWNED original finite Palatini action

On every original finite based face, the existing Palatini action uses its independently defined proper-Lorentz curvature and internal six-dimensional Hodge star. Because the matrix J_CAR is LITERALLY J_owned in the original basis, substituting

    star_owned ≡ (P₂ gamma_A gamma_B gamma_C gamma_D P₂) M_eta

rewrites the same original six-face action WITHOUT changing its value, any of the 16 coframe Euler derivatives, any of the 24 independent connection Euler derivatives, or the already-owned nonlinear mixed Einstein-response identities. This is a **carrier realization**, not a newly invented action or a proof of physical Book source equality.

The substantive gain is a precise original-carrier route:

    ORIGINAL four CAR modes → canonical degree-two invariant sector (dim6)
    → ORIGINAL Lorentz Hodge J → EXISTING finite Palatini curvature insertion.

The remaining source/physical gate becomes sharper: demonstrate that a real, complete, paid original Book03 ordered-memory programme takes the necessary *chirality-saturated* trace, keeps its full retained records and all failure/clock/preparation costs, and agrees on the same admitted variations with the complete geometric 16+24+matter equations. An arbitrary insertion of Gamma, the target Einstein tensor, or a fitted coefficient does NOT meet this gate.

## 5. Decisive controls and status

The standalone dependency-free checker in sources/d0_car16_hodge_palatinian_2026-10-20/check_original_car16_hodge.mjs performs:
- all 16 original Fock basis transformations with exact Jordan–Wigner signs;
- the 256 exact four-index chirality trace identities;
- all 36 entries of the existing Role-bivector Hodge matrix;
- B²=I and J²=−I (explicit signature control);
- signed B↔C Role transposition and J→−J;
- a nonzero oriented Palatini contraction reconstructed by the normalized CAR trace.

Independent JS integer tests were executed and passed on the same formulas. This document does not assert a remote CI or Lean build of the NEW checker; the consumed original Lean owners are separate.

**GR_closed=false. No PR/BOOK/CORE promotion, no actual native Book trace selector, no full128 execution mapping, no moving physical input or raw #216 closure.**