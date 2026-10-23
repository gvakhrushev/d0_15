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

The overlap is not an arbitrarily chosen kernel: it follows from the commuting Clifford halves, full trace and the chiral orientation. This is the spin-1 coherent-state overlap times its original fourfold CAR multiplicity. Its spherical polynomial has the harmonics `l=0,1,2`, with dimensions `1+3+5=9`. One-sided `P^L_-(s)=(I-A(s))/2` sees only `1+3=4` operators and cannot reproduce nine tensor components. **Crucial resource limit:** the nine settings are NOT a single compatible measurement. For the two orthogonal axis directions `s=e1`, `t=e2`, `[P(s),P(t)] != 0` and `Tr([P(s),P(t)]^T[P(s),P(t)])=3/2` exactly. Nine settings require separately registered runs or a physically admitted controller/setting register. Their setting probabilities, all four exit outcomes, preparation, work and complete source must be retained. One unknown state cannot be read in nine incompatible bases without such a protocol.

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

## 5. Exact Cost−Info/Info discriminator: KL is NOT the Book action

The next missing scalar may be controlled by old physical history, but the **sign and type of its price are already fixed** by [the pathwise branch-information cocycle](A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md) and [the fixed-AF pointer owner](A4D_AF_FIXED_POINTER_BOOK_INFORMATION_SOURCE_2026_10_17.md). A previous tempting shortcut would have put `D_KL(w||mu)` into the `Cost−Info` action just because the address reference code has `c_i=-log_phi mu_i`. That is **not the native Book pathwise Info law**. Do not perform this substitution.

Let an actual *complete* measured address word distribution be `w=(w_x,w_c)`, normalized, with fixed positive golden/Fibonacci reference `mu=(mu_x,mu_c)`, `sum mu=1`. For the original Book history binding `w=Pr(actual word)` its pathwise information is

```
Cost_i = -log_phi mu_i,
Info_i = log_phi(w_i/mu_i),
Cost_i - Info_i = -log_phi w_i.                           (N6a)
```

Thus, on the **same** complete fixed-round partition,

```
E_w[Cost-Info] = H(w)/log(phi),
E_w[Info]      = D_KL(w||mu)/log(phi),
E_w[Cost]      = [H(w)+D_KL(w||mu)]/log(phi).             (N6b)
```

The alternative mathematical contract `Cost - H(w)/log(phi) = D_KL(w||mu)/log(phi)` treats Shannon entropy as *Info*; (N6a–b) instead give expected surprisal as `Cost−Info`. The former contract could have a strictly positive Fisher Hessian and fix `chi=1`, but **does not follow from Book and cannot be inserted to repair gravity**. These are distinguishable experiments, not naming conventions.

The danger is more precise on the actual #334 conformal orbit. Suppose, *conditionally*, that a previously measured complete native history even had exactly the AF address probabilities

```
w_chi,x=mu_x chi_x,  w_chi,c=1-sum_x mu_x chi_x,
mu_c>0, w_(chi=1)=mu.
```

Then its genuine expected Book price has derivative and Hessian at `chi=1`:

```
D S_Book[ξ] = -[sum_x mu_x log(mu_x/mu_c) ξ_x]/log(phi),
D² S_Book[ξ,ξ] = -[sum_x mu_x ξ_x² +
                      (sum_x mu_x ξ_x)²/mu_c]/log(phi).    (N7)
```

For unequal reference weights, the first source is **NONZERO** at `chi=1`, and the Hessian is strictly **negative**, the exact opposite sign from the attractive but wrong KL-as-action Hessian. Independent free address variations of entropy would instead select uniform *measured* weights (`w_x=w_c`), generally not the unequal golden/Perron profile. An old measured history therefore does **not automatically** fix the conformal mode to the desired Einstein branch. Its actual source may even move the configuration away from that branch. Further real preparation/controller terms can cancel this source only by their own derived equations. The checker confirms (N7) and the distinct positive KL information Hessian on an explicit rational complete address example.

This is a physical-selection distinction, not a no-go for all native histories: the required address distribution and admissible independent ξ are not yet derived for the composed #334 five-cut, and other retained terms must enter the same price.

## 6. The surviving positive route: canonical trace **as an actual preparation marginal**

[The owned AF trace preparation theorem](A4D_NATIVE_AF_TRACE_PREPARATION.md) proves a unique **positive compatible tracial state across the full Fibonacci tower**:

