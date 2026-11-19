# Independent acceptance of the reconstructed oriented-price packet

21 October 2026. Reviewer: metric_source_synthesis. Existing PR #334;
bounded read-only review, no additional research or repository edits.

**ACCEPT the conditional mathematical reconstruction at its stated
interfaces.** No remaining mathematical defect was found. This acceptance
does not supply actual full quantum-query independence, compulsory Info,
native reference preparation, or the vanishing physical residual.

## Exact reviewed files

All inputs are in `/private/tmp/d0_restoration_oriented_20261021/`.

| File | SHA-256 |
|---|---|
| ORIENTED_COMPLETE_PRICE_RECONSTRUCTION.md | `977854fedc570c88c1e29714463dfed18109add94bafaf738158c3ab243ba626` |
| SOURCE_AND_RANK34.md | `125dc37a40b02f1091a98d61065833d5062ed8196c988edc46b00126f032f022` |
| check_oriented_complete_price.py | `fe6b278f81ccf5cc24be1dc7815d333ed2cc01c4325b8749a2db1e3370fc9d4a` |
| SOURCE_PINS.json | `2e91f93403d9b70d505dbeb990501e8dbf054106dbeaf743d8d58a3c97d147bd` |

All nine source pin hashes and Git blobs were independently checked against
the stated input snapshot `8ba0bd929499e639b0fe4640ffa448631f3b024b`.
The original Golden17 component calibration and the rank34 owner's actual
chart/selection boundary were read directly. Their historical computations
were consumed, not repeated or presented as new acceptance.

## Independent mathematical checks

1. **Finite bank and stopped sampler.** A pair of original Golden bits
   has raw probability p^3 for each of 10 and 01. For m pairs, each accepted
   d-ary code has raw mass p^(3m), so readiness d*p^(3m) and exact conditional
   uniformity follow. Independent disjoint slots remain independent after
   conditioning on their joint readiness. The stated d=24 selector and
   d=2n stop slots therefore implement the finite sampler exactly, with
   every failed and unused raw bit retained. Reach probabilities are
   `a_(n-1)(1-x)^(n-1)`; both the full termination-law telescope and the
   mean-call formula are correct. The derivative formula for f_N is
   positive for all finite N on the claimed domain. A vanishing readiness
   as N grows is not hidden by the normalizations.

2. **Complete entropy chain.** Condition on the entire prepaid bank.
   Each reached query has the same full conditional law by H1, and its
   reach indicator is known before that query. Its entropy contribution
   is therefore its reached probability times h(P). Averaging the selected
   category gives `A_N=h*mu_bar_N`. The shared category couples the call
   counts, but contributes no extra term after the complete bank is
   conditioned on. Executing both streams even when the first fails is
   essential and explicitly included. Fresh G1,G2 give
   `Pr(E)=p^2[1+r_N K_N/24]`; fresh G3 contributes precisely g*Pr(E).
   This independently yields
   `C_N=H(B)+2g+gp^2`, `c_N=gp^2 r_N/24` and the stated complete price.
   A premeasured retained third bit has zero extra conditional entropy
   when copied. The proof correctly keeps H5 or the separate additive
   net-ledger hypothesis: neither follows from the coarse Golden17 law.

3. **Kernel, mixed source and minima.** The six strict-positive amplitude
   contrasts and the inversion-invariant five complements give exactly
   `BC(P,Q)-BC(P,Q^-1)=b(P).b(Q)=k<R(P),R(Q)>_F`, with
   `k=p^4/98304`. The complements cancel only in the comparison. For finite
   N the kernel is b_N(P).b_N(Q), whose derivative has the stated positive
   diagonal factor at identity. Four-execution rectangular subtraction
   cancels self-prices algebraically, without deleting their cost/source
   from a single execution. The square completion and minimum criterion
   are exact. Necessity uses the independent admissibility of (P,P^-1)
   and inversion-evenness of the FULL A_N, not merely its coarse marginal.
   The strict version retains this assumption and the appropriate quotient.
   Positivity of a limiting excess alone is correctly not used to assert
   positivity for every finite cap.

4. **Lorentz reference and finite-N residual.** For the stated symmetric
   orthogonal eta, `J(X)=eta X^T eta` is a Frobenius-self-adjoint involution.
   Consequently Pi_- is the correct orthogonal projection; an arbitrary
   B^T cannot itself be presumed to be Lorentz Lie algebra valued. For
   A in that algebra and sufficiently small epsilon, the analytic root
   H commutes with A, J(H)=H and `(H-epsilon A)(H+epsilon A)=I`.
   Thus Q lies in the identity component and R(Q)=epsilon A exactly.
   The pairing with `A=Pi_-B^T` reproduces `tr(BR)`, including the moving
   reference derivative. Formula S11 is exactly the derivative of the
   complete finite price minus its proposed source; it retains both
   self-prices and the finite-N defect `K_N-k epsilon J`. Matrix existence
   does not establish native compilation or erase the reference price.

5. **Rank34 and full-source boundary.** The original rank34 result is
   used only as a local probability-coordinate theorem on its declared
   metric10+link24 chart. Formula S4 has the correct negative logarithmic
   Jacobian coefficient. S5 includes the moving price and score covariance.
   The coarse entropy Hessian is negative in probability coordinates;
   the conditional fine-record entropy and the second derivative of the
   nonlinear field embedding remain in S6–S7. The packet does not identify
   full128, Golden17 and the stopped programme by parameter count. A
   same-field preparation/readout map remains required.

## Fresh executed check and implementation corrections

The mathematical draft was run independently once from a byte-identical
scratch copy. The author then made two requested checker-only repairs:
bare asserts became explicit failures, and default execution became
stdout-only, with file output only under an explicit option. The frozen
checker listed above was therefore run once more to validate the changed
final bytes and output behaviour. Both runs passed; no mathematical
fixture or expected value was weakened.

Final independent result: `PASS_NEW_ORIENTED_RECONSTRUCTION`, 0.480 seconds.
The full N=1 price discrepancy was `8.69345191567e-70`; the mixed rectangle
was `4.3374513028005993886831073513763145e-18`, with discrepancy
`5.92624238964e-71`. The existing author receipt hash was unchanged by
the default invocation, confirming its read-only behaviour.

**Fixture boundary:** this complete N=1 replay treats the seventeen q_i
as an atomic fresh classical query law. It includes its actual five
complements, every bank record and both queries. It does not verify H1
for a finer quantum/coherent physical query transcript, nor H5 for
compulsory Book03 Info. Those remain explicit hypotheses of the analytic
full-transcript theorem.

Final independent output:
`/private/tmp/d0_restoration_allflag_20261021/ORIENTED_FINAL_INDEPENDENT_CHECK.json`,
SHA-256 `2821d910c041b6ad4598e04614fd9b5c6bf802ba5713a23c526fe02547b0f0b2`.

No historical ZIP, patch, test count, old review, native selection or GR
closure is certified by this new review.
