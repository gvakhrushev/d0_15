# Full cut-bootstrap source and its fixed-initial execution lift

27 October 2026. Existing research owner: gvakhrushev/d0_15, Draft PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input branch checkpoint: `5135327c6ef33a23f646be904827e5ddd9684bc2`.

**Result:** explicit end-to-end composition of the already owned complete
cut-Hodge heat/feedback cofield with the nonlinear Einstein–CAR field family,
and an exact lift to every generated execution-state equation for a genuinely
fixed-initial protocol. This is not a new source law or an assertion that the
specific heat/cut/controller has been selected by the entire D0 core.
`GR_closed=false`.

## 1. Recover the direct source route before adding another spectral task

The previous two-eigenvalue calculation is a correct identity on the stated
original two-parameter CAR16 source chart. I independently reconstructed its
16 by 16 matrices and checked `A^2-sA+tI=0` symbolically. It is not, however,
a field-to-native map for 42 components at each spatial site. Independence of
two native scalar responses cannot establish that missing map by itself.

More importantly, the claimed unresolved *algebraic field-source comparison*
already has an actual stronger input in the same research branch:

- `sources/d0_coupled_cut_partition_2026-10-22/COUPLED_PARTITION_PROOF.md`,
  sections 2, 4–6, at `438abae40fd6008e486504a31f92867084ebc1ba`;
- `A4D_ORIGINAL_GOLDEN_READY_COHERENT_BOOK_FULL42_BRIDGE_2026_10_22.md`,
  sections 1–4 at that same commit;
- `gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md`;
- `A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md`.

These owners must be consumed, not reclassified as absent. The result in
sections 2–3 below is an explicit application of their mathematical content,
not a claim that the complete-price identity was first discovered today.
The new combined endpoint includes the general nonlinear generated-state lift
in section 4 and an explicit check of what it does not authorize.

The literal Book03 section 03.25 defines

    B = beta^-1 log Tr exp(-beta Delta) - log det(I-zeta F).

For this specified action, a separately chosen Shannon or von Neumann entropy
is not an extra term to add without another action-identification theorem.
The previous entropy calculations remain correct for their stated quantities;
they are not a compulsory supplement to this explicit formula.

## 2. Exact complete-action source, not merely a reporting-cost source

Use the original coherent READY apparatus and its actual three-status
comparison. The original fine records remain in work. At fixed mesh and
fixed protocol, let M be the fine label count, W the full non-RIGHT work
dimension, and s=128 the actual tensor spectator multiplicity. Set

    p=phi^-1, beta=2p^2, zeta=2^-20,
    f(q)=4q(1-q), E(q)=exp[-beta f(q)].

The selected candidate heat is the already defined *cut Hodge* operator
`L_C=C^dagger C+CC^dagger`, with `C=(I-P)UP` for the actual completed
comparison word. The full trace contains every harmonic mode. For m active
statuses, with M-m dormant coordinates, its price is exactly

    Z = M W - 2m + 2 sum_active E(q_j),
    B_C = beta^-1 log(s Z) - s sum_active log[1-zeta f(q_j)].       (1)

This is the complete specified cut-bootstrap, not a division by active rank,
not a deleted baseline, and not the independently defined original tensor or
spatial Hodge heat. All statements here require this actual carrier and cut.

Write

    c_Z(q) = [s zeta/(1-zeta f(q)) - 2 E(q)/Z] f'(q).

Direct differentiation of the full scalar, including the moving heat
normalizer, gives

    dB_C = sum_active c_Z(q_j) dq_j.                              (2)

On the original common-null field family Sigma, let a=P_READY, r0 the actual
common local click probability, and eta_h the actual reporter attenuation.
The three probabilities are

    q_NR=1-a, q_NC=a(1-rbar), q_C=a rbar, rbar|Sigma=r0.

Their **ambient first derivatives are taken before restricting to Sigma**.
In particular rbar being constant as a restricted function is not a reason
to discard its transverse cofield. The original PF map gives, exactly,

    d_42 rbar|Sigma = eta_h^2/L^4 [r_f dF_h-r_q dQ_h],             (3)
    F_h=sum_z fhat_z, Q_h=sum_z q_z.

The original count cancellation is
`n_z/rho_z=N/L^4`, where `rho_z=L^4 n_z/N` and `a=2N p^(n+3)`.
There is no equal-prior assumption. The underlying reporter coefficients are

    Q_E=1-4 zeta p^3, R_E=1-4 zeta p^3(1+p^6),
    r0=1-Q_E R_E,
    r_f=4 zeta Q_E p^11,
    r_q=8 zeta p^6(R_E+Q_E p^6).

