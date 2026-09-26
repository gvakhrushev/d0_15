# MEMO A4D — J² smooth resonance closure

**Task:** \`EXP-A4D-J2-SMOOTH-RESONANCE-CLOSURE\`  
**Execution:** PR #216  
**Status:** IN_PROGRESS / terminal classification reached  
**Baseline:** \`73a71a74b93c5fc65d35b0357f5343dc72b5e1c3\`  
**Parent result:** merged PR #208  
**Certificate:** \`02_REGISTRY/research/certificates/a4d_j2_smooth_resonance_closure_check.py\`

## 0. Verdict

The diagonal quarter-wave obstruction found in #208 is **not** a nonlinear
no-go.

For the correctly polarized L=4 diagonal character
\[
z_A=z_B=z_C=z_D=i,
\]
the flat connection equation is linearly incompatible with a genuine metric
source, but its Lyapunov--Schmidt reduction has a nondegenerate cubic Euler
root.  Therefore the full analytic finite Euler equation has a small
Puiseux branch
\[
\boxed{
A_{\rm res}(\delta)
=
|\delta|^{1/3}K(u_\ast)
+
O(|\delta|^{2/3})
}
\]
for the tested \(q_{11}\) resonant metric source (with the obvious sign/source
choice encoded in the reduced equation).

For a \(C^\infty\) periodic smooth metric realization on \(T^4\), a
quarter-wave discrete Fourier coefficient is super-algebraically small in the
side length \(L\).  Taking a cube root preserves super-algebraic decay.
Consequently this diagonal Puiseux branch is
\[
o(L^{-m})
\]
for every prescribed \(m\), and in particular is invisible after the
\(L^2=\varepsilon_L^{-2}\) J² normalization.

However the diagonal orbit is not the whole polarized singular spectrum.
On L=4 the exact/numerically scanned polarized symbol has 56 singular
characters split by spatial \(S_3\) permutations and complex conjugation into
**nine orbit types**.  The present packet closes only the diagonal orbit and
its conjugate.

Therefore the honest terminal is

\[
\boxed{\texttt{J2-SMOOTH-PARTIAL-CLOSURE}.}
\]

The certified packet stops at the diagonal orbit.  Post-certificate work in
§§11--18 shows that the correct next object is the **full compact resonance
geometry**, organized by chiral/parabolic strata and the first source-visible
reduced Euler order, rather than eight independent L=4 calculations.  Those
new checkpoints are not yet checker-owned.

This result **scopes but does not invalidate** #208:

- #208 remains correct that one globally smooth *linear/IFT* all-mode
  connection section through flat does not exist;
- the stronger reading that the diagonal resonance is itself a terminal
  nonlinear obstruction is withdrawn;
- the diagonal resonance instead closes by a nonanalytic Puiseux branch.

---

## 1. Corrected polarized input from #208

For a real finite action a complex character \(z\) pairs quadratically with
\(z^{-1}\).  The load-bearing connection symbol is therefore the polarized
block of #208, not the earlier unpolarized exploratory formula.

Along the diagonal character
\[
z_A=z_B=z_C=z_D=t,
\]
#208 proves
\[
\boxed{
\det H_{AA}^{\rm pol}(t)
=
\frac{(t^2+1)^{12}}{16t^{12}}.
}
\]

Hence
\[
\det H_{AA}^{\rm pol}(1)=256
\]
at low momentum, while at
\[
t=i
\]
one has
\[
\operatorname{rank}H_{AA}^{\rm pol}=16.
\]

The genuine ten-component metric source enlarges the connection equation to
rank 20:
\[
\operatorname{rank}
\left[
(H_{AA}^{\rm pol})^T\mid H_{Aq}
\right]
=20.
\]

An explicit Fredholm witness pairs nontrivially with \(q_{11}\).  Thus there
is no differentiable connection graph
\[
A=A(q)
\]
through the flat point on the full finite carrier.

This packet asks the different nonlinear question: can a branch approach flat
with fractional scaling?

---

## 2. Diagonal resonant kernel

At \(t=i\), the complex connection kernel has dimension eight.

Using the connection coordinate order
\[
(K_1,K_2,K_3,J_{12},J_{13},J_{23})
\]
inside each Role block \(A,B,C,D\), a convenient kernel basis is:

\[
\begin{array}{c|l}
0 & A:(K_1+K_2+K_3)\\
1 & A:(J_{12}-J_{13}+J_{23})\\
2 & B:(K_1+J_{12}+J_{13})\\
3 & B:(K_2-K_3+J_{23})\\
4 & C:(K_1-K_3+J_{13})\\
5 & C:(K_2-J_{12}+J_{23})\\
6 & D:(K_1-K_2+J_{12})\\
7 & D:(-K_3+J_{13}+J_{23}).
\end{array}
\]

The source projection from the ten symmetric metric directions has rank four.
For the \(q_{11}\) source used below it lands only in the complex line generated
by basis vector 0.

Passing to the real L=4 cosine/sine representation gives a 16-dimensional
real resonant kernel.

A symmetry-closed source-active subspace is four-dimensional.  Write
\((a,b,c,d)\) for

\[
a:\cos(kx)\lambda_0,\qquad
b:\sin(kx)\lambda_0,
\]
and
\[
c:\cos(kx)(\lambda_2+\lambda_5-\lambda_7),\qquad
d:\sin(kx)(\lambda_2+\lambda_5-\lambda_7).
\]

The quadratic range forcing lies at harmonics \(0\) and \(2k\), whose
connection blocks are regular.

---

## 3. First nonzero reduced term

The direct quadratic reduced Euler term on the resonant kernel vanishes.
The naive quartic contribution from one range harmonic is not separately zero,
but the exact \(0\)- and \(2k\)-range Schur contributions combine with the
direct star term to give the following reduced quartic potential:

\[
\boxed{
V_4(a,b,c,d)=48P(a,b,c,d)
}
\]
with
\[
\begin{aligned}
P={}&36a^2b^2-3a^2bc-27a^2bd+2a^2cd+3a^2d^2\\
&-27ab^2c+3ab^2d+188abcd+22ac^2d-107acd^2-ad^3\\
&+3b^2c^2-2b^2cd+bc^3-107bc^2d-22bcd^2\\
&-6c^3d+38c^2d^2+6cd^3.
\end{aligned}
\]

For a real \(q_{11}\) quarter-wave source, the exact reduced linear source in
these variables is

\[
\boxed{s=(-8,8,0,0).}
\]

Hence the blown-up limiting Euler system is

\[
\boxed{
\nabla V_4(u)+s=0,
\qquad
u=(a,b,c,d).
}
\]

Because \(V_4\) is quartic, this is a cubic equation.  Balancing
\[
u^3\sim\delta
\]
already predicts
\[
u=O(\delta^{1/3}).
\]

---

## 4. Certified nondegenerate cubic root

A high-precision root of the reduced system is

\[
\begin{aligned}
a_\ast&=+0.14005420967421540954\ldots,\\
b_\ast&=-0.13701463188056607858\ldots,\\
c_\ast&=+0.03111354422107251129\ldots,\\
d_\ast&=-0.02645772859362619535\ldots.
\end{aligned}
\]

The certificate does not rely on this floating-point statement alone.
It centers a Newton contraction at the rational point

\[
a_0=\frac{7002710483711}{50000000000000},
\]
\[
b_0=-\frac{13701463188057}{100000000000000},
\]
\[
c_0=\frac{3111354422107}{100000000000000},
\]
\[
d_0=-\frac{2645772859363}{100000000000000}.
\]

Let
\[
F(u)=\nabla V_4(u)+s,\qquad J(u)=DF(u).
\]

At \(u_0\), exact rational arithmetic gives

\[
\|J(u_0)^{-1}F(u_0)\|_\infty
<
4.591\times10^{-15},
\]
\[
\|J(u_0)^{-1}\|_\infty
<
0.021146.
\]

On the infinity ball
\[
\|u-u_0\|_\infty\le10^{-10},
\]
an exact coefficient bound gives
\[
\|J(u)-J(u_0)\|_\infty
\le
8725.903\,\|u-u_0\|_\infty.
\]

Therefore the frozen-Newton map
\[
T(u)=u-J(u_0)^{-1}F(u)
\]
has contraction constant

\[
q<
1.846\times10^{-8}.
\]

Moreover
\[
\frac{\|J(u_0)^{-1}F(u_0)\|_\infty}{1-q}
<
4.591\times10^{-15}
\ll10^{-10}.
\]

Thus \(T\) maps the ball into itself and is a strict contraction.
There is a unique exact real root in this rational ball.

The Jacobian is very far from singular:
\[
\det J(u_0)\approx8.1987281\times10^7,
\]
and its numerical singular values are approximately
\[
177.51,\quad137.78,\quad62.60,\quad53.55.
\]

The contraction estimate, not the numerical singular values, is the
existence/uniqueness certificate.

---

## 5. Puiseux branch theorem

Write the genuine resonant metric-source amplitude as
\[
\delta=t^3.
\]

Split the connection variables into resonant kernel \(u\) and regular
complement \(w\).  The regular Hessian is invertible on the \(0/2k\) range
sectors, so the analytic implicit-function theorem gives
\[
w=w(t,u)
\]
near the origin.

After substitution, the resonant Euler equation has the blown-up form
\[
t^{-3}E_{\rm red}(t,tu)
=
\nabla V_4(u)+s+O(t).
\]

At \(t=0\), the certified root \(u_\ast\) is nondegenerate.
The ordinary implicit-function theorem in variables \((t,u)\) therefore gives
a unique local branch
\[
u(t)=u_\ast+O(t).
\]

Undoing the blow-up,

\[
\boxed{
A_{\rm res}(\delta)
=
\delta^{1/3}K(u_\ast)
+
O(\delta^{2/3})
}
\]
for the chosen real cube-root/source orientation.

Thus the linear Fredholm incompatibility is resolved by a continuous but
non-\(C^1\) connection branch.  This is exactly why the linear IFT of #208
fails while a nonlinear branch still exists.

---

## 6. Smooth T4 sampling makes the diagonal branch J²-invisible

Let \(f\in C^\infty(T^4)\) be one component of a globally periodic smooth
metric/coframe realization and let \(\widehat f_n\) be its continuum Fourier
coefficients.

For every \(M\) there is \(C_M\) with
\[
|\widehat f_n|
\le
C_M(1+|n|)^{-M}.
\]

The discrete L-grid Fourier coefficient at character \(k\) is the alias sum
\[
\widehat f^{(L)}_k
=
\sum_{\ell\in\mathbb Z^4}
\widehat f_{k+L\ell}.
\]

At a quarter-wave character at least one component of \(k\) is
\(\pm L/4\).  Hence
\[
|k+L\ell|
\ge cL(1+|\ell|)
\]
after changing the harmless constant \(c>0\), and for \(M>4\)

\[
|\widehat f^{(L)}_k|
\le
C'_M L^{-M}.
\]

Because \(M\) is arbitrary,

\[
\boxed{
\widehat f^{(L)}_{\rm quarter}
=
O(L^{-M})
\quad\text{for every }M.
}
\]

Let \(\delta_L\) denote the corresponding resonant metric-source amplitude.
The Puiseux estimate gives
\[
|A_{{\rm res},L}|
\le
C|\delta_L|^{1/3}.
\]

Given any \(P\), use the smooth-tail bound with \(M=3P\).  Then

\[
\boxed{
A_{{\rm res},L}=O(L^{-P})
\quad\text{for every }P.
}
\]

Thus the resonant connection branch remains super-algebraically small.
The regular range corrections are at least quadratic in this amplitude and are
smaller still.

In particular,

\[
L^2A_{{\rm res},L}\to0.
\]

So this diagonal UV repair is invisible at the
\(\varepsilon_L^{-2}=L^2\) J² scaling used by E-NJET.

No spectral filter has been inserted.  The suppression comes from smoothness
of the sampled continuum field plus the derived Puiseux exponent.

### Remaining interface caveat

The repository's typed T4 sampler is currently a local radius-two map.  The
Fourier-tail statement above applies to an actual globally periodic smooth
finite realization on the entire L-grid.  A theorem identifying the selected
global finite star state with that global smooth sampling remains part of the
finite-to-continuum realization interface.

The spectral statement itself is standard and exact conditional on such a
\(C^\infty\) periodic realization.

---

## 7. Full polarized L=4 singular spectrum

The corrected polarized block was scanned over all
\[
z_r\in\{1,i,-1,-i\},
\qquad 4^4=256
\]
characters.

There are

\[
\boxed{56}
\]
singular characters.

Their connection rank / augmented metric-source rank / incompatibility
dimension counts are

| rank \(H_{AA}\) | augmented rank | incompatibility dim | count |
|---:|---:|---:|---:|
| 20 | 24 | 4 | 24 |
| 22 | 23 | 1 | 12 |
| 22 | 24 | 2 | 12 |
| 20 | 23 | 3 | 6 |
| 16 | 20 | 4 | 2 |

Quotienting only by the symmetries used for classification here — spatial
\(S_3\) permutations and complex conjugation — gives nine orbit types.
Represent phases by
\[
0=1,\quad1=i,\quad2=-1,\quad3=-i.
\]

| A phase | sorted spatial phases | rank | augmented | incompat. | orbit size |
|---:|---|---:|---:|---:|---:|
| 0 | (0,1,1) | 22 | 23 | 1 | 6 |
| 0 | (0,1,3) | 22 | 24 | 2 | 6 |
| 0 | (1,1,2) | 20 | 24 | 4 | 6 |
| 1 | (0,1,2) | 20 | 24 | 4 | 12 |
| 1 | (1,1,1) | 16 | 20 | 4 | 2 |
| 1 | (1,3,3) | 20 | 23 | 3 | 6 |
| 2 | (0,1,1) | 20 | 24 | 4 | 6 |
| 2 | (1,1,2) | 22 | 23 | 1 | 6 |
| 2 | (1,2,3) | 22 | 24 | 2 | 6 |

The diagonal orbit
\[
(i,i,i,i)
\]
is the fifth row and is the one closed in §§2--6.

The other eight orbit types are not automatically equivalent to it.
Their kernel dimensions and metric-source cokernel dimensions differ.
A global H-J2-SMOOTH theorem therefore cannot yet be claimed from the diagonal
calculation.

---

## 8. Consequence for the Einstein J² bridge

The diagonal result removes the strongest interpretation of #208's blocker.

For globally smooth normal sampling, the diagonal resonant repair is
super-algebraically invisible.  Therefore it cannot modify the leading
J² coefficient
\[
\frac14E_{\eta,N}
\]
already certified by #201.

If every relevant resonance stratum admits a small branch with a **uniform
positive Hölder/Puiseux exponent on a finite compact stratification**, then the
same smooth-tail argument applies: super-algebraic metric Fourier tails remain
super-algebraic after the nonlinear solve.

Under that yet-unproved all-stratum statement, #201 + E-NJET would give

\[
E_\star[g]
=
-\frac12G[g]
\]
for the naked-star normalization.

No new coefficient selector is required.

The cosmological \(bg\) channel and finite-Noether-to-Levi-Civita-divergence
route remain separate exactly as in #208.

---

## 9. Theorem-ready statements

1. The corrected L=4 diagonal quarter-wave has complex connection kernel
   dimension eight and real resonant kernel dimension sixteen.

2. The genuine symmetric metric source projects to a four-dimensional
   subspace of the diagonal resonant cokernel.

3. For \(q_{11}\), a four-real-dimensional symmetry-closed resonant reduction
   suffices.

4. After exact elimination of regular \(0\)- and \(2k\)-range modes, the first
   nonzero reduced potential is the quartic \(V_4=48P\) displayed in §3.

5. The exact source vector in this reduction is \((-8,8,0,0)\).

6. The reduced cubic Euler system
   \[
   \nabla V_4+s=0
   \]
   has a unique real root in an explicit rational infinity ball of radius
   \(10^{-10}\).

7. The root is nondegenerate.

8. The full analytic diagonal connection Euler equation consequently admits a
   local Puiseux branch
   \[
   A_{\rm res}=O(|\delta|^{1/3}).
   \]

9. For any \(C^\infty\) periodic global sampling, quarter-wave discrete Fourier
   coefficients are super-algebraically small in L.

10. The diagonal Puiseux branch is therefore super-algebraically small and is
    \(o(L^{-2})\), hence invisible at J² scaling.

11. The polarized L=4 symbol has 56 singular characters grouped into nine
    spatial-\(S_3\)+conjugation orbit types.

12. Only the diagonal orbit is nonlinearly closed by this packet.

---

## 10. Terminal disposition

The diagonal quarter-wave resonance is no longer the first obstruction.

The exact positive terminal for that orbit is

\[
\boxed{
\texttt{DIAGONAL-QUARTER-WAVE-CLOSES-BY-CUBIC-PUISEUX-BRANCH}
}
\]
together with
\[
\boxed{
\texttt{DIAGONAL-RESONANCE-IS-SUPERALGEBRAICALLY-J2-INVISIBLE-ON-SMOOTH-SAMPLING}.
}
\]

But the requested all-spectrum H-J2-SMOOTH theorem remains incomplete because
eight additional polarized L=4 singular orbit types remain.

Therefore the task-wide terminal is

\[
\boxed{\texttt{J2-SMOOTH-PARTIAL-CLOSURE}.}
\]

The old orbit-by-orbit blocker is superseded by the post-certificate program
in §18.  The first exact upgrade is:

\[
\boxed{
\text{certificate the chiral UV gap and the parameterized }(w,w,i,i)
\text{ parabolic resonance family.}
}
\]

After that, parabolic isolation / generic-stratum discriminant control replaces
blind repetition over the remaining L=4 representatives.

No Einstein field equation, Newton coupling, finite covariant-divergence
derivation, or cosmological coefficient is promoted by this result.

---

## 11. Post-certificate resonance-geometry continuation

This section integrates the subsequent local research log **without upgrading the
task-wide terminal**.  Unless explicitly stated otherwise, the results below are
research checkpoints and are **not yet owned by the existing certificate**.

The certified state of §§0--10 remains:

\[
\boxed{\texttt{J2-SMOOTH-PARTIAL-CLOSURE}.}
\]

The diagonal quarter-wave is closed, but the all-resonance smooth-sector theorem
is still open.

### 11.1 Diagonal near-resonance opening: exact local scaling checkpoint

For the diagonal polarized family \(M(t)=H_{AA}^{\rm pol}(t)\) at \(t=i\),
the local calculation gives an 8-dimensional complex kernel and compressed
first phase derivative

\[
C_1=L^T M'(i)R
\]

of rank four.  Together with the order-12 determinant zero

\[
\det M(t)=\frac{(t^2+1)^{12}}{16t^{12}},
\]

this gives the local invariant-factor pattern

\[
\boxed{1,1,1,1,2,2,2,2}
\]

for the eight resonant modes: four open linearly in \(t-i\), while four open
quadratically.  Hence the diagonal near-resonant inverse can grow as

\[
\|M(t)^{-1}\|=O(|t-i|^{-2}),
\]

so the closest lattice mode can exhibit \(O(L^2)\) amplification.

The metric source is not transverse to this worst sector.  The local exact
projection found

\[
\rank J=4,\qquad \rank C_1=4,\qquad \rank[C_1\mid J]=6,
\]

with two genuine metric combinations reaching the quadratic-opening sector,
for example

\[
q_{01}-q_{03}-q_{12}+q_{23},
\qquad
q_{02}-q_{03}-q_{12}+q_{13}.
\]

This is a **diagonal local statement only**.  It must not be promoted to a
global finite-Sobolev threshold for the full four-phase symbol; later full-symbol
scans show stronger nonresonant conditioning can occur away from the diagonal.

### 11.2 Chiral splitting and UV separation

In the self-dual/anti-self-dual Lorentz basis

\[
\Sigma_i^\pm=K_i\pm iJ_i,
\qquad
J_1=J_{23},\quad J_2=-J_{13},\quad J_3=J_{12},
\]

the polarized \(24\times24\) connection symbol splits into two
\(12\times12\) chiral blocks,

\[
\boxed{
H_{AA}^{\rm pol}(z)\sim H_+(z)\oplus H_-(z).
}
\]

A local exact calculation at \(z=(1,1,1,1)\) gives

\[
\operatorname{spec}(H_+(1)^\dagger H_+(1))
=
\{16\times4,\;4\times8\},
\]

hence

\[
\sigma_{\min}(H_+(1))=2.
\]

Using the explicit Laurent coefficients, a conservative derivative estimate
was obtained,

\[
\|\partial_{\theta_j}H_+\|_F\le 6\sqrt2,
\]

so Weyl perturbation yields an explicit open neighborhood of zero momentum in
which the chiral block stays invertible.  The important structural conclusion
is:

\[
\boxed{\text{the resonance variety is uniformly separated from }z=1.}
\]

Therefore genuine resonant modes are UV modes, which is exactly the regime
where \(C^\infty\) Fourier tails can suppress finite-order Puiseux branches.

This chiral/gap packet is currently **research-exact but not checker-owned** and
must receive a certificate before theorem promotion.

### 11.3 Lattice resonance pattern: strong computational classification, not theorem

A scan over \(L=4,8,12,16,20\) found exact singular lattice characters only
for \(4\mid L\) on that tested range, and all observed points fit five families.
In particular:

1. a rank-22, \(d_{\rm incompat}=1\) family
   \[
   z_0=z_j=w,\qquad z_k=z_l=q,\qquad q\in\{\pm i\},
   \]
   with observed count \(6(L-2)\);

2. a rank-20, \(d_{\rm incompat}=4\) family
   \[
   z_r=z_s=q,\qquad z_u=w,\qquad z_v=-w^{-1},
   \]
   with observed count \(12(L-2)\);

3. its \(w=-q\) boundary, the six permutations of
   \[
   \{i,i,-i,-i\},
   \]
   with rank 20 and \(d_{\rm incompat}=3\);

4. the two diagonal points
   \[
   (\pm i,\pm i,\pm i,\pm i)
   \]
   with rank 16 and \(d_{\rm incompat}=4\);

5. an exceptional rank-22, \(d_{\rm incompat}=2\) family
   \[
   z_0=t,\qquad
   \{z_1,z_2,z_3\}=\{t^{-1},r,-r\},
   \qquad
   t^6=1,\quad r^2=-t^4.
   \]

The corresponding observed totals are

\[
N_{\rm sing}(L)=18L-16
\quad(4\mid L,\;12\nmid L),
\]

and

\[
N_{\rm sing}(L)=18L+8
\quad(12\mid L).
\]

These formulas matched the scanned sets, not only the counts, on
\(L=4,8,12,16,20\).  They remain a **strong conjectural lattice
classification** until a determinant/factorization proof is added.

### 11.4 Continuous resonance variety and generic stratum

The discrete root-of-unity families are only the lattice intersections of a
larger continuous resonance set

\[
Z=
\{z\in\mathbb T^4:\det H_+(z)=0\}.
\]

Numerical generic points on this set exhibit

\[
\rank H_{AA}=22,
\qquad
\rank[H_{AA}^T\mid H_{Aq}]=24,
\]

hence a two-complex-dimensional connection kernel and
\(d_{\rm incompat}=2\).  In the real \(k,-k\) representation this is the
balanced generic normal-form size

\[
\boxed{
4\ \text{real resonant variables}
\leftrightarrow
4\ \text{real sourced cokernel equations}.
}
\]

This generic-stratum statement is presently **numerical/structural**, not a
certified theorem.

The natural global organization is therefore no longer “solve eight more
\(L=4\) orbits”.  It is a finite algebraic stratification

\[
Z_{\rm generic}
\supset
Z_{\rm quartic\mbox{-}degenerate}
\supset\cdots
\]

by the first reduced homogeneous Euler term that becomes source-visible.

---

## 12. Exact parametric parabolic seam found in the rank-22 family

A particularly important rank-22 family admits the exact parameterization

\[
z_0=z_1=w,\qquad z_2=z_3=i.
\]

For generic \(w\), each chiral block has rank 11, and one kernel vector can be
written rationally as

\[
\lambda_+(w)=
\Big(
\frac{1-i}{2}\frac{w-i}{w},0,0;\
\frac{1-i}{2}\frac{w-i}{w},0,0;\
i,-1,-i;\
i,-i,1
\Big).
\]

The projected metric source is independent of \(w\):

\[
\boxed{
j_+(q)=j_-(q)
=-(1+i)(q_{02}-q_{03}-q_{12}+q_{13}).
}
\]

Thus this is a continuous resonance stratum carrying one fixed physical metric
channel, not an accidental collection of Fourier roots.

The resonant kernel lies in the parabolic algebra

\[
\mathfrak{sim}(2)
=
\operatorname{span}\{D,J,N_2,N_3\},
\]

with one convenient choice

\[
D=K_1,\qquad
J=J_{23},\qquad
N_2=K_2-J_{12},\qquad
N_3=K_3-J_{13},
\]

all preserving the null line

\[
n=(1,-1,0,0).
\]

On flat solder the star face functionals pair as

\[
\ell_{01}=D^\ast,\quad
\ell_{23}=J^\ast,\quad
\ell_{02}=N_2^\ast,\quad
\ell_{12}=-N_2^\ast,\quad
\ell_{03}=N_3^\ast,\quad
\ell_{13}=-N_3^\ast.
\]

For pure resonant-kernel links, the exact group structure gives

\[
P_{01}=I,\qquad
P_{02}=P_{12},\qquad
P_{03}=P_{13},
\]

while \(P_{23}\) lies in the normal null-translation subgroup.  The paired face
terms cancel, yielding the finite-amplitude identity

\[
\boxed{
S_\star\big|_{\rm pure\ resonant\ kernel}=0.
}
\]

This explains the high-order direct cancellations observed in raw Taylor
experiments: this kernel is genuinely action-flat before range elimination.

**Claim status:** exact local derivation in the research log; not yet owned by
the current repository checker.  It should be the first new certificate target.

---

## 13. Quartic-flat parabolic branch and nonlinear visibility order

At the representative \(w=1\), the quadratic range forcing from the full
four-real-dimensional resonant kernel spans subspaces

\[
\dim U_0=2,\qquad
\dim U_{2k}=4.
\]

The local exact calculation found complete isotropy with respect to the inverse
regular Hessians,

\[
\boxed{
U_0^T H_0^{-1}U_0=0,
\qquad
U_{2k}^T H_{2k}^{-1}U_{2k}=0,
}
\]

checked on the full basis of all ten quadratic monomials in the resonant
amplitudes.  Consequently

\[
\boxed{
V_4^{\rm red}\equiv0
}
\]

for this real resonant kernel.

Half-period translation acts as \(u\mapsto-u\), so the reduced action is even.
After the quadratic and quartic layers vanish, the first possible restoring
potential is therefore

\[
V_6,
\]

with first candidate Euler term

\[
\nabla V_6\sim u^5.
\]

If this sextic layer isolates the origin and sees the sourced cokernel, the
branch scale is

\[
u=O(\delta^{1/5})
\]

rather than the diagonal \(O(\delta^{1/3})\).

A second \(d_{\rm incompat}=1\), \(L=4\) orbit shows the same
\(\mathfrak{sim}(2)\) / common-null-line pattern and vanishing sampled reduced
quartic, but it does **not** yet have the full ten-monomial exact proof.
Family-wide “all \(d=1\) strata are quartic-flat” therefore remains a
hypothesis.

Conversely, for

\[
z=(1,1,i,-i),
\qquad d_{\rm incompat}=2,
\]

both complex kernel directions are source-active, and at
\(u=(1,2,3,4)\) the exploratory calculation gives

\[
V_4^{\rm direct}=-\frac{189894656}{3},
\]

range correction \(93220864\), and reconstructed

\[
V_4^{\rm red}=\frac{89767936}{3}\ne0.
\]

This is evidence for a generic quartic-active \(d=2\) stratum, but remains a
single-point exact/numerically reconstructed check rather than a certified
polynomial identity.

These observations motivate the bookkeeping invariant

\[
\boxed{
\nu(z)=
\min\{3,5,7,\ldots:
\text{degree-}\nu\text{ reduced Euler term sees the sourced cokernel}\}.
}
\]

Current status:

\[
\nu=3
\quad\text{for the certified diagonal branch,}
\]

\[
\nu\ge5
\quad\text{for the certified-local }w=1\text{ parabolic representative,}
\]

while generic \(d=2\) data are consistent with \(\nu=3\).

---

## 14. Topological replacement for orbit-by-orbit Newton solving

The useful invariant is not the exact value of \(\nu\) by itself.
For an even-character resonance, half-period translation gives an odd reduced
Euler map

\[
F(-u)=-F(u).
\]

If

\[
\boxed{
u=0\text{ is an isolated zero of the unsourced reduced Euler map},
}
\]

then on a sufficiently small sphere the normalized map

\[
\frac{F(u)}{\|F(u)\|}
:S^{m-1}\to S^{m-1}
\]

is odd and has nonzero mod-2 degree.  Therefore the local Brouwer degree is
nonzero, so all sufficiently small source directions have nearby solutions.

This replaces “find one Newton root per source” by the structurally cleaner
gate:

\[
\boxed{\text{prove isolation of the reduced resonant critical point}.}
\]

For a homogeneous leading term, projective critical-point exclusion is an
algebraic resultant/discriminant problem.

### Uniformity repair

A pointwise statement “\(\nu(z)<\infty\) for every \(z\)” is **not sufficient**
for the refinement limit if the visibility order can diverge along a sequence
of resonance strata.  The continuum theorem needs one of:

\[
\sup_{z\in Z_{\rm relevant}}\nu(z)<\infty,
\]

or, more generally, a **uniform positive Hölder/Łojasiewicz exponent** on a
finite compact stratification.

Likewise, curve selection alone supplies existence of analytic/subanalytic
arcs but not the quantitative inverse bound needed for the refinement
estimate.  The intended theorem stack is

\[
\boxed{
\text{isolated zero}
+\text{nonzero local degree}
+\text{Łojasiewicz/subanalytic inverse estimate}.
}
\]

This is the correct global replacement for a universal cubic LS ansatz.

---

## 15. Smooth UV suppression after stratified Puiseux/Hölder closure

The exact low-frequency gap separates the compact resonance set from
\(z=1\).  Therefore a resonant lattice mode has frequency

\[
|n|\ge cL
\]

for some \(c>0\).

For a fixed globally periodic \(C^\infty\) realization,

\[
|\widehat q_n|=O(L^{-M})
\qquad\forall M
\]

uniformly on such UV frequencies.

If each resonance stratum admits a branch satisfying a **uniform** local
Hölder estimate

\[
|A_{\rm res}|
\le C|\widehat q|^\alpha,
\qquad \alpha>0,
\]

then the resonant correction is again super-algebraically small,

\[
A_{\rm res}=O(L^{-P})
\qquad\forall P,
\]

hence

\[
\boxed{
L^2A_{\rm res}\to0.
}
\]

Thus for the \(C^\infty\) route the particular finite exponent
\(1/3,1/5,1/7,\ldots\) is irrelevant once a uniform positive Hölder exponent
is established.

Earlier local thresholds such as \(s>4\) for diagonal near-resonant linear
detuning and \(s>6\) for the diagonal cubic Puiseux model remain useful finite-
regularity diagnostics, but they are **not** the global theorem target.

---

## 16. Bump realization and the new continuum blocker

E-T4NAT already records that an arbitrary Lorentz metric 2-jet at a point of
\(T^4\) can be realized by a smooth bump-supported perturbation of a constant
Lorentz background while preserving signature.

For a fixed prescribed jet one may choose

\[
g^\sharp=\eta+q
\]

with sufficiently small support so that \(g^\sharp\) is globally as close to
flat in \(C^0\) as desired even when the prescribed curvature jet is not small.

The proof architecture is therefore

\[
j_x^2g
\longrightarrow
g^\sharp=\eta+q
\longrightarrow
\text{sample the entire finite torus}
\longrightarrow
q=q_{\rm IR}+q_{\rm UV}
\]

where the IR/UV split is used **only in the proof**, not inserted into the
physical finite action.

The IR sector uses the uniform low-frequency connection gap.  The UV sector
uses smooth Fourier decay plus the stratified nonlinear branch estimates.

### Order-of-limits requirement

The bump realization must be chosen **once for the prescribed jet**, independent
of the refinement parameter \(L\), and only then sampled as \(L\to\infty\).
Allowing the bump support to shrink with \(L\) would make derivatives of the
bump grow and would require a separate uniform Fourier estimate.

### Asymptotic locality / extension independence

The new continuum-level blocker is to prove that two global smooth
realizations of the same local metric 2-jet give the same reconstructed center
response asymptotically:

\[
j_x^2g^\sharp_1=j_x^2g^\sharp_2
\]

must imply

\[
\boxed{
R_{N,x}[g^\sharp_1]
-
R_{N,x}[g^\sharp_2]
\longrightarrow0.
}
\]

Only then does the reconstructed object factor through the local jet,

\[
E[g](x)=E(j_x^2g),
\]

rather than retain global extension memory.

Flat #201 is a positive control: although connection elimination contains
\(H_{AA}^{-1}\), its leading Schur complement collapses exactly to the local
polynomial Einstein stencil.  The nonlinear theorem must show the analogous
extension independence at the \(J^2\) scale.

Even after extension independence, **frame/grid erasure remains a separate
downstream gate** before the response is metric-only and eligible for the
E-T4NAT/Lovelock route.

---

## 17. Cross-wall hypothesis: parabolic null-line seam

The \(\mathfrak{sim}(2)\) geometry above should be compared with the independent
lower-wall work in PR #202, where parabolic/null-line sectors also produce
affine-residual blindness and quotient incompleteness.

The possible common object is

\[
\boxed{\text{parabolic null-line seam}}
\]

appearing as

\[
\text{connection resonance},
\qquad
\text{star-action flat direction},
\qquad
\text{affine-residual blindness}.
\]

This is currently a **cross-wall hypothesis only**.  No theorem identifying the
#202 and #216 mechanisms is claimed here, and this PR does not edit #202.

If both sides obtain exact compatible stabilizer statements, a separate
theorem task may later unify the upper and lower walls.

---

## 18. Updated gates and execution order

The old next blocker “run the same LS calculation on the other eight \(L=4\)
orbits” is now too narrow.  The durable research order is:

1. **Certificate the chiral/UV geometry:** chiral block split, explicit
   low-frequency gap, and the exact parameterized rank-22
   \((w,w,i,i)\) kernel/source formula.

2. **Certificate the parabolic action-flat identity**
   \[
   S_\star|_{\rm pure\ resonant\ kernel}=0
   \]
   and the \(w=1\) reduced-quartic cancellation
   \[
   V_4^{\rm red}\equiv0.
   \]

3. **Parabolic isolation gate:** compute \(V_6^{\rm red}\), or otherwise prove
   that the reduced unsourced Euler map has isolated zero at the origin.
   If isolated, use local degree rather than source-by-source Newton solves.

4. **Generic rank-22 gate:** derive the parameterized reduced quartic
   \(V_{4,z}\) on the generic \(d_{\rm incompat}=2\) stratum and compute the
   projective critical discriminant/resultant.  This decides whether cubic
   Puiseux rescue is generic and identifies the lower-dimensional degeneracy
   locus.

5. **Uniform stratification gate:** prove a finite resonance stratification
   with a uniform positive Hölder/Łojasiewicz exponent.  Pointwise finite
   visibility order is not enough.

6. **Smooth-sector continuum gate:** combine fixed-bump global sampling,
   IR invertibility, UV super-algebraic tails, and the uniform nonlinear
   estimate to prove resonant corrections are \(o(L^{-2})\).

7. **Asymptotic locality gate:** prove extension independence for two smooth
   realizations of the same local 2-jet.

8. **Frame/grid erasure remains downstream** and is not silently absorbed into
   the resonance theorem.

Until gates 1--7 are closed, retain

\[
\boxed{\texttt{J2-SMOOTH-PARTIAL-CLOSURE}.}
\]

No new filter, no weak-curvature assumption, no all-mode \(C^1\) section, and
no unconditional Einstein equation claim are introduced.

