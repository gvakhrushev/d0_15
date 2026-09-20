# Level-II Worker Queue after Truth Repair #1

Date: 2026-09-20

This queue is for normal worker agents. They may inspect/update the repository and implement Lean/Python.
The expensive research-only agent receives the separate A1 brief and should not be used for these tasks.

## Priority rule

Workers may continue in parallel. A worker task is accepted only if its final registry note can be copied
verbatim from the literal exported theorem proposition.

## W-B1 — Replace Fin 3 bookkeeping by explicit family subspaces

Branch: research/l2-b1-explicit-family-subspaces

Inputs:
- D0.Algebra.SedenionClifford8
- D0.Algebra.SedenionBrownS3
- D0.Algebra.CliffordThreeFamilies
- vp_sedenion_clifford8_car.py as exploratory/certificate support only

Task:
1. Define an actual source carrier V over the complexified Clifford representation.
2. Define S1 as an explicit span/ideal/subspace generated from a concrete projector/basis.
3. Define the Brown order-three operator Ppsi on V.
4. Define S2=Ppsi(S1), S3=Ppsi^2(S1).
5. Prove dimensions from the actual subspaces, not constants named semiSpinorDimPerGen/fullGenDimPerGen.
6. Prove direct-sum independence, preferably:
   finrank(S1 ⊔ S2 ⊔ S3)=finrank S1+finrank S2+finrank S3,
   or equivalent zero-intersection theorems.

Negative controls:
- S2:=S1 must fail the rank theorem.
- A deformed/non-Brown generator must not inherit the conclusion automatically.

Done:
- D0-CLIFFORD-THREE-INDEPENDENT-FAMILIES-001 can return to LEAN_PROVED only when the literal theorem
  contains actual subspaces and their direct-sum/rank statement.
- No Generation := Fin 3 is allowed as evidence.

## W-B2 — Prove the actual single gauge sector

Branch: research/l2-b2-gauge-lie-action

Dependency: W-B1 preferred, but generator algebra can start in parallel.

Inputs:
- existing colorBivector/hyperchargeOp/weakT3 definitions may be reused only after normalization audit.
- 2026 external construction may be used as formula source; record exact source/equation.

Task:
1. Define explicit generators for su(3), su(2), u(1) on the Clifford carrier.
2. Prove the required commutator/bracket table or an isomorphic Lie representation.
3. Prove the action preserves each physical family sector.
4. Prove Brown-family intertwining/commutation:
   Ppsi T_a Ppsi^{-1}=T_a, or the exact correct common-gauge statement.
5. Prove no three independent copies are introduced by the construction.

Done:
- literal theorem contains the Lie relations + same-action/S3 relation.
- 8+3+1=12 alone is explicitly insufficient.

## W-C1 — Derive the cochain census from the actual scene

Branch: research/l2-c1-derived-cochain-census

Inputs:
- K(9,11,13) canonical scene
- existing HodgeThreeLevelSpectrum and incidence machinery
- PhysicalCarrierInventory only as a target interface

Task:
1. Define/identify actual C0, C1, C2 types from vertices, edges, triangles.
2. Prove card/dim C0=33, C1=359, C2=1287 from those types.
3. Define actual boundary/coboundary maps.
4. Prove d1*d0=0 (or boundary-square-zero in chosen orientation).
5. Derive rank/nullity numbers 32,327,960 from operators/topology rather than declared constants.
6. Only after that test whether C1 is minimal for a common matter/gravity carrier.

Done:
- CARRIER-CENSUS may be promoted beyond FORMALISM only from derived carrier theorems.
- “unique minimal common carrier” requires a separate universal/minimality theorem.

## W-D1 — Construct the actual CAR Dirac and prove its square

Branch: research/l2-d1-car-dirac-operator

Inputs:
- ArchiveCARFockCarrier
- ArchiveCARRelations
- ArchiveNaturalTwistedDirac finite differences
- ArchiveRoleProductLaplacian

Task:
1. Define the finite Hilbert/module carrier explicitly.
2. Define D_L as an actual matrix/operator using finite differences and CAR creation/annihilation.
3. Define adjoint and prove D_L^*=D_L.
4. Prove by extensional/operator equality:
   D_L^2 = Delta_L^(4) tensor I_16
   with the exact normalization used by the metric product Laplacian.
