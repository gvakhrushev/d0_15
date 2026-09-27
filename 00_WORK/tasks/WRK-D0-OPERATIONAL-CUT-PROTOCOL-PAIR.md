# WRK-D0-OPERATIONAL-CUT-PROTOCOL-PAIR

Class: `WORKER`

State on registration: `PLANNED`

Parent: `CTRL-D0-OPERATIONAL-CUT-RESEARCH-INTAKE`

Repository: `gvakhrushev/d0_15`

Base: `main`

Branch: `wrk/d0-operational-cut-protocol-pair`

Primary artifact: `02_REGISTRY/research/certificates/d0_operational_cut_protocol_pair_check.py`

Execution: `GitHub-first`

## Why delegated

The bounded artifact is an exact finite pair of protocols, but it requires a
separate typed model and a checker with hostile controls. The key question is
whether the same owned verification/record contract can coexist with different
allowed transition relations. That is an independently reviewable finite
countermodel, not a repository bookkeeping edit.

## Objective

Construct two finite typed protocols over the same joint carrier and with the
same record and verification maps. Vary only the allowed transition relation
and its treatment of the system/apparatus cut. In one protocol, the subject
can acquire or move the enclosure, enter it, and reach a hazard-isolated state;
in the other, that transition is absent. Determine whether the safe state is
reachable and whether the protocol records distinguish it from the
hazard-exposed state.

Check both protocols against the exact contract in
`D0-POPPERIAN-BOOTSTRAP-001`; compare with
`D0-VERIFIABLE-REGISTRATION-ORTHOGONALITY-001` only at the stated density-
operator protocol boundary. If the owned contract forces a common transition
law after all, prove that exact restriction instead of assuming the pair
exists.

## Required controls

1. Same joint state with two cuts, to distinguish re-description from a
   physical transition.
2. Same records and verification map with different transition reachability.
3. A state with no distinguishing record, to show that record absence does
   not imply either safety or danger.
4. A hostile mismatch where the safe-state label changes but the record map
   does not, so no operational identification is inferred from the label.

The checker must report its complete finite state/action/record tables and
test each contract predicate explicitly. Use exact finite data; no floating
probabilities are needed.

## Terminal

Return either a checked pair of protocols satisfying the same owned
verification contract but differing on box-transfer reachability, or an exact
proof that the contract forbids such a pair. In either case state which
conclusion is about state reachability and which is about recorded knowledge.

## Scope fences

No Hilbert-space or collapse model, Born probabilities, interpretation of
standard quantum mechanics, physical claim, new claim ID, BOOK edit, or public
claim. This is a finite operational-semantics artifact. Do not modify A4D
tasks or #240.

## GitHub execution contract

Use fresh current `main`; confirm this row remains `PLANNED` and inspect open
PRs for this task ID. Only after explicit CONTROL dispatch, start the lifecycle
from the task's fresh branch and open a Draft PR before research edits. Keep
this task `PLANNED` until that dispatch; do not begin from its registration
PR. Before handoff, run the certificate and repository work/registry guards.
Never self-merge.

## Chat handoff

Return the task PR and baseline SHA, exact state/action/record tables, the
checked pair or exact obstruction, certificate and guard results, and the
state-versus-record boundary.
