# Existing golden/registration words read retained real coherences

17 October 2026. Same Draft #334. Consumer: the physical readout/cut arrow
after the complete native history/source calculation. This is a constructive
test-generation theorem for a precisely placed existing word, not a choice of
Info, a free coherent detector, a new action or an all-POVM assertion.

## 1. Exact owned primitives and the one application premise

The basis order of
[`GoldenCoherentMemory.fullStep`](../../03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean)
is `(active,record)=00,01,10,11`. The existing gate and registration are

```text
G=[[a,-p],[p,a]], a²=p, p+p²=1, p>0,
C(A,R)=(A,R XOR A),
fullStep=C(G tensor I).
```

These are the literal definitions in
[`GoldenOrderInterferometer.gate`](../../03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean)
and [`FiniteProtocolClock.register`](../../03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean).
Registration is a complete involutive permutation, not cloning of an unknown
superposition. Their complete action on nonblank records is defined, not just
their two blank-input columns.

Let the old complete tape be R=(Z/2Z)^r, r=7n for n original128-output rounds,
and let A be one independently initialized blank active port. For each bit j,
the **application premise** is permission to address that old coordinate by
the same registration C_j, with A as control and old R_j as target. This is
not inferred from the gate's matrix definition, a passive change of role names,
or the physical availability of registration into a fresh blank.

For t in R put X_t|omega>=|omega+t> and
C_t=product_(j:t_j=1) C_j. The C_j commute and give
C_t=diag(I_R,X_t) in the active basis. Thus no arbitrary Boolean gate is
needed. The finite word uses exactly 2+Hamming(t) forward primitives:

```text
V_t=(G tensor I) C_t (G tensor I).                       (1)
```

Its length is at most 2+7n. With the full pointer output, at most
128^n-1 nonzero-t settings supply the 128^n(128^n-1)/2 distinct pair
probabilities. This is exponentially many scalar entries/settings in n,
not a uniform refinement resource budget or a free full-state reconstruction.

No inverse, SWAP, reset, discarded failure or selected new angle occurs.
The complete operation is orthogonal on all inputs and correlations. It may
change the old basis labels; it retains their information in the full joint
state. It is not an assertion that the old labels remain immutable.

## 2. Actual Kraus amplitudes and every outcome

Applying (1) to |0> tensor psi gives

```text
V_t(|0> tensor psi)=|0> tensor K0 psi+|1> tensor K1 psi,
K0=p I-p² X_t, K1=ap(I+X_t),
K0* K0+K1* K1=I,
K1* K1=2p³(I+X_t).                                      (2)
```

The identities use only X_t*=X_t, X_t²=I and the golden relation. A final
active pointer therefore reads q1=2p³[1+Tr(rho_R X_t)]. Already for one old
bit, |+><+| and I/2 have the same old pointer distribution but give q1=4p³
and q1=2p³. The old translation-charge invariant does not forbid this test:
V_t commutes with each old translation, while the measured output effect
can read that conserved charge.

Retain the old pointer output as well. With P_i=|i><i| and j=i+t, the joint
outcome (active1,old i) has the positive effect

```text
E_ij=K1* P_i K1
    =p³[P_i+P_j+|i><j|+|j><i|], i!=j.                  (3)
```

All active/old outcomes together sum to I. Equation (3) is an outcome of
this complete experiment, not postselection installed as dynamics. The old
output i is the label **after** the test; (3) is not a passive event in the
unchanged original prefix tree.

## 3. All real symmetric matrix units, with an explicit source inverse

The original old-pointer cut supplies d_i=Tr(rho_R P_i). Equation (3) gives

```text
q_ij=p³[d_i+d_j+2 Re(rho_ij)],
Re(rho_ij)=q_ij/(2p³)-(d_i+d_j)/2.                       (4)
```

Every distinct pair i,j has the unique nonzero t=i+j. Therefore (3),(4)
prove, at every finite tape size, that the real linear span of these
executed positive effects and P_i is Sym_R(128^n). There is no sampled rank
argument. They separate all real symmetric densities and tangents. They do
not assert that every positive element of this span, or every POVM, is one
executable test: linear combinations in (4) may have negative coefficients,
and different pairs are different experiments with their own resources.

