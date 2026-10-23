# Independent review: complete original-native quantum history source

22 October 2026. Reviewer: independent `native_definitions` subagent.
Existing scientific owner: Draft PR #334. The author froze the three
inputs below before the single affected replay. No authored input or
expected output was modified during review.

## Verdict

**PASS for the declared finite-instrument theorem and bounded original
CAR16/full128 application.** No blocking mathematical or implementation
issue remains in the reviewed bytes.

The exact finite-tree entropy identity, the specified Book06-style
maximum-entropy pinching map, original stationary quantum-block formulas,
and all-mode regularization bounds are correct. The numerical source
diagnostic retains the moving invariant preparation, every positive
quantum mode, all physical outcome slots in the carrier accounting,
and the distinctions between mixed DATA, retained purification and an
independent oldRIGHT spectator.

The result is not a proof that this retained algebra or either entropy
convention is physically selected by Book03. It does not generate a free
exact finite preparation or identify this Fourier fixture with the
separate 42-field Einstein carrier.

## Exact frozen inputs

| Input | SHA256 |
|---|---|
| `COMPLETE_HISTORY_SOURCE.md` | `f1ee97765d7c8a82ff65f4ab81f46cb626e6780856fac34684efa8d4cac92d51` |
| `check_complete_history_source.py` | `cd0052f10bc43abb3736a1637c850c2a3d637f428dd116f6320f68bcf84e3931` |
| `COMPLETE_HISTORY_RESULT.json` | `6218f76ba21a2eeba064b9a855395d3fd358cf7c4d7ae58d4f56a5c1f9ef0515` |

The reviewer checked these hashes before and after execution. They were
unchanged. The native constructor's declared original Git blob is checked
by the reviewed program before AST-loading its six needed definitions.

## 1. Finite tree and complete source

For a complete finite stopping tree, every nonroot internal `s(X_w)`
occurs once with each sign. Thus the telescope is valid for different
history lengths, capped abort leaves and adaptive efficient instruments,
with actual preparation prefixes included as ordinary earlier nodes.
No independence or reset assumption is used.

At each live node, completeness makes `V_w` an isometry, so its coherent
output has the input's nonzero spectrum. Pinching this output gives the
direct sum of child blocks. Equality of its block-diagonal logarithmic
pairings proves the equal-mass relative-entropy formula. Positivity
ensures the unpinched operator has no support outside the support of its
pinched version: a zero diagonal quadratic form forces the associated
row and column of a positive operator to vanish.

The source recursion differentiates all three factors of
`K X K*`. The omitted `+I` terms in the whole entropy gradient cancel
only after summing the full normalized tree. The proof states its
fixed-support logarithmic formula and separately treats the amplitude
regularization used for the numerical rank-deficient blocks. Integer
cap changes are not misrepresented as smooth derivatives.

## 2. Exact Book06 maximum-entropy application

Equations (5a)--(5b) are sound. Specifying **all** block-diagonal
history-by-quantum-work tests fixes precisely the diagonal blocks
`Gamma`. For every compatible positive state `sigma`, its support lies
within that allowed by those blocks and

```
D(sigma || Gamma) = S(Gamma)-S(sigma) >= 0.
```

The equality condition establishes the unique maximizer `Gamma`, even
with rank-deficient blocks. Applying this to the actual stopped coherent
isometry `Omega=W rho_0 W*` yields

```
I_gain = S(Gamma)-S(rho_0) = D(Omega || Gamma).
```

The theorem therefore supplies a concrete conditional expectation and
maximum-entropy representative for that declared retention/loss
interface. It does not infer the physically selected algebra from a
convenient entropy value. Retaining the entire coherent algebra instead
gives zero forgetting gain, as the proof explicitly states.

The moving mixed-input boundary matters: the gain source is
`dS(Gamma)-dS(rho_0)`, not `dS(Gamma)`. The separate supplied
Cost-minus-CQ-entropy convention uses the latter. Both are distinguished
in the reviewed proof, and neither is silently declared compulsory.

## 3. Native operator, preparation and reference bookkeeping

The quantum-block identity follows directly from the original
`K_{j,b}` and `A Delta^-1 A=I`. It retains `N_j* N_j`, rather than
replacing those matrices by their traces. The ordinary blank remains
`B^2 Delta^-1/Z`. Two rounds use ordered Kraus products on the previous
output. The reviewed source includes the derivative of the normalized
inverse-square preparation and the true `dtheta/dr=81/40` factor.

The reference distinctions are correct:

- Mixed DATA and a readout omitting its purification have a conditional
  DATA entropy term.
- With a real pure purification retained, every efficient conditional
  DATA/reference block has rank one, so its CQ entropy is the complete
  pointer entropy. The purification's field derivative is included through
  the square-root Sylvester equation.
