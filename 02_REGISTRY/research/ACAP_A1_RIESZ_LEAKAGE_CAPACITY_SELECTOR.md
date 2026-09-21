# A-CAP — A1 Riesz Leakage / Capacity Selector

CONTROL disposition: **ACCEPT AS RESEARCH / CAPACITY-WEIGHT-SELECTOR-NOGO-TERMINAL**  
Research baseline: `d912d8d40d9758268551c2b8e8c8396d0d6639aa`  
Source memo: `MEMO_18_ACAP_A1_RIESZ_LEAKAGE_CAPACITY_SELECTOR.md`

This packet is a durable research summary, not a Lean proof owner.

## Terminal verdict

[
\boxed{\texttt{CAPACITY-WEIGHT-SELECTOR-NOGO-TERMINAL}}
]

The capacity route produces a sharp algebraic mismatch theorem but does **not** force the uniform A1 weight under currently owned D0 capacity/memory principles.

The accepted four-modulus finite family remains

[
\boxed{(\mu,\gamma,u,v)}.
]

## Exact algebraic mismatch

Let
[
K_+=\ker B_+
]
and
[
W=xI_{9,11}\oplus yI_{9,13}\oplus zI_{11,13},
\qquad x,y,z>0.
]

The physically accepted compensator-reduced A1 Euclidean Riesz Hessian is
[
A_W=
4\left[
W-WB_+^T(B_+WB_+^T)^{-1}B_+W
\right]\big|_{K_+},
]
and satisfies
[
A_W(K_+)\subseteq K_+.
]

Thus the reduced physical Hessian itself has no carrier leakage.

The canonical **bare-metric** mismatch is instead
[
L_W:=B_+W^{-1}\big|_{K_+}.
]

Equivalently, with
[
P_+=I-B_+^T(B_+B_+^T)^{-1}B_+,
]
define
[
C_W=(I-P_+)W^{-1}\big|_{K_+}.
]
Writing
[
J_+=B_+^T(B_+B_+^T)^{-1},
]
one has
[
C_W=J_+L_W.
]
Since (B_+) has full row rank, (J_+) is injective, so
[
\operatorname{rank}C_W=\operatorname{rank}L_W,
\qquad
C_W=0\iff L_W=0.
]

This is an exact algebraic diagnostic. Current D0 does not own the interpretation of (L_W) or (C_W) as a mandatory physical correction record or memory load.

## Six-sector action

On the three tensor sectors,
[
L_W|_{Z_{9,11}}=
L_W|_{Z_{9,13}}=
L_W|_{Z_{11,13}}=0.
]

On the three standard sectors:
[
L_W|_{A_9}
=
143\left(\frac1x-\frac1y\right)\iota_9,
]
[
L_W|_{A_{11}}
=
117\left(\frac1x-\frac1z\right)\iota_{11},
]
[
L_W|_{A_{13}}
=
99\left(\frac1y-\frac1z\right)\iota_{13},
]
where each (iota_n) identifies the edge standard copy with the balanced vertex standard representation in the corresponding zone.

Hence
[
\boxed{
\operatorname{rank}L_W
=
8\mathbf1[x\ne y]
+
10\mathbf1[x\ne z]
+
12\mathbf1[y\ne z].
}
]

The exact strata are:
[
\begin{array}{c|c}
x=y=z&0\\
x=y\ne z&22\\
x=z\ne y&20\\
y=z\ne x&18\\
x,y,z\text{ all distinct}&30.
\end{array}
]

Therefore
[
\boxed{
L_W=0
\iff
x=y=z
\iff
u=v=1.
}
]

In projective variables,
[
\operatorname{rank}L_W
=
8\mathbf1[v\ne1]
+
10\mathbf1[u\ne v]
+
12\mathbf1[u\ne1].
]

## Image and archive representation

The exact image is
[
\operatorname{im}L_W
=
\mathbf1[x\ne y]A_9^V
\oplus
\mathbf1[x\ne z]A_{11}^V
\oplus
\mathbf1[y\ne z]A_{13}^V,
]
with dimensions (8,10,12).

For all-distinct weights the image is the full 30-dimensional zone-balanced vertex carrier.

This has the same representation type as the owned dark archive decomposition. The relation is an owned zone-preserving representation isomorphism/reindexing, not a definitional equality of carriers.

## Why capacity does not select uniformity

Four independent gaps block the selector:

1. **Physical typing gap.** No theorem says (L_W\ne0) creates a correction datum that must be retained. The reduced physical Hessian (A_W) already preserves (K_+).
2. **Rank-to-memory gap.** Linear rank (r) does not canonically determine a finite state alphabet or record cardinality. A basis-label protocol would give a different bound from a binary-occupancy protocol.
3. **No-reuse gap.** No theorem says correction information requires a fresh independent archive copy. Existing finite-memory owners allow reuse/dependent encodings.
4. **Occupancy gap.** No theorem says the relevant physical archive has zero residual capacity. `SaturatedRegion` is a boundary-capacity/heat inequality, not memory fullness.

The current capacity predicates do not depend on (W,ho,u,v). Therefore uniform and nonuniform A1 backgrounds can satisfy exactly the same owned capacity propositions.

## Strong negative controls

For
[
\rho=(1,2,3),
quad
W=(1/2,1/3,1/6),
]
all block weights are distinct and
[
\operatorname{rank}L_W=30.
]
The standard-sector coefficients are
[
(-143,-468,-297).
]

For
[
\rho=(2,3,5),
quad
W=(1/6,1/10,1/15),
]
again
[
\operatorname{rank}L_W=30,
]
with coefficients
[
(-572,-1053,-495).
]

Both remain admissible under the frozen finite A1/Hodge/two-tick family and violate no owned memory/saturation theorem.

## Strongest available positive theorem

If one **adds**
[
W^{-1}(K_+)\subseteq K_+,
]
equivalently
[
L_W=0,
]
then the exact mismatch theorem gives
[
u=v=1.
]

This is a common-metric/self-duality condition. It is not derived from archive capacity.

## Generation maximality

No new (N_{gen}=3) maximality theorem follows. The three mismatch blocks arise because the frozen scene already has three zones; using them to prove three generations would be circular.

## Current CONTROL consequence

A-CAP is terminally closed as a selector route inside the current owned theory class.

The next positive internal target is the common finite parent-action/common-metric theorem. It must determine whether the owned A1, Hodge and two-tick structures genuinely share one generated Riesz structure and coefficient normalization, rather than assuming this in the definition of the action.

No CORE upgrade of `D0-HODGE-LINKS-001` follows from A-CAP alone.
