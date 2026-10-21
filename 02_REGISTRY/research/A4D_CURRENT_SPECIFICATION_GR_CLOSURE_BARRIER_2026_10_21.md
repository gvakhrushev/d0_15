> **Scope correction — 21 October 2026.** The title below should be read as a
> barrier for deriving GR from the *current explicit Cost-Info/history
> interfaces alone*. Book03 §03.25 already supplies a unique master bootstrap
> action `B_N = beta^-1 log Tr exp(-beta Delta_N(V)) - log det(I-zF_N(V))`.
> Hence the current specification is not missing an aggregation scalar at the
> action layer. What is still absent is the native same-execution
> identification/pullback of the bootstrap Hodge Laplacian `Delta_N(V)` and
> feedback `F_N(V)` to the actual moving GR carrier, including all field,
> observer, preparation, clock and refinement jets. Existing
> `A4D_NATIVE_SOLDERED_HEAT_SOURCE.md` explicitly records
> `bootstrap_heat_identification = OPEN`. Sections below remain valid as
> no-shortcuts showing that mean Cost-Info, normalized coherent amplitudes,
> endpoint allocation, or D_min cannot substitute for that pullback.

# Current-specification GR closure barrier

21 October 2026. Existing Draft PR #334 only.
Phase: native realization / final composition.

This theorem composes four already-owned exact boundaries:

1. the literal Book03 `Cost-Info` path formula;
2. the exact endpoint-allocation family from
   `gr_assembly/sources/d0_cost_info_boundary_2026-10-19/theorem.md`;
3. the formal `ActionProtocol` excess-profile classification and full depth-two
   response in `A4D_NATIVE_BOOK03_OPERATOR_VARIATION_BOUNDARY.md`;
4. the new native Golden first-source separation in
   `A4D_BOOK03_FIRST_SOURCE_UNDERDETERMINATION_THEOREM_2026_10_21.md`.

It proves a statement about **logical derivability from the currently explicit
G0/Book03 interface**. It does not forbid a future native completion, and it
does not weaken any positive finite GR construction.

`GR_closed=false`.

## 1. The current formal interface does not define one native action

The exact formal `ActionProtocol` fiber is already classified. For every
off-diagonal ordered pair, its nonnegative excess is independent; the type
imposes no path-composition, symmetry, refinement or field-source law.
`book03PathWeight` takes total `info` as a supplied real argument. The
formal owner explicitly records that `ActionProtocol` does not identify its
transition action with physical Book03 `Cost`, does not contain native
`Info(v)`, memory assignment or refinement, and therefore has no native field
source to differentiate.

Independently, Book03 writes

[
  S(gamma)=sum_{eingamma}C(e)-sum_{vingamma}I(v).
]

The exact boundary theorem shows that the literal all-vertices reading is
incompatible with nonzero `Info` if singleton histories are action identities
and path action is additive. The full additive repair is a one-parameter
family

[
  w_	heta(u,v)
  =C(u,v)-	heta I(u)-(1-	heta)I(v).
	ag{1}
]

For an open history from (v_0) to (v_n),

[
  oxed{
  S_	heta(gamma)-S_eta(gamma)
   =(	heta-eta)[I(v_n)-I(v_0)] .
  }	ag{2}
]

The current Book03 text does not select (	heta). Closed paths do not see
this freedom, but finite retained tapes are open histories. Whenever the
endpoint-information difference has a physical first jet,

[
  D S_	heta-D S_eta
  =(	heta-eta)D[I(v_n)-I(v_0)]
	ag{3}
]

is a genuine first-source ambiguity even with the same edge costs and the
same interior information values.

## 2. Even granting the strongest amplitude binding leaves a second,
independent first-source ambiguity

Now grant more than the formal G0 layer currently proves. Assume the normalized
Book vector on the complete orthogonal native history basis equals the actual
native coherent record. Then the existing amplitude-binding theorem forces

[
  I_omega=C_omega+rac12log_arphi q_omega+J,qquad
  S_omega=-rac12log_arphi q_omega-J.
	ag{4}
]

Thus relative branch gains and phases are fixed; only the common real mode
(J) remains.

For exactly the same complete history data define

[
  M=sum_omega q_omega S_omega
   =rac12H_arphi(q)-J,
qquad
  P=-log_arphi|Q_B|=-J.
	ag{5}
]

Both are scalar functions of the same amplitude-bound Book family. Their
first sources satisfy

[
  oxed{DM-DP=rac12,DH_arphi(q).}	ag{6}
]

The common mode cancels. Therefore an absolute anchor for (J) cannot make
these two variational readings equivalent on a chart with moving record
entropy.

On the literal original full128 Golden nonblank pair

[
  (q_0,q_1)=(p^2,p),quad (C_0,C_1)=(1,2),quad p=arphi^{-1},
]