Substitute (3) in (2):

    d_42 B_C|Sigma = G_h [dF_h+lambda dQ_h],                       (4)
    lambda=-r_q/r_f=-2p^-5(R_E/Q_E+p^6),
    G_h=(a eta_h^2/L^4)
        [c_Z(a r0)-c_Z(a(1-r0))] r_f.

Thus the kernel condition from the last two-probe proposal is not an
additional unresolved algebraic premise **for this particular full price**:
(4) proves it directly, on every original ambient field direction covered by
the reporter map. It does not prove that every conceivable Book-price
interpretation factors through the same q_j.

### The gain is strictly nonzero with the full thermal contribution retained

The consumed full-partition theorem gives

    Z_min=M(W-2),
    eta=2(1+2 beta)/[s zeta(1-2zeta) Z_min],
    (1-eta)s[j'(u)-j'(v)] <= c_Z(u)-c_Z(v)
                             <= s[j'(u)-j'(v)]

for u<v, where `j(q)=-log[1-zeta f(q)]`. At the original n20 counts
`M=72441`, `W>=50549`, and `beta<4/5`, the exact rational upper bound is

    eta < 111669149696/9598843598690745 < 1/80000.                 (5)

Since `0<r0<1/2`, `G_h>0`. This proves nonzero gain from the complete heat
and feedback, not by differentiating an inequality of action values.
For the conservative minimal-count control the ratio of complete to
feedback-only gain is 0.99999449483408311147796727965787753.
The actual W may be larger; the proof and bound cover it without deleting
any modes.

If the owned geometric source is `dJ2=gamma_h(dF_h+lambda dQ_h)`, with its
actual `gamma_h != 0`, then

    d_42 B_C|Sigma = (G_h/gamma_h) d_42 J2|Sigma.                  (6)

This is an actual source identity for the declared complete candidate.
It is not equality of the full actions on an open off-null chart.

## 3. Apply the source identity immediately to the existing nonvacuum family

Consume the original all40 theorem. The remaining two connection rows impose

    K_a(z)=[H(z+u)-H(z+u-a)]/2, a=2,3.

Its single remaining coframe row, including the two-component CAR matter, is

    -Delta_h^perp H(z+u)/(2h) - 2 lambda |D_u^+Psi|^2/h.

Therefore every original exact common-null Einstein–CAR root is also a root
of **all field rows of B_C**, by (6). One explicit original family is

    H_h(u_j,x,y) = -lambda |D_u^+Psi_{j-1}|^2(x^2+y^2)+W_h(u_j,x,y),
    Delta_h^perp W_h=0.

The unchanged midpoint construction supplies one fixed smooth nonvacuum
metric and the stated O(h^2) matter recovery. No new 42-row numerical root
search is needed. The symbol 42 means local components at every free site;
this is not a two-dimensional model of the entire spatial configuration.

This establishes the advertised application on the Brinkmann family. It is
not a claim of universal equivalence on arbitrary Lorentz metrics. In
particular, equality of solution sets in this family does not exclude
higher-curvature terms that vanish there or select a universal action class.

## 4. Exact lift to the generated execution states of a fixed-initial protocol

A closed execution has internal records, but this does not make every
intermediate state an independently selectable input. Here is the complete
nonlinear source lift for the declared action, including its heat term.

Let y be the actual admitted field/chart variables, and let X_k denote
vectors or protected-column matrices (use the Hilbert–Schmidt pairing for
matrices). The given fixed protocol supplies

    X_0=x_initial (fixed boundary), X_(k+1)=V_k(y) X_k.

All actual preparation steps must be included among the V_k. Let the full
price in these coordinates be J(y,X_1,...,X_N); explicit dependence on a
moving effect, cut or field is retained in J_y. Write its differential as

    dJ = J_y[v]+2 Re sum_k <g_k, dX_k>.

For the constrained variational calculation, and **not** as a new physical
price, use

    L = J + 2 Re sum_(k=0)^(N-1)
                     <lambda_(k+1), X_(k+1)-V_k(y)X_k>.

Define the multipliers backwards:

    lambda_N=-g_N,
    lambda_k=V_k^dagger lambda_(k+1)-g_k, k=N-1,...,1.            (7)

Then every generated-state Euler equation and every execution constraint
is satisfied exactly. The remaining field equation is

    dJ_reduced[v] = J_y[v]
       -2 Re sum_k <lambda_(k+1), (dV_k[v])X_k>.                 (8)

