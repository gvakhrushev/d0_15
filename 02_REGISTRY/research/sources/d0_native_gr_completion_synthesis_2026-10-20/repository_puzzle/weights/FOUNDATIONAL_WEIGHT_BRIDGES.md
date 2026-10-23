# Three concrete reuses of the old foundations for Book weight binding

20 October 2026. Existing PR #334; repository read-only at
`2c592f9b9437cd302fcd39352b85212341bff968`.

This note consumes, rather than repeats, the latest global composition.
Its specific refinement is to replace the informal requirement of matching
Born and Book weights by one finite response defect and a weighted
continuation transport test. No new detector, Info, task or sampling rule is
installed. All probability and logarithm formulae below use positive support;
the underlying linear effect sums retain zero-probability records as well.

## 1. Born + the finite Book future law: one exact response-defect test

The old Born owners prove normalization of an ALREADY supplied response:

    R_e=Tr(rho F_e),       F_e=A_e* A_e,
    q_e=R_e/sum_f R_f.

The strongest relevant assumption is visible in
`D0/Core/BornFinite.lean:118-121`: `response_rule` recovers this very raw
response. `BornFiniteEffects.lean` transports it through finite effects and
coarse sums. `BornQuadraticResponse.lean:25-117` derives norm-square inside
the quadratic, phase-blind, unit-calibrated family. These Lean statements
are rational finite-frame owners; their real matrix application requires the
already supplied actual matrix/effect interpretation, not identification of
two quantities with the same name.

At the SAME complete prefix and finite task let the existing Book future
law give the unnormalized completed-edge mass

    B_e=K_e Z_(N-1)(s_e),       K_e=phi^(-s_e^Book).

Here s_e denotes the complete next state in Z and s_e^Book denotes its edge
net price; both preparation/work and terminal chi are the actual ones.
Define the scalar response defect

    Gamma_e=R_e/B_e>0.

Then exactly

    log_phi(q_-/q_+)
      = -(s_-^Book-s_+^Book)
        +log_phi(Z_-/Z_+)+log_phi(Gamma_-/Gamma_+).        (1)

Thus the desired K_-/K_+=q_-/q_+ holds iff

    Z_- Gamma_-=Z_+ Gamma_+.                             (2)

Equal suffix partitions AND equal response defects are a useful sufficient
factorization of (2); neither is necessary separately. The full source
test is the differential of (1), including moving rho, effects, code,
terminal law and both defect terms. Equality only at one field value does
not supply that differential.

This is a sharper application than the equal-continuation statement in
the global synthesis: its remaining Born-to-Book premise is now an explicit
same-instrument scalar/effect equality, not an entropy identification.
For a fixed prepared family it asks only for the actual trace equality.
If the B_e are preparation-independent and equality of these normalized
laws is claimed for ALL normalized input states, the exact operator test is

    F_e=B_e H for one common positive operator H,
    H=(sum_f F_f)/(sum_f B_f).

Indeed equality of all normalized expectations gives
`Tr rho[F_e-(B_e/sum B)sum_f F_f]=0` for every rho, which gives the stated
operator identity. For a COMPLETE instrument on this input fibre,
sum_f F_f=I, it specializes to F_e=(B_e/sum_f B_f)I. More generally use
the corresponding compression to the actually allowed fibre and its
actual total-response calibration. Positivity alone is insufficient.
A common scalar calibration may depend on fields and affect an absolute
weight identification even though it cancels from the odds.

### The memory algebra makes Gamma substantive, not merely a notation

For a proposed Book amplitude interpretation, write each full event output

    v_e=sum_(gamma in H_e) w_gamma u_gamma,
    R_e=||v_e||²
       =sum_(gamma,delta in H_e) w_gamma w_delta
            <u_delta,u_gamma>.

These u_gamma include the actual ordered memory, preparation and retained
work. With density matrices the same identity uses the Hilbert-Schmidt
vectors A_gamma sqrt(rho). In contrast, the scalar completion partition is
sum_gamma w_gamma. Hence the Gram matrix of the ORIGINAL retained histories
is exactly what must turn the quadratic response into the scalar Book sum.
It cannot be removed by Born uniqueness. For two orthogonally tagged single
histories of unit norm, q_-/q_+=(w_-/w_+)², not w_-/w_+. This is a finite
countercontrol using the owned type split, not a competing probability law.

