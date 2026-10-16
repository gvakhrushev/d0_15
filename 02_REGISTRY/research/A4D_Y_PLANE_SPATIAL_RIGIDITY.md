# Exact spatial rigidity of the Y-plane joint vacuum

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.  
Input: `A4D_Y_SLOW_JOINT_CONTINUATION.md` and its literal all-row plane checker.  
Certificate: `certificates/a4d_y_plane_spatial_rigidity_check.py`.  
Status: exact nonlinear class reduction; not a task-level terminal.

## 1. Question

The existing all-order Y owner proves a large constant-coframe full joint
vacuum and an exact varying extension when only the time column changes
between neighboring time layers.  That varying metric is macroscopically
flat.  A possible task-level negative route would be much stronger: vary the
common spatial column as well, keep the exact Y microstructure, and obtain an
exact joint vacuum on a genuinely curved smooth metric.

This note closes that route for the whole canonical spacelike-plane Y class.
The full independent-edge equations force the spatial coframe variation to be
integrable; every smooth continuum realization is locally a pullback of
Minkowski metric.

## 2. Generalized coframe and exact Y links

Use the canonical normal form of the existing plane owner.  Let

[
q=e_0,qquad
u=(0,a,b,0)^T,qquad
v=(0,c,d,0)^T,qquad
Delta=ad-bc
e0.
]

At each site take the four coframe columns

[
oxed{
S(x)=igl(q, w(x), w(x)+u, w(x)+vigr).
}
	ag{1}
]

The common spatial column (w(x)) is allowed to be an arbitrary
time-independent periodic lattice field before imposing stationarity.

On Role 0 use the exact period-four Y wave

[
(W_0,W_1,W_2,W_3)=(U(z),I,U(z)^{-1},I),
]

where (U(z)) is the Cayley transform of (J_{12}); all other Role links
are identity.  The amplitude (z) is arbitrary real.  This is the same
literal link family as the all-order plane owner, not a linearization.

Write backward differences

[
d_s(x)=w(x-e_s)-w(x),qquad s=1,2,3.
	ag{2}
]

## 3. Full independent-edge equations

Differentiate the actual action with respect to every one of the six Lorentz
generators on each Role edge.  Spatial Roles 1,2,3 give, exactly,

[
egin{array}{lll}
d_2^3=d_3^3,&d_2^2=d_3^2,&d_2^1=d_3^1,\
d_1^3=d_3^3,&d_1^2=d_3^2,&d_1^1=d_3^1,\
d_1^3=d_2^3,&d_1^2=d_2^2,&d_1^1=d_2^1.
end{array}
	ag{3}
]

Thus

[
d_1^j=d_2^j=d_3^j,qquad j=1,2,3.
	ag{4}
]

These rows contain no (z) and no plane-shape coefficient.

For the remaining internal component (j=0), two Role-0 boost equations act
on ((d_1^0,d_2^0,d_3^0)).  The three (2	imes2) minors of their exact
coefficient matrix are

[
oxed{
rac{4Delta}{z^2+4},qquad
-rac{4Delta}{z^2+4},qquad
rac{4Delta}{z^2+4}.
}
	ag{5}
]

Because (Delta
e0) and (zinmathbb R), this matrix has rank two.
The vector ((1,1,1)) is in its kernel, hence its kernel is exactly that
line:

[
d_1^0=d_2^0=d_3^0.
	ag{6}
]

Combining (4) and (6),

[
oxed{D_1^-w=D_2^-w=D_3^-w.}
	ag{7}
]

Conversely, substituting one common difference vector into all literal edge
rows makes every one vanish.  The solder Euler rows remain zero identically
for arbitrary local (w), by the original Y-plane wedge identity.  Therefore
(7) is the exact spatial stationarity condition inside this generalized
class, not merely a necessary first jet.

No Fourier character or lattice size enters (3)--(7).

## 4. Periodic classification

On a connected (L^3) spatial torus, (7) is equivalent to invariance under

[
e_1-e_2,qquad e_1-e_3.
]

Hence there is a cyclic function (widetilde w) such that

[
oxed{
w(x_1,x_2,x_3)=
widetilde w(x_1+x_2+x_3pmod L).
}
	ag{8}
]

This classifies all spatial common-column fields compatible with the exact
Y links in (1).

The earlier exact theorem allowing neighboring time columns remains
orthogonal to (8): one may also take a time column (q=q(x_0)).  The two
allowed dependences therefore separate into one temporal and one diagonal
spatial coordinate.

## 5. Continuum metric is necessarily flat

Let a smooth realization have

[
q=q(y_0),qquad
w=w(s),qquad
s=y_1+y_2+y_3,
]

with fixed (u,v).  Locally choose primitives (Q'(y_0)=q(y_0)) and
(W'(s)=w(s)), and define the internal Minkowski-coordinate map

[
X(y)=Q(y_0)+W(y_1+y_2+y_3)+u,y_2+v,y_3.
	ag{9}
]

Then

[
partial_0X=q,quad
partial_1X=w,quad
partial_2X=w+u,quad
partial_3X=w+v.
]

Thus the coframe (1) is exactly (dX).  Wherever it is nondegenerate,

[
oxed{g=S^Teta S=X^*eta}
	ag{10}
]

and its Riemann and Einstein tensors vanish locally.

Global affine periods of (X) on the torus do not affect this local
curvature statement.

Consequently no member of this entire exact finite-amplitude Y-plane class
can furnish the missing curved smooth-background vacuum counterexample.

## 6. Why this matters for the response quotient

The smooth-source blow-up reduction in this PR shows that finite-amplitude
microscopic limits of an admissible sequence land in constant-coframe full
joint vacua.  The present theorem then removes a large natural continuation
class of the owned Y vacuum without any spectral census:

[
oxed{
	ext{Y-plane full joint continuation}
 + 	ext{full edge stationarity}
 Longrightarrow 	ext{flat continuum coframe}.
}
]

The result is stronger than observing that one previously constructed varying
example is flat: it proves that arbitrary spatial common-column variation in
the canonical plane ansatz is forced back to the integrable diagonal form.

It does not classify coupled-role vacua, arbitrary non-plane entire joint
vacua, or the horizontal second-order response of every component of the
joint-vacuum bundle.  Those remain the only possible locations for a
genuinely curved extra response branch.

## 7. Replay

```bash
python3 02_REGISTRY/research/certificates/a4d_y_plane_spatial_rigidity_check.py
```

The checker imports the existing literal all-row Y action routines, keeps
(z,a,b,c,d) symbolic, introduces independent incoming spatial differences,
and verifies (3) and the exact minors (5).  No floating arithmetic is used.

Verdict:

[
oxed{	exttt{A4D-Y-PLANE-SPATIAL-RIGIDITY-EXACT}}
]

No action change, source assignment, selector, connection uniqueness,
BOOK/CORE promotion or #310 terminal is asserted.
