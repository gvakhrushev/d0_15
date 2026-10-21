# Weighted Einstein-matter source: exact finite Ward defect on the original 16+24+2 carrier

21 October 2026. Existing scientific owner PR #334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, `constitutive/native-programme-v1`.
Pinned input: `401eafb2958e9d9626db833a25f02b35b3871c16`.

**Consumer:** section 9 of `WEIGHTED_WARD_AND_DUST.md` in this directory. That owner already proves the weighted continuum law and states a finite Ward defect as the next missing calculation. This continuation computes BOTH defect covectors on the actual six-face star and original forward scalar stencil, instead of assuming a finite diffeomorphism symmetry. It also records the precise two-scalar interpretation of the continuum equations.

No new detector, fundamental action, field writer, primitive price, root family, or physical GR acceptance is introduced. `GR_closed=false`.

## 0. Reconstruction and publication status

The previous chat described a weighted result without publishing its own code and mentioned 65 checks. That historical checker/receipt was NOT recovered. The current branch independently contains the substantive weighted theorem, its checker and review; they are consumed, not duplicated or claimed as a second discovery. The present files and JSON outputs are NEW actual replays. The prior 65-check statement is not used as evidence.

The convention is fixed once: `y=+tau*q/rho`, with the physical orientation already inside `F(x,y)=-alpha*beta*[h_phi(r(x,-y))-h_phi(r0)]`. Combining a negative y with this reflected F would change the source. The earlier chat's shorthand must not be used to mix those conventions.

## 1. Existing weighted continuum result, with both fields retained

The specified complete cap-one CQ field price is

`S=B0+M integral rho(z) F(tau eR/rho,tau q/rho) d^4z`,
`q=sum_(A=0,4) g^(mu nu) partial_mu psi_A partial_nu psi_A`.

On its declared fixed-cost field chart `D_field B0=0`. Actual independent upstream derivatives are not thereby zero. The continuum proof varies the original independent coframe, Lorentz connection and both real scalars before restricting fields. With `P=F-xF_x`, its exact identities are

`dP+yF_y dlog rho=0`, `T:=xF_x-yF_y=0`.

The useful off-shell algebra is

`dP+yF_y dlog rho = (F_x F_y/rho) d(rho y/F_x) - (T/F_x)dF_x`.       (1)

No division by y is made. Thus the invariant is valid through the null branch. The previously established stationary coframe map `g_E=U g`, `U=F_x/a>0`, `a=F_x(0,0)`, identifies it with

`rho y/F_x=(tau/a) Q_E`, hence `dQ_E=0`.

This is a theorem for the specified continuum dictionary, not an automatically admitted finite-lattice Lie variation.

### Two-scalar comparison, not a new physical action

The same stationary reduction gives

`S_eff=B0+M tau a integral e_E R(e_E,omega) + M integral rho K(tau Q_E/rho)`.

Let `k=K'(tau Q_E/rho)` and `mu=-k/(a e_E)>0` in the owned small chart. Its full reduced equations are

`G_ab=mu sum_A partial_a psi_A partial_b psi_A`,
`J_A:=nabla_a(mu partial^a psi_A)=0`, `Q_E=q_*` constant.

They are precisely the constrained Einstein equations of the COMPARISON functional

`I_*=integral e_E [R-mu(Q_E-q_*)]`                                 (2)

on solutions also satisfying the original coordinate/volume binding

`e_E mu=-K'(tau q_*/rho)/a`.                                      (3)

Here (2) is only a representation of the resulting equation class. It is not substituted for the paid CQ price, and its multiplier is not asserted to be a new native degree of freedom. Variation of mu gives Q_E=q_*; metric variation then eliminates the pressure term proportional to Q_E-q_*. Both original material components remain. Their quadratic stress can have rank two, so it is not generally a single dust. Stability and degrees of freedom are not inferred by analogy with mimetic models. Background context: Shen--Zheng--Li, arXiv:1909.01248, is a separate two-field analysis, not a D0 proof.

The full off-shell residual identity, with `E_ab=G_ab-mu sum_A partial_a psi_A partial_b psi_A`, is

