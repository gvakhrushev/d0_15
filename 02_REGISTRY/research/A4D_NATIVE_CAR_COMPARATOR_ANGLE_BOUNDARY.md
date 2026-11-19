# The full-CAR record and v10 comparator do not share the same projector pair

15 October 2026. Exact finite KILL-FIRST comparison of two existing owners.
This closes only the direct common-frame identification tested below. It does
not close G0, choose a physical action, or rule out a non-isometric history map.

## Result

The branch-information cocycle for the v10 comparator cannot be carried onto
the full-CAR chronology by simply identifying their two record cuts and
changing frame. The exact pair invariant

\[
K(P,Q)=(P+Q-I)^2
\]

has different spectra in the two owners:

| Existing record pair | Exact spectrum of \(K(P,Q)\) |
|---|---|
| Full 16-state CAR: \(P\), \(U^T P U\) | \(p\), multiplicity 16; \(p^2+p=1\) |
| v10 comparator: \(P_c\), \(P_r\) | \(9/25\), \(25/169\), and \(1\), each multiplicity 2 |

For the CAR owner, the actual golden gate decomposes into two 2-by-2 blocks
whose first rows are \((a,-p)\), with \(a^2=p\). Each CAR pair of cuts
therefore has squared principal angle \(a^2=p\). The full exterior lift retains
four apparatus copies, so the same invariant is \(p I_{16}\).

The v10 owner builds \(P_r=Q^T P_c Q\) from the pinned rotations with
cosines \(3/5\) and \(5/13\), plus the two-dimensional common zero sector.
Direct multiplication gives

\[
K(P_c,P_r)=\operatorname{diag}(9/25,9/25,25/169,25/169,1,1).
\]

None of these rational eigenvalues satisfies \(x^2+x-1=0\): the exact
residuals are \(-319/625\), \(-23711/28561\), and \(1\). A common unitary,
or any common pairing-isometric frame transport, preserves the spectrum of
\(K(P,Q)\). Therefore the two existing record pairs are not the same pair in
different coordinates, and the shared golden coefficient alone cannot bind
the v10 path-information result to the CAR metric chronology.

The same mismatch rules out a sharper natural extension. In the CAR owner,
\(PQP=pP\), where \(Q=U^TPU\). In the v10 pair,
\(P_cP_rP_c=\operatorname{diag}(9/25,0,25/169,0,0,0)\), which is not
\(pP_c\). A unital completely positive Heisenberg map that sends both sharp
CAR cuts to the two sharp v10 cuts would put both source projections in its
multiplicative domain, hence preserve \(PQP=pP\); the displayed exact matrix
contradicts that identity. Thus there is no sharp-to-sharp unital CP map of
the two projector pairs either.

There is a history-level obstruction as well. For the projective CAR
instrument induced by \(P\) and \(I-P\), each outcome confines the next state
to one of the two cut ranges. On either range, the probability of repeating
that same outcome at the next tick is exactly \(p\): the corresponding
compressed gate has squared norm \(pI\). If a history-preserving map to the
v10 instrument existed, then after any fixed positive-probability prefix its
encoded state \(\sigma\) would have v10 direct probabilities \(p\) and
\(p^2\) for the next one and two direct letters.

The actual v10 direct Kraus operator is \(C_0=pI+p^2V\), which is normal.
Writing \(E_0=C_0^*C_0\), the probabilities of \(n\) consecutive direct
letters from \(\sigma\) are \(\operatorname{Tr}(\sigma E_0^n)\). The exact
spectrum of \(E_0\) is

\[
1-\frac{36}{25}p^3,\quad
1-\frac{100}{169}p^3,\quad
1-4p^3,
\]
each twice. None equals \(p\): equality would force \(p=61/97\),
\(269/369\), or \(5/9\), respectively, and none satisfies
\(p^2+p=1\). Matching the first two repeated-direct probabilities would
give \(\operatorname{Tr}(\sigma E_0)=p\) and
\(\operatorname{Tr}(\sigma E_0^2)=p^2\), hence
\(\operatorname{Tr}(\sigma(E_0-pI)^2)=0\). Positivity would force support
on the nonexistent \(p\)-eigenspace. This rules out a fixed-state
instrument intertwiner preserving those direct histories.

## Scope and next mathematical test

This rejects common isometric transport, sharp-to-sharp unital CP transport,
and any fixed-state instrument intertwiner preserving these repeated-direct
histories. It does not exclude a history-dependent compression with auxiliary
memory or a different map from primitive D0 records to comparator outcomes.
Such a map must preserve the full branch tree and its refinement law; matching
one angle, one expectation, or the common coefficient \(4p^3\) is
insufficient. No new action, selector, or physical postulate is introduced
here.

The next G0 test is now narrower: use an already-owned history-dependent
retained state, if one exists, to construct the map that evades this
fixed-state obstruction, and verify all words and golden refinement. If the
existing AF/condensed refinement supplies no such map, the CAR and v10
instruments remain separate owners; do not combine their source derivatives.
If it does, compute the pulled-back joint metric/matter derivative before
using branch information as a source term. The full native preparation and
its physical admission remain open during that test.

The full-CAR parent checker currently has a stale transitive input pin: replay
of `a4d_native_fock_record_binding_check.py` fails because the saved certificate
expects SHA-256 `da99029a...` for
`a4d_native_matter_observer_pairing_certificate.json`, while the current pinned
file hashes to `600a1f5a...`. This result does not rewrite or silently refresh
that older receipt; the new calculation reconstructs the two exact operators
from the pinned source formulas directly.

## Reproduction

From the repository root:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_car_comparator_angle_check.py
```

The checker pins the actual Lean full-step source, the full-CAR binding and
chronology owners, and the v10 proof and executable source, then reconstructs
both pair invariants over exact rationals and the golden relation. Its receipt
is `certificates/a4d_native_car_comparator_angle_certificate.json`.

## Source pins

| Input | SHA-256 |
|---|---|
| `GoldenCoherentMemory.lean` | `6ea993e22c8b7d0b8a93b9537d51893cb4aff45af858d82ec7f9005ead96e2d7` |
| `A4D_NATIVE_FOCK_RECORD_BINDING.md` | `d85e57979a61972e641eae24442a776133c429c8696d0948590f6d290a60b045` |
| `A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md` | `601e5bb9203789a66ad2a945aad30da92b6233ac40417d54c6b47c95dc43536b` |
| v10 direct-forcing `RESULT.md` | `92fecc34d44a6bb22a63d09073d861ef0f5accdb866b33d658c80eaa0944832b` |
| v10 executable `verify.py` | `d5660e27d0fe2a6f46472084de30ef197fb7a187ff27c269574032a1dd189491` |

No claim status, task lifecycle, Lean owner, or existing PR terminal changes.
