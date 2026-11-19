# Independent review: complete READY cut-source equivalence

22 October 2026. Reviewer: independent `native_definitions` subagent;
the cut proof, checker and authored result were read-only inputs.
Existing scientific owner: Draft PR #334. No publication, lifecycle or
physical-GR acceptance is performed by this review.

## Verdict

**PASS for the exact stated mathematical scope.** The full paired-cut
heat plus feedback source is a uniformly positive scalar multiple of
the feedback source on every supplied smooth map into the stated
rank-one apparatus, at fixed dimensions and calibration. This includes
moving, noncommuting `P,U` and their generated preparation/controller
pullbacks. The critical Hessian and residual formulas follow with the
stated qualifications.

The reviewed theorem does **not** select this cut heat as the original
Book03 incidence heat, prove an independent preparation source vanishes,
add a CQ ledger to the bare bootstrap, or extend the configured common-null
all42 identification to a different off-null action. The proof retains
those boundaries correctly.

## Exact reviewed bytes

| Input | SHA256 |
|---|---|
| `CUT_SOURCE_EQUIVALENCE.md` | `8c75d01c5fe5f6892b129d3f51af8c9af71a7ccfff1052976bce42d647ddf0ad` |
| `check_cut_source_equivalence.py` | `01bce178bfb36422cb0703a9892ed5fd00823cd91de7bc4968f6a8b263a5eb7b` |
| `CUT_SOURCE_RESULT.json` | `82012c6a33e144a29d395be385316067593089ffdc6fc32a5dc7462a55e91ed2` |

All three hashes were checked before and after replay and were unchanged.
The checker itself verifies the three declared original-source Git blobs.

## Mathematical checks

### 1. Whole carrier and moving cut

For `C=(I-P)UP`, `rank P=1`, the active block `C* C` has sole possible
nonzero eigenvalue `f` in `[0,1]`. The ranges of `C* C` and `C C*` lie in
orthogonal active/archive subspaces. Thus `L_C=C* C+C C*` has the pair
`f,f`, with the full remaining complement harmonic, including at `f=0`.
This proves the scalar trace formula on every finite-dimensional complex
unitary/rank-one-projector pair, not only the real reflection fixture.

Consequently

```
J_f = s z/(1-z f),
H_f = -2 exp(-beta f)/(D_w-2+2 exp(-beta f)),
d(H+J) = (1+H_f/J_f) dJ.
```

The last identity is an equality of scalar differentials before pullback.
No eigenvector derivative or `dP=0` assumption is needed. The same pointwise
identity proves it for every actual admitted smooth execution map. At the
endpoints only realized tangent/one-sided variations are asserted.

### 2. Uniform positive coefficient

Writing `t=exp(-beta f)`, the inequality used in the proof is equivalent to

```
D_w-2+2t-D_w(1-z f)t
  = (D_w-2)(1-t)+D_w z f t >= 0.
```

For `D_w>=50549`, `s=128`, `z=2^-20`, this gives exactly

```
R >= 1-2/(s z D_w) >= 34165/50549 > 2/3.
```

This is an analytic all-parameter bound. Its validity is not inferred from
the checker's finite sample grid. `R<1` holds for finite positive beta and
finite work dimension; no false equality at an infinite-temperature or
infinite-dimension endpoint is used.

### 3. Critical set, Hessian and normalized source

Since `J_f>0`, the one-variable function `B=Phi(J)` is well-defined. With
`w=2 exp(-beta f)/(D_w-2+2 exp(-beta f))`, direct differentiation gives

```
w_f = -beta w(1-w),
R_f = [beta w(1-w)(1-z f)+z w]/(s z) > 0.
```

The chain rule therefore gives the displayed Hessian plus a positive
rank-at-most-one term. At criticality that term vanishes. The claimed
kernel/inertia equivalence concerns the reduced scalar functions on the
specified execution manifold or justified quotient. It is not an assertion
that every block of an independently enlarged KKT multiplier Hessian is
multiplied by R.

