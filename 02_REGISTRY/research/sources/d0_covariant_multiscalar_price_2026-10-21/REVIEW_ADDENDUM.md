# Independent addendum: regular prices share a covariant solution class

21 October 2026. Short equation-level composition within existing PR #334,
reviewed by the `preparation_closure` executor. This addendum does not modify
the previously reviewed proof, example, checkers or receipts.

Inputs inspected:

- The concurrent generic-price Ward theorem in
  `A4D_COMPLETE_PRICE_ONSHELL_DENSITY_RIGIDITY_2026_10_21.md`, sections 2--3
  and 6, at commit `7f87eaaba20a19b1dad3a27079a4417caff5bff1`, Git blob
  `b51a3fc3df1c29158361ab2ee5766a15e5e21b95`.
- This packet's `PROOF.md`, SHA256
  `e7a71e11ac1f8d6fd8fc49101aa231ccea4c5c23352f913a041d33995ebeccb2`,
  for the complete multiplier equations and positive volume-gauge map.

**Verdict.** The proposed generic-price corollary is valid with the specific
sector and local-coordinate qualifications below. It broadens the
equation-level correspondence from a common detector's cap valuations to
different regular local two-density prices. It does not identify their
critical sets in unchanged fixed-volume coordinates, their off-shell
actions, or their physical executions.

## 1. Exact common carrier and chosen sector

Use the SAME nondegenerate independent coframe/Lorentz-connection carrier,
the same two real scalar fields, the same fixed positive coordinate volume
`mu0`, and the same fixed scale `eta>0`:

    e=vol_g/mu0>0,
    K_mu_nu=sum_A partial_mu psi_A partial_nu psi_A,
    q=g^(mu nu)K_mu_nu,
    x=eta^2 eR(e,omega),    Y=-eta^2 q,
    S_F=integral F(x,Y) mu0.

There is no independent material spin-connection source and no extra
coordinate-dependent, nonlocal, preparation or clock term in this stated
action. The assertion concerns its field equations with all other actual
parameters fixed, as in the input continuum dictionary.

Let `F` be C2 on the operand neighborhood. Put

    T_F=x F_x-Y F_Y,    H_F=F-x F_x.

Choose a particular pair `(x_F,Y_*)` in an inverse-function neighborhood
of `(T_F,H_F)`, with

    T_F(x_F,Y_*)=0,
    F_x(x_F,Y_*) != 0,   F_Y(x_F,Y_*) != 0,
    k_F=F_Y(x_F,Y_*)/F_x(x_F,Y_*) > 0.

The pair therefore obeys `x_F=k_F Y_*`. Define the fixed kinetic sector
`q_*=-Y_*/eta^2`. Neither `q_*` nor the chosen sector pair is varied in
the covariant representation below.

The chosen local branch matters. Regularity of `(T_F,H_F)` is sufficient
for density rigidity, but by itself does NOT imply that `T_F(x,Y_*)=0`
has a unique root in x for every prescribed `Y_*`. The statement is made
for a specified root/sector of each price. If several such roots exist,
they can give different native volume-gauge sectors. Each may correspond
to the same covariant solution class at fixed `q_*`; their union must not
be silently treated as a single injective native sector.

Near `(0,0)`, the common sufficient conditions `F_x(0,0) != 0` and
`F_Y(0,0) != 0` give

    D(T_F,H_F)|_0 = [[F_x,-F_Y],[0,F_Y]],

so the Ward regularity is automatic there. The additional sign condition
selects the positive multiplier branch, rather than a zero or negative
one.

## 2. Direct equation-level proof

The local coframe rescaling and induced Lie variations give, at every
full stationary field,

    T_F=0,       dH_F=0.

On a connected field region with operand values in one stated
inverse-function neighborhood, these equations force both operands to
be constants. Restrict to the chosen sector `(x_F,Y_*)`. Therefore
`F_x,F_Y` are spacetime constants, and the full ambient first variation
is exactly

    delta S_F=eta^2 F_x integral
                 [delta(eR)-k_F delta q] mu0.             (1)

All fields are varied before any ansatz or connection elimination.
Equation (1) gives the ordinary independent Palatini equation, all metric
and coframe equations, and both original scalar equations:

    omega=omega_LC(e),
    eG_mu_nu=k_F K_mu_nu,
    partial_mu(g^(mu nu)partial_nu psi_A)=0.              (2)

The final expression is in a volume coordinate chart for `mu0`; in a
general chart the same fixed measure density is retained in this
divergence. The nonzero factor `eta^2 F_x` has not been assigned a
positive sign or a uniform bound.

For this fixed `q_*`, introduce the SAME covariant representation for
every such F:

    I_q*=integral vol_g [R-Lambda(q-q_*)].                (3)

