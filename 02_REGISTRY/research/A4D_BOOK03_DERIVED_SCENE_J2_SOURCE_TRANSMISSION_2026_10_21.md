# Book03 bootstrap source transmission through one derived scene conductance

21 October 2026. Existing Draft PR #334,
\`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`.

This theorem composes the exact weighted-scene Book03 bootstrap with the
already owned configured Golden-\`J2\` field source. It is a **source
embedding theorem and an Euler-interface dichotomy**, not a physical
admission theorem. No new action term, fitted coupling, detector, field or
calibration is introduced.

\`GR_closed=false\`.

## 1. Exact Book03 scene covector already owned

Use the complete 33-vertex \(K(9,11,13)\) weighted scene of
\`A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md\`. Let the three
automorphism-invariant cross-zone conductances be

\[
 x=w_{9,11},\qquad y=w_{9,13},\qquad u=w_{11,13},
\]

with every edge of one zone-pair carrying the same positive weight. Put

\[
 T=D_d^{-1}A,\qquad \Delta=I-T,
\]

and retain all 718 oriented histories with the exact return feedback

\[
 F_H=J(I-T^2)C.
\]

The Book03 §03.25 scalar on this carrier is

\[
 \mathcal B_{\beta,z}
 =\beta^{-1}\log\operatorname{Tr}e^{-\beta(I-T)}
  -\log\det[I-z(I-T^2)].
\tag{1}
\]

At the canonical scene \(x=y=u=1\), the complete first source factors as

\[
 D\mathcal B_{\beta,z}
 =g_{\beta,z}\,D\kappa,
 \qquad g_{\beta,z}=c_H(\beta)+c_F(z),
\tag{2}
\]

where

\[
 \kappa(x,y,u)=
 \frac{2574uxy}
 {(11u+9y)(13u+9x)(11x+13y)} ,
\]

and the exact equitable derivatives are

\[
 \boxed{
 \kappa_x(1,1,1)=\frac{91}{2816},\quad
 \kappa_y(1,1,1)=\frac{13}{6400},\quad
 \kappa_u(1,1,1)=-\frac{1209}{35200}.
 }
\tag{3}
\]

No independent heat/feedback jet is introduced here: (1)--(3) are the owned
same-scene complete bootstrap calculation with moving degrees, archive
pairing and history projector included.

## 2. One derived conductance transmits an arbitrary scalar field covector

Let \(\mathcal J(Y)\) be any differentiable dimensionless scalar of the
original finite field variables \(Y\). For the GR consumer take

\[
 \mathcal J(Y)=J_2(Y)-J_2(Y_*),
\tag{4}
\]

where \(J_2\) is the already configured Golden-\`J2\` scalar on the SAME
finite field carrier and \(Y_*\) is any one of its stationary
Einstein--CAR representatives. Thus

\[
 \mathcal J(Y_*)=0,\qquad D\mathcal J(Y_*)=DJ_2(Y_*).
\]

Define only a **derived scene preparation rule**

\[
 \boxed{x(Y)=1+\mathcal J(Y),\qquad y(Y)=u(Y)=1.}
\tag{5}
\]

This introduces no numerical coefficient. On a sufficiently small field
neighbourhood, \(x>0\).

By the exact chain rule and (2)--(3),

\[
 \boxed{
 D_Y\mathcal B_{\beta,z}\big|_{Y_*}
 =g_{\beta,z}\frac{91}{2816}\,DJ_2\big|_{Y_*}.
 }
\tag{6}
\]

Therefore, whenever \(g_{\beta,z}\ne0\),

\[
 \boxed{
 D_Y\mathcal B_{\beta,z}=0
 \quad\Longleftrightarrow\quad
 DJ_2=0
 }
\tag{7}
\]

at the base field, for the complete ambient \(J_2\) covector. In particular,
all configured 16 coframe + 24 proper-link + 2 matter rows are transferred by
one and the same nonzero factor. The coefficient is derived from the native
scene and fixed \((\beta,z)\); it is not fitted to the Einstein equation.

Equation (7) is an exact first-source equivalence, not equality of action
values, Hessians, minima, refinement norms or physical preparations.

## 3. The actual full128/HJR calibration is strictly off the stationary scene branch

Now use the existing diagnostic/native calibration appearing throughout the
original full128/HJR owners,

\[
 p=\varphi^{-1},\qquad
 \beta=2p^2,\qquad
 z=2^{-20}.
\tag{8}
\]

The shared-scene owner gives

\[
 c_H=
 -\frac{e^{-\beta(3/2-r)}-e^{-\beta(3/2+r)}}
        {2rZ_\beta},
 \quad
 r=\frac{\sqrt{10}}{40},
\]

\[
 c_F=
 \frac{2z[1-(1+\kappa_0)z]}
 {(1-z)(1-2\kappa_0z)+\kappa_0^2z^2},
 \qquad \kappa_0=\frac{39}{160}.
\tag{9}
\]

Here \(c_H<0<c_F\). Moreover the sign is strict without numerical root
finding. Write \(h=-c_H\). By the mean-value theorem,

\[
 h=\frac{\beta e^{-\beta\xi}}{Z_\beta},
 \qquad
 3/2-r<\xi<3/2+r<2.
\]

Using \(0<\beta<1\), the elementary bounds
\(\beta>7/10\), \(e^{-2}>1/8\), and \(Z_\beta<33\) give

\[
 h>\frac{7}{2640}.
\tag{10}
\]

Since \(z=2^{-20}<1/2\) and \(\kappa_0<1/2\), the positive denominator in
\(c_F\) is greater than \(1/4\), so

\[
 0<c_F<8z=\frac1{131072}.
\tag{11}
\]

Thus

\[
 \boxed{
 g_{2p^2,2^{-20}}=c_H+c_F<0.
 }
\tag{12}
\]

Hence the transmission coefficient in (6) is rigorously nonzero. A numerical
display, not used by the proof, is

\[
 g\approx-1.5565050643861\times10^{-2},
 \qquad
 g\frac{91}{2816}
 \approx-5.02989917823634\times10^{-4}.
\tag{13}
\]

So the fixed full128/HJR values are not on either weighted-scene stationary
\(z_*(\beta)\) branch.

## 4. Exact Euler dichotomy: source transmission versus an independent scene variable

The same calculation yields a decisive physical-interface condition.

If \(x\) in (5) is not a derived resource but an **independently varied
physical scene conductance**, then a full joint stationary point at the
canonical scene must obey its own Euler row

\[
 0=\partial_x\mathcal B_{\beta,z}\big|_{1,1,1}
   =g_{\beta,z}\frac{91}{2816}.
\tag{14}
\]

Because \(91/2816\ne0\), equation (14) forces

\[
 \boxed{g_{\beta,z}=0.}
\tag{15}
\]

But (15) sets the field-source transmission coefficient in (6) to zero.

Therefore:

### Source-transmission dichotomy

The same canonical conductance \(x\) cannot simultaneously be

1. an unconstrained independent Euler variable of the bare scene bootstrap,
   **and**
2. the sole carrier of a nonzero \(J_2\) field source through (5).

To transmit \(DJ_2\) with \(g\ne0\), \(x\) must instead be:

- a generated/derived variable fixed by the same physical field execution;
- a constrained variable with its genuine reaction retained; or
- part of a larger action whose independent \(x\)-equation receives an
  additional actual source.

At the calibration (8), (12) proves that the canonical scene is not
stationary under a free \(x\)-variation. Consequently the derived
interpretation is not optional if (5) is used for GR.

## 5. Composition with the paid writer results

The recent rational/moment writers show that finite Golden/CNOT programmes
can prepare finite catalogues of field-dependent resources with all failures
and oldRIGHT retained. They do **not** yet prove one autonomous same-initial
controller law that makes (5) a generated native variable rather than an
externally selected code.

This theorem therefore turns the writer/controller obligation into one
precise target:

> Construct on the same complete execution a generated positive scene
> conductance \(x(Y)\) whose first jet at the primary field section is
> \(Dx=DJ_2\), with \(x=1\) at the root, while \(y=u=1\), and carry the
> writer/controller/clock price and every independent upstream equation.

If that construction has no additional field source at the root (or a proved
source proportional to the same \(DJ_2\)), then equation (6) immediately
promotes the configured all42 finite roots to roots of the actual §03.25
scene bootstrap with a nonzero derived coefficient.

If instead the writer makes \(x\) a freely optimized independent coordinate,
equation (14) kills the desired transfer.

## 6. Scope

This theorem proves:

- the actual Book03 master bootstrap has a concrete finite scene-history
  realization capable of carrying the entire configured \(J_2\) first
  covector;
- at \((\beta,z)=(2p^2,2^{-20})\) the carrying coefficient is rigorously
  nonzero;
- no fitted scalar is required;
- independent scene optimization is incompatible with nonzero source
  transmission, so the exact missing physical theorem is a
  **generated/constrained scene writer**, not another metric solution.

It does not prove the same-initial physical generation of (5), controller
selection, its full paid price, raw216 refinement, or compulsory adoption of
this weighted-scene extension as the physical scene law.

\`GR_closed=false\`.
