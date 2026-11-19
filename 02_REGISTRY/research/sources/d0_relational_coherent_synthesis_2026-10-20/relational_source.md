# Relational orientation transport removes a spurious selection requirement

Read-only analysis of PR #334 at `0e4c9d6ca8b44574100338b04c27204cde7062dc`.
Consumers: `constitutive`, `contrast_refinement_transfer`, `on_shell_stationarity`.
This does not duplicate the generic transfer work in #386.

## Exact statement on the existing six-face source

Use the existing Lorentz metric eta, the four coframe columns e_r, and actual
based plaquette holonomies P_rs assembled from shared original Role links.
Put

    F(P) = (P - P^-1)/2,
    B_rs(e) = eps(r,s,u,v) Hodge(e_u wedge e_v) eta,
    f_rs(e,U) = -Tr[B_rs(e) F(P_rs(U))]/2,
    S_star = sum over r<s of f_rs.

Here u<v is the complementary Role pair and * is precisely the owned
Lorentzian Hodge operator. Overall constants remain those of that owner.

There are three different transformations, which must not be conflated.

1. **Passive reorientation of a based face.** Replace its oriented boundary
   word by its inverse, P_f -> P_f^-1, and its dual oriented coframe bivector
   by -B_f. The complete geometric contribution is unchanged:

       -Tr[(-B_f) F(P_f^-1)]/2 = -Tr[B_f F(P_f)]/2.

   Reorienting any subset of the six faces leaves the whole action identical
   as a function of ALL original coframe and shared-link fields. Consequently
   all 16 coframe plus 24 link derivatives at each site, all mixed jets, and
   the original global action/source are unchanged. Shared links need not be
   replaced by independent face variables: this is equality before pullback
   through the actual plaquette map. The inverse boundary is based at the same
   point. If another base point is used, include its ordinary transport.

2. **Proper local frame change.** For L in SO+(1,3), based curvature and dual
   coframe insertion transform together:

       F_f -> L F_f L^-1,   B_f -> L B_f L^-1.

   Cyclicity of trace gives the same scalar density. On actual lattices use
   the endpoint gauge action on each link; every based face transforms at its
   base point. For a fixed frame transformation T_L of the field chart,

       S_star o T_L = S_star,
       DS_star(T_L z) o DT_L(z) = DS_star(z).

   Thus Euler covectors transform by pullback; their numerical coordinate
   components are not asserted to be identical. For field-dependent gauge
   choices the chain rule includes the gauge derivative; gauge invariance
   annihilates the added vertical first derivative. At a stationary point the
   Hessian has the usual pullback congruence.

3. **Active inversion with the coframe/reference fixed.** Replacing P_f by
   P_f^-1 while retaining B_f negates f_f. This is a different change of the
   physical input/readout, not a passive relabelling. Simultaneously inverting
   independently prescribed faces may not arise from any common shared-link
   field, which must also be checked. A path and its inverse can of course be
   distinct paid executions and distinct future-memory records.

The first identity is compatible with the original retrospective memory
boundary: it does not identify all future observations of the two histories,
erase a clock, or set their execution costs equal. It only says that a
particular relational geometric observable and all of its field sources are
well-defined independent of the convention used to orient its face.

## Golden signed-marker transport

In the owned positive-root chart the two original Golden probabilities have

    q_(a,+) = k (m+s_a)^2,  q_(a,-) = k (m-s_a)^2,
    R_a = sqrt(2)/(2 sqrt(k)) [sqrt(q_(a,+))-sqrt(q_(a,-))]
        = sqrt(2) s_a.

Inversion exchanges the two outcome labels and sends R_a to -R_a. Expand the
same actual coframe insertion in the dual readout coordinates, B -> (b_a).
Passive face reorientation sends every b_a to -b_a, so

    sum_a (-b_a)(-R_a) = sum_a b_a R_a.

This exact identity holds before differentiation, including moving coframes
and the already-owned same-class normalization. The all-40 source identity
therefore survives the positive Golden representation. This is not the claim
that fixed Euclidean laboratory probe coordinates are Lorentz invariant: a
frame change transports the actual observer/probe basis and its dual pairing.
The physical G0 implementation and payment of that transported reference are
still required by the original programme.

