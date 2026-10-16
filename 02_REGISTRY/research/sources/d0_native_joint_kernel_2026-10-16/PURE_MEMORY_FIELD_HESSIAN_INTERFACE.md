# Pure E0 memory: exact field Hessian interface with its curvature retained

16 October 2026. This is a consumer of the **same conditional v8 action**,
the complete stored-adjoint chart and the rank-aware memory-source owner.
It does not select another action, preparation cost, observer law or measure.
The full carrier has4096 momenta and16 exterior coordinates; the prepared
shell still has128 dimensions and the reference remains C128. The actual
pure preparation has rank8. The faithful Morse–Bott theorem is unchanged:
its local classification does not extend automatically to this rank boundary.

The new checker is `pure_memory_curvature_check.py`, API `run(repo=None)`.
It extracts only SHA-pinned defining AST nodes. The rational finite return
is a member of the actual native constraint class, **not another root**.
No old suite,4096-momentum matrix assembly or root search is used. Here
“chart curvature” means the second derivative of the constrained operator;
it does not assert nonzero spacetime Riemann curvature of the example.

## 1. Exact action on the pure memory input

Write the whitened regular native variables as

```text
u_r(x)=(tau_r(x),rho_r(x) z_r(x)),  rho_r>0, z_r in S²,
O_r(x)=diag(1,R_r(x)), R_r(x) in SO3,
O_r(x)u_r(x+r)=u_r(x).
```

The time component and radius are constant along their own r-lines. The
stored backwards expression is, in the owned full exterior representation,

```text
D = L sum_r [c(u_r(x)) Lambda(O_r(x)) T_r-c(u_r(x))
        +b(u_r(x)) Lambda(O_r(x-r))^-1 T_-r-b(u_r(x))].       (1)
```

Own-leg transport is what makes this backwards expression the adjoint of
the forward expression; it is not optional. Every SO3 return fixes every
vector in `E0=span{mask0,mask1,mask14,mask15}`. For a unit chi in E0 and
`t_r(k)=exp(2pi i k_r/L)`, (1) gives the exact, whole-neighbourhood identity

```text
D [e_k tensor chi](x)
 = e_k(x) L sum_r [(t_r(k)-1)c(u_r(x))
                     +(bar t_r(k)-1)b(u_r(x))] chi.          (2)
```

This is an equality of actual16-component outputs, not a scalar expectation
or an assumption that the operator no longer depends on links. In particular
`D²(e_k chi)` need not obey the same simplification: after one application,
the intermediate state generally leaves E0. That is why the signed off-shell
Schur term below still depends on returns.

Take the existing eight modes `Omega={+/-e_s}` and their independent
reference labels, with each plane wave normalized by `N^-1/2`, `N=L^4`.
The preparation is

```text
Psi0 = (1/sqrt8) sum_(k in Omega) e_k tensor chi tensor |k>ref.
```

All128 reference coordinates remain available; this state occupies eight
of them. Let `lambda1=L²(2-2cos(2pi/L))`. For each occupied mode only one
phase differs from1. The linear CAR operator on the right of (2) then squares
to `lambda1 ||u_s(x)||² I16`. Consequently the **exact fixed-preparation**
energy on every nearby stored-adjoint field is

```text
R_fixed_chi(u,O) = ||D Psi0||²
                = lambda1/(4N) sum_(x,r) ||u_r(x)||²
                = lambda1/(4N) sum_(x,r) (tau_r²+rho_r²).     (3)
```

No link term or normalizer is thrown away: (3) follows from (1) and the
normalized amplitude. Moving native observers are handled by the existing
full16 whitening and its simultaneous preparation/Gram pullback. Keeping
the whitened coordinate chi fixed here does not freeze the original raw
observer or matter variables.

The whole-blank ray is `chi_native=(mask1+mask15)/sqrt2` in the owned basis;
the source packet uses `(mask1-mask15)/sqrt2`. Apply its existing simultaneous
`T=basis_phase Lambda(eta)` conversion to states and operators. Both rays
are fixed by SO3; all even-operator expectations used here agree. This is
not permission to omit that conversion in a general source or vector test.

## 2. Full Y survives, and its pure contraction can be computed analytically

Use the actual additive tau/rho and sphere/angle chart. For two first jets,
with tangent sphere vectors beta_i,beta_j, its true second spatial leg jet is

```text
u_ij,sp = delta rho_i beta_j + delta rho_j beta_i
                         -rho <beta_i,beta_j> z.
```

Thus `<a_i,a_j>+<u,u_ij>` cancels the orientation contribution and leaves
`delta tau_i delta tau_j+delta rho_i delta rho_j`. This is a use of the
actual second jet, not an ambient-linear replacement. For a nonselfconjugate
Fourier pair, write the real field as `z a_i e^(iqx)+bar z bar a_i e^(-iqx)`.
In the complex mixed convention `partial_(bar z_i) partial_(z_j)`, (3) gives

