# Independent review: actual-port maximum-entropy preparation

22 October 2026. Reviewer: bounded `stationary_native_source` reviewer
within existing Draft #334; independent of the maximum-entropy author.
This is acceptance of the scoped mathematical argument and its stated
parent use, not physical Book03/GR or assembly/lifecycle acceptance.

**Verdict: ACCEPT at the following frozen contents.**

| Reviewed path | SHA-256 |
|---|---|
| `MAXIMUM_ENTROPY_PREPARATION.md` | `0a58a36d5302960187869c2b5c0c73660a53bc4d0f105c2d03b1c0e0dcc34a87` |
| `check_maximum_entropy_preparation.py` | `46437bc428228dd5c86b3af872517e88037e82ec84cea888a8a8aef8dec97cde` |
| `MAXIMUM_ENTROPY_RESULT.json` | `fd4fd5827c6e54a14547a7068008e167337cd2ed9401097b9232032ef1fdfe37` |
| `../../A4D_NATIVE_COMPLETE_SOURCE_REDUCTION_2026_10_22.md` | `5f4f889276f1516870a085d7109b0b3d72c6b0664b5628e8bdf36e78d2052c10` |

The root-synthesis review concerns the mathematical composition and the
scope of the maximum-entropy and cut-source conclusions. The companion
complete-history numerical regularization is being independently
finalized and is not accepted by this review merely by appearing in the
same root document.

## 1. The variational problem is the specified native marginal problem

The actual original effect is a positive scalar multiple of Delta, so
preserving its actual mean response is equivalent to preserving
`Tr(sigma Delta)=d/Tr(Delta^-1)`. The maximizer's uniqueness follows from
strict concavity of entropy on faithful finite-dimensional states. For a
nonscalar positive Delta the harmonic mean lies strictly between its
extreme eigenvalues and below its arithmetic mean. The Gibbs energy
map has strictly negative derivative. Thus the positive dual multiplier
exists uniquely; the scalar exception is correctly treated separately.

This problem preserves **one specified DATA response test**. Neither its
state nor its multiplier is promoted to a compulsory whole-history
preparation or physical thermal selector.

## 2. The two-band iff and moving-test differential are valid

Equality of the normalized inverse state and a Gibbs state gives
`log(lambda)=a+beta lambda` at every spectral value. A strictly concave
logarithm cannot equal the same affine line at three ordered points.
Conversely the secant slope for two positive eigenvalues makes the two
state matrices equal, regardless of their multiplicities. The proof
does not accidentally assume equal eightfold multiplicities until the
native application.

The entropy envelope is exactly

`D S(sigma_ME)=beta_star [D h-Tr(sigma_ME D Delta)]`.

The moving-observable term is essential. The implicit-function argument
uses the nonzero energy variance, so smoothness persists when a tangent
splits a degenerate band. Smooth nonnegative relative entropy with zero
value then has zero differential in every Hermitian direction. This is
a statement about the **gain**; it does not incorrectly set the entropy
of the native state itself to a constant.

## 3. The noncommuting Hessian is correct

At the two-band equality point the matching trace and energy constraints
force `X=D rho-D sigma_ME` to have zero trace in each band. The inverse
derivative and exponential divided difference agree on cross-band
entries. The remaining block is therefore exactly

`X_aa=tau_a (beta_star-1/lambda_a) E_a^0`.

The relative-entropy Hessian at equality is
`Tr[X Dlog_rho(X)]`. As each base density block is scalar, substitution
gives precisely the displayed sum in Theorem 2. No factor two is missing:
the Taylor coefficient is one-half of this Hessian. Path acceleration
does not enter because the first differential vanishes in all directions.

I also made an independent noncommuting numerical control, beyond the
author's diagonal band-splitting check. It uses

```
Delta = diag(1,1,3,3)
E = [[1,.3,.4,-.2], [.3,-1,.15,.5],
     [.4,.15,.2,-.1], [-.2,.5,-.1,-.2]]
```

For this real Hermitian E, `||[Delta,E]||=1.944222209522358`.
The analytical Hessian is `0.16663770106853618`. Re-solving the actual
harmonic-energy Gibbs constraint on both spectra of `Delta +/- 10^-3 E`
gives the centered KL Hessian `0.1666374314590734`, error
`2.696094627829826e-7`, below the declared `2e-6` diagnostic tolerance.
Keeping only the cross-band entries gives `-1.4019639149904797e-11`,
consistent with the exact zero second response. This is a numerical
independent control of the analytical argument, not an interval bound.

