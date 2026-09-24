# WRK-A4D-LOCATED-PRIMAL-DUAL-STAR

## Class

WORKER / FORMALIZATION

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

READY NOW when a WORKER slot is assigned.

Do not wait for the flux-energy worker merely to formalize placement/topological duality.

If the flux worker's algebraic complementary pairing API has merged, reuse it. If it has not merged, formalize only the colored carriers, placement, orientation, independent dual incidence and topological star. Do not create a competing public algebraic-pairing API; leave the later bridge as a thin integration theorem.

Use current `main` at launch.
## Objective

Lean-own the reference located primal/dual complement already established at research level.

This task formalizes WHERE the existing CAR/Fock complement lives.

It does NOT select a nonlinear energy law.

## Frozen geometry

For cell label `S : ArchiveFockState`, use complement `Sᶜ`.

Reference placement:

[
F_{PD}(x,S)=(x-1_{S^c},S^c),
]

reverse:

[
F_{DP}(y,T)=(y+1_T,T^c).
]

Treat primal and dual as distinct colors/types.

Do not collapse them into one carrier.

## Main modules

Suggested:

```text
D0/Geometry/A4DLocatedPrimalDualCell.lean
D0/Geometry/A4DLocatedTopologicalStar.lean
```

Reuse Package A from the flux-energy worker wherever possible.

Do not duplicate the algebraic complement pairing under a new incompatible API.

## Package A — colored cell carriers

Define typed primal and dual cell labels over the existing:

`ArchiveRolePhaseGroup N × ArchiveFockState`.

Provide explicit conversions only where mathematically justified.

No cardinality-only equivalences.

## Package B — subset indicator translation

Define the site displacement:

[
1_S=\sum_{r\in S}e_r
]

using existing Role translations.

Prove complement identities required by the placement maps.

## Package C — center-matched placements

Define:

```text
locatedPrimalToDual
locatedDualToPrimal
```

with the formulas above.

Prove:

```text
locatedDualToPrimal_leftInverse
locatedDualToPrimal_rightInverse
```

for every `L=N+2`, including `L=2`.

No division by 2 in `ZMod L`.

If a doubled-center carrier is introduced, keep it a reference-coordinate construction and do not call it archive refinement.

## Package D — degree complement

Prove:

[
\deg(S^c)=4-\deg(S).
]

In particular, because 4 is even:

[
(-1)^{|S^c|}=(-1)^{|S|}.
]

Capstone:

`locatedStar_commutes_fockParity`.

Do NOT claim anticommutation.

The odd operator is `D_H`, not the 4D complement.

## Package E — orientation sign

Reuse existing ordered Role/CAR sign machinery.

Define the complement orientation sign `epsilon(S)`.

Prove:

[
\epsilon(S)\epsilon(S^c)=(-1)^{|S|(4-|S|)}.
]

## Package F — located topological star

Define the signed two-color map:

[
\star_{PD}|x,S\rangle
=
\epsilon(S)|x-1_{S^c},S^c\rangle.
]

Define the reverse star with the compatible sign.

Prove:

[
\star_{DP}\star_{PD}
=
(-1)^{k(4-k)}I
]

on homogeneous degree `k`.

No residual translation is allowed.

## Package G — independent dual incidence

Define the dual cubical differential independently with positive Role directions.

Do NOT define it by conjugating the primal differential through the star.

Prove the typed incidence theorem:

[
J_{k+1}d_P^k
=
(-1)^{k+1}(d_D^{3-k})^\vee J_k.
]

The converse classification should recover:

[
a(S\cup\{r\})=a(S)+r,
]

and therefore:

[
a(S)=c+1_S
]

within the stated translation-placement class.

If the full classification is expensive, the forward implication and center-matched instance are mandatory.

## Package H — Role permutation orientation law

Under `Perm Role`, prove the correct pseudoequivariance:

[
JQ_\sigma
=
\operatorname{sgn}(\sigma)Q_\sigma J
]

when ambient orientation is fixed.

For orientation-preserving permutations, give the strict specialization.

Do not incorrectly assert strict signed equivariance for all 24 permutations with a fixed orientation line.

## Package I — flat Dirac compatibility

Show that the located star transports the primal differential to the independently defined dual differential in the precise typed sense above.

Do not define a second same-color Dirac.

Do not claim a new spectrum.

Where easy, prove kernel/shell transport consequences only as transported eigenspaces after the relevant dual operator is typed.


## Package J — counting adjoint and chirality conjugacy

After the independently defined incidence theorem, identify dual functionals with dual cochains ONLY through the counting Riesz map.

Derive the degree-signed counting-adjoint relation:

[
J_{k-1}(d_P^{k-1})^\dagger
=
(-1)^k d_D^{4-k}J_k.
]

Then define the dual-degree chirality sign

[
\chi|_{D^\ell}=(-1)^{\ell(\ell-1)/2}I
]

and prove the correctly signed Dirac conjugacy:

[
J D_P J^{-1}=\chi D_D\chi^{-1}.
]

Do NOT simplify this to `J D_P J⁻¹=D_D` under the present incidence conventions.

This theorem transports the flat spectrum; it does not create a new spectrum, mass, or physical metric Hodge.


## Truth boundaries

Do NOT claim:

- physical metric Hodge;
- Lorentzian double-star sign `q=3`;
- nonlinear constitutive energy selection;
- BOOK `F_N`;
- physical time;
- scene-to-shell embedding;
- mass generation.

This task owns placement/topological duality only.

## Required controls

- `L=2` inverse placement;
- `L=3`;
- `L=5`;
- degree 0 through 4;
- parity;
- all 24 Role permutations;
- at least one odd permutation sign;
- independent dual incidence.

## Expected primary verdict

```text
REFERENCE-LOCATED-PRIMAL-DUAL-STAR-OWNED
```

Secondary:

```text
CENTER-MATCHED-DUAL-PLACEMENT-OWNED
LOCATED-STAR-INCIDENCE-INTERTWINER-OWNED
LOCATED-STAR-TOPOLOGICAL-SQUARE-OWNED
LOCATED-STAR-PARITY-EVEN
S4-ORIENTATION-PSEUDOEQUIVARIANCE-OWNED
```

Retain:

```text
LOCATED-DUAL-PAIRING-FIXED-NONLINEAR-CELL-ENERGY-LAW-MISSING
```

## Validation / lifecycle

Use narrow builds during work.

Before PR:

```bash
lake build D0.All
python3 03_FORMALIZATION/tools/check_no_sorry_in_core.py --all-modules
python3 tools/validate_repo.py
python3 tools/validate_work.py
python3 tools/generate_lean_views.py --check
git diff --check
```

One branch, one PR, no self-merge, no CI watcher.
