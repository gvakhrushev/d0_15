# D0 → GR: CAR16 two-sided null tomography, chiral correction and GNS conformal response

**Date:** 18 October 2026. **Owner:** bounded mathematical intake for existing Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334), `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. **Status:** EXACT FINITE ALGEBRA / CONDITIONAL GEOMETRIC BRIDGE / PHYSICAL D0→GR OPEN. No claim/BOOK/Lean promotion, no new action, code, matter field, borrowed Einstein dynamics, independent task or gate. The source is the existing CAR16 operator carrier; the projector tests below are algebraically definable but **not proven to be selected native Julia128 pointer events**.

## 0. New consumer of the existing #334 frontier

The full-source owner [§§6.5–6.6](A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md) proves an exact conformal preparation escape of the five-flag AF/star price:

```
mu_(chi,x) = chi_x mu_x,    v_(chi,x) = chi_x^(-1/2) v_x,
T_chi = sum_x sqrt(chi_x) Q_x + sqrt(c_c) Q_c,
F_(mu_chi)(v_chi,U) = F_mu(v,U),
      c_c = (1-sum_x chi_x mu_x)/mu_c > 0.
```

It preserves all 40 AF/star Euler rows, preparation/scene/reference rows on the balanced star root, and fixed collar; yet the original operational coframe metric is `g_chi=chi^(-1) g`, generically **not** Einstein vacuum. This is a direct obstruction to declaring all free-five-cut roots physical GR. Its resolution cannot be a fitted counterterm or an unexplained freeze `chi=1`.

The two-sided native Clifford algebra below provides a useful *kinematic* interface: **one original 16-grade CAR fibre produces exactly nine independent positive null-effect measurements** and an internal 4+12 null-silent/active split, if the relative chirality of its commuting left/right Clifford actions is respected. Its tensor-covector dimension matches the nine-dimensional Lorentz symmetric 2-tensor quotient by the metric. This does not identify its Born probabilities with the matter source. The exact GNS square-root amplitude in the AF counterexample simultaneously has the conformal Einstein-null focusing jet. Together these give one precise coupling test instead of another candidate EH action.

## 1. The same CAR16, not a second independent matter copy

On `H=Lambda^*(R^4)` with the original four A,C,D,B CAR grades and real creation matrices `c_a`, adjoints `c_a^*`, fermion parity `Pi=(-1)^degree`, and `eta=diag(1,-1,-1,-1)`, put

```
L_a = c_a + eta_aa c_a^*,
R_a = (c_a - eta_aa c_a^*) Pi.
```

Actual finite matrices give, for all `a,b`:

```
{L_a,L_b}=2 eta_ab I,   {R_a,R_b}=2 eta_ab I,
[L_a,R_b]=0.
```

The time-spatial bivectors `A_i=L_0 L_i`, `B_i^raw=R_0 R_i`, `i=1,2,3`, are *real self-adjoint involutions*. Within each family they satisfy `{A_i,A_j}=2 delta_ij I`, and the two families commute. Merely treating the raw `B^raw` as the same-chirality Pauli half is **false** on the full CAR16: `sum_i A_i B_i^raw` has eigenvalues `(-3)^2,(-1)^6,(+1)^6,(+3)^2`. This is a substantive anti-chirality control that the uncorrected two-sided rank test misses.

The missing factor is **already internal** to the original CAR algebra:

```
Omega_A = A_1 A_2 A_3,
Omega_B = B_1^raw B_2^raw B_3^raw,
H_rel   = Omega_A Omega_B,
H_rel^*=H_rel, H_rel^2=I, [H_rel,A_i]=[H_rel,B_j^raw]=0,
B_i = -H_rel B_i^raw.
```

The corrected `B_i` remain Hermitian involutions, anticommute within their family and commute with every `A_i`. The sign of this central correction is not an inserted interaction. It is the orientation branch which makes the intended **spin-0⊕spin-1** decomposition on all 16 grades; the opposite sign has no null-silent sector, and the raw algebra has the four eigenvalue classes just stated. The finite matrix checker exercises all three branches. Do **not** infer that D0 operational admissibility uniquely selects this relative chirality sign from Clifford algebra alone.

Set `Sigma=sum_i A_i B_i`. The corrected algebra satisfies the operator polynomial

```
Sigma^2 = 3 I - 2 Sigma.
```

Consequently

```
P_silent = (I-Sigma)/4,      rank=4,
P_active = (3I+Sigma)/4,   rank=12,
P_silent+P_active=I,       P_silent P_active=0.
```

These are *mathematical* singlet/triplet idempotents under the diagonal spatial Pauli action, with fourfold multiplicity inherited from CAR16. They are not a derived catalogue of particles or a selected physical vacuum/matter sector. A rational orientation-preserving spatial rotation in roles 1–2, lifted on the **same** exterior algebra, leaves this split invariant. Arbitrary moving-clock Lorentz-boost covariance, positivity in a changing observer pairing and physical measurement admission remain separate.

## 2. Nine positive null effects and one exact overlap kernel

For a spatial unit direction `s in S^2` in the positive clock frame write

```
A(s) = sum_i s_i A_i,  B(s) = sum_i s_i B_i,
P_ab(s) = (I+a A(s))(I+b B(s))/4,  a,b in {-1,+1}.
```

Both `A(s)` and `B(s)` square to I and commute. Thus the four `P_ab` are mutually orthogonal projections, each of rank 4, and `sum_ab P_ab=I`. No failure/other outcome is deleted. Define **the selected null effect**, not the total Cost−Info,

```
P(s) = P_--(s) = [I-A(s)][I-B(s)]/4.
```

It obeys `P_silent P(s)=0` for **every** direction, and is supported on `P_active`. An *exact trace identity*, checked with all CAR16 grades, is

```
Tr_16[P(s)P(t)] = (1+s·t)^2.                             (N1)
```

The overlap is not an arbitrarily chosen kernel: it follows from the commuting Clifford halves, full trace and the chiral orientation. This is the spin-1 coherent-state overlap times its original fourfold CAR multiplicity. Its spherical polynomial has the harmonics `l=0,1,2`, with dimensions `1+3+5=9`. One-sided `P^L_-(s)=(I-A(s))/2` sees only `1+3=4` operators and cannot reproduce nine tensor components.

Choose the nine *rational* future null directions `k=(1,s)`:

```
(+1,0,0),(-1,0,0), (0,+1,0),(0,-1,0), (0,0,+1),(0,0,-1),
(3/5,4/5,0), (3/5,0,4/5), (0,3/5,4/5).
```

The interpolation matrix with columns

```
1; s1,s2,s3; s1^2-s3^2,s2^2-s3^2,s1*s2,s1*s3,s2*s3
```

has determinant `41472/15625`. The exact Hilbert–Schmidt Gram `K_ij=Tr(P_i P_j)` has determinant

```
48922361856/244140625 != 0.
```

Even the *traceless density-tangent effects* `P_i-I/4` have positive Gram determinant

```
12230590464/244140625 != 0.                              (N2)
```

Therefore on the original faithful state `rho=I_16/16`, the map from **normalized density perturbations** to all nine `dq_i=Tr(drho P_i)` is surjective. The checker constructs an exact traceless symmetric density perturbation for the first unit vector of the nine probabilities, and an explicit small positive definite perturbed density. This is local operational distinguishability, not sourced Einstein dynamics. Duplicating the ninth direction makes the interpolation rank 8 and is rejected.

## 3. A canonical trace-free Lorentz tensor *symbol*, not a new matter law

For any normalized positive `rho` put `q_rho(s)=Tr(rho P(s))`. Define the real moments

```
w = Tr(rho P_active) in [0,1],
v_i = -(1/4) Tr[rho(A_i+B_i)],
C_ij = (1/8) Tr[rho(A_i B_j + A_j B_i)],
Q_ij = C_ij - (delta_ij/3) Tr(C).
```

The full probability polynomial is

```
q_rho(s) = w/3 + v_i s_i + Q_ij s_i s_j,   sum_i Q_ii=0.       (N3)
```

The following symmetric trace-free tensor in the clock frame is its **unique eta-trace-free representative**:

```
tau_00=w/4,
tau_0i=v_i/2,
tau_ij=Q_ij+(w/12) delta_ij,
eta^ab tau_ab=0,
     tau_ab (1,s)^a(1,s)^b = q_rho(s).                      (N4)
