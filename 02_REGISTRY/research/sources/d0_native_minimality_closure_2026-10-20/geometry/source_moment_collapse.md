# Actual full128 source transport at the energy-preserving stratum

20 October 2026. Existing #334, input
`f569c786730301e1603ee64062beccc6b20d05e7`.
This is a source calculation, not a new action or a physical selector.

Consumed owners:

* `A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md`, §§1–4:
  literal paired Julia recycling, its bistochastic/selfadjoint identity,
  original full128 process and flat CAR relaxation eigenvalues;
* `sources/d0_same_history_price_composition_2026-10-20/FULL128_HEAT_PRICE_RECYCLING_BRIDGE.md`,
  (4), (12), §3a: actual thinned transition and the two-moment value theorem;
* `A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md`, (1), (4), (7), (10):
  true observer-positive adjoint and all moving fields;
* `A4D_NATIVE_FULL128_JONES_OBSERVER_SO3_QUOTIENT_2026_10_20.md`:
  the measured quotient is metric plus a unit observer, not metric alone;
* `A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md`:
  the separate physical coframe input `v=h e`, full trace and Riesz128.

## 1. One first-moment jet replaces all higher first-source moments

Fix the native finite Hilbert carrier and integer round number. Write

\[
 \Delta=D^2,\quad B=I-\alpha\Delta,\qquad
 \mathcal N^*(Y)=Y+\alpha[D T^*(Y)D-\{\Delta,Y\}],
 \quad E_j=(\mathcal N^*)^j(I).
\]

All derivatives below are genuine field derivatives at fixed native clock
and calibration. Moving observer, adjoint, Julia roots and preparation are
included through their actual smooth matrices. In the original process
`T=T*` by the paired-Julia identity; the first lemma only needs unital CP.
Here N is the ideal critical-thinning map of its owner. A recorded finite
Golden controller approximates this map; its exact flat first-source
statement is given below. Neither its compulsory admission nor its work
and Info valuation is assumed to be free.

Suppose at the base field

\[
 T^*(\Delta)=\Delta,\qquad T^*(\Delta^2)=\Delta^2.
 \tag{1}
\]

Set `F=T*(Delta)-Delta`, and let `dot F` denote its complete derivative,
including `dot T`. For every polynomial f (and hence every analytic f on
the finite spectral neighborhood),

\[
 \boxed{\quad
 \partial_\xi[T^*(f(\Delta))-f(\Delta)]
       =D f_\Delta[\dot F].\quad}
 \tag{2}
\]

**Proof.** Use the literal smooth Kraus Stinespring isometry V, so
`T*(Y)=V*(Y tensor I)V`. Equality in the second moment gives
`Delta_out V=V Delta`. Put `A=V* dot V`, which is skew Hermitian.
Then

\[
 \dot F=T^*(\dot\Delta)-\dot\Delta+[\Delta,A].
\]

Differentiating a polynomial between the intertwining V and V* gives
`D f_Delta[T*(dot Delta)-dot Delta]+[f(Delta),A]`.
The polynomial identity
`D f_Delta[[Delta,A]]=[f(Delta),A]` proves (2). This proves a new collapse
of the source moment hierarchy; it does not reprove generic primitive-jet
composition. No derivative of a norm or of a square root of the variance
is taken at its zero.

Let `K_j=E_j-B^j`. The owned recurrence and (1) give `K_j=0` at the base.
Their full first jets obey the exact finite formula

\[
 \boxed{
 \dot K_m=-\alpha^2\sum_{j=1}^{m-1}(\mathcal N^*)^{m-1-j}
 \left[D\sum_{r=0}^{j-1}B^r\dot F B^{j-1-r}D\right].}
 \tag{3}
\]

Terms `dot N*(K_j)` and differentiated outer D factors vanish because
the undifferentiated defects vanish, not because those fields are frozen.
For the actual CP subunital transition and `0<=Delta<=Lambda I`,

\[
 \|\dot K_m\|\le {m(m-1)\over2}\alpha^2\Lambda\|\dot F\|
 \le2p^4\Lambda\|\dot F\|,\qquad m\alpha=2p^2.
 \tag{4}
\]

Thus (1) plus `dot F=0` on a specified variation space supplies the whole
first-source heat/history transport there. Value-level moment equality on
a family alone does not assert `dot F=0` in its normal directions.

## 2. Application to the actual flat full128: ALL scalar first-source rows

Take any homogeneous coframe, constant observer and identity links in the
original positive chart. Keep all site momenta and CAR16 grades. On a
Fourier block k the true shifted-adjoint CAR identity gives

\[
 D_k^2=\lambda_k I_{16}.
\]

