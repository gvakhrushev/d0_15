# Exact bridge from execution stationarity to the original field equations

20 October 2026. Read-only source inspection initially at
`024e7fd382e0fe5c5e0330f63ad367cd8e78babf`, reconciled with
`20d976647fa52e247d15139d3f4f14351f175b70`, existing PR #334.
No new physical selection law, action, task, terminal constraint or admitted
variation is proposed. The general variation/price-realization bridge is
ALREADY owned by `d0_native_joint_field_minimum_2026-10-20/
PROSPECTIVE_FIELD_REALIZATION_BRIDGE.md`, sections 2-4. It is consumed here,
not claimed anew. The new additions are its terminal adjoint and actual
priced-compensation test, and a terminal-constraint control on the already
owned whole-J2 carrier.

## 1. What the actual owners say

Repository-relative references at the inspected head:

* `01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md:125-131`
  names the complete stack, including terminal/boundary terms.
  Lines 166-176 give Cost-minus-Info and the MDL/stationarity sentence;
  lines 385-405 separately state `D S_stack=0` on `X_N` and the quadratic
  readout. This section does not define an execution-to-X_N variation map.
* `02_REGISTRY/aliases.csv:2` identifies the Book label `D0-ACTION-001` as
  LEGACY_BOOK_LABEL, with no independent release status. It is not a named
  theorem proving the execution-to-stack map.
* `03_FORMALIZATION/D0/Foundation/ProspectiveExecution.lean:85-90,144-156`
  supplies a price, initial state, goal and optimum over executable words.
  It supplies neither a smooth family of admissible words nor a field map.
  We do not repeat the older optimality-premise or empty-task boundary here.
* `03_FORMALIZATION/D0/Cosmology/FeedbackPartitionFunction.lean:33-45`
  proves a conjunction of explicitly supplied finite-source flags. It is not
  a derivative or an optimum-to-stationarity theorem.
* `03_FORMALIZATION/D0/Research/SchurStationaryTransfer.lean` proves exact
  block elimination, retaining an auxiliary source, and
  `saddle_constraint_without_inverse`: a shell constraint gives stationarity
  on its kernel, not the unrestricted field equation. Its zero shell block
  cannot be inverted. This is a relevant positive linear analogue.
* `02_REGISTRY/research/A4D_NATIVE_ACTION_INTERFACE_EXTENSIONS_2026_10_20.md`,
  section 10, already distinguishes the MDL sentence from the separate
  finite stationarity law. The present note adds the exact terminal-adjoint
  and compensated-variation conditions, rather than repeating its sampled-
  history first-jet counterexample.
* `.../causal_boundary_completion.md`, under
  `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20`,
  lines 40-130, supplies finite causal elimination and the actual fixed-
  oldRIGHT Gram preparation equation. It fixes independent boundaries;
  it does not assume an extra final-state constraint or prove that field
  parameters are physically selectable.

Thus Book03 §03.8 can be consumed as its separately stated stationary
equation, without an assumption of a field minimum. The missing object is
its binding to the complete actual execution, variables and price. No
inspected formal owner derives that binding from native programme optimality.

The fresh `book_source/NATIVE_CAR_ACTUATED_METRIC.md` supplies a real finite
live scalar/top rotation in the original addressed palette, conditional on
the live material-code/query binding. Thus an assertion that the expanded
native alphabet has NO field-changing action would now be wrong. Its section
8 explicitly does not supply the full field-and-price graph or a native
stationarity law. `COMPULSORY_QUERY_AND_COHERENT_MINIMUM.md` also separates
unavoidable source access from the full price. The present test respects
these new positive results and asks for the remaining terminal/price map.

There is also a concrete diagnostic for the newly owned actuator. The
original word `W^(2k)` has 18k primitive letters, holds the coframe and links
fixed, and changes only the selected scalar/top material pair. Its actual
reachable directions therefore do not cover the 42 field directions. Under
the owner's declared per-letter paid ledger, if Info refers to a fixed finite
classical target X given R, the already owned information-budget bound gives
`Cost-Info >= 18k-H_phi(X|R)`, before any other paid components. This consumes
the existing budget theorem and the actual word ledger; it does not declare
that every abstract written letter has unit physical cost without a price
contract. Dense recurrence of this real actuator alone consequently supplies
neither full field coverage nor a price-faithful smooth implementation limit.

## 2. Distinguish two legitimate composition routes

The execution-to-field distinction and price/tangent requirement are consumed
from the new prospective-field owner, not new no-go claims.

**Stack-to-field pullback.** If the actual selected stack state x_* really
satisfies `D S_stack(x_*)=0`, and an admitted differentiable map
`iota:(y,z)->x` binds the actual reduced execution price by

    d s = d(S_stack o iota),

then `d s=0` follows by the chain rule. Value equality is sufficient but
first-source equality is enough. No Hessian sign or field minimum is
required. There must be lifts of all the actual 16 coframe, 24 proper-link,
and two matter variations at each free site, with the real fixed collar.
No surjectivity ONTO the entire stack is required in this pullback direction.
The price equality must include Info, normalizer, source-query, preparation,
clock and terminal terms; one component of the stack is insufficient.

