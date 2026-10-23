# Complete pointer history: finite part and its actual smooth source

17 October 2026. Same Draft #334, continuation of `efa3f8f3`.
Consumer: complete the finite part left open by the
[leading information-scale theorem](A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md),
using the SAME 128-output programme, all spatial modes, all16 forms and
reference128. No code, action, ensemble, physical normalization or clock
law is selected here.

**Result.** At fixed native clock, fourth initial energy control gives
convergence of `H(pointer)-log(1/epsilon) E(number of exits)` to the
continuous labelled-path entropy relative to the actual waiting-time
measure. A uniform eighth initial moment and convergence of the actual
normalized preparation tangent give convergence of its smooth first
sources. The source proof uses differentiated finite-path products and a
weak Hilbert-space derivative, paired with a strongly converging logarithmic
vector. It does not differentiate a value remainder or assume convergence
of the full tape derivative in norm. There is no pointer-probability floor.

## 1. Fixed clock, actual preparation and sufficient assumptions

Let the parameter s range in a compact interval inside the owned uniformly
smooth strict Julia/coframe/proper-link/observer/density chart. Spatial
coefficients and the actual parameter derivatives are controlled in every
finite smooth seminorm used below. Equivalently, one can use the already
declared smooth compact chart, without a claim of a minimal finite
differentiability index. Proper-link derivatives are O(h), not arbitrary
unscaled O(1) lattice-link variations. All existing field directions remain.

In this theorem h, p and epsilon_h=p^2 h^2/64 are independent of s. The
integer n_h is also locally fixed in s, and T_h=n_h epsilon_h converges to
T>0. Choose one fixed T_*>sup_h T_h. A parameter-dependent programme is
typed separately in Section8; differentiating an integer floor is not used.

Write the actual normalized system/reference vector as Psi_0,h(s), in the
common true observer/density Hilbert representation. Its actual tangent is
Xi_0,h. In raw variables x this means

```text
x=I_s x_raw, N=||x||^2,
Psi_0=x/sqrt(N),
Xi_0=(I_s x_raw'+I'_s x_raw)/sqrt(N)-(N'/(2N))Psi_0.       (F1)
```

Thus neither a moving pairing nor the preparation normalizer is frozen.
After the exact Fourier embeddings, assume Psi_0,h converges strongly,
locally uniformly in s. For the source theorem also require strong locally
uniform convergence of Xi_0,h to its continuous actual tangent Xi_0. The
tangent need only be a Hilbert vector; no H2 assumption on it is made.
Reference128 and every form component are retained in these statements.

For the VALUE theorem assume a uniform fourth initial energy moment. For
the SOURCE theorem the following convenient sufficient bound is used:

```text
sup_(h,s) Tr G_h^8 rho_0,h < infinity,
G_h=E_h* G E_h, G=I-sum_r partial_r^2,
rho_0,h=|Psi_0,h><Psi_0,h|.                              (F2)
```

This is an eighth moment, or an H8 bound on the normalized amplitude; it
is not a consequence of an unknown preparation Euler equation. The owned
integer Lyapunov estimates propagate it through the actual process. Moment8
is sufficient rather than asserted sharp. It supplies the fourth logarithmic
moment below. A Hilbert tangent convergence hypothesis is stronger than a
density-tangent-only hypothesis and is stated explicitly.

The finite-heat, variable-process and first-source inputs used here are
listed with their SHA256 pins in Section9. No previous entrypoint is run.

## 2. Exact common waiting cells: no history is omitted

Denote the true blank Kraus map by B_h=I-epsilon_h Delta_h/2, and the
127 nonblank physical maps by sqrt(epsilon_h) ell_alpha,h. The complete
label0/port1 map is among the127, and is not absorbed into the blank.
At fixed h every record has m nonblank marks alpha_1,...,alpha_m. Let
j_i>=0 be the number of blanks immediately before its i-th mark. The
remaining number of blanks is

```text
j_final=n_h-m-sum_i j_i>=0.                              (F3)
```

