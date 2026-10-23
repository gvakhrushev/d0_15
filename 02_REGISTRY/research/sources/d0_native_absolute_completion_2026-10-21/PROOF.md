# Native absolute normalization, fixed-RIGHT feasibility, and the complete HJR response

**Date:** 2026-10-21. **Owner/consumer:** existing scientific Draft #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`constitutive/native-programme-v1`.
**Input:** `5edac80c86c17014fc83e0aa608e192f43c1fdba`.
**Status:** authored derivation and three executed calculations; independent
review and repository CI pending. `GR_closed=false`.

## 0. Exact question and correction to the preceding route

The preceding source-identifiability notes established that normalized
probabilities, by themselves, leave a common amplitude factor undetermined.
That is true for *unspecified* positive amplitude vectors. It is not a reason
to introduce an undetermined factor into an already supplied complete native
instrument. The latter's absolute norm is fixed by its Kraus completeness.
The repository also already owns the actual all-history port-cost transform
and its derivatives. Neither result is re-claimed here.

This application evaluates what happens when that known cost transform is
used to try to complete the proposed Book normalization. It follows the
operator through: absolute norm; isometric normalization; input and oldRIGHT;
the true complementary Book determinant; the given full HJR constructor; and
the original full-spectrum stationary fixture. It also constructs the
literal Golden success/failure completion at the discrete marker value.

The calculations supply two decisive applications not supplied by a
relative-weight criterion:

* On the original 256-site/CAR16/RIGHT128 primary input, the normalized
  cost-tilted whole record has a different RIGHT marginal. It is not the
  output of a deterministic LEFT-only execution from the same complete
  initial state. This is certified already at the vacuum member, hence
  persists in a sufficiently small part of the original nonvacuum family.
* Even where this RIGHT obstruction is absent, namely the original
  first-shell HJR preparation, the polar-normalized return changes the full
  HJR source. Outward evaluation on the entire original root enclosure
  excludes zero at two exact Golden marker values.

These are conclusions about the stated normalization proposal, not a
no-go for all D0 actions. In particular, no Info functional is defined from
the desired output law, and no costs are added to force an Einstein source.
The known full HJR and CQ constructions remain distinct executions.

## 1. Original complete instrument and its already-known cost transform

Use all original data modes, every CAR grade, all 64 SELECT label/coefficient
rows, both ports, and every purifying oldRIGHT column. Set

\[
p=\varphi^{-1},\quad p+p^2=1,\quad
A=hD/16=A^\dagger,\quad \Delta=D^2,\quad
\alpha=p^2h^2/128,\quad\epsilon=2\alpha.
\]

The literal original rows satisfy \(N_0=A\) and
\(\sum_kN_kN_k^\dagger=I\). Their 128 Kraus operators are

\[
K_{0k}=\delta_{k0}I-2p^2N_k^\dagger A,
\qquad K_{1k}=-2p\sqrt p\,N_k^\dagger A.
\tag{1}
\]

In particular

\[
\sum_{b,k}K_{bk}^\dagger K_{bk}=I,\quad
B=K_{00}=I-\alpha\Delta>0,\quad
E_1=\sum_kK_{1k}^\dagger K_{1k}=2p\alpha\Delta.
\tag{2}
\]

The strict positive blank domain is the original owner's domain, not a
new spectral assumption chosen after seeing a result. Physical field
variations use that owner's positive pairing and its moving isometric
trivialization; every derivative below is taken in the resulting fixed
finite Hilbert fibre. Nothing admits new field variations automatically.

For \(n\) fresh rounds, retain every ordered outcome \(\omega\), its product
\(K_\omega\), and the actual direct-0/return-10 port cost
\(C_\omega=n+\sum_jb_j\). The complete isometry is

\[
V_n=\sum_\omega|\omega\rangle K_\omega,
\qquad V_n^\dagger V_n=I.
\tag{3}
\]

Thus for any normalized input its absolute squared norm is exactly one,
and its full field derivative is zero. Multiplication by a positive scalar
\(a(y)\) preserves completeness iff \(a(y)=1\). This does **not** prove that
the Book memory-algebra sum equals \(V_n\); it proves that such an equality,
if asserted literally, cannot simultaneously leave its norm arbitrary.

The already-owned analytical cost transform is

\[
T_t=\sum_\omega e^{-tC_\omega/2}|\omega\rangle K_\omega,
\quad
Z_n(t;\rho)=\operatorname{Tr}(\rho T_t^\dagger T_t).
\tag{4}
\]