```
tau_n(A,B)=p^(n+1)Tr A+p^(n+2)Tr B.
```

The theorem applies to *tracial compatible states*. It does NOT show that every allowed physical GNS density is tracial, and its owner explicitly exhibits surviving full-state freedom. Nevertheless the conformal obstruction only needs one much narrower interface, not a full density selector. If an independently justified native admission/record compatibility law makes the **actual prepared address marginal** agree with that already-owned trace on the original address projections, then

```
Tr(rho_chi Q_x)=tau(Q_x)=mu_x  for every original address x,
Tr(rho_chi Q_x)=w_chi,x=mu_x chi_x,
mu_x>0  ==>  chi_x=1 for all x.                       (N8)
```

The complement normalization then also fixes `c_c=1`. This removes precisely the known non-Einstein GNS conformal family at **finite** level, without modifying the star action, prescribing a geometric counterterm, or adding a metric-independent choice of uniform probabilities. It is an elementary exact consequence *if* the two lines in (N8) belong to one physically admitted full history. It does not prove their native binding. The compatibility requirement is substantively stronger than the entropy Euler equation (N7) and has a separate preparation/admissibility provenance. The existing PF trace theorem fixes the reference, not all actual prepared-state probabilities.

This leaves two real branches:

- **Trace-selected branch:** show from the actual old retained verification programme that its admissible AF address marginal is constrained by the already-owned compatible trace; consume (N8), so the `chi` escape dies. Then derive and compare the complete nine null field sources of the same process, conserving observer/link/clock/matter and all outcomes.
- **Dynamical-compensator branch:** if physical preparations may vary `chi`, retain `r=sqrt(chi)` as a genuine scalar with its own Euler/source equation. The exact geometric null identity (N5) identifies its necessary focusing correction, but cannot declare `chi g_chi` the physical metric unless the actual rods/clocks/matter readout proves that coupling. Scalar-tensor or Weyl-interpreted gravity is not yet Einstein GR for the original operational metric.

**Single decisive native experiment:** on the same original AF/GNS+CAR16/reference128 full retained process, test whether the *inherited* address projectors/effects register exactly `Q_x` at the original AF carrier and whether genuine admissibility forces their state to be trace-compatible across the Fibonacci inclusions. If either effect identity or tracial-preparation selection fails, (N8) cannot be used. Independently inspect the complete measured entropy source (N7), never a hand-inserted KL term. The original five-flag cut does not measure those addresses, so no automatic inheritance is claimed.

The two-sided CAR projectors form a four-outcome mathematical experiment per direction, but **nine directions are incompatible settings**, and their registration, preparation, code, failure terms, clock and work remain physical inputs. Once the source is derived, their rank-nine map reconstructs the trace-free tensor only **after** actual null field equations are proved. The matter tensor/normalization/divergence and physical nonlinear/refinement bridge remain OPEN, as do #334's remaining Lorentz-link equations and source-preserving cubic Ward test. No new task or parallel action is created in this intake.

## 7. Reproduction and hostile controls

Run:

```bash
python3 02_REGISTRY/research/certificates/a4d_two_sided_car_null_tomography_check.py
```

The checker uses exact SymPy rational CAR16 matrices; no floating tolerance, fitted coefficient or external Einstein input. It verifies Clifford anticommutators and left/right commutativity, the nontrivial central chirality correction, `4+12` idempotents, the complete four-outcome projector algebra, rational `SO(3)` covariance on the genuine exterior lift, (N1), the two exact Gram determinants, all nine trace-free null tensor source rows, small-positive-state interpolation, the complete **nonblank** singlet pointer law, and the conformal Christoffel control. It rejects the raw-chirality shortcut, wrong central orientation, one-sided rank4 in place of rank9, repeated ninth ray and `null q=0 => Ricci vacuum` shortcut. The genuine Book entropy first-source and its negative Hessian are checked against the positive KL/Info Hessian as a hostile source-discriminator; no KL term is treated as the native Cost−Info action.

**Terminal:** `CAR16-TWO-SIDED-NINE-NULL-PROJECTORS-EXACT; FOUR-PLUS-TWELVE-CHIRAL-SPLIT; GNS-SQRT-CONFORMAL-FOCUSING-IDENTITY; TRACIAL-ADDRESS-MARGINAL-ADMISSION-OPEN`. Physical D0→GR is OPEN. This research does not change the #334 finite roots, independent AF/star vacuum recovery, original raw `h^-2`/#216 terminal, claims, books or release levels.