```

For every unit `s`, `q_rho(s)>=0` by Born positivity. Thus the tensor symbol satisfies a null-positivity inequality, **but this is not an assertion that general QFT stress or the physical matter stress of D0 must obey it**. It has no proven energy units, canonical normalization, local Ward divergence or independent matter dynamics.

The silent state `rho_silent=P_silent/4` gives `q(s)=0` for every direction and `tau=0`. The active isotropic state `rho_active=P_active/12` gives `q(s)=1/3` and `w=1`. Importantly the **complete** four-outcome distribution for a silent state is `(0,1/2,1/2,0)`, not `(0,0,0,0)` and not a deterministic all-blank event. Its full Shannon or coherent history price can still be nonzero. Zero selected null effect is not zero native Cost−Info; rank births also invalidate a silent C² assumption.

Under proper spatial rotations the exterior lift carries `P(s)` into `P(Os)`, preserving (N1–N4). Full local Lorentz covariance with a **moving positive clock** requires the real observer/adjoint transport of the owned full-Lorentz Julia channel. That is not automatic from SO(3) and cannot be solved by replacing `U^-1` with `U^*`.

## 4. The same square-root GNS amplitude is the conformal focusing scalar

The #334 preparation escape changes the coframe as `e_chi=chi^(-1/2)e`; in the same typing its operational covariant metric is `g_chi=chi^(-1)g`. Let `r=sqrt(chi)>0` and retain the *original* Levi-Civita connection `nabla^g` in the right-hand side. In four dimensions the exact conformal Einstein tensor formula, **without field equations**, implies for every `g`-null `k`:

```
G[g_chi]_(kk) = G[g]_(kk) + 2 r^(-1) Hess_g(r)_(kk).        (N5)
```

Proof: with `sigma=log r`, `g_chi=e^(-2sigma)g`, the Einstein difference equals `2 Hess_g sigma +2 d sigma^2` plus terms proportional to `g`. Null contraction kills the latter and `Hess sigma +d sigma^2 = r^(-1) Hess r`. All orders in sigma are retained.

The exact #334 flat/null conformal counterexample `chi=e^(2 kappa u)`, `g=eta`, gives

```
G[g_chi]_(uu)=2 kappa^2
              =2 r^(-1) partial_u^2 r > 0 for kappa!=0.
