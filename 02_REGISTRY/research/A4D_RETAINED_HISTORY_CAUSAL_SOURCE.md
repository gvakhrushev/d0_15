# Actual retained history reads a causal-cone source

16–17 October 2026. Same Draft #334. Consumer: the retained-program/source
interface after [the causal metric bridge](A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE.md).

**Result.** One existing nonblank Julia/Walsh label, with both golden ports
retained, defines an actual first-exit event on the permanent round records.
Its probability is of order h² over O(h^-2) rounds. On the existing smooth
LC cone family its h^-2 limit has a nonzero cone source, even though the
continuum sum D and its spectral H+J price lose this cone. No reference
tensor, extra gate, action term, reset, or new price is installed.

This is an actual conditional matrix-program readout. Physical generation
of its onsite Julia gates and the price assigned to this particular history
remain open. It is not the original fixed-source E_Q comparator terminal,
all ten Einstein rows, or a full stationary geometry/preparation family.

## 1. The same32 labels and their exact retained contrasts

Use the [full Lorentz positive-adjoint owner, §2](A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md).
In its fixed positive Hilbert frame, with all16 occupation states, let

```text
P_r=C_r M_r shift_r,  d_h=h^-1 sum_r(P_r-C_r),
D_h=d_h+d_h*,  Delta_h=D_h²,
J(X)=[[X,sqrt(I-XX*)],[sqrt(I-X*X),-X*]].                 (1)
```

The strict contraction domain supplies both positive defect roots. For each
of the four roles retain, in that order, the words
`J(P_r),J(P_r)*,-J(C_r),-J(C_r)*`, each repeated twice. Thus the actual
label is `(role:2 bits,word:2 bits,duplicate:1 bit)`. The existing32-label
uniform preparation/unpreparation is the Sylvester Walsh matrix S=H32/sqrt32,
and `Q=S SELECT S`. The coefficient qubit is retained.

There are exactly four role-only Walsh characters, not sixteen arbitrary
role sign choices. In binary label order their output indices are

```text
0:  (+,+,+,+),   16: (+,+,-,-),
8:  (+,-,+,-),   24: (+,-,-,+).
```

Writing `0` for the complete blank label/coefficient input, put

```text
D_chi,h=h^-1 sum_r chi_r(P_r-C_r+P_r*-C_r*),
A=Q_00=hD_h/16,
M_chi=Q_(0;chi,coefficient0)=Q_(chi,coefficient0;0)
     =hD_chi,h/16=M_chi*.                               (2)
```

Indeed each duplicate contributes twice, and the word-character00 sum
is `J(P)+J(P)*-J(C)-J(C)*`. Its coefficient00 block is
`P+P*-C-C*`. Thus (2) is a block identity for noncommuting inputs, using
the same unmeasured SELECT word. Coefficient10 defect blocks are not
silently removed from the rest of the instrument.

As a preliminary observation, cutting this label immediately after Q
reads `h² Tr(rho D_chi,h²)/(256 Tr rho)`. That prefix is not automatically
a permanent history: the following Q* can erase it. The actual event below
uses the final outputs of a whole golden round.

## 2. One actual round, then disjoint first-exit histories

For golden `a²=p`, `p+p²=1`, the existing comparator has

```text
W=Q*(I-2P_blank)Q,
K0=pI+p²W,   K1=ap(W-I),
B=P_blank K0 P_blank=I-2p²A²=I-alpha Delta_h,
alpha=c0 h², c0=p²/128.                                (3)
```

For a nonblank role label chi and coefficient0, the two final port
amplitudes are respectively `-2p² M_chi* A` and `-2ap M_chi* A`.
Their **union**, with neither port discarded, has input effect

```text
E_chi,h=4(p^4+p^3) A* M_chi M_chi* A
       =4p² A* M_chi M_chi* A
       =p²h^4 D_h D_chi,h² D_h / 16384.                 (4)
```

Ordering in (4) matters; D_h and D_chi,h generally do not commute.
For all output label/coefficient indices k, set
`F_k=P_blank Q |k><k| Q* P_blank`. Unitarity gives `sum_k F_k=I`.
Together with the blank amplitudes this proves completeness of all128
outcomes, not only of the displayed port union.

Define the retained event: rounds1 through j are the single complete blank
outcome; round j+1 has the nonblank label chi/coefficient0 and either
golden port; all later records are unrestricted. These are disjoint
projectors on the existing128^n round history. There is no repeated
measurement, reset or replacement of an old register. Later complete
unitary evolution sums to the identity in its effect. Therefore

```text
F_chi,n=sum_(j=0)^(n-1) B^j E_chi,h B^j,
q_chi,n=Tr(rho_h F_chi,n)/Tr rho_h.                     (5)
```

In particular, (5) is not `n E_chi,h`, an unconditional sum over every
round, or a power of one-frame feedback. If A annihilates an input, every
final chi amplitude annihilates it; a prefix signal alone would not prove
this permanent-history result. The positive occupied shell in §4 avoids
that zero-mode cancellation.

