# Recorded full128: cyclic incidence heat, complete archive spectrum and a uniform source bound

22 October 2026. Repository `gvakhrushev/d0_15`; existing scientific owner
Draft PR #334 / `exp/a4d-joint-response-continuation-2026-10-16`.
Read snapshot: `aa559595e7b800af8217c58885a4710c16747444`.

## 0. The missing premise addressed, without a replacement-action claim

The preceding native-block result reconstructed the original full128 instrument
and transported its **paired-cut** heat, retaining its 1984 extra identity modes.
That did not compute the heat of a normalized incidence Laplacian. Book03
03.1.2 defaults to normalized scene incidence, and 03.25 differentiates its
whole heat trace. A graph-incidence heat cannot be renamed paired-cut heat.
The J2 joint-root comparison note also correctly observes that the real clock
is cyclic: an open-path isospectral argument does not settle its source.

Here an explicit, finite, cyclic connection-incidence realization is constructed
on the unchanged scene graph `K(9,11,13)` times an execution clock. Its heat
source is computed with the **whole recorded unitary**, not just its initialized
column. The source is generically nonzero. Nevertheless it has a dimension-free,
explicitly bounded winding tail, including second derivatives. Applied to the
original full128 with its complete fine-label archive, it is computable from
128 matrices of size16 rather than from a huge heat matrix.

This is a new mathematical realization and source theorem for a precisely
specified graph/operator. It is NOT a proof that Book03 compulsorily selects
the Cartesian history graph, its homogeneous circuit fibre, its return cut or
this unitary completion. In particular, a quantum channel does not uniquely
fix a heat spectrum on unprepared columns. We use the original explicit
Julia/Walsh completion from the previous packet, not an arbitrary completion.
The actual native field writer, any additional selected paid-history terms,
and independently admitted apparatus equations are not inferred. No new root,
Lean theorem, external review, accepted Book edit or GR promotion is made.
`GR_closed=false`.

## 1. The actual normalized incidence operator in this realization

Let S be the complete tripartite graph with part sizes `(9,11,13)`. It has
33 vertices,359 edges, and degrees `(24,22,20)`. Let `C_m`, m>=3, be the closed
execution-stage graph. The clock executes a fully specified unitary word
`U_0,...,U_(m-1)` on a d-dimensional fibre. It may include every work, record
and retained-reference register. The SAME word is used at each vertex of S;
this homogeneous-fibre hypothesis is essential and is tested in section8.
It does not require the unitary's own internal registers or input state to be
homogeneous. It does require its placement over this base scene to be uniform.

Horizontal S-edges transport by identity. A vertical edge `(v,t)->(v,t+1)`
transports by U_t, including the closing edge. The full vertex degree is
`d'_v=d_v+2`, so it equals26,24,22 on the three parts. For each oriented
undirected edge i->j with unitary transport T_ji define the normalized incidence

    (D psi)_edge = psi_j/sqrt(d'_j) - T_ji psi_i/sqrt(d'_i).

Changing edge orientation only changes its unitary edge frame. Set

    L_hist = D*D.

Direct multiplication yields diagonal I and off-diagonal normalized transports.
Its quadratic form proves `0<=L_hist<=2I`. This is a genuine normalized
connection Laplacian, not `C* C+C C*` of a return defect, and not the unchanged
33x33 scalar scene Laplacian. The graph and normalization have been stated
rather than silently identified with either of those different operators.

Put `R=diag((d_v+2)^(-1/2))`, `B=R A_S R`, `C=R^2`. With S_U the stage shift
carrying U_t,

    L_hist = I - B tensor I - C tensor(S_U+S_U*).             (1)

All 33 scene modes, all m stage modes and all d fibre modes stay in the trace.
No normalized operator trace is substituted for the original counting trace.
The choice `beta=2 phi^-2` is fixed; it is not varied to suppress a source.

## 2. Gauge reduction is exact, but the cycle holonomy survives

Let V_t=U_(t-1)...U_0, V_0=I. The block-diagonal unitary with these V_t removes
all interior edge transports and leaves the actual complete holonomy

    V=U_(m-1)...U_0

on the closing edge. It also leaves horizontal edges unchanged because the
same V_t acts at every scene vertex. This is a representation change; no
physical inverse circuit is asserted to be executed for free.