There is exactly one record for these data. Use the disjoint path space

```text
Omega_*=disjoint_union_(m>=0)
  {u_i>=0, sum_i u_i<T_*} x {1,...,127}^m,
d nu=du_1...du_m times counting marks,
nu(Omega_*)=sum_m (127 T_*)^m/m! = exp(127 T_*).          (F4)
```

For m=0 this is a single atom. To record (F3) assign the FULL cell
prod_i[j_i epsilon_h,(j_i+1)epsilon_h). Its volume is epsilon_h^m.
Since sum j_i<=n_h-m, the cell lies in sum u_i<=T_h. These cells are
disjoint; other points have density zero. Jump steps consume one time
step each; ignoring the m in (F3) would give the wrong terminal factor.

On this cell define the Hilbert-valued density amplitude

```text
v_h=B_h^j_final ell_(alpha_m),h B_h^j_m ...
                  ell_(alpha_1),h B_h^j_1 Psi_0,h,
f_h=||v_h||^2=q_h(record)/epsilon_h^m.                    (F5)
```

The operators in (F5) tensor the unchanged reference identity. In
particular integral f_h dnu=1 EXACTLY. The cells and their normalization
are field-independent under the fixed-clock assumptions, so

```text
||partial_s v_h||L2(nu)^2=||Xi_h,final||^2,               (F6)
```

where Xi_h,final is the actual derivative of the complete finite tape
purification. This equality includes every one of the 128 outcomes.

Let E_t=exp(-t Delta/2). The continuum amplitude is zero outside sum u<T,
and inside it equals

```text
v=E_(T-sum u_i) ell_(alpha_m) E_u_m ...
                         ell_(alpha_1) E_u_1 Psi_0.      (F7)
```

Here ell_alpha is the limit of the physical maps, not a change to an
analytically recombined record basis. Some limiting marks vanish, but
they are still present in (F4). Conservativity gives integral ||v||^2=1.
The owned fixed-m trajectory convergence, followed by conservation to
remove the positive jump-number tails, proves

```text
v_h -> v in L2(nu; H_system tensor C128_ref),
f_h -> f=||v||^2 in L1(nu).                              (F8)
```

This is stronger than marginal-state convergence and follows from the
actual path construction. For example the density difference is at most
2||v_h-v||L2. Fixed-m convergence and the total norm1 control the remaining
L2 tails; a bound on derivatives of those tails is not inferred.

## 3. The complete finite part is uniformly integrable

Let ell_h=log(1/epsilon_h) and M be the number of exits. Equation (F5)
gives the EXACT identity

```text
J_h:=H(q_h)-ell_h E_q M = -integral f_h log f_h dnu.      (F9)
```

The leading information-scale owner proves, from the conditional native
probabilities and fourth unconditional moments,

```text
integral f_h |log f_h|^2 dnu <= C.                       (F10)
```

Zero density is interpreted by its continuous mass extension. Put
phi_R(x)=x clip(log x,-R,R), phi_R(0)=0. This is globally (R+1)-Lipschitz.
The error of replacing x log x by phi_R in the integral is at most C/R,
by (F10). The limit inherits (F10) by an almost-everywhere subsequence
and Fatou. Hence, with delta_h=||f_h-f||1,

```text
|J_h-J| <= (R+1)delta_h+2C/R,
J=-integral f log f dnu.                                (F11)
```

First h tends to0, then R tends to infinity. This proves finite-part
VALUE convergence. The measure is the actual waiting-cell measure
determined by the native epsilon_h, not a chosen probability reference
on paths. Enlarging T_* changes nothing because the extra density is0.
This relative path entropy can have either sign; it is not discrete
Shannon entropy without its clock term.

## 4. Eighth energy control gives the stronger logarithmic tail needed by sources

For completeness the required additional moment does not assume a bound
on exponentially many paths. At a prefix use the actual conditional state,
rates a_alpha and r=sum a_alpha, with blank probability1-epsilon_h r.
The native CFL gives 1-epsilon_h r>=b_*^2>0. The increment of log f_h
is Z_j=log(1-epsilon_h r) on a blank and log a_alpha on mark alpha.

