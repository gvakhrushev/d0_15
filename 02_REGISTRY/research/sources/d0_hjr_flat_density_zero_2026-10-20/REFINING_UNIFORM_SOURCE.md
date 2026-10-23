# Uniform full-HJR flat-holonomy source on EVERY refining L >= 11

**20 October 2026 · existing Draft #334 · bounded `constitutive/native_sector` source test.**
Task `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
This strengthens the [exact L8 flat-source gate](RESULT.md) to **all
integer L>=11**, without a numerical limiting fit, a newly assigned physical
action or a change of original Book/GR terminals.

## 1. New exact family and conclusion

Use the unchanged conditional original full-Lorentz positive-adjoint
`H+J+R` price in
[A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md](../../A4D_EXACT_CURVED_WHOLE_HJR_FIXED_COLLAR_ROOT_2026_10_20.md),
equation (1), now with original integer `L>=11`, `h=1/L`,
`p=(sqrt(5)-1)/2`, `alpha=p²h²/128`, `m=256L²`,
`beta=m alpha=2p²`, and `z=2^-20`. Keep every `16L^4`
counting-site/CAR16 mode, the full thermal and feedback traces, the true
shifted adjoint, and the fixed-right complete rank128 Riesz preparation.
The workspace factor `C_L` is field-independent on this declared chart;
no claim about physical clock/work admission is inferred from that choice.

Fix actual proper links `U_r(x)=I`, rest observer and smooth, invertible,
periodic coframes

\[
v_r(s,x)=\frac{s}{4}e_r,\qquad s>0,\qquad u=s^2.
\tag{1}
\]

All ORIGINAL based plaquettes equal I and every original six-face
Palatini density `f_i(v,U)` equals ZERO for **every** s. No face or
coframe area is deleted; this is the flat-holonomy test on the original
field carrier. In particular, for the same chart,
`D_s S_star=0` identically.

**Uniform analytic theorem.** At the *fixed nonsingular* point
`s=1/4`, for every integer `L>=11`, the full Riesz-reduced,
unchanged conditional action satisfies

\[
\boxed{\quad
 \left.\partial_u S_{HJR,L}\right|_{u=1/16}
 \ \ge\ \lambda_{1,L}
 =\frac{L^2}{16}(2-2\cos(2\pi/L))\ \ge 1.
\quad}
\tag{2}
\]

Therefore `D_s S_{HJR,L} >= 1/2` there, **uniform in h**.
The full action is not even `C^1`-approximately equivalent with `o(1)`
error (at the unchanged action/source normalization) to `F(f_1,...,f_n)`
or to a multiple of the original flat Palatini source on a field family
containing (1). This is stronger than the fixed-L8 derivative result:
the mismatch is not automatically erased by increasing `L`.

A source claim restricted to a genuine on-shell subfamily, another
admission domain, or an equivalence on the physical quotient requires its
own proved map; theorem (2) does **not** rule those out.

## 2. The exact Fourier spectrum, including every CAR mode

The original CAR creators, their genuine positive adjoints and commuting
site shifts give the exact full-Fock square

\[
\Delta_L(s,q)=u\lambda_L(q)I_{16},\quad
\lambda_L(q)=\frac{L^2}{16}\,\omega_L(q),\quad
\omega_L(q)=\sum_{r=0}^3[2-2\cos(2\pi q_r/L)]
\tag{3}
\]

for all `q in (Z/LZ)^4`. At every `L>=11`, the lowest positive energy
has exactly the eight momenta `q=+/-e_r`, each of full CAR multiplicity16:
the complete rank128 Riesz shell remains isolated. Its exact fixed-right
stationary preparation contributes `R_L(u)=u lambda_{1,L}`. This
does **not** assert that geometry itself is stationary.

Set

\[
 b_q=1-\alpha u\lambda_L(q)
     =1-\frac{p^2u}{2048}\,\omega_L(q),\quad
 w_q=b_q^{256L^2},\quad Q_L=\sum_q w_q.
\tag{4}
\]

For `u=1/16`, all `b_q\in[1-p²/2048,1]`, so B,F and the original
Julia positive domain remain strict. The **original** scalar action is

\[
S_L(u)=\frac{\log(16C_LQ_L)}{\beta}
 -2048\sum_q\log(1-z+zw_q)+u\lambda_{1,L}.
\tag{5}
\]

The feedback multiplicity `2048=128*16` is not adjustable.
No term involving the actual global `Z=16Q_L` is omitted.
Differentiating (5) gives, *exactly*,

\[
\begin{aligned}
D_u S_L={}&\lambda_{1,L}
 -\frac{\sum_q\lambda_L(q)b_q^{m-1}}{Q_L}\\
&+4096zp^2\sum_q
\frac{\lambda_L(q)b_q^{m-1}}{1-z+z b_q^m}.
\end{aligned}
\tag{6}
\]

Since `0<b_q^m<=1` and hence `1-z+zb_q^m<=1`, (6) proves

\[
D_u S_L\ge\lambda_{1,L}+
\left(4096zp^2-\frac1{Q_L}\right)
\sum_q\lambda_L(q)b_q^{m-1}.
\tag{7}
\]

Thus it suffices to show
\[
Q_L\ge \frac1{4096zp^2}=\frac{256}{p^2}.
\tag{8}
\]
This is the exact *global* normalizer threshold: neither a thermodynamic
mean-field replacement nor a fitted pressure counterterm is used.

## 3. An all-L EXACT rational proof of the partition threshold

For every integer `L>=11` the set `q_r=-5,...,5` embeds as
`11^4` **distinct** actual momenta. At `u=1/16` and
`x_q=p²\omega_L(q)/32768`, the elementary bounds

\[
-\log(1-x)\le \frac{x}{1-x},\qquad
2-2\cos(2\pi k/L)\le(2\pi k/L)^2
\]

give for each embedded `q`:

\[
w_q\ge \exp(-t_*|q|^2),\qquad
t_*=\frac{p^2\pi^2/32}{1-p^2/2048}.
\tag{9}
\]

The following are **exact strict rational bounds**, without any
floating-point oracle:

\[
\frac38<p^2=\frac{3-\sqrt5}{2}<\frac{191}{500},
\qquad \pi<\frac{22}{7},
\qquad
t_*<\frac{5916416}{50166641}<\frac{59}{500}.
\tag{10}
\]

For the p-bounds, use `sqrt5<9/4` and
`sqrt5>559/250`, checked by squaring rational integers.
The pi bound is the classical Archimedean inequality.

Write the exact degree-11 Taylor lower polynomial

\[
P_{11}(x)=\sum_{j=0}^{11}\frac{(-x)^j}{j!},\qquad
e^{-x}\ge P_{11}(x)\quad(x\ge0)
\tag{11}
\]

(the Lagrange remainder is
`+e^{-xi}x^12/12!`). All five values
`P_11((59/500)k²), k=1,...,5`, are strictly positive.
By Cartesian separation,

\[
\begin{aligned}
Q_L&\ge
 \left(1+2\sum_{k=1}^5 e^{-t_*k^2}\right)^4\\
&>
 \underbrace{\left(
1+2\sum_{k=1}^5
P_{11}((59/500)k^2)\right)^4}_{\text{ONE exact rational}}
>\frac{2048}{3}>\frac{256}{p^2}.
\end{aligned}
\tag{12}
\]

The script below verifies the **strict rational comparison** in (12)
without sampling any L. Its decimal display is about 688.469277635861,
versus 2048/3=682.666..., but decimals are not the proof.

Substituting (12) into (7) proves the first inequality of (2).
Finally, for `L>=2`, the elementary bound
`sin(pi/L)>=2/L` shows
\[
\lambda_{1,L}=(L^2/4)\sin^2(\pi/L)\ge1.
\tag{13}
\]
This proves (2) for **every L>=11**, not merely a subsequence or a
numerically checked finite set.

## 4. Actual source topology and the exact physical price test

The tangent `V=dv/ds` has four constant legs `e_r/4`, zero discrete
Lipschitz seminorm and zero link variations. In the **actual coefficient
C1 norm** of the whole-HJR uniform-preparation owner, its size is
`\|V\|_{C1}=1/4`. Equation (2) therefore implies

\[
\|DS_{HJR,L}\|_{(C^1)^*}
\ \ge\frac{|D_s S_{HJR,L}|}{\|V\|_{C^1}}
\ \ge 2
\quad(L\ge11)
\tag{14}
\]

*on this smooth original carrier and in the displayed unscaled full-action
normalization*. The point (1) need not belong to the separately published
small C1 **ball around the v8 stationary root**; (14) does not claim
that it does. It only uses the same coefficient norm definition.

If one selected native complete-price programme genuinely includes
`S_HJR+E_L`, and proposes an off-shell geometric source equality
`DS_{full}=c_L DS_star+o(1)` in this same C1-dual topology
on a domain containing (1), then `DS_star[V]=0` and necessarily

\[
\boxed{D_s E_L\big|_{s=1/4}\le-\frac12+o(1).}
\tag{15}
\]

An additional price with `o(1)` first source in this norm CANNOT
by itself compensate the full HJR pressure. The already-owned
exponentially small compact-flag FIRST source, if someday typed onto
this **same** admitted process, would therefore not cancel (14) alone;
genuinely nonvanishing preparation/work/clock/history or structural
operation sources, a different on-shell physical equivalence, or an
independently derived physical restriction are needed. No cross-carrier
identification with the compact instrument is asserted.

The separately accepted negative second variation on the fixed-L8
curved HJR collar is a **different** second-source gate; it must not be
silently equated with (14). A future selected full physical price must
pass its own genuine admitted-variation/minimality conditions as well.
This advances the named `constitutive/native_sector` comparison by
excluding a shrinking-refinement escape. It does NOT select an original
physical price, prove an Einstein/LC/Palatini source, establish an
interior + exterior global root, or discharge #216/#232, `GR`, or
`raw_response_terminal`.

### 4.1. Exact native Golden flag-only control: it CANNOT screen (2)

Consume the already-owned complete
[Golden flag code/source result](../../A4D_COMPLETE_FLAG_SOURCE_AND_NATIVE_MINIMUM_GATE_2026_10_20.md),
§§2–4. In the **distinct specified compact** original Golden-p
success-count instrument, each good attempt has probability
`g=p²` and code length 2, each bad attempt probability `p`
and code length 1, since `p²+p=1`.
For any fixed finite fully recorded terminating/stopped flag tree,
including every unfinished cap leaf,
\[
w_\gamma=p^{T_\gamma+K_\gamma}
=\varphi^{-\ell_\gamma},
\qquad \ell_\gamma=T_\gamma+K_\gamma,\qquad
\sum_\gamma w_\gamma=1.
\]
Therefore the **literal classical complete-code** source has the
exact identity
\[
\mathbb E_w\ell-H_\varphi(w)=0
\quad\text{for every fixed stopped-tree shape}.
\tag{G1}
\]
This is just the original Golden code, not an asserted definition of
the compulsory native whole price.

More strongly, if all ordered compact letters are the IDENTITY
at the actual flat links `U=I`, their complete chronological isometry
acts on an arbitrarily moving supplied preparation `\psi(s)` as
\[
|\Psi(s)\rangle
=\left(\sum_\gamma\sqrt{w_\gamma}|\gamma\rangle\right)
 \otimes|\psi(s)\rangle.
\]
Thus the **complete FLAG marginal is exactly pure**, independent of
the coframe s, despite retaining all BAD/unfinished branches:
\[
\rho_F(s)=|\phi_w\rangle\langle\phi_w|,\qquad
S(\rho_F)=0,\qquad
\partial_s S(\rho_F)=0.
\tag{G2}
\]
Both the classical code Cost−Info in (G1) and the specified coherent
flag relative-code excess `H_phi(w)-S(rho_F)/log(phi)` have
**zero coframe first source** on this class. A field-dependent
preparation cost, moving structural SELECT, observer/reference/work
action, a changing active gate or a newly admitted controller can
produce a nonzero source, but NONE is inside the *flag-only* statement.

Consequently a proposed physical completion consisting **only** of
this fair original Golden flag code/source on the same flat family
cannot cancel the uniform `D_s S_HJR>=1/2` of (2).
This is a same-field **conditional class-comparison control**, not a
declaration that the Golden instrument is actually the complete
physically selected HJR programme. If the genuine native source uses
coframe-sensitive translation/spectral states or an independently
priced preparation, its source must be explicitly computed instead.
The original Golden two-density six-phase atlas retains full Lorentz
observability on NONTRIVIAL plaquettes; it is not rejected by (G2).

## 5. A well-defined continuum scalar limit (not a GR limit)

For completeness, at fixed `u=1/16>0` the centered Fourier weights
obey an L-independent Gaussian majorant. The exact lattice bound
`\omega_L(q)>=16|q|²/L²` for centered `|q_r|<=L/2`,
together with `b^m<=exp(-m(1-b))`, gives
\[
w_q\le e^{-2p^2u|q|^2}.
\]
Moreover `\lambda_L(q)\le(\pi^2/4)|q|^2`,
and `b_q^{-1}` is uniformly bounded. Dominated convergence therefore
gives the following full-source continuum **scalar expression**:

\[
\begin{gathered}
t=\frac{p^2\pi^2}{2}u,\quad
\Theta(t)=\sum_{k\in\mathbb Z^4}e^{-t|k|^2},
\quad M_2(t)=\sum_{k\in\mathbb Z^4}|k|^2e^{-t|k|^2},\\
\lim_{L\to\infty}\partial_u S_L
=\frac{\pi^2}{4}
-\frac{\pi^2}{4}\frac{M_2(t)}{\Theta(t)}
+1024p^2\pi^2\sum_{k\in\mathbb Z^4}
\frac{z|k|^2e^{-t|k|^2}}{1-z+ze^{-t|k|^2}}.
\tag{16}
\end{gathered}
\]

Equation (2) gives a *strict* lower bound `>= pi²/4` to (16) at
`u=1/16`; the finite-gravity tensor, first-order physical Euler
response and original raw216 normalized norm are **not** being identified
with this scalar limit.

## 6. Deterministic evidence and next consuming substitution

Run `python3 check_refining_uniform_source.py` in this directory.
The checker computes inequalities (10)-(12) with exact
`fractions.Fraction` integer arithmetic; its optional direct Fourier
traces for `L=11,16,24` reproduce the FULL finite `H+J+R` first
source as independent diagnostics. No original certificate ledger, theorem
owner or claimed physical source is changed.

**Required next source calculation:** derive the actual physically
admitted full Cost/Info source on this same *smooth* one-parameter
constant-frame family, and on the separately owned curved collar; compare
the full first jet (15), the curved second-source negative direction and
the boundary traction from the same programme. Any compensation must
follow from the actual paid records, preparation/controller/clock/work
and genuine variations, never a hand-installed counterterm or
coframe-only definition of geometry.

Status: bounded analytic new no-shrinking-source result; physical
admission/selection, uniform joint root, GR and original raw216 OPEN.