For each eigenvalue exp(i omega) of V, the clock eigenangles are
`theta_k=(2 pi k+omega)/m` (a sign convention change gives the same total trace).
Thus, with

    f(theta)=Tr_33 exp[beta(B+2 C cos(theta))],

    Z_hist = exp(-beta) sum_(omega in spec V) sum_(k=0)^(m-1) f(theta_k). (2)

This gives the full operator trace, including multiplicities. It does not
replace the cyclic clock by an open path.

Because B and C have entrywise nonnegative real entries, the Laurent expansion

    f(theta)=c_0+2 sum_(n>=1) c_n cos(n theta),   c_n>=0

has nonnegative coefficients. Expand the exponential of
`B+C z+C z^-1`: each coefficient is a sum of nonnegative traces of genuine
ordered matrix products. No commutation of B with C is used. Root-of-unity
summation gives the exact all-spectrum identity

    Z_hist=m exp(-beta)[d c_0+2 sum_(ell>=1) c_(ell m) Re Tr(V^ell)]. (3)

Every graph heat moment of degree smaller than m is independent of V: such
closed walks do not wind around the execution cycle. The full heat is not
constant because moments of degree at least m do wind. A topological boundary
fact, rather than an assumed cancellation of heat and feedback, isolates the
source-bearing terms.

## 3. Uniform first and second source bounds

The normalized scene matrices obey

    ||B||_op <= a=12/13,       ||C||_op <= c=1/22.

The first follows by comparing `R A R` to the normalized adjacency of S,
with `max d_v/(d_v+2)=24/26`. For any ordered product, its trace is bounded
by33 times the product of operator norms. Counting its positive Laurent
coefficients therefore gives

    0<=c_n<=33 exp(beta a) I_n(2 beta c),                    (4)

where I_n is the modified Bessel function. This coefficient majorization
is valid even though B and C do not commute. The scalar generating identity
is NIST DLMF 10.35.2; its positive power series is DLMF 10.25.2. The current
application and the noncommuting bound (4) are derived here.

Let `H=beta^-1 log Z_hist`, with fixed graph, ranks and beta. For any admitted
smooth parameter direction v put `L1(v)=||D_v V||_op` and
`L2(v,w)=||D^2_(v,w) V||_op`. Let

    B1(m)=sum_(ell>=1) ell I_(ell m)(2 beta c),
    B2(m)=sum_(ell>=1) ell(ell-1) I_(ell m)(2 beta c).

By the product rule and unitarity,

    |D Tr(V^ell)| <= d ell L1,
    |D^2 Tr(V^ell)| <= d[ell L2+ell(ell-1)L1(v)L1(w)].

The incidence positivity bound gives `Z_hist>=33 m d exp(-2 beta)`. Hence

    |D_v H| <= C1(m) L1(v),
    C1(m) = 2 exp(beta(1+a)) B1(m)/beta,                    (5)

and

    |D^2_(v,w) H| <= C1(m) L2(v,w)+C2(m)L1(v)L1(w),
    C2(m)=2 exp(beta(1+a)) B2(m)/beta
           +4 exp(2 beta(1+a)) B1(m)^2/beta.               (6)

The ordinary fibre dimension and every fixed spectator multiplicity CANCEL
in these estimates through the heat denominator. The multiplicities are not
removed from the actual scalar H or the feedback action.

### Auditable positive tail bounds

The defining series gives, for x>=0,

    I_n(x) <= (x/2)^n/n! * exp[x^2/(4(n+1))].

For n=ell*m let b be this bound at n=m and
`r=(x/2)^m/[(m+1)...(2m)]`. Successive bounds have ratio at most r. Consequently

    B1<=b/(1-r)^2,       B2<=2 b r/(1-r)^3.                 (7)

At beta=2phi^-2, outward interval arithmetic verifies the safe rounded bounds

| m | C1(m) upper bound |
|---|---:|
| 11 | 2.523e-23 |
| 15 | 1.120e-33 |
| 16 | 2.430e-36 |
| 32 | 8.632e-82 |

At m=15 the mixed constant C2 is below9.574e-67. This is an operator-norm
source bound throughout the specified smooth unitary family, not merely a
small derivative observed at one fixture. It is not an absolute bound on a
42-covector until the actual 42 derivatives of V are bounded in the specified
field norm. Fixed coefficients/ranks are essential; beta-variation has its
own entropy source, and changing a discrete clock inventory is not a
continuous field variation.