For k=2,4, elementary scalar bounds and the fixed number127 give

```text
E(|Z_j|^k |prefix)<=C epsilon_h(1+r_j^2),
|b_j|:=|E(Z_j|prefix)|<=C epsilon_h(1+r_j^2).             (F12)
```

For the blank term its logarithm is bounded and is at most C epsilon_h r;
for exits use x|log x|^k<=C_k(1+x^2). Conditional rates may vanish.

Write d_j=Z_j-b_j. The scalar martingale fourth-moment inequality gives
E|sum d_j|^4<=C E(sum E(d_j^2|prefix))^2+C sum E|d_j|^4.
It follows directly by expanding (sum d_j)^2, orthogonality of its
martingale terms, and the L4 maximal inequality; no trajectory count
enters its constant. From (F12) and time Cauchy-Schwarz this is bounded
by unconditional moments through order4. For the drift, time Holder gives

```text
E|sum b_j|^4 <= C T_*^3 sum_j epsilon_h E(1+r_j^8).      (F13)
```

Conditional spectral Jensen bounds r_j^k by the conditional k-th energy
moment. Averaging gives exactly the unconditional actual state. The
integer-moment estimate and (F2) therefore prove

```text
integral f_h |log f_h|^4 dnu <= C.                       (F14)
```

Only (F10) is needed for values. A bounded second log moment alone would
NOT prove the strong logarithmic-vector convergence used for sources.

## 5. Actual differentiated-path lemma: weak, not strong, full tape convergence

The following derivation identifies the derivative independently of (F8).
It is the source step that cannot be replaced by value convergence.

The owned differentiated stencil estimates give Delta'_h uniformly of
order2 and ell_alpha,h,ell'_alpha,h uniformly of order1, with convergence
on smooth core vectors in the common Fourier embeddings. The special
h Delta_h/16 physical row is also uniformly order1 by whole-band CFL;
its smooth-core limit and derivative are0. All derivatives include true
adjoints and the moving observer/density representation.

The uniform elliptic graph estimates give, for every fixed required a,b,

```text
||B_h^j||_(H_h^a -> H_h^(a+2b))
                    <=C_ab[1+(j epsilon_h)^(-b)],
                         j epsilon_h>=delta>0.         (F15)
```

Indeed B_h>=b_*I and B_h(lambda)<=exp(-epsilon_h lambda/2). Apply
sup_lambda(1+lambda)^b B_h(lambda)^j<=C_b(1+t^-b), then the owned
uniform equivalence between powers of I+Delta_h and Sobolev norms.
Higher equivalences follow by iterating the same order-2 parametrix on
the smooth chart. Core consistency and interpolation give strong graph
convergence on every positive-time compact interval. The continuum E_t
has the corresponding estimates.

At fixed integer j the exact parameter derivative is

```text
partial_s B_h^j = -(epsilon_h/2) sum_(l=0)^(j-1)
                         B_h^(j-1-l) Delta'_h B_h^l,
partial_s E_t = -(1/2)integral_0^t E_(t-u)Delta' E_u du.  (F16)
```

For t>=delta split the sum/integral at u=t/2. In the first half, the
left factor has at least delta/2 smoothing, while Delta'_h B_h^l acts
boundedly from H2 to L2. In the second half the right factor supplies
all needed smoothing before Delta'_h, and the left factor is bounded
on the resulting graph space. Thus there is no nonintegrable endpoint
singularity. Strong initial H2 convergence needed for the first half
follows by interpolation from strong Hilbert convergence and the
uniform eighth moment. Actual prep-tangent terms are different:
the first positive-time factor smooths Xi_0,h directly, so its strong
Hilbert convergence suffices without an H2 bound.