**Proof.** Differentiate L with respect to X_N and then each X_k. Its
coefficients are precisely `g_N+lambda_N` and
`g_k+lambda_k-V_k^dagger lambda_(k+1)`. Equation (7) kills them. Differentiate
with respect to y at fixed X and substitute the execution constraints to
obtain (8). Alternatively differentiate the finite forward recurrence and
telescope its pairings with (7). This proves exactly the chain rule of the
same complete price. No positivity or quadratic-price assumption is used.

For (1), the terminal probability gradient is
`g_N=sum_j c_Z(q_j) Pi_j X_N` in the pure-report representation; formula (7)
therefore includes the actual nonlinear heat normalizer. More complicated
prepared cuts use their actual J derivatives instead of this special form.
The constraints vanish on execution and add no counterterm or new action.

### Application and strict boundary

Once a genuinely supplied fixed-initial native execution realizes the
field/report map of section 2, its exact field root lifts through (7) to a
constrained stationary point including **all its generated internal states**.
There is no separate free-controller or free-initial-state equation merely
because one can mathematically enlarge the ambient unitary group.

Conversely, an independently variable input u NOT generated by the declared
protocol contributes `J_u` (and its real constraints). Equation (7) does not
make it vanish. Nor does this proof authorize declaring a previously free
input fixed after seeing a nonzero source. If elementary matrices V_k(y)
have not been realized by the allowed native grammar, their availability
remains an explicit premise. Discrete code families are compared as finite
codes; an arbitrary continuous generator is not thereby a native primitive.
This is exactly the difference between removing a spurious equation and
suppressing a genuine physical variation.

## 5. What is still required, and an explicit intrinsic heat test

The full-cut source identity is mathematically available; the next scientific
application is **not another CAR spectrum or another field solution**. It is
whether this same field-dependent executable and its actual Delta belong to
the literal intended D0 physical action and native field-variation domain.

There is a sharp internally constructed test against identifying heats by
name. The owned stationary-section comparison uses

    H_g=beta^-1 log[s(a+2Z)], H_0=beta^-1 log(cZ),
    Z=Tr exp(-beta Delta), a>0,
    d(H_g-H_0)=a/[Z(a+2Z)] Tr(exp(-beta Delta)dDelta).             (9)

Both use the same internal DATA operator, but one keeps a paired cut's full
harmonic complement and the other uses the specified tensor heat.
For the original positive CAR chart `A=nu^2 B(r)` and `Delta=256A` at h=1,

    d_nu(H_g-H_0)=
       2a Tr(Delta exp(-beta Delta))/[nu Z(a+2Z)] > 0.            (10)

At the original r=1/9, nu=3/5, beta=2p^2 and a=2016, this derivative is
11.72710702795727655306131131311842. It is checked by independent direct
differentiation of both complete logarithms. This is a diagnostic on the
original local native scale chart, **not** a proof that this direction is
an admitted 42-field actuation or that the two heats differ on the particular
stationary geometric section. It proves only that their identification is
not a formal consequence of using internal variables and a closed apparatus.

No unique microscopic action is needed if a genuine source equivalence on
the actual field section is proved. No external observer or matter source
needs to be invented. But an actual map/identification cannot be replaced
by the names "closed", "native", "heat" or "Ward".

## 6. Actual validation and delivery

Executed locally with Python 3.13.5, SymPy 1.14.0 and mpmath at 100 decimal
digits:

- exact rational bound (5), exact Golden coefficient ratio and symbolic PF
  density cancellation without equal site priors;
- full nonlinear heat-plus-feedback derivative, not feedback alone;
- exact constrained-state equations and high-precision full-price adjoint
  agreement on a small, explicitly structural three-dimensional execution;
- symbolic substitution in the existing nonvacuum Poisson consumer;
- direct intrinsic heat-source mismatch (9)–(10).

`complete_book_source_application_check.py` uses raised exceptions rather
than optimization-removable assertions. It makes no claim to replay the huge
original READY apparatus, the original all40 symbolic owner, Lean, or CI.
The local symbolic CAR reconstruction separately verifies the previous
8+8 spectral identity; it is not used as a replacement for the field map.

Git cloning was unavailable in this runtime; source reads and persistence use
the connected GitHub tool. No structural full-repository gate, independent
review or merge is reported. The research parent remains Draft. Mathematical
field-source closure of the declared full-cut candidate is established;
unconditional D0-to-universal-GR closure is not established by this packet.