For any real symmetric tangent S, including preparation/field tangents when
the ACTUAL tape family is real, the left inverse is

```text
S_ii=dot d_i,
S_ij=dot q_ij/(2p³)-(dot d_i+dot d_j)/2.                (5)
```

For general complex tape families (5) reconstructs only Re S. Reality of
every admitted preparation and tangent is not asserted.

For a fixed real symmetric covector A the dual identity is

```text
Tr(A S)=sum_i[A_ii-sum_(j!=i) A_ij] dot d_i
                         +p^-3 sum_(i<j) A_ij dot q_ij. (6)
```

This reconstructs a source of a supplied real record functional from actual
test derivatives; it does not select that functional or identify it with
Einstein gravity. If A moves, include Tr(rho_R dot A). If the physically
placed primitives or output projectors move, include their actual dot E.

For an unnormalized positive record operator R and N=Tr R>0,

```text
rho_R=R/N,
dot q=Tr(E dot R)/N+Tr(dot E R)/N-q dot N/N.             (7)
```

In this fixed-p, fixed-label test dot E=0. The normalizer subtraction is
essential; (5) acts on dot rho_R, not on dot R/N with its radial part left
in. This state normalization is not automatically the raw Book/history
partition normalizer: the latter still needs its own binding.

## 4. Exact limits of the result

All these word matrices, blank-port preparations and pointer effects are
real in the stated tensor-bit basis. Thus the family reads Re rho_R, not
arbitrary imaginary coherences. For example (I+Y)/2 and I/2 give the same
probabilities for every real symmetric effect, although their purities are
1 and1/2. A further quadrature role/phase operation, or a proved real-state
preparation restriction, would be a separate premise. An algebraic complex
span is not physical access to complex POVMs or to maximal information gain.

The [literal v8 programme](sources/d0_record_generated_heat_v8_2026-10-14/RESULT.md),
§§2–3, explicitly has coherent Q and Q* **inside the current round** and
fresh workspace at each later round. Its existing schedule does not retarget
completed old tape bits. More generally, append-only operations or arbitrary
prefix controls sum_i P_i tensor U_i, with pointer-diagonal terminal tests,
pull back to pointer-diagonal old effects. This is an exact word-closure
fact. C_j on an old target leaves that class because it does not commute
with the old P_i; prefix control alone cannot supply its placement.

The [retained-admission owner](A4D_NATIVE_RETAINED_RECORD_ADMISSION.md), §1,
already includes old-target C_f in its explicitly supplied one-way class.
Hence that class must not be renamed a pointer-only test class. Its all-word
translation-charge preparation obstruction remains valid: a conserved
observable may be measured without being changed. The restricted
[closed executor](certificates/a4d_native_closed_record_engine.py) takes only
its current full16 matter and expressly distinguishes its predecessor
decoder from physical inverse access; it has no full128 tape-test decoder.

The remaining physical splice is specific: admit the same active-to-old-bit
registration placements and the joint output cut, with their preparation,
internal schedule and complete cost. This adds a real test programme; it
cannot be charged zero cost or silently identified with the unextended
fixed128 round. Matrix test generation does not choose pointer likelihood,
coherent entropy, complete-maximal-gain Info or physical admission. No
all-ten source identity, action/refinement terminal or GR closure follows.

## 5. Bounded verification

[`check_readout_splice.py`](sources/d0_retained_history_readout_2026-10-17/check_readout_splice.py)
pins the three literal Lean definitions and v8 resource/schedule owner by
SHA256, reads definitions only and imports no old certificate. Its symbolic
involution proof supplies the all-size identity; the full four-coordinate
check binds it to actual fullStep and register ordering. Matrix-unit and
source identities, moving normalization and hostile dephasing/imaginary
controls are exact over Q(a), a^4+a²=1. No Lean or old suite is run.
The separate [results](sources/d0_retained_history_readout_2026-10-17/RESULTS.json)
and [validation](sources/d0_retained_history_readout_2026-10-17/VALIDATION.json)
record the new ordinary/optimized comparison and exact inputs.