Here \(t\) is an analytical marker, not elapsed time, the primary matter
amplitude, or a newly selected physical fugacity. Define the rescaled
positive effect and map

\[
\Psi_t^*(X)=\sum_{b,k}e^{-tb}K_{bk}^\dagger X K_{bk},\quad
H_n=(\Psi_t^*)^n(I),\quad T_t^\dagger T_t=e^{-nt}H_n.
\tag{5}
\]

The original price-transfer owner proves the equivalent CP formula before
this rescaling. We consume it. In particular

\[
H_1=I-(1-e^{-t})E_1
=I-2p\alpha(1-e^{-t})\Delta.
\tag{6}
\]

For \(t\ge0\),
\(e^{-nt}I\le H_n\le I\); for every real finite \(t\), \(H_n>0\).
At \(t=0\), \(H_n=I\) on the whole smooth native chart, so
\(D_yH_n=0\). At nonzero \(t\), the normalizer is generally an operator,
not a freely chosen scalar. Its scalar expectation depends on preparation.

The full field jet is computed without enumerating \(128^n\) histories:

\[
H_{j+1}=\Psi_t^*(H_j),\qquad
D H_{j+1}=\Psi_t^*(D H_j)+(D\Psi_t^*)(H_j),
\tag{7}
\]

where \(D\Psi_t^*\) differentiates both sides of every Kraus factor,
including the genuine Julia-root, observer, calibration and input jets
when they move. Changing integer \(n\) is a programme comparison, not a
smooth derivative. The actual paid cost is still
\(-\partial_t\log Z_n|_{t=0}\); it is not newly identified with Book Info.

## 2. Exact finite normalization, with its actual input change

Set \(H=H_n\). The uniquely positive polar normalization is

\[
\bar V_t=e^{nt/2}T_t H^{-1/2},\qquad
\bar V_t^\dagger\bar V_t=I.
\tag{8}
\]

It can be factored into complete time-dependent instruments. Define
backward effects \(h_n=I\),
\(h_j=\Psi_t^*(h_{j+1})\), and

\[
\widetilde K_{j,bk}
=e^{-tb/2}h_{j+1}^{1/2}K_{bk}h_j^{-1/2}.
\tag{9}
\]

Direct summation gives \(\sum\widetilde K^\dagger\widetilde K=I\).
Chronological multiplication telescopes every intermediate square root:

\[
\widetilde K_\omega
=e^{-t\sum b_j/2}K_\omega H^{-1/2}.
\tag{10}
\]

This is finite polar/quantum-Doob normalization, not a claim of a newly
invented general transformation or a free native gate. The roots depend
on future supplied effects, and native preparation/control/admission and
payment of (9) do not follow from these algebraic identities.

For a normalized purification \(\psi\), reproducing the normalized tilted
record of the *original* input requires

\[
\psi_t=\frac{(H^{1/2}\otimes I_R)\psi}
{\sqrt{\langle\psi,(H\otimes I_R)\psi\rangle}},\qquad
\bar V_t\psi_t=\frac{T_t\psi}{\|T_t\psi\|}.
\tag{11}
\]

Using \(\bar V_t\) on \(\psi\), without this change, generally produces
another record. This is not repaired by calling (8) a scalar normalization.
For a prepared matrix \(C\), \(\operatorname{Tr}C^\dagger C=1\), write

\[
C_t=H^{1/2}C/\sqrt{\mathcal Z},\qquad
\mathcal Z=\operatorname{Tr}(C^\dagger H C).
\tag{12}
\]

When derivatives are needed, the unique positive square root \(S=H^{1/2}\)
satisfies the Sylvester equation
\(S(DS)+(DS)S=DH\), and
\(D(H^{-1/2})=-S^{-1}(DS)S^{-1}\). This retains noncommuting jets.

## 3. Fixed oldRIGHT is a decisive same-initial-state constraint

In the original column convention the RIGHT density is the transpose of
\(C^\dagger C\); using Gram matrices does not change any equality below.
The target in (11) has RIGHT Gram

\[
G_{R,t}=\frac{C^\dagger H C}{\mathcal Z}.
\tag{13}
\]

Every deterministic trace-preserving operation acting only on LEFT,
including fresh initially independent ancillas, leaves RIGHT unchanged.
Indeed, for any complete family \(L_j\), its final reference Gram is
\(\sum_j C^\dagger L_j^\dagger L_j C=C^\dagger C\).
This holds when LEFT and RIGHT are initially entangled. No locality,
continuum or physical light-cone assumption is being imported.

