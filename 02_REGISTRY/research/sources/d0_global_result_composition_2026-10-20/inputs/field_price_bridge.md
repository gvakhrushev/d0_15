# What a native programme minimum can imply about the fields

20 October 2026. Bounded continuation of existing #334 at baseline `63221d4f`.
This note consumes the accepted all-cost stopped and adaptive results. It does
not change their task, information algebra, query, compiler or reference. It
does not assume that the physical field is an action available to a controller.

## 1. Exact result and its consequence for the parent route

There are two different minimizations. `ProspectiveExecution.optimal` compares
admitted **words in one fixed dynamics**, at one complete initial state and one
goal. A minimum over field configurations compares different points of a field
space. To transport the first through the proposed same-price identification,
one must establish a realization theorem relating both the attainable fields
**and the complete paid prices**. The theorem below is a sufficient, explicitly
checkable bridge; it does not claim that every possible proof must use it.

The realization theorem below is exact, including approximation by finite
native words. Its native countercontrol is unusually direct: the already
proved stopped programme minimum exists on every member of a compactly
perturbed, off-shell Brinkmann family on which its complete configured
apparatus record is identical, although the transverse full physical source
is nonzero. Thus
implementation optimality alone does not imply the Einstein source equations.
This remains true for every finite admitted constant prefix price `T>=5` and
Golden price `ell>=1`; no favourable compiler-cost choice is needed.

Sources and scopes are listed in section 8. The accompanying checker performs
only finite exact controls and pins those sources. The general statements in
sections 2, 3, 4 and 7 are proved analytically here, not inferred from a scan.

## 2. A necessary type distinction: background, input, or generated field

Write the fixed prospective machine as

\[
 D=(X,A,\operatorname{step},\operatorname{allowed},c),\qquad
 \mathcal F=\{w:\operatorname{executable}(s_0,w),\
                   G(\operatorname{run}(s_0,w))\}.
\]

The exact Lean structure supplies these five fields and quantifies its
`optimal` field only over `alternative : List D.Action`. It does not quantify
over `D`, `initial`, `goal`, or an independently supplied physical parameter.

Three interpretations must therefore be kept distinct.

1. **External field parameter.** If a query is `W_y`, its transition rule is
   part of `D_y`. Comparing programmes within `D_y` does not compare `D_y`
   with `D_{y'}`. A derivative of their optimized prices is a response of a
   family of machines, not a consequence of each machine's optimality.
2. **Read-only field in the complete state.** Reify that same family as one
   dynamics on `(y,x)`, with
   `step((y,x),a)=(y,step_y(x,a))`. Induction on a word gives

   \[
   \operatorname{field}(\operatorname{run}((y_0,x_0),w))=y_0.
   \tag{1}
   \]

   The same complete initial state fixes the field. Controls, inverse queries,
   copied port records, retained work and advancing clocks do not change (1)
   when their primitive rules preserve the field coordinate. The supplied
   coherent-query interface has this form: it gives access to a field-labelled
   matrix, and supplies no field-writing action.
3. **Generated field.** If admitted actions really construct or change the
   physical field, supply a reconstruction `Y(w)` from the complete resulting
   history, the same-initial/goal admissibility of the alternative words, and
   their full prices. This is a substantive implementation map. The free
   coframe/link arguments of a matrix formula do not supply it.

Equation (1) is not a claim that fundamental physical fields cannot evolve.
It identifies precisely the current read-only query model and what must be
added before applying a field variation to `ProspectiveExecution`.

## 3. The price-graph realization theorem

Let `w_*` minimize the full prospective price `C(w)` on `F`. Let `M` be the
finite-dimensional fixed-boundary field chart, `Y:F->M` a supplied field
reconstruction, and

\[
 y_*=Y(w_*),\quad C_*=C(w_*),\quad
 \Gamma=\{(Y(w),C(w)):w\in\mathcal F\}\subset M\times\mathbb R.
 \tag{2}
\]

**Theorem 1 (price-faithful field realization).** Let `S` be continuous near
`y_*`. Suppose that a single field-independent constant `c_0` satisfies
`C_*=S(y_*)+c_0`, and for every `y` in a neighbourhood `U` there are admitted
same-initial/same-goal words `w_n` with

\[
 Y(w_n)\to y,\qquad C(w_n)\to S(y)+c_0.
 \tag{3}
\]

Then `y_*` is a local minimum of `S`. Equivalently, it suffices that the local
graph `{(y,S(y)+c_0):y in U}` lie in the closure of `Gamma`. Even the one-sided
upper approximation `limsup C(w_n)<=S(y)+c_0` suffices.

