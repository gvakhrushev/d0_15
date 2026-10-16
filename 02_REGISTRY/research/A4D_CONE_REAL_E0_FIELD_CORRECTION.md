# Real E0 preparations: an actual first-field-correction obstruction

17 October 2026. Same Draft #334. Consumer: actual retained-field
elimination after [complete-experiment Ward](A4D_FULL_EXPERIMENT_WARD_AND_METRIC_DESCENT.md),
not another abstract Ward or metric selector. The same conditional H+J+R,
proper LC cone, full16 carrier, reference128 and all preparation equations remain.

**Result.** On the owned winding cone, allowing arbitrary real smooth first
coframe/link/observer/measure jets does not repair the real rank8 balanced
E0 preparation. More generally, a real momentum-diagonal E0 preparation
must have zero mask1 and14 mass on axis1 to satisfy its first amplitude
equation. For a common Fock density on all eight momenta, its support must
therefore lie in span{vacuum,top}. This is a new constraint on actual
preparation, not a choice of a source or an appeal to a generic inverse.

The surviving vacuum/top (GHZ) sector, complex preparations, inter-momentum
coherences, other leading geometries and other actual experiments are not
excluded. No physical engine preparation or full stationary branch is asserted.

## 1. Same source-balanced input, including arbitrary preparation rank

Use [the source-balanced owner](A4D_CONE_SOURCE_BALANCED_PREPARATION.md),
Sections1–7: period2pi torus, theta(y)=y, y=x2, e=s O01, fixed positive
coordinate metric G=s²I, exact proper LC links and true positive adjoint.
The continuum operator and the literal finite first jet satisfy

```text
D_p=i sum_r p_r(c_r-b_r)/s, Delta0,p=|p|² I16/s²,
Delta_h=Delta0+h A1+O(h²),
Sigma={+/-e_r:r=0,1,2,3}, P=P_Sigma, epsilon0=1/s².       (1)
```

Keep the complete first shell, with all128 preparation/reference columns.
Consider the actual leading family already known to solve every leading
metric/torsion row conditional on its scalar scale equation:

```text
rho0=(1/8)sum_r (|+e_r><+e_r|+|-e_r><-e_r|) tensor sigma_r,
sigma_r real symmetric PSD, Tr sigma_r=1,
range sigma_r subset E0=span{|0>,|1>,|14>,|15>}.           (2)
```

Reality is the actual real occupation-coordinate convention, not a
replacement of complex matter by real matter in the whole theory.
E0 here is the fixed positive **coordinate-form** orthonormal occupation
plane, after the actual coframe intertwiner U_e. It is not automatically
the same plane as literal raw/native engine E0 on a moving coframe.
The thermal metric rows are equal. The four independent constant metric
equations, together with Tr rho=1, force w_r=1/4; these weights are not
fitted to the obstruction. The more general independently supported
source-balanced density has the same weights. Formula(2) additionally
specifies momentum-diagonal density, identical density at the two signs,
and real E0 support. Those hypotheses are retained below.

Every real PSD density in(2) has a real square-root purification. Any other
purification with the same density differs by a right reference partial
isometry, extendible to a unitary on the full128 reference. The left
amplitude equation and its Frobenius norm are invariant under this right
factor. This is an algebraic change for the proof, not a declaration that
reference transformations are physically admitted gauge operations.

## 2. Actual real same-momentum part of the finite stencil correction

The [first-corrector source](A4D_CONE_PREPARATION_FIRST_CORRECTOR.md) has
the coordinate generators

```text
M0=sin(2y)E02-cos(2y)E12+E21,
M1=-cos(2y)E02-sin(2y)E12-E20,
M2=E01-E10, M3=0, H_r=Gamma(M_r).
```

Each coefficient is constant in its own edge direction. Its actual
D1 is Taylor of the proper raising word followed by its true adjoint;
it includes H_r². To extract its real same-p part, only the zero Fourier
means of the first-derivative coefficients are needed:

```text
mean H0=Gamma(E21), mean H1=-Gamma(E20),
mean H2=Gamma(R01), mean H3=0,
Q_r=c_r mean(H_r)-mean(H_r)* b_r,
Re(A1)_(p,p)=-{gamma_r,Q_r}/s² for p=+/-e_r.             (3)
```

Here gamma_r=c_r-b_r. The remaining real D1 multiplication/second-
derivative coefficients give purely imaginary terms when anticommuted
with D_p. They have not been dropped from A1 or from its amplitude
equation; (3) extracts just a necessary real component.

The full16 CAR calculation yields, for BOTH momentum signs,

```text
Re(A1)_(p,p)=(B12,-B02,0,0)_r/s²,
B12=c1 b2+c2 b1, B02=c0 b2+c2 b0.                       (4)
```

No 128-by-128 eigenspectrum is recomputed. Equation(4) is verified directly
against all eight actual same-p blocks extracted from the frozen D0/D1
definitions. In literal ACDB occupation coordinates,

```text
B02|1>=|4>, B02|14>=|11>, B02|0>=B02|15>=0,
P_E0 B02 P_E0=0,
E0* B02(I-P_E0)B02 E0=diag(0,1,1,0).                    (5)
```

Also B12 E0=0. Thus the decisive real leakage is specifically axis1,
not a spurious requirement that all four sigma_r be the same.

## 3. Why no real first field jet can cancel it

Write the full smooth first geometric jet as v. The genuine first
preparation equation, including an arbitrary full reference correction C1,
is

```text
(Delta0-epsilon0)C1+(A1+delta_v Delta0-epsilon1)C0=0.
```

