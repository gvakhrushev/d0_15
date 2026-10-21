# Independent bounded review: finite retained-channel source reconstruction

21 October 2026. Reviewer: `native_action`, independently of the packet's
`compiler_source` author, within the existing PR #334. This review owns
only this file. No scientific task, physical selection rule or publication
status is introduced.

## Disposition and exact parent substitution

**ACCEPTED at the stated mathematical and operational scope.** The one-slot
channel identity is exact, the required endpoint unitaries have literal
forward Golden/CNOT words of equal per-address inventory, and the sixteen
separate tests reconstruct the full derivative of the declared terminal
CQ channel. The source calculation retains the original finite efficiency,
readiness and entropy law. I found no remaining mathematical defect in
this scoped construction after the qualifications described below.

The already published four-setting report-source result at
`f996faae1eabd552a4f1573174bb6738a4c61c35` owns the removal of the
limiting-word premise for the report/price-source test. This packet's
additional result is the exact derivative of the entire declared
256-work-output density, including surviving within-OR coherences. Its
proof does not identify equal report probabilities with equal work states.
No minimal number of settings is established.

The resulting finite test can be composed with the already owned spatial
source pullback. It does not construct the native admissible field
variation, choose an absolute Book03 action or imply physical stationarity.
Thus it removes a source-reconstruction approximation, not the remaining
physical source-selection premise.

## Reviewed files and immutable binding

The following SHA-256 hashes bind the final reviewed bytes. A subsequent
scientific change requires review of the actual delta; a matching filename
or unchanged PASS label is insufficient.

| File in this packet | SHA-256 |
| --- | --- |
| `PROOF.md` | `8c96b986b9c106ea41c4362ef8989a333f89dfff0f337de0181100fe9a1e34a7` |
| `check_finite_native_source.py` | `536b96d6ae7e4d4f162cfe3e582e4d307fc897c3855ab2e7ab69b8aaebc21cfc` |
| `RESULT.json` | `5b40ef29c640b79f6a46121f862b5a4f00538f03f759a7d9f32ef017dcbf42dc` |
| `SOURCE_PINS.json` | `e1299cc294d0b5787da9e408918b3759c2bcdf99ac4c24a77134cdf323d267a1` |
| `VALIDATION.json` | `24e33a0fca298bc4243747e239c9049f304f11b7cfad689ccd703a25a336c855` |
| `CONCURRENT_FOUR_RESULT.json` | `97289b6344a7a4d78e11ce4f629cf045536b099065075d0d282b5170b526a1c9` |

`SOURCE_PINS.json` separates the six original inputs at
`80d3b1bac1bb9a974f365dbc4c48d3ada539d3a2` from the concurrent four-setting
owner at `f996faae1eabd552a4f1573174bb6738a4c61c35`. I independently
verified all seven current file hashes, their Git object hashes, and
byte equality to the stated historical files. The new concurrent owner
is attributed rather than re-claimed.

## Hypotheses actually used

The channel theorem uses an unconditional factor `R(t) tensor I`, or its
implementation with the supplied known-one controller, inside the
specified fixed linear input/output maps. The logical data may be mixed
or entangled with a reference. The controller input is fixed; it is not
an unknown coherent superposition of bypass and active sectors.

The detector specialization uses the original two full8D queries,
rank-two preparation, coherent efficiency flags at `z=2^-20`, OR report,
and inherited compiler/abort record. The existing compiler law supplies
fixed, data-independent readiness `alpha beta` and its stated conditional
maps. The varying coordinates are the original `x,y`; independent changes
of preparation, readiness, work prices or clock dynamics are not included
by declaring their derivatives zero. Fixed additive primitive charges
and the original reach law underlie the equal-ledger comparison.

The phrase **full retained channel** refers to this declared final
work/OR plus inherited compiler/abort CQ interface. It does not add a new
state-dependent measurement between the primitive gates of a padded
word. Nor does it identify an independently readable program-setting
register, or a new per-tick work archive, across distinct programmes.
Such an enlarged carrier would require its own common-instrument map and
source calculation. This boundary prevents the terminal-channel theorem
from being read as a theorem about every possible physical clock archive.

## Independent mathematical checks

### One-slot identity and its necessary exclusion

With `p=phi^-1`, `a=sqrt(p)`, the exact relations are
`cos(2 theta)=p^3`, `sin(2 theta)=2 a p`, and
`sin(4 theta)=4 a p^4 != 0`. For a purified input through one unconditional
slot, let `w=w(theta)` and `v=w'(theta)`. The endpoint vectors satisfy

\[
w(3\theta)=c w+s v,\qquad w(-\theta)=c w-s v.
\]

Their outer-product difference is exactly

\[
2cs\bigl(|v\rangle\langle w|+|w\rangle\langle v|\bigr).
\]

The factor is `sin(4 theta)`. This directly proves the derivative as a
linear-map identity, including arbitrary off-diagonal entries and a
spectator/reference. A fixed CQ instrument preserves it by linearity.
No small-step limit or density normalization has entered.

The exclusion of coherent bypass is substantive. For controlled `R(t)`
on `(|0,0>+|1,0>)/sqrt(2)`, a density entry is `cos(t)/2`. The proposed
two-shift quotient gives `-sin(theta)/(2 cos(2 theta))`, whereas the
actual derivative is `-sin(theta)/2`. These differ. Both the final proof
and exact checker retain this negative control.