**Proof.** Every feasible price obeys `C(w_n)>=C_*`. Taking limits, or a
limsup in the one-sided version, gives `S(y)+c_0>=C_*`. At `y_*` this is an
equality. This is exactly the local-minimum statement. No continuous choice of
programmes, attainment at other fields or differentiability of an infimum is
needed. **End proof.**

The argument uses only a feasible candidate set and its full price. It
therefore also applies to an admitted stopped-policy class with its expected
all-outcome price and a specified field reconstruction. That is the separate
class supplied by the adaptive owner; an unbounded stopping policy is not
silently a literal finite-word instance of the Lean structure.

Condition (3) involves the actual complete price. Approximating only `Y(w_n)`
does not suffice. Nor can one subtract a different preparation or compiler
clock `c_n` from each candidate and call the remaining numbers its full price.
For example, the dense rational field values `q` with paid price `1+q^2` have
a minimum at zero; replacing that price by the proposed field score `S(q)=q`
does not make zero stationary. The omitted ledger `1+q^2-q` is positive and
has derivative `-1` there. This elementary control is not the native witness;
the native witness is section 5.

**Corollary 1 (a concrete descent is a compiler obstruction).** If a supplied
field path `y_e->y_*` has `S(y_e)<S(y_*)`, then (3) cannot hold at any such
`y_e`. If an admitted exact realization of `y_e` does exist, its additional
ledger relative to `S+c_0` must obey

\[
 C(w)-[S(y_e)+c_0]\ \ge\ S(y_*)-S(y_e)>0.
 \tag{4}
\]

Consequently the parent's genuine off-shell descent, when consumed, rules out
an unrestricted price-faithful field-minimum substitution. It does not refute
the already proved optimum over readout programmes at a fixed field.

## 4. Exact chain rule and the admitted tangent

A convenient sufficient construction for (3) is an admitted realization chart.
Let `u` vary in an open neighbourhood of zero in `R^m`. Supply words `rho(u)`
in `F`, with `C(rho(0))=C_*` and `Y(rho(0))=y_*`. The word-valued map need not
be smooth; its field and price composites must be. Write

\[
 y(u)=Y(\rho(u)),\qquad C(\rho(u))=S(y(u))+R(u).
 \tag{5}
\]

At a prospective minimum the ordinary chain rule gives

\[
 (Dy(0))^*DS(y_*)+DR(0)=0.
 \tag{6}
\]

Suppose the accepted stopped first-source identity applies to this same
complete field score: `DS=kappa DJ2`, with `kappa!=0`. If `DR(0)=0`, (6)
implies precisely

\[
 DJ_2(y_*)\big|_{\operatorname{im}Dy(0)}=0.
 \tag{7}
\]

The full Euler equation follows if `Dy(0)` is onto the full admitted
fixed-boundary field tangent (or onto an already justified physical quotient
on whose removed directions the source is known to vanish). Without this
coverage only (7) follows. For one-sided admitted paths one obtains the
corresponding one-sided inequality; an equality requires two-sided paths or
their proved reversible span. No field oracle may choose `rho(u)` for free.

If `R` is constant and `y` is a submersion at zero, its local image contains a
neighbourhood and Theorem 1 gives an actual field minimum. In contrast,
`DR(0)=0` alone gives only first-order stationarity: the higher ledger can
stabilize an otherwise descending field score. These conclusions must not be
interchanged.

For a moving actual prefix or Golden price, even the branch formula is

\[
 DS_k=\frac{DT+k\,D\ell}{q_k}
       -\frac{B_k}{q_k^2}Dq_k-DE_k,
 \qquad B_k=T+k\ell+\log_\varphi\frac{1-q_k}{p}.
 \tag{8}
\]

Here the complete-pointer correction has `E_k=DE_k=0` on the common-null
stratum. The usual nonzero-source theorem fixes `T,ell` under variation. A
realization with changing preparation, scheduler, clock or information cut
must account for those terms; its vanishing cannot be inferred from (7).

There is a useful exact finiteness warning. For a countable native alphabet,
the set of finite words, hence the set `Y(F)` at one fixed deterministic
initial state, is countable. A continuous map from a connected open set into
that subset of `R^d` is constant: if any coordinate changed, the intermediate
value theorem would put an interval in its image. Thus a nonconstant exact
smooth realization chart does not arise merely from finite Golden words.
Approximate realization can still work, but it needs the price-graph limit
(3). With a finite alphabet and a uniform positive primitive clock cost, a
uniform primitive-cost bound permits only finitely many words. This last
statement concerns actual Cost, not an assumed lower bound on Cost minus Info.

