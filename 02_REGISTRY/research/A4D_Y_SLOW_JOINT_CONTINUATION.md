# A4D Y slow joint continuation

**Task:** \`WRK-A4D-Y-SLOW-JOINT-CONTINUATION\`  
**Lifecycle:** REVIEW
**Research lane:** \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`

## 0. Exact branch terminal

`J2-Y-SLOW-CONNECTION-STATIONARY-RESPONSE-FACTOR-PERSISTS`

The explicit Y carrier has an all-order connection-stationary lift on the
#241/#259 **valued (frozen-cell) affine solder**. Its unrestricted solder Euler
vanishes identically, hence its complete 40-row phase/Gram response vanishes,
with the exact factorization `Delta E_Q = h^2 z R`, `R = 0`. This is an
existence terminal for the corrected Y branch, not a classification of the
three surviving N0 directions. Sections 8-11 give the finite formula, proof,
source contract, uniform limit, and a separate genuinely varying exact-metric
extension. Sections 2-7 retain the lower-order derivation and its historical
blocker; that blocker no longer prevents this branch terminal.

The mixed joint operator has obstruction rank 5 on the eight-real N0 carrier;
its surviving space is
`span{lambda1_COS, lambda3_COS-lambda6_COS, lambda4_COS+lambda6_COS}`.
The formula below supplies a branch through the original Y solution and its
amplitude direction. It does **not** continue the selected roles-2/3 COS ray,
classify the whole surviving space, or close #240's general homogenization
problem. The selected frozen-solder #260 ray remains obstructed as owned there.

## 1. Inputs

This packet consumes only merged owners:

- #232: exact curved nongauge Y-family at flat metric;
- #241: raw valued-slow-background pointwise response;
- #259: exact order-\(h\) connection-stationary lift at fixed microstructure amplitude \(z\);
- #270: moving metric-null Hessian complex;
- #273: direct Schur identification \(K_{\rm Schur}=-\tfrac12K_{G^{(1)}}\).

The primary scaling is

\[
z_h=h.
\]

The distinction between the formal slow parameter \(h\) and the microstructure amplitude \(z\) is essential.  A term that is order \(h^2z\) at fixed \(z\) is order \(h^3\) on the primary scaling.

## 2. First unresolved connection forcing after #259

Re-expanding the literal all-edge connection Euler after the #259 correction gives exactly ten nonzero order-\(h^2\) coefficients at fixed \(z\).

With \(D=3z^2+4\), the phase-1, role-0 entries are

\[
\begin{aligned}
E_{K,K_1}^{(2)}&=\frac{z^2(z-2)}{D^2},\\
E_{K,K_2}^{(2)}&=-\frac{z^2(z-2)}{D^2},\\
E_{K,J_{12}}^{(2)}&=-\frac{2x_0z}{D},\\
E_{K,J_{13}}^{(2)}&=\frac{2x_0z}{D},\\
E_{K,J_{23}}^{(2)}&=\frac{4x_0z}{D},
\end{aligned}
\]

and phase 3 carries the exact negatives.  All other phase/role/generator entries vanish at this order.

At \(z=h\), the boost pair begins only at total order \(h^4\).  The leading unresolved forcing is the total order-\(h^3\) slope term.

## 3. Flat period-4 correction operator

Let \(L_0\) be the real period-4 connection Hessian at the identity connection and standard solder on the 96-dimensional carrier

\[
4\text{ phases}\times4\text{ roles}\times6\text{ Lorentz generators}.
\]

The certificate builds \(2L_0\) as an integer matrix directly from the star pairing and the literal link Euler variation.  It proves

\[
\boxed{\operatorname{rank}L_0=80},
\qquad
\boxed{\dim\ker L_0=16}.
\]

Thus the higher-order connection correction is not unique.  This is the real conjugate-paired diagonal quarter-wave resonance, not a numerical near-kernel.

## 4. Metric readout of the homogeneous freedom

Let \(M_0\) be the pointwise 40-component metric readout on the same real carrier:

\[
4\text{ phases}\times10\text{ Gram directions}.
\]

The exact stacked rank is

\[
\boxed{
\operatorname{rank}
\begin{pmatrix}
L_0\\M_0
\end{pmatrix}
=88.
}
\]

Therefore

\[
\dim(\ker L_0\cap\ker M_0)=8_{\mathbb R},
\]

while \(M_0\) has rank \(8\) on the 16-real-dimensional connection kernel.