## 4. Complete old record changes the holonomy and must not be omitted

Consume the original exact native construction from the preceding packet:

    N N*=I_16,   Q=N* N,   rank Q=16,
    U=I_2048-2 T T*,   T=(p,sqrt(p))^T tensor N*,   T*T=I_16.

Here p=phi^-1; N consists of the actual64 Julia/Walsh blocks N_j. The output
fine label is alpha=2j+b, j=0,...,63, b=0,1. U reproduces all original128 Kraus
operators on the declared initialized source. The bare U has a fixed reflection
spectrum, so its cyclic heat is exactly field-independent.

That observation does NOT apply after genuine archival recording. On an explicitly appended
128-state fine-record bank A use the all-input reversible copy

    C_rec |alpha,psi,r> = |alpha,psi,r XOR alpha>.

The actually recorded whole word is

    V_rec=C_rec(U tensor I_128).                            (8)

Bank A is retained, not erased; if initialized blank, it records the complete
original alpha. The pointer itself remains available, so arbitrary previous
A-inputs are also reversibly recoverable. A previously retained oldRIGHT
reference R is a SEPARATE spectator and can be tensorized with identity; it
is not silently reused as this fresh bank. This is a declared recording
extension, not an assertion of free availability, zero printing cost, or
identity with every oldRIGHT implementation. Its additional actually selected
ledger must be included where a paid-history valuation requires it. The heat
calculation uses the full gate rather than pricing it by inference.

Generally V_rec is not an involution and its spectrum varies. Its dimension is
`2048*128=262144`. The original labelled DATA/oldRIGHT conditional maps remain unchanged; the
newly enlarged output also includes the explicitly recorded alpha copy. The
coherent extended column is related to the previous column by this declared
isometry, not literally the same vector in a smaller space. No binary
coarse-graining or projection onto a selected success is used.

### Exact small-matrix reduction of all record sectors

Fourier-transform the XOR bank over `(Z/2)^7`. Every character k gives a
whole-word sector `V_k=D_k U`, with

    D_k|alpha,psi>=(-1)^(k dot alpha)|alpha,psi>.

Define the genuine16x16 compression

    A_k=T* D_k T
       =[p^2+(-1)^(k_b)p] sum_j (-1)^(k_j dot j) N_j N_j*.  (9)

Keep all128 characters. For every positive integer ell,

    Tr(V_k^ell)=Tr(D_k^ell)-16[1+(-1)^ell]
                  +2 Tr T_ell(-A_k),                      (10)

where T_ell is the Chebyshev polynomial. One proof uses the determinant lemma:

    det(zI-D_k U)
     =(z-1)^(n_+-16)(z+1)^(n_--16)
         det[(z^2+1)I+2z A_k].

When an exponent is negative this is a rational identity whose factors cancel;
no negative physical multiplicity is assigned. Analytic continuation covers
A_k eigenvalues at +/-1. The reciprocal-root sum gives (10). Equivalently use
the invariant span of T and D_k T. Summing over the128 characters gives the
ENTIRE trace of `V_rec^ell` and all its existing derivatives.

The true derivative of every N_j is retained. A stable implementation uses

    T_0=I, T_1=-A_k, T_(ell+1)=-2 A_k T_ell-T_(ell-1)

and the differentiated matrix recurrence. It neither differentiates unstable
eigenvectors nor freezes the row-refinement operators. In particular,

    Tr V_rec=128 Tr(I-2p^2 Delta_CAR),
    D Tr V_rec=-256p^2 D Tr Delta_CAR,   Delta_CAR=N_0* N_0. (11)

This proves directly that the complete recorded heat has a source even when
the bare reflection's heat source is zero.

## 5. Actual original-fixture calculation and numerical trust boundary

Use the pinned original CAR order `(0,2,3,1)`, phases `(i,i,-1,-i)`, nu=3/5,
and rapidity `theta=log(5/4)=2 atanh(1/9)`. Derivatives below are d/dtheta,
NOT d/dr; dtheta/dr=2.025 at this point. Every original128 Kraus slot remains.

The positive Fourier coefficients in (3) were computed without an FFT:
the three collective scene modes use an ordered3x3 Laurent recurrence; the
other8+10+12 modes use their positive Bessel series. Outward90-digit intervals
and a degree64 exponential-tail majorant give a common coefficient error
below1.014e-97. This retains all33 modes. Interval endpoints are serialized
with directed Decimal rounding rather than rounded-to-nearest printed bounds.

