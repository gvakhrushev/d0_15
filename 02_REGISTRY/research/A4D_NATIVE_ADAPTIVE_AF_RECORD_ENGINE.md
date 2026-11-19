# Adaptive AF record and the literal retained-record engine

2026-10-16. Exact conditional transition theorem on the existing carrier.
Physical admission, a joint moving-metric law and the parent GR terminals
remain open. This result consumes the existing gate, price cut, full
AF/CAR intertwiner and engine selector; it introduces no fitted phase,
fresh blank, reset or external tick input.

The [role-orbit owner](A4D_NATIVE_AF_ROLE_ORBIT_CAR_GEOMETRY_2026-10-16.md)
found agreement for four transitions from the activated canonical AF seed
and a discrepancy on the fifth. The discrepancy is exactly the first
change of the engine's first-grade sign. Conjugation by the existing
price reflection gives an AF representation of the other branch on all
sixteen CAR coordinates. Adaptive reuse then agrees for every subsequent
defined engine step. The canonical activated orbit is defined at every
future tick by the analytic recurrence below.

## 1. Owned operators and the all-sixteen identity

Write `a²=p`, `p²+p=1`, with positive golden a,p. In the actual full-Fock
CAR basis let c be creation along the retained time axis, N=cc†,
P=I-N, X=DEG-N, and use the existing polynomial H(X) distinguishing
spatial degrees0,1 from2,3. The owner's literal gate is

```text
U(n)=a[(I-H)+H(I-2N)]
     +p[(I-H)(c-c†)-H(c+c†)].
```

For the same observer line with opposite sign, c changes to -c, while
N,X,H and P do not change. The existing price-cut reflection

```text
D=2P-I=I-2N,  D²=I,
DcD=-c,  Dc†D=-c†
```

therefore proves `U(-n)=D U(n)D` on the complete exterior space. This
is an operator identity, without any support restriction on the vector.
At the rest axis, `D=diag((-1)^(mask&1))` in all16 mask coordinates.
Direct substitution gives exactly both matrices of the owned engine's
`literal_axis_gate(state,sign)`, not merely their action on one orbit.

The engine actually selects `sign(m[1])` from the first-grade vector.
It does not select the sign from the newer correlated full-CAR current.
On the canonical orbit below that latter current is e0 even when m[1]
is negative, so these two readouts cannot be interchanged.

## 2. The same branches in the actual full AF carrier

Use the existing level1 embedding `Psi:C16->H4`, the full 89-dimensional
AF gate W+, price P_AF and retained blank cut B_AF from
`role.af_embedding(checks)`. In particular

```text
W+ Psi=Psi U+,  P_AF Psi=Psi P,
D_AF=2P_AF-I89,
W-=D_AF W+ D_AF,
W- Psi=Psi U-.
```

These follow by multiplying the already-owned intertwiners; no new
CAR-to-AF isometry is chosen. In the literal four-copy frame,
`D4=diag(1,1,-1,-1)` and W- has the existing `AF.record()` matrix with
every p-entry sign reversed. All a-entries are unchanged. Its whole
four-dimensional scalar channel is retained. The other69 directions
still have the identity action: the two outer reflections cancel there.
Both branches are unitary on all89 coordinates.

P_AF and B_AF are the two existing diagonal four-copy cuts, so
`[D_AF,P_AF]=[D_AF,B_AF]=0`. The retained blank cut is unchanged by
this conjugation. This does not rebuild a new intrinsic blank from an
instantaneous nonzero top-grade coefficient: that coefficient can vanish.
An admission theorem requiring such a rebuild needs its own retained
orientation resource. The present transition supplies no fresh blank.

For any full AF state x whose CAR projection m=Psi†x belongs to the
engine domain, set

```text
s(x)=sign(m[1]),  T_AF(x)=W_s(x) x.
```