The type split also gives an immediately usable positive alternative:
if a genuine complete instrument supplies amplitudes sqrt(w_gamma), with
orthogonal retained labels, then R_e=sum_gamma w_gamma and Gamma_e=1.
This is only a sufficient implementation condition, NOT a permission to
replace the Book03 amplitude coefficients by square roots. Existing exact
Kraus-history owners can be checked against it; no tomography is needed.

## 2. TheoryTransfer can prove equal suffix sums, once its missing weight
##    diagram is supplied

The older `TheoryTransfer.Interpretation` already proves every finite-word
and readout diagram from primitive diagrams. It has no price field. Its
`NativeContextCoverage` likewise concerns observations, not multiplicities
or weighted sums of native implementations. The exact extension needed for
the current comparison is small and finite.

Let L_-,L_+ be the full positive weighted continuation operators at matched
clock cuts, including every complete compiler transcript, failure and
terminal record. Let R pull back functions by an invertible relabelling of
the two complete state spaces. Assume ACTUAL primitive weighted diagrams

    L_- R=R L_+,       chi_-=R chi_+.

Then induction gives

    L_-^n chi_-=R L_+^n chi_+                            (3)

for every finite n. At matched initial states this proves Z_-=Z_+, with all
records retained. If the diagrams hold smoothly on the admitted field chart,
all their first sources agree by differentiation, including the derivative
of a moving R. No equality of minimum suffix prices is used.

For a variable-length compiler, the same condition is imposed on its actual
clock-expanded finite acyclic transfer; the existing source-preserving
Schur/clock reduction may then be applied. Its direct term and both boundary
vectors remain. Dropping them because the internal determinant is one would
invalidate (3).

If native implementations form many-element fibres over one source word,
the exact requirement is fibrewise sum of complete native weights = source
weight (up to a single stated common factor), not equality of one chosen
compiler word's price. This is precisely where extra retained compiler
records enter. Their sum can be computed from the already owned original
marked transfer rather than a new apparatus.

There is also a direct quantum version on the actual Kraus carrier. Let

    L_e*(H)=sum_b phi^(-C_(e,b)) A_(e,b)* H A_(e,b),
    H_0=T_terminal,       H_n=sum_e L_e*(H_(n-1)).

Then Z_n(rho)=Tr(rho H_n), with all fine b labels retained in the physical
instrument. A unitary/invertible actual representation transport that
intertwines these weighted adjoint maps and the terminal effect proves
equality of Z for the transported prepared inputs. Positivity and unweighted
channel equivalence alone do not imply the weighted intertwining.

The actual old same-history owner already provides this nontrivial operand:

    Z_n(t)=Tr Phi_t^n(rho),
    Phi_t(X)=x[X+epsilon((p²+p x)T(DXD)-{Delta,X}/2)],
    x=exp(-t).

At t=ln(phi), its first-round Z_1=p-p³r and dZ_1=-p³dr,
where r is the actual total return-port probability. This rules out replacing
the weighted operator by a scalar times the unweighted channel. Reuse its
actual recursion, not only its output probabilities, for the diagram (3).

### Why ordinary future equivalence is not enough for the Julia endings

VerificationCore identifies complete records exactly when every admitted
future profile agrees. The +/- report itself remains an admitted retained
readout. The two endings therefore need not be equal in that quotient, and
deleting the report in order to force equality is invalid. A paid symmetry
or invertible relabelling can relate DISTINCT retained records while proving
the weighted continuation diagram; it need not quotient them together.

This is the useful non-obvious reuse: seek an actual price-preserving arm
symmetry/intertwiner, not an assertion that the measured endings are the
same state. A common terminal identity gives H_0=I and Z_0=1 immediately,
but does not establish that stopping there is the compulsory task.

## 3. Old PF/current and branch-cocycle owners isolate exactly what remains

For the owned scalar positive Book matrix K, the Perron law is

    P_uv=K_uv h_v/(lambda h_u).

For a complete n-edge path gamma from u to v,

    P(gamma|u)=lambda^(-n) h_v/h_u product_e K_e.          (4)

This is the existing finite coboundary, not a new stochastic law. Its useful
application is that two SAME-CLOCK paths with the SAME active endpoints
have exactly their Book weight ratio, without a long-time limit. On a
closed path the h factors cancel; for unequal clocks the power of lambda
does not. On an archive-dependent full process the scalar h(vertex) may be
insufficient: the existing ordered-history firewall prevents silently
declaring different Q8/noncommuting histories equivalent. Formula (4) is
consumed only for the owned scalar ensemble, or after a proved weighted
full-history map of section 2.

