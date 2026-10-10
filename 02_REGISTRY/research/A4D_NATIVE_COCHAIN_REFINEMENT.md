# Native cochain refinement: operators, normalization and readout boundary

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Input head: `227c1609c41b720dcfb7517a8e57f0e8d76cb764`.
CONTROL/main baseline: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Status: **general finite construction and scoped composed-readout obstruction**,
pending CONTROL acceptance. Positive GR and global closure remain OPEN.

The frozen maps described by `Archive1DCochainRefinement` really form an
unscaled cochain map. This note constructs them, binds the vertex map to the
actual archive matrix, and proves their norms. The actual `dForward` uses a
level-dependent factor L, requiring a degree-dependent correction. The full
counting Gram trace is 625 at L=2; 256 is a different, partially normalized
trace. Exact finite chain compatibility does not imply consistency with the
physical fixed-torus sampling maps: the composed frozen lift fails even on a
constant smooth one-form when L is doubled.

No action, selector, physical equation or stationarity gate is introduced.
The frozen maps are constructed from the existing comments and projection.
Their necessary normalization is computed, not selected as a physical law.

## 1. Literal one-dimensional construction, all sizes

For L>=2 let C_L have vertices and positively oriented edges indexed by
0,...,L-1; the last edge wraps to zero. Define

    (D_L f)(i) = f((i+1) mod L) - f(i),
    (B0_L f)(i) = f(i) for i<L, and f(0) for i=L,
    (B1_L a)(i) = a(i) for i<L, and 0 for i=L.

B0_L is exactly `archiveLiftOperator (L-2)` acting on vectors, since the
actual projection is i mod L. B1_L copies the L old edges and annihilates
the new collapsed edge. No injective-inverse or approximate interpolation
hypothesis is needed. With the ordinary real counting pairings,

    <B0 f,B0 g> = <f,g> + f(0)g(0),
    <B1 a,B1 b> = <a,b>,
    B0^T B0 = M_L = diag(2,1,...,1),   B1^T B1 = I_L,
    D_(L+1) B0 = B1 D_L.                                      (1)

The last equality follows row by row: the first L-1 differences copy;
row L-1 is f(0)-f(L-1); row L is f(0)-f(0)=0. Thus it includes the wrap
and collapsed edges. The associated energy pullback is

    B0^T D_(L+1)^T D_(L+1) B0 = D_L^T D_L.

It is not a Laplacian intertwiner L_f B0=B0 L_c. In particular it does not
contradict the adjacent-spectrum obstruction already proved in
[A4D_NATIVE_WEIGHTED_TRACE_LIFT_BOUNDARY](A4D_NATIVE_WEIGHTED_TRACE_LIFT_BOUNDARY.md).
For L>=3, D_L^T D_L is the canonical simple-cycle graph Laplacian. At L=2
it is twice that graph Laplacian because oriented incidence retains both
edges between the two vertices. This exception is explicitly tested.

The [Lean capsule](certificates/a4d_native_cochain_refinement.lean) proves
both bilinear Gram identities, (1), scalar linearity, literal projection
and matrix bindings, energy pullback and the scale identity. Its m+1 size
parameter is generic, not a fixed-size matrix fixture.

## 2. All 16 sectors and the actual forward scale

Use the owned site space `(ZMod L)^Role` and Fock labels `Role -> Bool`.
The equivalence `archiveRolePhasePointGroupEquiv` identifies each coordinate
with Fin L. The order A,B,C,D is the actual `roleOrderIndex` order. For an
occupied subset S, k=|S|, define

    B_S = tensor_(r in Role) (B1 if r in S, otherwise B0).

In coordinates, for y in {0,...,L}^4, let q(y)_r=y_r mod L. Then

    (B_S f)(y) = 1_[y_r<L for every r in S] f(q(y)).             (2)

This gives an explicit nonempty operator on every sector, with full domain
dimension L^4, including the occupied directions. On a creation block
S -> S union {r}, r not in S, apply (1) to coordinate r and leave the three
other tensor factors unchanged. The same fixed Jordan-Wigner sign multiplies
both sides. Already occupied directions give zero on both sides. Summing
these blocks proves the unscaled full graded chain equation for all L.
This is a general tensor proof; finite tests are not its induction argument.

The literal `ArchiveCubicalDifferential.forwardDifferenceScale N` equals
L=N+2. Its `dForward` is L times the unscaled graded operator. Consequently
B_S alone does **not** commute with actual `dForward` across levels. Let

    c_L=(L+1)/L,             Bhat_S = c_L^k B_S.