The source evaluation then combines these coefficients with double-precision
native operator moments. It is NOT an interval enclosure of the original
Kraus matrices. Independent finite differences rebuild the original word and
differentiate the small winding part, not the difference of two H-values of
size~23 whose tiny difference would round to zero.

| m | computed d_theta H_hist | general bound using 2||dQ||_F |
|---|---:|---:|
| 3 | +7.04558057555e-11 | 1.10104e-4 |
| 11 | +1.54843552856e-29 | 3.49758e-23 |
| 15 | +6.15093505354e-40 | 1.55218e-33 |
| 16 | +1.30570218580e-42 | 3.36861e-36 |

The whole-word norm estimate is `||DV_rec||<=2||DQ||_F≈1.38653` here, because
the actual recording map is fixed. The bare reflection has exactly zero heat
source. With the protected A-bank support of rank128, per ONE passive reference copy,
the initialized feedback source is `d_theta J_pre≈-2.344012184324785e-6`. These numbers refer to
the same native Fourier parameter but different explicitly specified heat
operators: the new incidence H_hist is NOT added to the old paired H_cut.
Only the chosen single heat is used in H+J.

For the full product return cut with scene identity, J additionally carries
the REAL rank33 factor; for a fixed protected scene subspace of rank r_S it
carries r_S. The reported J_pre is per scene copy and per passive reference copy, with
A-rank128. The pre-existing oldRIGHT, if it has rank128 as in the original
packet, supplies an ADDITIONAL spectator multiplier128: it adds log(128)/beta
to heat, leaves its derivative unchanged, and multiplies J and its derivative
by128. Equal numerical register sizes do not identify the two registers.
The reported heat/J ratio is conservative relative to the full33-scene and
oldRIGHT-multiplied feedback, not a silent equality of normalizations.

The test clocks in this table are mathematical diagnostics. No claim is made
that m=15 or m=16 is the paid elementary duration of the original full128
implementation. The explicit earlier nine-block forward macro-word, expanded
as `W=H D H`, plus recording and closing idle, has a15-stage block schedule;
its full primitive expansion and actual cost may be longer. This identity
is not a license to pad a clock merely to obtain a desired source bound.

## 6. Feedback and heat can be evaluated on one cyclic execution

For a declared word with final closing idle, use transported source projectors
`P_t=V_t P_0 V_t*` up to the last real gate and set the terminal projector back
to P_0. On the whole stage sum, the complementary Book feedback is zero on
every transported interior transition and on the closing idle; only the
actual return comparison survives. This is the existing autonomous-clock
identity, applied to the true recorded word.

The reversible fine-record copy commutes with the initialized return projector
`P_0=|alpha=0><alpha=0| tensor I_DATA tensor I_record`. Therefore its feedback
is precisely the already owned

    F_pre=I-K_0* K_0=4p^2 Delta_CAR(I-p^2 Delta_CAR),
    J_pre=-128 Tr_16 log(I-zeta F_pre).                      (12)

Tensoring a protected scene support or the separately retained oldRIGHT adds
its actual rank multiplier. Equation(12) is per passive reference copy. There
is no m factor in the feedback logdet with this one-return cut. The heat
trace (3) still includes every stage and every fibre mode. Thus the complete
FIRST field source for the declared Section03.25-type realization is

    D(H_hist+r_S J_pre)=r_S D J_pre+D H_hist,                (13)

with exact formula(3) and uniform bounds(5)-(6) for the last term. No source
cancellation, new fitted counterterm, discarded archive or extra CQ price is
used. If another P_N or another complete ledger is actually selected, its
source must be included instead of assuming(13).

## 7. Global refinement consumer: physical clock growth suppresses this heat beyond every power

This is stronger than a one-fixture estimate. Suppose an already justified
family of executions satisfies, as h->0:

1. fixed beta and the graph/fibre hypotheses of section1;
2. actual clock length m_h>=c log(1/h), c>0, arising from the executed programme;
3. ||DV_h||, ||D^2V_h|| and any chosen inverse nonzero source normalization grow
   at most polynomially in h^-1 in the stated field norms.

Then(7) and m!>= (m/e)^m give

    C1(m_h), C2(m_h)=o(h^N) for EVERY fixed N>0.