The reducing property gives `Psi†T_AF(x)=U_s(m)m`. Scalar and complement
components remain present; they are not declared invisible to the entire
action just because this CAR readout does not read them.

Each W_s separately lies in the actual old-right commutant A7. This
does not imply that the nonlinear selected map T_AF itself is
old-right-equivariant: the selector need not be invariant under a right
action. It is a piecewise unitary state map, not one global linear
unitary or a demonstrated fixed quantum channel.

The literal engine has six zero equations on masks `(2,3,4,5,8,9)`;
the remaining support is ten-dimensional, with all16 entries stored.
It also requires nonzero input and output m[1] and exact Z[a] storage.
The zero equations are branch-invariant, but arbitrary states in this
sector can still hit the first-grade singularity. No generic domain
closure is inferred from unitary norm preservation.

## 3. The canonical activated seed has an infinite defined orbit

Tick0 here means AFTER the actual `AF.activate(1,Omega1)`, with
`Omega1=(p,0,0,p,ap)`. Its CAR component is

```text
m(0)=ap(e0+e14)+p²(e1-e15).
```

Its norm squared is2p²; the scalar AF mass p³ is retained, so the whole
AF state has norm1. This is the actual activated preparation, rather
than the earlier active role-frame seed outside the inherited image.

Define the notation

```text
R(theta)=[[a,-p],[p,a]],  cos(theta)=a, sin(theta)=p,
Z=diag(1,-1).
```

Theta is only a notation for the existing golden coefficients. It is
not a new angle, clock calibration or adjustable phase. On the pair
`(m0,m1)`, the selected gate is R(s theta); on `(m14,m15)` it is
`Z R(s theta)`. The first five values of m1 are exactly

```text
p²,  2ap²,  9p-5,  4ap5,  45-73p,
 +     +      +      +       - .
```

Thus the first four selected gates equal W+, and the fifth equals W-.
For example `p>45/73` follows by squaring `sqrt5>163/73` with positive
sides. Let `L3=p R(theta)^4 e0`, `L4=p R(theta)^5 e0`. Since
`R(-theta)L4=L3` and `R(theta)L3=L4`, the low pair subsequently
alternates L3,L4, whose second coordinates are nonzero with opposite
signs. This proves the absence of a first-grade singularity for all
future steps on this seed, without extrapolating a finite orbit replay.

The high pair has the exact continuing archive recurrence, for r>=0,

```text
(m14,m15)(3+2r)=p(cos(2r theta), sin(2r theta)),
(m14,m15)(4+2r)=p(cos((2r+1)theta),-sin((2r+1)theta)).
```

It follows from `U_s,high=Z R(s theta)` and `ZR(theta)Z=R(-theta)`.
The full state is not a two-state low-pair cycle: its higher grades
continue to carry the record. Already at tick1, m15=0 and m14=p.
The helper verifies the recurrence base and generic rotation induction;
it does not replay the old128-tick orbit suite.

An infinite mathematically defined orbit is not free finite information.
Sixteen real/ring coordinates or fixed H4 do not bound the number of
bits in their exact coefficients. The owned Z[a] integer coefficients
and audit codec may require increasing storage; `bounded_step` has an
explicit overflow failure. No bounded finite-bit implementation,
physical clock law, new cell count or refinement trigger follows.

## 4. Exact feedback of every retained sign word

In the existing Hadamard basis the full CAR gate is

```text
U_s=[R(s theta) (+) Z R(s theta)] tensor I4,
P=diag(1,0,1,0) tensor I4.
```

For a chronological word s1,...,sr, with operators multiplying Ur...U1,

```text
U_word=[R(theta S+) (+) Z^r R(theta S-)] tensor I4,
S+=sum_j s_j,  S-=sum_j (-1)^(j-1)s_j.
```

This is induction using `ZR(theta)Z=R(-theta)`, with empty word I.
Consequently the literal feedback `P U_word†(I-P)U_word P` has

