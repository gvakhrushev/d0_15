# Native two-tick evolution: complete regular field-readout boundary

Date: 2026-10-08. Source input: `ad2e43f4eae418d6fe7386d37c7ee4c76400ed42`,
existing research PR #310. Supported D0 tree:
`fd8dfc359d23c9bd79ca23eeed7c045ce9c68c6b`.

**Result:** the owned two-tick evolution has a completely classified linear
readout into the existing common-parent transfer family. Such a readout
reaches only the kernel of the spatial operator. Every differentiable
nonlinear readout obeying the same dynamics has this restriction on its
derivative at the native fixed state. An exact error identity gives the
corresponding quantitative obstruction to a uniformly regular approximate
readout. This resolves the proposed *direct time-evolution preparation*
route, at the precise scope below. It does not close G0 or establish a
no-go for every D0 preparation.

No new physical action, selector, lift or equation is installed. The common
generator was already constructed in
[A-PARENT](APARENT_FINITE_GRAVITY_COMMON_ACTION_SELECTOR.md); constructing it
again would not derive its spatial coefficients. Here the new question is
whether the already fixed native evolution can actually induce that
generator's dynamics through a field readout.

## 1. Primary definitions and the comparison being tested

| Input | Actual data used | Interpretation not supplied by the input |
|---|---|---|
| `D0/Dynamics/ToralAutomorphism.lean` | `T = [[0,1],[1,-1]]` | No field-dependent spatial coupling |
| `D0/Core/FixedDetectorTimeLadder.lean` | `TimeState = Fin 2 -> Int`, `evolveState n = T^n` | No differentiable preparation of coframe/link/matter fields |
| `D0/Dynamics/TwoTickSymplectic.lean` | `updateQ=q-p`, `updateP=-q+2p`, actual symplectic and generating relations | A 2D symplectic form is not a physical spacetime signature or a 4D action |
| `APARENT_FINITE_GRAVITY_COMMON_ACTION_SELECTOR.md` | Common finite generator and transfer `M_A` for supplied self-adjoint `A` | Existence of the generator does not select `A` or identify it with a native readout |

The first three paths are under `03_FORMALIZATION/`. The compiled capsule
binds the real formulas directly to both the actual rational update and the
actual integer `evolveState 2`; it does not rely on a matching comment or
theorem name. It proves these bindings by reducing the definitions, without
using the old `native_decide` proof of the matrix entries.

Let E and F be real vector spaces. The comparison class is explicitly

```
B(q,p) = (q-p, -q+2p),                  (q,p) in E x E,
M_A(h,k) = (h-k, (-I+A)h+(2I-A)k),      A : F -> F linear.
```

For the actual native state, E=R is the stated real extension of Z².
Taking E=R^m permits any number of synchronously evolving copies as a
mathematical comparison class; the core is not claimed to select those
copies or their independent physical variations. The exact linear
classification does not require A to be self-adjoint, invertible, positive
or diagonalizable. Self-adjointness is needed only when interpreting A
through the existing quadratic common generator.

A fixed readout P intertwines the dynamics when `M_A P = P B`. A nonlinear
readout f obeys `f(Bz)=M_A f(z)`. These are substantive hypotheses on a
proposed bridge, not consequences of verification or definitions of a
native on-shell gate. Spatial archive refinement is a different operation.

## 2. Complete classification of every linear readout

**Theorem.** For every linear P:E²->F²,

```
M_A P = P B
  iff
P(q,p) = (Uq+Vp, Vq+(U-V)p),   AU=AV=0,
```

for uniquely determined linear U,V:E->F. Consequently

```
range P is contained in ker A x ker A;
A injective                => P=0;
P surjective               => A=0;
dim {all such P} = 2 dim(E) dim(ker A)   in finite dimensions.
```

Proof. Set `D_A=diag(A,A)`. Direct multiplication gives

```
B²-3B+I=0,
M_A²-3M_A+I = -D_A M_A,
B^-1(q,p)=(2q+p,q+p),
M_A^-1(h,k)=((2I-A)h+k,(I-A)h+k).
```