`(mu/2) partial_b Q_E = -nabla^a E_ab -sum_A J_A partial_b psi_A`.   (4)

All derivatives of mu, including rho, are retained in J_A. Thus nonzero actual field residuals drive the kinetic-constraint defect; they cannot be discarded by invoking Bianchi only on part of the source.

The converse is local: for any smooth solution of (2) with mu>0, fixed q_* and operands in the common chart, matching the positive volume form `mu vol_g` to the prescribed positive density in (3) gives a local coordinate representative of the reduced price. A one-coordinate integral constructs that map after shrinking the box. Both scalars pull back; they need not both be kept as coordinate labels. Time-dependent shifts and transformed collars must be retained. The stationary auxiliary inverse then reconstructs the original variables. Arbitrary coordinate relabeling is not proved to be a physical gauge of the finite execution. On nonnull fields the original metric is generally `U^-1 g_E` and its independent connection has the already-owned vector torsion; on the null branch U=1.

## 2. Exact original finite dictionary and legitimate test tangent

At each site use the ORIGINAL operational coframe `e^a_mu`, independent proper links U_mu and both real scalar/top fields. Put

`G=(e^T eta e)^-1`, `w_(A,mu)=D_mu^+ psi_A`,
`q=sum_A G^(mu nu) w_(A,mu) w_(A,nu)`.

`eta=diag(1,-1,-1,-1)` is the literal rest-basis form; no positive-Hilbert norm is substituted. The independent matter stencil is the same forward difference in the owner.

Take a compact/collar-compatible lattice vector xi. The sampled Lie TEST is

`delta e^a_mu = xi^alpha D_alpha^+ e^a_mu + e^a_alpha D_mu^+ xi^alpha`,
`delta psi_A = xi^alpha D_alpha^+ psi_A`.                            (5)

For the link test, in a strict near-identity chart write `U_r=exp(h Omega_r)`, with the six exact eta-skew generators `G_k`. Use

`V_r=xi^alpha D_alpha^+ Omega_r + Omega_alpha D_r^+ xi^alpha`,
`delta U_r=h V_r U_r`.                                             (6)

This is an actual left proper-link tangent on ALL24 link coordinates. It is a first-order consistent sample of the continuum connection Lie derivative, NOT a claim that left multiplication equals the exact derivative of `exp(h Omega)` at finite h. The latter difference is O(h^2) on bounded smooth charts. Formula (6) is the declared finite test used throughout; no hidden exact lattice coordinate symmetry is assumed. Algebraic availability of these field tangents is not physical gate/field-writer admission.

Use periodic sums for the replay or complete stencil collars with the actual boundary terms zero. Zero-padding a nonzero field or dropping predecessors changes the identity.

## 3. Closed material defect: the missing finite product and inverse rules

For each direction alpha define the exact inverse-metric chain defect

`B_alpha = D_eG[D_alpha^+ e] - D_alpha^+G`,
`L_alpha=(D_alpha e)^T eta e+e^T eta (D_alpha e)`,
`H_alpha=(D_alpha e)^T eta (D_alpha e)`.

The inverse identity gives EXACTLY

`B_alpha = h[(D_alpha^+G) L_alpha G + G_(+alpha) H_alpha G]`.         (7)

Products are ordered matrix products. This does not use commuting coframes.

Define scalar C_alpha and tensor R_(nu,alpha) by

`C_alpha=sum_A { B_alpha(w_A,w_A)
 -h G(D_alpha w_A,D_alpha w_A)
 -2h (D_alpha G)(w_A,D_alpha w_A)
 -h^2 (D_alpha G)(D_alpha w_A,D_alpha w_A) }`,

`R_(nu,alpha)=2h sum_(A,mu) G^(mu nu) w_(A,mu) D_nu^+ w_(A,alpha)`.  (8)

Then the exact finite first variation is

`delta_L q = xi^alpha D_alpha^+q + C_alpha xi^alpha
              +R_(nu,alpha) D_nu^+xi^alpha`.                       (9)

