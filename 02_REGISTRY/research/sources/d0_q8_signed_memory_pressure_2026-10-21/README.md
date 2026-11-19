# Exact Golden/Q8 signed memory-pressure source

Research packet, 21 October 2026; existing Draft PR #334, same GR owner.
Primary note: [signed memory pressure and Gram-source formula](../../A4D_Q8_SIGNED_MEMORY_PRESSURE_AND_GRAM_SOURCE_2026_10_21.md).

This packet proves an exact first differential for a specified represented
memory-amplitude log norm. The source is a signed history weight plus an
explicit moving-memory term, not an unconditional Born mean of branch prices.
The common-unitary memory-frame Ward cancellation is exact.

Its new application consumes Book01's already known *full two-port*
Golden/Q8 order interferometer and Book03's existing positive history
weights. The selected dark port has amplitude p³, scoped pressure 3,
and exact branch-cost score (phi²,-phi). A formal +1 change of the
destructive branch's cost lowers this **selected-port** pressure to 2.
The unmeasured complementary port has probability 4p³, so the full
two-port normalized state has pressure zero. An orthogonal regular
memory realization has a different, nonnegative score.

## Reproduce
From this folder:

\`\`\`bash
python3 check.py
\`\`\`

The check uses only the Python standard library; it performs 22
exact arithmetic checks in Q[a]/(a⁴+a²−1) and integer Q8 matrices.
The result is recorded in [RESULT.json](RESULT.json).

## Exact scope and next consumer

No new native primitive, Book03 Info law, same-initial controller,
cut, heat, or physical first Euler source is selected by this result.
The formal ± history is a **single represented detector-port query**,
not a faithful representation of the full path group algebra. The
+1 branch-cost control is a score-table variation, not an asserted
physically admitted separately timed arm.

On a genuine full execution, the required new input for this
amplitude-pressure component is the actual branch cost/gain and
represented memory Gram matrix **including their complete jets**.
The fully paid Book03/oldRIGHT/clock/observer execution, independent
input equations and original continuum refinement remain open.
Keep \`GR_closed=false\`.
