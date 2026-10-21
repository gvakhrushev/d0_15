# Independent review: READY scope and normalized range/cut logic

21 October 2026. Reviewer: the separate `universality_selection` read-only
subtask of existing PR #334. Scientific input:
`441bdef5a02bef09a74ebe48dcf4d5527ba18988`.

**Decision: PASS at the stated scope.** This is a mathematical internal
review, not external peer review or physical GR acceptance.

Reviewed exact bytes (SHA-256):

- `PROOF.md`: `5e605974ef2ba6d20226e34286e918171c1aaca905f9e97003e054397432e99b`
- `check_binding.py`: `20d861773c2f4c4d86636a90d738fbc13f4f144144d42ecfc33c7dd71ac7a14b`
- independent output: `8f79c4627784a65beb8692a73b74c679e34adc92afe5d05fa04a67c09bcbc200`

## READY calculation

I checked the complete first-crossing mass identity, the retained FR/RF,
FF/RR and overshoot classes, and the distinction between a scalar probability
weight and an absolute orthogonal-record amplitude. For normalized conditional
branch vectors, replacing `sqrt(P_omega)` by `P_omega` necessarily produces
`P_omega^2/sum P^2`. The conditional odds square, so a non-half READY click
probability changes. A common amplitude normalization cannot repair odds.

The proposed amplitude repair is correctly only a binding condition:
`I_amp=C+(1/2)log_phi P+J`. The proof does not infer this physical Info law
from the relative-likelihood equation, and explicitly requires equality on
the entire relevant input sector before drawing an operator conclusion.
Agreement at one prepared state is not used to determine a larger-input
Book determinant. READY and the moment writer remain distinct executions.

## Normalized determinant and actual cut

For fixed initialized isometry i, full-column W and invertible T, the two
matrices N and `(1-z)N+z A*A` undergo the same congruence by T. Their
determinants acquire the same positive factor `|det T|^2`, proving exact
invariance without a commutation assumption. Field-dependent derivatives
of T cancel because the equality is an all-parameter identity. Equivalently
the normalized output range projector is unchanged.

For the actual AB/BA writer the kept u=1 work makes all late branches
orthogonal to the u=0 initialized cut, while early aborts remain common.
Together with the common charged-schedule normalizer, this yields zero
code contrasts even with a nonzero early corner. The proof uses the actual
retained work; it neither erases failures nor inserts an extra flag.

Consequently a genuine same-range/full-amplitude binding cannot give this
particular initialized-cut determinant a nonzero source. A different active
cut, return map, physical range, heat operator or independent price term
can change that conclusion and is explicitly outside the theorem. No sum
of prices from different executions is inferred. A zero determinant source
does not imply that the whole Book price is zero, nor does equality at a
stationary field identify field equations.

## Independent bounded replay

Ran the unchanged checker with the source repository supplied explicitly.
It returned PASS, 54 checks, exact arithmetic in Fraction and Q(p), with
source fingerprints verified. Its READY figures reproduce the stated
full probability `0.3416407870701547`, squared-amplitude value
`0.2165417371274254`, and squared conditional click
`3.42710066570647e-12`. The rational matrix fixtures retain the nonzero
early corner, the normalization denominator, noncommuting right changes
and a failing denominator-omission control.

The replay tests the finite identities; the all-parameter range invariance
is the analytic congruence proof. It does not simulate a whole physical
factory, derive native admission, or select Book03 heat/Info/cut. No
substantive correction was required. `GR_closed=false` is preserved.
