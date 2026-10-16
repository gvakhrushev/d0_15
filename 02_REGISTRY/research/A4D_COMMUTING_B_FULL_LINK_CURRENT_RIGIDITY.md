# Full-link commuting B: conserved response magnitude and spatial compensation

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input head: `53450f234a2a48d7b5e6a6bd1715ba2dcbac35f3`.
Certificate: `certificates/a4d_commuting_b_full_link_current_check.py`.
Companion joint-gap owner: `12afd2561da48a79031cdde9c91ead8aeb85c325`.
Companion warped-current owner: `66bbff7d6c2b5f78d2436d7eec5394f7a050c363`.
Status: exact nonlinear class theorem and analytic all-period source estimate;
the unrestricted noncommuting task remains open.

This extends the temporal-only commuting result to **all four link roles**,
with arbitrary full-four-dimensional dependence. Spatial links need not be
identities, small, smooth or phase repeated. The proof uses shared-face
currents and the local Lorentz Ward identity; it does not enumerate carriers.

## 1. Domain and source convention

Let `h=1/L` and `x in (Z/LZ)^4`. Keep the original action and its ten Gram
slots `(00,01,02,03,11,12,13,22,23,33)`, with the owner dual convention.
Set

\[
B=K_1+K_2+K_3,\qquad B^3=3B,
\qquad L_{x,r}=\exp(\alpha_r(x)B),\quad \alpha_r(x)\in\mathbb R.
\tag{1}
\]

The boost subgroup is isomorphic to the additive real line. Thus each link
has a unique real rapidity; there is no angular winding or finite-order
ambiguity. This is also the entire real identity-component Cayley B chart.
No uniform bound on the rapidities is needed below.

Require **all** right-trivialized connection Euler equations, including
variations outside B:

\[
E_K(S_h,L)=0,\qquad \Xi(S_h,L)=h^2\tau_h.
\tag{2}
\]

The source family is specified independently before solving the links.
On (2), the Ward/Gram section owner identifies Xi with the descended
metric Euler. The norm is the full unweighted physical owner sum

\[
\|\Xi\|_{\mathrm{owner},1}
=\sum_x\sum_{j=1}^{10}|\Xi_j(x)|.
\tag{3}
\]

For the flat theorem, `S=I`, `Q=eta`, and the designated comparator is the
exact root `L^sm=I`, with Xi=0. For the curved exclusion use the same fixed
warp and predeclared diagonal source bound as the existing boost owner.
Neither theorem prescribes a source from a computed candidate.

## 2. The full plaquette still has one exact constitutive pair

All four factors of a face commute, so

\[
P_{rs}(x)=\exp(F_{rs}(x)B),\qquad
F_{rs}=\alpha_r+D_r^+\alpha_s-\alpha_r(x+e_s)
=D_r^+\alpha_s-D_s^+\alpha_r.
\tag{4}
\]

Here `D_r^+ u(x)=u(x+e_r)-u(x)`. Hence F is an exact real two-cochain.
In particular, its sum on every periodic coordinate two-plane is zero.
Define

\[
z_{rs}=\frac{\sinh(\sqrt3 F_{rs})}{\sqrt3},\qquad
c_{rs}=\cosh(\sqrt3 F_{rs})
=\sqrt{1+3z_{rs}^2}\ge1.
\tag{5}
\]

The actual odd plaquette curvature is `z_rs B`. The literal face action is
`w_rs z_rs`, where `w_rs=<W_rs(S_x),B>`. Its right B derivative at either
incidence is exactly `+w_rs c_rs` or `-w_rs c_rs`.
Therefore for every role, without an amplitude expansion,

\[
E_K(x,r)[B]
=\sum_{s\ne r}\sigma_{rs}D_s^-[w_{ab}c_{ab}](x),
\quad (a,b)=(\min(r,s),\max(r,s)),
\quad \sigma_{rs}=\begin{cases}1&r<s,\\-1&r>s.\end{cases}
\tag{6}
\]

This is the same constitutive current as the temporal-only identity. Adding
commuting spatial links changes the actual face increments F; it does not
add a transport torque or change the constitutive law.

## 3. Flat Ward identity reduces the response to one scalar

At S=I the six face weights on B are `(1,1,1,0,0,0)`. The literal vertical
solder current, evaluated on the six Lorentz generators, is `V z`, with
face order `(01,02,03,12,13,23)` and

\[
V=\begin{pmatrix}
0&0&0&-1&-1&0\\
0&0&0&1&0&-1\\
0&0&0&0&1&1\\
-1&1&0&0&0&0\\
-1&0&1&0&0&0\\
0&-1&1&0&0&0
\end{pmatrix}.
\tag{7}
\]

Local Lorentz invariance gives `V z=0` whenever **every** E_K row vanishes.
The exact matrix has rank four, so at every physical site

\[
z_{01}=z_{02}=z_{03}=z(x),\qquad
(z_{12},z_{13},z_{23})=s(x)(1,-1,1).
\tag{8}
\]

