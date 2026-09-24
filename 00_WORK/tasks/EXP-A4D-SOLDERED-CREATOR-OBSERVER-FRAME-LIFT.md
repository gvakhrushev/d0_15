# EXP-A4D-SOLDERED-CREATOR-OBSERVER-FRAME-LIFT

## Class

EXPENSIVE / BREAKTHROUGH CONSTRUCTIVE RESEARCH

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

IN_PROGRESS

## Baseline

Repository:

`https://github.com/gvakhrushev/d0_15`

Minimum baseline:

`c45e6c94759b2d52efdfbe28065038f1bfe60474`

Use newer `origin/main` if available.

## Research source

Read fully:

`MEMO_A4D_LOCATED_METRIC_STAR_CELL_ACTION_SELECTOR`.

Primary frozen terminal from that memo:

```text
SOLDERED-CREATOR-FRAME-LIFT-PRIMITIVE-REQUIRED
```

Do not repeat its located-star, Nyquist, corner, boost, shell or reverse-locality calculations except as controls.

## Frozen facts

Treat as research input:

1. The center-matched two-color topological placement is
   [
   F_{PD}(x,S)=(x-1_{S^c},S^c),
   qquad
   F_{DP}(y,T)=(y+1_T,T^c).
   ]
2. The complement commutes with Fock parity in 4D.
3. Independent dual incidence gives the degree-signed primal/dual intertwiner.
4. The reference cell laws
   [
   W_1=I+H+M_q,qquad W_2=I+H+2M_q
   ]
   share the same full first jet and fail the naive positive-counting Lorentz boost test.
5. A pointwise Lorentz exterior star has the correct signature square but cannot reproduce the off-site staggered first jet and does not equal the flat counting form.
6. If both forward and reverse scalar stars are uniformly local and their exact composition is a scalar sign, the accepted neighboring scalar first jet is impossible. Do not attempt to repair this by changing only the nonlinear diagonal `q`.
7. The first unowned constructive package is a local frame lift of the CAR/exterior fiber, moving creators/annihilators and compatible neighboring transport.

## Newly merged owners to consume

PR #69 owns the constitutive nonselection baseline: the radius-one Ward class, polynomial nonlinear nonselection, determinant-density freedom and metric-compatibility nonuniqueness.

PR #70 owns the affine Cartan background/link package: affine node gauge, exact flat translation gauge equal to `forwardGaugeCoframe`, affine path transport, open curvature/torsion, based holonomy, uniform-radius Lie-closure no-go and factorized-local resource accounting.

Therefore the neighboring-transport phase must first test whether the LINEAR PART of the owned affine link can be lifted by the exterior representation `rho` onto the existing Fock carrier. Do not introduce a second connection carrier until this possibility is exhausted.

For a Lorentz-subgroup affine link, the natural candidate is `T_CAR = rho((A_xy).lin)`. Test creator covariance directly. The affine translation part acts on solder/coframe placement; it does not automatically act on the exterior fiber.

## New coordinator observation: observer Euclideanization

Let `V=ℝ^Role` with Lorentz form `η=diag(+---)`.

For a unit future/timelike vector `n` with

[
η(n,n)=1,
]

define

[
oxed{
h_n(v,w)=-η(v,w)+2η(v,n)η(w,n).
}
]

Research starting facts to verify formally:

- `h_n` is positive definite on real `V`;
- for the reference observer `n_0=e_A`,
  [
  h_{n_0}=I
  ]
  in the Role basis, exactly reproducing the flat counting one-form metric;
- for every Lorentz transformation `Λ`,
  [
  h_{Λn}(Λv,Λw)=h_n(v,w).
  ]

For the rational A/B boost

[
Λ=
egin{pmatrix}
5/4&3/4\\
3/4&5/4
end{pmatrix},
]

[
n_0=(1,0)
mapsto
n'=(5/4,3/4),
]

and the transformed positive form is