Intertwining and the first two identities give `D_A M_A P=0`. The
surjectivity of B and `M_A P=P B` give `D_A P=0`. On this image M_A is
exactly B acting on F². Write P in four blocks. Commuting with B says that
its lower-left block equals its upper-right block V, and its lower-right
block equals U-V, where U is its upper-left block. Conversely these blocks
commute, and AU=AV=0 removes every A term. Both implications and the kernel,
injective and surjective consequences are compiled for arbitrary modules.
Uniqueness of U,V follows by reading the first output on `(q,0)` and `(0,p)`;
the finite-dimensional count then follows from Hom(E,ker A)².

There is no quotient by `ker A` in this argument. Every kernel direction
survives. It is not declared gauge, nor discarded because it lacks a
spatial response. Singular and nondiagonalizable A are included.

Finite consistent time-delay windows do not help a *linear* readout:
`z -> (z,Bz,...,B^r z)` is an invariant linear embedding, and its induced
evolution still satisfies the same quadratic polynomial. Independent
feedback variables with another evolution law are outside this statement.

## 3. Nonlinear preparations: the actual derivative theorem

Let E,F be normed real spaces, A continuous linear, f:E²->F² differentiable
at zero, and `f(Bz)=M_A f(z)`. Zero is the native fixed state. No assumption
`f(0)=0` is required: the intertwining equation itself makes f(0) a target
fixed state. The chain rule yields

```
P B = M_A P,     P=Df(0).
```

The previous theorem applies. Hence `A(Pv)_h=A(Pv)_k=0` for every v;
a surjective Df(0) forces A=0. With injective A, the complete first
derivative vanishes. This is compiled with actual `HasFDerivAt` and the
chain rule; the first-jet intertwining equation is not inserted as a
hypothesis of the nonlinear theorem.

An O(|z|²) modification of a forbidden nonzero first jet cannot repair this
equation. The result concerns regular variations at the native fixed state.
It does not require a flat physical metric, but neither does it identify
f(0) with a physically admitted background or turn every target coordinate
into a metric probe. Such identifications require their own owners.

## 4. Exact quantitative identity and the uniformity needed

For any linear P define its actual defect `E_P=M_A P-P B`. There is an exact
identity, compiled in the capsule:

```
D_A P = -E_P + M_A^-1 E_P B^-1.                         (1)
```

To verify it, expand the right side and use
`B+B^-1=3I`, `M_A+M_A^-1=3I-D_A`. No smallness, rank or inverse bound is
assumed in (1). For compatible operator norms this implies

```
||D_A P|| <= (1+||M_A^-1|| ||B^-1||) ||E_P||.           (2)
```

Suppose additionally `||D_A y|| >= sigma ||y||` on the target space with
sigma>0, and P has a right inverse R with `||R||<=C_R`. On a nonzero target
space, `1<=||P|| C_R` and `sigma||P||<=||D_A P||`, so

```
||E_P|| >= sigma / [C_R(1+||M_A^-1|| ||B^-1||)].        (3)
```

The norm consequences are analytic corollaries of (1), not printed as
already compiled limit theorems. Thus a uniformly conditioned right
inverse and a uniformly separated coupled mode are incompatible with a
vanishing intertwining defect. For self-adjoint A the same argument may
be applied after projecting onto an invariant nonzero spectral sector;
its kernel remains untouched. Bounds on a growing full operator are not
silently inferred from a bound on one sector.

Concrete rational control: E=F=R, A=2I, pair maximum norm. Then
`||B^-1||=3`, `||M_2^-1||=2`, and sigma=2, giving
`||E_P||>=2/(7 C_R)`. These constants do not involve an asymptotic mesh.
Conversely `A_h=hI`, P=I has defect O(h): its spatial gap tends to zero,
so it is a counterexample to dropping the uniform sigma premise.

For an approximate nonlinear intertwining relation, E_P is minus the
derivative of its residual at zero. A small residual in values alone is
insufficient: `r_h(x)=h sin(x/h)` tends uniformly to zero, while
`r_h'(0)=1`. No native metric-action contrast estimate is inferred from
(2); that remains a different map and norm.

