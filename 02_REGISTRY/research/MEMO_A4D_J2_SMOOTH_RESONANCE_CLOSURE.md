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

---

## 19. J² target is already numerical: pressure shifts to theorem closure

The upper-wall target is no longer an unknown continuum tensor.  Conditional on
the surviving smooth-sector theorem, #201 + E-NJET fix the naked-star response

\[
\boxed{
E_\star[g](x)=-\frac12\,G[g](x).
}
\]

On the fixed-\(T^4\) Lovelock/Navarro route this is the ray

\[
\boxed{(a,b)=(-\tfrac12,0)}
\]

for the naked star channel.  The remaining work is therefore not to search for
an Einstein tensor from scratch, but to prove that two effects cannot change
this already-fixed \(J^2\) coefficient:

1. UV resonant connection branching must admit a uniform flat-approaching
   rescue with positive Hölder exponent;
2. the reconstructed center response must forget the chosen global extension
   of the same local metric \(2\)-jet.

Finite curved vacuum existence is a separate lower-wall question.  In
particular, the parabolic action-flat sheet discussed below is not itself a
candidate finite vacuum merely because the restricted star action vanishes.

---

## 20. Shrinking-bump realization inside the nonlinear metric quotient

The earlier fixed-bump route is sufficient in principle, but there is a sharper
local construction which makes the \(J^2\) factorization quantitative.

Let \(h=\varepsilon_N\), let \(J\) be a fixed Lorentz metric \(2\)-jet in
normal coordinates at the center, and let \(P_J(x)\) be its quadratic normal
polynomial.  Choose a smooth cutoff \(\chi\equiv1\) near the origin and

\[
\boxed{
q_h(x)=\chi(x/\rho_h)P_J(x),
\qquad
\rho_h=h^\alpha,
\qquad
\frac12<\alpha<1.
}
\]

Because

\[
\frac{h}{\rho_h}=h^{1-\alpha}\to0,
\]

the complete radius-two finite stencil eventually lies in the region where
\(\chi=1\).  Thus the finite stencil sees the prescribed metric \(2\)-jet
literally, not merely asymptotically.

### 20.1 Nonlinear solder section

With repository convention \(\Theta_{\rm flat}=\eta\), define locally near the
flat metric

\[
\boxed{
\Theta(Q)=(Q\eta)^{1/2}\eta,
}
\]

using the analytic square root near the identity.  Since \(Q\eta\) is
\(\eta\)-self-adjoint, the local analytic square root is also
\(\eta\)-self-adjoint, and therefore

\[
\Theta(Q)\eta\Theta(Q)^T=Q.
\]

For \(Q=\eta+q\),

\[
\Theta(\eta+q)
=
\eta+\frac12q+O(q^2).
\]

Consequently the solder-vector tangent perturbation is

\[
H=\delta\Theta\,\eta
=
\frac12q\eta,
\]

exactly the ten-component metric lift used by #201 to obtain the pure Einstein
flat ray.  Hence the shrinking-bump realization can be placed inside the
actual nonlinear solder/metric quotient rather than an external metric
carrier.

### 20.2 Fourier/Wiener scaling

In four dimensions \(P_J\) is quadratic, so after the rescaling
\(x=\rho_h y\),

\[
q_h(x)=\rho_h^2 f_J(y)
\]

for a fixed compactly supported smooth profile \(f_J\).  Therefore

\[
\boxed{
\|\widehat q_h\|_{\ell^1}=O(\rho_h^2),
}
\]

and for every integer \(m\ge0\),

\[
\boxed{
\sum_n |n|^m|\widehat q_h(n)|
=
O(\rho_h^{2-m}).
}
\]

If the resonance set is separated from \(z=1\), a UV mode satisfies
\(|hn|\ge\theta_0>0\).  Hence

\[
\sum_{\rm UV}|\widehat q_h(n)|
\le
C_m h^m
\sum_n |n|^m|\widehat q_h(n)|
=
O(h^m\rho_h^{2-m}),
\]

that is,

\[
\boxed{
\sum_{\rm UV}|\widehat q_h(n)|
=
O\!\left(h^{2\alpha+m(1-\alpha)}\right).
}
\]

