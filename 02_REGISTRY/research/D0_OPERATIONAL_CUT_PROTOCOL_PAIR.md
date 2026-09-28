# D0 operational-cut protocol pair

**Task:** `WRK-D0-OPERATIONAL-CUT-PROTOCOL-PAIR`  
**Class:** `WORKER`  
**Certificate:** `02_REGISTRY/research/certificates/d0_operational_cut_protocol_pair_check.py`  
**Terminal:** `D0-OPERATIONAL-CUT-PROTOCOL-PAIR-EXACT`

## Result

The finite pair exists.

Two protocols are built over the same five-state joint carrier, the same five
action labels, the same owner-facing injective verification record, the same
two witness lines, the same two catalogue values, the same comparator, and the
same scenario archive projection.  They differ only in the allowed transition
relation.

The common verification apparatus satisfies the exact functional obligations
owned by `D0-POPPERIAN-BOOTSTRAP-001`:

- the state carrier is nontrivial;
- there are two distinct registered lines;
- the catalogue is nonempty;
- the owner-facing record map is injective;
- on every line and catalogue value, comparison of two records returns exactly
  whether the represented states are distinct.

The allowed-transition protocol contains

```text
exposed_none --acquire_enclosure--> carrying_none
carrying_none --enter_and_isolate--> safe_none
safe_none --record_safe--> safe_recorded
```

whereas the blocked protocol omits the first two physical edges.  Therefore
`safe_none` exists in the common carrier but is reachable from
`exposed_none` only in the allowed-transition protocol.

This is an exact finite countermodel to the proposition that the accepted
verification contract by itself fixes the transition law.

## State table

| state | has enclosure | inside | hazard isolated | archive | safe |
|---|---:|---:|---:|---|---:|
| `exposed_none` | 0 | 0 | 0 | none | 0 |
| `carrying_none` | 1 | 0 | 0 | none | 0 |
| `safe_none` | 1 | 1 | 1 | none | 1 |
| `safe_recorded` | 1 | 1 | 1 | safe | 1 |
| `exposed_recorded` | 0 | 0 | 0 | exposed | 0 |

The verification record is the full finite state tuple and is injective.
The scenario archive projection is the final `archive` column.  These are
deliberately different typed maps.

## Action table

| action | type |
|---|---|
| `noop` | identity |
| `acquire_enclosure` | physical cross-cut transition |
| `enter_and_isolate` | physical cross-cut transition |
| `record_safe` | archive write |
| `record_exposed` | archive write |

Both protocols have this same action type.  Availability is determined only by
the protocol's transition relation.

## Cut control

The two cut labels are

```text
subject|apparatus
subject+enclosure|hazard
```

and re-describing any declared joint state under either cut returns the same
joint state.  By contrast, `acquire_enclosure` changes
`exposed_none` to `carrying_none`.  A cut re-description is therefore not
silently counted as a physical transition.

## Record control

`safe_none` and `exposed_none` both have scenario archive value `none`,
but the first satisfies the state predicate `inside && hazard_isolated` and
the second does not.  Hence absence of that archive record implies neither
safety nor danger.

This does not conflict with the accepted Popperian owner.  Its `P.record`
must be injective, and in this checker it is: the owner-facing verification
record is the full finite state tuple.  The coarse scenario archive is an
internal projection of the joint state, not a replacement for `P.record`.

A hostile control flips the English/semantic `safe` label on
`exposed_none` while leaving both record maps and the comparator unchanged.
The operational data do not follow the label, so no safety identification can
be manufactured by renaming.

## Relation to the two owners

`D0-POPPERIAN-BOOTSTRAP-001` fixes the verification obligations above.  The
finite pair shows that those obligations do not additionally determine which
physical state transitions are allowed.

`D0-VERIFIABLE-REGISTRATION-ORTHOGONALITY-001` is not instantiated here.
That result is typed on density operators and an exact comparison measurement.
This finite transition model defines neither density operators nor a
measurement effect, so the orthogonality theorem is only a boundary condition:
nothing here promotes the finite states to quantum states or imports an
orthogonality claim into the transition relation.

## Boundary of the conclusion

The conclusion is about two finite operational semantics.

- **State reachability:** the safe state is reachable only when the declared
  transition relation contains the box-transfer/isolation path.
- **Recorded knowledge:** the scenario archive can be empty on both a safe and
  an exposed state, so archive absence alone determines neither.

There is no Hilbert-space model, collapse dynamics, Born probability,
measurement-problem solution, physical cat claim, new claim ID, or BOOK
promotion.

## Validation

```bash
python3 02_REGISTRY/research/certificates/d0_operational_cut_protocol_pair_check.py
```

Expected terminal:

```text
D0-OPERATIONAL-CUT-PROTOCOL-PAIR-EXACT
```
