# E-LOR — Typed Lorentz Continuum Owner

CONTROL disposition: **ACCEPT AS RESEARCH / PROP-BUNDLE-NOT-OBJECT-BRIDGE-OPEN**  
Source memo: `MEMO_21_LORENTZ_CONTINUUM_TYPED_OWNER.md`

## Exact result

The current continuum-facing Lean bridge structures are proposition-registration shells.

Examples:

- `RieffelGHPContinuum` stores proposition fields and proofs;
- `ConnesReconstruction` stores proposition fields and proofs;
- `CovarianceSystem` stores proposition fields and proofs;
- `HeatTraceWeylAssumptions` stores independent propositions for convergence, four-dimensional Weyl behaviour and Lorentz signature;
- `LorentzBridgeAssumptions` stores proposition fields for a macro limit and spin-cover integration.

They do not construct one typed object
[
(M,g)
]
with (M) a smooth connected four-manifold and (g) a smooth Lorentz metric of signature ((1,3)).

No audited owner returns:

- a smooth manifold type with chart/tangent structure;
- a Lorentz metric section on that manifold;
- dimension four and signature ((1,3)) as predicates of the same object;
- a finite-stage point map (X_N	o M);
- a cochain/field reconstruction map;
- a finite response to smooth (S^2T^*M) map;
- a concrete gravity-operator convergence theorem.

## Positive finite structure

D0 does own real finite objects:

- `ArchiveRolePhasePoint n` with cardinality ((n+2)^4);
- finite refinement projections;
- a finite normalized phase metric;
- the 4D role-product Laplacian;
- generic complete-pseudometric Cauchy/convergence theorems.

These are not yet joined to one smooth Lorentz target.

## Separate finite-side blocker

The accepted scene gravity carrier
[
K_+=\ker B_+\subset SceneC1
]
is a fixed 326-dimensional carrier of the single (K(9,11,13)) scene.

The actual archive refinement tower uses `ArchiveRolePhasePoint n` / `ArchivePoints n`.

No typed (K_{+,N}), `SceneC1` refinement tower, or theorem relating the fixed scene carrier to the archive role-phase tower is currently owned.

## Minimum positive passport

A future positive owner must carry actual data, schematically:
[
(M,g_L,\iota_N,K_N,E_N,
R_N^{field},S_N^{field},R_N^{resp},
\mathcal E,\text{convergence})
]
under explicit BRIDGE/PASSPORT assumptions.

It must not return only a conjunction of propositions.

The earliest failure is object reification, hence the terminal verdict:
[
\boxed{\texttt{PROP-BUNDLE-NOT-OBJECT-BRIDGE-OPEN}}.
]