## 3. Exact clock limit and full source

Let `n_h` be the actual integer round count, `beta_h=2n_h alpha`, with
`beta_h=beta+O(h²)`, beta>0. For fixed finite selfadjoint D,D_chi,
the ordinary norm Riemann-sum limit of (4)–(5) is

```text
h^-2 F_chi,n -> L_chi,
L_chi=(1/256) integral_0^beta
 exp(-t Delta/2) D D_chi² D exp(-t Delta/2) dt,
Delta=D².                                              (6)
```

The coefficient follows from `p²/(32768 c0)=1/256`, not from fitting a
continuum source. For a normalized density supported at Delta=lambda>0
and commuting with D,

```text
Tr(rho L_chi)=(1-exp(-beta lambda)) Tr(rho D_chi²)/256.   (7)
```

The same result is an actual smooth-stencil matrix-element limit here.
Assume the C192 controlled proper-link/positive-adjoint class and uniform
ellipticity of [the heat/source owner](A4D_SECOND_ORDER_HEAT_REMAINDER.md),
with the exact parallel links, a fixed smooth finite-rank purification C0
on the same128 reference, and its sampled form normalizer. The graph
estimates give, uniformly for `j<=n_h`,

```text
||B_h^j||_(H_h^k -> H_h^k)<=C_k,
||B_h^j-exp(-j alpha Delta_h)||_(H_h^(k+4)->H_h^k)
 <=C_k j alpha²=O(h²).                                 (8)
```

The second estimate follows from scalar `0<=e^-x-(1-x/m)^m` bounds
and graph-norm equivalence; B_h is a nonnegative spectral contraction.
Smooth-core consistency `Delta_h-Delta0=O(h):H^(k+3)->H^k`, Duhamel
and uniform graph stability then imply

```text
sup_(j<=n_h)||B_h^j C0,h-exp(-j alpha Delta0)C0||_H_h^2
 <=Ch.                                                 (9)
```

For the order-two insertion one uses the corresponding H4 estimate
(and, safely, a bounded H12 input). Consequently
`D_chi,h D_h B_h^j C0,h` differs in Hilbert–Schmidt norm by O(h)
from its smooth counterpart, uniformly in j. Their norms stay bounded.
Each squared-norm summand in (5) thus has O(h) error after removing its
explicit h^4 factor. Since n_h=O(h^-2), multiplication by h^-2 leaves
O(h) total error; the time Riemann-sum error is O(h²).
Aliasing/sampling is controlled by the same smooth graph estimates, with
the additional Fourier-tail padding already covered by C192 rather than
only by the principal smooth-core H^(k+3) bound.
This proves (6) in the stated matrix elements with O(h) error.

One bounded smooth parameter derivative obeys the same estimate after
reserving additional graph derivatives. For this cone family the argument
is especially direct: Delta0 is independent of theta and
`delta Delta_h=O(h)` on smooth cores, so differentiating B_h^j gives
`-alpha sum_(l<j) B_h^l(delta Delta_h)B_h^(j-1-l)`, of order O(h).
No uniform estimate over arbitrary rough raw C0 field rows is inferred.

The source is fully normalized. At finite h and fixed integer n,

```text
delta q=Tr[delta rho (F-q I)+rho delta F]/Tr rho,
delta F=sum_j[(delta B^j)E B^j+B^j(delta E)B^j+B^jE(delta B^j)],
delta B^j=sum_(l=0)^(j-1) B^l(delta B)B^(j-1-l),
delta B=-alpha delta Delta-(delta alpha)Delta.           (10)
```

For (6), with H_t=exp(-tDelta/2) and V=D D_chi² D,

```text
delta L=(1/256)[(delta beta)H_beta V H_beta
 +integral_0^beta (delta H_t V H_t+H_t delta V H_t+H_t V delta H_t)dt],
delta H_t=-(1/2)integral_0^t H_(t-s)(delta Delta)H_s ds,
delta V=(delta D)D_chi²D+D{D_chi,delta D_chi}D+D D_chi²(delta D).
                                                               (11)
```

Use the same normalized formula as (10), replacing F by L. All adjoint,
endpoint pairing, coframe, observer and preparation jets enter D,D_chi,rho.
In the tested field variation p,h,n are fixed, hence delta beta=0. If a
real calibration depends smoothly on fields, its actual delta alpha and
`delta beta=2n delta alpha` belong to (10)–(11); the integer n itself is
not differentiated. This observable adds no hidden thermal Z: the global
Z of H+J remains in that price and has not been changed.
The factor1/256 in (6) and (11) uses exactly the owned relations
`A=hD/16`, `alpha=p²h²/128`. If a different field-dependent compiler
normalization is actually supplied, its resulting prefactor and its
derivative must also be retained; a delta-beta endpoint term alone would
not account for such a change. No such new calibration is made here.

## 4. Exact cone signal on the faithful full shell