[
h_{n'}=
egin{pmatrix}
17/8&-15/8\\
-15/8&17/8
end{pmatrix},
]

with

[
Λ^T h_{n'}Λ=I.
]

This shows that positive flat counting normalization and Lorentz covariance are compatible if the observer transforms; `I` itself is not claimed Lorentz invariant.

Verify and generalize this before any all-order archive construction.

## Primary objective

Construct or terminally exclude a **sitewise Lorentz-frame-covariant exterior/CAR lift** on the existing 16-state carrier such that:

1. sites remain fixed under internal frame transformations;
2. the exterior/CAR fiber transforms by an independently defined lift `ρ_x`;
3. soldered creators and annihilators transform tensorially;
4. neighboring links transform as
   [
   T'_{xy}=ρ_yT_{xy}ρ_x^{-1};
   ]
5. the observer-dependent positive form `h_n` has flat gauge `I`;
6. the resulting finite local energy can reproduce the complete staggered first jet `H(e)`, including Nyquist and the distance-two corner.

Do not select a nonlinear cell law before this frame lift exists.

## Phase A — exterior representation on ArchiveFockState

Identify the existing subset/Fock basis with the exterior basis of `Λ^*V` without introducing a new 16-state carrier.

For arbitrary invertible `Λ:V→V`, construct the degree-preserving exterior lift

[
ρ(Λ)=igoplus_{k=0}^4 wedge^k Λ
]

using exact minors/determinants in the subset basis.

Prove:

[
ρ(Λ_1Λ_2)=ρ(Λ_1)ρ(Λ_2),
qquad
ρ(I)=I.
]

This is the exterior representation. Do NOT call it a Dirac-spinor representation.

Do not use `Spin(1,3)` unless a separate Clifford-spinor submodule is actually constructed.

## Phase B — algebraic creators and contractions

For `v∈V` define

[
c^dagger(v)=sum_a v^a c_a^dagger.
]

For `α∈V^*` define

[
c(α)=sum_a α_a c_a.
]

Prove:

[
{c(α),c^dagger(v)}=α(v),
]

and the frame laws:

[
ρ(Λ)c^dagger(v)ρ(Λ)^{-1}=c^dagger(Λv),
]

[
ρ(Λ)c(α)ρ(Λ)^{-1}=c(Λ^{-ee}α).
]

Keep algebraic dual contraction separate from any positive adjoint.

## Phase C — observer-positive adjoint

Use `h_n` to identify vectors and covectors and define the observer-dependent positive Fock pairing induced on all exterior degrees.

At the reference observer `n_0=e_A`, prove this exterior pairing is exactly the existing counting pairing on the subset basis.

Determine the observer-dependent adjoint relation between creation and annihilation.

Under simultaneous:

[
Λ,quad nmapsto Λn,quad ψmapsto ρ(Λ)ψ,
]

prove the positive exterior pairing is invariant.

This is covariance of a family of positive forms, not invariance of the fixed counting form.

## Phase D — local sitewise frame action

For `Λ:X_N→O(1,3)`, define:

[
(Q_Λψ)(x)=ρ(Λ_x)ψ(x).
]

No archive site permutation or map `x↦Λx` is allowed for continuous Lorentz frames.

Classify how the uncentered coframe/solder components transform so this agrees with the existing right Lorentz action on the solder matrix.

Resolve vector/covector conventions explicitly.

## Phase E — soldered creators

Given the local uncentered/soldered leg associated with archive direction `r`, define a moving creator

[
C_r^dagger(e,x)
]

as creation by the appropriate local frame vector/covector.

Construct the corresponding contraction/annihilation.

Required transformation law:

[
Q_Λ C_r^dagger(e,x)Q_Λ^{-1}
=
C_r^dagger(e^Λ,x)
]

with the correctly transformed local data.

Do not define `e^Λ` merely by demanding this identity.

## Phase F — neighboring transport

For a link `T_{xy}` acting on the same exterior/CAR fiber, require or derive:

[
T_{xy}c^dagger(v)T_{xy}^{-1}
=
c^dagger(L_{xy}v)
]

for the underlying frame-vector transport `L_{xy}`.

Under local frame change prove:

[
T'_{xy}=ρ_yT_{xy}ρ_x^{-1}.
]

Audit whether existing `ArchiveChainConnection` / `ArchiveCovariantCubicalDifferential` can instantiate this or only treat an independent coefficient fiber.

The earlier fixed-creator `dConn` theorem must not be silently promoted to rotating-CAR covariance.

## Phase G — covariant finite differential candidate

Construct the strongest honest first-order operator from:

- archive shifts;
- moving creators/contractions;
- frame-compatible links;
- uncentered local geometry.

Its flat limit must be the existing `d,d^dagger,D_H`.

Derive its exact local frame transformation law.

Do not require nilpotency in curved geometry unless curvature vanishes.

## Phase H — reproduce the accepted H(e)

Linearize the candidate at:

[
e=0,quad n=n_0,quad T=I.
]

Test whether its induced quadratic positive energy has first variation exactly:

[
H(e)=
sum_r B_r(e_r{}^r)I
-sum_{s,r}
left(
M_{e_s{}^r}U_sA_rE_{sr}
+
E_{rs}A_r^*U_s^{-1}M_{e_s{}^r}
ight).
]

This must include:

- the endpoint half-average;
- the off-site scalar hop;
- the `s-r` corner;
- all degree blocks.

If it misses any term, identify the minimal additional half-edge/common-center transport required.

## Phase I — Nyquist

At `L=2`, the construction must use enough uncentered data to retain the one-form Nyquist response invisible to centered `Θ`.

If the proposed frame lift factors only through centered solder/Gram, reject it.

## Phase J — rational boost

Repeat the exact A/B boost, now transforming:

- the observer `n`;
- the matter exterior fiber;
- the solder/coframe;
- links if nontrivial.

The observer-positive flat form must pass exactly.

Then test the first-order staggered energy, not the old fixed-counting congruence.

Distinguish:

- a covariant family `h_n`;
- an invariant Lorentzian action;
- a gauge-fixed positive Hamiltonian.

## Phase K — Lorentzian versus positive forms

Construct and compare two bilinear structures:

1. the Lorentzian exterior form induced from `η`;
2. the positive observer form induced from `h_n`.

Determine which one should enter:

- the covariant spacetime action;
- the positive Hamiltonian/counting energy;
- the definition of annihilator adjoints;
- the located primal/dual Riesz map.

Do not force them to be the same.

## Phase L — relation to located J

Keep the topological located complement `J` fixed.

Determine whether the frame lift commutes/pseudocommutes with `J` after the orientation line is treated correctly.

Do not redefine placement.

The metric/observer structure may weight the pairing but must not change the cell anchor without a new theorem.

## Phase M — relation to nonlinear Q

Only after a frame-covariant seed reproducing `H(e)` exists, revisit nonlinear laws.

The conditional scalar-deformation theorem remains hostile:

[
E_cmapsto(1+λz_c)E_c,
quad z_c(0)=Dz_c(0)=0.
]

Frame covariance alone need not select the all-order material coefficient.

If the frame lift itself determines an energy coefficient/measure law, state it explicitly.

## Phase N — connection and curvature

Once the same CAR fiber is transported, derive how primal and dual pairing-compatible links relate.

For `J:P→D^*`, use the contragredient law, not an unjustified similarity:

[
T_D=J_y^{-T}T_P^{-T}J_x^T
]

in compatible bases.

Determine the induced curvature relation.

## Required direct answers

1. Is `ArchiveFockState` sufficient as the exterior Lorentz carrier?
2. What is the exact arbitrary-`Λ` exterior lift?
3. Is any spinor representation needed?
4. Does `h_n` reconcile flat counting with Lorentz covariance?
5. Can `n=e_A` be treated only as a reference observer gauge rather than a physical time theorem?
6. What is the exact local transformation law of uncentered `e`?
7. Can moving creators be defined on the existing carrier?
8. What link compatibility do they require?
9. Does the existing connection API satisfy it?
10. Can the complete `H(e)` be recovered as the first variation?
11. Where does the half-average arise?
12. Where does the `s-r` corner arise?
13. Does the construction pass `L=2` Nyquist?
14. Does it pass the rational boost when `n` is transformed?
15. Is the positive energy observer-dependent?
16. Can a Lorentzian covariant action remain observer-free?
17. Is the located `J` unchanged?
18. What primitive remains before selecting nonlinear `Q`?

## Exact controls

Mandatory:

- arbitrary exterior degree `0..4`;
- all four fixed creators at `Λ=I`;
- a nontrivial Role permutation;
- rational A/B Lorentz boost;
- `n=e_A` gives `h_n=I`;
- transformed observer gives `Λ^T h_{Λn}Λ=h_n`;
- `L=2` Nyquist;
- `L=3` corner;
- flat `D_H`;
- at least one nontrivial link/frame pair.

## Terminal menu

Return ONE:

```text
OBSERVER-COVARIANT-SOLDERED-CAR-LIFT-CONSTRUCTED
FRAME-LIFT-CONSTRUCTED-STAGGERED-JET-MISSING
SOLDERED-CREATOR-TRANSPORT-PRIMITIVE-REQUIRED
OBSERVER-POSITIVE-HAMILTONIAN-PRIMITIVE-REQUIRED
ROTATING-CAR-LINK-COMPATIBILITY-NOGO
```

## Deliverable

Produce:

`MEMO_A4D_SOLDERED_CREATOR_OBSERVER_FRAME_LIFT.md`

with theorem-ready Lean handoff.

Do not finish by selecting a nonlinear `Q` unless the frame construction itself proves that selection.