## 5. Necessary-hypothesis controls

* A=0 admits the identity readout and all U,V of Section 2.
* A with a nontrivial kernel admits all the stated nonzero kernel readouts,
  including for a nondiagonalizable nilpotent A. These are not removed.
* The nonconstant polynomial `f(q,p)=(q²-qp-p²,0)` intertwines B with
  M_1. Its derivative at zero is zero. The exact intertwining and
  nonconstancy are compiled. Thus injectivity of A does not force the
  entire nonlinear map to be constant.
* Even the strictly elliptic M_2 admits smooth nonlinear factors away
  from the native fixed state. This analytic control excludes a global
  nonlinear no-go: in real eigen-coordinates B(u,v)=(lambda u,lambda^-1 v),
  lambda=(3+sqrt(5))/2, choose a nonzero smooth chi supported in (1,2) and set
  `f(u,v)=chi(uv) w(log|u|/log lambda)` for u!=0, zero for u=0. Here
  `w(t)=(cos(pi t/3)+sin(pi t/3)/sqrt(3),2sin(pi t/3)/sqrt(3))`
  satisfies `w(t+1)=M_2 w(t)`. The support condition makes f identically
  zero in a neighborhood of every axis point, so it extends smoothly and
  has zero first jet at the origin. It is nonconstant. No such map is
  adopted as a native physical preparation.
* Equality of the characteristic traces, symplecticity, and existence of
  a generating function are weaker than the actual full intertwining
  relation. The existing common generator's coefficients remain supplied.

The source is the real extension of the **integer** time state. A smooth
readout of this extension is an explicit comparison assumption. The core's
bare integer state type does not itself possess these continuous variations.
Arbitrary readings on discrete time orbits, time-dependent readings,
singular encodings, preparations based away from the fixed state, independent
history/memory dynamics, another carrier, and limits using a different
physical observable are not exhausted here.

## 6. What this changes in the G0 proof

The native time operator cannot be used as a shortcut from the existing
common generator to a regularly prepared coupled field dynamics in this
class. The complete linear family is now known, the nonlinear first-jet
consequence is derived, and the uniform approximation boundary is explicit.
In particular, appending a higher-order preparation correction or a finite
linear time-delay record does not produce the missing coupled directions.

The next substantive object remains an independently owned *coupled*
history/state evolution and its field-action/variation/refinement binding.
It must actually use state components or a preparation outside the proved
class and derive their laws. Merely choosing one spatial A in the already
available common generator would add precisely the missing physical input.
No external-model assignment or waiting dependency is created: this is
continuing research in the existing execution.

G0, source/Ward, quantitative metric contrast, joint curved solutions,
soundness/recovery, physical time, positive GR and global closure remain
open. This result does not change #310's original fixed-source/raw-owner
terminal, nor the independent #202/#317 criteria.

## 7. Reproduction and proof boundary

Twenty compiled propositions, 163 exact controls and three transitive D0
source pins pass. All twenty actual types and transitive axiom lists are
printed; only `propext`, `Classical.choice` and `Quot.sound` occur.

The research capsule, compiler transcript, transitive owner hashes and
exact checker are adjacent under `certificates/a4d_native_time_field_intertwiner*`.
The checker independently constructs the Sylvester operator for several
complete finite spaces, verifies the full nullspace and its parametrized
span, the general symbolic defect identity, rational norm controls and
necessary-hypothesis counterexamples. Finite ranks are controls; the
universal completeness proof is the compiled theorem in Section 2.

```
cd 03_FORMALIZATION
lake env lean ../02_REGISTRY/research/certificates/a4d_native_time_field_intertwiner.lean
```

From the repository root:

```
python3 02_REGISTRY/research/certificates/a4d_native_time_field_intertwiner_check.py
```

The diagnostic prints all capsule theorem types and their transitive
axioms. No supported Lean owner or canonical claim is edited. Source pins,
printed propositions, exact results and stated scope are checked together;
a green arithmetic certificate does not promote the remaining G0 premises.