Consequently an exact realization of the **whole normalized tilted pure
record** from the same complete initial state must satisfy

\[
\boxed{C^\dagger H C=\mathcal Z\,C^\dagger C.}
\tag{14}
\]

For a fixed supplied \(C\), this is also sufficient for a mathematical
LEFT isometric implementation. It makes \(C_t^\dagger C_t=C^\dagger C\).
The map \(Cv\mapsto C_tv\) is then a well-defined isometry of the column
span, extends to a unitary on DATA, and can be followed by \(\bar V_t\).
This proves mathematical sufficiency, not the availability or price of
that unitary in D0. For all normalized input purifications, (14) forces
\(H\) scalar. On a restricted input support it can hold without scalarity
on the whole DATA space.

Thus identity tensor action on oldRIGHT does not imply that a
**postselected/renormalized** target has its old RIGHT marginal. Retaining
the excluded outcomes is precisely what restores that marginal.

### 3.1 Literal primary application, retaining all 128 columns

Use the original L4 periodic regulator and its actual primary vacuum input:
256 sites, CAR16, oldRIGHT128, \(h=1/4\), \(\sigma=p^3\), and
\(\rho_x=256\,\mathrm{count}_x/10946\). The exact original cost20 F/R
routing has counts 29 through 78. Its integer vector has inherited SHA256
`fbca167a01fcca76356153586a1006ad1144b612f97740b7611f163f5a3164e9`.
The checker reconstructs only this pinned definition, not an old physics
suite or a new history census.

Let \(F_{xa}\in\{0,1,-1\}\) be the original 128 real Fourier numerators
from the first 64 lexicographic pairs \(k<-k\). They obey
\(F^TF=128I\). The preparation is exactly

\[
C_{(x,j),a}=\frac{F_{xa}}{128}
\left(\sqrt p\,\delta_{j1}+p\,\delta_{j14}\right),
\qquad C^\dagger C=I_{128}/128.
\tag{15}
\]

No column or CAR component is dropped. At this primary member, with
\(a_x=\sigma\sqrt{\rho_x}\) and the owned REST legs

\[
v_u=(1/2,-1/2,0,0),\quad v_v=(1,1,0,0),\quad
v_x=-e_2,\quad v_y=-e_3,
\]

the entire shifted positive-adjoint Dirac application is

\[
(DC)_x=\frac1h\sum_r\left[
 a_x c(v_r)(C_{x+r}-C_x)
 +c(v_r)^\dagger(a_{x-r}C_{x-r}-a_xC_x)\right].
\tag{16}
\]

The finite calculation forms \(Q=C^\dagger\Delta C=(DC)^\dagger DC\).
For original zero-based columns 57 and 55 (the sine columns of
\((1,0,0,0)\) and \((0,2,2,1)\)), outward 85-digit arithmetic gives

\[
Q_{57,57}=0.0068747884807911777\ldots,
\quad Q_{55,55}=0.1009784871783217566\ldots,
\]

\[
\boxed{Q_{55,55}-Q_{57,57}>0.09410369869753.}
\tag{17}
\]

The exact interval endpoints, not only these shortened decimals, are saved
in `primary_result.json`. Each inner product sums all nonzero rows of the
full16 operator; the heterogeneous weights are never averaged.

At the original marker \(t=\ln\varphi\), (6) is
\(H_1=I-k\Delta\),
\(k=2p\alpha(1-p)>0\), \(\alpha=p^2/2048\). Therefore

\[
(C^\dagger H_1C)_{55,55}-(C^\dagger H_1C)_{57,57}
\in[-8.28645040838,-8.28645040837]10^{-6}.
\tag{18}
\]

Equation (14) is impossible: its right side is scalar. This is an exact
same-boundary obstruction to deterministic LEFT realization of this
normalized target, **on the original primary input**. A diagnostic full
matrix calculation gives
\(\|G_{R,t}-I/128\|_{HS}=2.26195999135\times10^{-5}\).
The strict sign is established by (18), not by a floating rank threshold.

The original local nonvacuum primary family and its positive-adjoint
operator are analytic near this member, and retain \(C^\dagger C=I/128\).
Thus the strict inequality persists for sufficiently small nonzero
primary matter amplitude. No explicit uniform interval in that amplitude
or mesh is claimed. Nor is a one-round result silently promoted to all
round counts: each horizon uses its own \(H_n\) in (14).

