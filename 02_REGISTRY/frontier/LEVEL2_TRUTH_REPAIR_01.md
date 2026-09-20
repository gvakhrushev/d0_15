# Level-II Truth Repair #1

Date: 2026-09-20
Base audited: main @ ec793278f55ae4d8f0c82e06ea7344f3b33ae292

## Purpose

This is a reviewer-side truth repair of load-bearing Level-II claims added after the Brown S3 merge.
The rule is literal: a claim is CORE only when the exported Lean proposition proves the substantive
statement written in the registry note. Comments, definitions whose value is chosen to equal the desired
answer, arithmetic identities about declared dimensions, or Python evidence are retained as support but
do not close a stronger theorem target.

No worker branch is blocked by this audit. The purpose is to separate reusable mathematics from status
inflation while workers continue producing material.

## Findings

### GREEN / retained as substantive core

- Brown S3 scalar-extension algebra remains CORE.
- Sedenion left-action Cl(0,8) relations, Frobenius-orthogonal Clifford monomials and Witt CAR in
  D0.Algebra.SedenionClifford8 remain strong algebraic support.
- D0-GRAVITY-VARIATIONAL-CARRIER-AUDIT-001 is retained in narrowed scope: raw unrestricted matrix
  divergence obstruction, conserved/symmetric 2L for an IsGraphLaplacian, and the traceless pairing lemma.
- Local tick discrimination remains useful: global homogeneous rescaling is gauge in the tested internal
  cone-speed sense, while an inhomogeneous two-point tick profile changes a local ratio.

### AMBER / useful formalism but not the stronger narrative

- D0-CARRIER-CENSUS-001: current module introduces the dimension constants and proves arithmetic
  consistency; it does not derive the dimensions from an actual cochain complex or prove C1 uniquely
  minimal for matter+gravity. Release scope changed to FORMALISM.
- D0-ARCHIVE-NATURAL-TWISTED-DIRAC-OWNER-001: current theorem proves the forward/backward finite
  difference adjoint relation; the self-adjoint Dirac/twist narrative remains downstream.
- D0-ARCHIVE-METRIC-MEASURE-HODGE-LIFT-001: current theorem proves the k=0 and k=1 endpoint formulas
  and 16-sector cardinality; uniqueness/canonicity across all grades is not proved.

### RED / reopened as PROOF-TARGET

1. D0-SEDENION-D0-REPRESENTATION-FUNCTOR-001
   - PR #28 itself states that no typed map into the D0 generation carrier is introduced.
   - Missing: explicit source family sectors and typed/equivariant source -> D0 generation map.

2. D0-CLIFFORD-THREE-INDEPENDENT-FAMILIES-001
   - Current owner proves 3*8=24, 3*16=48 and vacProj0 != 0.
   - Missing: explicit S1,S2,S3 and a direct-sum / intersection / finrank independence theorem.
   - Generation := Fin 3 is bookkeeping only.

3. D0-CLIFFORD-SINGLE-GAUGE-SECTOR-001
   - Current owner proves 8+3+1=12 and reflexivity of colorBivector.
   - Missing: Lie brackets, representation action, and Brown-S3 commutation/intertwining.

4. D0-ARCHIVE-CONCRETE-SPECTRAL-PROPINQUITY-001
   - Current owner defines C/L and proves an algebraic identity for C/L+C/M.
   - Missing: a genuine spectral-propinquity distance Lambda and Lambda(T_L,T_infty)<=C/L.

5. D0-ARCHIVE-LATREMOLIERE-TORUS-INSTANTIATION-001
   - Current owner checks numeric/boolean checklist fields by reflexivity.
   - Missing: theorem hypotheses as proof fields and an actual application of the cited external theorem.

6. CAR Dirac family
   - D0-ARCHIVE-CAR-DIRAC-OWNER-001
   - D0-ARCHIVE-CAR-DIRAC-SQUARE-001
   - D0-ARCHIVE-CAR-ZERO-MODE-OWNER-001
   - D0-ARCHIVE-CAR-PARITY-SPECTRUM-001
   - D0-ARCHIVE-CAR-SPECTRUM-AMPLIFICATION-001
   - D0-ARCHIVE-DIRAC-HEATTRACE-MULTIPLICITY-001
   Current owners mostly prove declared dimensions/factors rather than the advertised operator, kernel,
   parity, spectrum or trace equalities. All are reopened with exact missing artifacts.

7. D0-ARCHIVE-PRODUCT-SPECTRUM-CONVERGENCE-001
   - Zero modes and |Role|=4 are proved.
   - The O(L^-2) discrepancy inequality and actual heat-trace factorization are not.

8. D0-ARCHIVE-PSEUDOINVERSE-TWIST-OWNER-001
   - Current owner proves only cardinalities and coefficient 8.
   - Missing typed rho_L(a), E_L(a)P0=0 and the exact twisted commutator.

9. D0-ARCHIVE-TWIST-DISPLACEMENT-BOUND-001
   - Current owner proves scalar factor positivity/monotonicity only.
   - Missing the operator norm inequality and convergence consequence.

## Strategic consequence

The worker-generated strike package contains valuable ingredients and no-go results, but Assembly Gate I
and II must not consume the reopened rows as closed dependencies.

Immediate reviewer priorities:

1. Repair claims before assembly.
2. Preserve worker throughput; review only load-bearing exports.
3. Route the expensive research agent to A1 variational/Bianchi mathematics rather than repository work.
4. Give worker agents concrete theorem upgrades for each reopened row.

## Reviewer acceptance rule for future Level-II PRs

For every load-bearing claim, the PR must include one sentence of the form:

> Literal exported theorem: <Lean proposition in mathematical notation>.

The reviewer compares only that proposition with the registry note. A comment or a chosen definition is
not evidence for a stronger statement.
