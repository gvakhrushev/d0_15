# Proposed research: operational cut and record

**Disposition:** proposed finite research question, not an accepted result or a
claim about quantum measurement.

## The idea in operational terms

The submitted “cat takes the box from the same backpack” example questions
whether a system/apparatus boundary has been fixed in advance. Its useful
research content is not that the cat is thereby proved alive. It is that the
scenario leaves unspecified whether moving the box is an allowed transition
inside one protocol or a change to the protocol itself.

Represent the proposal using four explicit ingredients:

1. a joint finite state space for subject, hazard, enclosure, and record
   carrier;
2. a cut or decomposition that says which components are treated as a system
   and which as apparatus;
3. a typed relation of allowed operations, including or excluding box
   transfer, enclosure entry, and hazard isolation;
4. a record map describing which outcomes an observer or archive can actually
   distinguish.

A boundary change can then be classified as either a re-description of one
joint state or a genuine state transition with a changed interaction pattern.
Those cases must not be silently identified. “The cat is safe” is a state
predicate; “the protocol recorded the cat as safe” is a statement about the
record map. Failure to obtain a record does not prove either safety or danger.

## Connection to current D0 owners

`D0-POPPERIAN-BOOTSTRAP-001` relates a killing test to a verification contract
and records that such a contract does not uniquely determine its carrier.
`D0-VERIFIABLE-REGISTRATION-ORTHOGONALITY-001` proves an orthogonality result
for a supplied exact comparison protocol. Neither result supplies the
box-transfer operation, the system/apparatus cut, or the record map in this
example. They are comparison points for a new typed model, not a ready-made
resolution.

## Proposed terminal

The planned task should produce an exact finite comparison with one of two
honest outcomes:

- **Allowed-transition outcome:** the fixed joint protocol contains a
  box-transfer/isolation operation, and an explicit record distinguishes the
  resulting safe state from the poison-exposed state.
- **Underspecified-protocol outcome:** the proposed conclusion requires an
  operation, permission, state predicate, or record that the declared protocol
  does not contain; adding it defines a different protocol.

In both cases, state whether “alive” is determined by the model's state or only
recorded after a distinguishing event. Use finite transition systems and exact
records. Do not import Hilbert-space dynamics, collapse rules, Born
probabilities, or make a claim that the standard measurement problem has been
solved.

## Registration boundary

The executable research task is registered as
`WRK-D0-OPERATIONAL-CUT-PROTOCOL-PAIR` in `00_WORK/manifest.json` with state
`PLANNED`. Registration is not permission to start it; it requires the normal
CONTROL handoff and a fresh current-main launch.