Operationally:

- eight homogeneous connection directions are source-visible and cannot be freely added while preserving a fixed smooth metric source at the same normalized order;
- eight are joint-invisible at the linear level.

This is the precise place where connection stationarity alone stops and the metric/source equation starts selecting the sheet.

## 5. Exact identification with #260

The certificate inserts the four complex owned #260 vectors

\[
\begin{array}{c|c|c}
&\text{Role}&(K_1,K_2,K_3,J_{12},J_{13},J_{23})\\ \hline
\lambda_1&0&(0,0,0,1,-1,1)\\
\lambda_3&1&(0,1,-1,0,0,1)\\
\lambda_4&2&(1,0,-1,0,1,0)\\
\lambda_6&3&(1,-1,0,1,0,0)
\end{array}
\]

with cosine dressing \((1,0,-1,0)\) and sine dressing \((0,1,0,-1)\).

These eight real vectors are independent and obey

\[
L_0N_0^{\rm real}=0,
\qquad
M_0N_0^{\rm real}=0.
\]

Since the stacked nullity is exactly eight,

\[
\boxed{
\ker
\begin{pmatrix}
L_0\\M_0
\end{pmatrix}
=
N_0^{\rm real}.
}
\]

So the residual seam after the Y range correction is not a new FUGU sector and not a new letter.  It is exactly the already-owned diagonal source-invisible joint sector.

## 6. The next range correction exists

Factor \(x_0\) out.  On the primary scaling the total order-\(h^3\) forcing is solved by

\[
\boxed{
r_3=
\frac{x_0h^3}{2}
\left[
(K_2-K_3)_{\phi=0}
-
(K_2-K_3)_{\phi=2}
\right].
}
\]

The certificate checks this as an exact integer identity after clearing the common factor four:

\[
L_0r_3+f_3=0.
\]

Thus there is no Fredholm obstruction in the range channel at this order.

## 7. The complete \(h^3\) response cancels

The #259 corrected metric response has, at \(z=h\), a total order-\(h^3\) slope component on Gram entries

\[
(12,13,22,33)
\]

with phase signs \((+,+,-,-)\).

The metric response \(M_0r_3\) is exactly its negative on all four phases and all ten Gram components:

\[
\boxed{
E_Q^{(3)}\big|_{\#259}
+
M_0r_3
=0.
}
\]

Hence the canonical range continuation has no normalized order-\(h\) response:

\[
h^{-2}\Delta E_Q
=
O(h^2)
\]

through the orders controlled here.

This is stronger than the #259 statement \(O(h)\) for its first correction alone.

## 8. Why this is the useful bridge to the stationary-sheet theorem

The stationary-sheet synthesis in #240 says that response variation along a stationary sheet is the obstruction to transporting that sheet horizontally in metric space.

This calculation realizes that statement concretely:

1. the explicit slow forcing is in the range through the next primary-scaling order;
2. its range correction cancels the metric response;
3. the only remaining nonuniqueness is the true joint kernel \(N_0^{\rm real}\).

Thus the possible macroscopic response defect is localized to the nonlinear fate of the joint-invisible seam, not to the generic range variables.

The raw #241 \(-1/4\) pointwise limit was therefore not a stable anomaly.  It disappeared first under #259 stationarity and then again under the next exact range correction.

## 9. Remaining blocker

#260 has already followed the same \(N_0\) sector nonlinearly on the constant solder.  Its current exact state is:

- real cosine/sine rays are curved;
- scalar, connection Euler and metric Euler vanish through degree 4 after the zero-mode and character-\((-1)\) corrections;
- the first missing coefficient is the degree-5 connection Euler of those corrected real rays.

For the present slow-background problem one must additionally include cross terms between:

- the \(O(h)\) Y background microstructure,
- the \(O(h)\) slow Gram value,
- the range corrections above,
- and an \(O(h^2)\) homogeneous \(N_0^{\rm real}\) amplitude.

That nonlinear coupled map is not computed here.  Computing it independently in this PR would duplicate the scientific core of #260.  The next step must consume or coordinate with #260's degree-5 result rather than create a parallel germ convention.

This is the named blocker:

\[
\boxed{
\texttt{Y-SLOW-N0-NONLINEAR-CROSS-TERM-MISSING}.
}
\]

## 10. Boundary

This packet does not prove global response decoupling for arbitrary realizable correlation measures.  It proves a much narrower but constructive statement for the explicit #232 Y family and primary scaling \(z=h\).

No new action term, torsion constraint, selector, Fourier cutoff, finite diffeomorphism gauge, or continuum Einstein theorem is introduced.

## Validation

\`\`\`bash
python3 02_REGISTRY/research/certificates/a4d_y_slow_joint_continuation_check.py
\`\`\`


## 8. Finite formula on the owned valued solder

Write the coframe with columns `s_mu`, and use the exact owner convention

\[
 S(h,b)=I+\frac h2(\alpha\eta)^T+\frac b2(\beta\eta)^T,
 \qquad b=h^2x_0,
 \quad \eta=\operatorname{diag}(1,-1,-1,-1).
\]

Here `x0` is held fixed in the all-edge variation, exactly as in the #259
checker. This distinction matters: `S^T eta S` agrees with the stated
`Q_h = eta + h alpha + h^2 x0 beta` only to first order in the Gram lift.
No assertion below identifies these two matrices to all orders.

Define

\[
 u=s_2-s_1,\quad v=s_3-s_1,\quad
 B=-(uv^T-vu^T)\eta,\qquad k=-\tfrac12\operatorname{tr}(B^2).
\]

Then `B^3=-kB`, and at `h=b=0`, `B=Y`, `k=3`. On this solder,

\[
 k=3+2h+\frac{h^4}{16}-\frac{b^2}{2}-\frac{b^2h^2}{16},
 \qquad \det S=1-\frac{h^2}{4}+\frac{b^2}{4}.
\]

Set

\[
 t=z\left(1-\frac{h(z+2)}4\right),\qquad
 U=\left(I-\frac t2B\right)^{-1}\left(I+\frac t2B\right)
 =I+\frac{4t}{4+kt^2}B+\frac{2t^2}{4+kt^2}B^2.
\]

For `p=sum(x_mu) mod 4`, use

\[
 K_0(x)=(U,I,U^{-1},I)_p,\qquad K_j(x)=I\quad(j=1,2,3).
\]

The amplitude choice fixes the homogeneous Y freedom so that the **entire
fixed-z order-h right-log correction** equals #259, not just its first term
in z. With `D=4+3z^2`, the certificate checks

\[
 U_0^{-1}\partial_hU|_0
 =-\frac{z(z+2)}D J_{12}-\frac{2z^2}D J_{23},
\]
\[
 U_0\partial_h(U^{-1})|_0
 =\frac{z(z+2)}D J_{12}-\frac{2z^2}D J_{13}.
\]

The derivative in `b`, at leading order in `z`, is `(K2-K3)/2`.
Thus `b=h^2 x0`, `z=h` recovers exactly the #275 slope correction
`h^3 x0 (K2-K3)/2`, with its opposite at phase 2. More precisely, the
full difference from the #259 truncated lift at phase 0 is
`h^3 [x0 (K2-K3)/2 - Y/4] + O(h^4)`; the additional `-Y/4` is the allowed
homogeneous, jointly invisible Y direction. The certificate checks the whole
jet, not merely its slope part. Higher coefficients are specified by the
rational formula, rather than left as a formal jet.

For `|h|,|b| <= 1/4`, the difference plane is spacelike, `S` is nondegenerate,
and `k>2`; in particular `4+kt^2 >= 4` for real amplitudes. One way to see the
plane condition is `-<u,u> = 2(1+h/2)^2-b^2/4 > 0`, together with `k>0`.
The formula is consequently analytic on a fixed neighbourhood of the seed.

## 9. Full Euler proof and exact certificate

The theorem is more general: for **any constant nondegenerate coframe with
spacelike difference plane** `span{s2-s1,s3-s1}`, the preceding links are
stationary under all link and all coframe variations.

Spatial faces are flat. Each `(0,j)` face has odd curvature

\[
 F_{0j}(x)=\sigma_p\frac{4t}{4+kt^2}B,
 \qquad \sigma=(1,1,-1,-1),
\]

independently of `j`. Its solder-area sum is

\[
 s_2\wedge s_3-s_1\wedge s_3+s_1\wedge s_2=u\wedge v.
\]

The star pairing with `B` is a multiple of
`(u wedge v) wedge (u wedge v)=0`. At **fixed B and fixed links**, its
variation is also zero, since every summand of
`delta(u wedge v) wedge (u wedge v)` repeats `u` or `v`.
This proves all 16 solder Euler components, not merely a derivative along
the composite map `S -> K(S)` or an averaged scalar.

For the connection Euler, Lorentz covariance reduces the spacelike plane to
`span{e1,e2}`. Use independent real symbols

\[
 s_1=w,\quad s_2=w+(0,a,b_0,0)^T,\quad
 s_3=w+(0,c,d,0)^T,\quad s_0=q,
\]

and the Cayley rotation of `J12`. The checker differentiates **every occurrence
of each edge** in its incident plaquettes using

\[
 \delta F=\tfrac12(\delta P+P^{-1}\delta P P^{-1}),
\]

with `delta K=K X` and `delta K^{-1}=-X K^{-1}` for all six Lorentz generators.
All 96 rational expressions vanish as identities in the independent symbols.
This normal form covers arbitrary lengths and angle of the two differences;
the amplitude absorbs their oriented area. No Fourier projection or averaging
is used. Lorentz invariance follows directly from the bivector metric and star
pairing; it is the ordinary internal Lorentz symmetry, not a claim of finite
coframe/diffeomorphism symmetry.

The same calculation allows **independent time columns q_n and q_(n-1)**
while holding the three spatial columns fixed. Thus it also proves the
nonconstant-coframe theorem used in section 10, with actual incoming-cell
values. It verifies 96 connection equations and 64 unrestricted solder rows.
The metric rows are their prescribed linear combinations; all 40 vanish,
as does every ten-slot readout. The negative control freezes the old Y plane
on `S(h,0)` and recovers the nonzero #259 forcing `2z/(4+3z^2)`.

Reproduce:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_slow_exact_plane_check.py
python3 02_REGISTRY/research/certificates/a4d_y_slow_joint_continuation_check.py
```

The first checker proves the all-order theorem; the second retains the original
Taylor/rank/cross-map calculation. A proof of the full eight-real nonlinear N0
classification is neither required nor supplied for this explicit existence
terminal.

## 10. A genuinely varying extension for the exact metric Q_h

The previous theorem does not silently replace `S(h,h^2*n0)` in every neighbour:
that polynomial coframe has a spatial Gram matrix changing at quadratic order
in `b`, and is not covered by the constant-spatial-Gram argument.
Instead, the **exact stated metric** admits the following separate construction.
Let

\[
 H=\begin{pmatrix}1&-h&0\\-h&1&0\\0&0&1\end{pmatrix},
 \quad T^TT=H,\quad
 w_n=-b_nT^{-T}e_1,\quad
 N_n=\sqrt{1+\frac{b_n^2}{1-h^2}},
\]

where `T` is a fixed positive square root, `|h|<1`, and `b_n=h^2 n0` on an
interior slab (or any periodic sequence on a finite periodic lattice).
Use columns

\[
 \bar s_0(n)=(N_n,w_n)^T,\qquad
 \bar s_j=(0,Te_j)^T.
\]

Their Gram matrix is exactly

\[
 \bar S_n^T\eta\bar S_n
 =\eta+h\alpha+b_n\beta.
\]

The three spatial columns, hence their difference plane and its `B`, are
constant. Section 9 therefore proves exact joint stationarity for the same
four-phase links, with arbitrary neighbouring `b_n`. The identity-link
configuration on this same coframe is also jointly stationary, as follows by
setting `z=0`. There is no fitted source: both configurations solve the fixed
vacuum source contract `T_source=0`.

To express this in a changing internal frame, choose any Lorentz matrices `g_n`
constant on spatial layers and put

\[
 S_n=g_n\bar S_n,\qquad
 K_0(n,p)=g_nW_p g_{n+1}^{-1},\qquad K_j=I.
\]

Neighbour factors cancel inside every plaquette, so its curvature is conjugate
to the time-gauge curvature at its base. Euler transforms covariantly and remains
zero. For example `g_n=exp(b_n K1/2)` and the symmetric `T` reproduce the #259
linear solder jet; they are an exact Gram completion, not an equality with its
quadratic-and-higher polynomial truncation. The background transport
`g_n g_(n+1)^-1` is retained, never discarded. On a finite torus the coframe and
frames must be periodic; the nonperiodic linear profile is asserted only
locally/on an interior slab, without a false wraparound identification.

This profile is a **macroscopically flat metric**. For a smooth `b=b(t)`,

\[
 ds^2=N(t)^2dt^2-
 (dx-H^{-1}b(t)e_1dt)^TH(dx-H^{-1}b(t)e_1dt).
\]

The substitutions `y=x-integral H^-1 b(t)e1 dt` and `tau=integral N(t)dt`
turn it into `d tau^2-dy^T H dy`. This is a computation of the continuum
metric curvature, not an assertion that a finite lattice coframe change is
an exact diffeomorphism gauge. Consequently zero response here does not prove
a curved-background Einstein limit or close #240's general class.

## 11. Source, remainder, and precise terminal boundary

Compare the constructed branch at amplitude `z` with its `z=0` branch on the
**same coframe**. Both connection and solder equations have been solved
independently above at the fixed vacuum source. Their difference is therefore

\[
 \Delta E_Q\equiv0=h^2z\,R,\qquad R\equiv0.
\]

It is not legitimate to infer general homogenization merely because two
unspecified objects were declared to solve the same source equation. Here the
nontrivial result is the explicit existence construction and the full Euler
verification; the zero comparison is its consequence. No identification with a
unique #216 stationary sheet beyond this shared vacuum contract is assumed.
For the same reason, comparison with the #273 low-frequency Schur/Einstein
symbol is zero-versus-zero on this flat metric and yields no extra theorem.

At `z=h`, in every componentwise, maximum, or finite-lattice lp norm,

\[
 \|h^{-2}\Delta E_Q\|=0.
\]

This is a uniform bound, not formal divisibility of a Taylor polynomial.
On each bounded `|x0|<=X` choose `h` small enough that `|h^2x0|<=1/4`;
all denominators of section 8 stay separated from zero. Section 10 has
`N_n>=1` and positive `H` for `|h|<1`, and gives the same exact zero bound
at every interior cell. No unbounded slow remainder is hidden in `R`.

The branch is curved at finite nonzero amplitude: `F_0j` is the displayed
nonzero multiple of `B`. Such curvature cannot be removed by an internal
Lorentz gauge transformation. This is microscopic curvature on a particular
macroscopically flat background.

Closed here: the explicit Y-branch stationary lift, its owned first corrections,
full metric response, and uniform response remainder. Still outside the
terminal: arbitrary slow curved metrics/sources and the global #240 limit;
the other surviving N0 directions; full #260 isolation; the unrelated #202
finite Euler problem. In particular the selected COS roles-2/3 direction
survives the linear cross gate but is not declared nonlinearly continued by
this formula.

### Reproducible mixed-operator ledger

`certificates/a4d_y_slow_joint_cross_matrices.json` contains the full numeric
`2L0`, `2M0`, undoubled `B3`, metric `B3`, `P`, `PB3`, input/output orderings,
all eight connection image witnesses and all three joint image witnesses.
The connection projection has rank zero (all eight directions remain in its
range); the stacked metric condition has obstruction rank five. The zero
connection projection is not misreported as joint solvability.

The checker recomputes and compares the ledger byte-for-byte by default;
`--write` is an explicit regeneration mode. To avoid expanding unused powers
through h^28, `a4d_y_slow_jet_algebra.py` performs exact arithmetic in
`Q(z,x0)[h]/(h^3)` for the #259 next forcing and in `Z[h,a]/(h^2,a^2)` for the
mixed map. In the latter, `a` represents the independent amplitude multiplying
`h^2`; thus its `h*a` coefficient is exactly the desired total-order h^3.
The #259 correction begins at h^2 on z=h and the next range correction at h^3,
so their products with that amplitude start at h^4 and h^5 respectively and
cannot alter B3. Four COS/SIN columns retain direct full rational plaquette
checks of a nonzero connection and metric entry as independent controls.


### Validation and source pins

The inherited mixed-map input is PR #275 head
`1dc1e9e543cb41555d570f65ad472e3c7dbf8a99`; the final branch is refreshed onto
main `25f4796c` (merged #305). The owned #259 script is re-executed, not
replaced by printed expected results. The new plane certificate, full legacy
forcing/rank calculation, mixed-map direct controls, and all image-witness
identities pass. The ledger has rank B3=8, rank metric_B3=7, rank P=16,
rank PB3=0; the joint augmented rank is 93 over a base rank of 88.

Repository, active-work, agent-protocol, generated-view, formalization-debt,
claim-strength, and certificate-freshness guards pass locally. No Lean source
is changed by this task and no new Lean theorem is claimed. Merge/acceptance
remains CONTROL's action; the mathematical terminal has the scope above.