Proof: use the REAL forward product rule

`D^+(uv)=(D^+u)v+u(D^+v)+h(D^+u)(D^+v)`.

The local coordinate-index terms cancel between delta G and delta w. The surviving shifted-product and inverse terms are exactly (7)--(8). No continuum chain rule is imported into a finite difference.

For the ACTUAL reduced source slope `k_z=K'(tau q_z/rho_z)/b`, `b=K'(0)>0`, summation by parts gives its explicit residual covector

`W_mat,alpha = k C_alpha -sum_nu D_nu^-[k R_(nu,alpha)]`.             (10)

Therefore

`sum k(delta_Lq-xi.D^+q)=sum xi^alpha W_mat,alpha`                   (11)

for arbitrary finite xi, not merely slowly varying test vectors. The derivative of k MUST stay inside D^-; actual PF/source variation is part of this formula. The replay rejects pulling k outside it.

## 4. The geometric defect is now computed on the unchanged six-face action

The exact scalar density used is

`f_h=h^-2 sum_(r<s) epsilon_(rsuv) G2(e_u wedge e_v, STAR b(C_rs))`,
`P_rs=U_r(z)U_s(z+r)U_r(z+s)^-1 U_s(z)^-1`,
`C_rs=(P_rs-P_rs^-1)/2`, `b(C)=(C eta)_(a<b)`.

This is `h^-4 P_star(h e,U)` from the original owner. Both inverse link occurrences, every face orientation and all incident anchors are differentiated. The checker uses the unmodified `G2` and `STAR_MAP` from `a4d_star_density_variation_pressure_check.py`.

Let `E_e,E_Omega` denote its exact coframe and h-scaled left-link Euler rows. There is no variation restricted to a null ansatz. If A_r is any collection of one-form components and E_r its exact corresponding source, the adjoint of the test in (5)--(6) is

`L_h^*(A,E)_alpha = sum_(r,k) E_(r,k) D_alpha^+A_(r,k)
                    -sum_r D_r^-[sum_k E_(r,k) A_(alpha,k)]`.

Thus the COMPLETE computed geometric covector is

`W_geom = L_h^*(e,E_e)+L_h^*(Omega,E_Omega)`.                       (12)

Its exact defining property is `D sum f_h[L_h xi]=sum xi.W_geom`. It is generally NONZERO at finite h. The code also checks genuine local Lorentz gauge invariance; that exact internal gauge Ward must not be conflated with spacetime Lie invariance.

For transparency, the matrix reverse derivative of one face uses

`grad_P[Tr(W^T (P-P^-1)/2)] = (W+P^-T W P^-T)/2`.

All four chronological factors are then differentiated with the ordinary matrix product rule; inverse-factor gradients are `-U^-T grad_(U^-1) U^-T`, scattered back to their true source sites. No finite-difference gradient or automatic-differentiation engine is used to manufacture the covector. Independent finite differences of the COMPLETE original action test the implemented derivative.

## 5. New full42 identity and a quantitative finite-to-continuum criterion

Normalize the given reduced action only for analysis by its ACTUAL nonzero common coefficient `M tau b`. The normalized geometric coefficient is `a_bar=a/b`, and the matter source coefficient is k from (10). The full normalized field source is denoted E_h. Any extra real price remains in its own source; it is not chosen to cancel anything.

For the accounted same-price component the exact finite identity is

`L_h^* E_h = a_bar W_geom + k D_h^+q + W_mat`.                       (13)

Here `L_h^*E_h` includes ALL16 coframe,24 link and2 material rows. The test maps source covectors, not just density values. An actually supplied additional price adds its actual projected source to the left or, equivalently, an explicit remainder on the right.

At a full stationary point, (13) therefore gives

`k D_h^+q = -a_bar W_geom-W_mat`.                                  (14)

This replaces the previously symbolic E_geom/E_mat in section9 of the weighted owner by explicit computable arrays on the SAME fields. It does NOT assert exact finite constancy of q.

More generally let `r_h=L_h^*E_total/(M tau b)` after the appropriate consistent normalization, with every other real source separated explicitly. If k>=k_min>0, then

