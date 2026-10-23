# Complete quantum return balance on the original stopped native tape

22 October 2026. Existing Draft #334, native-programme-v1. Phase: native
realization / final source composition. This file owns the exact quantum
endpoint application of the already proved complete-history telescope and
non-reset first-return occupation law. It selects no new physical Info,
preparation, task, clock, Book03 action or GR status.

## 0. Parent substitution and consumed inputs

The missing parent term is the conditional terminal quantum WORK information
of the same stopped fine history. On the declared mixed-DATA carrier, the
stationary return marginal equals the initial density exactly. This turns
that term into a terminal Holevo information and yields an exact complete
relative-entropy price, its preparation boundary, and a stronger quantum
memory budget than a dimension bound.

Consumed inputs at local baseline a2790455c8477fc687202a6a203d596f7bd63045,
synchronized with published e92ecb3bdc53a2b958b1cc09a7b0398f978c87f3:

- [Complete native history theorem](../d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_SOURCE.md),
  Git blob cbd85b5173563f0f7bc5b17a31ddef7562916dff: exact efficient-instrument
  entropy telescope, actual block pinching and moving preparation.
- [Stopped fine KL theorem](../../A4D_NATIVE_FULL128_STOPPED_KL_QUANTUM_MEMORY_BUDGET_2026_10_22.md),
  Git blob 3a17ab2819b180d63197d7591a95b20e45354a2b: same-language reference,
  stationary fine-label counts and classical preparation defect.
- [Sequential stationary occupation](../d0_first_match_wald_2026-10-22/SEQUENTIAL_STATIONARY_OCCUPATION.md):
  true ordered CP products, transience and finite-cap occupation.
- Original CAR16/full128 constructor
  ../d0_book_uniform_source_2026-10-21/check_uniform_book_source.py,
  pinned Git blob ee8de4635d24c668949ac9a0186616ab7d59f2ed.

The original inverse-square stationary DATA state and its native generation
are inputs. No old checker or geometric root is replayed by this proof.
The parent application is
[A4D_NATIVE_COMPLETE_SOURCE_REDUCTION_2026_10_22.md](../../A4D_NATIVE_COMPLETE_SOURCE_REDUCTION_2026_10_22.md).
The independently authored native checker and raw-partition application
consume the identities below on their separately owned paths.

## 1. Carrier, stopping rule and exact terminal return

Let \(\mathcal I_z\) be a finite instrument on a DATA space of dimension
\(d\), with CPTP sum \(\Phi=\sum_z\mathcal I_z\). For the original complete
fine instrument, \(z\) resolves every Kraus index and
\(\mathcal I_z(X)=K_zXK_z^\dagger\). The CP identities below also hold
before such refinement, but the interpretation as coherent-pointer
dephasing gain uses the complete efficient instrument.

Fix a faithful density \(\rho\), active fine probabilities
\(q_z=\operatorname{Tr}\mathcal I_z(\rho)>0\), and a fixed coarse predicate
\(b(z)\in\mathcal A\), with \(m=|\mathcal A|\). The first outcome is the
anchor. Execute later rounds until the first later label with the same
coarse value; retain the whole fine history.

The literal [original first-label return](../d0_first_match_wald_2026-10-22/SEQUENTIAL_FULL128_BOOK_RETURN.md),
§2, compares the entire native seven-bit output: \(b(z)=z\).
On the owned nonzero-boost fixed-support chart, 64 of the 128 physical
fine slots are active, so this rule has \(m=64\). The native numerical
stopped diagnostics in this packet instead declare
\(b(z)=\text{port}(z)\), with \(m=2\), while still retaining all fine
labels. These are different stopping trees on the same instrument.
The theorem below is generic in the declared predicate; a port-return
result is not silently a full-label-return result. In particular the
stationary uncapped mean lengths are respectively 65 and 3.
Native resolvent, finite-cap and compressed-pair numerical diagnostics
here use the declared port predicate.

Put

\[
A_a=\sum_{b(z)=a}\mathcal I_z,\qquad
T_a=\Phi-A_a,\qquad
R_a=(I-T_a)^{-1}=\sum_{j\ge0}T_a^j .
\tag{1}
\]

Assume every \(T_a\) is transient, meaning its spectral radius is below
one. Inverses in (1) are superoperator inverses. No operators are assumed
to commute. The uncapped stopping experiment is complete because every
killed tail tends to zero. Uniqueness of the stationary state is not
needed for the following identities once stationarity and transience
are supplied; the native owner already supplies both.

For now suppose \(\Phi(\rho)=\rho\). The unnormalized sum of states before
later comparisons with anchor \(a\) is

\[
X_a=R_a A_a\rho=R_a(I-T_a)\rho=\rho.
\tag{2}
\]

Its trace is one for each anchor, although the initial probability of that
anchor need not be one. This is occupation over all its possible lengths,
not a renormalization of the anchor event.

Summing the genuine matched terminal states gives