```text
Y_pure,ij = lambda1/2 sum_(r:q_r=0)
       [bar delta tau_i,r delta tau_j,r
                         +bar delta rho_i,r delta rho_j,r].  (4)
```

The active roles have zero tau/rho first jets by the actual own-leg
constraints. All16 leg slots are still present in the full chart; their
allowed Fourier combinations,12 rotation slots and observer pullback are
not replaced by an arbitrary restricted matter model.

Let `J_i(k):k->l=k+q` be the existing full stored first jet, and
`X_i(k)=D_l J_i(k)+J_i(k)D_k`. With `Q=I-P_Omega`,
`r_k=0` on Omega and `r_k=(lambda_k-epsilon)^-1` elsewhere, define

```text
H_pure = H_spectral_full + Y_pure - QSchur_pure,              (5)
QSchur_pure,ij = (1/8) sum_(k in Omega)
 [r_(k+q) <X_i(k)chi,X_j(k)chi>
  +r_(k-q) <X_j(k-q)^*chi,X_i(k-q)^*chi>].
```

The second term's field ordering is intentional. Equivalently it is the
expectation of `X_j X_i^*` in the operator formula (7) below. The resolvent
is indefinite; the ground term is never changed to an absolute gap.
`H_spectral_full` is the second derivative of the actual full heat/feedback
price, including its constrained D_ij term. Its fullZ, M=128, calibration
and all119 energy features stay unchanged. The rank-one normalizer term
vanishes for a nonzero Fourier mode by its off-diagonal momentum support;
that argument does not apply to q0. Selfconjugate q uses the real
polarization directly, rather than counting q and -q twice.

For q outside Omega-Omega, `P X_i P=0` for every preparation rank, so the
rank-aware `T_k` row vanishes by exact support. After eliminating Q,
(5) is therefore the complete field block on the same native quotient
of dimension `17-2p`; shell-density tangents are retained separately.
This does not inherit the faithful block's inertia.

## 3. Countercontrol: the pure curvature correction is strictly nonzero

Take q=(3,3,0,0), role r=2, fixed coframe and observer, and the owned
unscaled stabilizer `W=[omega]_cross`, `omega=w_2`, `W u_2=0`. A genuine
native curve is `O_2(x)=diag(1,exp(theta(x)W))`, other returns I, with
`theta(x)=z e^(iqx)+bar z e^(-iqx)`. Since q_2=0, own-role transport is
exact. A rational Cayley parametrization has the same first/second jet and
provides the checker's literal finite-parameter member of this curve class.

Let `Gamma=Lambda_*(W)`. In the same mixed convention,

```text
D_ij(k)=L[t_2(k)c(u_2)+bar t_2(k)b(u_2)] Gamma².
```

`Gamma chi=0`, so its pure contraction is zero. In contrast, full16 CAR
trace identities give

```text
Tr16 Gamma² = -8 ||omega||²,
Tr16 c(v)b(u_2)Gamma² = Tr16 b(v)c(u_2)Gamma²
                      = -4 ||omega||² <v,u_2>.
```

At `G_rs=d delta_rs+o(1-delta_rs)`, sum the **eight occupied phases**.
They obey
`sum_Omega Re[t_2 bar z_s]=2L(1-cos(2pi/L))(2delta_2s-1)`, hence

```text
C_old=(2/128) sum_Omega Tr16[D_k D_ij(k)]
     =-c_L(d-3o)||omega||²,
c_L=L²(1-cos(2pi/L))/4,
C_pure=0.                                                  (6)
```

The existing stationary-root identity is `C_kappa+C_old=0`. Therefore
the total chart-curvature term for the pure state is
`C_kappa+C_pure=C_pure-C_old=+c_L(d-3o)||omega||²`, not zero.
The consumed root rectangle strictly has d-3o>0. For the unscaled role2
axis, `||omega||²=a²+2b²`; the checker supplies strict rational lower and
upper bounds using only that receipt. Omitting the second jet predicts0
for this correction and is rejected. The conventional real cosine
second derivative is one half the complex-symbol value in (6).

The operator-valued curvature in the existing **floating**
`diagnostic_memory_fibre.py` has a consistent normalization. Its `B0,B1`
prefactor is `4/8`, but each contribution is the anticommutator
`B@mat+mat@B`. Under the I16/16 trace this gives
`2*(4/8)/16=8/128`, exactly the scalar coefficient in
`diagnostic_old_frequency.direct_second`. Comparing the prefactors without
this anticommutator factor would incorrectly report an error. The new
checker verifies this positive normalization control and independently
checks(6) with eight literal full16 blocks. The saved midpoint crossing,
slope and neutrality values keep their original floating, noncertificate
status; no foreign diagnostic or receipt is rewritten.

