# Every minimizing stopped Golden branch retains the full source for any fixed T >= 5 and rotation price ell >= 1

20 October 2026. Bounded constructive extension within the existing D0 research
owner #334. This removes the **upper bound on the compiled fixed prefix cost**
from the nonzero-source conclusion of the prospective stopped Golden theorem,
and allows every fixed real per-rotation price `ell>=1`.
It does not supply the compulsory physical task, select Book03 Info, or price
additional moving work. `full_D0_price_selected=false`, `GR_closed=false`.

## 1. Exact input and statement

The input is commit `f22c1864bd85e097166abd75dc048164d8d63c65`, specifically
`A4D_PROSPECTIVE_STOPPED_GOLDEN_MINIMUM_SOURCE_REVERSAL_2026_10_20.md`
and its companion `check_stopped_source_minimum.py`. Byte-identical snapshots,
the observed failed run of the original checker, and a one-target correction
are included in this packet. The original proof's source formulas (8) and (11)
are correct; the last numerical check in the original script has a factor-two
error. Section 7 gives the exact diagnosis.

The reviewed upstream proof at
`1cb164de3753f9dbaf214ea140eb9ea21a7b9d90`, also preserved byte-identically,
supplies the explicit full-work entropy and finite-retained-cutoff bounds
used below. Its corrected checker is not the failed historical snapshot.

Reuse the original same-initial-state, full-work cleanup and actual Golden
reporter. Write

\[
p=\varphi^{-1},\qquad p^2+p=1,\qquad
\sin\theta=p,\quad\cos\theta=\sqrt p,\qquad
q_k=\sin^2(k\theta),\quad k\ge1.
\]

The explicitly declared prospective task repeats the same fresh-work attempt
until the first actual port1. Every failure, the final `10`, and oldRIGHT are
retained. Each attempt pays the same fixed pre-report prefix `T+k ell`, with
fixed price `ell>=1` per original Golden rotation and the original `0/10`
reporter priced separately. Under the whole-pointer Shannon information assignment, the exact
value and inherited first jet at a background `y0` in the common-null stratum
`Sigma` are

