# Complete native source: actual cut, marginal selection and full quantum history

22 October 2026. Existing scientific Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334),
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`constitutive/native-programme-v1`. This is a bounded research application;
`GR_closed=false` and physical Book03 source selection remain open.

## Parent result and exact application

The [integrated source reduction](../../A4D_NATIVE_COMPLETE_SOURCE_REDUCTION_2026_10_22.md)
consumes the original generated-thermal/causal source packet. It replaces
three explicit missing calculations with reusable results on their own
carriers. It does not identify the coherent READY apparatus, the original
stationary CAR16/full128 instrument, and the configured geometric 42-field
action merely because each has a source.

| New result | Concrete use in the parent argument | Preserved boundary |
|---|---|---|
| [Whole actual-cut source](CUT_SOURCE_EQUIVALENCE.md) | On the owned rank-one READY apparatus, `d(H_C+J)=R dJ`, with `34165/50549 <= R < 1`. Every admitted preparation/controller tangent is included; critical Hessian kernel and inertia are preserved. | Fixed calibration/dimension; this is the actual constructed cut heat, not a proof that default L913 is that heat. An independent input reaction survives. |
| [Native marginal maximum entropy](MAXIMUM_ENTROPY_PREPARATION.md) | The actual `rho*=Delta^-1/Tr(Delta^-1)` is the maximum-entropy state retaining its one-port moment exactly when Delta has at most two bands. On the original two-band point, the marginal gain and its entire first source vanish. | The generated dual multiplier is not the original fixed Golden temperature. Marginal entropy gain does not replace history/reference information. |
| [Complete quantum history](COMPLETE_HISTORY_SOURCE.md) | The full efficient-instrument tree supplies conditional quantum-work entropy and every preparation/probability derivative. Pinching onto all history-diagonal quantum-work tests is its unique maximum-entropy representative. | The retained algebra and physically paid preparation must be selected independently. One/two-round native diagnostics do not supply a complete geometric or infinite-time refinement theorem. |

The exact finite-tree source uses the final measured state
`Gamma=direct_sum_leaves p_w rho_w`:

\[
S(\Gamma)-S(\rho_0)=\sum_{w\;\mathrm{live}}p_w c_w,
\qquad
c_w=H(q_{\cdot|w})+\sum_bq_{b|w}S(\rho_{wb})-S(\rho_w).
\]

For the full coherent output Omega and the declared pinching E,

\[
I_{\rm gain}=S(E\Omega)-S(\Omega)
=S(\Gamma)-S(\rho_0)=D(\Omega\Vert E\Omega).
\]

The corresponding information sources are different when the input moves:
`dI_gain=dS(Gamma)-dS(rho_0)`. The proof retains preparation and capped
abort leaves, conditional quantum work, moving probabilities and genuine
input equations. It has no iid-reset premise.

## Actual original-native numerical application

The unchanged original constructor has Git blob
`ee8de4635d24c668949ac9a0186616ab7d59f2ed`. The checker loads only its six
needed definitions; it does not execute the old suite. The fixture is
`r=tanh(theta/2)=1/9`, `nu=3/5`, with the actual moving inverse-square
stationary marginal and `dtheta/dr=81/40`. Entropy uses natural logarithms.
The direction `v=partial_r-nu h_r/(2h) partial_nu` keeps the complete
one-port Born law fixed.

| Actual derivative | One round, 128 outcome slots | Two rounds, 16,384 outcome slots |
|---|---:|---:|
| `partial_r S(pointer)` | -0.0144689074544 | -0.0289378392451 |
| `partial_r S(CQ)` | -0.0302590042780 | -0.0451512597578 |
| `partial_r I_gain` | -0.0148923366769 | -0.0297845921568 |
| `D_v S(pointer)` | +0.0051885095419 | +0.0103769945369 |
| `D_v S(CQ)` | -0.0106761098945 | -0.0059854683564 |
| `D_v I_gain` | +0.0046905577066 | +0.0093811992447 |

The moving initial DATA entropy source is approximately
`-0.0153666676011` in both directions. The conditional quantum term
therefore cannot be replaced by a coarse pointer mutual-information bound.
A real retained pure DATA/reference purification instead has pure
conditional branches, giving CQ entropy equal to pointer entropy. A fixed
independent oldRIGHT128 spectator adds `log(128)` to normalized entropy
and zero to the whole source; it does not multiply that entropy by 128.

All singular values of actual Kraus amplitudes are included. There is no
positive-mode cutoff or eigenvalue clipping. Only identically zero odd
Walsh rows are omitted from numerical summation, while all physical slots
remain in the dimension. With `eta=1e-22` and a smaller `1e-24` control,

