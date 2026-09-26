# MEMO A4D — joint-holonomy affine quotient completeness

**Task:** \`EXP-A4D-JOINT-HOLONOMY-QUOTIENT-COMPLETENESS\`  
**Execution:** PR #186  
**Status:** active EXPENSIVE research  
**Baseline:** \`297067714e7c1a246b06ed981578105c58d9f3db\`

## 0. Current verdict

The two-holonomy translational residual is not merely a witness that one
nongauge affine edge mode can be detected. On an exact generic curved
homogeneous \(L=2\) control, the full family is locally complete on the entire
affine edge-shift quotient.

For each of the sixteen period-two characters \(\chi\), let

\[
D_\chi:V\to V^{\oplus 4}
\]

be the covariant node-difference symbol and let

\[
J_\chi:V^{\oplus4}\to
\bigoplus_{S_1\ne S_2}V
\]

be the linearized map from affine edge shifts to all ordered two-holonomy
residuals

\[
R_{2|1}
=
\det(I-P_1)t_2
-
(I-P_2)\operatorname{adj}(I-P_1)t_1.
\]

Exactly, in every sector,

\[
\boxed{
\operatorname{rank}D_\chi=4,
\qquad
\operatorname{rank}J_\chi=12,
\qquad
J_\chi D_\chi=0.
}
\]

The domain has dimension \(16\). Therefore

\[
\boxed{
\ker J_\chi=\operatorname{im}D_\chi
}
\]

sector by sector.

Summing the sixteen Fourier sectors gives

\[
\boxed{
\operatorname{rank}D_L=64,
\qquad
\operatorname{rank}J=192,
\qquad
\ker J=\operatorname{im}D_L.
}
\]

Hence the full joint residual family detects all \(192\) nongauge affine edge
directions on this exact curved control and kills exactly the \(64\)
node-translation directions.

This is the first exact finite local-completeness result for the translation
quotient in this lane.

The result is not yet a global nonlinear quotient theorem. It is a tangent
classification on a declared homogeneous curved \(L=2\) stratum.

---

## 1. Independent reproduction of the joint residual

For two based affine holonomies

\[
H_i=(P_i,t_i),\qquad i=1,2,
\]

write

\[
M_i=I-P_i,
\qquad
d_i=\det M_i.
\]

Define

\[
q_i^\#=\operatorname{adj}(M_i)t_i.
\]

The polynomial residual anchored on loop 1 is

\[
\boxed{
R_{2|1}
=
d_1t_2-M_2q_1^\#.
}
\]

Under simultaneous affine conjugation

\[
P_i'=gP_ig^{-1},
\qquad
t_i'=gt_i+(I-P_i')c,
\]

one has

\[
(q_1^\#)'=gq_1^\#+d_1c
\]

and therefore

\[
\boxed{
R_{2|1}'=gR_{2|1}.
}
\]

Thus \(R_{2|1}\) is a genuine affine-translation-free Lorentz vector.

The exact checker in this task reconstructs the residual independently; it
does not import the active #185 certificate.

---

## 2. Generic homogeneous \(L=2\) control

Use four constant rational proper-Lorentz positive-direction links

\[
\begin{aligned}
L_A&=BR_{BC},\\
L_B&=BR_{CD},\\
L_C&=R_{CD}R_{BC},\\
L_D&=BR_{BC}R_{CD}B^{-1},
\end{aligned}
\]

where \(B\) is the rational \(A/B\) boost with entries \(5/3,4/3\), and
\(R_{BC},R_{CD}\) are quarter-turn spatial rotations.

Every link satisfies

\[
L_r^T\eta L_r=\eta,
\qquad
\det L_r=1.
\]

For every one of the six plaquette faces,

\[
P_{rs}=L_rL_sL_r^{-1}L_s^{-1}
\]

lies in the generic affine-conjugacy stratum:

\[
\boxed{
\det(I-P_{rs})=-\frac{64}{9}\ne0.
}
\]

So the completeness calculation is not being driven by a singular
single-loop residual.

---

## 3. Momentum-symbol construction

For one character

\[
\chi=(\chi_A,\chi_B,\chi_C,\chi_D),
\qquad
\chi_r\in\{\pm1\},
\]

write the affine edge-shift amplitude as

\[
u=(u_A,u_B,u_C,u_D),
\qquad
u_r\in V.
\]

For face \(S=(r,s)\), the translational part of the based affine plaquette is

\[
t_{rs}=T_{rs}(\chi)u,
\]

with exact \(4\times16\) symbol blocks

\[
T_{rs}^{(r)}
=
I-\chi_sP_{rs}L_s,
\]

\[
T_{rs}^{(s)}
=
\chi_rL_r-P_{rs},
\]

and all other edge-role blocks zero.

The node gauge symbol is

\[
D_\chi\xi
=
\bigl(
(I-\chi_A L_A)\xi,\ldots,
(I-\chi_D L_D)\xi
\bigr).
\]

The checker forms all \(30\) ordered distinct face pairs and therefore a
\(120\times16\) residual symbol \(J_\chi\).

For all sixteen characters, exact DomainMatrix ranks give

\[
\operatorname{rank}D_\chi=4,
\qquad
\operatorname{rank}J_\chi=12.
\]

Direct multiplication gives

\[
J_\chi D_\chi=0.
\]

Since

\[
16-4=12,
\]

gauge inclusion plus the rank equality proves exact quotient completeness.

---

## 4. Genericity rather than one lucky point

The entries of the finite symbols are algebraic functions of the Lorentz link
entries; on the Lorentz group the inverse is polynomial through

\[
L^{-1}=\eta L^T\eta.
\]

Rank \(12\) means that at least one \(12\times12\) minor of every sector symbol
is nonzero on the exact control.

Therefore quotient completeness persists on a nonempty open algebraic
neighborhood of this control inside the homogeneous \(L=2\) Lorentz-link
class, provided the rank-four node-gauge condition remains satisfied.

Thus the correct scope is:

\[
\boxed{
\texttt{JOINT-TWO-HOLONOMY-TRANSLATION-QUOTIENT-LOCALLY-COMPLETE-
ON-A-GENERIC-HOMOGENEOUS-L2-STRATUM}.
}
\]

This is stronger than a single witness and weaker than a global theorem for all
finite link configurations.

---

## 5. Spatial Role orbit decomposition

The spatial stabilizer \(S_3\) fixing Role \(A\) does not make all ordered
face pairs equivalent.

Write \(T\) for faces containing \(A\) and \(S\) for purely spatial faces.
The thirty ordered distinct pairs split into six orbits per site:

| orbit | cardinality |
|---|---:|
| \(T\to T\) | 6 |
| \(S\to S\) | 6 |
| \(T\to S\), incident | 6 |
| \(T\to S\), complementary | 3 |
| \(S\to T\), incident | 6 |
| \(S\to T\), complementary | 3 |

This is already enough to show that spatial Role naturality does not force one
coefficient for the joint-residual action.

On the first exact symmetric control, the global residual-map ranks are

\[
\begin{array}{c|c}
\text{orbit}&\operatorname{rank}\\
\hline
T\to T&112\\
S\to S&112\\
T\to S\ {\rm incident}&192\\
S\to T\ {\rm incident}&192\\
T\to S\ {\rm complementary}&191\\
S\to T\ {\rm complementary}&191.
\end{array}
\]

Thus either incident cross-type orbit alone is sufficient to separate the full
translation quotient on that control.

---

## 6. The attractive checkerboard coincidence is not a theorem

On the first symmetric control the complementary cross-type orbit loses
exactly one quotient rank in the sector

\[
\chi=(-1,-1,+1,+1).
\]

That sector satisfies

\[
\kappa_\eta^2=0
\]

and is exactly one of the three previously owned Lorentz-null checkerboard
characters of the flat star-density Hessian.

An explicit representative of the extra complementary-orbit null class,
after removing a node-gauge representative from the \(A\)-edge block, is

\[
w=
\left(
\begin{array}{c}
0,0,0,0;\\
4/3,5/3,3/8,5/8;\\
-1/2,0,-5/8,-3/8;\\
0,3/8,0,3/8
\end{array}
\right)^T.
\]

Exactly,

\[
J_{\rm comp}w=0,
\]

while

\[
\operatorname{rank}[D_\chi\mid w]=5,
\]

so \(w\) is nongauge, and

\[
J_{\rm incident}w\ne0.
\]

This looked like a possible structural bridge to the old checkerboard
rank-drop.

It fails hostile falsification.

A second exact rational generic link control

\[
\begin{aligned}
\widetilde L_A&=BR_{BC},\\
\widetilde L_B&=BR_{CD},\\
\widetilde L_C&=R_{CD}R_{BC},\\
\widetilde L_D&=BR_{CD}R_{BC}^{-1}
\end{aligned}
\]

again has

\[
\det(I-\widetilde P_{rs})=-64/9
\]

on all six faces, but now every one of the four cross-type orbits has rank
\(12\) in every one of the sixteen momentum sectors.

Therefore

\[
\boxed{
\text{the }(-1,-1,+1,+1)\text{ complement defect is a background-dependent
resonance, not a selector theorem.}
}
\]

The coincidence is worth retaining as a hostile/special control, but it cannot
be promoted to physics.

---

## 7. Quadratic scalar action channels

Because \(R_{2|1}\) is a Lorentz vector,

\[
I^\eta_{2|1}=R_{2|1}^T\eta R_{2|1}
\]

is a full-affine scalar.

For any orbit \(\mathcal O\), define

\[
S^\eta_{\mathcal O}
=
\sum_{x}\sum_{(1,2)\in\mathcal O}
R_{2|1}(x)^T\eta R_{2|1}(x).
\]

On the exact controls, the Hessian of the full equal-weight Lorentz scalar has
the same quotient-complete rank:

\[
\boxed{
\operatorname{rank}H^\eta_\chi=12
}
\]

for every momentum sector.

More strongly, on the hostile generic link control each of the two
pair-exchange-symmetrized cross-type scalars

\[
S^\eta_{\rm inc}
=
S^\eta_{T\to S,\rm inc}
+
S^\eta_{S\to T,\rm inc},
\]

and

\[
S^\eta_{\rm comp}
=
S^\eta_{T\to S,\rm comp}
+
S^\eta_{S\to T,\rm comp}
\]

has rank \(12\) in all sixteen sectors.

Their \(16\times16\) quadratic symbols are exactly linearly independent.

Hence even after imposing anchor/target pair-exchange symmetry, affine gauge
invariance plus quotient completeness leave at least a two-dimensional action
space before overall normalization.

Equivalently, at least one projective modulus survives.

---

## 8. Observer-positive scalar does not remove the ambiguity automatically

With the owned observer metric one may also form

\[
I^n_{2|1}=R_{2|1}^Th_nR_{2|1}.
\]

This is positive for nonzero \(R\) and is full-affine invariant when the
observer is included in the transformed carrier.

However target-loop reversal gives

\[
R_{2^{-1}|1}=-P_2^{-1}R_{2|1}.
\]

Therefore

\[
R^T\eta R
\]

is automatically reversal invariant, whereas

\[
R^Th_nR
\]

is not unless the observer data are transported by an additional compatible
rule.

The exact control gives

\[
I^n_{\rm reversed}-I^n
=
\frac{4096}{9}
\]

at the rest observer, while the Lorentz norm is unchanged.

This task records only the algebraic distinction. It does not claim that the
repository's spatial Role naturality has already imposed target-loop reversal
as an independent axiom. Therefore it does not use this control to eliminate
the \(h_n\) channel globally.

---

## 9. Flat regression

At flat linear holonomy,

\[
P_1=P_2=I.
\]

Then

\[
I-P_i=0,
\qquad
\det(I-P_i)=0,
\qquad
\operatorname{adj}(I-P_i)=0,
\]

so

\[
\boxed{
R_{2|1}=0
}
\]

for arbitrary translational loop data.

More generally, near identity the residual begins at fourth order in
\(M_i=I-P_i\):

\[
R=O(M^4 t).
\]

Consequently any quadratic joint-residual action begins at least at eighth
order in the linear holonomy deviation before its \(t^2\) factor is counted.

The important finite conclusion is simpler:

> a polynomial joint-residual term contributes zero to the accepted flat
> \(L=2\) Hessian.

Therefore it cannot spoil the existing flat star-density result, but the flat
result also cannot normalize its coefficient.

---

## 10. The unavoidable curvature-sector modulus

Suppose the relative-solder branch supplies an affine-invariant base action

\[
S_\star^{\rm rel}
\]

and one adds any nonzero quotient-detecting joint residual scalar \(S_R\).

Then for every real coefficient \(\mu\),

\[
\boxed{
S_\mu
=
S_\star^{\rm rel}
+
\mu S_R
}
\]

is still exactly affine gauge invariant.

Gauge symmetry therefore does not select \(\mu\).

On the generic curved controls, every nonzero coefficient multiplying a
quotient-complete quadratic term removes the accidental relative-solder
edge-diagonal kernel at the tangent level.

But at flat holonomy,

\[
S_R
\]

has zero Hessian, so the already accepted flat rank calculation also does not
select \(\mu\).

Thus current owned principles leave at least one genuine relative
curvature-sector normalization modulus.

The strongest stable statement at this stage is

\[
\boxed{
\texttt{AFFINE-JOINT-RESIDUAL-ACTION-COMPLETION-HAS-UNFIXED-CURVATURE-MODULUS}.
}
\]

This conclusion is independent of whether the final residual aggregate uses
the incident, complementary, observer-positive, or a larger Role-natural
channel family. Those choices can only increase the unresolved selector space
unless an additional principle is supplied.

---

## 11. Consequence for the curved-vacuum question

The next step is **not yet** to solve

\[
\operatorname{EL}_{v^{\rm rel}}=0,
\qquad
\operatorname{EL}_{L}=0
\]

for a unique completed theory.

The Euler system depends on the unfixed relative coefficient \(\mu\) and,
before further selection, on residual orbit/channel weights.

Therefore a curved stationary point found at one arbitrary coefficient would
be a solution of one member of an action family, not yet a prediction of D0.

The correct next research problem is a relative-normalization/selector theorem:

- derive a finite principle that fixes the residual action ray relative to
  \(S_\star^{\rm rel}\); or
- prove that no currently owned symmetry, flat regression, positivity or Role
  naturality can fix it, and register the modulus as an explicit new parameter.

Only after that gate should the nonlinear curved stationary sector be solved.

---

## 12. Scope

This packet does **not** claim:

- global nonlinear affine orbit completeness;
- completeness on arbitrary inhomogeneous lattices or arbitrary \(L\);
- Einstein equations or GR equivalence;
- diffeomorphism symmetry;
- torsion-free/Levi-Civita connection;
- a wave or time interpretation of checkerboard sectors;
- a selected physical value of the new curvature coefficient;
- a unique final action.

No Lean, claim/release, BOOK or public scientific promotion is made.

Exact certificate:

\`02_REGISTRY/research/certificates/a4d_joint_holonomy_quotient_completeness_check.py\`.
