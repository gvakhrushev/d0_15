# Full retained history: information binding, clock scale and first source

17 October 2026. Same Draft #334, input `090c957fddde61946da03cac7d1e658a6197f4e5`.
Consumer: derive the actual information/price source of the retained history,
rather than try another code or identify a scalar curvature coefficient with
Einstein gravity. All 128 actual outputs, all spatial modes, full16 matter,
reference128, moving preparation and the true clock are retained.

**Results.** Under the existing SAME-history likelihood binding, code changes
cancel pointwise from Cost minus Info, including every source jet. On the
actual full128 process the pointer Shannon entropy and every smooth first
source have a derived leading scale: log(1/epsilon_h) times the actual total
exit count and its source, with uniformly bounded remainders. This is proved
directly on the complete history, without enumerating paths or differentiating
an unproved entropy limit. It does not choose this physical binding, discard
its raw normalizer or identify pointer entropy with coherent record entropy.

## 1. What is forced after a SAME-history binding

Use the [branch cocycle](A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md) and
[partition-corrected source](A4D_NATIVE_PARTITION_CORRECTED_BRANCH_INFORMATION.md)
on one fixed complete finite history frame Omega. In phi units, let

```text
mu_omega=phi^(-C_omega),  w_omega=phi^(-S_omega),
N=sum_omega w_omega>0,  q_omega=w_omega/N,
S_omega=C_omega-I_omega.
```

If these w, q, code and histories are the actual bound objects, algebra gives

```text
I_omega=[log(q_omega/mu_omega)+log N]/log(phi),
S_omega=[-log q_omega-log N]/log(phi),
E_q S=[H(q)-log N]/log(phi).                             (1)
```

