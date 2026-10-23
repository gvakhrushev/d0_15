# The literal D_min code-length difference does not supply the Book03 branch gain

21 October 2026. Existing Draft PR #334.

This is a scoped no-shortcut theorem for the most direct attempted repair of
the current Book03 information gap. It consumes the exact complete-code owner
and the native full128 Golden pair. It does not rule out a different native
information construction.

`GR_closed=false`.

## 1. Exact literal code interface

The complete-code source theorem gives a declared exact comparison interface
in which terminal Golden symbols are represented by the literal binary words

- `F -> 0`, with `|D_min(F)|=1`;
- `R -> 10`, with `|D_min(R)|=2`;

and `Can` is the identity on the complete literal-word equivalence classes.
This is the owner's exact countermodel showing that `D_min` canonicity and
golden word counts alone do not imply the entropy source.

Suppose one tries to close Book03's currently undefined branch
`Info(v)` by the most direct MDL rule

[
 I_i=F_0(X_{m prior})-F_0(X_i),
 qquad F_0(X)=|D_{min}(X)|.
	ag{1}
]

For the two terminal branches the common prior cancels, so

[
 oxed{I_R-I_F=-(2-1)=-1.}	ag{2}
]

If the sign convention is reversed instead, the relative gain is (+1).

## 2. The native Golden amplitude requires a different exact gain

For every original nonblank full128 label, the literal port Kraus pair is

[
 K_F=pL,qquad K_R=sqrt p,L,
 qquad p=arphi^{-1},
]

with physical report charges

[
 C_F=1,qquad C_R=2.
]

The existing same-record amplitude theorem proves that absolute Book amplitude
matching requires

[
 I_R-I_F=rac32.
	ag{3}
]

The scalar-probability binding instead requires (2), while an EXTRA
multiplier on the already executed native Kraus vector requires (1).

Therefore the literal code-reduction rule (1) matches none of the three
typed interfaces:

[
 -1
erac32,qquad -1
e2,qquad -1
e1.
]

The reversed code difference (+1) matches only the **extra-marker** type.
It still fails the absolute amplitude and scalar-probability Book bindings.
Thus using the reversed sign does not construct the missing Book03 absolute
gain.

## 3. What the actual native amplitudes do fix

The scalar Kraus amplitudes themselves have exact Golden exponents

[
 -log_arphi p=1,qquad
 -log_arphisqrt p=rac12.
]

If these are read as the net amplitude-bound path prices, then

[
 S_F=1,qquad S_R=rac12,
]

and consequently

[
 I_F=C_F-S_F=0,qquad
 I_R=C_R-S_R=rac32.
	ag{4}
]

Equation (4) reproduces the required amplitude gain exactly. But it is a
different construction: the information value is obtained from
**primitive charge minus the actual native scalar amplitude exponent**.
It is not a consequence of `F_0=|D_min|` alone.

For a general native branch the Kraus/memory operator need not factor into one
positive scalar times a canonically normalized memory operator. Therefore
(4) is a complete answer only on scalar-factorizable branches such as this
Golden pair. Extending it to the entire retained history requires the missing
memory normalization theorem already isolated by the current-specification
closure barrier.

## 4. Consequence for the closure route

Book01's `F_0` remains a valid state-complexity definition. What is excluded
is the shortcut

[
 	ext{Book03 branch Info}
 stackrel{m shortcut}{=}
 	ext{one-step reduction of }F_0
]

on the literal Golden terminal code.

This agrees with the existing complete-code source theorem, which already
proves that ordinary `D_min` canonicity does not force the Shannon/entropy
source without a same-object decoder/equivalence theorem.

The remaining native theorem must therefore derive `Info` from the actual
history/memory/action object or prove a different explicit relation to
`F_0`; it cannot be obtained by merely subtracting the endpoint code lengths
1 and 2.

The accompanying exact checker
`check_dmin_info_obstruction.py` verifies all three typed gain comparisons
and the native Golden scalar exponents.

No geometric or finite-GR result is changed.

`GR_closed=false`.
