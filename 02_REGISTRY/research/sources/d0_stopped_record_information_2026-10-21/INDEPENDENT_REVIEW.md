# Independent review: original stopped-record information source

21 October 2026. Reviewer: `record_recovery_source`. **ACCEPT** within the
stated finite-clock, declared-record-algebra scope. No substantive blocker.

Proof: `A4D_ORIGINAL_STOPPED_RECORD_INFORMATION_SOURCE_2026_10_21.md`, SHA-256
`c6f85eba8205db743f3f5b11115af5f48bb6ef36923129fbf07dab6d7cd72b27`.
Checker: `sources/d0_stopped_record_information_2026-10-21/check_stopped_info.py`,
SHA-256 `ae1cf6e60cfe6bf94893e91ac777dfc52f2afcccc0f4e72516338b82de59a3d8`.

Reviewed the proof, the final changed checker, the actual stopped-instrument
owner, the old AF Gram/central-reference owner and the pinned builder's
recycling/source conventions.

* For columns v_omega and the global pure state sum v_omega tensor |omega>,
  the flag density is `(M* M)^T`, and its nonzero spectrum equals that of
  `M M*`. The latter is exactly the stated stopped CP sum, with the full
  actual reference in H tensor R, all 127N+1 labels and the unresolved leaf.
  The entropy being computed is S(F). R remains physically retained and is
  in its computational complement H tensor R; S(F tensor R) would be a
  different chosen information cut, not the displayed formula.
* Subtracting the genuine blank channel yields the stated exit map, including
  the negative epsilon-squared term. The forward derivative and backward
  recurrence (5) retain both Kraus sides, exit-map motion and the true initial
  preparation derivative. Xi is the gradient at the current sigma, not an
  additional variable to differentiate in this first-source calculation.
* Finite-dimensional amplitude entropy is C1 through rank birth, with born
  contributions O(t^2 |log t|). The regularized-log interpretation is valid;
  no Hessian or N/h-uniform conclusion is implied. The pointer chain rule
  includes every surviving prefix, stopping time and terminal unresolved
  probability. Structural dark labels are not physically deleted.
* Both Info signs and moving-code cancellations are correct. Quantum relative
  entropy to a noncentral code reference is not automatically the measured
  one-copy maximum; the note explicitly retains that missing physical input.
  The coherence difference is finite with its actual support and enters the
  two net-price conventions with opposite signs. Paid coherent padding stays
  in W; entropy equality does not license a cheaper execution clock.
* The final two-port noncentral-reference control is correct. For controller
  label k>=1 the original flattened Kraus indices are 2k and 2k+1, with ratio
  p^(-1/2); the first-prefix leaf columns are 2k-1 and 2k. The flag transpose
  convention therefore gives tau_(k0,k1)=r_(k0)/sqrt(p)>0 on a possible leaf.
  The product-code ratio is mu_(k1)/mu_(k0)=p, so the commutator entry is
  `(p-1) mu_(k0) r_(k0)/sqrt(p)`, strictly negative. These are two original
  nonblank labels of the same prefix, not a cross-clock or omitted-blank pair.
* The Fourier/rank16-reference fixture and the primary full-site RIGHT128
  application remain explicitly distinct. The primary preparation source is
  given a usable formula, not an uncomputed numerical stationary claim.

Verification: static compilation of the final checker succeeded. An independent
small complex cap-2 control checked the nontrivial flag transpose, complete
Gram normalization, nonlinear adjoint and simultaneous exit/preparation finite
difference. It passed in approximately 0.2 seconds. Per the validation budget,
the full original-builder numerical replay was left to the integrator; it is
not claimed as independently rerun here. No repository file was edited.