The second vector has zero full solder current and zero Gram readout. The
first has readout

\[
\boxed{\Xi(x)=z(x)m,\qquad
m=(0,0,0,0,-1,1,1,-1,1,-1).}
\tag{9}
\]

Thus arbitrary invisible spatial circulation is allowed in this argument.
It is not called gauge and need not be classified. It cannot alter (9).
Extremizing the action only within the B subgroup is insufficient for (8);
the unrestricted Lorentz variations are essential.

## 4. Stationarity conserves the magnitude on the entire torus

Injectivity of the odd function in (5) turns (8) into
`F_01=F_02=F_03=F(x)`. Put `c(x)=sqrt(1+3z(x)^2)`. Equation (6) becomes

\[
\sum_{i=1}^3D_i^-c=0,\qquad D_0^-c=0.
\tag{10}
\]

For each time slice, the first equation states
`3c(x)=sum_i c(x-e_i)`. At a maximum all three predecessors have the same
value. Backward coordinate steps generate the connected spatial torus, so
the finite maximum principle makes c constant on that slice. The second
equation makes it constant across all time slices. Consequently

\[
\boxed{|z(x)|=a\quad\text{at every site, for one }a\ge0.}
\tag{11}
\]

If a>0, write `z=a epsilon`, `epsilon(x) in {+1,-1}`. Its sign cannot be
globally constant: (4) gives zero sum of F_01 on every coordinate
(0,1)-plane, whereas a constant nonzero sign would make that sum nonzero.
No uniqueness statement about the signs, links or invisible s is required.

Equation (11), rather than the microscopic pattern, is the surviving
response memory. The stationary #227 field has the nonconstant sign cycle
`(1,1,-1,-1)` and remains allowed. Conservation alone does not erase its
sitewise response; the independent source regularity does the final work.

## 5. Smooth sources give the original raw owner-sum limit

Suppose `tau_h` is sampled from a predeclared smooth periodic function, or
from a mesh-dependent periodic family with uniform derivative bound

\[
\max_{r=0,1,2,3}\|\partial_r^k\tau_{h,11}\|_\infty\le M_k.
\tag{12}
\]

If a>0, equations (2) and (9) give
`tau_h,11(x)=-(a/h^2) epsilon(x)`. A nonconstant periodic sign array has a
nonconstant cycle in at least one coordinate r. Every power of its cyclic
difference is nonzero: if `D_r^k epsilon=0`, periodicity first makes
`D_r^(k-1) epsilon` constant on each cycle; its cyclic sum is zero when
k>1, and induction gives `D_r epsilon=0`. Since differences of signs are
even integers,

\[
\|D_r^k\epsilon\|_\infty\ge2.
\tag{13}
\]

Repeated integration of the kth derivative of the independently specified
source gives `||D_r^k tau_h,11||_infinity<=h^k M_k`. Thus

\[
\frac{a}{h^2}\le\frac{M_k}{2}h^k,\qquad
\boxed{h^{-2}\|\Xi-\Xi^{\rm sm}\|_{\mathrm{owner},1}
=6L^4\frac{a}{h^2}\le3M_kh^{k-4}.}
\tag{14}
\]

The same inequality holds trivially for a=0. With a uniformly C5 source,
the requested **unweighted** normalized response tends to zero at rate
O(h). With a fixed C-infinity source it is O(h-infinity). No volume
normalization, reconstruction weakening, candidate expansion, small-link
assumption or connection inverse is used.

This proves the flat smooth-source image-collapse theorem for the entire
full-link real B subgroup. A merely bounded rough source does not satisfy
(12) and admits the mandatory nonzero #227 response control.

## 6. The curved bounded-source exclusion also survives every spatial B link

The companion
[all-role warped-current owner](A4D_COUPLED_BOOST_ALLROLE_CURRENT_RIGIDITY.md)
already owns this extension. Its constitutive map is replayed here as the
curved consistency control for the general current formula; the inequalities
below are consumed from that owner and its temporal parent.

Use the fixed nonconstant background

\[
S_h=\operatorname{diag}(1,1,f(hx_1),f(hx_1)),\quad
f(y)=1+\frac{1-\cos(2\pi y)}{50},\quad L\in4\mathbb N.
\tag{15}
\]

Its exact B face weights are `(f^2,f,f,0,0,0)`. Every spatial B face has
zero derivative in all three diagonal Gram slots. Therefore arbitrary
spatial B holonomies leave the already owned diagonal constitutive map
unchanged:

\[
\begin{pmatrix}z_{01}\\z_{02}\\z_{03}\end{pmatrix}
=T_f\begin{pmatrix}\Xi_{11}\\\Xi_{22}\\\Xi_{33}\end{pmatrix},\qquad
T_f=\begin{pmatrix}
f^{-2}&-1&-1\\
-f^{-1}&f&-f\\
-f^{-1}&-f&f
\end{pmatrix}.
\tag{16}
\]

The same exact temporal Euler identity follows from (6):