Every original paired Julia factor preserves k. Its recycling is
bistochastic, so `T*(P_k)=T(P_k)=P_k`; therefore (1) holds on the entire
carrier. Here `P_k` is the full sixteen-dimensional block, not one grade.

For **every** smooth ambient variation of the actual coframe, proper
links or observer, including spatially varying variations,

\[
 \boxed{\quad(\dot F)_{kk}=T_k^*((\dot\Delta)_{kk})
                         -(\dot\Delta)_{kk},\qquad
              \operatorname{Tr}_{16}(\dot F)_{kk}=0.\quad}
 \tag{5}
\]

Indeed each base Kraus matrix is block diagonal. In the kk block of
`(dot T*)(Delta)`, its undifferentiated factor forces the intermediate
momentum to be k. This block is consequently
`lambda_k (dot T*)(I)_kk=0`. Bistochasticity then gives the trace statement.
This is valid even though the differentiated Kraus factor mixes momenta.

On each diagonal block, duality gives

\[
 \operatorname{Tr}_{16}(\mathcal N^*Y)_{kk}
       =b_k\operatorname{Tr}_{16}Y_{kk},\qquad
 \operatorname{Tr}_{16}(D_k X D_k)=\lambda_k\operatorname{Tr}_{16}X,
 \quad b_k=1-\alpha\lambda_k.
\]

Applying these identities to (3) proves, at every finite m,

\[
 \boxed{\quad
 \operatorname{Tr}_{16}(\dot E_m-\partial_\xi B^m)_{kk}=0
                     \quad\hbox{for every k and every ambient }\xi.
 \quad}\tag{6}
\]

In particular all of the following have equal values **and equal full
first derivatives** at this actual flat base:

\[
\begin{aligned}
 \operatorname{Tr}E_m&=\operatorname{Tr}B^m,\\
 \operatorname{Tr}\log[(1-z)I+zE_m]
   &=\operatorname{Tr}\log[(1-z)I+zB^m],\\
 \operatorname{Tr}(\rho E_m)&=\operatorname{Tr}(\rho B^m),
 \qquad \rho=\sum_k w_k P_k.
\end{aligned}\tag{7}
\]

The derivative statements in (7) follow from (6); the feedback weight
`z/[(1-z)+z b_k^m]` is scalar in each full CAR block. A moving normalized
preparation contributes `Tr(dot rho K_m)=0`, so it was not frozen.
The original fixed-RIGHT128 Riesz density is the case `w_k=1/128` on
its complete eight-momentum shell and zero elsewhere. OldRIGHT is an
unchanged identity spectator throughout.

This is the promised actual parent substitution: the flat **full trace,
feedback and complete-Riesz scalar first-source** comparison does not need
infinitely many separately bounded source moments. Every original ambient
field row is included. Neither a full Book valuation nor a thermal
preparation law follows from equating these candidate scalar functionals.

For homogeneous coframe and observer variations with links kept identity,
the scalar-block identity holds throughout the varied chart, and actually
`dot F=0` as an operator. This stronger statement does not extend to all
proper-link directions.

**The real finite-cap controller is also covered on this flat base.**
For any field-independent actual acceptance `c_*` in [0,1], put
`alpha_*=p epsilon c_*` and use the literal sub-map
`N_*^*=Id+(epsilon-alpha_*)D T*(.)D-epsilon{Delta,.}/2`.
The same proof has `b_k` replaced by `1-alpha_* lambda_k`:
`N_*^*(I)=B_*`, its kk-block trace scales by `b_*k`, and its differentiated
identity is `dot N_*^*(I)=-alpha_* dot Delta`. Thus (6)–(7) hold exactly
with `B_*^m` for the owned finite-cap `c_M`. Comparison of that factor
to the original B still requires the actual finite-cap error bound;
the controller records and their complete price remain retained.

### 2.1. Actual paid-port consumer, with NO thinning or extra controller

Use the original unconditioned full128 map, not N:
`Phi*(Y)=Y+epsilon[D T*(Y)D-{Delta,Y}/2]`.
The already owned literal 0/10 price is

\[
 C_{\rm port,n}=n+p\varepsilon\sum_{j=0}^{n-1}
                   \operatorname{Tr}[\rho(\Phi^*)^j\Delta].
\]

Its known flat value is `n+p epsilon n R`. The NEW assertion is that its
**full ambient first source**, not only the derivative restricted to the
flat family, is exactly

\[
 \boxed{\quad
 d C_{\rm port,n}=p\varepsilon n\,d\operatorname{Tr}(\rho\Delta)
                 =p\beta\,dR,\qquad n=m/2.
 \quad}\tag{7a}
\]