5. Derive kernel, parity and heat-trace claims as corollaries only after the square theorem.

Negative controls:
- wrong sign in one CAR term must break the square identity.
- wrong derivative scale must produce a visible normalization mismatch.

Done:
- CAR-DIRAC-OWNER and CAR-DIRAC-SQUARE may close first.
- zero-mode/parity/spectrum/heat-trace rows stay open unless separately derived.

## W-D2 — Prove fixed-mode product spectral convergence

Branch: research/l2-d2-product-spectrum-convergence

Inputs:
- ArchiveProductSpectrumConvergence definitions

Task:
1. Prove for fixed integer k and sufficiently large L the sine approximation inequality actually used:
   |4*pi^2*k^2 - 4*L^2*sin^2(pi*k/L)| <= C*k^4/L^2
   with an explicit valid constant.
2. Sum over four Role coordinates.
3. Prove convergence of each fixed 4D mode.
4. Prove the actual heat-trace product factorization from the tensor/product eigenvalue set.
5. Keep heat-trace limit interchange separate unless dominated/uniform estimates are proved.

Done:
- D0-ARCHIVE-PRODUCT-SPECTRUM-CONVERGENCE-001 literal theorem contains an inequality and limit,
  not merely a defined discrepancy function.

## W-D3 — Turn the pseudoinverse twist narrative into operators

Branch: research/l2-d3-pseudoinverse-twist

Dependency: W-D1 actual D_L.

Inputs:
- PseudoinverseTwistAlgebra
- ArchiveCanonicalZeroModeProjector
- ArchiveDiracPseudoinverse

Task:
1. Define pi(a), E_L(a), D_L^+ and rho_L(a)=pi(a)+E_L(a)D_L^+ on one carrier.
2. Prove E_L(a)P0=0.
3. Prove exact twisted commutator.
4. Define operator norm and Lip seminorm used by the theorem.
5. Prove ||rho_L(a)-pi(a)|| <= 8/L * L_L(a), or return the correct constant.
6. Prove epsilon convergence to identity from the actual norm inequality.

Done:
- both pseudoinverse-twist rows can close only with operator-level statements.

## W-D4 — Genuine Latremoliere theorem application

Branch: research/l2-d4-spectral-propinquity-application

Dependencies: W-D1 and W-D3; W-D2 useful.

Task:
1. Pin exact Latremoliere theorem (paper/version/theorem number).
2. Encode its hypotheses as a structure whose fields are PROPOSITIONS/proofs, not Bool/Nat labels.
3. Instantiate every field with D0 theorems.
4. Apply the external theorem/bridge explicitly.
5. Export a literal bound involving the actual spectral propinquity Lambda.
6. Only then derive the common-limit Cauchy inequality.

Done:
- D0-ARCHIVE-LATREMOLIERE-TORUS-INSTANTIATION-001 and
  D0-ARCHIVE-CONCRETE-SPECTRAL-PROPINQUITY-001 can close.

## W-A0b — Upgrade the variational audit while A1 research runs

Branch: research/l2-a0b-variational-types

Do not solve the conceptual A1 problem. Prepare the types needed for the expensive memo to land.

Task:
1. Define edge-variable space, symmetric-matrix embedding, measure carrier and pairings.
2. Define S_A2(h,rho) in Lean for arbitrary finite graph.
3. Prove the exact fixed-rho gradient formula.
4. Prove raw divergence formula.
5. Define M,D_M,L_M and prove the exact completion identity.
6. Do NOT call 2L the physical variational response.

Done:
- A1 memo can be integrated without redoing basic algebra.

## W-I1 — Lightweight automatic status-inflation guard

Branch: tooling/l2-claim-scope-guard

Task:
Add a non-authoritative lint report (warning first, not hard fail) for common inflation patterns:
- owner theorem is only rfl/arithmetic while note contains “spectrum”, “kernel”, “Lie”, “convergence”, “unique”;
- claim release CORE but theorem target is a constant defined immediately above;
- module comments advertise operator equality absent from theorem type.

This lint is heuristic and must never replace reviewer judgment.

## Merge order

Independent now: W-B1, W-B2, W-C1, W-D1, W-D2, W-A0b, W-I1.
Then: W-D3 -> W-D4.
A1 conceptual closure waits for the separate expensive-agent memo, but W-A0b prepares its Lean landing zone.