## 5. A native same-family countercontrol: optimal readout, nonzero source

Consume the all-40 arbitrary-Brinkmann identities (6)--(12). Start from one
of their exact Einstein--CAR roots `H_*`, with matter profile `Psi(u)` fixed.
Choose a real site function `chi` supported strictly inside the transverse
collar and away from the designated fixed `u` collar, including the one-step
padding needed by the staggered connection. Put

\[
 H_s=H_*+s\chi,\qquad
 K_{a,s}(z)=\tfrac12[H_s(z+\hat u)-H_s(z+\hat u-\hat a)],
 \quad a=x,y.
 \tag{9}
\]

All matter records and their oldRIGHT purification are held fixed. Each
coframe remains nondegenerate with the same determinant, each link remains
proper, and the original Cartan rows vanish. The scalar values `f_i=q_i=0`
hold for **every** `s`; hence the complete query has `t=0` and the cleanup
output is exactly `|0>J` for every `s`, not merely to first order.

For the same fixed `T,ell`, every stopped port history, its full clean work
and the prescribed clock charges therefore have the same law on this whole
family. The active set of minimizing `k` and the adaptive optimum are the
same. The accepted all-cost theorem gives a nonempty finite active set and
`B_k>=2` for each of its members, for all `T>=5, ell>=1`.

Nevertheless the full coframe row changes by

\[
 DJ_2(H_s)[\partial_{v_v^+(z)}]
 =-\frac{C_h s}{2h}\Delta_h^\perp\chi(z+\hat u),
 \tag{10}
\]

where `C_h!=0` is the existing source normalization in the all-40 theorem,
not a new coupling. The matter part has no change. For a unit interior spike
at `(j_0,x_0,y_0)`, the transverse Laplacian at its centre is `-4/h^2`.
At `z=(j_0-1,x_0,y_0)` the row in (10) is consequently

\[
 2C_hs/h^3\ne0\quad(s\ne0).
 \tag{11}
\]

Every active fixed programme has