Then on each creation block

    (L+1) D_f c_L^k B_S = c_L^(k+1) B_(S+r) L D_c,

and hence `dForward_(L+1) Bhat = Bhat dForward_L`. The scalar identity
(L+1)c_L^k=L c_L^(k+1) fixes this correction once the vertex map is fixed.
The capsule proves the generic one-dimensional scaled block equation and
the literal owner scale. The full typed 4D `dForward` theorem through the
Fin/ZMod equivalence is proved analytically here and checked by exact finite
matrices; it is **not represented as already compiled in a supported Lean
owner**. The source-hashed owner formulas retain every creation sign and
scale. There is no renaming of a trace or cardinality theorem as a chain map.

One may instead use integrated-cochain coordinates L^(-k) times the
component fields, in which B_S is the chain map. Changing this convention
also changes field readout and norms; it cannot preserve every old formula
simultaneously. Section 5's component readout obstruction persists after
conversion back from integrated cochains.

## 3. Full Gram, trace and the meaning of 256

Tensoring (1),

    W_S = B_S^T B_S = tensor_(r not in S) M_L tensor_(r in S) I_L,
    W_S(x) = product_(r not in S) m(x_r), m(0)=2, m(j)=1 otherwise,
    Tr(W_S) = L^k (L+1)^(4-k),
    sum_(all S) Tr(W_S) = (2L+1)^4.                            (3)

The I_L factors still have trace L. They do not disappear from the full
site-amplitude carrier. At L=2 the per-sector values are:

| degree k | number of sectors | full counting trace | trace divided by 2^k |
|---:|---:|---:|---:|
| 0 | 1 | 81 | 81 |
| 1 | 4 | 54 | 27 |
| 2 | 6 | 36 | 9 |
| 3 | 4 | 24 | 3 |
| 4 | 1 | 16 | 1 |
| total | 16 | **625** | **256** |

`total_hodge_gram_trace_sum_eq` remains a true theorem about its defined
arithmetic constant 256. Its interpretation as the complete counting Gram
trace in the existing comments is not correct. Dividing each sector's trace
by L^k gives the partially normalized trace in the last column; this is an
explicit alternate trace functional, not an identity for the full trace.
One common multiplicative calibration cannot do this: the scalar sector
requires factor 1, while degree one requires 1/2. Normalizing both site
pairings by their full number of sites instead gives the common Gram factor
(L/(L+1))^4; at L=2 its total is 10000/81, also not 256.

For the actual scale-corrected maps,

    What_S = c_L^(2k) W_S,
    sum_S Tr(What_S) = ((L+1)+(L+1)^2/L)^4,

which is 50625/16 at L=2. These are positive counting Gram operators. None
of these trace identities establishes a Lorentz Hodge star, physical metric
uniqueness, a stress tensor or Einstein dynamics.

## 4. Actual metric-measure formula, all grades

Let all m_r(x)>0, mu=product_r m_r and c_r=mu/m_r. The already defined
owner expression is

    hodgeMetricMeasureWeight(k,mu,product_(r in S)c_r)
       = mu^(1-k) product_(r in S)(mu/m_r)
       = mu / product_(r in S)m_r
       = product_(r not in S)m_r.                             (4)

Both equalities hold for every finite S. The capsule proves them generically
with explicit nonzero denominators, using the actual owner definition with
integer power; no all-grade identity is supplied as a hypothesis. For the
scaled map use c'_r=c_L^2 c_r, which gives c_L^(2k) times (4). This computes
how the conductances must change under the convention, without asserting
that an independently owned physical constitutive law chooses them.

## 5. One-step estimates and composed fixed-torus failure

Declare the physical readout in this section: a smooth periodic k-form is
sampled as its fixed coordinate components f_S(x/L) on the unit four-torus.
Errors use normalized site-counting component norms. This is a specified
class, not a theorem about every possible native-to-physical readout.

For bounded Lipschitz f_S, each coordinate of q(y)/L differs from y/(L+1)
by torus distance at most 1/L. Except where an occupied direction hits the
collapsed edge, the Bhat error is bounded by

    A_L = (c_L^k-1) ||f_S||_infty + 4 c_L^k Lip(f_S)/L.

The exceptional-site fraction is at most k/(L+1), and there the error is at
most ||f_S||_infty. Thus

    ||error||_1 <= A_L + k ||f_S||_infty/(L+1) = O(1/L),
    ||error||_2^2 <= A_L^2 + k ||f_S||_infty^2/(L+1) = O(1/L).