Therefore the normalized heat FIRST AND SECOND source tends to zero faster
than every prescribed polynomial order. For a growing field dimension, the
row-sum factor is retained; polynomial growth can be absorbed in the same
estimate. This conclusion does not follow merely from small heat values.
It uses explicit derivative bounds.

Polynomial word-jet control has a direct compositional sufficient condition:
for a product of unitary gates, `||DV||<=sum_t||DU_t||` and
`||D^2 V||<=sum_t||D^2U_t||+sum_(s!=t)||DU_s||||DU_t||`.
Thus polynomially many gates with polynomially bounded native derivatives
suffice; no exponentially bad product norm is needed on the real unitary chart.

The original Golden address-coverage owner supplies an actual logarithmic
COST-depth schedule. It is a potential consumer, not an automatic proof of
all three hypotheses: variable stopping, primitive expansion, scene placement,
actual field writer and source normalization still need their same-execution
identification. We do not insert a longer artificial programme for free.

If a matching feedback root has a verified Banach/degree margin, (5)-(6) are
now an explicit heat acceptance test in that SAME field norm. For example,
the normalized heat budget is bounded by `|a_h| C1(m_h) sup||D_i V_h||`.
The old J2 or paired-spectral root is not promoted by substituting the one
rapidity number in section5 for all42 derivatives. Source convergence also
does not by itself imply recovery of exact lattice roots or Einstein dynamics.

## 8. Essential guards: where the theorem does not apply

- **Scene-dependent placement.** If U_t depends on the scene vertex, prefix
  trivialization changes horizontal connections and produces mixed short loops.
  Then heat can see the field long before winding the whole clock.
  The checker gives a direct example on `K2 x C15`, with a phase y on one
  vertical edge: `D_y Tr L^4=-8 sin(y)/81`. At y=.41 its actual heat derivative
  is about -2.2875921e-5. It is not bounded by the homogeneous tiny constant.
  This is not a no-go for GR: it identifies the real additional local-curvature
  source that a spatially varying scene map would need to retain.
- **Different heat operator.** A scalar scene Laplacian, paired-cut Hodge,
  tensor-sum heat and the normalized product-incidence operator(1) have different
  spectra. No equality between them is asserted.
- **Moving base graph or beta.** Their source is additional and is not in(5).
- **Unprepared completions.** Channel equality alone does not select V_rec on
  every column. The explicit original W is part of the input here.
- **Physical admission and cuts.** No algebraic identity forces this graph,
  independently actuated controls or a particular Book03 P_N. No cost is erased
  by Fourier/gauge changes used solely in the calculation.
- **GR status.** The result supplies a genuine cyclic-incidence heat source
  and a uniform remainder theorem. It does not construct the missing native42
  field writer, solve all independent physical inputs or establish generic GR.

## 9. Sources and reproduction

Pinned inputs: original native excerpt Git blob
`ed8a505d00337037d7aec976098717c3a4c43308`, and native-block constructor
`de371c016bfd1bbc1222971589fc51ac6786c1eb`, both checked at runtime.
Book03 blob `ecdd31abb52c94e9f2a157a80c7c49a6f5ac31aa`, sections03.1.2,03.25;
Book06 blob `99721fb50de66688564638f5f2b449a38675d7bd`, heat/clock distinction.
The J2 comparison note's open-path/cyclic warning is consumed explicitly.
The preceding native-block heat-transport packet is preserved unchanged.

Standard scalar reference: NIST DLMF https://dlmf.nist.gov/10.35 and
https://dlmf.nist.gov/10.25 (Bessel generating and positive power series).
No external reference is used to replace an unproved D0 physical selection.

Reproduce without overwriting receipts:

    OPENBLAS_NUM_THREADS=1 python interval_coefficients.py
    OPENBLAS_NUM_THREADS=1 python check_scene_heat.py
    OPENBLAS_NUM_THREADS=1 python -O check_scene_heat.py

The full checker passes105 non-removable controls in both modes with identical
JSON. Direct finite controls include the actual198-dimensional scene-clock
Laplacian and its Duhamel source, a384-dimensional recorded-clock heat, all128
native character sectors, and independent rebuilt word derivatives. General
identities and source bounds are proved above; floating fixtures are not an
interval root certificate or an independent formal proof of the whole theorem.