Now fix m and restrict to a compact waiting simplex with ALL m+1 gaps,
including the terminal gap, at least delta. Differentiate the finite
product (F5): insert one ell'_alpha,h, one derivative (F16), or Xi_0,h.
Positive gaps, (F15),(F16) and smooth-core consistency prove convergence
of these differentiated products there, uniformly on compact parameter
intervals. This includes the physical marks whose leading limit is0.
Constants may depend on m and delta; no uniform derivative estimate
as m tends to infinity is asserted by this argument.

Finite m and such interior time cutoffs, with smooth output vectors,
together with tests compactly outside sum u<=T, form a dense test class
in L2(nu;H). On those exterior tests the discrete amplitudes and their
derivatives are eventually0. The boundaries removed have measure0;
the m=0 atom has its positive terminal time T. Independently, the owned
orthogonal-innovation estimate and (F6) give the GLOBAL bound

```text
sup_(h,s) ||partial_s v_h||L2
 <=sup ||Xi_0,h||+C sqrt(T_* E1)+C T_* sqrt(E2)<infinity. (F17)
```

The converging differentiated core products therefore define a bounded
functional on that dense class. Its unique Hilbert representative is
denoted v_s'. Every weakly convergent derivative subsequence has these
same pairings, so

```text
partial_s v_h weakly -> v_s' in L2(nu;H).                (F18)
```

The same conclusion holds when s_h tends to s: the core convergence is
locally uniform and the bound (F17) is uniform. The limiting core products
are the actual product-rule derivatives of (F7). They identify the weak
derivative and make v_s' weakly continuous in s. This proves identification;
it is not a guess based on Fisher boundedness alone. No derivative-tail
convergence, no uniform-in-m smoothing constant and no strong full tape
derivative have been used.

## 6. Weak actual derivative times a strong logarithmic vector

Set t_h=v_h log f_h, with value0 where v_h=0. For a Hilbert vector v,
the radial truncation

```text
T_R(v)=v clip(log ||v||^2,-R,R), T_R(0)=0
```

is globally (R+2)-Lipschitz. From (F14),
||t_h-T_R(v_h)||L2<=sqrt(C)/R, and the same estimate holds for v.
Consequently

```text
||t_h-v log f||L2
 <=(R+2)||v_h-v||L2+2 sqrt(C)/R ->0.                    (F19)
```

This treats zero-density paths without defining their score by division.
Equivalently, f'_h/sqrt(f_h) has its actual Fisher bound and is paired
with the strongly converging sqrt(f_h)log f_h. An unidentified weak score
on a zero-density set contributes0.

At finite h, pointer entropy is C1 through probability births. Since
integral f_h=1, its derivative has integral0. EXACTLY at fixed clock,

```text
J'_h=-integral f'_h log f_h dnu
    =-2 Re <partial_s v_h, t_h>L2
 -> -2 Re <v_s',v log f>L2 =: j(s).                     (F20)
```

Thus the actual first source has been passed by (F18),(F19), not by
differentiating (F11). The right-hand side is continuous: v_s' is weakly
continuous, v log f is strongly continuous by the same truncation argument,
and the derivatives are uniformly bounded. Passing to the limit in the
finite-h fundamental theorem of calculus proves J is genuinely C1 with
J'=j. The sequential locally uniform version of (F18),(F19) also proves
locally uniform convergence of J'_h on the stated compact chart.

All ten smooth metric slots available in the full matrix chart, proper
connection, observer/density and actual preparation directions are included
by choosing the corresponding parameter curve. This does not enlarge
the restricted stored-adjoint variation image or prove a rough all-grid
raw source norm. The eighth moment and actual tangent hypotheses are
uniform assumptions on the given prepared family, not on unknown optima.

## 7. What is closed, and what weaker inputs do not prove

We have the actual fixed-clock expansion with its finite source,

```text
H(q_h)=ell_h E M+J+o(1),
dH(q_h)[V]-ell_h d(E M)[V] -> dJ[V].                     (F21)
```

The count on the left remains the actual finite-h count. If its own
weighted preparation-jet hypotheses from the first-source owner also
hold, its already proved limiting source can be inserted. For example
strong actual initial tangents in the first weighted space, together
with (F2), satisfy that additional count-source interface. Mere Hilbert
convergence of the tangent is not silently promoted to weighted convergence.