## 4. Actual complementary Book determinant after polar normalization

Return to the owner's actual active blank corner, with its work/status and
clock identification explicitly supplied. At \(n\) rounds the unmarked
DATA blank amplitude is \(B^n\). The polar-normalized corner is

\[
\bar A_t=B^n H^{-1/2},\quad K=B^{2n},\quad
\bar R_t=H^{-1/2}K H^{-1/2},\quad
\bar F_t=I-\bar R_t.
\tag{19}
\]

If the real active corner is zero because of a retained clock or terminal
status, (19) is not substituted for it. The earlier clock owners specify
exactly that boundary. The following is a same-cut operator test.

Let \(r_R=128\) be the original oldRIGHT multiplicity and
\(M_t=(1-z)H+zK\). The exact complete determinant is

\[
\boxed{\bar J_t=r_R\log\det H-r_R\log\det M_t.}
\tag{20}
\]

Proof: \((1-z)I+z\bar R_t=H^{-1/2}M_tH^{-1/2}\); take the determinant.
No \([H,K]=0\) assumption is used. The source at fixed \(r_R\) is

\[
\boxed{
D\bar J_t=r_R\operatorname{Tr}(H^{-1}DH)
-r_R\operatorname{Tr}\!\bigl(M_t^{-1}[(1-z)DH+zDK+(K-H)Dz]\bigr).
}
\tag{21}
\]

A moving embedding, actual clock or original calibration has its own
contribution in \(DH,DK\); nothing permits setting it to zero by name.

A necessary correction to the older scalar argument is

\[
A\mapsto aA\quad\Longrightarrow\quad
F\mapsto I-a^2A^\dagger A
=a^2F+(1-a^2)I,
\tag{22}
\]

not \(F\mapsto aF\) or \(a^2F\). A logdet derivative derived for a
multiplicative change of \(F\) remains correct *for that change*, but it
cannot be imported into the true complementary cut without (22).