Because \(\alpha<1\), choosing \(m\) arbitrarily large makes the UV source
super-algebraically small in \(h\), even though the bump support itself shrinks.

### 20.3 Candidate \(J^2\) error budget

The flat linear symbol from #201 has the expansion

\[
\mathcal L(\theta)
=
\frac14E_\eta(\theta)+O(|\theta|^3).
\]

After \(h^{-2}\) normalization, the cubic symbol error is bounded by

\[
h^{-2}
O\!\left(
h^3\sum_n |n|^3|\widehat q_h(n)|
\right)
=
\boxed{O(h\rho_h^{-1})}
=
O(h^{1-\alpha}).
\]

A coarse analytic nonlinear remainder controlled quadratically in Wiener norm
has size

\[
O(\|q_h\|_A^2)=O(\rho_h^4),
\]

and therefore contributes after \(h^{-2}\) normalization

\[
\boxed{O(h^{4\alpha-2})}.
\]

Under a uniform UV stationary-rescue estimate, the remaining resonant
contribution is \(O(h^\infty)\).  Thus the candidate theorem has the form

\[
\boxed{
\mathcal E_h(J)
=
-\frac12G(J)
+
O(h^{1-\alpha})
+
O(h^{4\alpha-2})
+
O(h^\infty).
}
\]

The admissible window is exactly

\[
\frac12<\alpha<1.
\]

Balancing the two displayed algebraic errors gives

\[
1-\alpha=4\alpha-2,
\qquad
\boxed{\alpha=\frac35},
\]

and the coarse optimized rate

\[
\boxed{
\mathcal E_h(J)
=
-\frac12G(J)+O(h^{2/5})+O(h^\infty).
}
\]

This is **not yet a theorem**.  It is conditional on a uniform analytic/Wiener
remainder estimate for the actual eliminated finite action, the UV
Hölder/Puiseux rescue, and stability of response reconstruction on the
near-flat chart.

No weak-curvature assumption is introduced: for any fixed finite jet \(J\),

\[
\|q_h\|_\infty
=
O(|J|\rho_h^2)\to0,
\]

so the global realization eventually enters the same near-flat analytic chart.

---

## 21. Replace a global connection function by a stationary correspondence

The finite theory does not need one globally single-valued connection graph
\(K=K_\ast(Q)\).  The natural finite object is the stationary correspondence

\[
\boxed{
\mathscr C_h
=
\{(Q,K):E_K(Q,K)=0\}.
}
\]

On the IR principal stratum the projection
\(\mathscr C_h\to Q\) is locally a graph by the ordinary implicit-function
theorem.  On a UV resonance stratum it can be a branched/Puiseux
correspondence.

Suppose every branch approaching flat satisfies, uniformly on the relevant
stratum,

\[
\|K_h-I\|
\le
C\|s_h\|^\beta,
\qquad
\beta>0.
\]

For the shrinking \(C^\infty\) bump, \(s_h=O(h^\infty)\); hence

\[
K_h-I=O(h^\infty).
\]

Any two flat-approaching UV sheets then differ by \(O(h^\infty)\).  Provided
the reconstructed response is uniformly locally Lipschitz/analytic on the same
near-flat chart, sheet dependence disappears after \(h^{-2}\) normalization.

This suggests the weaker and more natural continuum definition

\[
E(J)
=
\lim_{h\to0}
\mathcal E_h(Q_h^J,K_h)
\]

for **any** flat-approaching stationary branch \(K_h\).  Finite connection
multivaluedness is then compatible with a single-valued \(J^2\) continuum
response.

This does not prove that every arbitrary global smooth sampling sequence has
the same limit; that stronger global-continuum statement can remain separate
from the local equation-class theorem.

---

## 22. Local degree should be used only after isolation

For a real analytic reduced resonant Euler map

\[
F_z:\mathbb R^m\to\mathbb R^m
\]

with odd symmetry \(F_z(-u)=-F_z(u)\), an isolated zero at the origin gives an
odd normalized map on a sufficiently small sphere and hence nonzero local
degree.  Together with a Łojasiewicz inverse estimate this yields

\[
\|u\|
\le
C\|s\|^{1/\nu}
\]