\[
 DS_k=-\frac{B_kq'_k}{q_k^2}\,dt
       =\kappa_k\gamma_h DJ_2,
 \qquad \kappa_k\ne0,
 \tag{12}
\]

and hence a nonzero full transverse source at these off-shell points, despite
being a minimizing implementation at each fixed point. In the particularly
transparent semantic-cost control `T=5,ell=1`, the accepted unique choice is
`k=2`, with `q_2=4p^3`, `B_2=2`, and

\[
 DS_2=-p^{-3/2}dt.
 \tag{13}
\]

The universal conclusion does not assume the actual compiler has price five;
(13) is only its exact small arithmetic control. At threshold ties no single
differential of the optimized envelope is asserted: (12) concerns each
active admitted branch, and the accepted adaptive theorem supplies the
directional envelope formula.

The perturbation can leave the initial `u` slice and transverse boundary
unchanged, with the connection's shifted support also interior. This is a
statement about the owned finite field chart, using periodic spectator `v`
or the corresponding admissible local boundary setup. It is not a proof that
the original D0 machine can generate those alternative future fields from
one full initial record. If that record already encodes the entire field,
case 2 applies and they are different initial states. If it contains only
initial physical data, a native generation map is still required. Ordinary
fixed-boundary conditions alone do not provide or exclude that map.

Restricting all admitted variations to the Brinkmann ansatz makes `J2` and
the entire stopped value constant and avoids this transverse descent. It
also removes the sole coframe Euler row which carries the Poisson/Einstein
equation. Thus that restriction does not derive the desired field equation.

## 6. What remains a valid positive use of the prospective optimum

The optimum over implementations remains useful and nonvacuous: after a
genuine future task and the complete information/payment interface have
been supplied, it selects the active programme(s) and gives their exact
physical response (12). All work, failed trials and clocks remain counted.
The response need not vanish because the controller does not optimize the
external field it is measuring.

For a genuine generated-field programme, equations (3) or (5)--(8) are a
precise positive reduction target. One can prove a restricted physical
stationarity law on the attainable tangent without pretending to have an
unrestricted field minimum. If the parent supplies a full-field descending
path, an unrestricted constant-ledger realization is excluded by (4);
the actual source must then contain the compensating ledger, or the native
admissible field class must exclude that path. Such a restriction cannot be
chosen after observing the desired Einstein equation.

If executed states have already been eliminated through their actual
recurrence `X_(n+1)=V_n(y)X_n` at a fixed `X_0`, use that reduced **complete**
price in (5). Its total derivative includes the response of the executed
states; an adjoint representation merely computes that same derivative.
This elimination preserves values. It neither adds new reachable fields nor
turns an externally parameterized `D_y` into a control action. The admitted
control or field tangent in (6), and the full remaining ledger, still have
to be supplied. No additional optimal-control law is postulated here.

## 7. Why replacing the missing task by exact future verification fails

The existing future-profile theorem is an availability statement: distinct
future profiles admit a separating finite word and test. Retaining the full
profile can already be achieved by the identity encoding, so it does not
force the execution of that word. This implication was established in the
consumed native-task search; it is not reproved here.

There is a stronger obstruction to interpreting it as an obligation to
produce a finite, error-free certificate of a continuous field equation.

**Theorem 2 (no finite exact certificate at a continuous boundary).** Keep
one initial apparatus/logical/oldRIGHT state and a policy fixed independently
of the unknown field. Suppose every finite-clock native experiment is a
continuous quantum instrument in `y`, with a finite registered alphabet at
each primitive step. Let `P` be a predicate whose false points accumulate
at `y_0`, where `P(y_0)` is true. No zero-error policy can announce `P=true`
with positive probability in finite time at `y_0`.

**Proof.** If its finite-time announcement probability is positive, the
event of announcing it by some finite clock `N` has positive probability
at `y_0`: finite stopping is a countable union of bounded-clock events.
The bounded-clock probability is continuous, because it is a finite sum of
Born probabilities of fixed, finite, retained-history circuits. It therefore
remains positive in some neighbourhood of `y_0`, which contains a false
point. That is a false positive, contradicting zero error. **End proof.**

The argument also allows a general final two-verdict measurement: its fixed
POVM effect has a continuous expectation. It does not assume that the port
bit is the only information available. A finite expected native tick count
implies almost-sure finite stopping, so cannot evade the result.

For the actual cleanup, `r(t)=4t^4(1-t^2)` gives a concrete one-sided control.
A detected nonclean outcome certifies `t!=0` for `|t|<1`, but never occurs at
`t=0`. Repeating until such an event has mean attempts `1/r(t)` for nonzero
`t`, diverging like `t^-4`, and does not complete at the primary stratum.
The Golden rotated port at `t=0` instead has both outcomes with nonzero
probability for `k>=1`; relabelling either as a certificate of `t=0` is
unsound. Checking `DJ2=0` is at least subject to the same boundary theorem
when noncritical fields accumulate and the finite query family is continuous.

This theorem does not exclude discrete promised tasks, finite-error tests,
or indefinitely retained experiments. It says that none is supplied merely
by an abstract injective future profile or deterministic `VerificationContract`.
That contract's exact `record` and `compare` functions are not a proof that
unknown nearby Born laws can be exactly decoded in a finite paid execution.
If an orthogonal classical field description is already in the initial
record, the fixed-initial/continuous-input hypothesis changes and must be
stated explicitly. No external success label or error threshold has been
introduced in this note.

## 8. Consumed sources and reproducible scope

At the stated baseline the consumed original paths are:

- `03_FORMALIZATION/D0/Foundation/ProspectiveExecution.lean`: fixed dynamics,
  full-state words, `optimal`, and the already-owned empty-task theorem.
- `03_FORMALIZATION/D0/Foundation/FutureExecution.lean` and
  `FutureExecutionCompleteness.lean`: future profiles and separating tests.
- `03_FORMALIZATION/D0/Foundation/VerifiabilityNecessity.lean`: the exact
  deterministic verification contract and its application boundary.
- `02_REGISTRY/gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md`,
  equations (6)--(12): the actual complete geometric and matter source.
- `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md`,
  equations (8)--(14): complete cleanup and Golden port response.
- The adjacent `source_selection/history/NATIVE_TASK_SEARCH_4867.md` and
  `source_selection/records/ADAPTIVE_ALL_COST_EXTENSION.md`: existing task
  boundary and the all-cost adaptive envelope. No Bellman or geometry proof
  is rerun here.
- `02_REGISTRY/research/A4D_GOLDEN_FULL_SOURCE_SELECTION_SYNTHESIS_2026_10_20.md`:
  current integration and exact scope of these consumed results.

`check_prospective_field_bridge.py` pins the exact bytes of these nine inputs
and checks the compact-support staggered stencil, unchanged collars, a
nonzero full coframe row, the exact Golden coefficient (including its factor
of two), the read-only field invariant, the missing-ledger negative control,
and bounded cleanup certificate controls. All checks remain active under
Python `-O`. It does not claim a proof of native field-generation admission,
run geometry again, or replace the analytical quantifiers by finite examples.
