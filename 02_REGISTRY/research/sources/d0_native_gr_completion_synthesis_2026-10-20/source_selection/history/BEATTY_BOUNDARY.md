# Golden weights do not yet derive a Golden rotation clock

Same pinned native prospective-law source as `FISHER_HORIZON_TEST.md`.
This is a precise boundary on deduction from the current source law, not a
claim that all connections between Beatty sequences, D0 and a native clock
are impossible.

For the original unit-edge-Cost graph and neutral terminal task, put K=cA for
ANY c>0. The complete length-n partition is c^n A^n 1, so the actual next-step
law is identically

    Q_n(u,v)=c A_uv c^(n-1)(A^(n-1)1)_v/[c^n(A^n1)_u]
            =A_uv (A^(n-1)1)_v/(A^n1)_u.

It is independent of c. In particular c=phi^-1 gives exactly the same
probability law as c=1/2, 2/3, 1 or 7/3. The common Golden factor affects the
unnormalized price and pressure, but supplies no phi-specific conditional
history or clock coding at a fixed horizon. The infinite native Doob law is
equally invariant: rho(cA)=c rho(A), r(cA)=r(A), so

    P_uv=A_uv r_v/[rho(A) r_u].

This alone does not rule out a numerical coincidence with a Golden rotation;
it establishes that dependence on the base cannot force it here.

The actual record language gives a second, independent boundary. From a
fixed K9 vertex there are 24 two-step returns and 286 three-step returns,
all with positive native probability. In fact the root has a first-return
word of EVERY length n>=2: choose the n-1 intermediate vertices alternately
from K11 and K13 and then return to the root. Every original vertex has at
least 20 outgoing choices, so at least 20^n complete original histories of
length n start at a fixed root. These remain distinct in the full retained
label record.

A Sturmian binary rotation code has only n+1 distinct length-n factors.
Any fixed finite-window deterministic decoding of such a code therefore has
at most n+O(1) distinct output words of length n. It cannot reproduce the
exponentially large full original native language. Alphabet grouping or
selecting a particular path can produce a smaller language, but does not
preserve the whole current history law.

The measure-theoretic version is sharper and not restricted to a finite-window
decoder. The stationary native Perron-Doob process has entropy rate

    h(P)=-sum_uv pi_u P_uv log P_uv
        =log rho(A)>0,

because log P_uv=log r_v-log r_u-log rho(A) on every supported edge, and
stationarity cancels the two r terms. Here rho(A) is the positive root of
rho^3-359 rho-2574=0, approximately 21.8373824011252, so h(P) is about
3.08362329027 nats per original vertex transition. An irrational circle
rotation with its invariant measure has zero entropy; every stationary
finite-alphabet measurable factor also has zero entropy. Consequently the
ENTIRE present stationary native process cannot be exactly that kind of
deterministic rotation factor. The actual original one-sided process has the
same asymptotic entropy rate; changing only its initial law does not remove
this obstruction.

The zero-entropy statement has an elementary proof in the present setting.
A partition of the circle into finitely many intervals produces at most
O(n) atoms in its n-fold orbit refinement, since it has only O(n) iterated
endpoints. Its n-symbol entropy is therefore at most log O(n), giving rate
zero. Approximate any finite measurable partition in measure by a finite
interval partition with disagreement probability delta. The per-symbol
conditional entropy is at most the binary entropy H_b(delta) plus
delta log(k-1), where k is the original finite alphabet size. The chain rule
bounds its entropy rate by that of the approximating interval partition plus
this error. Letting delta tend to zero proves zero rate for every finite
measurable partition. Thus this boundary does not depend on a special choice
of the two-interval Sturmian cut.

This does NOT rule out a Beatty subsequence used as an additional clock, a
coarse observable with zero entropy, a chosen path, a random coupling, or a
different derived source with actual Golden state-dependent structure.
Those are distinct constructions requiring their explicit map and paid
clock/record law. A useful next positive test would exhibit such a map and
show which original distinctions and probability law it preserves.

The later `4867b6d43b262da7e0e08b9b14a7a7a20d9a2ac4` amendment to
`sources/d0_native_triz_reference_2026-10-20/TRIZ_MATCHED_LOOP_VOID_SOURCE.md`
is compatible with this conclusion. It fixes the unit conversion
S_phi=-log(P)/log(phi)=J/log(phi) IF a particular void event has first been
physically admitted and charged. That is a normalization of the code price
for a supplied probability, not a derivation of a Beatty event process,
a finite clock, or the admission rule. Its own finite prefix lengths and
termination/work caveats remain.

`check_native_beatty_boundary.mjs` checks exact common-factor cancellation for
four rational replacements at horizons 1..12, the actual rooted 2/3 return
counts, supported first-return witnesses at every length 2..12, the integer
language-growth lower bound, and the full33 entropy telescoping identity.
The all-length claims above are proved symbolically, not extrapolated from
those finite checks.
