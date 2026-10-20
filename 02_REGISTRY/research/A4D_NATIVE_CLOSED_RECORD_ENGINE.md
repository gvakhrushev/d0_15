# A closed retained-record engine, exact memory and hereditary refinement

Date: 13 October 2026. Existing Draft #310. Input SOURCE
`585a6c21e09c07d7704c6c7ef1e2e0b45ba9b83a`; main
`fa2b04b9c8aae5a0b8470322d6091712ce56567a`.

**Result.** The literal full native record has a nonempty, indefinitely
iterable sector in the previously stated endpoint-pairing binding. An actual
blank seed enters it after two ticks. All sixteen exterior components are
retained; the observer is recomputed from the current matter, without an
iteration input, a reset, a new blank or an external history. The visible
scalar/first-grade pair becomes a two-cycle, while the retained higher
grades never repeat. The complete previous state is algebraically recoverable
on this orbit. Exact finite storage is explicitly charged, rather than hidden
inside arbitrary-precision amplitudes.

The actual archive projections give a hereditary pullback which commutes
with this local engine. This is a concrete compatible building block for the
common preparation arrow. It supplies neither an endogenous trigger for
refinement nor a link/affine evolution. This packet does not install either
as a physical law. The endpoint-isometry and constitutive-admission premises
of [the preceding result](A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md) remain.
The original #310 fixed-source/raw-owner terminal and #202/#317 are unchanged.

## 1. State, apparatus and transition

Take Q=G=I, q=eta=diag(1,-1,-1,-1) on the full real exterior fibre. Use the
actual CAR gate (3) and the original price cut of the preceding packet.
In occupation-mask order retain every coordinate m_0,...,m_15. Consider
the collinear invariant sector

    m_2=m_3=m_4=m_5=m_8=m_9=0,   y=m_1 != 0.

These are three spatial first grades and three mixed second grades, not
discarded coordinates or a physical gauge quotient. The other ten
coordinates are free before the further invariant-band restriction below.
The actual observer is n=sign(y)e_0; k=y^2. Thus the solved endpoint metric
is eta again whenever the next y is nonzero. Spatial D=I and b=0 on a
homogeneous periodic carrier satisfy D q D^T=q at every tick. The local
executor does not supply a spatial interaction or a temporal link equation.

Let a,p>0, a^2=p, p+p^2=1. For each spatial mask M not containing e_0,
write x=m_M, v=m_(M union {0}), and sigma=sign(m_1). The **full** operator is

    spatial degree 0 or 1: (x,v) -> (a x-sigma p v, sigma p x+a v),
    spatial degree 2 or 3: (x,v) -> (a x-sigma p v,-sigma p x-a v). (1)

The certificate compares all sixteen basis columns, for both signs,
directly with the published intrinsic CAR formula. It does not replace
the native operator with a fitted low-dimensional matrix. Each fixed-sign
operator is orthogonal. Its transpose supplies an algebraic inverse;
physical permission to run an inverse remains a separate question.

The Python `State` contains precisely the sixteen current field values.
`step(state)` reads only that state. The loop ordinal in the diagnostics
is not a clock field, a phase schedule or an input to the transition.
The basis/bit roles and immutable gate program are the declared apparatus
data of this local model. Their manufacture from M1 is not asserted.

## 2. One actual seed, a uniform all-time domain and retained history

Use the genuine whole-blank seed m=e_0+Omega. Its norm squared is 2;
division by the one constant sqrt(2) gives a normalized state and does not
change any observer, gate or projective statement. In the following table
only four nonzero coordinates are displayed; the executor keeps all sixteen.

| State | scalar x | first grade y | spatial top b | full top c |
|---|---|---|---|---|
| seed | 0 | 1 | 0 | 1 |
| first output | -p | a | -p | -a |
| second output | -2ap | 2p-1 | 0 | 1 |
| third output | 5p-4 | a(4p-3) | -p | -a |

Define A=(-2ap,2p-1), B=(5p-4,a(4p-3)). The golden equations imply

    3/5 < p < 5/8,  a>3/4,
    A_y > 1/5,  B_y < -3/8,
    lowerStep(A)=B,  lowerStep(B)=A.                  (2)

For example the p bounds follow by substituting their rational endpoints
in p+p^2=1 and monotonicity on p>0. The a bound follows from a^2=p>3/5.
The two identities follow by reducing a^2 to p and p^2 to 1-p.
The first two y values are also greater than 1/5. Consequently the seed
orbit is defined for **every** finite number of transitions, with

    |m_1|>1/5,  k>1/25.                              (3)