If only density value convergence and a Fisher bound are known, (F18)
is missing: derivatives can oscillate with the parameter. If only the
old log2 bound is known, (F19) is missing: bounded L2 logarithmic vectors
need not converge strongly. Those weaker hypotheses prove (F11), not
this source theorem. The actual differentiated core lemma and log4
estimate above are the two additional arguments.

No full strong h-jet of a Bernoulli-to-waiting-Fock purification is asserted.
Such a different claim can encounter concentrated collision layers.
Here h tends to0 while the genuine field derivative s is taken at each
fixed cell structure, which is why (F6) and the weak identification apply.

## 8. Moving programme and physical price are separate typed inputs

If epsilon_h(s) moves at locally fixed n, the waiting cells in (F4),(F5)
move. Then (F6) is NOT obtained by pretending that their indicators have
an ordinary L2 derivative. The exact finite-pointer identity instead gives

```text
J'_h=-sum_omega q'_omega log(q_omega/epsilon_h^M)
                              +(epsilon'_h/epsilon_h) E M.       (F22)
```

For a fixed reference geometry one may rescale waiting times by T_h=n epsilon_h.
Unit waiting cells then have side1/n, independent of s. If g_h is the density
on this unit simplex, f_h=T_h^(-M)g_h under the time change, and exactly

```text
J_h=-integral g_h log g_h dnu_unit+log(T_h) E M.          (F23)
```

The Jacobian/source terms in (F22),(F23) agree. Applying a source theorem
in that representation requires the actual supplied bounded clock jet,
its convergence and the corresponding differentiated finite-path products
including terminal time. They are not inferred by differentiating an
integer-depth floor or by choosing a convenient clock. The fixed-clock
theorem above does not discard them.

Finally J is an evaluation of the actual pointer history, not a newly
selected physical action or a coherent entropy. Under the SAME-history
likelihood binding the full source still includes the original raw
-d log N/log(phi), besides its clock/count part. Its cancellation or
normalization must be proved by the native prefix/test map. Nor may
subtracting ell_h E M be selected as a physical renormalization merely
because the finite part has now been computed. The all-ten fixed-g,
independent-tau, unweighted raw h^-2/#216 target, actual physical binding
and nonempty compatible joint refinement are not supplied by this theorem.

## 9. Fixed analytical inputs and execution boundary

The derivation uses the following actual owners, with SHA256 at intake:

| Owned input | SHA256 |
| --- | --- |
| [Leading history scale](A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md) | `6a14686fcaab0b48b78b8ff4f784d989ea3ead1edf0ee28d48b7c20f76c4a7ed` |
| [Actual path process/conservation](A4D_VARIABLE_RECORD_CHANNEL_CONSERVATIVITY.md) | `44578338d793d96fbd8d575d182cf4087c721e3010c69a77163da0f40bef4715` |
| [Whole-grid calculus/moments](A4D_VARIABLE_RECORD_ENTROPY_AND_CODE_LIMIT.md) | `e934b157a7bb34c11a9ad377b32bb8838a6e342da31ab716bf0f14c4c913787f` |
| [Actual first jets/innovation](A4D_VARIABLE_RECORD_FIRST_SOURCE_LIMIT.md) | `bacfeb70e261f600cd4d1e305612eaf3ab6fe6f71bd384aab2f04fd588493d93` |
| [Finite heat/embeddings](A4D_NATIVE_FINITE_HEAT_SOURCE_LIMIT.md) | `4b69c188dcb3571429f4b45eddb1713621014de260c6e8b2095cc2907d9e4730` |

This is a bounded analytical continuation of those definitions and estimates.
No previous helper, certificate, spectral/rank census, receipt regeneration,
Lean build or scientific replay was executed. No new helper or JSON receipt
is introduced for this proof. The common-operator/all-field hypotheses,
strong normalized preparation tangent, moment8 source budget and fixed-clock
qualification are part of the theorem, not an unrecorded acceptance shortcut.
