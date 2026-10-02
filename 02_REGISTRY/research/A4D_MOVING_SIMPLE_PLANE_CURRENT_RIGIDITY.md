# A4D moving simple-plane current rigidity

Task: \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, Draft PR #310.  
Certificate:
\`certificates/a4d_moving_simple_plane_current_rigidity_check.py\`.  
Parent exact current/plane owner:
\`A4D_Y_SLOW_JOINT_CONTINUATION.md\`.

Status: exact two-layer shared-link theorem for the canonical one-coordinate
simple-plane class.  It removes a varying-plane gluing class without a Bloch
census.  It is not the unrestricted four-dimensional task terminal.

## 1. Setup

Use one active lattice role, called role 0.  At two neighboring layers choose
nondegenerate coframes whose three spatial columns have the canonical form

\[
s_1=e_3,\qquad
s_2=e_3+(0,a,b,0)^T,\qquad
s_3=e_3+(0,c,d,0)^T
\]

and

\[
s^-_1=e_3,\qquad
s^-_2=e_3+(0,A,B,0)^T,\qquad
s^-_3=e_3+(0,C,D,0)^T .
\]

Their oriented difference-plane areas are

\[
\Delta=ad-bc,\qquad \Delta_-=AD-BC.
\]

Take the four-phase temporal links

\[
(U(z),I,U(z)^{-1},I),\qquad
(U(y),I,U(y)^{-1},I)
\]

on the two layers, where \(U(q)\) is the Cayley rotation of \(J_{12}\).
All spatial links are identity.

This is exactly the shared-link geometry of the existing simple-plane theorem,
but now the incoming and outgoing spatial difference planes are independent.

## 2. Metric response is zero before imposing connection stationarity

For every base phase, the six based face curvatures are simple-plane
curvatures proportional to the same local \(J_{12}\).  The complementary
area combination is the local simple bivector \(u\wedge v\).  The middle
star pairing therefore contains the repeated plane

\[
(u\wedge v)\wedge(u\wedge v)=0,
\]

and its unrestricted coframe derivative repeats one of the two plane vectors.

The checker differentiates all sixteen coframe coordinates and proves

\[
\boxed{E_Q=0}
\tag{1}
\]

at the current layer for arbitrary \(a,b,c,d,A,B,C,D,y,z\).
It also proves every temporal-link Euler row is zero.

Thus this class can only fail the joint equations through the shared
**spatial-link current**, not through a hidden metric response.

## 3. Exact spatial current equations

At one phase the only nonzero spatial-link rows are the first two boost
components, plus one oriented-area row.  For roles 3 and 2 they can be written
compactly with

\[
M(q)=
\begin{pmatrix}
q&2\\
2&-q
\end{pmatrix},
\qquad
M(q)^2=(q^2+4)I.
\]

Let

\[
u=\binom ab,\quad v=\binom cd,\qquad
u_-=\binom AB,\quad v_-=\binom CD.
\]

The role-3 and role-2 equations are exactly

\[
(y^2+4)M(z)u=(z^2+4)M(y)u_-,
\tag{2}
\]
\[
(y^2+4)M(z)v=(z^2+4)M(y)v_-.
\tag{3}
\]

The independent role-1 area row is

\[
\boxed{\Delta-\Delta_-=0.}
\tag{4}
\]

The remaining role-1 boost rows are consequences of the same transport once
(2)--(4) hold; the checker verifies them directly in the two stationary
alternatives below.

Equations (2)--(3) give

\[
u=R(z,y)u_-,
\qquad
v=R(z,y)v_-,
\tag{5}
\]

where

\[
R(z,y)=\frac{M(z)M(y)}{y^2+4}.
\]

Its exact conformal factor is

\[
R(z,y)^TR(z,y)
=
\frac{z^2+4}{y^2+4}I,
\qquad
\det R(z,y)=\frac{z^2+4}{y^2+4}.
\tag{6}
\]

Consequently

\[
\Delta=
\frac{z^2+4}{y^2+4}\Delta_-.
\tag{7}
\]

Combining (4) and (7) yields

\[
\boxed{(z^2-y^2)\Delta_-=0.}
\tag{8}
\]

On the nondegenerate coframe chart \(\Delta_-\ne0\),

\[
\boxed{z^2=y^2.}
\tag{9}
\]

This is the exact conserved-current rigidity.

## 4. The two stationary transitions

If \(y=z\), then

\[
R(z,z)=I.
\]

The two spatial difference vectors are unchanged.

If \(y=-z\), then

\[
R(z,-z)=
\frac1{z^2+4}
\begin{pmatrix}
4-z^2&4z\\
-4z&4-z^2
\end{pmatrix}
\in SO(2).
\tag{10}
\]

The checker substitutes both alternatives into **every** spatial-link Euler
row and obtains zero exactly.

Therefore an exact stationary transition preserves

\[
u^Tu,\qquad v^Tv,\qquad u^Tv,\qquad \Delta
\tag{11}
\]

and preserves the Cayley amplitude magnitude.  The apparent second
alternative is only a common internal spatial rotation of the two difference
vectors together with the sign change of the four-phase amplitude.

Hence the full spatial difference-plane Gram is a conserved quantity of the
stationary current.

## 5. M1/source-image consequence

Equation (1) says that the whole class is response-null before the connection
equation is imposed.  Equations (8)--(11) say that imposing connection
stationarity forbids that response-null packet from carrying a changing
spatial Gram.

Thus a new microscopic representative in this class does **not** create a
new source-image branch.  It either

1. violates \(E_K=0\); or
2. propagates by an isometry of the spatial difference plane and keeps
   \(E_Q=0\).

This is exactly the conservation-law version of the M1 reduction: the
microscopic phase representative is forgotten, while the conserved spatial
Gram/current is retained.

## 6. One-coordinate continuum corollary

After a layer-dependent internal \(SO(2)\) frame alignment, every stationary
transition in this canonical class has a fixed spatial Gram.  The parent
simple-plane theorem already allows independent neighboring time columns
when the spatial columns are fixed.

A smooth one-coordinate continuum metric obtained from such aligned data has
the ADM form

\[
ds^2=N(t)^2dt^2-
(dx-\beta(t)dt)^T H (dx-\beta(t)dt)
\tag{12}
\]

with constant positive spatial matrix \(H\).  The substitutions

\[
y=x-\int\beta(t)\,dt,
\qquad
\tau=\int N(t)\,dt
\]

make (12) a constant Lorentz metric.  Therefore this response-null
simple-plane transport cannot realize a genuinely curved one-coordinate
continuum background.

This is a continuum interpretation of the exact conserved spatial Gram, not
a claim of a finite lattice diffeomorphism gauge.

## 7. Scope

The checker fixes a canonical common spacelike 12-plane for the two-layer
algebra; the second stationary alternative supplies the exact internal
rotation within that plane.  The theorem does not classify transitions in
which the spatial difference plane changes to a genuinely different
Lorentz 2-plane before stationarity is imposed.

It also does not classify arbitrary coupled center mixtures, all four active
roles, or a full four-dimensional background.  Those remain in the finite
degree-2/3/4 correlation/source-image problem.

What is closed here is the first nontrivial moving-plane gluing class:

\[
\boxed{
\texttt{A4D-MOVING-SIMPLE-PLANE-CURRENT-RIGIDITY}
}
\]

No new action, selector, torsion condition, spectral cutoff or task-level
Einstein terminal is introduced.

## Replay

\`\`\`sh
python3 02_REGISTRY/research/certificates/a4d_moving_simple_plane_current_rigidity_check.py
\`\`\`