To prove it, write `Y_j=(Phi*)^j Delta`. At the base `Y_j=Delta`.
The literal derivative of the map with its input held fixed satisfies
`[(dot Phi*)(Delta)]_kk=0`: the `dot T*(Delta)` block vanishes as in
(5), while the remaining terms are
`epsilon lambda_k(dot D_kk D_k+D_k dot D_kk-dot Delta_kk)=0`.
Moreover `Tr16(Phi*X)_kk=Tr16 X_kk`. Induction in the differentiated
Y recursion gives `Tr16(dot Y_j)_kk=Tr16(dot Delta)_kk` for every j.
The moving-preparation term contributes `n Tr(dot rho Delta)`, yielding
(7a) without freezing rho. For the actual fixed-Gram Riesz128 preparation,
`dot rho` is tangent to its unitary orbit and `[rho,Delta]=0`, so this
preparation term is zero; the whole independent field covector remains.

Thus the existing literal port code supplies a genuine `p beta` multiple
of the Rayleigh first-source slot on the full flat ambient chart. There
is no fair extractor, extra symmetrizer, readout entropy assumption or
new physical price in (7a). Other paid labels, work and Book Info remain
separate. This statement does not extend (7a) to a curved family without
controlling its actual recycling sources.

## 3. An ORIGINAL allowed link has a nonzero operator source at that base

Use the literal homogeneous full16 family `C_r=nu c_r`, `0<nu<1`,
rest observer and identity links. This is the source owner's fixed-nu
continuum carrier; it is distinct from the `nu=h` physical scale of §4.
The native creator order may be `(0,2,3,1)`; the calculation uses those
actual creators and is unchanged by a common occupation-basis conjugacy.
Take momentum `(k,0,0,0)`, `theta=kh`, and the one real proper link

\[
 U_0(t)=\exp(ht\Omega_{23}),\qquad
 \Gamma=c_2c_3^*-c_3c_2^*.
\]

This is a spatial rotation fixing the original time leg and observer;
it even preserves the old own-leg/positive-adjoint conditions. It uses an
existing proper-link field slot, without enlarging the matrix domain.
Exact compilation into compulsory primitive gates is not established here.
Let `b_J=sqrt(1-nu^2)` and `s=(1-b_J)/2>0`. The owned flat Clifford
eigenvalue formula gives `T_0(Gamma)=(1-s)Gamma`. Direct differentiation
of the original forward plus its true adjoint gives

\[
 \lambda_h={4\nu^2\over h^2}\sin^2{kh\over2},\quad
 \dot\Delta=-{2i\nu^2\over h}\sin(kh)\Gamma,
 \boxed{\quad \dot F=-s\dot\Delta\ne0\quad}
 \tag{8}
\]

whenever `sin(kh)!=0`. Here `dot T*(lambda_h I)=0` exactly, since the
actual recycling remains unital while the link moves. Thus the zero of
the scalar trace in (6) is not a zero of the real operator source.

The discrepancy can be summed at the actual arbitrary round depth.
Put `b=1-alpha lambda_h` and `r=1-alpha lambda_h(1+s)`. Gamma commutes
with D on this momentum block, and `N*_0(Gamma)=r Gamma`. Equation (3)
then yields

\[
 \boxed{
 \dot K_m=
 \left[m\alpha b^{m-1}-{b^m-r^m\over\lambda_h s}\right]\dot\Delta.
 }\tag{9}
\]

The same identity follows by directly differentiating each of the actual
m steps, with no new choice of history weight. With fixed physical k,
`alpha=p^2h^2/128`, `m=256h^{-2}`, `beta=2p^2`, the coefficient tends to

\[
 e^{-\beta\lambda}
 \left[\beta-{1-e^{-\beta\lambda s}\over\lambda s}\right]>0,
 \qquad \lambda=\nu^2 k^2,\qquad
 \dot\Delta\longrightarrow-2i\nu^2k\Gamma.
 \tag{10}
\]

The positivity uses `1-exp(-x)<x` for x>0. Therefore this actual
operator first-source discrepancy does not disappear in the fixed-time
continuum limit, although (6) remains exactly true. A supplied spin-biased
test density can see it; no such density is declared compulsory or
identified with the original complete Riesz128 density. The result
forbids promoting scalar/Riesz equality to equality of all retained
operator sources or all complete native prices.

**The scaling boundary is essential.** The nonzero limit (10) uses the
literal unscaled operands `C_r=nu c_r`, whose nonzero physical-momentum
energies tend to `nu^2 k^2`. On the primary common-coframe operands
`C_r=h nu c_r`, substitute `nu_h=h nu` everywhere in the same exact
finite formula instead. Then

\[
 \lambda_h=4\nu^2\sin^2(kh/2),\quad
 \dot\Delta=-2ih\nu^2\sin(kh)\Gamma,\quad
 s_h={1-\sqrt{1-h^2\nu^2}\over2}.
\]