The covector norm estimate is immediate from positive scalar
proportionality. Dividing both sides by the same actual normalization is
legitimate, including a mesh-dependent normalization. It does not repair
a source normalization already lost by the underlying reporter.

### 4. Additional price, calibration and discrete dimensions

All explicit exceptions are correct:

```
d(B+A) = R d(J+A)+(1-R)dA,
dB = R dJ+H_beta d beta+(1-R)J_z dz,
H_beta = -log(s Z_0)/beta^2 - 2 f exp(-beta f)/(beta Z_0),
J_z = s f/(1-z f).
```

The `s` factor remains inside the absolute heat logarithm. It cannot be
dropped when beta moves. Appending one dormant base harmonic mode gives
the stated positive finite logarithmic change; changing an integer
programme size is not an infinitesimal fixed-chart variation.

The tensor spectator is assumed genuinely untouched. If the execution
couples it or the cut ceases to factor, the one-eigenvalue formula must be
rederived. This qualification is present in the reviewed proof.

### 5. Independent input reaction

For the reflection `U=I-2A`, `A^2=A`, the normalized-input real gradient
follows from `q=<psi,A psi>` and `f=4q(1-q)`:

```
grad_psi B = 8(1-2q)(J_f-w)(A-q)psi.
```

The original `q_0` lies strictly between zero and one-half, so the normal
reaction survives the added heat. The proof does not declare this sphere
direction admitted when the input is actually generated from fixed blanks.
Simultaneous conjugation of `P,U` is correctly distinguished from moving
the input against a fixed event. Fixed/generated factory registers do not
create free Euler coordinates by notation.

## Implementation and support inspection

The new Python `native_base()` reproduces the ten original Golden/H/CNOT/X
gates in the pinned JavaScript owner's order, with the same bit numbering,
full eight-dimensional forward matrix and two-bit click projector. Its
reflection is the same full `V.T @ CZ @ V`; no output column is dropped.
The old gate-compilation suite is not imported or replayed.

The numerical matrix test uses all eight base columns. It includes the
remaining `D_w-8` dormant harmonic modes analytically in its heat trace
and keeps the true `s=128` feedback multiplicity. `D_w=50549` is explicitly
the lower-dimension diagnostic for a theorem valid at every larger actual
work dimension; the checker does not claim to have numerically built the
whole original cost20 work circuit. The small matrix fixture and the
actual READY `q_0` gradient check are identified separately.

The tested matrix tangents are real skew-generator directions; the
complex-unitary theorem is analytical. The checker does not falsely
claim that four numerical paths enumerate all apparatus tangents.
The noncommuting matrix source, independent Cayley-path secant, gauge
control, Hessian composition, calibration and added-price checks are
appropriate narrow controls. Removing the harmonic complement is
explicitly rejected by a negative gain in the small-carrier control.

## Read-only replay

Python: primary runtime `3.12.14`. Commands, each without
`--write-result`:

```
python check_cut_source_equivalence.py
python -O check_cut_source_equivalence.py
```

Both passed **100 checks** and compared their computed payload with the
existing receipt. Their complete stdout was byte-identical. No reviewed
proof, checker or result bytes changed. Numerical tolerances are stated
in the checker and receipt; this is not an interval certificate.

## Synthesis review comments sent to the integrator

The root synthesis `A4D_NATIVE_COMPLETE_SOURCE_REDUCTION_2026_10_22.md`
correctly separates the READY and original sequential full128 carriers,
distinguishes marginal entropy from maximum-entropy gain, and retains
the physical selection/valuation boundary.

Two bounded edits were requested by message, without modifying the root
file in this review:

1. In Section 2, explicitly qualify the sentence saying the original
   42-equation family is inherited: the configured all42 identification
   is inherited **on the previously proved common-null source family**.
   The global statement in this packet relates `B_C` to `J_READY`; it
   does not establish a new off-null identification with another action.
2. Remove the stray `+` immediately following the Section 3
   maximum-entropy Markdown link.

These comments do not invalidate the reviewed cut theorem. The review
does not certify future edits outside the three exact hashes above or
declare the physical D0-to-GR parent complete.
