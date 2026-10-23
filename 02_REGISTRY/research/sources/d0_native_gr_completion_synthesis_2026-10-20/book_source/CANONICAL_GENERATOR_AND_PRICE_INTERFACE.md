# The two-tick generator, saddle polarization, and complete-price interface

20 October 2026. Bounded connection for existing PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE` /
`native-programme-v1`. Read-only snapshot:
`24eebbda2a44896970271e03bf99b9518941234b`.

**Result.** The already-owned two-tick matrix determines an explicit
generating function. A partial Legendre transform gives a saddle for the
same map. The existing exact coframe dressing has an exact cotangent lift
that transports the WHOLE source graph, including preparation, history and
clock momenta. This supplies a precise stationary mechanism and removes
individual matching of higher compiler coefficients. It does not identify
the generator with literal Book price or supply native field trajectories.

## 1. Actual carrier and exact generator

`03_FORMALIZATION/D0/Dynamics/TwoTickSymplectic.lean` proves, from the
already-owned integer toral matrix,

\[
T=\begin{pmatrix}0&1\\1&-1\end{pmatrix},\quad
A=T^2=\begin{pmatrix}1&-1\\-1&2\end{pmatrix},\quad
A^TJA=J,\quad J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

It also proves the rational update and generating relations

\[
Q=q-p,\quad P=-q+2p,\qquad p=q-Q,\quad P=q-2Q.                 \tag{1}
\]

These phase coordinates are not the material quadratic \(q_i\), the
Brinkmann coordinates, or the inverse metric \(q_H\). The formal owner does
not select their physical interpretation. The real derivatives below are
the scalar extension of (1) on a chosen local lift, not an already-derived
continuous physical phase space or time interpolation.

On that lift set

\[
L(q,Q)=\tfrac12q^2-qQ+Q^2
      =\tfrac12(q-Q)^2+\tfrac12Q^2.                         \tag{2}
\]

The SAME map, without a new dynamical assumption, satisfies

\[
p=\partial_qL,\qquad P=-\partial_QL,\qquad
dL=p\,dq-P\,dQ.                                            \tag{3}
\]

On a connected lifted graph this fixes \(L\) up to a constant, once the
normalization of \(p\,dq\) is fixed. It does not fix physical \(\hbar\),
SI time, or the scale of Book Cost-minus-Info.

For a compatible lifted path,

\[
d\sum_{n=0}^{N-1}L(q_n,q_{n+1})
=p_0dq_0-p_Ndq_N+
\sum_{n=1}^{N-1}(-q_{n-1}+3q_n-q_{n+1})dq_n.                \tag{4}
\]

The owned two-tick recurrence therefore makes this generator stationary at
fixed endpoints. This stationarity follows from the specified map; it is
not an assumption that all physical fields minimize an action. Its
Dirichlet Hessian is \(3I\) minus nearest-neighbor adjacency, hence positive
definite.

**Winding remains part of the record.** Equation (2) is not a globally
periodic scalar on the torus. If output representatives obey
\(Q=q-p-m,\ P=-q+2p-n\), with fixed integers \(m,n\), the correct chart
primitive is

\[
L_{m,n}(q,Q)=L(q,Q)-mq+(2m+n)Q.                             \tag{5}
\]

Its derivatives give those actual representatives. Changes of winding or
chart are not smooth variations with these terms discarded. Equation (4)
uses a compatible real lift, or chart primitives retaining the corresponding
winding and boundary data.

## 2. A saddle from the same matrix

Solve \(P=-\partial_QL\) for \(Q=(q-P)/2\). Its partial Legendre transform is

\[
F_2(q,P)=L(q,Q)+PQ=\frac{q^2+2qP-P^2}{4},\qquad
p=\partial_qF_2,\quad Q=\partial_PF_2.                      \tag{6}
\]

Thus it generates exactly (1), while

\[
D^2L=\begin{pmatrix}1&-1\\-1&2\end{pmatrix}>0,\qquad
D^2F_2=\frac12\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\quad (D^2F_2)^2=\tfrac12I.                                \tag{7}
\]

The latter eigenvalues are \(\pm1/\sqrt2\). The already-owned matrix has a
genuine saddle generator in mixed endpoint coordinates.

This does not turn a scalar function's minimum into a saddle by a
coordinate diffeomorphism: the endpoint pairing \(PQ\) and the independent
endpoint variables have changed. A physical use requires that boundary
polarization and its actual price/record interpretation. For \(b=2m+n\),
the fixed-winding version is

\[
F_{2;m,n}(q,P)=\tfrac12q^2-mq-\tfrac14(q-b-P)^2.             \tag{8}
\]

Its Hessian is unchanged. No consumed owner equates either generator with
the complete Book price.

There is also an exact local Hamiltonian embedding of this SAME
two-dimensional matrix. The owned invariant form is
\(G=\left(\begin{smallmatrix}-2&1\\1&2\end{smallmatrix}\right)\).
Writing \(K=JG\), one has \(K^2=5I\) and \(A=\frac32I-\frac12K\).
For \(\phi=(1+\sqrt5)/2\),

\[
A=\exp\!\left[-\frac{2\log\phi}{\sqrt5}JG\right],\qquad
\mathcal H_A(z)=-\frac{\log\phi}{\sqrt5}\,z^TGz.             \tag{8a}
\]

Indeed \(\cosh(2\log\phi)=3/2\) and
\(\sinh(2\log\phi)=\sqrt5/2\); the Hamiltonian equation
\(\dot z=J\nabla\mathcal H_A\) yields \(A\) at unit mathematical time.
This is the real principal-logarithm embedding on the same local cover.
It is not a global continuous torus flow, a selected physical clock,
a four-dimensional gravitational Hamiltonian, or an identification with
Book price. In particular \(\phi\) here is the eigenvalue parameter of
the integer transfer, not an unproved identification with the Golden
gate's rotation angle.

## 3. Exact canonical transport of the full compiler normal form

The owned coframe-equivalence theorem applies to

\[
S(y,\zeta)=B(\zeta)+\sum_iw_i(\zeta)t_i(y)
             +t(y)^TH(y,\zeta)t(y),\qquad w_i\ne0,           \tag{9}
\]

where independent coframe radial fields satisfy
\(Z_it_j=2\delta_{ij}t_j\). The internal variables \(\zeta\) are independent
of those radial fields, and \(t\) is independent of \(\zeta\). Its exact
shell-fixing local diffeomorphism is

\[
\Theta(y,\zeta)=(F(y,\zeta),\zeta),\qquad
e_i\mapsto\sqrt{1+(Ht)_i/w_i}\,e_i,\qquad
S=S_0\circ\Theta,\quad S_0=B+\sum_iw_it_i.                  \tag{10}
\]

All shared links, matter coordinates and retained internal records remain.
In the actual vacuum full-ledger application, the complete stopping/compiler
law supplies a local scalar \(F_N(f_i,\zeta)\) with nonzero derivative
\(c_i(\zeta)\) at zero. Its higher-order remainder has this form. Equivalently,

\[
e_i\mapsto
\sqrt{\frac{F_N(f_i,\zeta)-F_N(0,\zeta)}
             {c_i(\zeta)f_i}}\,e_i
\]

has smooth limiting factor \(1\). This consumes the particular vacuum
ledger chart; it does not assert the normal form for bare full HJR or
arbitrary sourced matter. The baseline \(B(\zeta)\) and every moving-weight
source remain.

Here is the precise connection to the stationary cotangent-relation owner.
Write \(A_y=D_yF,\ C=D_\zeta F\). Where \(\Theta\) is locally invertible,
its full cotangent lift is

\[
\widehat\Theta:
(y,\zeta;\pi_y,\pi_\zeta)\longmapsto
\left(F,\zeta;\,
 \Pi_y=A_y^{-T}\pi_y,\,
 \Pi_\zeta=\pi_\zeta-C^TA_y^{-T}\pi_y\right).                \tag{11}
\]

Direct substitution gives the exact Liouville identity

\[
\widehat\Theta^*(\Pi_y\,dF+\Pi_\zeta\,d\zeta)
                  =\pi_y\,dy+\pi_\zeta\,d\zeta,            \tag{12}
\]
and consequently
\[
\widehat\Theta(\operatorname{graph}dS)
                         =\operatorname{graph}dS_0.        \tag{13}
\]

No preparation Hessian inverse or nondegeneracy is used. The zero-section
intersections and the full stationary Hessian inertia are preserved. The
\(C^T\Pi_y\) term is essential: freezing the dressing while varying a clock
or preparation loses a real source.

This is an exact canonical relation on the entire configuration/history
space. If \(\Theta\) is nonlocal, it is not automatically a causal per-tick
conjugacy or an admitted native writer. No physical implementation of the
coordinate change is free or inferred. At the source-graph level, however,
the full nonlinear ledger transports without separately matching every
higher coefficient. A price-faithful stationary realization of \(S_0\),
including \(B(\zeta)\), would have an exactly equivalent generating family
for \(S\). Admitting the corresponding native realization remains a
separate requirement. The identity never sets \(dB\) to zero.

## 4. The moving coframe shear and its boundary control

The current field-writer owner gives the original Brinkmann dictionary

\[
e_H=\begin{pmatrix}1&0\\H/2&1\end{pmatrix},\qquad
F_H=e_H^{-1}F_0.
\]

The shear \(S_H=e_H^{-1}\) satisfies \(S_H^TJS_H=J\).
Thus the required moving positive coordinate pairing is algebraically
compatible with symplectic transport. Identifying this coordinate plane
with physical toral phase coordinates is still an extra map; equal
dimension is insufficient.

A useful exact control prevents this kinematic fact from being mistaken
for bulk gravitational dynamics. For endpoint frames,

\[
A_n(H)=S_{H_{n+1}}AS_{H_n}^{-1},
\]

the generator on compatible lifted charts is

\[
L_H(q_n,q_{n+1})=L(q_n,q_{n+1})
 -\tfrac14H_nq_n^2+\tfrac14H_{n+1}q_{n+1}^2.               \tag{14}
\]

Its extra terms telescope, so this generator has zero derivative along
interior variations of the lower-shear parameter \(H\). This is correct
canonical covariance. It is also compatible with the original Palatini
action being constant along the common-null \(H\)-family. These are NOT
the independent normal coframe variations: (14) does not evaluate the
\(e_v^+\) row or establish its vanishing.

The original all40 owner supplies the additional, independent test. Its
normalized normal coframe source is
\(-\frac12\Delta_h^\perp H-2\lambda_-|D_u^+\Psi|^2\).
For a buffered profile \(H_E+c(x^2+y^2)\chi\), it is \(-2c\) on a
unit-coframe variation supported where \(\chi=1\), with the original
overall normalization retained. It is nonzero for \(c\ne0\).
A proposed canonical field/price map must realize and evaluate that
normal variation separately. The lower-shear identity alone supplies
neither that source nor a contradiction to it; it proves only the
endpoint nature of the specified \(H\)-frame change.

## 5. One concrete remaining interface: the priced generating primitive

Once ACTUAL native phase input/output records and their endpoint
polarization are supplied, the complete-price question has a finite test.
Let \(\ell\) be the genuinely charged local kernel, including its declared
Info and boundary convention. For the owned two-tick step in a fixed
winding chart, a priced primitive at fixed scale \(\gamma\ne0\) requires

\[
\partial_q\ell=\gamma(q-Q-m),\qquad
\partial_Q\ell=\gamma(-q+2Q+2m+n).                          \tag{15}
\]

On a connected chart this is equivalent to
\(\ell=\gamma L_{m,n}+b(\zeta)\). Every \(D_\zeta b\) source remains.
A moving scale contributes its real derivatives. Momenta must be the
actual native input/output quantities; defining them as price derivatives
and then calling them native is not a proof of (15).

For a field-bearing step, the corresponding test on its actual graph is
\(d\ell=\pi_{\rm in}\,dx_{\rm in}-\pi_{\rm out}\,dx_{\rm out}
+r\,d\zeta\), with the genuine independent internal sources \(r\) retained.
Alternatively those internal coordinates must themselves have an admitted
canonical extension. Once this identity is proved for a real execution,
composition cancels intermediate momenta as in (4); the internal terms
remain until their actual equations are solved. Stationarity in the covered
endpoint coordinates follows from native momentum matching, rather than a
full-field minimum postulate. Consuming all40+2 still requires the admitted
map to lift the original 16 coframe, 24 proper-link and two matter
directions and to respect the fixed collar and real terminal constraints.

The actual full compiler owner supplies the scalar law

\[
S_{\rm CQ}=C_{\rm pre}-H_{\rm pre}
 +\alpha[\mu-H_T-\beta h_\phi(q)]E_N(\beta q),
\]

not the native canonical relation (15). Its absolute Book-mean binding
\(\theta H-J_{\rm abs}\) is a separately typed quantity. Equation (11)
transports a proved realization of either with its own complete baseline;
it does not identify them or provide an unowned cancellation of
\(dJ_{\rm abs}\).

This gives one checkable next interface on one executed programme. Neither
the constrained-Hamiltonian passport, the \(\mathbb F_2\) branch symplectic
form, nor a formal Legendre transform alone supplies it.

## Sources and bounded validation

All paths are relative to `gvakhrushev/d0_15`; the Git blobs were read
at the stated snapshot.

| Consumed owner | Git blob |
|---|---|
| `03_FORMALIZATION/D0/Dynamics/ToralAutomorphism.lean` | `d6c7789c4cc55c24dc27de59acf574c8e1b20d36` |
| `03_FORMALIZATION/D0/Dynamics/TwoTickSymplectic.lean` | `e5b35dd66cf3be3158ad662217e5ae5d7a5fe205` |
| `03_FORMALIZATION/D0/Foundation/BranchSymplecticForcing.lean` | `027f552c4b14c917c307b32b00bf12ab3c29719c` |
| `03_FORMALIZATION/D0/Bridge/ConstrainedHamiltonianEmbeddingPassport.lean` | `0e2e82767b15ee01eff3b00fb1f424a957d3f197` |
| `02_REGISTRY/research/sources/d0_relational_coherent_synthesis_2026-10-20/coframe_equivalence.md` | `0b62260970a6ac8712d7989cf22897a5bd17dd0e` |
| `02_REGISTRY/research/A4D_STATIONARY_SOURCE_COTANGENT_RELATION.md` | `4b008f7e63a050c64295d6b196582d2601499dad` |
| `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_FIELD_WRITER_BRIDGE.md` | `fa59e9f59e061e6bcda0f05f29abed1e641f8ebb` |
| `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/stationary_information/STATIONARY_EXECUTION_BRIDGE.md` | `15d24f331ccf4328c3a48bba52fc825fa00588dd` |
| `02_REGISTRY/research/sources/d0_global_result_composition_2026-10-20/FULL_PRICE_COMPOSITION.md` | `b0d4483c42e4ac8281603b1459c1f2464da1fff9` |
| `02_REGISTRY/gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md` | `050ee972efa0f2ae37206b2ef9e3b4122dbac204` |

The adjoining standard-ECMAScript checker uses exact BigInt rationals.
It checks the type-I/type-II equations, winding corrections, Hessian
inertia, endpoint shear, and an off-shell full cotangent/source lift with
nonzero history mixing. Hostile omissions of the Legendre pairing,
winding, one endpoint term and the history-momentum correction fail as
intended. This validates the new finite compositions, not native price
admission or old GR/compiler/Lean suites. The executed environment was
the JavaScript V8 tool runtime; no Python or Lean run is claimed.