for some finite \(\nu\).

Two scope corrections are essential.

First, the certified diagonal cubic map \(C_3=\nabla V_4\) is **not** isolated
at zero: its projective zero set contains the two coordinate directions
represented by the \(a\)- and \(b\)-axes.  Thus one must not invoke a global
odd-map degree on the whole diagonal \(S^3\).  This does not reopen the
physical diagonal source: the actual \(q_{11}\) source
\(s=(-8,8,0,0)\) already has its independently certified nondegenerate cubic
root.

Second, the degree route is most useful on:

- the generic \(d_{\rm incompat}=2\) stratum after proving the parameterized
  leading quartic Euler map has isolated projective zero away from its explicit
  degeneracy set; and
- the parabolic \(w=1\) stratum after \(V_6^{\rm red}\), or another exact
  argument, isolates the unsourced origin.

If isolation and boundary nonvanishing hold uniformly in a neighborhood of a
compact resonance stratum, Brouwer degree persists under sufficiently small
phase detuning.  A compact resonance variety can then be covered by finitely
many nonlinear LS tubes; the complement uses the ordinary uniform inverse.
This is the intended replacement for pointwise Diophantine estimates on
\(1/\det H\).

---

## 23. Cross-wall exact algebraic lemma: the parabolic null-flag / compound seam

The upper- and lower-wall parabolic mechanisms admit a common algebraic
description that is stronger than the earlier qualitative
“null-line seam” analogy.

Let a nontrivial Lorentz parabolic plaquette be a null rotation

\[
P=e^N,
\qquad
N=n\wedge m,
\]

with

\[
n^2=0,
\qquad
n\cdot m=0,
\qquad
m^2\ne0.
\]

As an endomorphism,

\[
N^2=-m^2\,n\otimes n^\flat,
\qquad
N^3=0,
\]

so

\[
P=I+N+\frac12N^2.
\]

Set

\[
A=I-P.
\]

Then

\[
A=-N\left(I+\frac12N\right),
\]

where the factor in parentheses is invertible.  Therefore

\[
\boxed{
\operatorname{im}A
=
\operatorname{im}N
=
\operatorname{span}\{n,m\}
=:\Pi.
}
\]

Moreover,

\[
\boxed{
A^2=N^2,
\qquad
\operatorname{im}A^2
=
\operatorname{span}\{n\}
=:\ell.
}
\]

Thus every nontrivial rank-two parabolic plaquette canonically determines the
null flag

\[
\boxed{\ell\subset\Pi}
\]

directly from \(P\).  At \(P=I\) scalar invariants lose this datum.  The natural
resolved carrier is therefore the graph closure of

\[
P
\longmapsto
\left(
\operatorname{im}(I-P)^2
\subset
\operatorname{im}(I-P)
\right).
\]

Over the flat point the exceptional fibre is the space of null flags.  Its
expected real dimension is \(2+1=3\): two parameters for a projective null line
and one for a transverse direction in \(\ell^\perp/\ell\).

### 23.1 Rank-adapted compound residual

The old joint residual uses top exterior compounds:
\(\det A=\wedge^4A\) and \(\operatorname{adj}A\), Hodge-dual to the third
compound.  These vanish automatically when \(\operatorname{rank}A=2\).

For a fixed rank-\(r\) stratum define instead

\[
\boxed{
\mathcal Q_r(A,t):
\Lambda^rV\to\Lambda^{r+1}V,
\qquad
\omega\longmapsto
t\wedge(\wedge^rA)\omega.
}
\]

Under affine node translation

\[
t\longmapsto t+Ac
\]

one has

\[
(Ac)\wedge(\wedge^rA)\omega=0,
\]

because all \(r+1\) factors lie in the \(r\)-dimensional
\(\operatorname{im}A\).  Hence

\[
\boxed{
\mathcal Q_r(A,t+Ac)=\mathcal Q_r(A,t).
}
\]

If \(\operatorname{rank}A=r\), then
\(\operatorname{im}(\wedge^rA)=\wedge^r\operatorname{im}A\) is a nonzero line,
and therefore

\[
\boxed{
\mathcal Q_r(A,t)=0
\iff
t\in\operatorname{im}A.
}
\]

