# Full commuting Y-plane rigidity: variable amplitude cannot curve the metric

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.  
Depends on: `A4D_Y_PLANE_SPATIAL_RIGIDITY.md` and the exact pure-Y transport owner.  
Certificate: `certificates/a4d_y_plane_variable_amplitude_rigidity_check.py`.  
Status: exact nonlinear class reduction; not a task-level terminal.

## 1. The remaining loophole in the plane class

The spatial-rigidity theorem allowed an arbitrary common spatial column
(w(x)) but held the real Y Cayley amplitude fixed.  In principle a varying
amplitude could have cancelled the coframe forcing and produced a genuinely
curved exact joint vacuum.

It cannot.

For the entire canonical spacelike-plane Y class, the literal independent-edge
connection equations force the amplitude to be constant on the connected
even carrier.  The previous spatial-rigidity theorem then forces the only
remaining coframe variation to be integrable.  Consequently every smooth
nondegenerate continuum realization of this full commuting class is locally
flat.

This removes a whole nonlinear completion class, not one Fourier sector.

## 2. General field

Use

[
S(x)=igl(e_0, w(x), w(x)+u, w(x)+vigr),
]

with

[
u=(0,a,b,0)^T,qquad v=(0,c,d,0)^T,qquad
Delta=ad-bc
e0.
]

Nondegeneracy is

[
det S(x)=Delta,w_3(x)
e0.
]

On every even site place a real Cayley amplitude (A(x)).  Role 0 carries

[
C_{J_{12}}(A(x))
]

on phase 0 and its Lorentz inverse on phase 2; odd phases and Roles 1,2,3
carry the identity.  No smoothness, fixed sign or Fourier support of (A)
is assumed.

The common column (w(x)) is also arbitrary before imposing the equations.

## 3. Six exact transport equations survive arbitrary coframe variation

For each spatial role (s=1,2,3), two selected boost variations of the
**full literal edge Euler equation** compare the two even amplitudes at the
ends of a physical graph move.

Let (x,yinmathbb R) denote those two amplitudes and write

[
(X_s,Y_s)=
egin{cases}
(a-c,b-d),&s=1,\
(c,d),&s=2,\
(a,b),&s=3.
end{cases}
	ag{1}
]

For the moves (e_s-e_0), the two rows are, up to one common nonzero factor,

[
(x-y)left[
X_s(xy-4)+2Y_s(x+y)
ight],
]

[
(x-y)left[
Y_s(xy-4)-2X_s(x+y)
ight].
	ag{2}
]

For the moves (e_s+e_0), the signs of the second terms reverse:

[
(x-y)left[
X_s(xy-4)-2Y_s(x+y)
ight],
]

[
(x-y)left[
Y_s(xy-4)+2X_s(x+y)
ight].
	ag{3}
]

The certificate derives (2)--(3) from all incident plaquettes with independent
coframe differences retained.  The omitted common factor is a sign times

[
rac{2w_3}{(x^2+4)(y^2+4)},
]

hence is nonzero on the declared nondegenerate coframe.

No derivative of (w), no lattice period and no Fourier character appears in
the two amplitude brackets.

## 4. Real rigidity of each edge

Assume (x
e y).  Vanishing of (2) makes

[
egin{pmatrix}
X_s&2Y_s\
Y_s&-2X_s
end{pmatrix}
inom{xy-4}{x+y}=0.
]

Its determinant is

[
-2(X_s^2+Y_s^2).
]

For (3) the determinant is the opposite nonzero number.  Since
(Delta
e0), all three real vectors in (1) are nonzero: (u
e0),
(v
e0), and (u-v
e0).  Therefore

[
xy=4,qquad x+y=0.
]

Over the reals this would give (-x^2=4), impossible.  Hence

[
oxed{x=y}
	ag{4}
]

on every one of the six graph moves.

These moves generate the complete even-sum lattice.  The exact integer
minor gcd is 2, equal to its index in (mathbb Z^4).  Thus on every
periodic (Lin4mathbb N) carrier,

[
oxed{A(x)equiv A_0.}
	ag{5}
]

This reproduces the old sign-free pure-Y rigidity but now with the whole
varying plane coframe present in the literal equations.

## 5. Return to the spatial equations

After (5), no amplitude gradient remains to compensate the coframe.  Apply
the exact spatial-rigidity theorem at the constant real value (A_0).  It
gives

[
D_1^-w=D_2^-w=D_3^-w.
	ag{6}
]

Therefore

[
w(x_1,x_2,x_3)
=widetilde w(x_1+x_2+x_3!!pmod L).
]

Together with the independently allowed time-column dependence, every smooth
continuum realization has the exact local primitive

[
X(y)=Q(y_0)+W(y_1+y_2+y_3)+u,y_2+v,y_3
]

and hence

[
S=dX,qquad g=S^Teta S=X^*eta.
]

Thus

[
oxed{operatorname{Riem}[g]=0,qquad G[g]=0.}
	ag{7}
]

## 6. Consequence for the #310 closure search

The entire natural completion of the owned finite-amplitude Y microstructure
inside a common spacelike difference plane is now classified:

[
oxed{
	ext{full joint stationarity}
Longrightarrow
	ext{constant Y amplitude + integrable coframe}
Longrightarrow
	ext{locally flat metric}.
}
]

So this class can neither provide a curved zero-source counterexample nor
carry a new horizontal (h^2) response over a curved smooth background.

This is exactly the class-cutting architecture required by the M1 response
quotient: varying amplitude and varying coframe do not create new cases to
enumerate; the full equations collapse the whole class back to one flat
observable class.

By Role permutation and proper-Lorentz covariance the same statement applies
to the corresponding single-role/simple-spacelike-plane presentations.
What remains outside this theorem is genuinely **coupled-role / non-simple
joint-vacuum structure**, not another choice of Y amplitude, sign, wavelength
or common-column envelope.

## 7. Replay

```bash
python3 02_REGISTRY/research/certificates/a4d_y_plane_variable_amplitude_rigidity_check.py
python3 02_REGISTRY/research/certificates/a4d_y_plane_spatial_rigidity_check.py
```

Both certificates use literal independent-edge Euler rows and exact symbolic
arithmetic.

Verdict:

[
oxed{	exttt{A4D-Y-PLANE-FULL-CLASS-RIGIDITY-EXACT}}
]

No action modification, selector, Fourier cutoff, source assignment,
connection uniqueness, BOOK/CORE promotion or task-level terminal is asserted.
