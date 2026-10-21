# One exact remaining coframe equation on the new double-zero sheet

21 October 2026. Bounded source-level application of remote
`c7e0c3d2f6bcfbcc8bd43034ff72da85b8cdd18a`, existing scientific PR #334.
Author: Book-binding lane. This preserves the new finite double-zero and
three-row existence theorem, and identifies one of its explicitly unsolved
ambient geometric equations. No earlier source file or receipt is changed.

## 1. What composes exactly

The new rank-two construction really supplies `f_star=q=0` at every
constructed free anchor, two genuine conserved scalar currents, and the
local radial coframe Euler equation. At those values the SAME original
complete N=1 CQ first covector equals its affine first covector in **all42
ambient field directions**, with fixed actual PF counts and the declared
field-independent baseline. This removes the earlier nonlinear matter-slope
activation on this exact sheet. It does not assume a smooth PF sequence.
The comparison requires a complete free stencil with every contributing
anchor on the sheet; it does not repair an incompatible fixed collar.

In the required canonical Cartesian convention, the original price is
`F_cart(x,y)=F_null(-x,y)`. Writing `a=F_null,x(0,0)<0` and
`b=F_null,y(0,0)>0`, the common source is the nonzero factor `M tau (-a)`
times the source of

    A_h = sum_z [f_star,h(z)+kappa q_h(z)],
    kappa=b/(-a)>0.

This is the original sign retyping, not selection of another detector.
The amplitude used below is the owned `epsilon^2=1/(2 kappa)`, with no fit.

## 2. A legitimate nonradial coframe variation

At a constructed site let

    e(v)=diag(A(r)v, B(r)/v, r, r),
    A=sqrt(r) exp(-r^2/4), B=1/A,
    dr/dt=exp(-r^2/2).

The original exact six-face scalar has the proved form

    f(v)=[L_h v+M_h+R_h/v]/h^2,                         (1)

where

    L_h=2 A r C(h k1,h k2),
    M_h=r^2 sinh[h(k1(t+h)-k1(t))]+A B C(h k2,h k2),
    R_h=2 B r sinh[h(k2(t+h)-k2(t))],

and C, k1, k2 are precisely the original source's boost-commutator function
and link coefficients. All noncommuting spatial boost faces are retained.
The owned positive root v_star solves `L_h v_star^2+M_h v_star+R_h=0`.

The actual two scalar forward increments at that point are

    p_t=epsilon A^2 v_star^2,       p_x=epsilon.

In a genuine independent coframe Euler variation, **these actual matter
increments and the independent Lorentz links are held fixed**. One must
differentiate first, and only then insert their displayed background values.
The scalar query as a function of the independently varied v is therefore

    q(v)=p_t^2/(A^2 v^2)-epsilon^2 v^2/B^2.

Although `q(v_star)=0`, its correct partial derivative is

    q_v(v_star)=-4 epsilon^2 A^2 v_star,
    kappa q_v(v_star)=-2 A^2 v_star.                     (2)

The resulting ambient Euler component is exactly

    E_v := partial_v [f+kappa q]_(fixed actual matter,links)
         = (L_h-R_h/v_star^2)/h^2-2 A^2 v_star.          (3)

This is a real linear combination of the original sixteen coframe rows:
`E_v=A E_(e00)-(B/v_star^2)E_(e11)`. Since
`det e(v)=A B r^2=r^2` for every v, it is a volume-preserving, nonradial
direction. It belongs to the fifteen geometric coframe conditions left
open by the new theorem. The scalar value equation `f(v_star)=0` does not
imply the extra derivative equation

    L_h-R_h/v_star^2=2 h^2 A^2 v_star.                  (4)

## 3. Exact nonzero leading residual

Let a dot denote the original time derivative
`dot g=exp(-r^2/2) partial_r g`. The exact original holonomy formulas give

    L_h/h^2 = L0+O(h^2),       L0=2 A r k1 k2,
    R_h/h^2 = R0+h R1+O(h^2), R0=2 B r dot k2,
                              R1=B r ddot k2.

There is no order-h term in `L_h/h^2`, because the spatial commutator
function C(h k1,h k2) starts with h^2 and then even higher powers. The
owned projection has

    v_star=1+h v1+O(h^2),
    v1=-3(r^4-1) exp(-r^2/2)/(8r^3).

Since `L0-R0=2 A^2`, substitution into the **ambient** source (3) yields

    E_v=h [2(R0-A^2)v1-R1]+O(h^2)
       =h exp(-r^2)(3r^2+1)(r^4-3)/(4r^4)+O(h^2).      (5)

In particular, at a free anchor with r=1,

    E_v=-2h/e+O(h^2) != 0                              (6)

for all sufficiently small positive h. This is an analytical source
obstruction for the particular projected representative, stronger than
merely observing a nonzero floating-point maximum of its forty geometric
rows. No earlier grid suite is needed to obtain (5).

More strongly, for `1 <= r <= 6/5`, its h coefficient obeys

    exp(-r^2)(3r^2+1)(r^4-3)/(4r^4)
       <= -(193/432) exp(-36/25) < 0.                  (7)

The source and implicit section are smooth on this fixed compact interval,
so the O(h^2) remainder is uniform for sufficiently small h. Thus the
uncorrected projected family has a nonzero ambient source uniformly there.
Multiplication by the nonzero original N=1 source gain cannot remove it.
Other corrected field/link representatives are not excluded.