\[
\boxed{\rho_T=\sum_a A_aR_aA_a\rho
=\sum_a A_a\rho=\rho.}
\tag{3}
\]

More precisely, if the last fine label is \(z\), then its full
subnormalized terminal DATA block is

\[
\boxed{X_z^{\rm last}
=\mathcal I_zR_{b(z)}A_{b(z)}\rho
=\mathcal I_z\rho.}
\tag{4}
\]

Thus the stopped last-fine-label/DATA marginal is exactly the original
one-round CQ state. This is an operator identity, stronger than a
terminal probability identity.

The total pretrial occupation, including the initial trial at the root,
is

\[
\boxed{\sum_{w\ {\rm live}}P(w)\rho_w
=\rho+\sum_aX_a=(m+1)\rho.}
\tag{5}
\]

Here each live prefix is counted once, just before its next native trial.
Taking a trace gives \(\mathbb ET=m+1\); applying a fine effect gives the
owned count law \(n_z=\mathbb E[\#z]=(m+1)q_z\).

## 2. Full quantum relative entropy and the gain price

For a complete stopped fine word \(\gamma\), let

\[
X_\gamma=K_\gamma\rho K_\gamma^\dagger,\quad
P_\gamma=\operatorname{Tr}X_\gamma,\quad
\eta_\gamma=X_\gamma/P_\gamma,\quad
\Gamma=\bigoplus_\gamma X_\gamma .
\]

Zero blocks contribute zero. Define the same-language iid reference
\(Q_\gamma=\prod_{z\ {\rm in}\ \gamma}q_z\), the classical stopped
divergence \(\mathcal M=D_{\rm KL}(P\Vert Q)\), and

\[
\chi_T=S(\rho_T)-\sum_\gamma P_\gamma S(\eta_\gamma),\qquad
\Xi=\bigoplus_\gamma Q_\gamma\rho,\qquad
\mathfrak D=D(\Gamma\Vert\Xi).
\tag{6}
\]

Both \(P\) and \(Q\) are normalized on this same prefix-free stopping
language. \(Q\) does not replace the native dynamics. Faithfulness and
integrability are established in §7.

The CQ entropy identity and (3) give

\[
\boxed{I_{\rm gain}=S(\Gamma)-S(\rho)=H(P)-\chi_T.}
\tag{7}
\]

For the complete efficient instrument, this is precisely the already
owned coherent-to-pinched entropy gain on the declared full pointer/work
block algebra. Directly expanding the block logarithm gives

\[
\begin{aligned}
\mathfrak D
&=\mathcal M+\sum_\gamma P_\gamma D(\eta_\gamma\Vert\rho)\\
&=\mathcal M+\chi_T+D(\rho_T\Vert\rho).
\end{aligned}
\tag{8}
\]

Consequently, on the stationary return,

\[
\boxed{\mathfrak D=\mathcal M+\chi_T
=(m+1)H(q)-I_{\rm gain}.}
\tag{9}
\]

Let \(\ell=\ln\varphi\) and \(c_z\) be genuinely additive charged
fine-outcome costs, with \(C_1=\sum_zq_zc_z\). Define
\(\mathscr S_1=C_1-H(q)/\ell\), the one-round **pointer** baseline;
it is distinct from the one-round gain price \(C_1-G(\rho)/\ell\).
For the declared
Cost-minus-gain convention, the exact same-experiment price is

\[
\boxed{\mathscr S_{\rm gain}
=(m+1)\left[C_1-\frac{H(q)}{\ell}\right]
+\frac{\mathfrak D}{\ell}.}
\tag{10}
\]

Actual additional preparation, comparator, controller, clock and work
charges retain their own ledger and source. Equation (10) does not price
such a ledger unless it is actually represented by the stated \(c_z\).
For the convention using \(S(\Gamma)\) itself instead of the gain,
subtract \(S(\rho)/\ell\) from (10).

## 3. Exact one-round quantum budget and compressed witnesses

Define the complete one-round instrument channel
\(F(X)=\bigoplus_z\mathcal I_z(X)\) and its entropy gain
\(G(\sigma)=S(F\sigma)-S(\sigma)\). The original one-round output
Holevo information on the stationary state is

\[
\chi_1=S(\rho)-\sum_zq_zS(\mathcal I_z\rho/q_z)
=H(q)-G(\rho).
\tag{11}
\]

### Convexity gives the complete stopped upper budget

For a faithful reference \(\rho\), the exact Bregman remainder of \(G\) is

\[
G(\sigma)-G(\rho)
-\operatorname{Tr}\big[M_G(\sigma-\rho)\big]
=D(\sigma\Vert\rho)-D(F\sigma\Vert F\rho)\ge0,
\tag{12}
\]

where \(M_G=\log\rho-F^*(\log F\rho)\), with the output logarithm
restricted to its fixed support. This follows by expanding both relative
entropies; the inequality is quantum data processing. Since
\(\rho>0\), every positive \(\sigma\) satisfies \(\sigma\le c\rho\),
so \(F\sigma\) is supported in \(F\rho\). The formula remains valid
for singular \(\sigma\) by continuity. It proves convexity of \(G\);
no convexity of the Shannon term alone is substituted.

Apply the owned full quantum telescope and then (5):

\[
\begin{aligned}
I_{\rm gain}
&=\sum_{w\ {\rm live}}P(w)G(\rho_w)\\
&=(m+1)G(\rho)+\mathcal L,\\
\mathcal L
&=\sum_{w\ {\rm live}}P(w)
\left[D(\rho_w\Vert\rho)-D(F\rho_w\Vert F\rho)\right]\ge0 .
\end{aligned}
\tag{13}
\]

The root contributes zero to \(\mathcal L\); the linear term in (12)
cancels by the full operator occupation (5). Equations (9), (11), and
(13) yield the exact complete quantum source decomposition

\[
\boxed{\mathfrak D=(m+1)\chi_1-\mathcal L.}
\tag{14}
\]

By (4), coarsening the full history to its last fine label gives the
one-round terminal ensemble. Holevo monotonicity under this coarsening
implies \(\chi_T\ge\chi_1\). More explicitly,
\(\chi_T-\chi_1=\sum_\gamma P_\gamma
D(\eta_\gamma\Vert\rho_{z_{\rm last}(\gamma)})\ge0\);
each reference block contains the supports of its constituent leaves.
The iid reference's last-fine probability is also \(q_z\): its anchor
class \(a=b(z)\) has probability \(q_a=\sum_{b(u)=a}q_u\), and the
eventual match within that class has conditional law \(q_z/q_a\).
Hence terminal-fine data processing gives explicitly
\[
\mathfrak D\ge
D\!\left(\bigoplus_z\mathcal I_z\rho\middle\|
         \bigoplus_zq_z\rho\right)=\chi_1 .
\]
Together with the stronger \(\chi_T\ge\chi_1\), this yields

\[
\boxed{\mathcal M+\chi_1
\le\mathfrak D=\mathcal M+\chi_T
\le(m+1)\chi_1,\qquad
0\le\mathcal M\le m\chi_1.}
\tag{15}
\]

Equivalently, the exact positive budget is

\[
\boxed{\mathcal M+(\chi_T-\chi_1)+\mathcal L=m\chi_1.}
\tag{16}
\]

This consumes the actual one-round output quantum information, rather than
only the coarser bound \(\chi_1\le S(\rho)\le\ln d\). It identifies three
nonnegative values: measured predictive memory, terminal quantum
information beyond the last fine label, and instrument data-processing
loss. It does not identify any of them with a selected physical Book Info.

### Consume the existing complete two-round receipt

Let \(I_1\) and \(I_2\) be the complete entropy gains after exactly one
and exactly two native rounds from this stationary input. These are the
objects already computed by the complete-history owner. Every depth-one
prefix is visited in the present stopping experiment, because the first
possible match is the second trial. The exact first-depth loss is

\[
\boxed{\mathcal L_{\rm first}
=\sum_zq_z\left[D(\rho_z\Vert\rho)
              -D(F\rho_z\Vert F\rho)\right]
=I_2-2I_1\ge0,\qquad
\rho_z=\mathcal I_z\rho/q_z.}
\tag{16a}
\]

Indeed \(I_2=G(\rho)+\sum_zq_zG(\rho_z)\) and
\(\sum_zq_z\rho_z=\rho\); apply (12). The remaining live-prefix
losses in (13) are nonnegative, so
\(\mathcal L\ge\mathcal L_{\rm first}\).
Also the stopped classical KL obeys
\(\mathcal M\ge I(Z_0;Z_1)\), by projecting its first two labels.
Together these give the stronger exact value window

\[
\boxed{\chi_1+I(Z_0;Z_1)
\le\mathfrak D
\le(m+1)\chi_1-\mathcal L_{\rm first}.}
\tag{16b}
\]

The existing [complete-history receipt](../d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_RESULT.json),
without a replay, gives the following numerical substitution on the
original CAR16/full128 chart at \(r=1/9,\nu=3/5\):

| Receipt-derived quantity | Nominal value in nats |
|---|---:|
| \(\chi_1\) | \(0.00016955914079330725\) |
| Fine first-two \(I(Z_0;Z_1)\) | \(6.512430039684602\cdot10^{-10}\) |
| \(\mathcal L_{\rm first}=I_2-2I_1\) | \(3.9309466792758485\cdot10^{-9}\) |
| Lower endpoint in (16b), declared port diagnostic \(m=2\) | \(0.00016955979203631122\) |
| Upper endpoint in (16b), declared port diagnostic \(m=2\) | \(0.0005086734914332425\) |

The exact inequalities are proved above. These displayed decimal endpoints
are not outward interval certificates: they inherit the owned receipt's
all-mode regularization budgets and floating evaluation scope. They are
not values of the full stopped \(\mathfrak D\), and their \(m=2\) upper
endpoint does not apply to literal full-label return.

For that literal rule, substitute \(b(z)=z\), \(A_z=\mathcal I_z\),
\(T_z=\Phi-\mathcal I_z\) and \(m=64\), using the already owned
transience of every active label. The exact application is

\[
\boxed{\mathbb ET_{\rm label}=65,\qquad
\mathscr S_{{\rm gain,label}}
=65\mathscr S_1+\mathfrak D_{\rm label}/\ell,}
\tag{16c}
\]
\[
\boxed{\chi_1+I(Z_0;Z_1)\le\mathfrak D_{\rm label}
\le65\chi_1-\mathcal L_{\rm first}.}
\tag{16d}
\]

Its exact nonnegative budget is
\(\mathcal M_{\rm label}
+(\chi_{T,{\rm label}}-\chi_1)+\mathcal L_{\rm label}=64\chi_1\).
The one-round \(\chi_1\), fixed-two-round mutual information and
\(\mathcal L_{\rm first}\) are shared inputs independent of either
stopping rule. Each rule nevertheless has its own stopped law,
reference, terminal ensemble and total loss. Equations (16c)–(16d)
are an analytic full-label application, not a numerical evaluation
of its full entropy, stopped source, cap boundary or resolvents.

The same receipt yields
\(\partial_r\mathcal L_{\rm first}\simeq8.11970971\cdot10^{-8}\) and
\(D_v\mathcal L_{\rm first}\simeq8.38316117\cdot10^{-8}\), where \(v\)
is the owner's one-port-invisible tangent. These are direct differences
of the full one/two-round source entries, with their inherited errors;
they do not result from differentiating (16b).
For the original rapidity coordinate,
\(r=\tanh(\theta/2)\) and \(dr/d\theta=40/81\) at this point.
An equality closure \(\mathcal L=0\) would require every prefix loss,
including (16a), to vanish; the existing numerical receipt supplies no
basis for imposing that equality.

Along a genuine smooth moving-stationary family, under §7's derivative
hypotheses, the exact source is
\(\dot{\mathfrak D}=(m+1)\dot\chi_1-\dot{\mathcal L}\).
Neither (15) nor positivity of these values supplies a derivative bound.
For a tangent leaving stationarity, use the explicit defects in §§4–6.

### Finite compressed first-two-plus-terminal quantum witness

Keep the first two fine labels \(u,v\) and terminal DATA, and sum over
all intermediate later fine labels. Write \(a=b(u)\). The exact compressed
quantum blocks are

\[
Y_{uv}=
\begin{cases}
\mathcal I_v\mathcal I_u\rho,&b(v)=a,\\
A_aR_a\mathcal I_v\mathcal I_u\rho,&b(v)\ne a.
\end{cases}
\tag{17}
\]

Their probabilities are the actual first-two probabilities
\(p_{uv}=\operatorname{Tr}\mathcal I_v\mathcal I_u\rho\), because the
remaining continuation is trace preserving. Their sum is \(\rho\).
The reference marginal is exactly \(q_uq_v\rho\): the iid future on the
same stopping language sums to one for each specified pair. Data
processing therefore gives the finite-matrix witness

\[
\boxed{\mathfrak D\ge
D\!\left(\bigoplus_{u,v}Y_{uv}\middle\|
         \bigoplus_{u,v}q_uq_v\rho\right)
=I(Z_0;Z_1)+\chi_{(Z_0,Z_1):D_T}.}
\tag{18}
\]

The two classical marginals are both \(q\) by stationarity. The same
construction works with the retained first two coarse ports: replace
\(\mathcal I_u,\mathcal I_v\) by \(A_a,A_b\). Its unequal-port block is
\(A_aR_aA_bA_a\rho\), and its equal-port block is \(A_aA_a\rho\).
This finite compression is a rigorous lower bound on the full value,
not a computation of the full stopped archive or its full derivative.
Different compressed lower bounds cannot be added without justification.

## 4. Arbitrary input: count, terminal and preparation defects

Now let \(\rho>0\) be arbitrary, keeping the same transient maps. Set

\[
\delta=(\Phi-I)\rho,\qquad
X_a=R_aA_a\rho=\rho+R_a\delta,\qquad
g_z=\sum_a\operatorname{Tr}\mathcal I_zR_a\delta .
\tag{19}
\]

The fine counts are \(n_z=(m+1)q_z+g_z\). The exact terminal defect is

\[
\boxed{e=\rho_T-\rho
=\delta+\sum_aA_aR_a\delta,}
\tag{20}
\]

and the last-fine block is
\(\mathcal I_z(\rho+R_{b(z)}\delta)\).
Equation (20) follows by applying each terminal \(A_a\) to (19), summing,
and using \(\sum_aA_a=\Phi\). In particular \(e\) is traceless; it is not
the stationary-preparation defect \(\delta\) alone.

Expansion of the full relative entropy gives, for any such input,

\[
\mathfrak D=-S(\Gamma)-\sum_zn_z\ln q_z
-\operatorname{Tr}(\rho+e)\log\rho .
\tag{21}
\]

Since the gain price is
\(\sum_zn_zc_z-[S(\Gamma)-S(\rho)]/\ell\), the signs are fixed:

\[
\boxed{\mathscr S_{\rm gain}
=(m+1)\left[C_1-\frac{H(q)}{\ell}\right]
+\frac{\mathfrak D}{\ell}
+\sum_zg_z\left(c_z+\frac{\ln q_z}{\ell}\right)
+\frac{\operatorname{Tr}(e\log\rho)}{\ell}.}
\tag{22}
\]

Both defects have zero value on a stationary input and can have nonzero
first sources there. The general information identities are

\[
I_{\rm gain}=H(P)-\chi_T+S(\rho_T)-S(\rho),\qquad
\mathfrak D=\mathcal M+\chi_T+D(\rho_T\Vert\rho).
\tag{23}
\]

One cannot silently reuse the stationary endpoint in (7) off that section.

For the explicit preparation cotangent, put

\[
w_z=c_z+\frac{\ln q_z}{\ell},\quad
E_z=\mathcal I_z^*(I),\quad F_c=\sum_zw_zE_z,
\]
\[
\boxed{B=\sum_aR_a^*F_c+
\ell^{-1}\left[\log\rho+
\sum_aR_a^*A_a^*(\log\rho)\right].}
\tag{24}
\]

The entire extra term in (22) is exactly \(\operatorname{Tr}(B\delta)\),
even away from stationarity. At a stationary base its first source is

\[
\boxed{\operatorname{Tr}(B\dot\delta),\qquad
\dot\delta=(\dot\Phi)\rho+(\Phi-I)\dot\rho.}
\tag{25}
\]

The adjoint order \(R_a^*A_a^*\) in (24) is essential. This is the actual
finite-memory preparation boundary supplied to the entropic-Poisson
consumer; it is not permission to freeze an independently variable input.

## 5. First source and reference cancellation at a stationary base

All native Kraus and actual preparation derivatives remain in
\(\dot X_\gamma\) by the full ordered product rule. Let
\(\mathcal L_\rho\) denote the Fréchet derivative of the matrix logarithm:

\[
\mathcal L_\rho(U)=\int_0^\infty
(\rho+tI)^{-1}U(\rho+tI)^{-1}\,dt .
\]

Differentiating the normalized complete relative entropy gives

\[
\begin{aligned}
\dot{\mathfrak D}
={}&\sum_\gamma\operatorname{Tr}\dot X_\gamma
 [\log X_\gamma-\ln Q_\gamma I-\log\rho]\\
&-\sum_zn_z\frac{\dot q_z}{q_z}
-\operatorname{Tr}\rho_T\mathcal L_\rho(\dot\rho).
\end{aligned}
\tag{26}
\]

The eigenvalue-zero terms use the amplitude limit in §7. The derivative
of total mass is zero, so no identity term is missing.

For every normalized moving \(\rho\),
\(\operatorname{Tr}\rho\mathcal L_\rho(\dot\rho)
=\operatorname{Tr}\dot\rho=0\).
At a stationary **base point**, (3) and \(n_z=(m+1)q_z\) cancel both
reference gradients in (26), even when the tangent has
\(\dot\delta\ne0\). Hence

\[
\boxed{\dot{\mathfrak D}
=\sum_\gamma\operatorname{Tr}\dot X_\gamma
 [\log X_\gamma-\ln Q_\gamma I-\log\rho]}
\tag{27}
\]

at that base point for every admitted tangent. This reference cancellation
does not cancel the price defects in (22). The complete price source is

\[
\boxed{\dot{\mathscr S}_{\rm gain}
=(m+1)\dot{\mathscr S}_1+
\dot{\mathfrak D}/\ell+\operatorname{Tr}(B\dot\delta).}
\tag{28}
\]

On a genuinely moving stationary family \(\dot\delta=0\); a frozen
preparation at a stationary base generally has
\(\dot\delta=(\dot\Phi)\rho\ne0\).

More generally, substituting \(n_z=(m+1)q_z+g_z\) and \(\rho_T=\rho+e\)
into (26) leaves the reference terms
\(-\sum_zg_z\dot q_z/q_z-\operatorname{Tr}e\mathcal L_\rho(\dot\rho)\).
This is also the exact finite-cap formula with the cap defects below.

## 6. Every finite-cap abort and its first source

Fix an integer \(K\ge1\), meaning at most \(K\) **later comparisons**
after the anchor. The cap is held fixed during differentiation. Define

\[
R_{a,K}=\sum_{j=0}^{K-1}T_a^j,\quad
X_{a,K}=R_{a,K}A_a\rho
=(I-T_a^K)\rho+R_{a,K}\delta,\quad
B_K=\sum_aT_a^K\rho .
\tag{29}
\]

The complete terminal state includes both matched and aborted branches:

\[
\rho_{T,K}=\sum_a[A_aX_{a,K}+T_a^KA_a\rho].
\tag{30}
\]

The continuation map \(G_{a,K}=A_aR_{a,K}+T_a^K\) is CPTP.
Indeed trace preservation of \(\Phi\) makes its trace telescope, while
each term is CP. Substituting
\(A_a\rho=(I-T_a)\rho+\delta\) in (30) proves the general endpoint:

\[
\boxed{e_K=\rho_{T,K}-\rho
=(I-\Phi)B_K+\left[I+\sum_aG_{a,K}\right]\delta.}
\tag{31}
\]

In particular, on a stationary family,

\[
\boxed{e_K=(I-\Phi)\sum_aT_a^K\rho.}
\tag{32}
\]

The stationary finite-cap terminal density need not equal \(\rho\).
Its exact fine counts, including the last failed comparison, are

\[
\begin{aligned}
n_{z,K}&=q_z+\sum_a\operatorname{Tr}\mathcal I_zX_{a,K}
=(m+1)q_z+g_{z,K},\\
\boxed{g_{z,K}
&=-\operatorname{Tr}\mathcal I_zB_K
+\sum_a\operatorname{Tr}\mathcal I_zR_{a,K}\delta.}
\end{aligned}
\tag{33}
\]

Use the complete capped reference \(Q_{\gamma,K}=\prod_{z\in\gamma}q_z\),
including its abort words. It is normalized. Equations (21)–(23) and
(26) remain exact after replacing all objects by their capped versions
and using \(g_{z,K},e_K\). In particular the full capped price is (22)
with these replacements. Its reference terms generally do not vanish
even at stationary input.

For completeness, the terminal last-fine block at finite cap is

\[
X^{\rm last}_{z,K}
=\mathcal I_zX_{b(z),K}
+\sum_{a\ne b(z)}\mathcal I_zT_a^{K-1}A_a\rho .
\tag{34}
\]

The second term consists of genuine capped aborts. Neither this block
nor its iid reference weight is generally the uncapped one in (4).

### Exact finite-cap jets

For \(j\ge1\),

\[
\dot T_a^j=\sum_{i=0}^{j-1}
T_a^i\dot T_aT_a^{j-1-i},\qquad
\dot B_K=\sum_a[\dot T_a^K\rho+T_a^K\dot\rho].
\tag{35}
\]

At a stationary base, with an arbitrary tangent,

\[
\boxed{\dot e_K
=-\dot\Phi B_K+(I-\Phi)\dot B_K
+\left[I+\sum_aG_{a,K}\right]\dot\delta,}
\tag{36}
\]

\[
\boxed{\dot g_{z,K}
=-\operatorname{Tr}[(\dot{\mathcal I}_z)B_K
+\mathcal I_z\dot B_K]
+\sum_a\operatorname{Tr}\mathcal I_zR_{a,K}\dot\delta.}
\tag{37}
\]

Thus differentiating (32) alone for a frozen preparation omits the last
term in (36). Away from stationarity, also differentiate the coefficients
of \(\delta\) in (31) and (33). These are finite matrix identities and
require no exchange of an infinite sum with a derivative.

### Trace-norm boundary estimates

If \(T_a^*(I)\le\kappa I\) for every anchor, with
\(\kappa=1-\varepsilon<1\), then
\(\operatorname{Tr}B_K\le m\kappa^K\). Equation (32) implies
\(\|e_K\|_1\le2m\kappa^K\).

There is also the sharper stopped-tail estimate. The genuine abort mass is
\(p_{{\rm abort},K}=\sum_a\operatorname{Tr}T_a^KA_a\rho
\le\kappa^K\). Continuing each aborted state with the CPTP eventual-match
map \(A_aR_a\) changes a state of this total mass, so

\[
\boxed{\|\rho_{T,K}-\rho_T\|_1
\le2p_{{\rm abort},K}\le2\kappa^K.}
\tag{38}
\]

On a stationary input this bounds \(\|e_K\|_1\).
These are value estimates. By themselves they give no bound on
\(\dot e_K\), an entropy derivative, or a uniform field/refinement source.
Equations (35)–(37) keep the actual jets explicitly.

## 7. Normalization, finite entropy and local differentiability

### Exact value domain

Finite dimension, a finite active alphabet, \(\rho>0\), and
\(r(T_a)<1\) suffice for all uncapped values above.
Transience makes every ordered killed tail decay geometrically, so
\(P\) is normalized and \(\mathbb ET<\infty\) also for nonstationary
inputs. Every active coarse reference probability is positive, so the
iid law \(Q\) terminates almost surely and is normalized on the same
language.

Let \(q_{\min}>0\). Then
\(-\ln Q_\gamma\le|\gamma|\,|\ln q_{\min}|\), whose actual expectation
is finite. The standard countable Gibbs inequality gives
\(H(P)\le\mathbb E_P[-\ln Q]<\infty\).
Conditional DATA entropies are between zero and \(\ln d\); therefore
\(S(\Gamma)<\infty\), all endpoint Holevo quantities are finite, and
(8) is finite because
\(-\log\rho\le|\ln\lambda_{\min}(\rho)|I\).
No terminal block needs to be faithful. Its support is automatically
contained in the full support of the reference \(Q_\gamma\rho\).

The complete stopped Kraus effects sum to \(I\): the omitted positive
effect is exactly the surviving killed tail and tends to zero.
Consequently the coherent stopped map is an isometry into the countable
history space. Its entropy is \(S(\rho)\), and pinching gives the stated
finite entropy gain. The finite telescopes converge to (13).
For example each local entropy change has absolute value at most
\(\ln|\mathcal Z_+|+\ln d\), and the total expected number of remaining
trials tends to zero at the cut. This also justifies summation of the
nonnegative Bregman losses in (13); each is bounded above by
\(D(\rho_w\Vert\rho)\le|\ln\lambda_{\min}(\rho)|\).

If \(q_z=0\) at a faithful input, positivity implies
\(\mathcal I_z=0\) on all operators. Such a structurally dark slot remains
on the physical carrier but contributes zero. The derivative statements
here use a fixed active alphabet and do not cross a birth of such a
reference probability.

### A sufficient local C1 theorem, separate from a value-tail bound

For uncapped derivatives require a fixed coarse predicate and finite
alphabet, C1 native Kraus amplitudes and C1 faithful input on a
neighborhood, with uniform lower bounds on the active \(q_z\) and the
input eigenvalues. Require locally uniform killed contraction, for example
\(T_a^*(I)\le\kappa I< I\) throughout that neighborhood. Smooth costs
are required for the price source. These assumptions suffice for
termwise differentiation of the entropy and relative-entropy sums.

Here is an explicit summability argument that retains every quantum mode.
For words of length \(n\), stack all amplitudes
\(V_\gamma=K_\gamma\sqrt\rho\). A killed mismatch step has stacked
operator norm at most \(\sqrt\kappa\). Bounded C1 single-step derivatives
and the full product rule therefore give, with local constants,

\[
p_n=\sum_{|\gamma|=n}\|V_\gamma\|_{\rm HS}^2
\le C\kappa^{n-2},\qquad
b_n=\left(\sum_{|\gamma|=n}
\|\dot V_\gamma\|_{\rm HS}^2\right)^{1/2}
\le C'(n+1)\kappa^{(n-3)/2}.
\tag{39}
\]

There are at most \(N_n=d|\mathcal Z_+|^n\) squared singular values
\(\lambda_j\) in this shell. The amplitude entropy is C1 even at a
zero singular value: \(s^2\log s^2\) and its first derivative tend to
zero as \(s\to0\). Its directional derivative obeys

\[
\left|\frac{d}{dy}
\left(-\sum_{|\gamma|=n}\operatorname{Tr}
V_\gamma V_\gamma^\dagger
\log(V_\gamma V_\gamma^\dagger)\right)\right|
\le2b_n
\left[\sum_j\lambda_j(\log\lambda_j+1)^2\right]^{1/2}.
\tag{40}
\]

For any probability vector \(\mu\) on \(N\) entries,
\(\sum_j\mu_j\log^2\mu_j\le(\log N)^2+2\log N+2\).
Indeed the tail of \(-\log\mu_j\) under \(\mu\) is bounded by
\(\min(1,Ne^{-t})\), and integrating \(2t\) times that bound proves
the inequality. Apply this to \(\mu_j=\lambda_j/p_n\); the exponential
bound on \(p_n\) controls also \(p_n\log^2p_n\). Thus the right side
of (40) is bounded by a fixed polynomial in \(n\) times \(\kappa^n\),
uniformly on the neighborhood. Its sum converges.

The reference terms are also absolutely differentiable:
\(|\log Q_\gamma|=O(n)\), \(|\dot{\log Q_\gamma}|=O(n)\),
\(\log\rho\) and \(\mathcal L_\rho(\dot\rho)\) are bounded, and
\(\sum_{|\gamma|=n}\|\dot X_\gamma\|_1\le2b_n\sqrt{p_n}\).
Uniform convergence of these first-derivative sums proves (26) and its
stationary specialization; this is a local C1 argument, not an inference
from a small scalar entropy tail.

One-step contraction is a convenient sufficient condition rather than
a necessary one. At a finite-dimensional transient point, some common
power satisfies \((T_a^*)^L(I)\le\kappa I<I\); continuity preserves
this inequality locally. Grouping mismatches into \(L\)-round blocks
gives the same summability proof with altered constants.
None of these constants is asserted uniform under physical mesh
refinement or across a changing active alphabet.

### Application of the C1 hypotheses to the original strict native chart

The required killed contraction is an actual native consequence here.
The [complete record owner, §§1 and 3](../../A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md)
gives \(N_{\rm blank}=A_{\rm native}=A_{\rm native}^\dagger\) and
\(\sum_jN_jN_j^\dagger=I\), together with the complete port1 effect.
The [original preparation proof, §1](../d0_native_preparation_closure_2026-10-21/PROOF.md)
fixes its units: on the Fourier block use
\(\Delta=A_{\rm native}^2\), with \(\epsilon=4p^2\) and
\(p=\varphi^{-1}\). These are the original normalized block units,
not a replacement of the unscaled physical \(\Delta_h\).
The actual identities are

\[
0<\Delta\le I,\qquad
E_1=A_1^*(I)=4p^3\Delta,\qquad
E_0=A_0^*(I)=I-4p^3\Delta.
\tag{41}
\]

The upper bound on \(\Delta\) follows by selecting the positive blank
summand in \(\sum_jN_jN_j^\dagger=I\); strict positivity is the
regular inverse-square-preparation chart. Since
\(1-4p^3=p^6>0\), these effects satisfy
\(E_0\ge p^6I\) and
\(E_1\ge4p^3\delta_{\min}I\), where
\(\delta_{\min}=\lambda_{\min}(\Delta)>0\).
For this packet's declared binary port-return diagnostic, \(T_0=A_1\) and
\(T_1=A_0\). Thus, writing
\(\delta_{\max}=\lambda_{\max}(\Delta)\le1\),

\[
\boxed{T_a^*(I)\le\kappa I,\qquad
\kappa=\max\{4p^3\delta_{\max},
                   1-4p^3\delta_{\min}\}<1.}
\tag{42}
\]

On a sufficiently small neighborhood of the regular strict Julia chart,
\(\delta_{\min}\) has a positive lower bound. The actual Julia square
roots and normalized inverse-square preparation are smooth there.
On its fixed active Fourier/boost alphabet the positive \(q_z\) also
have local lower bounds. Therefore the local C1 conclusion above applies
to the original unmodified full128 instrument and its generated
preparation, rather than remaining an unspecified contraction assumption.

For the literal full-label rule, the relevant killed maps are instead
\(T_z=\Phi-\mathcal I_z\) for all 64 active fine labels. The port-effect
bound (42) is not a bound for these maps. Their transience is already
proved in the [stationary occupation owner, §3](../d0_first_match_wald_2026-10-22/SEQUENTIAL_STATIONARY_OCCUPATION.md):
a unique faithful stationary density and \(q_z>0\) exclude an invariant
surviving state for any such killed map. The original preparation proof's
strict recycling bound supplies that uniqueness on this native chart.
Finite dimension, the finite active alphabet and continuity then give a
common locally contracting power, as proved in the preceding C1 argument.
Thus the same local C1 conclusion applies to literal full-label return,
using its own killed maps and chart-dependent constants.

Neither finite-chart application provides an all42 field-writer transport,
a bound through a dark mode or a mesh-uniform source.

This argument does not prove C2 entropy at a rank birth. A
\(t^2\log t^2\) contribution is C1 but can have a singular second
derivative. Any Hessian application keeps its separate smooth-support
or second-jet hypotheses.

## 8. Fixed spectator, actual purification, and physical boundary

For an independent fixed oldRIGHT density \(\tau\), the full blocks are
\(X_\gamma\otimes\tau\), the stationary return is
\(\rho\otimes\tau\), and the reference is
\(\bigoplus_\gamma Q_\gamma(\rho\otimes\tau)\).
Entropy adds \(S(\tau)\) to both the initial and final CQ states, while
\(\mathfrak D\), every Holevo quantity and the gain are unchanged.
Restrict to the fixed support if \(\tau\) is not faithful. A normalized
entropy or its source is never multiplied by the oldRIGHT dimension.

An actually retained pure DATA/reference preparation is a different
carrier. For a fully resolved efficient leaf instrument its conditional
joint states are pure, so
\(S(\Gamma_{DR})=I_{{\rm gain},DR}=H(P)\).
Stationarity of the DATA marginal does not assert
\(\omega_{DR,T}=\omega_{DR,0}\). In particular the pure initial joint
state is generally not a faithful reference containing all terminal
supports; \(D(\Gamma_{DR}\Vert\bigoplus_\gamma Q_\gamma\omega_{DR,0})\)
can be infinite. The mixed-DATA formula (10) cannot be relabeled as this
joint price. On that genuinely pure retained carrier the gain convention
has the pointer price, with correction \(\mathcal M/\ell\).

Finally, a finite paid preparation is part of the actual history tree.
Replacing it by \(\rho_*\) removes its record and price unless that
replacement is independently justified. The present stationary section
and its explicit off-section/cap defects provide a constructive input to
the complete native source and Poisson reduction. Selection of that
preparation, retained algebra, whole Book03 heat/feedback, clock,
controller, admitted all42 field map and uniform refinement remains
separate. **GR_closed=false.**
