# The actual paid-history effect and its complete prepared-cut feedback

20 October 2026. Same PR334; input
`b8574656b0613fac8e4ff65e2292d6b180cbd8d0`. This is a constructive operator
transport for one retained history. It does not identify an experimental
readout of cost with the physical action, select `Info`, or declare a new
apparatus free. The original full128 process is consumed, not replaced.

## 1. The common history and the two legitimate cuts

For a fixed finite horizon let the complete original instrument have Kraus
words `K_gamma(q)`, with every record, failure and old RIGHT retained. Its
Stinespring isometry is

    V(q) x = sum_gamma |gamma> K_gamma(q) x,   V* V = I.

The code and integer horizon are fixed under field differentiation. Write
`C_gamma` for the actual integer paid-port cost, and, for an ANALYSIS variable
`t>0`, set

    E_t = diag_gamma(exp(-t C_gamma)) tensor I,
    G_t(q) = V(q)* E_t V(q).

Then `Tr(rho G_t)` is exactly the paid-port partition of the companion
full128 transfer theorem. It includes the entire chronological word; no
choice of entropy is used. A field-dependent preparation contributes
`Tr((d rho) G_t)` to its derivative.

Let `i:H->K` be the fixed blank-apparatus input isometry and let `W(q)` be
the actual full unitary realization, so `V=W i`. Introduce a marker with the
mathematical Julia rotation

    J_E = [[sqrt(I-E), -sqrt(E)], [sqrt(E), sqrt(I-E)]],
    U_echo = diag(W*,W*) J_E diag(W,W).

This formula declares a test apparatus. Its physical compilation, both uses
of the original programme, marker controls and all associated cost still
belong to the admission/payment map. A square-root formula alone is not a
native primitive. For the one-round Golden costs below the marker has only
the original two Golden probabilities, without a fitted angle.

If the active cut includes EVERY input workspace state,
`P_all=I_K tensor |0><0|`, then its original-form feedback is

    F_all = P_all U_echo* (I-P_all) U_echo P_all
          = W* E W.

It is isospectral to the fixed marker. Consequently its FULL counting-trace
logdet is field independent. The prepared expectation of this same effect
may vary. This statement does not apply to a field-dependent marker or to
the owned paired comparison, whose field enters interfering relative arms.

## 2. Exact feedback on the actual blank input, including the work complement

For the prepared input cut use
`P_in = i i* tensor |0><0|`, with the ORIGINAL complement `Q_in=I-P_in`.
Do not replace that complement by the selected marker outcome alone. On H
the active block and true feedback are

    A = V* sqrt(I-E) V,
    F_in = I - A^2.

In particular the following is an exact positive transport, independent of
how W is extended away from its actual input isometry:

    F_in = G + L,
    L = V* sqrt(I-E) (I-V V*) sqrt(I-E) V >= 0.       (1)

Proof: `G=I-V*(I-E)V`; expand `I-A^2-G`. The term `L` is precisely the
marker-zero output in the complement of the prepared work subspace. It is
retained in the genuine `Q_in`. Thus (1) is not a postselection formula.
It retains all output columns and gives the full operator on the input H,
not only the response of one vector. Old RIGHT remains a tensor spectator.

This resolves two different mistakes in a proposed price transport. The
all-work determinant has constant spectrum; the prepared-cut determinant
has the additional positive `L`. Neither can simply be renamed the
prepared paid-history expectation. The full source of (1) is `dG+dL`,
including the moving isometry and any moving preparation in a subsequent
expectation. A field-dependent input cut can be represented by a moving
isometry, whose derivatives must also be retained.

## 3. Exact specialization to the unchanged original full128 round

Let `p=phi^-1`, `a=sqrt(p)` and `epsilon=p^2 h^2/64`. The original coherent
round has two Golden port maps

    K_0 = p I + p^2 W,       K_1 = p^(3/2)(W-I),