For k=0 there is no exceptional set and the sup error is O(1/L). For a
constant unit one-form the exact one-step errors are 2/(L+1) in L1,
1/L in squared L2, and 1 in supremum norm. Uniform pointwise refinement
consistency is therefore false for this component convention.

More seriously, compose the **actual adjacent** maps from size L to K>=L.
Induction gives

    (P0_(K<-L) f)(i) = f(i) for i<L; f(0) for L<=i<K,
    (P1_(K<-L) a)(i) = a(i) for i<L; 0 for L<=i<K.              (5)

Each step appends one copy of the zero vertex and one zero edge. This is
not the single modulo map i -> i mod L when K>L+1. The scale factors
multiply to K/L. Tensoring and including the degree factor preserves the
exact graded chain equation at every K, but not physical resampling.

At K=2L a constant one-form along A is sent by Bhat to component 2 on
0<=i_A<L and 0 on L<=i_A<2L. The physical constant sample is 1 everywhere.
The normalized L1 and squared L2 errors are both **exactly 1 for every L**.
Even weak smooth testing fails: pairing the difference with sin(2 pi y_A)
converges to 2/pi. This follows either by the Riemann sum or the finite
identity sum_(j=0)^(L-1) sin(pi j/L)=cot(pi/(2L)). It is not a pointwise-only
obstruction. The effect is unchanged on L in 4N, or when only every fourth
archive level is displayed while using the composed native arrows.

A scalar/geometric control is Omega(y_A)=1+sin(2 pi y_A)/10. On the new
half the prolongated scalar is 1; the freshly sampled scalar is not. Its
normalized squared L2 error restricted to that half is exactly 1/400,
because sum_(j=0)^(L-1) sin^2(pi j/L)=L/2. The conformal coframe Omega I
is smooth, nondegenerate and has nonzero derivatives/curvature; it is only
a readout probe and is not an on-shell native solution. Arbitrary corrections
tending uniformly to zero in the sampled components cannot remove either
constant lower bound. Merely small averaged errors at a single coarse
vertex are not assumed to remain small after P0: that vertex has increasing
multiplicity. The certificate also checks that even an independently chosen
constant tail cannot exactly match the nonconstant scalar tail at the finite
sizes; no infinite lower bound is inferred from that extra control.

Therefore the full class consisting of frozen adjacent maps, their actual
composition, and ordinary fixed-torus component sampling cannot satisfy
uniform compatible resampling over scale intervals [L,2L]. This scoped
NO-GO remains true although one-step L1 error is O(h) and exact chain
compatibility holds. A physical action-contrast estimate needs its own
operator/action bounds and error propagation. These facts neither prove nor
refute every O(h) half-contrast transfer: an observable might discard the
bad directions, but such a factorization would need proof. Moving grids,
other readouts or other independently owned native arrows are outside this
class and are not silently introduced as repairs.

## 6. Reproducible evidence and remaining closure

The capsule compiles twelve propositions with 37 transitive D0 source pins.
All printed axiom dependencies are propext, Classical.choice and Quot.sound;
no sorryAx occurs. [Compiler output](certificates/a4d_native_cochain_refinement_output.txt)
and [receipt](certificates/a4d_native_cochain_refinement_results.json) preserve
actual exit status, source hashes and toolchain/manifest hashes.

The [exact checker](certificates/a4d_native_cochain_refinement_check.py) and
[immutable ledger](certificates/a4d_native_cochain_refinement_certificate.json)
replay 92 grouped controls. The 1D sizes are 2 through 8. Every sector and
every one of the 32 nonzero graded blocks is checked at L=2,3,4, on every
fine row, at both differential scales (5,184, 16,384 and 40,000 row equations).
The L=2 Gram calculation is independently repeated with actual 81-by-16
tensor matrices. Negative controls cover the missing scale factor, 256 versus
full trace, common versus degree-dependent normalization, energy versus
operator commutation, C2, and one-step versus composed readout consistency.

Replay from the repository root:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_cochain_refinement_check.py
```

The all-size proofs are in Sections 1–5; finite enumeration is not presented
as their proof. No supported Lean owner, registry claim or release is edited
in this research task. CONTROL can review the finite construction and the
explicit correction to the trace interpretation without declaring the
native physical refinement arrow complete. The original #310 fixed-source
raw-owner terminal and the independent #202/#317 terminals remain open.
Native action/variation transfer, its on-shell consequence, source/Ward,
nonlinear curved existence, soundness and recovery are still required.