## 4. Why solving a restricted action on Sigma would be empty

Write `Sigma={f_z=q_z=0 for every required anchor}`. On this sheet,

    A_h|Sigma=0,
    D(A_h|Sigma)=0

for every point, including the points with the nonzero source (5). The
complete centered fixed-count CQ price is likewise constant there up to its
fixed baseline. Its tangent pullback therefore cannot distinguish a full
stationary root from an arbitrary double-zero point.

Equivalently, for the constraint map `C(y)=(f_z(y),q_z(y))`, the ambient
source is `DC(y)^T lambda`, with the fixed original coefficient vector
lambda. For every tangent eta with `DC eta=0`, its contraction with eta
vanishes automatically. Full stationarity requires that **ambient
covector itself** to vanish. Differentiating the relation
`p_t=epsilon A^2 v^2` during the independent coframe variation would silently
replace the real Euler equation (3) by such a restricted derivative.

This explains precisely why the new all42 source equality plus the three
solved conditions cannot imply the other equations. It establishes the
correct common source to solve, not a new implication from trace to tensor.

## 5. The next finite coupled test

The remaining target is the original full ambient **15 nonradial coframe
and 24 proper-link components**, with their actual gauge dependencies. The
old Brinkmann 40-to-3 cancellation is specific to its different null-link
ansatz and cannot be applied to these noncommuting rank-two boost links.
The projected links here are trial links; their Cartan source has not been
set to zero by solving (1).

A useful corrected construction may retain the local implicit elimination
of v using `f_v=2 A^2+O(h)>0`, but must then evaluate and solve the remaining
**ambient** source, not differentiate the already constant restricted
action. At a projected point y_h, a concrete next linear test is

    D E_remaining(y_h) delta y = -E_remaining(y_h),
    D(f_z,q_z)(y_h) delta y = 0,

together with the actual first variations preserving the chosen conserved
currents, volume and fixed collar. The permitted link/coframe/matter changes
must be represented on the whole connected stencil with an honest gauge
quotient. Solvability or a uniform inverse is not asserted here.

Link corrections participate at both temporal endpoints: when
`U_i(t) -> exp(h^2 Z_i(t)) U_i(t)` with `U_t=I`, the exact first face
variation is

    delta P_0i(t)/h^2 = Z_i(t+h)P_0i(t)-P_0i(t)Z_i(t).

Consequently a one-site Cartan correction is not a whole-slab inverse.
Both-end scalar data also impose a real compatibility condition. If the
constant-current prescription is retained, the actual history satisfies

    psi1(t_n)-psi1(t_0)=epsilon sum_j h A_j^2 v_j^2.

Fixed endpoint values require preserving this sum, in addition to local
current conservation. Neither the local v-root nor a restarted scalar
history can silently change the prescribed boundary data.

## 6. Centered F and the precise PF scope

The consumed original `native_master.py` defines exactly

    F(x,y)=-alpha beta [h_phi(r(x,-y))-h_phi(r0)].

Thus `F(0,0)=0` is true for this **centered operand-dependent term**, and
`F-x F_x-y F_y` vanishes at Sigma for that term. The baseline is still in
the original complete price B0. If one instead writes the raw uncentered
entropy price, its constant contributes `F_raw(0,0) D(sum_z rho_z)`;
that disappears only when the relevant common total weight is fixed, or
is explicitly retained in the baseline. None of these facts proves
`D_preparation B0=0` or removes the true rho dependence inside the
coframe/material dictionary. The source theorem consumed here holds at
the specified **fixed actual counts and fixed paid-cost interface**.

## 7. Narrow validation and immutable inputs

`check_coframe_residual.py` verifies just the new symbolic expansion, the
fixed-matter derivative, its determinant-preserving direction, the original
projected-root coefficient, and the nonzero/negative coefficient in (5)-(7).
It checks the following source hashes without executing their numerical
suites. The two original inputs remain in the sealed packet's sibling
`inputs` directory; the two new c7 inputs are separately frozen in
`late_inputs`. Optional positional arguments select the original root and
then the late root, preserving that historical boundary. With SymPy available:

    python3 check_coframe_residual.py

Explicit interface: `python3 check_coframe_residual.py [original_root] [late_root]`.

| Frozen root | Source relative to that root | SHA256 |
| --- | --- | --- |
| `late_inputs` | `02_REGISTRY/research/A4D_RANK2_EXACT_FINITE_DOUBLE_ZERO_UNIMODULAR_PF_SYNTHESIS_2026_10_21.md` | `dcfc4ed42147d047fae32c11b10c25a9d77df6a2dc3009ab6ad0c7d16da2af31` |
| `late_inputs` | `02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_exact_null_sheet_unimodular.py` | `098d11cd21c4bfc07f24ba32b23f9abe08eecb527bff451a1278bd8ffcdbbf05` |
| `inputs` | `02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py` | `666b921e53fba8de2332a88c89a572f5ab14d8c03348744494e06b381f2f18b8` |
| `inputs` | `02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py` | `23752ce9f4780c7713bbb7fe0d339d8952fe2e422e5541df736e8e08e754e60d` |

The existing double-zero/matter/radial theorem remains valid. The specific
projected representative is not an exact all42 root. A corrected simultaneous
geometric root, physical field-writing, compulsory Book price, all upstream
equations and a selected physical GR process remain separate questions.
`GR_closed=false`.