followed by all64 original work labels; the initial work label is blank.
The owned blank block is

    W_00 = I - epsilon Delta/(2 p^2),   Delta=D*D.

Summing ALL64 label effects, unitarity of W gives the actual return-port
effect

    R = sum_label K_(label,1)* K_(label,1)
      = p^3(2I-W_00-W_00*) = p epsilon Delta.          (2)

The other64 effects sum to `I-R`. This uses the full original instrument,
not an independently chosen binary detector. At `t=ln(phi)`, cost1 has
marker effect p and cost2 has marker effect p^2. Hence

    G = p(I-R) + p^2 R = p I - p^3 R,
    A = p(I-R) + a R = p I + (a-p) R,
    F_in = p I - 2p(a-p) R - (a-p)^2 R^2,
    L = (a-p)^2 (R-R^2).                             (3)

Every equality is an operator identity; no simultaneous diagonalization
with a variation or preparation is assumed. For any admitted first jet,

    dG = -p^3 dR,
    dF_in = -2p(a-p)dR - (a-p)^2(R dR+dR R),
    dL = (a-p)^2(dR-R dR-dR R),
    dR = p[(d epsilon)Delta + epsilon dDelta].         (4)

The source of the true prepared-cut feedback therefore differs already in
the FIRST native small-epsilon coefficient. On a scalar eigenmode with
`0<R<1/2`, increasing R gives a strictly positive omitted complement
source. Neither a zero-cost interpretation of the discarded work nor an
endpoint-only price can remove (4).

For a moving density, `d Tr(rho L)=Tr((d rho)L+rho dL)`. For a feedback
component, its source instead is the original counting-trace expression
`z Tr((I-z F_in)^-1 dF_in)` (plus the z derivative if z moves).
These are different readouts. The paid mean is generated by
`-partial_t log Tr(rho G_t)|_(t=0)`; it is not the logdet of (3).
Workspace/reference multiplicities in a full determinant are retained.

## 4. A controlled positive long-history transport, including first/second jets

There is also a useful positive conclusion. If every n-round word costs
at least n, put `b=exp(-tn)`, so `0<=E<=b I`. Let
`D_E=sqrt(I-E)-I`, `eta=1-sqrt(1-b)`. Then

    ||D_E||<=eta,
    L=V* D_E^2 V-(V* D_E V)^2,
    0<=L<=eta^2 I.                                  (5)

For a C2 isometry family, with `||dV[u]||<=M1||u||` and
`||d2V[u,v]||<=M2||u||||v||`, differentiation at fixed t/code/horizon gives

    ||dL|| <= 6 M1 eta^2,
    ||d2L|| <= (6 M2+14 M1^2) eta^2.                 (6)

Proof: differentiate the last identity in (5). For
`C=V*D_E V`, one has `||C||<=eta`, `||dC||<=2M1 eta`,
`||d2C||<=(2M2+2M1^2)eta`. The corresponding bounds for
`V*D_E^2 V` are `2M1 eta^2` and `(2M2+2M1^2)eta^2`.
Product differentiation gives (6), including both orders of each mixed
product. These are operator bounds on the complete input space.

Thus `F_in-G` is O(b^2), while the actual partition effect G is O(b).
If the ACTUAL isometry jets and counting dimension grow at most
polynomially in n, the normalized first-source difference `b^-1 dL`
vanishes exponentially. Moving-preparation trace norms must be included
as well; bounded preparation source contributes `||d rho||_1 eta^2`.
This is an explicit transport estimate, not deletion of L at finite n.

For fixed `0<=z<1`, the full feedback-source difference satisfies

    |d[-log det(I-z F_in)+log det(I-z G)]|
    <= dim(H) eta^2 M1
       [6z/(1-z) + 2z^2 b/(1-z)^2].                 (7)

Use `dG= dV* E V+V*E dV`, the resolvent identity and (6).
The factor `dim(H)` is the genuine counting dimension; it is not silently
replaced by a prepared trace. At fixed n the mandatory baseline cost n is
still present in the original partition. The factor b^-1 in this estimate
is a stated comparison normalization, not a new physical coupling or a
license to make increasingly long programmes free.