\[
S_k(T,\ell)=\frac{T+k\ell+D(q_k)}{q_k},\qquad
D(q)=D_\varphi\bigl(\operatorname{Bern}(q)
                   \Vert\operatorname{Bern}(p^2)\bigr),
\tag{1}
\]
\[
dS_k=-\frac{B_kq_k'}{q_k^2}\,dt,
\quad B_k(T,\ell)=T+k\ell+\log_\varphi\frac{1-q_k}{p},
\quad q_k'=4\cos(k\theta)\sin(k\theta),
\quad dt=\gamma_h\,dJ_2,\quad\gamma_h>0.
\tag{2}
\]

Here `T` and `ell` are **fixed under the field variations being considered**.
Formula (1) is not being asserted as an exact
scalar description of all off-stratum quantum histories: only its owned value
and full first jet at `Sigma` are consumed. The fixed-k actual programmes must
remain admissible near the background for the variational conclusions below.

In particular the actual full-pointer score must retain the conditional work
entropy. The reviewed input gives, for each fixed k and a fixed finite chart,

\[
S_k^{\rm actual}(y)=
\frac{T+k\ell+D(q_k(y))}{q_k(y)}-E_k(y),\qquad
E_k=H_\varphi({\rm work}\mid{\rm stopped\ ports})\ge0,
\]
\[
0\le E_k\le
\frac{h_\varphi(r(t))+r(t)\log_\varphi d}{q_{\min}}
=O(t^4|\log|t||),\qquad r(t)=4t^4(1-t^2),
\quad E_k|_\Sigma=dE_k|_\Sigma=0.
\tag{2a}
\]

Here d is the finite per-attempt work alphabet and `q_min>0` is a local
lower bound for the exact scalar port success probability. Those scalar
port effects make the port sequence law independent of the conditional
logical state; they do not make the remaining work disappear. The bounds
are inherited for each fixed mesh and k, with no uniformity over refinement
or all k asserted. Thus (1)--(2) are exactly the value and first jet of the
actual branches at Sigma; (1) alone is not their full off-stratum score.

If the Info cut also includes quantum oldRIGHT, retain its fixed entropy
baseline and replace E by the conditional classical-work entropy given both
the ports and oldRIGHT. Scalar port effects leave oldRIGHT independent of
the port sequence. The conditional work entropy is nonnegative and no larger
than the bound in (2a), so it likewise has zero first jet. This observation
preserves oldRIGHT; it does not select that Info cut as the physical one.

**Theorem.** For every pair of finite real numbers `T >= 5`, `ell >= 1`, the
minimum of (1) over every integer `k >= 1` exists. Every minimizing integer satisfies

\[
\boxed{\quad k<\frac{T}{12}+\frac{13}{3},\qquad B_k\ge2.\quad}
\tag{3}
\]

Consequently the coefficient `-B_k q_k'/q_k^2` is nonzero for **each** minimizing
branch. Its complete first-source zero equation is precisely

\[
\boxed{\qquad dS_k=0\quad\Longleftrightarrow\quad dJ_2=0.\qquad}
\tag{4}
\]

Equation (4) refers to the full admitted field covectors. It does not assert
that `dS_k` is nonzero at a state where the physical source `dJ2` vanishes.
For `5 <= T <= 50` and every `ell>=1` the minimizing integer is uniquely `k=2`. No uniqueness for
all larger `T`, and no differentiability of a minimum envelope at a tie, is
required for (3) or (4).

## 2. An all-k algebraic separation bound

Put `x=cos(2 theta)=2p-1`, and let `T_k(x)` denote the Chebyshev polynomial.
To avoid confusing this polynomial with the paid prefix `T`, set

\[
A_k=\cos^2(k\theta)=\frac{1+T_k(x)}2.
\]

The recurrence

\[
A_0=1,\quad A_1=p,\qquad
A_{k+1}=2xA_k-A_{k-1}+1-x
\tag{5}
\]

proves `A_k` belongs to `Z[p]` for every k. Equivalently, the Chebyshev
recurrence gives `T_k(2p-1)=1 mod 2` in that ring. Under the nontrivial field
conjugation `p -> -phi`,

\[
x'=-\varphi^3,
\qquad
A_k'=\frac{1+(-1)^k\cosh(k\eta)}2,
\qquad \cosh\eta=\varphi^3,\quad\eta>0.
\tag{6}
\]

For odd positive k, `A_k'<0`; for even positive k, `A_k'>1`. Thus neither
`A_k=0` nor `A_k=1` is possible: either would force its field conjugate to be
the same rational endpoint. Since `A_k` is a squared cosine, this proves
`0<A_k<1` for every k. In particular every `q_k` is strictly between zero and
one and every `q_k'` is nonzero. It also proves the already-owned irrationality
of `theta/pi`: a rational value would give `A_k=1` for some positive k.

The nonzero algebraic integer `A_k` has a nonzero integer norm, so

\[
1\le |N(A_k)|=A_k|A_k'|.
\tag{7}
\]

The absolute value is necessary: the norm is negative when k is odd. For
`u=k eta>0`,

\[
|A_k'|\le\frac{1+\cosh u}{2}<e^u.
\]

Moreover

\[
\cosh(5\log\varphi)-\varphi^3
=\frac{\varphi^5+p^5}{2}-\varphi^3
=\frac{3\sqrt5-4}{2}>0,
\]

so strict monotonicity of cosh on the positive half-line gives
`eta<5 log phi`. Combining these inequalities with (7) yields the universal
separation estimate

\[
\boxed{\qquad 1-q_k=A_k>p^{5k}\qquad(k\ge1).\qquad}
\tag{8}
\]

This is an analytic algebraic-norm argument. No finite enumeration of k, no
numerical Diophantine assumption, and no assumed lower bound on a large-k
trigonometric residual enters it. Therefore

\[
\boxed{\qquad B_k(T,\ell)\ge B_k(T,1)>T-4k+1.\qquad}
\tag{9}
\]

## 3. A finite candidate bound valid for every finite T

Nonnegative relative entropy, `q_k<1` and `ell>=1` imply `S_k(T,ell)>T+k`.
Thus `S_k(T,ell)->infinity` as k tends to infinity for every fixed finite pair.
At least `k=2` is admissible with a finite score, so the discrete minimum
exists.

The additional per-rotation price favors k=2. Indeed, put `R_k=k/q_k`.
Then

\[
R_1-R_2=\frac{2p-1}{2p^3}=\frac12>0,
\qquad R_k>k\ge3>R_2\quad(k\ge3).
\]

Here `R2<13/6<3` follows from `q2>12/13`, proved in (11). Therefore R has the
unique global minimum k=2. The exact decomposition

\[
S_k(T,\ell)=S_k(T,1)+(\ell-1)R_k
\]

shows that any minimizer at price `ell>=1` obeys

\[
S_k(T,1)-S_2(T,1)
\le-(\ell-1)(R_k-R_2)\le0.
\]

This is a **sublevel comparison**, not a claim that k must minimize the
unit-price score. It is precisely what the tail argument needs: every such k
satisfies

\[
k<S_k(T,1)-T\le S_2(T,1)-T.
\tag{10}
\]

Two simple uniform inequalities control this right-hand side. The Bernoulli
relative entropy `D(q)` is strictly convex in `0<q<1` and extends continuously
to endpoints `D(0)=1`, `D(1)=2`; hence `D(q)<2` in the interior. Also

\[
p>\frac8{13},\qquad
q_2=4p^3=8p-4>\frac{12}{13}.
\tag{11}
\]

For example the first strict inequality follows because
`(8/13)^2+8/13-1=-1/169<0` and the Golden polynomial is strictly increasing on
the positive half-line. Therefore

\[
S_2(T,1)-T
<\frac{T+4}{12/13}-T
=\frac{T}{12}+\frac{13}{3}.
\tag{12}
\]

Combining (9) and (12), every minimizing k obeys

\[
B_k>\frac{2T-49}{3}.
\tag{13}
\]

In particular `T>=50` gives `B_k>17`. This is a proof for every finite real T
in that half-line; a gigantic compiled prefix price does not create a missing
upper-bound hypothesis.

## 4. The finite window and the uniform positive bound

The original unit-price all-k comparison on `5<=T<=50` is independently
replayed by the new active checker. Its exact inputs are

\[
q_2=4p^3,\quad 1-q_2=p^6,\quad
D_2=4p^3(\log_\varphi4-1)-5p^6,
\quad 1.497<D_2<1.498.
\]

The logarithmic enclosure uses rational bounds on p and the positive atanh
series with an explicit rational remainder. It gives `S2(5)<9` and
`S2(50)<57`. For every `k>=7`, the lower bound `S_k>=T+k` excludes that k on the
whole window: `S2(T)-T` is increasing and is less than 7 at the upper endpoint.
For `k=1,3,4,5,6`, exact Chebyshev values give `q_k<q_2` and
`(5+k)/q_k>9`. The affine difference `S_k(T)-S_2(T)` has positive slope, so
each such competitor stays strictly above `S2` for all `T>=5`.

Thus the unique unit-price minimizer throughout the window is k=2. Adding
`(ell-1)R_k` preserves its strict advantage for every `ell>=1`. Since

\[
\log_\varphi((1-q_2)/p)=\log_\varphi(p^5)=-5,
\qquad B_2(T,\ell)=T+2\ell-5\ge T-3\ge2,
\]

the window bound and the tail bound `B_k>17` prove (3) for every `T>=5` and
`ell>=1`. The lower bound 2 is attained at `T=5,ell=1,k=2`.

## 5. Ties: what survives, including genuine local minimality

Every minimizing deterministic branch has the nonzero source coefficient
in (2). Distinct k have distinct q values, because equality of two squared
sines would force `(k-l)theta` or `(k+l)theta` to be an integer multiple of pi.
For any fixed ell, their scores are affine functions of T with distinct slopes.
On a bounded interval of T, (12) allows only finitely many candidate k, so the
exceptional T values with ties form a locally finite set. This does not
exclude a tie at a particular physically compiled T.

At a tie, the field minimum envelope need not be differentiable, and opposite
branch derivatives can put zero in a Clarke subgradient even with `dt!=0`.
We do not equate that generalized stationarity with the source equation.

There is nevertheless a direct necessary statement for a **true local
minimum**. Let `y0 in Sigma` and fix T and ell during variation. Suppose the actual
fixed-k scores are defined and admissible near y0, with the inherited full
first jets (2), and let

\[
F(y)=\inf_{k\ge1} S_k^{\mathrm{actual}}(y)
\]

have a local minimum at y0 over the **full allowed field neighborhood**.
This must include the directions transverse to Sigma needed for the claimed
full source; minimization restricted to Sigma would imply only its tangential
restriction. For any branch k active at y0,

\[
S_k^{\mathrm{actual}}(y)\ \ge F(y)\ \ge F(y_0)
=S_k^{\mathrm{actual}}(y_0)
\]

holds in that neighborhood. That fixed branch itself has a local minimum, so
its full differential vanishes. Equations (2)--(3) then force

\[
\boxed{\quad
\text{a true local minimum of the optimized stopped score at }y_0
\quad\Longrightarrow\quad dJ_2(y_0)=0.
\quad}
\tag{14}
\]

This argument does not assume differentiability of F or a uniform first-jet
expansion over all k. It only uses an active differentiable admissible branch.
As usual, obtaining equality rather than one-sided necessary inequalities
requires two-sided variations in the claimed field directions. In particular,
a local minimum relative to an extra boundary constraint has only the
corresponding constrained variational conclusion.

No converse is proved: `dJ2=0` is not shown sufficient for a local minimum, and
the theorem does not prove existence of any physical local minimum. The
elementary envelope `min(u,-u)=-|u|` illustrates why a zero Clarke subgradient
at a downward cusp is not a counterexample to (14).

If a primitive price moves with the field, (2) has an additional term
`(dT+k d ell)/q_k`; an arbitrary such term could cancel the selected coefficient. This
is why the fixed-price assumption and all genuine extra price/Info sources
must remain explicit.

## 6. Exact parent substitution and what remains

The removed premise is: **the actual fixed compiled prefix cost must be at
most 50 in order for stopped prospective minimization to retain the full
original source.** For this defined component model, any finite fixed
`T>=5` suffices, even when the minimizing rotation count changes. The exact
unit-price requirement is also removed: any fixed `ell>=1` is covered.

The retained premises are the genuinely required stopping task, the original
whole-pointer Shannon information cut, the full paid fixed prefix and fixed
G charge at least one, and compatibility of every additional work/preparation/material
source. These are not consequences of the algebraic-norm argument. The
construction uses the already-owned 42-direction `dJ2` first jet; it does not
rebuild geometry, replace the original `H+J+R`, or select a physical task by
declaring its desired source.

Although `B_k>=2` is uniform, the theorem does not give a uniform lower bound
on the entire source coefficient through arbitrary mesh refinement: the factor
`q_k'` and the inherited `gamma_h` can become small. The exact finite-carrier
source zero equation and a uniform continuum estimate are separate claims.

## 7. Reproduction and the upstream factor-two defect

The byte-identical original checker, run under normal Python, exits with
`AssertionError` at its final source comparison. It computes the correct
source but sets its comparison target to `-2/p^(3/2)` at `T=5,ell=1`. Exactly,

\[
\frac{q_2'}{q_2^2}=\frac1{2p^{3/2}},\quad B_2(5)=2,
\qquad dS_2=-p^{-3/2}\,dt.
\]

The corrected copy changes only `target=-D(2)/...` to `target=-D(1)/...`;
the tolerance and every assertion remain byte-identical. That normal-Python
run passes. The source formulas in the original proof already agree with the
corrected target. At `T=3` the exact branch coefficient vanishes, which is a
separate retained hostile control and is outside this theorem's `T>=5` domain.

The upstream issue was concurrently resolved in
`1cb164de3753f9dbaf214ea140eb9ea21a7b9d90`: that version has the correct target
and explicit active checks. This packet preserves the actual f22 failure and
our independently corrected copy as historical evidence. Its one-line patch
is a minimal diff against f22, **not a patch to apply to current upstream**.

`check_stopped_all_cost_source.py` independently executes the rational
finite-window proof, the Golden field identities, the hyperbolic comparison
identity, the tail-bound algebra, and the correct source normalization. All
its checks remain active under `python -O`. Its finite norm examples are
controls of (5)--(8); the universal norm, irrationality and discrete-minimum
arguments are the analytic proofs above. `UPSTREAM_REPRODUCTION.json` and its
logs distinguish the actual failed historical run from the corrected run.
`PROVENANCE.md` lists inputs, exact commands and scope.