\[
E_K(x,0)[B]=\sum_iD_i^-[w_i\sqrt{1+3z_{0i}^2}],
\qquad w=(f^2,f,f).
\tag{17}
\]

Sections 8--9 of [the existing boost owner](A4D_COUPLED_BOOST_CURVED_REALIZABILITY.md)
use only (16)--(17), positivity and physical plane counts. Hence their
complete estimates apply to (1), with no source-transfer error:

\[
\boxed{\|E_K\|_{\mathrm{owner},1}
\ge\frac{102}{625}L^3-90M^2,\qquad
\|\tau_{h,\mathrm{diag}}\|_\infty\le M.}
\tag{18}
\]

Any exact stationary member also requires

\[
\boxed{\|\Xi_{\mathrm{diag}}\|_\infty
\ge\frac{\sqrt{22117}}{1875}.}
\tag{19}
\]

Thus bounded independent sources are infeasible on fine meshes in the
**whole** full-link B subgroup, including unrestricted spatial amplitudes.
For the preset vacuum (18) excludes a joint root at every allowed mesh.
Spatial compensation must leave this subgroup. This is source infeasibility
on (15), not a response-gap counterexample or an unrestricted task terminal.

## 7. Exact remainder when spatial transport does not commute

For arbitrary Lorentz links, retain a temporal face
`P_i(x)=L_0(x)L_i(x+e_0)L_0(x+e_i)^-1 L_i(x)^-1`. Define its literal left
momentum, with the actual weight at the face base, by

\[
M_i(x)[X]=\frac12\langle W_{0i}(S_x),XP_i+P_i^{-1}X\rangle.
\]

For a fixed right-link generator B set

\[
J_i(x)=M_i(x)[\operatorname{Ad}_{L_0(x)}B],
\]
\[
T_i(x)=M_i(x)[\operatorname{Ad}_{L_0(x)}
\{B-\operatorname{Ad}_{L_i(x+e_0)}B\}].
\tag{20}
\]

Differentiate both actual incidences of the temporal link. The outgoing
variation is the first momentum in (20); the incoming variation at
`y=x-e_i` is `-M_i(y)[Ad_(L_0(y)L_i(y+e_0)) B]`. Consequently

\[
\boxed{E_K(x,0)[B]
=\sum_iD_i^-J_i(x)+\sum_iT_i(x-e_i).}
\tag{21}
\]

This is an exact all-field identity. The torque vanishes when the spatial
links commute with B; in the full common B subgroup it reduces to (17).
For noncommuting spatial links, deleting it is incorrect. Moreover the
general momenta need not be reconstructed by the three diagonal source
slots. Both facts are retained in the finite quartic correlation system.
For a general generator section b at link endpoints, replace B in J_i(x)
by b(x+e_0), and replace the two occurrences in T_i(x) respectively by
b(x+e_0) and b(x+e_0+e_i). Equation (21) then evaluates E_K(x,0) on
b(x+e_0). This version is covariant under the actual local Lorentz frames;
a fixed coordinate B is not an additional gauge invariant observable.

The remaining closure is therefore control of this transported remainder
and the full response projection on the **exact noncommuting joint/source
equations**. The current proof imposes neither an extra conservation law
nor a spectral filter to remove it.

## 8. Verification and status

The companion
[all-role joint-gap owner](A4D_FLAT_ALLROLE_COMMUTING_B_SOURCE_COLLAPSE.md)
certifies the restricted physical symbol on the whole unit torus and proves
smooth-source collapse for log-O(h) fields. The current proof above is
independent of that inverse. It removes the small-field hypothesis and gives
the explicit unweighted owner-sum rate from C5 regularity. The two arguments
have compatible domains and preserve the same nonzero rough-source control.

The checker independently derives every flat Gram/vertical coefficient and
every warped diagonal coefficient from literal 4x4 face weights. Exact
full-lattice arrays have nonidentity links in all four roles and nonzero
spatial face curvatures. Every right B Euler projection, all local Lorentz
Ward rows and the diagonal inverse replay over Q. A separate noncommuting
array verifies (21) and rejects omission of the torque. The stationary
nonzero fast-response control is preserved; cyclic difference powers and
an open-path hostile control verify the scope of the source estimate.

The maximum principle, sign-integrality argument and all-mesh limit are the
analytic proofs in Sections 4--5, not extrapolations from finite grid tests.

```sh
python3 02_REGISTRY/research/certificates/a4d_commuting_b_full_link_current_check.py
```

Verdicts: `FULL-COMMUTING-B-FLAT-SMOOTH-SOURCE-IMAGE-COLLAPSE` and
`FULL-COMMUTING-B-WARPED-BOUNDED-SOURCE-EXCLUDED`.
The primary task remains `PARTIAL / OPEN`, Draft / `IN_PROGRESS`.
Noncommuting coupled centers, general coframes and the full nonlinear
source-image theorem are not covered. No Lean, selector, action, source,
BOOK/CORE or release claim is changed.