Projection to the first shell eliminates the C1 term exactly. Its signed
off-shell solution `Q C1=-Q(Delta0-epsilon0)^-1 Q(A1+delta_v Delta0)C0`, when compatible,
does not alter this shell equation. Ground modes remain in that resolvent.

At a fixed same momentum p, every real native field jet contributes only

```text
(delta_v Delta0)_(p,p)=a_p I16+i K_p,
a_p real, K_p real antisymmetric.                       (6)
```

This is an image containment, not an assumption of arbitrary independent
Hermitian delta Delta. Constant metric means give the scalar part; all24
real torsion/connection means have real symmetric delta D and therefore
pure imaginary antisymmetric {D_p,delta D}. A constant measure-whitening
generator commutes with the raising operator. A true changing coordinate/
positive-frame identification has resonant commutator [K,Delta0] equal0.
Nonconstant jets contribute only their zero Fourier means to this diagonal
block. These facts are the complete real field interface established in
the linked source-balanced owner, not a restriction to old SO3 links.

Choose the real block square-root C0 of(2) for the proof. Its reference
columns for different momenta are independent. In the output momentum
p=+/-e1 and the corresponding input-reference columns, project the
real part of the shell equation further to E0-perp. Scalar a_p and
epsilon1 act inside E0, while iK_p C0 is purely imaginary. Equations(4)–(6)
therefore force

```text
B02 sqrt(sigma_1)=0,
range sigma_1 subset ker(B02) intersect E0
                         =span{|0>,|15>}.              (7)
```

The same conclusion follows for every purification of that real density.
Positivity is essential: `Tr sigma_1 B02²=0` implies
`B02 sqrt(sigma_1)=0`. A scalar epsilon1, a radial normalization term,
reference mixing or a freely chosen off-shell correction cannot remove(7).

For independently varying sigma_r, only sigma_1 is forced into this
kernel by this calculation. For a COMMON real sigma at all momenta,
sigma itself must have vacuum/top support. No stronger conclusion about
other sigma_r or arbitrary momentum coherences follows from a diagonal-
reference-column argument.

## 4. A positive residual on the actual balanced rank8 input

For any real density in(2), and any real v,epsilon1, the full projected
amplitude residual obeys the exact lower bound

```text
||P(A1+delta_v Delta0-epsilon1)C0||_HS²
 >= [sigma_1(1,1)+sigma_1(14,14)]/(4s^4).              (8)
```

Both signs of axis1 carry weight1/8. Real E0-perp projection is an
orthogonal contraction in the underlying real Hilbert space, so discarding
all other output blocks only lowers the squared norm. This proves(8)
without minimising over, or solving, the remaining imaginary field rows.

In particular the previously constructed balanced E0 vector
`chi_bal=(|0>+|1>+|14>+|15>)/2` has leakage mass1/2. Keeping its full
rank8 purification and reference128,

```text
rho0=(P_Sigma/8) tensor chi_bal chi_bal*,
||projected first eigen-equation residual||²>=1/(8s^4),
||projected normalized amplitude Euler coefficient||²>=1/(2s^4). (9)
```

The last line uses the actual factor2 in `2(Delta-R)C`; the first bound
is for the eigen-equation itself. Consequently lowering preparation rank
from128 to this balanced8 does not restore the first corrector, even after
arbitrary real first coframe/link/observer/measure corrections.

A common real coordinate-form E0 seed with nonzero mask1 mass is likewise
excluded on this particular cone/first-shell family. An actual raw engine
input is covered only if its full native-to-form encoding is proved to
land in(2). For a moving O01(theta(y)), Lambda(O^T eta) can rotate its
first-grade direction, mix E0 and introduce momentum coherences; that
encoding cannot be replaced by an identity. No such global engine/form
identification or ring admission is inferred here. The proof does not
assert that every preparation in the full native experiment is
momentum-diagonal, real, or constrained by an engine slot.

## 5. The surviving branch and the actual next equation

The common real GHZ plane span{vacuum,top} survives the NEW real leakage
test. For example `(vacuum+top)/sqrt2` has B02 chi=0. This does not solve
its imaginary same-p rows, nonzero-q rows, first field equations, scalar
scale equation or next preparation equation. It also has zero first-grade
slot and is not thereby an admitted input of the old engine.

The immediate constructive consumer is therefore the full remaining
projected first equation on this two-dimensional support, together with
the actual linearized field equations and their signed off-shell source.
Alternatively an owned complex/momentum-coherent preparation or a different
leading geometry must be supplied explicitly. No new action or compensating
stress is defined by subtracting this residual from an Einstein tensor.

Unlike a generic hypothesis r_*(g) in a Ward/Schur theorem, this computation
tests an actual candidate retained preparation. In particular it prevents
claiming a smooth metric-neighborhood elimination using chi_bal here.
The Ward identity, the fine-history causal readout and the separate
history-to-action mapping remain intact; none solves this amplitude row.

## 6. Exact evidence

[The new helper](sources/d0_cone_real_e0_field_correction_2026-10-17/check_real_e0_field_correction.py)
executes only the pinned creator/connection/D0/D1 construction prefix,
stopping before any old assemble(), spectrum or run(). It checks the eight
same-p blocks, all10 real metric and24 torsion means, full E0 leakage,
full128-reference rank8 normalization, source-balanced weights and bounds.
It also checks the GHZ survivor to reject a false all-partial-rank no-go.
Normal/-O outputs and source identities are preserved beside it. No old
spectral checks or Lean targets are replayed.