Use the owned cone `e=s O01(theta(y))`, y=x2, s>1, on the period2pi torus.
All coordinate forms, exact proper LC transports and all16 components are
as in [the first matter-corrector owner](A4D_CONE_PREPARATION_FIRST_CORRECTOR.md).
After the constant positive isometry, `C_r=C_r^unit/s` and

```text
D0=s^-1 sum_r gamma_r partial_r, Delta0=-s^-2 sum_r partial_r²,
H_r=Gamma(M_r), J_r=C_r^unit H_r+H_r* I_r^unit,
sum_r C_r^unit H_r=0, sum_r J_r=0,
M2=theta' R01, M3=0.                                   (12)
```

For the **one actual** role character chi=(+,+,-,-),

```text
J_chi=-2J2=-2theta' gamma2 Gamma(R01),
Tr16 J_chi²=32(theta')².                                (13)
```

These are all-angle CAR identities, not an extrapolation from small theta.
The remaining Gram entries are
`Tr J0²=Tr J1²=4(theta')²[1+cos²(2theta)]`,
`Tr J2²=8(theta')²`, `Tr J0J1=-4(theta')² cos²(2theta)`,
and `Tr J0J2=Tr J1J2=-4(theta')²`.

Retain all eight first-shell momenta and the entire Fock density:
`rho0=P_Omega/128`, `lambda=1/s²`. Its purification is the original
full128-column faithful shell preparation. The kinetic part of D_chi has
squared expectation lambda. Opposite momenta cancel the kinetic/potential
cross term (the full16 trace also vanishes). Equations (12)–(13) give

```text
Tr(rho0 D_chi,0²)=lambda+(2/s²)<(theta')²>,
lim_(h->0) h^-2 q_chi,n
 =(1-exp(-beta/s²))[1+2<(theta')²>]/(256 s²).            (14)
```

Here <> is normalized torus average. By (8)–(9), (14) holds with O(h)
error and after a bounded smooth cone variation. Its actual cone Euler
density is

```text
E_theta=-(1-exp(-beta/s²)) theta''/(64 s²).              (15)
```

The same positive coefficient is independent of theta. This is a genuine
permanent-history source of the same matrix program. A constant SO4 rotation
has theta'=0 and is correctly invisible. Equation (15) compares just one
cone variation with the corresponding curvature row; it does not derive
all ten metric equations. For winding theta=my it is zero despite a nonzero
value of the readout, which also prevents a value-only stationarity claim.

There is an exact geometric consumer on this family. The owned Lorentz
curvature reading gives `I_EH[theta]=-2s²<(theta')²>`. Thus, writing L_chi
for the scalar limit in (14),

```text
L_chi[theta]-L_chi[constant]
 =-(1-exp(-beta/s²)) I_EH[theta]/(256 s^4).              (16)
```

At fixed s,beta its theta source is exactly (15). The coefficient is
calculated from the existing event and clock, not fitted to that row.
Scale/metric variations also differentiate the coefficient in (16).
This is one explicit history-to-curvature comparison on the named cone
family; it does not identify the full price with EH, produce all ten
metric rows, or select a Newton constant.

The unmodified faithful shell on this sampled LC family fails its actual
first amplitude corrector, as the linked owner proves. Formula (14) is
therefore a readout/source theorem, not a stationary preparation continuation.
The rank-balanced preparation work and independent source rows are retained.

## 5. What the present price does and does not read

For each individual final record, the exact effect has form
`4p³ A F_k A` on golden port1, and the union in (4) is its corresponding
two-port event. Summing over k removes F_k. The existing conditional
H+J_program+R depends on B/Delta and the matter reading, not separately
on every F_k or every first-exit probability. Hence an instrument-history
variation with fixed A can change a fine readout without adding a source
to that particular scalar price. The word's actual records already contain
the signal; which native Cost−Info functional prices it is a separate
same-program binding question, not a reason to insert a new term.

For comparison, within the original Fock apparatus one can extract the
literal recorder without an arbitrary CNOT: with beta=C_n+C_n*,
gamma=C_n-C_n* and G=aI+p gamma, `beta G beta=G*`, so
`C_rec=U_n beta G beta`. Then `X_record=beta C_rec beta C_rec`.
This is an internal same-history operation. It does not commute with the
entire spatial CAR algebra and is not the external reference128 tensor.
The first-exit construction above avoids that spectator-reference gap.

## 6. Bounded evidence

[New exact helper](sources/d0_retained_history_causal_source_2026-10-16/check_retained_history.py)
executes only pinned creator/order definitions, never old run() functions.
It checks the full16 noncommuting Julia/Walsh block, actual two-port factor,
all128 completeness, chronological first-exit sum, moving normalizer,
clock coefficient1/256, and all-angle cone Gram identities. Hostile controls
reject a blank-label substitution, commuting/incoming order, one-port loss,
reset, frozen normalizer, and summing away the cone contrast. The analytic
smooth-stencil estimate above is a proof consumer, not empirical continuum
extrapolation from a finite matrix test. No old source suite, fitted source,
new action, physical admission or GR terminal is claimed.
