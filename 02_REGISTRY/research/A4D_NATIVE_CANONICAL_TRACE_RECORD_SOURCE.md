# Canonical trace record: complete source transfer and the second active record

Date: 2026-10-15. Research continuation of #310; no parent terminal or
physical information contract is promoted.

The actual canonical trace seed now gives a constructive source through the
existing AF/CAR record. A complete first-record operator readout has zero
old relative-entropy preparation source. Its smaller left-algebra readout
has a nonzero source, exactly compensated by the retained archive. The next
**active** native record transports that smaller readout into the complete
next operator algebra. There its inherited source is genuinely nonzero:

```text
d A_old,operator10 = +0.4341544459248843867...
d A_gain,operator10 = -0.6507665321409446093...
d Cost_operator10 = -0.2166120862160602226...
```

These are exact analytic spectral derivatives with outward numerical bounds,
not a fitted remainder or a claim of physical stress. The source is supplied
by the actual second record of the existing preparation. The common physical
field/action binding, admission of its preparation germs, and the joint
stationary and continuum problems remain open.

## 1. Inputs and distinct carriers

Write p=(sqrt(5)-1)/2, a=sqrt(p), g=log(phi)=-log(p). Thus p+p²=1.
The native owners are:

- [Fibonacci record activation](A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md),
  especially its actual right-module path decomposition and regular carrier;
- [full Fock record binding](A4D_NATIVE_FOCK_RECORD_BINDING.md), including
  every one of the sixteen real exterior-matter components;
- [amplitude source regularity](A4D_NATIVE_AMPLITUDE_SOURCE_REGULARITY.md),
  which supplies first differentiation through zero eigenvalues;
- #322's published bridge at commit
  `e04e4e8adf76e7508829cec478e43f5d2e9a97f2`, checker Git blob
  `f6a369b25bb45e0144a44e22eefa22360daf544c`. Its fixed gate/price/blank
  intertwiner is consumed, without importing or executing that checker.

Let A_n=M_(F_(n+2)) (+) M_(F_(n+1)); its PF reference has scalar weights
mu_(n,j)=p^(n+1+j), j=0,1, on the two defining blocks. H_n denotes its
full regular GNS space. The operator algebra of the actual three-step record
on H_(n+3) is A_(n+6), represented with old-right multiplicities.

| Readout/process | Defining algebra | Working GNS dimension | Full regular GNS dimension of that algebra |
|---|---|---:|---:|
| First record's left readout | A4=M8 (+) M5 | H4: 89 | 89 |
| First record's complete right-module operator readout | A7=M34 (+) M21 | H4: 89 | H7: 1597 |
| Second active record's complete operator readout | A10=M144 (+) M89 | H7: 1597 | H10: 28657 |

The same abstract algebra, its working representation, and its regular GNS
representation must not be interchanged. Nor are the regular lift of the
first operator state and the second actively recorded state the same state
merely because both can be written on H7.

The two declared spectral contracts remain separate:

```text
A_old(sigma;mu) = D(sigma||mu)/g = Cost - H(sigma)/g,
A_gain(sigma) = H(sigma)/g,
Cost = -Tr(sigma log(mu))/g.
```

These labels do not select native physical Info(v).

## 2. General native six-level source-transfer identity

For a normalized seed vector X in H_n, put d_0=A,d_1=B. In orthonormal GNS
coordinates its two matrices are M_j=sqrt(mu_(n,j)) X_j, with
sum_j Tr(M_j*M_j)=1. The owned three-step frame decomposes

```text
H_(n+3) = K_0 tensor C^A (+) K_1 tensor C^B,
dim K_0 = 13A+8B,  dim K_1 = 8A+5B.
```

These are the actual dimensions of A_(n+6). The owner's path bijection
concatenates a three-step row path and a reversed three-step column path;
it is not an arbitrary enlargement to all operators on H_(n+3).

Let G_j:C^(d_j)->K_j be the canonical inclusion isometries. Any actual
unitary W in this right-module algebra is W_j tensor I_(d_j). The recorded
vector's right-module factors are