\[
0\le S-S_\eta\le D\eta,\qquad
|dS-dS_\eta|\le4\sqrt{D\eta}\,\|dA\|_{\rm HS},
\qquad D=16\cdot128^n.
\]

The largest displayed CQ source regularization bound is below
`8.37e-9`; including the initial-state bound makes the largest gain-source
bound below `8.40e-9`. Independent one-round value derivatives agree
within `2e-9`. These are bounded numerical checks with analytical
regularization bounds, not interval enclosures of floating-point error.

## Concurrent work is consumed without conflating its source conventions

[Concurrent intake](CONCURRENT_INTAKE.md) pins the independently published
stopped Cost-minus-CQ/Poisson preparation calculation and the original
sixteen-stage clock-cut theorem at
`e02855b68a1de758436b0e80c1ee98171bc5c4f4`. The former's numerical fixture
has two Kraus outcomes; the CAR16/full128 application here supplies a
different, previously missing concrete source component. Its input
cotangent transforms exactly as

\[
M_{\rm gain}=M_{\rm CQ}-(\log\rho+I)/\log\varphi.
\]

Clock-only cuts have a constant feedback source on the declared original
reversible stage machine. A variable history entropy does not bypass that
theorem. The entropy conditional expectation E and a Hilbert-space Book
active projector P_N have different types and still need their actual
physical identification.

The concurrently published [open full42 branch and continuous-source budget](../../A4D_EXACT_FULL42_OPEN_PF_COLLAR_BRANCH_AND_CONTINUOUS_BOOK_RESIDUAL_2026_10_22.md)
provides a sufficient whole-42 residual criterion at its separately
certified finite CQ root. This packet supplies no transport of these
Fourier-fixture numbers into that root's normalized coordinates and makes
no claim that its `3e-22` budget is met or violated. The older common-null
source inheritance and this newer finite off-null continuation remain
distinct applicable theorems.

## Frozen checks, independent reviews and replay

| Authored checker | Checks | Frozen receipt | Independent review |
|---|---:|---|---|
| `check_cut_source_equivalence.py` | 100 | [CUT_SOURCE_RESULT.json](CUT_SOURCE_RESULT.json) | [Cut review](CUT_SOURCE_INDEPENDENT_REVIEW.md) |
| `check_maximum_entropy_preparation.py` | 23 | [MAXIMUM_ENTROPY_RESULT.json](MAXIMUM_ENTROPY_RESULT.json) | [Maximum-entropy and synthesis review](MAXIMUM_ENTROPY_INDEPENDENT_REVIEW.md) |
| `check_complete_history_source.py` | 50 | [COMPLETE_HISTORY_RESULT.json](COMPLETE_HISTORY_RESULT.json) | [Complete-history review](COMPLETE_HISTORY_INDEPENDENT_REVIEW.md) |

All three author runs pass in ordinary and optimized Python. Independent
reviewers reproduced the frozen affected calculations without rewriting
their expected receipts. The packet has **173 scoped checks**; they are
not 173 new physical premises or acceptance flags.

The registered read-only entrypoint is:

```bash
python -B 02_REGISTRY/research/certificates/a4d_native_complete_source_reduction_check.py
```

It verifies [SOURCE_PINS.json](SOURCE_PINS.json), runs only these three
checkers, compares their exact interfaces and numerical diagnostics with
the frozen receipts, and checks that all frozen input bytes remain
unchanged. It never passes an authoring/write flag. Strings, flags,
integer counts and regularization parameters must match exactly; ordinary
float diagnostics use `2e-9` absolute plus `2e-8` relative replay tolerance.
Tiny analytical error bounds use `1e-18` absolute plus `2e-8` relative.
These replay tolerances are separate from each checker's mathematical
controls. The cut checker additionally compares its rounded receipt exactly.

The source manifest records original input commits, Git blobs and SHA256,
plus the frozen new proofs/checkers/receipts/reviews. The main memo and task
brief are navigation consumers, not mutable numerical expected output.
The three concurrent e02855 inputs are kept byte-for-byte under
`published_inputs/`, with their original `source_path` and commit in the
manifest. This preserves the precise inspected intake while the live
concurrent source files continue to evolve. Runtime native constructors
remain the actual pinned repository files; the snapshots are proof inputs,
not alternative constructor implementations.
No old geometric root, full suite, Lean build, claim promotion or lifecycle
transition is part of this replay.

Standard instrument/entropy results are used as background, not claimed as
new general quantum theory; see [Shirokov, entropy reduction of quantum
measurements](https://arxiv.org/abs/1011.3127) and [Jacobs, efficient
measurements and purification](https://arxiv.org/abs/quant-ph/0306039).
The new application and its exact scope are in the pinned repository proofs.