**Execution-to-field descent.** If only stationarity under admitted execution
variations is known, its projection must cover the desired field variations
and must not add an unpaid compensation source. This is the exact theorem
below. Surjectivity is required in this direction, not in the preceding
chain-rule statement. A discrete optimal word has no such tangent map until
a native implementation/variation chart is actually supplied.

## 3. Terminal constraints survive causal-state elimination

Fix the actual finite programme and clock. Let y be its independent field
coordinates and z all genuinely adjustable upstream apparatus/preparation
coordinates, in charts already respecting the true input Gram constraint.
Intermediate states satisfy the actual retained recursion

    X_0=i(y,z) M(z),       X_(j+1)=V_j(y,z) X_j.

The owned backward adjoint eliminates the X_j and gives the exact complete
price `s(y,z)`. Fixed initial task records and the spatial boundary collar
are held only because they are boundary data of this particular comparison.
They are not made free, nor may selectable preparation be relabelled fixed.

Suppose the actual goal additionally imposes smooth equalities
`c(y,z,X_N)=0`; after causal elimination write them as `cbar(y,z)=0`.
At a regular point, stationary feasible execution gives exactly

    s_y + C_y^* lambda = 0,
    s_z + C_z^* lambda = 0,          C_y=D_y cbar, C_z=D_z cbar.       (A)

**Proof.** Stationarity says ds annihilates the kernel of Dcbar. At a
regular constraint manifold every kernel vector is the velocity of a
two-sided feasible curve. Finite-dimensional linear algebra says its
annihilator is the range of Dcbar*, giving (A). This argument is first
order and requires no minimum or positive second form. Without regularity,
use the tangent space of actual feasible curves; a singular linearized
kernel can be larger than that tangent space.

Equivalently, run the owned backward recursion on `J+lambda.c`: the final
adjoint acquires the term `(D_XN c)^*lambda`, and the explicit field/
preparation source also acquires `lambda.D_(y,z)c`. These two contributions
combine into `C_y^*lambda,C_z^*lambda` above. They must not be omitted or
double-counted. The causal adjoint is unique GIVEN lambda; it does not set
the terminal multiplier to zero.

For the particular selected solution, the exact necessary and sufficient
extra condition for `s_y=0` in (A) is

    C_y^*lambda=0.                                                (B)

Strictly slack inequalities impose no local constraint. Active inequalities
instead generally give only one-sided conditions/normal-cone reactions.
An isolated boundary optimum does not imply zero ambient source.

## 4. A constructive sufficient lifting test, with all compensation paid

Let Y have dimension d=42 times the number of free site slots (with the
actual incidence sharing and fixed collar). Suppose stationarity holds for
all two-sided feasible variations. It is sufficient to supply a linear lift
`L:Y->Z` such that

    C_z L=-C_y,          s_z L=0,                                (C)

and every `(v,Lv)` is realized by an admitted feasible curve through the
same complete initial task. Then `(A)` evaluated on this lift gives

    0=ds(v,Lv)=s_y v+s_z Lv=s_y v,

for every field direction v, hence all d original field equations. The
second equality in (C) is essential: compensation of a terminal error by
changing a paid input may itself carry the entire missing source.

This is directly checkable by solving the finite matrix equation

    [ C_z ] L = [ -C_y ],
    [ s_z ]     [   0  ].                                       (D)

Its linear solvability is equivalent to equality of the ranks of the left
matrix and that matrix augmented by the d right-hand-side columns. Smooth
regular constraints then integrate the tangent vectors into feasible
curves; actual native admission is a separate required input. If native
controls parameterize only a smaller variation space, first compose these
matrices with the actual compiler Jacobian, rather than use unavailable z.

If the independent upstream equations are already solved, `s_z=0`, (C)
reduces to `im C_y subset im C_z`. A useful stronger sufficient condition
is that C_z is onto: then (A) and s_z=0 force lambda=0. If z is genuinely
fixed, no compensator exists; full field variation at fixed terminal data
requires C_y=0. Only a restricted field equation otherwise follows.

Without compensation sources and for an attainable field tangent subspace
R, the best conclusion is `s_y in R^annihilator`. Requiring this to imply
zero for EVERY possible field covector is equivalent to R=Y. If a particular
owned source class W is already established, the sharp weaker condition is
`W intersect R^annihilator={0}`. This explains precisely which rank is needed
and does not replace source computation by a rank count.

The existing scalar input-effect theorem can supply s_z=0 on the ACTUAL
fixed-oldRIGHT data-preparation tangent when all explicit preparation terms
vanish. It does not supply free control of the entire initial work state,
nor prove C_z is onto. For the whole-J2 reporter the scalar effects are
independent of logical preparation; such preparation generally cannot
compensate a terminal port-probability change at all.

