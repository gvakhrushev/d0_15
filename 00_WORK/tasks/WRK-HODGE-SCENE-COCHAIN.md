# WRK-HODGE-SCENE-COCHAIN

## Class
WORKER

## Objective
Reimplement the literal $K(9,11,13)$ scene cochain complex and finite Hodge decomposition on current main using existing topology owners without overclaiming physical identification.

## Scope
1. Inspect current `D0.Topology.*` and reuse existing `boundary2R`, Hodge spectrum, and simplicial complex definitions.
2. Formalize the canonical discrete cochain complex $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ on the unit scene with verified incidence maps.
3. Prove $d_1 d_0 = 0$ (coboundary squared zero) and the finite Hodge orthogonal decomposition $\ker(d_1) = \text{im}(d_0) \oplus \mathcal{H}^1$.
4. **Boundary:** Do not introduce physical Hamiltonian, TT dynamics, or matter-gravity identification beyond what is mathematically proved.

## Source Payload
- Local `SceneCochainComplex.lean`
- Local `SceneHodgeDecomposition.lean`
- Local `PhysicalCarrierInventory.lean`

## Affected Claims
- `D0-HODGE-001`
- `D0-CARRIER-CENSUS-001`
- `D0-HODGE-THREE-LEVEL-SPECTRUM-001`
- `D0-HODGE-LINKS-001`

## Exit Condition
The literal K(9,11,13) scene cochain complex and the honestly supported finite Hodge decomposition from the local payload are reimplemented on current main using existing topology owners where possible; actual incidence maps replace declared dimension constants where supported; d₁d₂=0 and claimed decomposition facts build in Lean; no physical Hamiltonian, TT dynamics, or matter-gravity identification is promoted beyond what is proved.