## 4. Minimal finite correction and the next consumer

Keep the complete existing scalar moment assembly for the faithful
matrix `H_old`:41 J moments and257 X moments, with all119 features and
7140 scalar pairs, fullZ and signedR. For any internal sigma,

```text
H_sigma,ij = H_old,ij + Tr16[(sigma-I16/16) M_ij],
M_ij = (1/8) sum_(k in Omega)
       [J_i(k)^* J_j(k)-r_(k+q) X_i(k)^* X_j(k)]
     + (1/8) sum_(l in Omega)
       [J_j(l-q) J_i(l-q)^*-r_(l-q) X_j(l-q) X_i(l-q)^*]
     + (1/8) sum_(k in Omega) {D_k,D_ij,0(k)}.                (7)
```

`D_ij,0` is the true zero-frequency mixed second chart jet. Formula(7)
is operator valued on **all C16**, not a fitted scalar residual. It is
the internal diagonal average of the actual matter Schur operator.
At most16 occupied-edge evaluations are needed; no4096x16 matrices are
needed for this correction. J has9 Laurent coefficients of Clifford
degrees1/3; X has33 coefficients of degrees0/2/4, as proved by the existing
native algebra. Their scalar weights remain those of the same price.

For the full-trace curvature used in `Tr M_ij`, only the degree1 part of
`D_ij,0` pairs with D_k. Nine degree1 operator moments
`P_nu=sum_k kappa_k exp(ik.nu)D_k`, nu in E9, suffice for the spectral
curvature; they use the existing scalar Fourier data. For the pure scalar
contraction, use (4). To obtain the **full** M_v or M_v chi, retain the
actual second jet: the scalar identity(4) does not determine its vector
action on variations leaving E0.

There is a further exact shortcut for this particular whole-blank state.
Write the existing eight Hermitian Majoranas as
`g_2j=c_j+b_j`, `g_(2j+1)=i(c_j-b_j)`. Among even Clifford monomials,
the functional `ell_chi(A)=<chi,A chi>` has precisely eight nonzero values:

```text
mask:   0   3   60  63   204 207  240 243
value:  1  -i   -1   i    -1   i   -1   i.
```

This follows from fixed occupation of mode0 and the equally weighted
spatial-empty/spatial-full components. It does not discard either parity
sector. Consequently the **same-parity** exact Gram blocks
`S_chi[I,J]=ell_chi(g_I^* g_J)` have at most eight entries per row, given
by signed XOR: this applies to Jodd/Jodd and Xeven/Xeven. The full256
Gram also has cross-parity entries from the coherent state, and is not
claimed to have this sparsity. Replace a full Fock trace by the sparse
same-parity functional for the occupied J/X terms; do not keep the old
scalar rho=1/128 there.
For an eventual single candidate v, form M_v via signed Clifford products
or small full16 matrices at those16 nodes. Products can have degree6/8:
projecting M_v back into the99-component X subspace would lose equations.

An efficient next API can therefore expose

```text
pure_field_symbol(q,shared) -> H_pure, curvature_correction
matter_operator(q,v,shared) -> M(q;v), M(q;v)chi
```

using the fixed root-box scalar data and the existing mean-slice basis.
For a nonselfconjugate pair, `M(q;v)=sum bar v_i M_ij v_j` is a complex
sesquilinear symbol; the real velocity `v e^(iqx)+bar v e^(-iqx)` has
twice this operator, whereas `v cos(qx)` has one half. Use the real
convention of the nonlinear memory owner consistently.

**One decisive bounded consumer:** N06/N07, pure endpoint q=(3,3,0,0),
13 native quotient coordinates. First validate its field kernel/inertia
on the owned root rectangle with (5) or (7), including (6), without
rerunning the old faithful matrices. If a genuine kernel vector remains,
compute M_v and test the real pure-memory condition

```text
M_v chi = lambda chi + sum_r beta_r B_r chi,
lambda,beta_r real.
```

The actual positive Gamma gives the real orthogonal projection explicitly:
`lambda=<chi,M_v chi>`,
`beta=Gamma^-1 Re[(<B_s chi,M_v chi>)_s]`.
A nonzero remainder excludes the second stationary jet for that velocity;
a zero remainder alone proves neither a convergent branch nor physical
admission. The previous midpoint crossing is not used as a kernel proof.
This tests the internal memory subfibre, not every amplitude tangent.
The existing [rank8 amplitude fibre](RANK8_AMPLITUDE_FIBRE.md), Section6,
already has source rank151 and the smooth flat amplitude family of
dimension57195. Its remaining full field-normal operator H8^V has real
dimension40806, and criterion(R15) is open. The13-coordinate q3300 block
here is one bounded input to that criterion, not its full inverse or
complete rank8 kernel classification.
All matter/preparation Euler rows, observer representation sources,
reference and unpriced affine shifts remain in their original scopes.