use (Dq=(-1,+1)). Exactly,

[
  DH_arphi=log_arphi(q_0/q_1)=-1,
]

so

[
  oxed{DM-DP=-rac12.}	ag{7}
]

This remains true for every (DJ).

## 3. Matching the configured CQ price does not remove the ambiguity

Let the already-owned complete CQ scalar be

[
  S_{m CQ}=ar C-H_arphi.
	ag{8}
]

If one requires the **mean** amplitude-bound Book path price in (5) to equal
this CQ value, then necessarily

[
  J=rac32H_arphi-ar C.
	ag{9}
]

The amplitude pressure of the SAME Book vector is then

[
  P=S_{m CQ}-rac12H_arphi,
]

hence

[
  oxed{DP-DS_{m CQ}=-rac12 DH_arphi.}	ag{10}
]

On the Golden tangent this is (+1/2).

Conversely, if the amplitude pressure is required to equal (S_{m CQ}),
then

[
  J=H_arphi-ar C,
]

and

[
  M=S_{m CQ}+rac12H_arphi,qquad
  oxed{DM-DS_{m CQ}=rac12DH_arphi,}	ag{11}
]

which is (-1/2) on the same native tangent.

Therefore no choice of the common amplitude anchor makes both already present
scalar readings equal the configured CQ action, even in value and first source,
unless (DH_arphi=0). The original Golden pair supplies an exact nonzero
counterexample.

This is stronger than saying that Shannon has not been proved to be Book
Info. It says that after a complete amplitude binding and after one scalar
value-identification are supplied, a separate **aggregation theorem** is
still logically necessary.

## 4. Model-theoretic closure consequence

Consider the currently explicit G0/Book03 specification as the common theory.
A completion may add an interpretation of the missing physical variational
scalar while preserving every currently proved equation.

Completion A selects the complete mean path price (M).
Completion B selects the absolute amplitude pressure (P).

They may share:

- the same scene and path carrier;
- the same actual native Kraus histories and Born probabilities;
- the same actual primitive charges;
- the same normalized complete coherent Book vector, including phases;
- the same common amplitude anchor (J);
- the same one-step Golden marginal and all already measured native
  probabilities.

Yet by (7) they give different first Euler covectors.

Hence the currently explicit G0/Book03 specification has at least two
consistent completions with different native first sources. A unique Einstein
source, or any other unique nonzero field source, is therefore **not entailed**
by that specification alone.

This is a logical non-entailment statement, not a statement that no stronger
unwritten intended rule exists. To make a physical GR theorem, that intended
rule must be added/proved explicitly.

## 5. The missing theorem is now minimal and irreducible

No further geometry census can repair this barrier. The remaining G0 theorem
must simultaneously fix:

1. **History composition / endpoint allocation** — select the actual additive
   placement of branch information, removing the (	heta) coboundary (2).
2. **Native Info** — derive (I(v)) or (I_gamma) from the same admitted
   `Sigma`/history/readout object, with its first jet.
3. **Memory normalization and refinement** — identify the represented
   memory operator/vector on the actual retained tape and the native
   multi-tick composition.
4. **Aggregation** — identify the one scalar functional whose stationarity is
   the physical finite Euler equation and prove its relation to the Book03
   action stack.

The existing `D_min/F_0` definition does not supply item 2: the current
`BOOK_SOURCE_BINDING` owner records explicitly that state code length is not
identified with the Book03 vertex gain on the native full128 tape.

Once items 1--4 are supplied, the existing finite machinery can compute the
full source and test the original 16+24+2 equations. Before that point,
declaring the complete CQ price, a raw amplitude norm, normalized feedback, a
mean `Cost-Info`, or a prospective minimum to be “the Book action” is an
additional constitutive choice.

## 6. Research disposition

This theorem changes the programme priority.

- Do **not** spend the next cycle on another metric solution, rank scan,
  continuum example, or source reconstruction.
- Do **not** try to tune the common scalar (J); equation (7) is independent
  of it.
- Do **not** infer the missing rule from the one-step Golden probabilities;
  the existing two-tick counterexample already proves that those marginals do
  not determine the native history law.
- Do derive one explicit same-execution Book03 history/action object from the
  common initial D0 state that fixes items 1--4. If this cannot be derived
  from existing core axioms, the theory itself requires an explicit new
  definition/theorem before D0->GR can be closed.

The accompanying checker
`check_current_spec_closure_barrier.py` verifies the exact Golden
first-source gaps, both CQ matching corollaries, and the endpoint-allocation
source difference.

Positive results remain intact: exact all40 Cartan families, the configured
all42 CQ source, rank-two double-zero finite sheets, paid writers, direct
signed-curvature readouts, full128 preparation/input closure and conditional
GR recovery all remain valid within their declared interfaces.

`GR_closed=false`.