There is an exact source-preservation control relevant to a proposed live
actuator. Suppose its actually admitted differentiable extension still has
`ds=kappa dt`, while the terminal equality is `cbar=q(t)-q(0)` with q'!=0.
For ANY tangent compensator satisfying `t_z L=-t_y`, one necessarily has

    s_z L=kappa t_z L=-kappa t_y=-s_y.

Thus terminal compensation is NOT price-neutral whenever the desired field
source is nonzero: it cancels precisely that source. This is a conditional
identity, not a claim that a continuous actuator has been admitted. Genuine
additional actuator/preparation prices must be differentiated too. They
cannot be excluded by retaining only the old scalar component source.

## 5. Exact terminal-calibration control on the original whole-J2 carrier

Consume the already checked slice in
`continuation_selection/STOPPED_FIELD_SADDLE.md` and its exact ridge:

    t(a,0)=0,        t_u(a,0)=g(1-a),        g>0,
    Dt=gamma_h DJ2 on this common-null curve.

Choose any nearby a_0!=1, u=0. Thus Dt and DJ2 are NONZERO there. Matter,
the full logical input M, oldRIGHT, compiler and paid prefix are fixed;
only the original coframe/shared-link field coordinates change. Their
mathematical query-input admission remains the inherited conditional one.

For a fixed original Golden programme k>=1, its EXACT complete port law is

    q_k(t)=[s(1-2t^2)+2c t(1-t^2)]^2+4c^2 t^4(1-t^2),
    s=sin(k theta), c=cos(k theta), q'_k(0)=4cs!=0.

Declare the calibration equality

    cbar(y)=q_k(t(y))-q_k(0)=0.                                 (E)

This is an explicit mathematical boundary control on an already existing
readout, NOT a derived native goal. It imposes one condition; all other
retained outputs remain present and are not discarded or constrained by
fiat. The local inverse theorem in the single real variable t implies that
(E), near t=0, is exactly t(y)=0.

Here full retained output can be checked, not just the pointer: the actual
cleanup is

    VJ=(1-2t^2)|0>J+2t(1-t^2)|1>J-2t^2|1>QWJ.

On t=0 this is EXACTLY |0>J for every logical input, including oldRIGHT.
After G^k all fresh work is clean, the logical input is unchanged, and all
complete stopped history/clock labels have the same geometric law. Their
actual charged ledger is the same at every point of (E). Therefore the
already-owned complete fixed-k pointer price F_k is EXACTLY constant on
this local constraint manifold: its work-entropy defect is identically zero
there, not merely first-order small. This is a genuine non-strict constrained
local minimum (and maximum) of the original full retained-record component.
It is not claimed globally optimal over a newly constrained class of other
programmes or a compulsory total Book price.

Nevertheless its unrestricted covector is

    D F_k=kappa_k Dt!=0,      D cbar=q'_k(0)Dt.

The exact terminal multiplier

    lambda=-kappa_k/q'_k(0)

makes `D F_k+lambda D cbar=0`. The constraint removes precisely the source
that would otherwise be consumed as the Einstein equation. Hence even a
true constrained local minimum of this native retained-price component
does NOT imply the unrestricted 42 Euler equations.

At this point the existing allowed logical preparation tangent cannot repair
the lost field variation: scalar port effects give `C_z=0` for all such
preparation directions, while `C_y=q'_k Dt!=0`. Equation (D) therefore has
left rank zero and augmented rank one. This is a concrete failed lifting
test on the actual retained input fibre, not a generic missing-rank remark.

For the already owned pointer choice T=5,ell=1,k=2,

    q_2=4p^3, q'_2=8p^(9/2), kappa_2=-p^(-3/2),
    lambda=1/(8p^6).

This uses the corrected existing factor; it is not `-2p^(-3/2)`.
No Info is inferred: the test consumes the already specified pointer/cq
price. Its purpose is to test terminal-to-field inference on the same
carrier, not to choose a new calibration task physically.

## 6. Concrete next composition, without another geometric campaign

For one genuinely supplied execution and terminal contract:

1. Give the actual map from each free 16+24+2 field coordinate into its
   admitted programme parameters. The geometric mathematical charts are:
   independent coframe entries; proper-link multiplication by each of the
   six Lorentz generators per link; the two original scalar/top amplitudes,
   with the retained normalization complement varied as specified.
2. Differentiate the full retained recursion and the real terminal contract.
   This produces C_y,C_z. State exactly which initial/collar records are
   fixed by the task and which preparation/clock/observer coordinates are
   independently selectable. Programme identity and clock are discrete
   choices, not continuous Euler directions within one fixed branch.
3. Use the actual full-price adjoint, including Info and terminal multiplier,
   to compute s_y,s_z; check (B), or construct the d lifts (C)-(D).
4. Only then consume the already owned all40 section 5.1 source identity.
   If the direct Book stationary-stack route is used instead, supply its
   map and exact full-source pullback from section 2; no minimum is needed.

This is a finite matrix/adjoint target on the existing programme. The current
causal owner already performs the internal-state part, while its source-
preserving terminal/variation binding remains genuinely unproved. An added
Lagrange multiplier is only a calculation of existing constraints and must
never be counted as a new physical action term.