So \(\mathcal Q_r\) is a complete polynomial tensor detector of the affine
translation coset on a fixed-rank stratum.

For the parabolic seam,

\[
\boxed{
\mathcal Q_2(A,t)
=
t\wedge(\wedge^2A)
}
\]

survives exactly where the determinant/adjugate residual becomes blind, while
\([\operatorname{im}\wedge^2A]\) is the Plücker coordinate of the degenerate
plane \(\Pi\).

This is an **affine-quotient detector / resolution candidate**, not a new term
in the physical action and not a new \(I\)-channel.  The general algebraic
lemma is elementary; ownership of its role in the selected D0 quotient still
requires a lower-wall certificate and compatibility check with the existing
Grassmann graph-closure machinery.

---

## 24. Revised pressure after the new synthesis

The shortest route to the naked-star \(J^2\) theorem is now:

1. **UV rescue, not orbit enumeration.**  Prove isolation/degree/Hölder control
   on a finite compact resonance stratification.  The diagonal physical source
   is already closed; \(V_6\) on the parabolic \(w=1\) stratum is a \(J^2\)
   isolation problem, not a search for a finite vacuum on the action-flat
   sheet.

2. **Shrinking-bump estimate.**  Promote §20 from a scaling calculation to a
   theorem for the actual eliminated finite response, including the
   \(O(h^{1-\alpha})\), \(O(h^{4\alpha-2})\), and \(O(h^\infty)\) pieces.

3. **Branch independence / locality.**  Prove that the limit is independent of
   UV stationary sheet and of the smooth realization of the same local
   \(2\)-jet.  The local shrinking-bump construction can establish the equation
   class before the stronger arbitrary-global-sampling theorem.

4. **Lower wall separately:** on PR #202, prove that the six transverse Euler
   numerators on the reconstructed four-parameter parabolic family vanish only
   on the flat locus.  If so, stop searching for a finite curved vacuum on that
   sheet and move the finite-vacuum search to its complement.

5. **Compound seam:** certificate \(\mathcal Q_2\) and the recovered flag
   \(\ell\subset\Pi\) as a rank-two affine-quotient resolution mechanism before
   deciding whether it changes any lower-wall physical carrier.

Until the UV rescue and locality/branch-independence gates close, retain

\[
\boxed{\texttt{J2-SMOOTH-PARTIAL-CLOSURE}.}
\]

The target coefficient itself is already fixed:

\[
\boxed{E_\star=-\frac12G}
\]

for the naked star channel, conditional only on these remaining bridge gates.

---

## 25. Rank-adapted affine quotient: complete fixed-rank coordinate lemma

Section 23.1 recorded the rank-adapted compound detector.  The stronger
fixed-rank statement needed for the lower-wall seam is as follows.

Let

\[
H=(P,t),\qquad M:=I-P,\qquad \operatorname{rank}M=r,
\]

and define

\[
\boxed{
\Psi_r(M,t)
:=
\bigl[
\omega\mapsto t\wedge(\Lambda^rM)\omega
\bigr]
\in
\operatorname{Hom}(\Lambda^rV,\Lambda^{r+1}V).
}
\]

Under node translation \(t\mapsto t+Mc\),

\[
(Mc)\wedge(\Lambda^rM)\omega=0
\]

because all \(r+1\) factors lie in the \(r\)-plane
\(\Pi=\operatorname{im}M\).  Hence

\[
\boxed{\Psi_r(M,t+Mc)=\Psi_r(M,t).}
\]

Under a Lorentz change of frame

\[
M'=gMg^{-1},
\qquad
t'=gt+M'c,
\]

naturality of exterior powers gives

\[
\boxed{
\Psi_r(M',t')
=
(\Lambda^{r+1}g)\,
\Psi_r(M,t)\,
(\Lambda^rg^{-1}).
}
\]

Because \(\operatorname{rank}M=r\),
\(\operatorname{im}\Lambda^rM=\Lambda^r\Pi\) is a nonzero line.  Therefore

\[
\boxed{
\Psi_r(M,t)=0
\iff
t\in\operatorname{im}M.
}
\]