Its full equations are obtained before any gauge restriction:

    omega=omega_LC(e),   q=q_*,
    G_mu_nu=Lambda K_mu_nu,
    div_g(Lambda grad psi_A)=0.                          (4)

Given a native stationary field, `Lambda=k_F/e>0` turns (2) into (4).
Conversely, any local positive-Lambda solution of (4) can be placed in
the volume gauge

    Lambda vol_g=k_F mu0.                               (5)

The existing positive-volume coordinate construction proves this
locally. Tracing (4) and using (5) gives

    R=-Lambda q_*,
    x=-eta^2 e Lambda q_*=k_F Y_*=x_F,
    Y=Y_*.

The covariant scalar equations reduce to (2), and (1) proves every full
native field equation. This is the reverse implication for the given
generic F; no equality of prices or imposed restriction on native
variations is used.

Consequently, at this fixed local sector,

    NativeSol(F;x_F,Y_*) / Diff_mu0
       <-> CovariantSol(I_q*;Lambda>0) / Diff_+ .         (6)

The quotient notation has the same local meaning as the packet's
original proof: germs/local solutions, compatible chart domains and
transported boundary data. The residual transformations of (5) preserve
`mu0`. No metric-only or microscopic equivalence is inferred.

## 3. Different prices, the same q sector, and the exact Jacobian

Let two prices `F_1,F_2` satisfy the preceding conditions on chosen
sectors `(x_1,Y_*)`, `(x_2,Y_*)`, with positive ratios `k_1,k_2`.
They have the SAME `eta`, scalar dictionary and thus the SAME `q_*`.
Both sides of (6) have the identical covariant target (3). Their local
covariant quotient solution classes therefore coincide.

An especially simple representative map is available. Start with a
native F1 solution in coordinates z, satisfying `e_1 Lambda=k_1`.
Choose a local orientation-preserving coordinate map Z(z) with CONSTANT
Jacobian

    det(DZ/Dz)=k_1/k_2.

For example a constant rescaling of one coordinate suffices on a small
box. Transport the metric, independent connection and both scalar fields
as geometric fields; do not rescale the metric as a new physical field.
The target native model keeps its prescribed coordinate volume `d^4Z`.
Equivalently this is a pullback of the covariant solution with the target
external volume held fixed, not a claimed symmetry obtained by passively
transporting that external volume together with all the fields. At
corresponding points the volume density transforms as

    e_2(Z)=(k_2/k_1)e_1(z),
    e_2 Lambda=k_2,
    Y_2=Y_*,
    x_2(Z)=(k_2/k_1)x_1(z)=k_2 Y_* .                    (7)

The last value is exactly the chosen F2 trace-sector value. The
covariant equations remain true under this coordinate change, and the
reverse implication from section 2 proves that the transported fields
solve the F2 native equations. The inverse map has Jacobian `k_2/k_1`.

Thus changing a regular price within this common class can change the
native density-sector relation and its volume gauge without changing
the covariant fixed-q solution class. Equation (7) is NOT a theorem
that `Crit(S_F1)=Crit(S_F2)` for the same coordinate components and the
same untransported fixed-volume boundary data. The special common-r
all-cap theorem has that stronger same-coordinate conclusion under its
own hypotheses; this generic corollary does not replace it.

## 4. Null sector, collar and remaining boundaries

At `Y_*=q_*=0`, the trace equation with `F_x != 0` forces `x_F=0`.
Use `k_F=F_Y(0,0)/F_x(0,0)>0` directly. Every positive-multiplier
solution of the same `I_0` admits each price's gauge, and (7) still
applies. No step divides by `q_*`, `Y_*`, curvature or a scalar
gradient. This includes the packet's rank-two non-VSI witness as
well as aligned null and vacuum subcases on their respective local
domains.

The constant-Jacobian map generally cannot be the identity on an
arbitrary old fixed collar when `k_1 != k_2`. This corollary transports
local boundary data; it does not assert the same fixed-boundary task.
Likewise it supplies no identification of clocks, paid record lengths,
spatial compiler weights or quantum preparation resources. Those are
actual physical data outside the stated continuum coordinate map.

Degenerate Ward branches, `F_x=0`, `F_Y=0`, a nonpositive ratio, explicit
spacetime dependence, varying internal parameters, and additional
source terms are outside the proof unless separately analyzed. The
equivalence concerns stationary solutions, not equality of values,
off-shell sources, Hessians, minimum selection or stability. No new
generic-F Jacobi or boundary-preserving gauge theorem is asserted in
this addendum.

This corollary uses the concurrent author's generic-F Ward result with
the independently reviewed covariant map. The proof is the direct
variation, trace and positive-volume calculation above; it needs no
new large numerical suite. Compulsory Book03 valuation, physical
admission, actual field-writing, finite-lattice lift, independent
upstream equations and uniform refinement remain open.
`GR_closed=false`.