### Forward implementation and work outputs

The two cells have full controlled operators `diag(G,G)` and
`diag(G,G^-1)`. Three cells produce `diag(G^3,G^k)` for `k=-1,1,3`.
The inactive controller block is retained, and the active known-one
controller returns to its input. The identity therefore applies to the
logical data/reference with that supplied controller, not to an arbitrary
coherently controlled extension.

Padding all eight occurrences gives `24 G + 52 CNOT` per reached query
block, including the original four tail CNOTs. The output expansion keeps
all 256 work labels and fixed efficiency monomials. Its amplitude
coefficients lie in `Q[a]/(a^4+a^2-1)`; the full amplitudes also contain
`sqrt(z)` and `sqrt(1-z)`. Squared probabilities lie in `Q[a]`.

The final code checks 4,096 endpoint amplitude equalities and 2,048
individual output-probability first-jet identities. The proved
polarization identity then covers the 65,536 density entries per slot;
these are not represented as an independently enumerated matrix test.
Fixed OR dephasing preserves the result and retains the coherences inside
each report block.

### Original coordinates, entropy and sign

The eight slot derivatives add with their actual coordinate factors
`D_x theta_E=a/2` and `D_y theta_b=-a^3`. Consequently

\[
D_x\Omega=\frac{1}{8p^4}\sum_{\ell\in E}\Delta\Omega_\ell,
\qquad
D_y\Omega=-\frac{1}{4p^3}\sum_{\ell\in b}\Delta\Omega_\ell.
\]

Applying the original report effect yields exactly

\[
r_x=4zQp^{11},\qquad r_y=-8zp^6(R+Qp^6),
\]

with the original definitions of `Q,R` and `z`. The source follows from
the actual family law

\[
S=B-\alpha\beta h_\varphi(r),\qquad
DS=-\alpha\beta h'_\varphi(r_0)\,Dr.
\]

This is the chain rule of the specified CQ family. It is not a shifted
entropy-value identity, and it does not assume an ambient entropy
Fréchet derivative at arbitrary rank-deficient matrices. The nonlinear
negative controls are correctly retained; directly shifting the entropy
produces nonzero errors at this fixture.

The sign transport is explicit: this detector uses
`y=+eta^2 q` and `b=(p-p^2 y)^2`; the covariant two-density packet uses
`Y=-eta^2 q=-y`. Therefore `r_Y=-r_y` and
`r_Y/r_x=-lambda_minus(2^-20)>0`. The raw negative sigma-minus ratio
cannot be reused as the positive `Y`-coordinate multiplier.

## Paid inventory, aborts and statistical interpretation

The value 76 is the inventory of a reached query block. The value 1,216
is the available query inventory for one launch of every setting, or its
upper bound if an earlier inherited abort prevents query execution. It
is not an unconditional average executed charge. Preparation, compiler,
abort, routing, record and repetition costs remain additional. The same
qualification applies to the concurrent four-setting owner's 496-query-tick
inventory. Both results retain the actual readiness law.

The unconditioned observation `Y=1` only for a ready OR click has mean
`alpha beta r`; all other runs contribute zero while their records remain.
The displayed signed estimators are therefore unbiased for the original
source components. Their variance formulas sum the eight independent
Bernoulli means in each component, and the Hoeffding/union bound has the
correct sixteen-mean factor. The pullback norm and required signal
normalization must be included in a concrete spatial precision budget.
The calibration `h'_phi(r0)` is treated as known; learning it needs the
additional baseline estimation the proof explicitly reserves.

Exact algebraic differentiation does not mean exact finite-sample
inference. A signed classical reconstruction statistic is also not the
physical price of the multi-run apparatus. The latter keeps its positive
paid ledger and all observed aborts.

## Bounded replay and limits of validation

I independently ran the final checker with Python 3.12.14 and mpmath
from `/tmp/d0_math_deps`, using

```sh
PYTHONPATH=/tmp/d0_math_deps python3 \
  02_REGISTRY/research/sources/d0_finite_native_source_reconstruction_2026-10-21/check_finite_native_source.py
```

It completed successfully in approximately 0.50 seconds, produced no
stderr, and its stdout was byte-identical to the bound `RESULT.json`:
`5b40ef29c640b79f6a46121f862b5a4f00538f03f759a7d9f32ef017dcbf42dc`.
The final change after this replay was only the precise prose statement
that polarization is proved analytically and then used, rather than
separately enumerated by the code. The checker and all data bytes did
not change.

The author's normal/optimized replay agreement is recorded in the bound
`VALIDATION.json`. The concurrent four-setting result was inspected as
an existing input, and its supplied receipt hash was verified against
that validation record; I did not count the author's separate concurrent
replay as my own. No large historical compiler suite, all42 continuum
suite, Lean build, sampled physical experiment or compulsory Book-price
derivation was performed or asserted by this review.

## Remaining physical boundary

This packet supplies a finite exact test of an already specified source
and a stronger terminal-channel derivative interface. It does not give
an ordinary continuous derivative to a fixed finite native word family,
a same-initial-state field writer, a compulsory complete Book03 Info
functional, or a proof that independently variable preparation/clock/work
sources vanish. The original field-minimum exclusion and upstream source
obligations remain in force. `GR_closed=false`.