```

The checker computes `R_uu=G_uu=2 kappa^2` independently by the **full four-coordinate Christoffel formula** in `ds^2=-2du dv+dx^2+dy^2`, not by assuming an Einstein equation. The square root `r` occurs both in this identity and in the AF/GNS amplitudes `sqrt(chi_x) Q_x`. **Their functional coincidence is exact; the physical identification of this geometric focusing with a price/source of those amplitudes is not proved.**

The compensated null response

```
C_(kk)[g_chi,r] = G[g_chi]_(kk) -2 r^(-1) Hess_g(r)_(kk)
               = G[g]_(kk)
```

is an **identity of two metric descriptions**. It cannot be promoted to D0 dynamics or used to rename the native operational metric into an Einstein-frame metric. Conversely null directions/projectors depend on the conformal cone, not its scale: at fixed CAR matter state and normalized clock direction, `P_chi(s)=P(s)` under the coframe rescaling. Hence a pure angle-based nine-probe measurement cannot *by itself* remove the #334 `chi` degeneracy. A silent `rho` plus nonconstant `chi` explicitly has all nine `q=0` but `G[g_chi]_(uu)!=0`. This is the decisive negative control against the false inference `nine Born zeros => Einstein vacuum`.

## 5. Single mathematically sufficient native exit: the **inherited address Cost−Info**, if admitted

The correct way to try to remove `chi` is not to add a chosen `R`-source. It is to test whether the actual *older, fully retained* history already measures **the same AF/GNS address weights** that the five-cut leaves free. Let positive reference weights `(mu_x,mu_c)` sum to1, with `mu_c>0`, and let `w_chi,x=mu_x chi_x`, `w_chi,c=mu_c c_c=1-sum_x mu_x chi_x`. Conditional on a genuinely inherited complete address measurement with these Born probabilities and a fixed, supplied φ-code `c_i=-log_phi mu_i`, its actual measured average price would have the **computed** form

```
Cost(w_chi)-Info(w_chi)
  =sum_i w_chi,i c_i -H(w_chi)/log(phi)
  =D_KL(w_chi || mu)/log(phi).                           (N6)
```

This equation is an elementary identity for that fully specified code/Info contract. It is **NOT** an assertion that the old 128 words have these probabilities or that D0 selected that complete measurement. In the old owner, `q_rho(word)=mu_PF(word)Tr(rho M_word)`, generally not `mu_PF(word)`. The present five-flag protocol explicitly did not measure the address `x`; adding the distribution (N6) without proving those effect/source identities would violate the existing source firewall.

Nevertheless, (N6) has an unusually sharp consequence **if the binding is proved**. At `chi=1` its first derivative vanishes, and its full Hessian on actual relative GNS variation `xi_x=dchi_x` is

```
D²(Cost-Info)(xi,xi) = (1/log phi) *
    [sum_x mu_x xi_x² + (sum_x mu_x xi_x)²/mu_c] > 0       (N7)