`||D_h^+q||_inf <= [||r_h||_inf+|a_bar| ||W_geom||_inf
                                      +||W_mat||_inf]/k_min`.      (15)

If an additional source was not included in r_h, add its projected norm on the right. Never confuse the projected residual with a small unscaled norm of the original source: L_h^* contains backward differences and can amplify a high-frequency error.

On a connected finite region with graph-path macroscopic diameter D, matching q=q_* at a compatible collar gives

`||q-q_*||_inf <= D * right_hand_side_of_(15)`.

Without that boundary condition the same estimate controls pairwise differences; one reference value supplies the constant.

### What convergence is genuinely justified

For samples of uniformly C^4 coframes/connections/scalars on complete collars, bounded inverse coframes, `U_r=exp(h Omega_r)`, and uniformly C^1 slope k, (7)--(10) give `W_mat=O(h)` directly. The constants retain bounds on e,e^-1, matter derivatives and k, including actual rho_min and derivative budgets.

For W_geom, expand the ORIGINAL plaquette and its first source, not a replacement action: `C_rs/h^2=F_rs+O(h)` in C^1 on such charts. Differentiating the four actual factors with their shifted anchors gives the continuum Palatini Euler covectors plus C^1 O(h). In (12) their continuum leading combination is the compact-Lie variation of the four-form `epsilon e wedge e wedge F`, a total divergence. Its coefficient is zero, leaving `W_geom=O(h)`. This is a consistency statement for uniformly smooth sampled fields, not an exact finite Diff symmetry. The source expansion requires the stated derivative and link-log controls; mere C0 convergence is insufficient.

Consequently a family of EXISTING smooth-regime full finite roots with k_min bounded below obeys `q_h=q_*+O(h)` with the declared collar. Approximate roots require the actual projected residual in (15) to tend to zero. This is a conditional finite rigidity/transport theorem, not construction of all roots, compactness, an O(h^2) claim or raw216 closure.

Rough PF weights, closing master-chart radii, high-frequency fields or unsupported boundaries can keep the defect finite. The exact identity still holds, but the asymptotic conclusion cannot be asserted. No recurrence/Bratteli scaling has been silently reinterpreted as physical smoothness.

## 6. Reproducible evidence and actual limitations

Run from repository root:

```
OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_causal_native_weighted_synthesis_2026-10-21/weighted_dynamics/check_discrete_material_ward.py
OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_causal_native_weighted_synthesis_2026-10-21/weighted_dynamics/check_full_star_ward.py
```

The first script checks noncommuting rational inverse/product identities, the correct weighted invariant including its radial residual, both material components, and a new 75-digit replay of the actual N=1 Golden master. It reproduces the earlier reported U and e_E mu values at rho=1/2,1,2,3; the worst normalized branch residual is below 5e-68.

The second computes all geometric and material source rows and verifies (13) on four-dimensional periodic diagnostic grids with 256,4096,20736 and65536 sites, noncommuting proper links, all six Lie-algebra directions and both nonconstant scalars. The actual nonlinear K' slope and a/b are used at every diagnostic site. Rho is a smooth positive DIAGNOSTIC array, not a claimed actual AF refinement. The complete nonlinear material price is also differentiated independently at the smallest grid. No diagnostic is called a stationary root.

`DISCRETE_MATERIAL_RESULT.json` and `FULL_WARD_RESULT.json` are actual outputs of these new runs. Ordinary and optimized Python stdout agree byte-for-byte in the recorded environment. The exact identities follow from the displayed algebra; floating checks are numerical verification, not a proof of arbitrary-field statements or an interval certificate.

Remaining physical obligations are unchanged: selected absolute Book/CQ valuation, actual moving-query and field-writing admission, the rest of the full preparation/clock/controller source, fixed-collar constraints, existence and regularity of general joint finite roots and common physical readout/refinement. On nonnull fields the original operational metric still has the prior explicitly determined conformal/torsion distinction. No pipeline/CI/Lean acceptance is inferred from these checks.