- A genuinely independent fixed oldRIGHT128 tensor factor adds
  `log(128)` to normalized total entropy. For an individual unnormalized
  branch it adds `P(w) log(128)` and the corresponding probability source;
  the latter sums to zero on the complete normalized tape.
- The same register is not counted simultaneously as a purification and
  as an independent maximally mixed spectator.

The separate determinant's multiplicity 128 is not applied as an entropy
multiplier. The existing complete coherent record marginal is also not
confused with the complete pure system/reference/record state.

## 4. All-mode SVD and quantified regularization

The final reviewed checker has no positive-eigenvalue cutoff and performs
no clipping of a Hermitian spectrum. For each actual word amplitude
`A=K_word sqrt(rho)`, it uses every squared singular value and its
directional derivative

```
lambda_i = s_i^2,
d lambda_i = 2 s_i Re[(U* dA V)_ii].
```

This gives the derivative of the symmetric regularized spectral sum
also at repeated singular values. Zero singular values are retained and
contribute through the same regularized formula.

The bounds in the proof are valid. For `lambda>=0`,

```
0 <= lambda log(1+eta/lambda) <= eta.
```

For its derivative,
`b_eta(lambda)=log(1+eta/lambda)-eta/(lambda+eta)`, the inequality
`sqrt(lambda) b_eta(lambda)<=2 sqrt(eta)` follows, for example, from
`log(1+x)<=2 sqrt(x)`. Differentiating `A A*` and applying the
Hilbert--Schmidt Cauchy--Schwarz inequality gives the stated
`4 sqrt(D eta) ||dA||` source bound, including the amplitude limit at
zero singular values.

The whole-word amplitude derivative bound follows from the product
rule for the complete sequential isometries: all undifferentiated
isometries have operator norm one. Although CQ amplitudes can be arranged
block-diagonally whereas coherent amplitudes are stacked, the sum of
their squared Hilbert--Schmidt derivative norms is identical. This
justifies the norm bound used for the CQ blocks.

The carrier factor remains `D=16*128^n`, including the structurally dark
word slots. Only exact odd-Walsh rows are omitted from numerical work;
their vanishing follows from the constructor's adjacent duplicated
words and is checked. All remaining positive labels and every singular
value in their amplitudes are retained. The checker does not infer zero
support from a floating tolerance.

At review request the author added explicit initial-entropy and gain
error budgets before freezing the final inputs. The final receipt now
contains the initial `D=16` bound and the sum of initial plus CQ bounds
for the dephasing gain. The largest displayed gain-source regularization
budget over the four native diagnostics is approximately `8.40e-9`.
These are analytic **regularization** budgets instantiated numerically,
not certified enclosures of all floating arithmetic; the proof and
receipt state that distinction.

## 5. Numerical application and targeted validation

The original constructor is read from the pinned blob and its older
test suite is not run. The added analytic `(theta,nu)` source extension
keeps the original words and both Julia-defect derivatives. Its primal
and theta source are compared against the unchanged original constructor.

The diagnostic uses every physical one- and two-round slot, checks
normalization and the differentiated stationary marginal, verifies every
stationary nonblank quantum-block identity, and compares the first source
with independent five-point value derivatives. The algebraically
one-port-neutral tangent retains a nonzero fine-pointer source and a
different complete CQ source, as reported. The two regularizations
`eta=1e-22` and `1e-24` agree within the declared bounds.

The separate rational noncommuting tree retains two preparation rounds,
an anchor, both stopping outcomes and capped aborts. Its probability and
source normalization are exact rational equalities. Its entropy/source
telescope is numerical. The check rejecting deletion of conditional
quantum work is nonvacuous. This fixture is correctly presented as a
bookkeeping control, not a native physical-preparation replacement.

The native stationary boundary remains a consumed marginal theorem;
it is not offered as an uncharged finite preparation. A real finite
preparation must be included in the complete execution tree, as required
by the analytical theorem.

## 6. Single affected read-only replay

Environment: primary Python runtime `3.12.14` with its NumPy/SciPy.
After the author declared the final freeze, the reviewer executed exactly
one affected run:

```
python check_complete_history_source.py
```

No `--write` option was used. **All 50 checks passed.** Its stdout was
compared byte-for-byte with the frozen `COMPLETE_HISTORY_RESULT.json`
and matched. The proof, checker and receipt hashes were unchanged
afterward. No older suite was replayed. The author's separate normal
and optimized parity report is not misrepresented as an additional
reviewer execution.

## Accepted scope and parent boundary

The reviewed result supplies a complete finite-tree information-source
map and a concrete original-native stationary-marginal application,
including the conditional quantum-work contribution and a specified
maximum-entropy forgetting interface. Its missing physical application
remains the selected Book03 heat/cut/retained algebra, the actual paid
preparation and controller, and the source/refinement transport to the
existing geometric carrier. `GR_closed=false` remains correct.