```text
F_j = W_j G_j M_j,
F_j*F_j = M_j*M_j.
```

Consequently the complete operator density F_j F_j* has the same nonzero
spectrum as the seed's left density M_j M_j*. All zero modes and old-right
multiplicities remain present. Since mu_(n+6,j)=p^6 mu_(n,j),

```text
H_operator = H_seed,
Cost_operator = Cost_seed + 6,
A_old,operator = A_old,seed + 6,
A_gain,operator = A_gain,seed.                         (1)
```

This is a pointwise identity, hence a first-source identity on every C1
normalized seed-amplitude germ and differentiable right-module unitary germ.
It includes noncommuting dW and gives no extra source from dW in this class.
The amplitude regularity owner handles support births. The theorem concerns
GNS seed vectors and their induced left states; it does not assert equality
of left and right entropy for an arbitrary mixed density on B(H_n).

Active iteration in (1) uses the actual next seed vector in H_(n+3), whose
left state is a different readout from its operator state in A_(n+6).
Therefore zero first-record operator source need not persist under a new
active record. Passive state extension is a separate operation.

## 3. Whole canonical seed and the complete first operator state

Use the entire normalized trace seed of A1, in orthonormal GNS coordinates:

```text
Omega1 = (p,0,0,p,ap),  ||Omega1||²=2p²+p³=1.
x4 = W1 J1 Omega1 = a V0 Omega1 + p V3 Omega1.
```

The scalar M1 component is retained. The working frame has twenty dimensions
and a further sixty-nine-dimensional identity complement inside H4.
In the owned right-module coordinates, F0 is 34 by 2 and F1 is 21 by 1:

```text
F0*F0=p² I2,  F1*F1=p³.
```

Thus sigma7 has nonzero eigenvalues p²,p²,p³ and zero multiplicities 32,20.
With mu7=p8 I34 (+) p9 I21, its likelihood is h7=p^-6 P7. Hence

```text
A_old,7=6,  A_gain,7=2+p³,  Cost7=8+p³.
```

The old action's full amplitude covector is zero, including arbitrary fine
amplitude germs at this state. The gain action's covector need not vanish:
in the fixed real16 matter plus real4 scalar chart, using dA=2 Re<dx,h>,

```text
h_old=0,
h_gain,m=-p³ m,  h_gain,c=2p² c.
```

Its complement covector is exactly zero by calculation. A variation of the
old central masses remains visible; a norm-preserving rotation inside the
matter component is invisible to both complete first operator actions.

## 4. Actual CAR chart and a nontrivial full blank variation

The bridge uses the complete real16 CAR basis B, the Pauli map chi and

```text
T = [[1,0,1,0],[1,0,-1,0],[0,1,0,1],[0,1,0,-1]]/sqrt(2),
Psi = V_M2 (T tensor chi) B*.
```

Complex matrix entries implement this real physical chart; they do not turn
its sixteen real matter components into thirty-two physical components.
At the actual post-record state,

```text
m0 = ap(e_0+e_14) + p²(e_1-e_15),
c0 = (p²,0,0,ap²).
```

Here e_k labels the CAR mask, not a tower level. Their squared norms are
2p² and p³. Conditioning away c0 would change the preparation.

Take the exact norm-preserving matter curve

```text
m(t)=cos(t)m0+sin(t) dm,
dm=-p²(e_0+e_14)+ap(e_1-e_15),   c(t)=c0.             (2)
```

The tangent has zero radial component. Its preimage through the same fixed
golden gate is V2 Omega_M2, in the owner's full fresh-blank plane and
orthogonal to V0. The incoming real matter is

```text
p[cos(t)(e_0+e_14)+sin(t)(e_1+e_15)],
```

with incoming scalar (ap,0,0,0) fixed. Thus (2) is not falsely called an
old-seed-only variation through W V0. Orthogonality of the actual module
isometries proves that its complete first operator spectrum is constant for
all t, not merely at first order.

