# Integration review of the remaining two proofs and the residual lemma

20 October 2026. Root reviewer, separate from their authors. Input commit
972ce692a84b5b23bdf91e93a047b1882ad582d4; integrated over dec8b42a.

The two original independent reviews remain byte-identical. This review
covers the future-algebra theorem, the forced-record countermodels, and the
new residual lemma, with the hashes listed below. All five narrow checkers
were executed on final copied files; outputs are in VALIDATION.json.

## Accepted mathematical scope

1. The original Golden observables restrict to the three Pauli matrices on
   the two-dimensional code. A trace-preserving conditional expectation is
   trace-self-adjoint, so preserving all three expectations for every state
   fixes all Hermitian matrices and has the entire M2 range. This does not
   choose a scalar information functional. Book Info is scalar; Z is
   algebra-valued. Evaluating pointer entropy is distinct from discarding
   coherent state information. The script uses ordinary Python assertions
   and was executed without optimization; no -O validation is claimed.
2. The (x,b,H) model preserves every old distinction under injective T,Q,X,
   has an internal retained clock, noncommuting payload operations, and an
   injective complete future profile. T can still leave the unresolved pair
   observationally equal after any finite number of actual steps. This is
   a counterexample to the stated interface implication, not to all D0.
   The separate destructive-battery example concerns only generic future
   completeness and is explicitly not retention preserving.
3. For the residual lemma, zero a derivative gives a constant ridge by the
   mean-value theorem. At any neighboring a with nonzero u derivative,
   sufficiently small positive and negative u yield both signs relative to
   that SAME ridge value. Existence of two-sided partial derivatives and a
   nonzero limiting multiplier suffice. No differentiation of an entropy
   Hessian, uniform remainder, or C2 assumption is used in this proof.
4. The stronger C2 formulation correctly divides the DJ2 multiplier by
   gamma_h. The flat value of the multiplier alone would be uninformative;
   the neighboring limit is required. The residual PSD criterion is a
   necessary second-order slice condition, never sufficient for a full
   minimum. A zero first jet at the single root can stabilize, but a zero
   full first source on every neighboring ridge point cannot.
5. E_corr denotes the difference of the actual full scalar price and the
   supplied stopped branch. It is not Tr(rho R)+W in isolation: moving
   state, scalar, mark, controller and work terms must all be included,
   with no double counting. The algebraic cancelling control is not
   proposed as an admitted physical action.

The main synthesis keeps original stationary Einstein-CAR roots and finite
mesh/no continuum-uniform scope. The adaptive envelope has descent; at ties
it is not asserted to have an ascent. No Book/core/claim status is promoted.

A final independent consumer spot review by `/root/full_price_weld` found
and corrected one Russian notation error: the nonzero quantity in the
normalization formula is kappa_k, not the source kappa_k dt at a stationary
root, where dt=0. The corrected consumer now explicitly states this. The
review otherwise accepted its scope; no mathematical input or checker changed.

## Reviewed SHA-256

- `FUTURE_ALGEBRA_AND_STOPPED_NORMALIZATION.md`: `fa5f10facfd02a888dff41a7a9070f30a70acbe0234b135d8cc8dd03a94c6569`
- `check_future_algebra_and_stopped_normalization.py`: `8114c91d2cebe1f83fbf7af0eb3af8937fe191284399d0a683df6d71b3ec877d`
- `FORCED_RECORD_FUTURE_TEST_972CE.md`: `7de2cdc28fa5ec2b8a3b09ebd6398341a378b2be8b589f2b6b30ad4d9c906d54`
- `check_forced_record_future_test.py`: `6157544de87d11e376e21da583d10a2ddc460baedefbbe395dce8873d9589da2`
- `CORRECTION_SECOND_JET.md`: `439cc3de63db6788e5a8fb6c0d42c9c3e32bc34cf297971e590a83e4688b9505`
- `check_correction_second_jet.py`: `0d675802aa796fd4d0c3e457946bccb55a40663402b55942959e13767e6bf59c`