More strongly,

\[
\boxed{
\Psi_r(M,t)=\Psi_r(M,t')
\iff
t-t'\in\operatorname{im}M.
}
\]

Thus on every fixed-rank stratum \(\Psi_r\) gives a canonical injective
coordinate map

\[
\boxed{
V/\operatorname{im}M
\hookrightarrow
\operatorname{Hom}(\Lambda^rV,\Lambda^{r+1}V)
}
\]

without choosing a quotient basis.

In four dimensions the hierarchy is:

\[
\begin{array}{c|c}
r & \dim\operatorname{coker}M\\ \hline
4&0\\
3&1\\
2&2\\
1&3\\
0&4
\end{array}
\]

with \(\Psi_0=t\), while the familiar adjugate/cofactor construction is the
\(r=3\) Hodge-dual member of the same hierarchy.

This identifies the precise mechanism behind the parabolic blindness:
determinant and adjugate are the \(r=4,3\) compounds, but the null-rotation
stratum has true rank \(r=2\).

### 25.1 Null flag is already contained in the Plücker plane

For a nonzero Lorentz parabolic plane

\[
\Pi=\operatorname{im}(I-P)
\]

the null line satisfies

\[
\boxed{
\ell=\operatorname{rad}\Pi
=
\Pi\cap\Pi^\perp.
}
\]

Consequently the projective top nonzero compound

\[
\boxed{
[\operatorname{im}\Lambda^2(I-P)]
=
[\Lambda^2\Pi]
}
\]

already determines the whole null flag \(\ell\subset\Pi\); the operator
\((I-P)^2\) is an algebraic extractor of \(\ell\), not extra independent
memory.

This matches the existing graph-closure architecture: a rank-changing seam is
naturally remembered by the **top nonzero exterior compound**.  The earlier
rank-four gauge-image incidence used the top nonzero compound of its carrier;
the parabolic holonomy seam uses \([\Lambda^2(I-P)]\).

Scope is essential: \(\Psi_2\) is a rank-stratified quotient coordinate, not a
globally translation-invariant tensor across higher-rank strata.  If
\(\operatorname{rank}M>r\), the term
\((Mc)\wedge\Lambda^rM\) need not vanish.  This is compatible with the existing
single-loop no-go and is exactly why graph closure / resolved rank strata are
the appropriate carrier.

A positive observer diagnostic such as

\[
\|\Psi_2(M,t)\|_{h_n}^2
\]

may be used on the rank-two stratum and vanishes exactly on the trivial cokernel
class, but **must not be inserted into the #202 action merely because it is
available**.

---

## 26. Two-bump locality is a corollary of the same UV theorem

Take two shrinking realizations of the same fixed metric \(2\)-jet \(J\),

\[
q_h^{(i)}
=
\chi_i(x/\rho_{h,i})P_J(x),
\qquad
\rho_{h,i}=h^{\alpha_i},
\qquad
\frac12<\alpha_i<1.
\]

For sufficiently small \(h\), both cutoffs equal one on the complete
radius-two stencil.  Hence the owned centered Einstein stencil sees the same
quadratic polynomial **exactly** in the two realizations; the leading
\(\frac14E_{\eta,h}\) contribution at the center is identical before taking a
limit.

Under the uniform UV Hölder-rescue theorem, the remaining difference is bounded
by

\[
O(h^{1-\alpha_1})+O(h^{1-\alpha_2})
+
O(h^{4\alpha_1-2})+O(h^{4\alpha_2-2})
+
O(h^\infty),
\]

and therefore

\[
\boxed{
\mathcal E_h^{\chi_1,\alpha_1}(J)
-
\mathcal E_h^{\chi_2,\alpha_2}(J)
\longrightarrow0.
}
\]

Thus **bump-profile independence is not a second independent large search**.
For this local \(J^2\) construction it is a corollary of:

1. exact agreement of the local quadratic stencil;
2. the analytic/Wiener remainder bounds of §20;
3. one uniform UV Hölder theorem.

A stronger theorem covering arbitrary fixed global smooth sampling sequences
can remain downstream; it is not required to identify the local naked-star
equation class.

---

## 27. The upper-wall blocker can be stated as uniform flat isolation

Let \(Z\) be the compact resonance variety separated from the IR neighborhood,
and after gauge/range reduction let a connected resonance stratum
\(Z_\sigma\) carry a finite-dimensional real-analytic reduced equation

\[
F_\sigma(z,u,s)=0.
\]

The sufficient upper-wall theorem is:

\[
\boxed{
F_\sigma(z,u,0)=0,\quad |u|<\varepsilon
\Longrightarrow
u=0
\quad\text{uniformly for }z\in Z_\sigma,
}
\]

together with

\[
\boxed{
\deg_0F_\sigma(z,\cdot,0)\ne0.
}
\]

Uniform isolation plus compact real-analytic/subanalytic Łojasiewicz control
then gives some stratum-wise positive exponent

\[
\beta_\sigma>0,
\qquad
|u|\le C|s|^{\beta_\sigma}.
\]

For \(C^\infty\) sampling the numerical value of
\(\beta_\sigma\) is immaterial: every fixed positive exponent preserves the
super-algebraic UV suppression.

If isolation and boundary nonvanishing hold continuously on a connected
stratum, local degree is constant until a zero crosses the chosen boundary
sphere.  Hence the target is **connected resonance strata**, not lattice
orbits.

Equivalently, a failure of uniform flat isolation would produce a sequence

\[
z_k\to z_\ast,
\qquad
u_k\to0,
\qquad
u_k\ne0,
\qquad
F(z_k,u_k,0)=0.
\]

Under the semialgebraic/subanalytic hypotheses of the reduced finite system,
curve selection then produces a nontrivial zero-source stationary germ
entering the flat point.

Therefore the actual obstruction to the \(J^2\) theorem is

\[
\boxed{
\text{a nontrivial zero-source stationary germ accumulating at flat},
}
\]

not the existence of finite curved stationary points elsewhere.

A disconnected finite-amplitude curved vacuum bounded away from the flat
solution does **not** obstruct the local \(J^2\) theorem.

---

## 28. Live lower-wall update: exact enlarged parabolic family and the new cross-wall question

PR #202 has now exactified the enlarged E(2) pattern

\[
e_2=
(\alpha,\beta,j,\;
 \alpha,\beta,j,\;
 \gamma,\delta,0,\;
 \delta,-\gamma,0)
\]

on the lean \(L\equiv0\), \(D=(1,1,1)\), \(U=0\) packing.  On the exact
subfamily

\[
\boxed{\alpha=\beta=0}
\]

the six transverse equations vanish symbolically, the twelve free-internal
E(2) derivatives vanish on the exact rational certificate battery, and the
witness

\[
(j,\gamma,\delta)=(2,0,1)
\]

has

\[
\boxed{\mathrm{curv}^2=32}
\]

with exact \(12+6\) residual zero in the declared packing.

This supersedes the earlier broad statement that the whole parabolic sector
should be excluded as a finite vacuum.  The narrower complement-zero
four-parameter leaf remains flat-only on the certified slices, but the enlarged
parabolic carrier contains an exact curved stationary family in the currently
tested residual package.

For the upper wall, however, existence of this family is not by itself a
problem.  The cross-wall question is now sharper:

\[
\boxed{
\text{does the exact #202 family define a nontrivial physical stationary germ
approaching the flat quotient?}
}
\]

In particular, sending \((\gamma,\delta)\to(0,0)\) while keeping \(j\ne0\)
kills the sampled curvature in the current certificate, but one must determine
whether the remaining \(j\)-holonomy is physically flat/gauge in the selected
quotient or retains a nontrivial finite holonomy class.  Conversely, a scaling
in which all physical holonomy and residual data approach the flat quotient
would be directly relevant to the uniform-isolation theorem above.

Thus #202 now carries two logically distinct questions:

1. **finite vacuum:** does the exact family survive the full classical
   internal equations, channel response \(R=R_\ast(C)\), and hostile \(L=3\)
   gate?
2. **upper-wall isolation:** regardless of finite-vacuum survival, can any
   nontrivial member or continuation of the family accumulate at the flat
   physical quotient?

Only the second question is load-bearing for the naked-star \(J^2\) theorem.