At fixed physical k these are respectively O(h^2), O(h^2), O(h^2),
and (9) gives `dot K_m=O(h^6)` on that block. Uniformly in lattice
momentum, the same bounded physical-link tangent gives `dot K_m=O(h^3)`.
Neither estimate alone controls an unnormalized sum over O(h^-4) modes;
the exact first-trace cancellation (6) still does. Thus (10) is NOT an
operator-source no-go for the differently scaled primary carrier.

## 4. Same physical flat coframe: heat matching does not solve observer Euler

This is a new application to the **same physical coframe** of the primary
flat-source owner, not a re-use of the four-return Euclidean `record(G,n)`
candidate in `A4D_NATIVE_RELATIVE_OBSERVER_SOURCE_JET.md`.

Keep the null metric, coframe `v_r=h e_r`, proper links I and full128
Riesz shell from that owner. The genuine independent observer curve is

\[
 n(\chi)=\cosh\chi\,{e_++e_-\over\sqrt2}+\sinh\chi\,e_x,
 \qquad h_n=-\eta+2n_\flat n_\flat^T.
\]

The physical Lorentz metric and all coframe/link variables stay fixed.
At zero the positive pairing is I, and its only derivative entries are
`(dot h_n)_(+,x)=(dot h_n)_(-,x)=-sqrt(2)` and their transposes.
For `a_r=exp(i theta_r)-1`, the exact full-CAR symbol is
`Delta(k,chi)=(a* h_n(chi) a) I16`. Consequently

\[
 \mu=\sum_r(2-2\cos\theta_r),\qquad
 \dot\mu=-2\sqrt2\,\Re[\bar a_x(a_++a_-)].
 \tag{11}
\]

The rank128 shell has only one nonzero momentum coordinate per mode;
thus `dot mu=0` on that entire shell and the true Rayleigh first source
is zero. The actual H and feedback first derivatives are the original
scale-source formula with `mu` in its numerator replaced by `dot mu`.
For any even-in-each-angle weight f(mu), the sine cross terms sum to zero
exactly, leaving

\[
 \sum_k\dot\mu_k f(\mu_k)=-2\sqrt2\sum_k A(\theta_k)f(\mu_k),
 \quad
 A=(1-\cos\theta_x)[(1-\cos\theta_+)+(1-\cos\theta_-)]\ge0.
\]

The same bounded-band finite-B argument already owned for this physical
scale therefore gives

\[
 \boxed{
 {1\over L^4}\partial_\chi S_{HJR}\big|_0\longrightarrow
 -4096\sqrt2\,z\beta
 \int_{[0,2\pi]^4}
 {A(\theta)e^{-\beta\mu(\theta)}\over
  1-z+ze^{-\beta\mu(\theta)}}\,{d^4\theta\over(2\pi)^4}<0.
 }\tag{12}
\]

The integral is strictly positive before its minus sign. The H derivative
is O(1) and vanishes after dividing by L^4; the R derivative is exactly
zero. Thus the observer at this original flat representative is not a
stationary observer of the bare HJR price for sufficiently fine meshes.
Equation (7) transfers this very source to the actual ideal-thinning
candidate; it does not cancel it. A genuine envelope minimum would have
to move the measured observer, or the actual independently derived
remaining price must supply the missing source. The SO(3) quotient in
the separately specified Jones experiment retains a genuine observer;
it supplies no license to discard this independent observer row or to
declare its movement physically invisible on the present carrier.
This is a test of the conditional price, not a no-go for full D0 or for
every possible selected observer.

## 5. What this settles in the minimality-to-GR argument

The new substitution is (2)–(7a), with the real link obstruction (8)–(10).
It closes the scalar flat full128 **first-source comparison**, while
pinpointing why it cannot by itself give a metric-only law. It supplies
neither the full-price observer stationarity required by an envelope nor
local second-order metric dynamics.

For a genuine complete price S(g,u,other), a differentiable attained
interior observer minimum does give `d S_eff=partial_g S` on its observer
Euler solution. Its differentiated response is
`S_gg-S_gu S_uu^{-1}S_ug` when the stated inverse exists. The original
observer enters the true adjoint and the whole fixed-positive-time heat
functional; nothing in (1), minimum attainment or (7) makes that inverse
a pointwise algebraic operator, removes the global log normalizer, or
truncates the heat functional to its curvature coefficient. The already
owned fixed-positive-time source limit explicitly retains those terms.
This exact interface identifies what a future full-price minimum must
prove; it does not install that minimum as a new premise of the native law.

No new Lovelock proof, geometric rank survey, changed action, admitted
controller, selected Info, implicit deletion of records, or primary
Brinkmann full-price evaluation is asserted here.