Equation (7) alone does not give a Palatini source: G is the paid-history
effect actually derived above, and its field law has to be evaluated.
For arbitrary long histories, physical compilation of `J_E` and its
extra clock/work requires its own admitted construction. The n=1 exact
Golden specialization is not an automatic implementation for all n.

### 4a. The actual original repeated-history jets meet the polynomial premise

Here d and d2 denote field tangents at fixed h and n in an h-uniform
chart norm. Refinement h->0 is the external sequence, not an unscaled
derivative with respect to h. The resulting estimate controls an absolute
normalized source difference; it does not preserve a nonzero geometric
coefficient unless that separate source has itself been proved.

This premise need not be left as an arbitrary future assumption for the
original fresh-round instrument. Fix a bounded C2 field chart with a
uniform strict margin for all of its actual Julia contractions, bounded
observer isometries/inverses and their jets, and bounded jets of the
coframe and proper links. Use the source convention of the original
finite instrument, including the positive stored adjoint. Each round has
the same finite32 controlled Julia words and128 Kraus rows. Shifts and
Walsh controllers have operator norm one. The square-root derivatives
are uniformly bounded on the strict-margin chart: their first jets solve
`B dB+dB B=dM`, with `B>=sqrt(delta) I`, and the second jet solves the
same Sylvester equation with the two retained first-jet products.
Consequently its complete one-round isometry satisfies

    ||dV_1||<=B1,       ||d2V_1||<=B2,

with constants independent of the site count. This also follows directly
by summing the128 row-jet bounds. The scaled Dirac input is `hD/16`, a
fixed finite sum of the bounded native word blocks; no unscaled
`||D||=O(h^-1)` is incorrectly used in that isometry bound.

Append the real fresh output registers at each round, retaining every
old register. Composition of these isometries and the product rule give
on the complete chronological carrier

    M1<=n B1,
    M2<=n B2+n(n-1) B1^2.                              (10)

There is no factor128^n: all untouched factors are isometries. For mixed
directions the `n(n-1)` term contains both orders of the differentiated
rounds. This is an application of the existing primitive first-jet
composition principle, with its explicit second product rule; no new
physical law or allowed operation is inferred.

On a fixed-volume four-dimensional lattice, including the unchanged
finite reference multiplicity, `dim(H)=O(h^-4)`. In the actual positive
clock regime `n epsilon_h` in a fixed compact positive interval and
`epsilon_h=p^2 h^2/64`, this is `O(n^2)`. At `t=ln(phi)`, (7) therefore
gives the genuine bound `O(n^3 p^n)` for the `p^-n`-normalized first-source
error. The bound tends to zero. Bounded actual preparation trace jets
can be included as above. This is a uniform transport of the two stated
test effects on that strict chart; it is not the original unscaled raw216
norm, not a fixed-clock theorem for the full Book action, and not a
physical authorization to remove the mandatory n-step price.

## 5. Parent use and scope

The former unproved replacement "measured price partition -> same full
feedback determinant" now has a precise constructive version: either use
the complete `F_in=G+L` and all source rows, or prove the quantitative
transport (5)-(7) at the actual refinement/normalization. With a full-work
cut the determinant instead loses the prepared response by isospectrality.
These are checked maps with different domains, not alternative names for
one action.

This feeds the same-history action/source composition before the existing
Einstein/Holst theorem. It does not supply the original physical `Info`,
the admission/payment of the echo apparatus, a nonzero selected Einstein
coefficient, the missing same-action nonlinear refinement or raw216.
The full HJR stationary/minimum results keep their previous scope.

The companion exact checker verifies the Golden operator polynomials,
all-output finite echo identity, the nonzero complement source and the
all-work determinant source. The universal estimates are proved above;
finite fixtures are checks, not a substitute for the C2 argument.