This is an induction on an invariant two-band domain, not a finite-run
extrapolation. More generally tA/tB with t>0 and arbitrary eight spatial
degree-2/3 coordinates form a closed sector. The absolute bound scales by t.
The full native state class, noncollinear perturbations and physical
admission of this sector are not classified by this theorem. The previously
published genuine blank which has zero output first grade still fails.

On each higher spatial pair let

    H+ = [[a,-p],[-p,-a]], H- = [[a,p],[p,-a]],
    R=H- H+ = [[r,-s],[s,r]],
    r=2p-1, s=2ap, r^2+s^2=1.                       (4)

From the second output onward the actual signs alternate +,-. After k
complete returns the seed's (b,c) is R^k(0,1); at the intervening tick it
is H+ R^k(0,1). Nothing is reset when the lower pair returns to A.

Here R has infinite order. A proof avoiding numerical rotation-angle
recognition is useful. Its cosine coordinate is T_k(r), where

    T_0=1, T_1=r, T_(k+2)=2r T_(k+1)-T_k.

It belongs to Z[p]. Apply the exact conjugation p -> p'=-1-p.
Then r'=-3-2p=-C, C>4. Put Z_k=(-1)^k T_k(r')=T_k(C).
The recurrence proves by induction Z_0=1, Z_1=C, Z_(k+1)>=C Z_k
and therefore Z_k>=C^k>4^k for k>0: once Z_k>=Z_(k-1)>=0,
`2C Z_k-Z_(k-1)>=(2C-1)Z_k>=C Z_k`.
If R^k=I for k>0 then T_k(r)=1 and hence T_k(r')=1, a contradiction.
Equality of two seed return states would fix (0,1) under a nonzero power
of the rotation; that forces the power to be I. Odd and even states have
different lower pairs, and the two initial states have different lower
pairs from A,B. Thus **all states on the full seed orbit are distinct**.

There is an index-free predecessor decoder on this orbit. Recognize the
seed and its first two successors by their complete states. For later
states use the transpose of U_(-sign(y)); its predecessor has the opposite
sign. This recovers the actual preceding full state; iterating the decoder
recovers the finite prefix back to the seed. It uses no persistent external
journal. The orbit-membership premise is essential: state-dependent
orthogonality is not a proof of injectivity on every native state.

The diagonal full-top readout c^2/2 is an internal observable in the
prepared exterior apparatus, although a finite experiment cannot know an
arbitrary real probability exactly. Even this readout differs at different
complete returns: equality of the cosines squared would make a sum or
difference of the two rotation powers a multiple of pi and imply a
nonzero finite order. This is distinct from a finite-resolution detection
or independent-verification theorem, which is still needed physically.

## 3. No free infinite-precision memory

The executable uses canonical elements of Z[a], a^4+a^2-1=0, with four
integer coefficients in the basis 1,a,a^2,a^3. This basis is unique:
p has degree two over Q; if a lay in Q(p), the norm of a^2=p would be
the square of a rational number, but Norm(p)=-1. Hence a has degree four.
Every arithmetic operation and every sign decision in the engine is exact.

The sign algorithm first compares u+vp using integer squares against 5.
For X+aY with X,Y in Q(p) of opposite sign, it compares X^2-pY^2.
Equality with nonzero X,Y would contradict the same degree argument.
No numerical approximation controls the observer or the transition.

Write c_(2+2k)=T_k(r)=u_k+v_k p and H_k=max(|u_k|,|v_k|).
Since |p'|=1+p and C>4, the preceding proof gives

    (2+p) H_k >= |u_k+v_k p'| = Z_k > 4^k,
    H_k > 4^k/3,                  k>0.              (5)

Thus the integers which the executable really stores become unbounded,
even though the real norm of the entire state is exactly 2 at every tick.
This is a rigorous coefficient-storage bound for this explicit codec.
It is **not** a lower bound against every compressed representation. A
symbolic seed-and-power representation can be much smaller but must itself
store an unboundedly distinguishable power/state. Independently of codec,
N distinct exact states require at least N store configurations, or
ceil(log2 N) bits for a binary store. A finite prefix does not imply
unbounded physical precision or future expansion of the real universe.

All 64 signed integers are encoded by a self-delimiting binary code; the
decoder reconstructs the entire matter state exactly. `bounded_step` rejects
both an oversized input and a next state which exceeds a stated capacity.
It never rounds, resets, silently allocates cells or keeps a hidden history.
The audit counts persistent data, not the compiler, program or peak arithmetic
workspace. It is not an independently derived physical bit-per-cell law.
The canonical code size need not increase at every tick; (5) proves
unbounded required capacity along the returns, not monotonic local volume.

## 4. Genetics as hereditary preparation on the actual archive tower

Use the owned ArchivePoints_n=Fin((n+2)^4) and the actual adjacent projection
pi_n(y)=y mod (n+2)^4. Do not replace their composites by one distant modulo
map or identify their levels with a physical metric mesh without a bridge.
For a field f of the full states define the ordinary pullback

    (J_n f)(y)=f(pi_n(y)).                            (6)

This is literal inheritance of the entire current state under one immutable
rule. It adds no random mutation, selection score, freshly initialized
detector or different gate for children. For the pointwise engine T,

    T_(n+1) J_n = J_n T_n.                           (7)

Proof: both sides at y apply the same function (1) to f(pi_n(y)). This holds
at every level and after every number of ticks on the admitted local sector;
it is not extrapolated from the first three finite tests. The surjectivity
of pi_n lets one recover each parent value from its equal children.
The inverse-limit/profinite carrier from the existing condensed owner is
therefore actually used as a compatible support, at its stated set-level
scope. No linear heat-operator naturality is inferred from (7).

The first projection has child multiplicities 5 or 6. Unscaled pullback is
therefore not an isometry for the two unweighted counting pairings.
There are two equivalent, explicitly conditional descriptions of an
isometric hereditary embedding. In counting coordinates set

    (J_iso f)(y)=f(pi_n(y))/sqrt(d_(pi_n(y))),

where d_x is the fibre cardinality. Alternatively retain (6) and use
positive weights mu_(n+1)(y)=mu_n(pi_n(y))/d_(pi_n(y)). Conservation of
parent weight and symmetry among its children uniquely give those weights.
The local gate is positively homogeneous and its observer and Q are
unchanged by positive rescaling, so the normalized embedding also satisfies
(7). This is an exact compatibility construction **conditional on those
pairing requirements**, not a derived physical measure/heat-action law.

The executor keeps refinement as an explicit adapter. It does not call it
whenever the external loop reaches a chosen number. Its capacity diagnostics
also display the least (n+2)^4 exceeding the code length under the declared
one-audit-bit-per-point convention. That column neither schedules the engine
nor defines the physical information capacity of ArchivePoints.

Cloning a spatially constant field remains spatially constant. The initial
torus and K(9,11,13) owners are preserved, but no toral transport, graph
interaction or characteristic speed is silently appended to this local
record. Their actual coupling is precisely the next constitutive arrow;
copying a state does not by itself supply it.

## 5. Existing price and the next sharp question

The original P=I-N is the same for observers +e_0 and -e_0. At each adjacent
pair of actual seed gates their signed angle is +1 or -1. Substitution in
the already derived complete chronological determinant gives in both cases

    det(I_16-z F)=(1-4 z p^3)^4.                     (8)

For angle -1, A=1, B=1-4zp^3 and C=(1-4zp^3)^2; for +1, A=B=1-4zp^3,
C=1. Thus the unbounded retained history is invisible to this particular
two-tick price along this orbit. It is not absent from the full state.
This is not a claim that all ten metric derivatives vanish, or that the
whole Hodge heat/source or all native stress is zero. The prior transverse
joint differential, its matter terms and the nonzero factor-heat jet retain
their scopes. No native on-shell or curved GR claim is obtained by this run.

The next engine experiment is now an exact question, not another candidate
census: **which already owned same-state preparation/interaction couples
the increasing retained distinctions to archive allocation and the
constrained (q,D,b,m) transition?** It must specify the capacity/readout
comparison internally, preserve prior required distinctions under the actual
projection and carry the full price/tangent. One must derive its transition
from the owned operation/price, rather than insert `stage += 1`, a new force,
a source-fitted term or a geometry-growth animation. This remains the same
common-preparation obligation of G0, feeding G1-G4 and the original terminal.

## 6. Executable evidence and proof boundary

Run `python3 02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py
--steps 4096` for a compact reproducible trace. Add `--capacity-bits 256`
to test the finite-store stop. The paired exact checker derives the native
matrix identities, all-time-band algebra, return recurrence and conjugate
growth, checks storage/rewind on a long exact run, exercises the actual
hereditary projections and rejects specified mathematical mutants.

The generic research Lean capsule proves the golden rational bounds,
lower-band closure/nonzero iterates and the growing-conjugate recurrence.
It lives outside the supported CORE import tree. Native sixteen-row
binding, the degree/conjugation argument and hereditary physical admission
must not be advertised as fully Lean-formalized by that capsule. Its actual
declarations, axioms, source hashes and compilation output are recorded in
the associated receipt. Finite checks supplement the general proofs above;
the 4096 ticks do not prove an infinite-duration physical universe.