```

for every nonzero xi. Strict convexity/relative-entropy positivity fixes `chi=1` uniquely along the exact compensating orbit of the *same star action*; it does not disturb the existing correct `chi=1` root because its source vanishes there. The checker tests the Hessian with an explicit rational complete-address example. **This is the exact one-scalar-source mechanism capable of killing the explicit non-Einstein #334 family without fitting an Einstein curvature term.** It is conditional on a native inherited-address measurement and its complete price/source, not a suggested insertion of KL by fiat.

There are therefore precisely two admissible **research forks** rather than a fake theorem:

1. **Operational metric really is `g_chi` (as currently typed).** Derive the old address-price binding (N6) as the same history/measurement; then (N7) fixes the conformal weight and removes this known counterexample. The nine projector effects provide the separate candidate null-matter readout, which still needs source conservation/normalization and complete cost compatibility.
2. **The physical clock/rods actually couple to the combined `g=chi g_chi`.** Then the scalar is a potential Weyl compensator, and (N5) explains its null focusing. But the *same experiment's* operational clock and matter response must select that composite metric. Merely noticing action invariance (7.7) cannot turn `chi` into gauge; the old native CAR metric reads `g_chi` and can distinguish it.

Neither fork can infer the full physical Einstein equation without admitting, differentiating and refining the **same complete native price**, as in [strategic synthesis §§7.1–7.4](A4D_STRATEGIC_SYNTHESIS_FOUNDATIONS_TO_GR_2026_10_17.md). The selected naked-star Schur relation is not the full native Hessian; the cubic same-source Ward test, actual finite Lorentz-link rows and matter equations remain open.

## 6. Actionable single-PR consumer and acceptance criteria

The next experiment should not rebuild the Einstein projector or introduce a preferred prior. **On the existing full AF/GNS plus CAR16/reference128 experiment**, test whether the *already retained old history* has a physical pointer effect `E_x` equal, on the very same admitted state and normalization, to the AF address observable `Q_x`, and whether its complete Cost−Info contains the fixed code contribution with the differential (N6). Its source must be differentiated with all work/controller/failure and preparation variations retained. **A mismatch of `E_x` and `Q_x`, or a nonzero residual source, kills fork 1 for this owned programme.** No new task or parallel project is needed until that one native-binding test has a definite input.

In parallel as a bounded algebra-only sublemma, check whether the two commuting Clifford dichotomic measurements `A(s),B(s)` can be implemented *without adding new oracles* from the existing addressed Julia/G/CNOT grammar, with all four outcomes and their execution price. Their mathematical completeness (N1) is proven; their native operational admission is not.

If source binding holds and the compensation is genuinely eliminated, then recover the actual null geometry/matter response and use the nine-direction algebraic lemma (rank9) to reconstruct the tensor only **after** proving the nine scalar field laws. Conservation of the independent matter source then determines the metric-proportional remainder (constant Λ on a connected region). The complete physical route still needs the same-source cubic Ward/refinement/observer sector; finite null tomography is not itself gravitational dynamics.

## 7. Reproduction and hostile controls

Run:

```bash
python3 02_REGISTRY/research/certificates/a4d_two_sided_car_null_tomography_check.py
```

The checker uses exact SymPy rational CAR16 matrices; no floating tolerance, fitted coefficient or external Einstein input. It verifies Clifford anticommutators and left/right commutativity, the nontrivial central chirality correction, `4+12` idempotents, the complete four-outcome projector algebra, rational `SO(3)` covariance on the genuine exterior lift, (N1), the two exact Gram determinants, all nine trace-free null tensor source rows, small-positive-state interpolation, the complete **nonblank** singlet pointer law, and the conformal Christoffel control. It rejects the raw-chirality shortcut, wrong central orientation, one-sided rank4 in place of rank9, repeated ninth ray and `null q=0 => Ricci vacuum` shortcut. The address Fisher Hessian is checked as a conditional algebraic lemma and is *not* treated as an observed code-source identification.

**Terminal:** `CAR16-TWO-SIDED-NINE-NULL-PROJECTORS-EXACT; FOUR-PLUS-TWELVE-CHIRAL-SPLIT; GNS-SQRT-CONFORMAL-FOCUSING-IDENTITY; REAL-ADDRESS-SOURCE-BINDING-OPEN`. Physical D0→GR is OPEN. This research does not change the #334 finite roots, independent AF/star vacuum recovery, original raw `h^-2`/#216 terminal, claims, books or release levels.