The one common factor allowed by isometry is a phase. For
\(A'=e^{i\chi(y)}A\), the actual complement satisfies
\(F'=I-A'^\dagger A'=F\) identically, including its full first jet: the
\(D\chi\) terms cancel. Thus a common phase does not supply a hidden
complementary-feedback source either. This statement concerns the
specified complement, not a different oriented determinant of \(U\),
nor an independently redefined heat generator.

### 4.1 Sign fixed by the original paid occupation effect

At \(t=0\), define the actual expected port1 count effect

\[
P_n=\sum_{j=0}^{n-1}(\Phi^*)^j(E_1),\qquad
\partial_tH_n|_0=-P_n,
\]

where \(\Phi^*\) is the original unmarked channel. Substitution in (21)
gives

\[
\boxed{\partial_t\bar J_t|_0
=-r_Rz\operatorname{Tr}\left[((1-z)I+zK)^{-1}K P_n\right]<0}
\tag{23}
\]

for \(K>0\), \(P_n\ne0\), \(0<z<1\). The sign follows from positivity
of \(((1-z)I+zK)^{-1}K\), not commutation of \(P_n\) with it.
This computes an actual marker response, not a choice of its sign.

## 5. Full conditional HJR test, not just a loop statistic

The inherited HJR constructor uses a specified return-generated heat,
complementary feedback and the original quadratic matter reading. To test
whether polar normalization transports this constructor source-neutrally,
substitute (19) and the *required input* (12):

\[
\bar S_t=\frac1\beta\log(C_{\rm work}\operatorname{Tr}\bar R_t)
-r_R\log\det((1-z)I+z\bar R_t)
+\operatorname{Tr}(\rho_t\Delta),
\quad
\rho_t=H^{1/2}\rho H^{1/2}/\operatorname{Tr}(\rho H).
\tag{24}
\]

This is an explicit **transport test**: the same supplied HJR constructor
is evaluated on the normalized marked operators, while its DATA reading
\(\Delta\), units and regulators are held as declared. It is NOT a claim
that (24) is compulsory Book physics or the original unmodified action.
In general the normalized Kraus family no longer has the original
\(B=I-\alpha\Delta\) block-encoding with the same \(D\). That failure is
part of the transport test, not hidden by assigning a new matter operator.
Uncomputed costs of realizing the normalization are not declared zero.

For fixed \(\beta,C_{\rm work}\) the full derivative is

\[
D\bar S_t=
\frac{\operatorname{Tr}(D\bar R_t)}{\beta\operatorname{Tr}\bar R_t}
+D\bar J_t
+\operatorname{Tr}(D\rho_t\,\Delta+\rho_tD\Delta).
\tag{25}
\]

The checker explicitly differentiates \(\rho_t\), including a nonzero
LEFT-unitary input jet that preserves the *original* RIGHT Gram. It
compares (25) against the derivative of the whole value. Notably,
subtracting the normalization term \(r_R\operatorname{Tr}H^{-1}DH\)
from (21) gives an erroneous native fixture source about \(-2.63867\)
instead of about \(-7.82\times10^{-6}\).

### 5.1 Entire original HJR root enclosure

Use the published L8 critical-point enclosure, without a new root search:

\[
d_0=0.063635191594344535042829697433316630182693569761541,
\quad o_0=0.0040167350432317252873844519148251220686807163526359,
\]

with both coordinates in radius \(10^{-12}\). The existence proof and
all local stationary rows are inherited. Retain every one of the
4096 Fourier modes and all16 CAR components, i.e. 65536 thermal modes;
retain oldRIGHT multiplicity128. The actual parameters are

\[
n=8192,\quad \alpha=p^2/8192,\quad\beta=2p^2,\quad z=2^{-20}.
\]

On each original invariant scalar Fourier block with energy \(\lambda\),
(5) gives exactly

\[
H_n(\lambda)=h_t(\lambda)^n,\quad
h_t(\lambda)=1-2p\alpha(1-u)\lambda,\quad u=e^{-t},
\]
\[
\bar R_t(\lambda)=k_t(\lambda)
=\frac{(1-\alpha\lambda)^{2n}}{h_t(\lambda)^n}.
\tag{26}
\]

This uses the owned invariant scalar blocks, not an assumption that every
noncommuting variation is scalar. The occupied first shell has one energy
\(\lambda_s=d(128-64\sqrt2)\), so \(H_n\) is scalar on that entire
preparation support. Here \(C_t=C\): the RIGHT obstruction of Section 3
is absent. This isolates a *genuine whole-price source failure*, not an
artifact of silently changing this root's preparation.

Along the allowed homogeneous ray \(D\mapsto e^sD\), define

\[
\ell_t(\lambda)=\frac1{1-\alpha\lambda}
-\frac{p(1-u)}{h_t(\lambda)}.
\]

With all spectral multiplicities included,

\[
\partial_s\bar H=-2\frac{\sum\lambda k_t\ell_t}{\sum k_t},\quad
\partial_s\bar J=2r_Rz\beta\sum
 \frac{\lambda k_t\ell_t}{1-z+zk_t},\quad
\partial_s\bar R=2\lambda_s.
\tag{27}
\]

Outward 85-digit evaluation on **the entire old rectangle** yields:

| Supplied marker | Full radial source interval |
|---|---|
| \(t=0\) | \([-7.612,7.612]\,10^{-10}\) |
| \(t=\ln\varphi\) | \([-0.497238841832,-0.497238839255]\) |
| \(t=2\ln\varphi\) | \([-0.724148414370,-0.724148410730]\) |

The unmarked enclosure is a consistency check with the inherited exact
root, not a fresh existence certificate. The two other intervals exclude
zero and therefore also exclude it at that exact root. A separate
80-digit computation differentiates the whole scalar value by central
finite differences and agrees with (27) to better than \(10^{-25}\).
Its role is an independent formula check, not independent human/agent review.

This calculation refutes the particular claim that normalizing the paid
record supplies a source-neutral completion of the old HJR root. It does
not claim that no different stationary solution exists for the altered
constructor, and it does not turn that altered constructor into D0 physics.

## 6. Literal Golden realization retains failure; it is not the polar map

At \(t=\ln\varphi\), the weight \(e^{-tC_\omega/2}=p^{C_\omega/2}\)
has a finite realization using the already supplied Golden splitter.
After each actual cost unit, apply it to a fresh initially blank flag.
Conditioned on the existing retained history, use \(C_\omega\) such
flags; keep every flag string and all original records. Controlled routing
and the actual clock/cost of those calls are explicit requirements, not
free operations or a new fundamental selector.

The all-accept subamplitude is exactly \(T_t\). Summing **all** success
and failure strings gives the identity effect. Consequently RIGHT is
unchanged for the complete output. For one original round there are
384 nonzero outcome/flag leaves: 64 cost1 outcomes with two flag strings
and 64 cost2 outcomes with four. The checker verifies their completeness
and equality of the original reduced DATA channel after forgetting the
*new* flags mathematically; no physical erasure is executed.

For the actual active blank DATA/work corner, all original outcomes and
all extra flags must be blank. Its amplitude is

\[
A_{\rm flags}=p^{n/2}B^n,
\qquad F_{\rm flags}=I-p^nB^{2n},
\tag{28}
\]

not the normalized corner \(B^nH_n^{-1/2}\). If a real forward clock is
included, its new blank duration must also be included. For a window of
width \(M\), actual blank duration \(d'\), and DATA dimension \(d_H\),

\[
J_{\rm clock}
=\max(M-d',0)J_{\rm flags}
-r_R\min(M,d')d_H\log(1-z).
\tag{29}
\]

Here \(d'\) includes every extra flag call and the real control prefix.
Using the old clock delay after appending those calls would be a different
false transport. The earlier clock theorem is consumed, not re-proved.

For the original primary input of Section 3 the raw success probability
is approximately \(0.6176608397871732\); the full failure probability is
\(0.3823391602128269\). Their RIGHT Grams add exactly to \(I/128\).
Dropping and renormalizing the latter is precisely the prohibited
same-initial-state substitution diagnosed by (18).

## 7. What is settled by this application

The original instrument's absolute norm is settled: it is one. Its supplied
paid transform is also explicit: (5)-(7), with actual preparation dependence.
The polar transformation, its full input/reference requirement, its true
complementary determinant and full conditional HJR source have now been
calculated and tested, including the original primary and full root carriers.
The discrete Golden success/failure completion has been distinguished from
that normalized map, with its failures and changed clock still present.

Therefore the previous claim that only one arbitrary scalar anchor remained
was too weak and misleading when applied to this actual complete execution.
No such scalar is free once the executed isometry is fixed; changing the
weights is a different process, and its normalization has an operator-valued
input and source effect. It does not establish the Book/Cost−Info binding.

The mathematical GR source and existing nonvacuum solutions are not
recomputed here. The proposed normalization route fails its intended
same-initial and same-source substitution. A valid physical closure must
instead derive the actual *same-programme* Book valuation/admitted variation
map, with its independent input and clock/work equations. No unknown
counterterm, Info table, compensating stress, physical prior, or new coupling
has been installed to make the tests pass. Full D0→GR is not proved here.

### Concurrent fixed-processor result, read before integration

The subsequent branch head `7c3efe0a9faad4a6340ddcff9bdc9a6b165084c5`
contains `A4D_FIXED_PROCESSOR_JOINT_RESOURCE_SOURCE_2026_10_21.md`.
Its fixed Golden/Bell processor and paid transitive scheduling prove
stationarity of the processing price in every stated independent resource
copy at the configured field root. Its actual own-resource preparation
price and absolute Book binding are explicitly retained obligations.
Those are positive results on a DIFFERENT supplied execution; this packet
neither repeats nor refutes them.

Our fixed-RIGHT criterion applies if a proposed upstream resource map
actually asks to produce the normalized tilted record of the original
full128 input while preserving its same reference. It does not prohibit
all resource preparation or identify that processor with the raw full128
instrument. Likewise its spectral first-source equivalence need not imply
our earlier per-history Gibbs/cycle equality: those tests belong to
particular proposed bindings, not universal necessary conditions for any
possible gravitational stationary-set transport. The parent must keep
that distinction. No parallel file is replaced by the present additions.

## 8. Reproduction and provenance

Run `verify.py` from this directory. It executes three new bounded checks:

1. Literal full128/CAR16 Fourier interface and analytic boost jets; full
   CP contractions, polar/Doob products, full HJR differentiation and
   discrete Golden success/failure completion.
2. Outward full original L8 spectral-root transport with all 119 exact
   feature classes; separate high-precision whole-value finite difference.
3. Original 256-site/128-column primary reference test, exact integer F/R
   routing and outward two-column witness from the entire CAR operator.

Ordinary and optimized Python runs are compared byte-for-byte. Numerical
matrix equalities have explicit tolerances; only outward interval signs
are advertised as rigorous numerical enclosures. Universal identities
are proved above, not extrapolated from finite checks. Historical large
root/support/geometry/Lean suites are not claimed replayed. No independent
review or remote CI run is claimed. See `SOURCES.json` and `VALIDATION.json`.
