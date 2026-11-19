# Forced next record is not a forced field query

20 October 2026. Read-only continuation, baseline
`972ce692a84b5b23bdf91e93a047b1882ad582d4`, existing parent PR #334.
This extends `source_selection/history/NATIVE_TASK_SEARCH_4867.md`; it
does not repeat its branch-price search or introduce a new physical goal.

## 1. The exact substitution still absent

The actual Lean conclusion of `StaticToDynamicsOwner.lean:43–49` is

    J Y != Y J
    and forall n, archiveCirculations(neumannTerm n)=n
    and forall n, ladderAmount(n+1)=ladderAmount(n)/phi.

It contains neither an executed history nor a terminal predicate. The
Feshbach owner explicitly retains the zero-circulation term (`:101–102`).
The conclusion concerns order sensitivity, path grammar and a weight,
not an obligation to execute a specified distinguishing experiment now.
Book03:236 points to this finite chain; Book06:245 requires preservation
of the invariant needed for the next registration, without defining a
test to be answered by that next registration.

The future-completeness conclusion is instead

    s != t -> exists finite w, test q,
      observe(run(w,s),q) != observe(run(w,t),q).

These statements compose as preservation/accessibility of distinctions.
They do not change the quantifiers into: the actually chosen next history
must execute one specified w or strictly reduce one specified ambiguity.
`ProspectiveExecution.goal` and `.optimal` remain separate supplied data.

Three indices must not be identified without a theorem: Neumann archive
order n, actual paid primitive clock L, and additional reporter rotation
count k in G^k. In `book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md`, k=0
still executes the common full query/cleanup prefix, all actual reads and
records, and the paid forward clock. It is not the empty history. Even
an additional premise L>=1 would not imply k>=1, let alone k=2.

## 2. A retention-preserving countermodel to the proposed composition

This is a countermodel to the abstract inference from future completeness,
ordered noncommuting operations and a mandatory new record. It is not an
assertion that these particular operations instantiate physical G0, nor a
countermodel to every unexamined D0 axiom. The purpose is to identify the
additional premise a native application has to supply.

Let a state be (x,b,H), with x,b in {0,1} and H a finite intrinsic history.
The available readout is (b,H). Each event stores its operation label and
new visible bit in H. Define three deterministic operations:

    T: (x,b,H) -> (x,b,H ++ [(T,b)]),
    Q: (x,b,H) -> (x,b xor x,H ++ [(Q,b xor x)]),
    X: (x,b,H) -> (1-x,b,H ++ [(X,b)]).

All states and records at every finite depth are finite. The clock is |H|,
read off the actual intrinsic history; no external clock or outside
catalogue is used. Every operation adds a new distinguishable record.
Every operation is injective: remove its last record and invert its
reversible two-bit payload operation. Thus every old distinction is
preserved, including x. No trace, reset, discarded failure or erased
ordering is hidden in T.

The complete future profile is injective. If b or H differ, the empty-word
readout separates the states. If only x differs, the single existing word
Q separates them. Hence this is already the minimal future-equivalence
state, not a padding register that the owned future quotient removes.
Any memory sufficient for all these future readouts must retain x.

The payload operations are genuinely noncommutative: starting from
(x,b)=(0,0), chronological Q;X gives (1,0), whereas X;Q gives (1,1).
The history also retains this order. This is stronger than merely adding
a clock to an otherwise commuting action alphabet.

Nevertheless, from the two initial states (0,0,empty) and (1,0,empty),
every positive number of T steps produces identical actually observed
histories. The pair stays distinguishable by a later Q. Thus:

    mandatory fresh records + exact retention + future completeness
    + order-sensitive internal operations
    do not imply progress in answering the hidden-bit question.

This remains true if the comparison domain requires precisely one next
record: T is an admissible nonempty history. Under positive declared
prices it can also be the unique prospective minimum: give T,Q,X the
literal lengths 1,3,4 of Golden prefix words 0,100,1010. Their Golden
weights sum to p+p^3+p^4=1, p=phi^-1. For a fixed complete input and
deterministic executions every complete terminal record is deterministic,
so its Shannon entropy is zero; the shortest nonempty history is T.
This pricing example is an explicitly declared abstract compiler, not a
derivation of native G0 prices or a proposed physical replacement.

The model does not claim that the concrete D0 J,Y matrices act as Q,X.
The actual static owner's finite conjunction has no variable linking
its J,Y to a compulsory terminal query; adding that independent true
conjunction cannot manufacture the missing linkage.

## 3. What future completeness does construct positively

For a finite candidate carrier S with injective future profile, choose a
separating (w,q) for each unordered pair. There are at most |S|(|S|-1)/2
pairs. The finite vector

    E(s) = (observe(run(w_i,s),q_i))_i

is injective. This is a finite separating description of the already
declared future profile. With enumerable operations/tests, decidable
execution/readout and the fixed native code order, the first separating
pair can be found by finite search for any explicitly given s!=t; the
search halts by future completeness. Choosing the first such witness
introduces no independent choice catalogue.

There is an operational restriction: E evaluates each word from the same
initial state. It is not automatically one sequential physical protocol.
Copies, restoration or suitable non-destructive tests must be admitted
and paid before one runs that finite battery. Generic future completeness
alone is insufficient: take initial states u0,u1,u2 and absorbing z0,z1;
observe blank on each ui and bit j on zj. Query a_i maps ui to z1 and all
other initial states to z0, while fixing z0,z1. All five future profiles
are different, but any first query merges two possible inputs forever.
No deterministic single-copy strategy identifies all three initial states.
This second control is only for the generic FutureExecution interface;
it is not retention preserving and must not replace the stronger model
in section 2.

For an actual pending verification request in the complete initial state,
however, one obtains a useful conditional operational goal. Suppose its
declared contract demands different terminal answers on an unresolved
pair s,t, the current observable transcripts coincide, and the supplied
test family is future complete. Then a constant/no-query transcript cannot
complete that request. The canonical finite witness provides a possible
experiment; its actual implementation and complete price are charged.
This is ordinary correctness of an already present verification request,
not a new physical axiom that every possible test must be performed now.

## 4. Exact parent boundary and next usable target

To exclude the parent's k=0 alternative one must supply a native pending
request/closure condition whose REQUIRED terminal answer is not already
provided by the common query prefix and its complete retained output.
The request must be part of the same initial apparatus/task for every
competitor. Its correctness must fail for k=0, while a specified admitted
continuation satisfies it; all its work, information and clocks then enter
the same price. Merely naming k=2 as the goal, selecting port 1 as success,
or requiring a nonzero source would insert the desired answer.

None of the inspected owners provides that substitution. A compulsory
new record is compatible with the countermodel and, in the actual parent,
with the common paid prefix already present at k=0. The constructive
output is therefore a precise conditional route: derive an unresolved
request from the actual next-record contract first, then use existing
future-complete readout and the canonical witness compiler to solve it.
There is no need for another scalar source encoder at this step.

The narrow checker verifies the exact finite models, reversibility,
future separation, noncommutativity, transcript equality, the Golden
prefix identity and the destructive-battery control. It writes stdout
only and makes no repository changes. The universal statements above
are established by the displayed algebra, not by extrapolating its finite
enumeration.
