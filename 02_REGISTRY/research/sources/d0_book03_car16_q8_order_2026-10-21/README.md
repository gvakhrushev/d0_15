# Book03 order comparator on the original CAR16 Spin/Q8 carrier

This exact finite certificate composes two already owned mathematical pieces:
the Book03 §03.26.1 equal-cost order/identity comparator and the faithful
parity-even `Q8` representation constructed from the original four-mode
Jordan–Wigner CAR operators on `ArchiveFockState` (`Fin 16`). It closes the
algebraic carrier map between those pieces: the comparator's quaternion axes
act on the original CAR16, not only on Book03's separate four-coordinate
quaternion carrier.

For an arbitrary CAR16 input `ψ`, place it in arm 0 with a blank retained bit,
run the 15 chronological operations, then reversibly copy the output arm into
the bit. In the exact ring `Q[a,p]/(a²−p, p²+p−1)`, the record effects are

```text
identity word: E(record=1) = 0,       E(record=0) = I₁₆
order word:    E(record=1) = 4 p³ I₁₆, E(record=0) = p⁶ I₁₆.
```

Thus the result holds for every CAR16 vector, and for a normalized vector the
record probabilities are `(1,0)` and `(p⁶,4p³)`. The same two 15-step words
are put on the existing 16-label reversible clock with a final idle stage; a
stored program label gives one fixed 2048-coordinate clocked machine. A
common-`i` negative control removes the record contrast.

Replay with:

```text
python3 02_REGISTRY/research/sources/d0_book03_car16_q8_order_2026-10-21/check_book03_car16_q8_order.py
```

The checker reconstructs the integer CAR16 matrices, checks all CAR and
Clifford identities used here, matches all 64 quaternion products against the
existing Book03 `Fin 8` convention, reads the Golden gate from its Lean source,
and verifies every stage and terminal effect exactly. `SOURCE_PINS.json`
records the input Git blobs and SHA-256 digests at the existing PR #334 head
`dfc0275eea67ebc21ffe539de9b6ea96713863a5`. `RESULT.json` is deterministic
checker output.

## Scope boundary

This is a representation and finite-program result. The arm, clock, program
label and retained bit are explicit apparatus factors. The calculation does
not prove that G0 physically admits or pays for the controlled `Q8` actuation,
port routing, blank preparation, record, or clock; it does not construct the
field-to-`Q8` pullback or the same-execution full Book03 `Cost−Info` source.
The literal `fullStep` still has no such `Q8` input. It supplies no native
stationarity, matter Ward identity, or Einstein recovery. `GR_closed=false`.