For a pair of symmetrically weighted inverse face descriptions, w_f=w_bar_f,

    (w_f f_f + w_bar_f f_bar_f)/(w_f+w_bar_f) = f_f,

because f_bar_f=f_f after relational orientation transport. In contrast,
unmarked curvature averages to F(P)+F(P^-1)=0. Thus even history weights and a
reversal-invariant complete relational density do not force geometric source
cancellation. This is precisely where retaining the coframe/reference in the
source map matters. It is not a derivation of the charged physical action from
these weights.

## Exact hostile witness and all-40 check

The standalone `check_relational_source.py` uses only SymPy rational arithmetic.
Four actual noncommuting proper Lorentz links generate all six shared faces.
At an invertible rational coframe the existing six-face density is

    S_star = -98913/160000 != 0.

For 16 independent coframe and 24 proper-link tangent directions it checks:
original jet = jet after reorienting faces {0,2,5} = pulled-back jet after one
noncommuting proper boost/rotation frame change = both transformations.
All 40 exact equalities pass. This is a one-site four-shared-link fixture of
the universal algebraic identity, not a claim that one site is a full refining
lattice.

A smaller witness exposes the sign issue. Let J=J23 and let P be the spatial
23 rotation with cos(theta)=3/5 and sin(theta)=4/5. The proper, time-orientation
preserving matrix L=diag(1,-1,1,-1) has det L=1 and L J L^-1=-J. Therefore a
fixed-frame J23 coordinate changes sign under an allowed spatial frame change.
However

    -Tr[J F(P)]/2 = 4/5,
    -Tr[(-J) F(P^-1)]/2 = 4/5,

so the two relational descriptions contribute 8/5, not zero. The same example
is also carried by the positive Golden signed markers. No arrow of time and
no reversal-odd primitive fee is used in this identity.

## Precise consequence for the prospective-minimum theorem

The new `ProspectiveReversalSymmetry.unique_minimum_signed_zero` theorem is
correct. Its required signedSource must genuinely be odd under the same
involution that preserves the whole feasible set and full price.

It cannot be applied to the complete Palatini density under passive face
reorientation: that density is EVEN. Nor does its uniqueness hypothesis follow
from uniqueness of the physical geometry. If pi(h) is a geometric readout and
pi(R h)=pi(h), two distinct equally priced histories h and R h can yield the
same unique geometric result. Their retained operational records may remain
distinct. No deletion of those records is licensed.

Consequently the constitutive target should be **nonzero coframe-referenced
curvature coupling in the selected full source**, not selection of the sign of
an uncontracted fixed-frame J23 component or a unique oriented microscopic
history. This keeps the already-owned indispensable alpha != 0 Palatini
channel. It removes the stronger, unnecessary prerequisite of deriving a
physical time-arrow or reversal-breaking microscopic price before a nonzero
Einstein source can exist.

## Narrow audit of current language

`A4D_PROSPECTIVE_DMIN_REVERSAL_SYMMETRY_CHIRAL_EULER_SOURCE_AND_GOLDEN17_INFORMATION_COST_2026_10_20.md`
section 1 and its section 4 quoted next-step criterion are valid for their
explicitly specified **unique odd response**. They should remain. That
criterion must not be read as a necessary condition for the full GR source:
first establish whether the actual observer/coframe transforms and whether
the proposed physical scalar is odd. The retained pair benchmark with the
same fixed J23 tester is an active experimental comparison and is also valid;
it is not a counterexample to the relational even contraction above.

`A4D_COMPLETE_BOOK_GOLDEN_SELF_CODE_STATIONARY_ENVELOPE_AND_ODD_GEOMETRY_2026_10_20.md`
section 4.1 correctly excludes probability-only permutation-invariant coding
as the source of a fixed-reference linear signed mark. Its conclusion allows
the original Book/CAR/Gamma feedback with a paid coframe reference; that is
exactly the relational branch above. There is no need to retract that result.
The clarification is that reference-sensitive coupling does not imply a
fundamental violation of frame/reorientation symmetry or a time arrow.

The existing pretrace and CAR trace results already contain the two algebraic
ingredients separately. The new synthesis is their application to the later
prospective-symmetry criterion, with exact all-40 source transport, removing a
specific stronger premise from the proposed route. It does not derive the
remaining actual paid G0 constitutive law, its alpha coefficient, the matter
source, or its refinement limits.