This fixed-tuple bridge is not a proof of Lorentz equivariance of the entire
exterior representation, an intrinsic orientation update, or physical
admission of every full-blank input. The separate P1/current and chronology
owners retain their actual domains. The calculation uses no new orientation,
reset, selected temperature, or restriction of matter grades.

## 5. Coarse A4 spectrum, full covector and archive compensation

In normalized GNS coordinates the actual x4 consists of diagonal matrices

```text
M8=diag(b+c0,b+c0,b+c1,b-c0,b-c0,b,b,b-c1),
M5=ap³ I5,
b=p³, c0=p²/sqrt(2), c1=ap²/sqrt(2).
```

Here c0,c1 are local scalar amplitudes in this display, not the scalar vector
in Section 4. The coarse defining densities are M8 M8* and M5 M5*, with
**no additional PF factor**: the coordinates already contain its square root.
All thirteen eigenvalues are strictly positive:

```text
(b+c0)² [2], (b-c0)² [2],
(b+c1)² [1], (b-c1)² [1], p6 [2], p7 [5].
```

Their values give

```text
Cost4=5+5p7=5.172209268743165...,
H4/g=4.035793011264687...,
A_old,4=1.136416257478478... .
```

The implementation retains the complete generic-log amplitude covector on
all89 coordinates. For either contract put G_old=C4+log(sigma4)/g,
G_gain=-log(sigma4)/g, where C4=(5 I8,6 I5). The normalized half-gradient is

```text
h=(G-<G>)M.
```

This includes the moving normalizer. Its pullbacks to Psi and the scalar
frame retain all16+4 components; the remaining69-component covector is
generally **nonzero** and is retained. Restricting its use to the stated CAR
chart does not erase the ambient covector.

For completeness, explicit real-coordinate coefficients are executable in
`generic_costates`: dA=2[k0(dm0+dm14)+k1(dm1-dm15)+t0 dc0+t3 dc3].
The other twelve matter and two scalar coefficients are exactly zero at this
base point. Both the generic gradient and these closed coefficients are
checked as symbolic expressions with independent logarithm variables.
On (2),

```text
0.43415444592488 < dA_old,4 < 0.43415444592489,
-0.65076653214095 < dA_gain,4 < -0.65076653214094,
dCost4=-8ap7.
```

These nonzero coarse sources must not be relabelled as the complete first
operator source. For the actual PF-preserving embedding iota:A4->A7, define
the recovered state R_mu(sigma4)=mu7 iota(mu4^-1 sigma4). The path groups
obey 3p8+2p9=p5 and 2p8+p9=p6, so this is normalized and its reference is
the actual mu7. Since sigma4 is precisely the restriction of sigma7,

```text
D(sigma7||mu7)-D(sigma4||mu4)
    =D(sigma7||R_mu(sigma4)).                         (3)
```

To prove (3), split log R_mu=log mu7+iota(log(mu4^-1 sigma4)); central
PF weights commute, and restriction transfers the last expectation exactly.
Here R_mu is faithful, so support causes no extra convention. The archive
term is approximately 4.863583742521522 in units g. Its derivative on (2)
is exactly -dA_old,4. The analogous entropy difference cancels dA_gain,4.
This is an actual algebraic archive contribution, not a chosen counterterm.

## 6. The second active record supplies a complete nonzero source

Now apply the owned next activation, rather than a passive extension:

```text
x7_active(t)=W4 J4 x4(t)=AF.activate(4,x4(t)).
```

The new working space is the full H7, dimension1597. Its right-module
operator algebra is A10=M144 (+) M89, with old-right multiplicities8,5.
The exact n=4 frames give F_j=R_j M4,j, R_j*R_j=I. Thus (1) applies:

```text
A_old,operator10=6+A_old,4=7.136416257478478...,
A_gain,operator10=H4/g=4.035793011264687...,
Cost_operator10=6+Cost4=11.172209268743165... .
```

The thirteen positive eigenvalues of Section 5 are now the complete
operator-state nonzero spectrum; all220 other defining modes are retained.
No diagonalisation of a 1597 by 1597 matrix is needed: the actual native
isometries prove the spectral identity and its differentiated version.
Consequently the complete second-record source on the inherited variation
is exactly the nonzero interval in Section 5. More generally its full
seed-amplitude covector, including the69 complement, is the coarse covector
of that section. Noncommuting variation of the new right-module unitary
alone contributes zero, by (1).