This applies on positive-probability histories, with expectations defined
by the usual zero-mass extension. For ANY other supplied code mu', including
a moving code, C and I change by the SAME function
log(mu/mu')/log(phi). They cancel before averaging. Their full coframe,
proper-link, observer/density, preparation and actual clock derivatives
therefore cancel too. A syntactic code choice is not an independent source
selector in this contract. A change of history/test cut is a different map
and is not covered by this cancellation.

The exact expected source is dH/log(phi)-dlog N/log(phi). N=1 at a single
configuration is insufficient. If the Book weights are proved to be the
normalized probabilities of the complete trace-preserving instrument, then
N is identically1. Otherwise its actual raw-frame source remains. Multiplying
all raw w by a field-dependent common factor leaves normalized q unchanged
but changes that source; normalized outcome data alone cannot determine it.
This is a statement about the fixed raw-frame interface, not a new physical
weight or freedom asserted at every native prefix.

For example, if a proposed binding also proves projectivity
sum_child w_(omega child)=w_omega on the SAME complete prefix tree and
w_empty=1, its normalizers at all complete fixed-depth cuts are1 by induction.
One must establish that binding; it is not inferred for a geometry partition
or a different stopping cut from Born normalization on this instrument.

## 2. The actual probabilities, including every blank and both ports

The [complete channel](A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md)
and [variable-process owner](A4D_VARIABLE_RECORD_CHANNEL_CONSERVATIVITY.md)
give the exact finite round

```text
K_0=B_h=I-epsilon_h Delta_h/2,
K_alpha=sqrt(epsilon_h) ell_alpha,h,  alpha=1,...,127,
sum_alpha K_alpha* K_alpha=I-B_h^2,
epsilon_h=p^2 h^2/64, p+p^2=1.
```

The label0/port1 outcome is one of those 127 outputs. It is not absorbed
into the blank. From the actual native CFL bound,

```text
B_h >= b_* I,  b_*=1-2p^2>0.                            (2)
```

A supplied clock variation is covered only when its actual Kraus identities
and a uniform positive blank bound persist along the family; this proof
does not authorize a different programme by assigning epsilon arbitrarily.

After any positive-probability prefix omega of length j, use the actual
normalized conditional system/reference state rho_(j|omega). Set

```text
a_alpha=Tr ell_alpha,h*ell_alpha,h rho_(j|omega),
r=sum_alpha a_alpha
 =Tr(Delta_h-epsilon_h Delta_h^2/4)rho_(j|omega).
```

The conditional blank probability is 1-epsilon_h r>=b_*^2; conditional
nonblank probability alpha is epsilon_h a_alpha. The conditional state
contains the entire recorded history. No reset, uniform preparation,
reference pinching, fixed first-exit cut or extra ensemble is used.

Let M(omega) be the number of ALL nonblank outcomes in the n-round record,
q_h its full path distribution and m_h=E_q M. Define

```text
ell_h=log(1/epsilon_h),
L_h(omega)=q_h(omega)/epsilon_h^M(omega).                 (3)
```

L_h is an analytical likelihood density relative to counting times the
waiting-cell volume. It is not a replacement physical code or Book weight.
All logarithms in Sections2-5 are natural. The exact identity is

```text
H(q_h)=ell_h m_h-E_q log L_h.                            (4)
```

## 3. A uniform log-density bound on the full growing tape

Assume the existing uniformly smooth compact native chart and n epsilon_h
in a compact positive time interval. A uniform fourth initial energy moment
gives uniform fourth unconditional moments at every round by the
[whole-grid and integer-moment proofs](A4D_VARIABLE_RECORD_FIRST_SOURCE_LIMIT.md).
Write Lambda_h=I+Delta_h and M4=sup_(h,j)Tr Lambda_h^4 rho_h,j<infinity.

On the random history, log L_h is a sum of increments Z_j: log(1-epsilon r)
on a blank, and log a_alpha on outcome alpha. Zero-probability outcomes
carry no mass. From (2), -log(1-epsilon r)<=C epsilon r. Elementary scalar
bounds |x log x|+x log^2 x<=C(1+x^2), x>=0, and the fixed 127 marks give

```text
|b_j|:=|E[Z_j | prefix]| <= C epsilon_h(1+r_j^2),
E[Z_j^2 | prefix] <= C epsilon_h(1+r_j^2).                (5)
```

For the second bound the blank contribution is at most C epsilon_h^2 r_j^2;
for exit contributions use sum a_alpha^2<=r_j^2. No positive lower bound
on any a_alpha is required. The fixed number of marks, not the exponentially
large number of histories, occurs in C.

Decompose sum Z_j into the martingale sum of Z_j-b_j plus sum b_j. Orthogonal
martingale differences give the variance bound C sum epsilon E(1+r_j^2).
Cauchy-Schwarz in time gives

```text
E|sum_j b_j|^2 <= C T sum_j epsilon_h E(1+r_j^4).
```

For k=2,4, conditional spectral Jensen yields
r_j^k <= Tr Lambda_h^k rho_(j|omega). Averaging conditional states recovers
the exact unconditional rho_h,j. Hence (5) and the owned moment estimates imply

```text
E_q (log L_h)^2 <= C_(T,M4).                            (6)
```

This proves the required log-tail bound on the complete growing pointer
distribution. It does not presume a finite tape dimension, a support floor,
conditional-state convergence or an independently bounded history count.
In particular, (4) now gives

```text
|H(q_h)-ell_h m_h| <= C_(T,M4).                          (7)
```

## 4. Actual full first source: Fisher control removes the growing alphabet

Let V be a bounded smooth field/preparation direction in the declared chart.
Use the SAME normalized actual initial preparation and its tangent from the
first-source owner, including observer/density trivialization and normalization.
The integer n is locally fixed; any epsilon'_h/epsilon_h is an actually supplied
uniformly bounded programme jet. The owned orthogonal-innovation estimate gives
a uniform bound on the derivative Xi_h of the actual pure final
system/reference/full-tape vector Psi_h.

Resolve it in the literal full-tape basis as vectors v_omega,h. Then
q_omega=||v_omega||^2 and q'_omega=2 Re<v_omega,v'_omega>. Therefore

```text
sum_(q_omega>0) (q'_omega)^2/q_omega <=4||Xi_h||^2.       (8)
```

At q_omega=0 its first derivative is0. Finite-h pointer entropy is genuinely
C1 through such births; the formula uses its continuous zero-mass extension.
Since sum q'_omega=0 and M labels a fixed history at fixed n,

```text
H'_h-ell_h m'_h=-sum_omega q'_omega log L_h(omega).       (9)
```

Cauchy-Schwarz, (6) and (8) bound the absolute value by
2||Xi_h|| (E log^2 L_h)^(1/2), uniformly in h. No derivative of an O(1)
value remainder has been inferred. The actual amplitude tangent supplies
the Fisher bound; a density-tangent convergence hypothesis alone does not.

Equation (9) remains exact when epsilon moves. In differentiating (4), the
term -(epsilon'/epsilon)m from ell'_h m cancels the opposite explicit term
in the derivative of E log L_h. Dropping either term would give a false
clock source. Integer-depth changes have no ordinary derivative here.

## 5. The derived leading scale and its all-field limiting covector

Under the fourth-moment/weighted preparation-jet assumptions of the
first-source owner, the actual total count and its source converge to

```text
m_T=integral_0^T Tr Delta rho(t)dt,
dm_T[V]=integral_0^T[Tr Delta'[V]rho(t)+Tr Delta eta_V(t)]dt,
```

with the actual clock endpoint when supplied. These expressions retain all
coframe, true adjoint, proper-link, observer/density and matter jets.
Consequently (7),(9) prove

```text
H(q_h)/ell_h -> m_T,
dH(q_h)[V]/ell_h -> dm_T[V].                            (10)
```

Locally uniform input/jet bounds give locally uniform conclusions for bounded
families of these smooth directions. This includes all ten ambient metric
slots of the full matrix chart; it neither enlarges the restricted stored
variation image nor proves an all-grid rough raw source norm.

For a moving epsilon the derivative of the normalized H/ell_h has the extra
term +(epsilon'/epsilon)H/ell_h^2=O(1/ell_h); thus its actual derivative
has the same limit. We prove the leading limit and bounded remainders,
not convergence of the unnormalized finite part H-ell_h m_h or its source.

The normalization by ell_h in (10) is an evaluation of the given observable,
not a newly selected physical action unit. If (1) is the physical law, its
complete leading source additionally contains -dlog N/log(phi). To use (10)
for that action, one must prove N identically1 or control log N and its jet
relative to ell_h. A field-independent baseline cannot cancel dm_T.

## 6. What this changes in the gravity composition

On the [exact-LC cone family](A4D_SPATIAL_PREPARATION_VARIATIONAL_LIMIT.md#8-decisive-geometric-consumer-preparation-cannot-restore-an-invisible-cone),
the limiting labelled process and Delta are constant in coordinate forms.
Thus m_T and the leading normalized pointer price are also cone-independent
for the same transported preparation. The observed order-h^2 history signal
remains and is not determined by this leading limit. A physically selected
source at that scale needs the actual cut/normalizer/clock law, including
its full variation, rather than a different syntactic code under (1).

The [maximal operational-gain theorem](A4D_NATIVE_OPERATIONAL_GAIN_AND_MEMORY.md)
is a DIFFERENT conditional binding: for central reference and all stipulated
tests it gives I_max=Cost-S_vN, so net Cost-I_max=S_vN. It does not retain a
port cost term and merely change the coefficient in Cost-S_vN. The full
coherent golden tape need not have central reference. Importing that
theorem requires its actual test-algebra/reference hypotheses. Likewise,
the port-coercive preparation theorem applies to its stated Cost-S_vN
candidate and is not automatically a theorem for the net entropy in (1).

The complementary [coherent rank-birth analysis](A4D_COMPLETE_RECORD_NORMAL_BIRTH_SCALE.md)
tests the subleading fine history through the full output state, not by
substituting a rare probability for entropy. The physical history/test map
must determine which law is used. Neither law is chosen by this analysis.

All prior receipts and owners remain unchanged. This proof uses the exact
native probability/clock effects, moment propagation and actual tape-jet
bound; no history enumeration, old replay or Lean build is required.
The original fixed-g/independent-tau/all-ten raw h^-2/#216 terminal,
physical full-price selection and nonempty compatible joint refinement
remain OPEN. The [bounded packet](sources/d0_complete_history_information_2026-10-17/README.md)
pins the inputs and the separate finite algebra check used by the coherent
consumer; that check is not a proof of the analytic entropy/source limit.
