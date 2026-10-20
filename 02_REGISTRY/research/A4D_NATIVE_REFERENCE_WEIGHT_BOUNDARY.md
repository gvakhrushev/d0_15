# Native reference weights: coefficient, frame and range classification

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft #310.
Input: `75527846bf3603a1c51acf445f8354e3254341be`.
CONTROL/main baseline: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Status: **a complete obstruction for the stated existing weight family**, plus
an exact kernel/range classification at one nondegenerate constant coframe.
Positive GR and global closure remain OPEN; this is a research intake.

The owner `A4DLocatedMatterCellEnergy` already defines

    W_c(e) = I + H(e) + c M_q(e),
    q_empty(x) = sum_(r,a) e_r^a(x)^2,
    q_S(x) = sum_(r in S,a) e_r^a(x)^2 for S nonempty.          (1)

This family depends on metric-shape data omitted by volume-only models.
It is therefore tested directly, not assigned to the volume-fiber no-go.
The owner itself calls these supplied reference weights, explicitly not a
metric star or Lorentz-covariant stress. Its two named examples are c=1,2;
no coefficient-selection theorem or independent action is supplied there.

We prove that **no c, nor any mesh-dependent sequence c_h, makes this family
descend under the existing raw Lorentz action and exterior field action**.
The sharp two-probe scalar defect is at least 5/86. In addition, c=1 and c=2
have different kernels and uniform-inverse behavior, despite the same flat
value and complete first coframe jet. This is an operator result; no new
native action or physical on-shell gate is introduced by calling W_c psi=0
an algebraic kernel equation.

## 1. Literal scalar reduction and field action

Use the actual site carrier `(ZMod L)^Role`, L=N+2, Fock labels and counting
pairing. All CAR bilinears c_s^dagger c_r annihilate the empty Fock label,
even when its scalar amplitude varies with the site. Both forward and
adjoint ordered flux terms vanish on this sector. The owned link term gives

    (W_c(e) f)_empty(x)
      = f(x)
        + 1/2 sum_r [ e_r^r(x) f(x+r) + e_r^r(x-r) f(x-r) ]
        + c sum_(r,a) e_r^a(x)^2 f(x).                        (2)

All non-scalar output components are zero. This identity is compiled for
every N and every site-dependent e,f, not just on constant fixtures.
For e independent of the site and f=1 it becomes

    F_c(e) = 1 + tr(e) + c ||e||_F^2.                         (3)

The [Lean capsule](certificates/a4d_native_reference_weight.lean) binds the
actual scalar occupation vector to the unit of the actual exterior algebra:
`archiveFockExteriorBasis fockVacuumState = 1`. It then proves that the owned
`archiveExteriorFrameLift` fixes that vector for **every** linear frame
equivalence. This rules out a mistaken scalar transformation as an explanation
of the defects below. The test works for both an endomorphism intertwiner
and a contragredient weight/pairing law: each would preserve the scalar
matrix element. No spinor transformation is substituted for the owned
exterior representation.

## 2. All-coefficient raw Lorentz obstruction

Write eta=diag(1,-1,-1,-1), Theta=eta+e, and use the actual right action

    Theta' = Theta Lambda,      e' = Theta Lambda - eta.

The raw metric is g=Theta eta Theta^T. The proper, time-oriented rational
A/B boost is

    Lambda_AB = [[5/4,3/4],[3/4,5/4]],

with the identity on C,D. It satisfies Lambda eta Lambda^T=eta and det=1.
The capsule binds this transformation to `rawFullSolderFrameAction`, proves
`IsRoleLorentz Lambda`, and uses the actual owner to prove Gram invariance.

Two constant, nondegenerate raw solders give:

| perturbation e | det(eta+e) | F_c(e) | F_c(e') | defect |
|---|---:|---:|---:|---:|
| 0 | -1 | 1 | 1+5c/4 | 5c/4 |
| diag(0,-1,0,0) | -2 | c | 41c/8-1/4 | 33c/8-1/4 |

Both before/after metrics are identical within their rows. Scalar invariance
on the first row forces c=0, while the second then has defect -1/4. Thus no
coefficient works on the whole stated class. These are nondegenerate inputs,
not an argument using empty physical fibers or singular Gram matrices.

Let D0=5c/4 and D1=33c/8-1/4. Their exact identity

    D1 - (33/10) D0 = -1/4

implies

    max(|D0|,|D1|) >= 5/86.                                  (4)

Equality holds at c=2/43. The capsule proves the actual two-readout version
of (4), not a bound for unrelated placeholder variables. Since normalized
site averaging leaves these constant scalar values unchanged, the bound
holds at every L, including L in 4N. Allowing c=c_h does not help. Endpoint
readout errors O(h) change the maximum defect by at most O(h), so cannot
restore asymptotic frame descent. A fixed nonzero overall calibration also
cannot turn this positive bound into zero. This is a weight/readout
obstruction, not a separately proved gravitational action-contrast theorem.

### The obstruction also occurs arbitrarily near the flat coframe

Let e_delta=diag(0,-delta,0,0). For the exact rational boost

    a=(1+t^2)/(1-t^2), b=2t/(1-t^2), 0<|t|<1,

replace 5/4,3/4 by a,b. Direct substitution into the same owner reduction gives

    F_c(e_delta') - F_c(e_delta)
      = (a-1) [ -delta
          + 2c { a(delta^2+2delta+2) + delta^2+delta } ].       (5)

At delta=0 it is 4ca(a-1), forcing c=0 for invariance even on arbitrarily
small boost neighborhoods. At c=0 it is -delta(a-1), nonzero for every
small delta!=0. All states can approach e=0 while retaining nondegenerate
raw Gram. The failure is therefore not confined to the larger second row
of the rational table.

Nor is it an artifact of allowing a singular or negative reference weight.
At each fixed finite stage W_c(0)=I and W_c varies polynomially with e;
self-adjointness follows from owned H self-adjointness and the real diagonal
M_q. Hence a sufficiently small coframe neighborhood has strictly positive
W_c for each fixed c. Choose the small t,delta above inside that neighborhood.
This local positivity argument does not claim a new uniform physical
constitutive bound or a selected coefficient.

## 3. Why a ten-component metric covector cannot repair the defect

For constant scalar input the full coframe derivative of (3) is

    K_c(e) = I + 2c e.                                       (6)

This is the derivative of an operator readout, **not** a derived matter
stress tensor. If the readout were a function of g alone, this covector
would annihilate every raw Lorentz direction dTheta=Theta X with
X eta+eta X^T=0. Equivalently there would be a symmetric metric covector T
with K_c=2T Theta eta, using the Frobenius pairing and all ten packed metric
components, including their off-diagonal factor two.

Take the infinitesimal A/B boost X_AB=X_BA=1. At the boosted first table row,
<K_c,Theta X>=9c/2. At the boosted second row it is 57c/4-3/4. No constant c
makes both zero. The exact certificate computes all ten rows of the Gram
Jacobian at the relevant states. It has rank 10; adjoining the attempted
coframe covector to its transpose raises the rank to 11 for c=1,2 at the
first boosted row and c=0 at the second. Thus fitting ten metric-source
components cannot erase the vertical response. Discarding that response
would require a different action/readout or a restriction with its own owner.

## 4. Exact coefficient-dependent kernel and range

At the fixed constant coframe e_*=-I/2, the raw solder is

    Theta_* = diag(1/2,-3/2,-3/2,-3/2),
    g_* = diag(1/4,-9/4,-9/4,-9/4), det Theta_*=-27/16.

This is a nondegenerate flat metric. The capsule proves

    F_c(e_*)=c-1,
    W_1(e_*) scalar(1)=0,
    W_2(e_*) scalar(1)=scalar(1)!=0,
    F_1(e_*+t v)=t^2 ||v||_F^2.                              (7)

The last identity says that this scalar readout's first coframe variation
vanishes in all 16 directions. It does not declare (7) an on-shell solution
of a native gravitational action. The kernel has W_1 singular, so it must
not be inserted into a class requiring a strictly positive weight.

For arbitrary scalar f, the compiled literal formula is

    W_c(e_*) f = (c-1) f + (1/4) sum_r (2f-U_r f-U_r^-1 f).   (8)

To classify the entire operator, use the finite Fourier basis at momenta
p_r=2pi n_r/L and the actual A,B,C,D order. For S nonempty, k=|S|, the diagonal
coframe makes every off-diagonal CAR coefficient zero and q_S=k/4. Literal
ordered shift/average substitution gives the full 16-sector symbols

    lambda_empty(p) = c-1 + 1/2 sum_r (1-cos p_r),
    lambda_S(p) = k-1 + ck/4
                      + 1/2 sum_(r not in S) (1-cos p_r).     (9)

These formulae follow algebraically from the definitions, for all L.
The certificate checks every Laurent block symbolically before doing finite
controls, rather than inferring the formula from a numerical spectrum.

Fourier completeness here is finite algebra: the geometric-sum identity
`L^(-1) sum_(j=0)^(L-1) exp(2pi i j(n-m)/L)=1_[n=m mod L]`
makes the character matrix unitary. Its fourfold tensor covers every site
amplitude, so (9) lists the whole spectrum, not a selected subspace.

Consequences of 1-cos p>=0 and this completeness:

* c>1: W_c(e_*) is strictly positive at every stage, with sharp lower bound
  min(c-1,c/4). In particular W_2>=I/2 and its inverse norm is at most 2,
  independently of L.
* c=1: W_1 is positive semidefinite. Its entire kernel is the single constant
  scalar mode. Every nonempty sector has lower bound at least 1/4.
* On the orthogonal complement of that one kernel at c=1, the sharp gap is
  min(1/4, sin^2(pi/L)). The unscaled inverse norm therefore grows as
  L^2/pi^2. Removing the exact kernel does not give a uniform inverse.
* c<1: the constant scalar has negative eigenvalue c-1, so strict positivity
  is impossible at this coframe. No classification of every other zero of
  an indefinite c<1 operator is asserted.

The scalar kernel cannot be called local Lorentz gauge: the owned exterior
frame action fixes it, and an invertible frame action cannot send a nonzero
field to zero. Equation (8) is a positive counting Laplacian over **all four**
Role directions. It is not a Lorentzian wave equation, causal-time result,
or the physical 24-row connection linearization. Scaling its scalar part
by L^2 changes the operator being estimated; no physical normalization is
silently substituted into the unscaled bound.

Thus the two existing coefficients have different operator/kernel behavior,
not merely different names for one identical equation. Neither is selected
as physical, and the Lorentz obstruction in Section 2 applies to both.

## 5. Evidence and placement in the closure path

The [capsule](certificates/a4d_native_reference_weight.lean) compiles seventeen
propositions, including actual scalar/exterior-unit binding, with 56 transitive
D0 source pins. Its printed axioms are propext, Classical.choice and Quot.sound;
there is no sorryAx. [Output](certificates/a4d_native_reference_weight_output.txt)
and [receipt](certificates/a4d_native_reference_weight_results.json) preserve
actual compilation, source and toolchain hashes.

The [checker](certificates/a4d_native_reference_weight_check.py) and
[immutable ledger](certificates/a4d_native_reference_weight_certificate.json)
contain 40 exact grouped controls: all scalar coframe derivative slots,
all 16 CAR/Laurent blocks, raw Gram invariance, proper-frame and actual
exterior controls, all ten Gram rows and impossible metric-covector fits,
the small-boost identity, sharp frame gap, and independent real-space
matrices for all 16 sectors at L=2. Selected exact Fourier-mode controls
include L=4,8,12. Infinite-size and inverse claims use (9), not extrapolated
ranks. Immutable replay must reject a changed frame-gap ledger.

```sh
python3 02_REGISTRY/research/certificates/a4d_native_reference_weight_check.py
```

This closes the declared standalone reference-weight family as a physical
raw-Lorentz constitutive realization. Additional native terms, moving pairings,
other field representations, constraints or readouts that change the necessary
scalar test are outside the class; none is supplied here as a repair. The
first positive GR arrow still requires an independently owned physical
state/action/variation map and compatible refinement, followed by native
source/Ward, actual curved joint solutions, soundness and recovery. The
original #310 fixed-source raw terminal and #202/#317 remain separate.