## 4. Numerical replay and native temperature boundary

I executed the unchanged `check_maximum_entropy_preparation.py` through
a read-only subprocess, parsed its output, and compared it with the
authored `MAXIMUM_ENTROPY_RESULT.json`. The outputs are exactly equal:
**23 explicit checks PASS**. Expected evidence was not regenerated.

The checker uses exact rational native inputs and 80-digit Decimal
logarithms/exponentials. Its Gibbs root and band-splitting checks are
high-precision diagnostics; the proof correctly does not claim interval
certification. The scalar degeneracy is rejected by the unique-multiplier
routine, and the mixed three-band control has a strict positive gain.

The native `beta_0=2p^2` and the dual multiplier around `72.412` remain
different. The numerical use of a minimum-energy subtraction inside
normalized Gibbs weights is only a stable evaluation and is not applied
to the absolute physical heat. The native thermal mismatch is retained.

## 5. Parent scope and corrected boundary

The root synthesis preserves the three required separations:

- Coherent rank-one READY cut and sequential original full128 instrument
  remain distinct actual carriers.
- Solving the native one-moment marginal maximum-entropy representative
  does not select whole-history Book03 Info or replace its nonzero
  conditional quantum source.
- The source-bearing `chi_y,V_y` writer remains open, while fixed
  Golden prefix/controller data and generated intermediate registers
  are not fictitious independent Euler variables.

I also reviewed its new whole block-diagonal-algebra application in
Section 4. Retaining every block-diagonal test fixes `E(sigma)=E(Omega)`.
Pinching cannot decrease entropy, and equality is possible only for the
already block-diagonal state. Thus `E(Omega)` is the unique maximum;
the standard same-trace relative-entropy identity proves the stated
gain. The complete efficient-history isometry preserves the initial
spectrum, giving `S(Omega)=S(rho_initial)`. The root correctly retains
the derivative of that initial entropy and distinguishes a retained
pure purification. This analytical conditional-expectation application
is accepted; it does not select the block algebra physically or turn
the full-CQ entropy alone into Book03 Info.

The root text's original stray plus after the maximum-entropy link has
been corrected. The requested fixed-boundary clarification is now
present: a fixed complete initial state and fixed autonomous finite word
cannot by themselves provide a varying field chart. No remaining
mathematical correction or physical overclaim was found in the reviewed
maximum-entropy application and its composition.

## 6. Follow-up review: measured-CQ price and forgetting-gain price

This follow-up reviews only the Section 5 source-convention delta from
the previously accepted root-synthesis SHA-256
`4a8c96891e5d0be0ba7a3ac6a8b682d3a374c7ebdf466c49bad2181e3e839346`
to the current synthesis pinned above. The unchanged maximum-entropy
proof, checker and receipt retain their earlier acceptance; no tests
were rerun for this prose/formula correction.

The finite-tree identity gives
`S(Gamma)=S(rho_initial)+sum_w p_w c_w`. Therefore the measured-CQ price
`E C-S(Gamma)/ell` has exactly the source now displayed:

`dS_CQ=dE C-dS(rho_initial)/ell-sum_w(dp_w c_w+p_w dc_w)/ell`.

For the distinct forgetting-gain convention
`I_A=S(Gamma)-S(rho_initial)`, the price `E C-I_A/ell` instead has

`dS_gain=dE C-sum_w(dp_w c_w+p_w dc_w)/ell`
`=dS_CQ+dS(rho_initial)/ell`.

The signs and the initial-entropy subtraction are correct. The product
rule retains both moving prefix weights and moving conditional quantum
states; the two price sources coincide only when the admitted initial
entropy has zero differential. This does not assume a fixed mixed
preparation on a genuinely moving inverse-square input. A retained pure
purification must still use its own complete states, as Section 4 says.
The root explicitly computes both declared conventions without selecting
either as compulsory Book03 Info or adding one to the bare cut action.
**Delta verdict: ACCEPT; no mathematical correction or physical-source
overclaim found.**

`GR_closed=false`; no BOOK text, accepted assembly premise, lifecycle or
physical admission flag is changed by this review.