Combining (4) with the old branch cocycle gives a diagnostic convention
identity. If K_uv=phi^(-C_uv+I_uv), and the reference is explicitly
mu_ref,uv=phi^(-C_uv), using the SAME charged C, then

    I_cocycle(uv)=log_phi(P_uv/mu_ref,uv)
      =I_uv+log_phi h_v-log_phi h_u-log_phi lambda.       (5)

Consequently the difference between the edge Info and the observed path
likelihood Info is NOT an adjustable entropy: it is the original endpoint
and clock pressure. It cancels on equal-endpoint/equal-clock ratios and
persists in the absolute source. With the original stationary flow pi P,

    E[I_cocycle-I]=-log_phi lambda,
    E[C-I_cocycle]=E[C-I]+log_phi lambda
                 =H_phi(P | pi).                       (6)

This explains exactly why both a positive conditional-current KL minimum
and the scalar Perron pressure can be correct for the same supplied process
without selecting the physical Book Info or the required current. The old
current contraction conditions on an externally specified feasible j; its
required-task premise is still a separate native assertion.

The absolute branch binding is already owned as

    w=N q  =>  Info=log_phi(q/mu)+log_phi N,
    dInfo=dlog_phi(q/mu)+dlog_phi N.                      (7)

Thus successful odds/intertwining tests fix a relative price. They cannot
drop dlog N or replace the full priced quantum memory by the scalar (6).

## Exact remaining premise and immediate use

The old foundations do not lack an existence theorem for available tests:
`FutureExecutionCompleteness.future_complete_forces_a_test` already gives
one finite admitted witness whenever a pair is required to be faithfully
distinct. VerificationCore supplies its record/comparison and TheoryTransfer
its finite implementation. None of those structure fields designates WHICH
comparison/current must be completed now or supplies its Book price.
Prospective Bellman/no-detour operates after that initial state, goal, price
and optimality contract is given; its goal field is not reconstructed from
the future-profile kernel.

The smallest next input is therefore one already requested native comparison
contract on the SAME complete initial archive, with its actual terminal
effect/chi and full price weight. On that input, reuse existing operators to:

1. Compute R_± and completed B_±, and test the explicit defect (1)-(2).
2. Prove equal suffix weights via the actual weighted primitive diagram (3),
   rather than by equal minimum prices or by erasing the recorded sign.
3. Retain the pressure/normalizer derivative (5)-(7) in the complete source.

These are finite exact interface checks, not a new geometry campaign. They
leave the native compulsory-task/Info admission explicit, while reducing it
to concrete existing operands rather than asking for a new physical law.

## Source map at the pinned head

* `03_FORMALIZATION/D0/Core/BornFinite.lean`, lines 118-159;
  `BornFiniteEffects.lean`, response/effect/coarse-readout declarations;
  `BornQuadraticResponse.lean`, lines 25-117 and 119-181;
  `BornQuadraticOrigin.lean`, lines 25-68.
* `03_FORMALIZATION/D0/Foundation/TheoryTransfer.lean`, lines 34-81,
  379-417; `VerificationCore.lean`, lines 131-182, 230-240;
  `FutureExecutionCompleteness.lean`, lines 28-44.
* `03_FORMALIZATION/D0/Foundation/ProspectiveExecution.lean`, lines
  147-156, 170-226: explicit goal/optimality and their suffix consequence.
* `02_REGISTRY/research/A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md`,
  sections The missing scalar, Refinement and joint variation, Exact boundary;
  `A4D_NATIVE_PARTITION_CORRECTED_BRANCH_INFORMATION.md`, equations 1-4.
* `02_REGISTRY/research/A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md`,
  section 2: the finite completion law; not claimed anew here.
* `02_REGISTRY/research/A4D_ORIGINAL_BOOK_ALL_PATHS_FLOW_PRESSURE_ACTION_AND_EXACT_HISTORY_SCHUR_2026_10_19.md`,
  section 2: original PF kernel and exact coboundary cancellation;
  `A4D_GLOBAL_327_BOOK_FISHER_CAR16_MAGNETIC_WICK_AND_DARK_REVIVAL_2026_10_20.md`,
  section 8: conditional current contraction and its required-task boundary.
* `02_REGISTRY/research/A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md`,
  sections 1-2 and 6: actual marked map, source-preserving clock reduction,
  and the exact existing finite-future application.
* `02_REGISTRY/research/A4D_GLOBAL_RESULT_COMPOSITION_2026_10_20.md`,
  section 4: the existing equal-suffix Julia ratio test consumed here.