```text
lambda+=sin²(theta S+), lambda-=sin²(theta S-),
```

each with multiplicity4 on CAR, and eight other zero modes. Its
complete counting determinant is

```text
det16(I-z F_word)=(1-z lambda+)^4(1-z lambda-)^4.
```

On the actual full AF H4 the same two eigenvalues each have
multiplicity5, because the scalar four-copy channel also remains.
The remaining79 feedback eigenvalues are zero, including the whole
69-dimensional identity complement. Therefore

```text
det89(I-z F_word)=(1-z lambda+)^5(1-z lambda-)^5.
```

For two steps, equal signs give `4p³` in the low channel and zero in
the high one; opposite signs exchange the channels. Thus the native
CAR determinant is always `(1-4zp³)^4`, but its feedback projector need
not be the same. Full AF has exponent5. These are counting-trace
feedback prices, not the AF PF-weighted spectral Cost-Info contract.
Logarithmic prices require their usual positive-determinant domain.

At fixed pairing and golden coefficients, any finite strict sign word
has locally constant gates. Its sign chamber is an intersection of
linear strict-sign conditions on the initial matter vector. The
counting-feedback gate price consequently has zero smooth matter source
inside such chambers; no derivative across a rejected m1=0 boundary is
claimed. Moving noncollinear n, metric/pairing and their source terms
are not removed by this discrete sign identity.

## 5. Same H4 words preserve the complete A7 spectral price

There is a second, stronger constant-price statement for the canonical
seed on this SAME working carrier. It is not the next active AF record.
Decompose H4 under the inherited old-right A1 action. The two complete
A7 factors of the activated canonical vector have

```text
F0†F0=p² I2,  F1†F1=p³ I1.
```

Every selected W_s and every retained word is unitary in this commutant.
It preserves these Grams, hence the complete A7 nonzero Schmidt
spectrum `(p²,p²,p³)` and all zero modes. With the existing reference
`mu7=p8 I34 (+) p9 I21`, all retained words have exactly

```text
A_old,7=6,  H7/log(phi)=2+p³,  Cost7=8+p³.
```

Neither sign feedback nor reuse of this word produces the earlier
nonzero second-active-record source. That source belongs to a new
activation of the changed A4 left state into a different working level,
as proved by the [canonical trace record owner](A4D_NATIVE_CANONICAL_TRACE_RECORD_SOURCE.md).
Its distinction between active continuation and passive/same-carrier
readouts is retained. A state-conditioned word cannot be called another
fresh activation to manufacture an entropy or matter source.

For a varied seed the same commutant theorem instead preserves that
seed's nonzero spectrum; it does not make every preparation price6.
Here the source-zero statement concerns the canonical prepared word
family at fixed pairing and the stated counting/spectral contracts,
not the full native action with all direct fields and preparations.

## 6. Evidence and remaining transition boundary

The new helper
[`adaptive_engine.py`](sources/d0_native_adaptive_engine_2026-10-16/adaptive_engine.py)
exports `run(repo=None)`. It pins the role/AF/Fock/current/engine definition
sources, calls only the selected `role.af_embedding(checks)` weld, and
uses no old `build_result`, suite entrypoint, JSON receipt or Lean run.
Controls cover both literal16-row engine branches, the whole AF operator,
old-right generators, exact signs and the infinite recurrence, generic
word induction, both two-tick projectors, feedback multiplicities and
the complete A7 Schmidt/reference identities. The general results are
the analytic identities above, rather than inference from sampled ticks.

The common conditional transition arrow now holds beyond the original
four-step segment, on the existing selector and named embedding. It
does not identify the full correlated-current observer with first grade,
derive a noncollinear/moving-pairing AF intertwiner, turn amplitude-sign
control into an admitted quantum channel, select the physical Info or
controller price, or close the common curved action/source/refinement
problem. The new comparator/preparation continuations and the retained
controller compiler theorem keep their own scopes; none is overwritten.