This removes one missing constructive arrow: a real source of a declared
spectral readout is now carried by an existing complete active AF process.
It neither selects that readout as physical Info nor equates it with the
earlier full GNS heat or chronology terms. Matter stationarity must still be
tested in the actual common action; a nonzero derivative by itself is not a
stationary solution or an Einstein source.

## 7. Full regular first-record lift and two different archive projections

The owner's normalized regular preparation of the first operator state is

```text
X7_regular=W1 e/p³ in GNS(A7),  e=V0 V0*, tau7(e)=p6.
```

Its regular norm is one, and its left density agrees exactly with sigma7
from Section 3. This is not x7_active of Section 6. Two well-typed
projections on its1597-dimensional regular space give different observables:

| Reference projection Q | Retained dimension | Actual occupation q | Jet on the lifted (2) |
|---|---:|---|---|
| I-L_e, left multiplication by the corner | 89 | p² | 4ap³ |
| I-J_(1->7) J_(1->7)*, full canonical GNS inclusion | 5 | 1-p7 | 4ap9 |

The first observable transports the working corner. The second projects
onto the actual coarse **GNS image** and is generally not left multiplication
by an AF algebra projection. The focused consumer independently constructs
the trace adjoint by summing every native six-step copy in the right-module
basis. It obtains

```text
C_(1<-7)(X7_regular)=ap³ I,
C_(1<-7)(dX7_regular)=-p4 z_M2.
```

Therefore the canonical retained norm is p7 and dq=4ap9. The working H4
archive has q_work=p², giving q_regular=1-p6(1-q_work) and
dq_regular=p6 dq_work; using q_work on the full regular canonical projection
would be a carrier error.

For the separately declared reference heat generator Delta=nu Q, the
complete derivative at fixed Q and beta is

```text
dS=(q-p_thermal)dnu+nu dq,
p_thermal=(D-d)exp(-beta nu)/(d+(D-d)exp(-beta nu)).
```

At beta=log2,nu=1, the canonical regular projection has
p_thermal=796/801 and gap source 5/801-p7. The working89 projection instead
has p_thermal=42/47; the regular left-corner projection has
p_thermal=754/843. These are different reference generators. They do not
contradict (1), do not cancel a Cost-Info source numerically, and do not
supply a physical gap/temperature law.

## 8. Focused reproduction and remaining physical arrow

The parallel #322 capacity continuation, published at
`3bed4c2019d8832fd7715f7a319ab39d60bf29bf`, uses this same active recursion:
its working dimensions are F_(6k+5), beginning5,89,1597. Its named
orthogonal-history PVM has entropy k(2-p)g on the canonical trace preparation.
That history entropy, the defining-left entropy above, and the pure global
GNS state's entropy are distinct readouts. Resolution/history growth does
not by itself select physical Info or induce a metric variation. The
nonzero second-operator source here is compatible with the preserved old
Lorentz observables; it does not require them to move.

The single entrypoint is
`certificates/a4d_native_canonical_trace_record_source_check.py`. It imports
only the hash-pinned existing AF/F definitions and the new source module.
It checks the full89 state, all16+4 chart, full ambient gradient, actual
right-module readout, rank-changing source interpretation, retained archive,
regular lift/copy-adjoint, and next-record spectral transfer. It does not
execute the foreign bridge checker, old suites or Lean builds.

The next scientific use is to bind this actual second-record source to the
constrained physical (q,D,b,m) preparation and the same complete action used
for metric, link and matter variation. The existing source recursion and
joint compatibility equations can consume that derivative once the binding
is derived. In particular, independent q/link/shift jets, native Info(v),
physical preparation admission, full stationarity, curved solutions and
refinement-uniform comparison cannot be supplied by declaring (2) physical.
The original fixed-source/raw-owner #310 terminal, #202 and #317 are open.
