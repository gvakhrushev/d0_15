# D0 v15 Higgs Scalar Projector Proof (constructive)

## Definitions

Frozen scalar doublet subcarrier: ℋ_ϕ ≅ ℂ² with inclusion ι_ϕ : ℂ² ↪ ℋ_matter.

Frozen SU(2)-like generators on the doublet:

X = [[0,1],[1,0]]

Z = [[1,0],[0,-1]]

Scalar projector: P_ϕ = ι_ϕ I₂ ι_ϕ^†

## Theorem Statement

If P is a positive idempotent on the frozen scalar doublet block and [P, X]=0 , [P, Z]=0 , then P = a I₂ .

If additionally P²=P and P≠0 , then P=I₂ and rank(P)=2 .

The nonzero gauge-compatible scalar projector is uniquely the rank-2 doublet projector.

Multiplicity rule: On full carrier with multiple copies, commutant is I₂⊗A ; rank-2 uniqueness requires the frozen scalar subcarrier or explicit multiplicity selector frozen first.

## Proof

Algebraic/numeric coefficient argument:

Let P = [[a,b],[c,d]] .

[P,Z]=0 ⇒ b=c=0 (off-diagonals vanish).

[P,X]=0 ⇒ a=d .

Thus P = a I₂ .

Idempotence: a²=a ⇒ a∈{0,1} .

Nonzero ⇒ a=1 ⇒ P = I₂ , rank=2 , self-adjoint, commutes with X/Z .

Explicit construction: P_ϕ = eye(2) satisfies all.

## Negative Controls

Rank-1 projectors (P0=[[1,0],[0,0]], P1=[[0,0],[0,1]], P+ = 1/2 [[1,1],[1,1]]) break commutation with X or Z .

Rank>2 requires extra multiplicity selector (would introduce additional scalar DOF).

Second mass anchor for Yukawa is forbidden.

## Cert Tokens (from 05_CERTS/vp_higgs_scalar_projector_constructive.py)

PASS_HIGGS_SCALAR_PROJECTOR_RANK_TWO

PASS_HIGGS_SCALAR_PROJECTOR_IDEMPOTENT

PASS_HIGGS_SCALAR_PROJECTOR_SELF_ADJOINT

PASS_HIGGS_SCALAR_PROJECTOR_COMMUTES_FROZEN_SU2_XZ

PASS_FROZEN_SU2_XZ_COMMUTANT_SCALAR

PASS_NONZERO_IDEMPOTENT_FORCES_IDENTITY_DOUBLET

PASS_YUKAWA_SECTION_NO_SECOND_MASS_ANCHOR

PASS_SINGLE_ACTION_SECTION_PRESERVED

(and the four expected FAIL_* negative controls)

## Book Patch Text (for Book 04 / 05)

The legacy Higgs/scalar projector no-go is resolved by the certified FrozenSU2-compatible rank-2 scalar projector (P_ϕ = I₂).

The remaining Yukawa work is numerical transfer/passport, not scalar-projector construction.

In Book 05: add SCALAR-PROJECTOR-CERT-CLOSED (finite rank-2 scalar projector exists, unique on frozen doublet, commutes with FrozenSU2_X/Z, preserves single-section discipline).

Forbidden: rank-1 promoted to Higgs doublet; rank>2 without multiplicity selector; commutant applied without frozen doublet; Yukawa introducing second mass anchor.
