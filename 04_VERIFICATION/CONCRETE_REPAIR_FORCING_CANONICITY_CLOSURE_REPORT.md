# CONCRETE REPAIR FORCING CANONICITY — VERIFIED CLOSURE REPORT

Commit: uncommitted working-tree result

Lean modules:
- `D0.Foundation.IndependentDetectionSideSymmetryBoundary`
- `D0.Foundation.ConcreteRepairForcingCanonicity`
- `D0.Foundation.CascadeFullForcingSynthesis`

Certificate:
- `vp_cascade_full_forcing_dag.py`

Claim retained as `NO-GO`:
- `D0-INDEPENDENT-DETECTION-SIDE-SYMMETRY-BOUNDARY-001`

Claim promoted to `CORE-FORMALIZED`:
- `D0-CONCRETE-REPAIR-FORCING-CANONICITY-001`

## Correction to the previous closure

The exact labelled support grammar contains four realised profiles:
`empty`, `left-only`, `right-only`, and `both`. The two singleton repairs are distinct comparisons
with distinct exact supports. M1 admissibility alone does not force exchange symmetry, so the old
phrase "no residual semantic premise" was too strong when read for labelled detector sides.

The positive three-class theorem is now stated at its exact structural scope. The two independent
repetitions are preregistered, while their names are treated as protocol gauge. Two supports are
equivalent iff a permutation of the registered side labels carries one support to the other. Lean
proves, for arbitrary concrete comparisons, that this orbit relation is equivalent to equality of
computed support arity. The proof uses the general finite-set permutation theorem, not an
enumeration of alternative comparison models.

## Strengthened forcing edges

- the protocol-orbit quotient is equivalent to the structural repair quotient;
- the left-only and right-only repairs are distinct before quotienting and equal only in the
  relabeling orbit;
- the repair-to-`TorusShell` equivalence is unique among rank-preserving equivalences;
- `qT / card(Role) = 11` and `card(Dyad) = 2` compute sizes `9,11,13` from rank;
- the computed capacity sizes agree pointwise with the named shell table;
- the trivial defect class generates the zero cycle;
- the carried nontrivial closed defect generates the nonzero circulation;
- the corrected full forcing DAG consumes the generated cycle, unique rank-preserving shell map,
  and capacity-derived sizes.

## Exact scope

The closure is internal to the concrete in-repo binary `Observation` protocol with two
preregistered independent repetitions modulo permutation of their labels. It does not claim that
M1 alone forces side-exchange symmetry or that every external physical detector must use this
gauge. An external formalization must justify or instantiate the same protocol quotient.

## Gate

- `validate_csv`: PASS, 671 claims
- `d0_logic_chain`: PASS, 530/671 chained
- `d0_value_model`: PASS
- `d0_score --strict`: PASS, 76.8%, zero integrity demotions
- `check_cert_can_fail`: PASS
- cascade closure certificate: PASS with orbit, defect, size, and mutation controls
- v15 closure certificates: PASS
- core certificates: PASS
- book assembly / aggregate idempotence: PASS
- `lake build D0.All`: PASS, 4533 jobs
- `check_no_sorry_in_core`: PASS

The independent v16/publication aggregate retains a pre-existing unrelated failure in
`vp_publication_claim_register_guardrail.py`: the publication abstract lacks the expected literal
phrase `not as proof of quantum gravity`. This result neither imports nor exercises the repaired
M1/cascade modules and is not counted as green here.
