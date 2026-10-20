# The original closed return as a coherent record partition: paid moments and the exact pressure sign

20 October 2026. Existing PR #334 / `native-programme-v1`; bounded continuation
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. Input native `f569c786`.

**Exact parent substitution.** The original full128 return determinant has an
explicit, positive, basis-independent coherent-record realization, including
its actual port-clock moment insertions. Its thermal companion is the norm of
the complementary blank amplitude of the same retained execution. This gives
an exact H/J partition and price-response identification, rather than a new
supplied price effect. It also determines the variational sign: these H/J
terms are positive log-partition pressures, while minimization of the matching
Born-amplitude code free-price produces their negative, with the required
factor two. No physical Info law or physical permission to prepare the new
symmetric trace boundary is inferred.

The construction uses every original data/CAR mode and oldRIGHT component.
The symmetric multi-run carrier and its trace purification are **additional
mathematical inputs**, not an actual single prepared full128 run. It preserves
ordered records inside each run and all ordered output slots. The parent
owns the finite occupation-cap and source-error application separately.

## 1. Exact original inputs and distinction from the owned results

Use the literal full128 history isometry and cost-return identities from
`d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md`
and `d0_same_history_price_composition_2026-10-20/paid_port_history.md`.
On the data space H with all sites and CAR16, and the unchanged oldRIGHT R of
dimension r_R=128, set `mathcal H=H tensor R`. At the actual fixed n rounds,

\[
 V_n=\sum_\omega(K_\omega\otimes I_R)\otimes|\omega\rangle,
 \qquad V_n^*V_n=I_{\mathcal H}.
\tag{1}
\]

The unique all-blank record is `port0,label0` at every round. Let P_0 select
that record and Q_0=I-P_0. With the actual self-adjoint native D, write

\[
 B=I-\alpha\Delta>0,\quad\Delta=D^2,\quad m=2n,
 \quad K=B^m,\quad\beta=m\alpha,
\]
\[
 A_0=P_0V_n=(B^n\otimes I_R)\otimes|0^n\rangle,
 \qquad A=Q_0V_n,
\]
\[
 A_0^*A_0+A^*A=I,\qquad
 F=A^*A=(I-K)\otimes I_R.
\tag{2}
\]

The actual known chronological port price on a retained record is
`C(omega)=n+N_1(omega)`, so n<=C<=2n. This is not the complete apparatus,
label, preparation, controller or information price. A physical second
inverse is not charged merely because the Gram formula contains an adjoint.
For the analytical mark t>=0 define, on the same Q_0 output space,

\[
 A_t=e^{-tC/2}A,\quad F_t=A_t^*A_t=A^*e^{-tC}A,
 \quad C_j(t)=A^*C^j e^{-tC}A.
\tag{3}
\]

Thus `partial_t^j F_t=(-1)^j C_j(t)`. All original records remain in the
parent isometry. Q_0 is this particular return readout, not free physical
postselection or record erasure. The already proved native identity is

\[
 F_t=\big[(\Phi_t^*)^n(I)-e^{-tn}B^{2n}\big]\otimes I_R,
\]
\[
 \Phi_t(X)=x\{X+\epsilon[(p^2+px)\mathcal T(DXD)
                         -\{\Delta,X\}/2]\},
\quad x=e^{-t},\quad\epsilon=2\alpha,
\quad\mathcal T(X)=\sum_kN_k^*XN_k.
\tag{4}
\]

Equation (4), its full noncommuting first source and the exact original
Kraus rows are consumed, not recomputed as a new physical law. Likewise,
the prospective finite-future scalar Gibbs/Doob law and the H+J+R auxiliary
maximum are already owned. The new bridge below identifies a **coherent
record realization of this specific F_t determinant** and its price moments.

## 2. A basis-independent coherent realization, with phase and clock retained

For an integer j>=0 let P_sym,j be the orthogonal symmetric projector on
`mathcal H^{tensor j}`. For j=0 it is the scalar identity. Define

\[
 W_j(t)=A_t^{\otimes j}P_{\rm sym,j},\qquad
 \Omega_j(z,t)=z^{j/2}\operatorname{vec}W_j(t),
\quad 0<z<1.
\tag{5}
\]

Vectorization uses the conjugate input space as an explicit trace-purifying
reference. It is invariant under simultaneous changes of input basis and
conjugate-reference basis. The output is still the **ordered tensor product**
of j complete original data/oldRIGHT/tape outputs. P_sym,j specifies an
extra coherent input boundary; it does not quotient those output records.
Neither a physical symmetrizer nor its work/preparation price is supplied
by writing (5).

Let d=dim(mathcal H). Since P_sym,j commutes with F_t^{tensor j},

\[
 \|\Omega_j\|^2
  =z^j\operatorname{Tr}(P_{\rm sym,j}F_t^{\otimes j})
  =z^j h_j(F_t),
\tag{6}
\]

where h_j is the complete homogeneous symmetric polynomial of the
nonnegative eigenvalues of F_t. The last equality is a proof tool, not a
physical eigenbasis preparation: each occupation tuple contributes once
to the trace on the symmetric input space.

**Theorem 1 (same-return coherent partition).** The orthogonal direct sum
of (5) has

\[
 \boxed{\quad
 Z_J(z,t):=\Big\|\bigoplus_{j\ge0}\Omega_j(z,t)\Big\|^2
   =\sum_{j\ge0}z^j h_j(F_t)
   =\det_{\mathcal H}(I-zF_t)^{-1}.
 \quad}
\tag{7}
\]

Proof: diagonalize F_t only to evaluate its trace. The symmetric basis
is indexed by occupations n_1,...,n_d>=0. Summing the absolutely convergent
nonnegative geometric products gives `product_i(1-z lambda_i)^{-1}`.
Because F_t<=F<=I and z<1, convergence is immediate. Every finite occupation
cut is a finite vector construction; the infinite sum is the exact analytic
generating object already present in Book03's determinant. It is not
permission for an infinite physical run or a free infinite carrier.

No scalar replacement of the original memory amplitudes occurs. In
particular, the j=1 vector is `sqrt(z) vec(A_t)` and recovers **all** entries
of A_t. Thus the full vector construction is injective in that original
return amplitude for fixed z>0. Its norm, as expected, only sees A_t^*A_t;
the retained vector contains additional phase information which that
particular scalar price does not read. Interference inside each native
K_omega and every original ordered tape entry are preserved.

To see the actual positive output-history measure without selecting an
eigenbasis, write A as its complete nonblank tape blocks A_omega and
E_omega=A_omega^*A_omega. For an ordered tuple of j tapes, its unnormalized
Born mass after tracing the retained data/reference, but not deleting them,
is

\[
 b_{j,\boldsymbol\omega}(z,t)
  =z^j e^{-t\sum_a C(\omega_a)}
    \operatorname{Tr}\!\left[
      P_{\rm sym,j}\bigotimes_{a=1}^j E_{\omega_a}\right]\ge0.
\tag{8}
\]

Positivity follows from `Tr(P T)>=0` for positive P,T. Summing all ordered
tuples gives (6). This is not the false claim that each individually
ordered term in `Tr(F^j)` is a nonnegative classical loop probability.
The symmetric trace in (8) is essential. Its induced correlations need
not equal independent original prepared runs. The complete pure state
in (5) remains the memory carrier; (8) is one explicitly declared pointer
readout of it.

The added operational obligations are therefore concrete: the symmetric
input boundary, its trace-purifying reference, the distribution or cut of
j, and all their actual work and clock costs. Merely having the one-run
V_n does not prove these obligations. The original determinant identity
itself does not need physical occupation of all data modes.

### 2.1. A normalized complete apparatus with every failed return retained

The raw trace boundary has a concrete normalization; it must not be hidden.
Let `d_j=rank P_sym,j=binomial(d+j-1,j)` and prepare the mathematical input

\[
 |\Xi_z\rangle=Z_{\rm in}^{-1/2}
   \bigoplus_{j\ge0}z^{j/2}\operatorname{vec}P_{\rm sym,j},
 \qquad Z_{\rm in}=\sum_jd_jz^j=(1-z)^{-d}.
\tag{7a}
\]

Apply the **complete** isometry `directsum_j V_n^{tensor j}` on its active
input, retaining all ordered output tapes and the trace-purifying reference.
Its total norm is one. The projection asking that every one of its j output
tapes be in Q_0 gives (5), divided by sqrt(Z_in). The empty sector j=0
satisfies this event. Consequently

\[
 \boxed{\Pr_{\Xi_z}(\hbox{all returns})=Z_J/Z_{\rm in},
 \qquad J=\log\Pr_{\Xi_z}(\hbox{all returns})
                  +\log Z_{\rm in}.}
\tag{7b}
\]

Thus (7) has a normalized complete-instrument interpretation, not merely
an unnormalized vector. Every complementary outer failure remains in the
complete output. Preparing (7a), physically obtaining any chosen event,
and comparing different j still require their real resources. In
particular, the probability in (7b) need not be near one. At a finite j-cut
the same construction is exactly finite, with `Z_in` and `Z_J` both replaced
by their actual finite sums; the parent supplies the controlled cut limit.
This input is not the original single-run prepared Riesz state.

## 3. True known-cost moments of this exact record ensemble

On sector j the known price is the sum of the j actual retained port
prices. Dividing (8) by (7) gives an honest positive law. Define
`R_t=(I-zF_t)^{-1}`. Differentiating its finite/countably summable
cost transform, or directly differentiating (7), proves

\[
 \boxed{\mathbb E_{z,t}C_{\rm tot}
   =-\partial_t\log Z_J
   =z\operatorname{Tr}(R_t C_1(t)).}
\tag{9}
\]

The trace is over mathcal H, so the original oldRIGHT multiplicity128
is included exactly once. If F_t and C_j are written on data H instead,
the same formulas carry the prefactor128. No probability floor, pinching
or commuting assumption between F_t and C_j is needed.

The exact variance and occupation moments are

\[
 \boxed{\operatorname{Var}_{z,t}C_{\rm tot}
   =z\operatorname{Tr}(R_t C_2(t))
    +z^2\operatorname{Tr}(R_t C_1(t)R_t C_1(t)),}
\tag{10}
\]
\[
 \mathbb E j=z\operatorname{Tr}(R_t F_t),\qquad
 \operatorname{Var}j=z\operatorname{Tr}(R_t^2 F_t),\qquad
 \operatorname{Cov}(C_{\rm tot},j)=z\operatorname{Tr}(R_t^2 C_1(t)).
\tag{11}
\]

Both terms in (10) are nonnegative: the second is the trace of the square
of the Hermitian `R_t^{1/2}C_1 R_t^{1/2}`. The chronological bounds are

\[
 n\,\mathbb E j\le\mathbb E C_{\rm tot}\le2n\,\mathbb E j.
\tag{12}
\]

For several commuting tape marks C_a, the mixed covariance replaces C_2
by `A^* C_a C_b e^{-sum t_c C_c}A` and the second quadratic term by
`z^2 Tr(R C_a(t) R C_b(t))`. Thus the original clock, port counts and
other actually supplied diagonal record prices can be carried jointly;
this does not invent the missing physical Info.

For a genuinely moving field on the same trivialized Hilbert fibre,
fixed integer n, and fixed z,

\[
 d\mathbb E C_{\rm tot}
 =z\operatorname{Tr}(R_t\,dC_1(t))
 +z^2\operatorname{Tr}(R_t(dF_t)R_t C_1(t)).
\tag{13}
\]

Moving z adds `Tr(R_t^2 C_1(t)) dz`. All preparation/observer/adjoint
terms in A must move. If the actual price operator C also moves,

\[
 dF_t=(dA)^*e^{-tC}A+A^*e^{-tC}dA
 -\int_0^t A^*e^{-(t-s)C}(dC)e^{-sC}A\,ds.
\tag{14}
\]

For the original fixed 0/10 clock, dC=0. An integer change in n is a
different execution comparison, not a smooth derivative hidden in (13).

### A positive exact price-response reconstruction

Set J(t)=log Z_J(z,t). Since C>=nI on the return output,
`0<=F_t<=e^{-nt}F`, so J(t) tends to zero. Therefore

\[
 \boxed{J(0)=\int_0^\infty\mathbb E_{z,t}C_{\rm tot}\,dt.}
\tag{15}
\]

This reconstructs the unchanged Book feedback price from positive known
cost responses on the same coherent record family. For a finite smooth
chart with C>=cI>0, bounded actual jets and `z||F||` uniformly below1,
(14) is bounded by a constant times `(1+t)e^{-ct}`. The resolvent is
uniformly bounded. Differentiation under the integral is then justified,
and `dJ=integral d(E C_tot)dt`, including all terms in (13)-(14).

Equation (15) is not `J=E C` at one selected mark. It is invariant under
C->aC by changing the integration variable, although a physically paid
clock cost scales by a. It consequently cannot fix the absolute native
price unit or Info. The parameter t is an analytical source variable,
not a chosen physical temperature or a new law of motion.

### 3.1. The unconditional known price of the complete apparatus is different

In (9)-(15), the normalized law is conditioned on the all-return event of
(7b). Those expressions must not be called the entire paid cost of producing
that event. Let

\[
 C_{\rm op}=V_n^* C V_n
\]

include **all** original tape outcomes, including all blank/complementary
ones. It is the known port-price effect of one complete original run.
For j>=1, the normalized input density `P_sym,j/d_j` has every one-copy
marginal I/d: it is invariant under every common unitary U^{tensor j}, so
that marginal commutes with all U and has trace1. Hence the actual mean
sum of j complete known run prices is `j Tr(C_op)/d`, even though the
copies are initially correlated. From (7a), `E_in j=d z/(1-z)`, and
therefore

\[
 \boxed{\quad\mathbb E_{\rm complete} C_{\rm tot}
   =\frac{z}{1-z}\operatorname{Tr}_{\mathcal H}C_{\rm op}.
 \quad}
\tag{15a}
\]

The corresponding complete cost transform is, exactly,

\[
 Z_{\rm complete}(t)
  =\frac{\det[I-zV_n^*e^{-tC}V_n]^{-1}}{Z_{\rm in}},
 \qquad Z_{\rm complete}(0)=1.
\tag{15b}
\]

This follows by the same symmetric trace, now using the complete V_n.
There is no omitted outer failure. The already owned true port-cost identity
makes (15a) entirely explicit on the original instrument:

\[
 C_{\rm op}=
 \left[nI+p\epsilon\sum_{a=0}^{n-1}(\Phi^*)^a(\Delta)\right]
 \otimes I_R.
\tag{15c}
\]

At fixed z,d,n its full field derivative is simply
`z Tr(dC_op)/(1-z)`, including the actual native channel and observer jets.
This still counts only the known original port price, not preparation,
symmetrization, controller or the unknown full Info. For an actual finite occupation cap J_max, set
`Z_in,cap=sum_(j=0)^J_max d_j z^j` and
`mean_cap=z partial_z log Z_in,cap`. Then the exact complete known price is
`mean_cap Tr(C_op)/d`. No infinite-run approximation is needed for this
finite statement; the parent owns its cutoff error and source bounds.
If separately admitted independent fresh attempts are repeated until the
all-return event, the known expected payment is (15a) divided by its actual
success probability (7b); fresh-attempt preparation/reset prices remain
additional. No such repetition task is selected here.

### 3.2. Complete-output entropy does not supply an omitted field source

After tracing only the **added dual-input trace reference** from the
complete apparatus of (7a), its input density is
`directsum_j z^j P_sym,j/Z_in`. The complete isometry preserves its
nonzero spectrum on the output containing data, all tapes and oldRIGHT.
At fixed d,z and fixed occupation cut its entropy is exactly

\[
 S_{\rm complete}=\log Z_{\rm in,cap}
                          -(\log z)\operatorname{mean}_{\rm cap},
 \qquad d_y S_{\rm complete}=0.
\tag{15d}
\]

The convergent unbounded formula uses `Z_in=(1-z)^{-d}` and
`mean=d z/(1-z)`. The entire purification is pure before and after the
isometry as well. This is **not** a statement that the isolated pointer
record entropy is constant: that marginal can acquire field-dependent
entropy by transferring information into correlations. Nor does (15d)
define Book Info. It shows precisely which complete-output entropy cannot
cancel the genuine field derivative of (15a). Changes of d, z, cut or
initial preparation have their own entropy terms and are not frozen by
this fixed-task assertion.

## 4. The original thermal pressure and fixedRIGHT matter have an exact common-process identity

Use the unchanged H+J+R price owner:

\[
 S_{\rm native}=\operatorname{Tr}(\rho\Delta)
 +\frac1\beta\log(C_{\rm env}\operatorname{Tr}_H K)
 -128\operatorname{Tr}_H\log[I-z(I-K)].
\tag{16}
\]

`C_env` is the original fixed workspace/reference multiplicity from that
owner; it is not a new calibration. Let `Z_H=C_env Tr_H K`. The same
blank amplitude in (2) gives the exact norm identity

\[
 Z_H=\frac{C_{\rm env}}{128}\|\operatorname{vec}A_0\|^2.
\tag{17}
\]

The factor compensates precisely for the already present oldRIGHT trace.
This is a full counting-trace boundary, not the chosen physical Riesz
preparation and not a replacement by a low-mode expectation. On a normalized
trace-purifying input, its actual blank-event probability is
`Tr_H K/dim(H)`, so `H=log[C_env dim(H) Pr(blank)]/beta`. Both its
complement and its complete known price are retained by V_n. Its actual
blank tape always has port cost n, hence its marked norm is
`Z_H(t)=e^{-nt}Z_H`. This conditional component has known mean cost n
and variance0 even when its **field** pressure source is nonzero. The
field source reads the survival/preparation amplitude; it is not a
nonzero derivative of the fixed port-clock length.

Put

\[
 \Lambda=-\frac1\beta\log K=-\frac1\alpha\log B,
 \qquad \sigma_H=K/\operatorname{Tr}K.
\]

For every actual normalized data preparation rho, including a moving,
noncommuting one,

\[
 \boxed{\quad H+R=
 \frac{D(\rho\Vert\sigma_H)}\beta
 +\frac{S_{\rm vN}(\rho)+\log C_{\rm env}}\beta
 +\operatorname{Tr}[\rho(\Delta-\Lambda)].\quad}
\tag{18}
\]

Proof: `log sigma_H=-beta Lambda-log TrK`; expand the relative entropy.
No identification of any of these terms with Book Info is used.
For the **original** fullRIGHT128 preparation `rho=M M*`,
`M*M=I_128/128`, its nonzero spectrum is exactly 1/128, so
`S_vN(rho)=log128` for every admitted preparation variation. This is
true on the adequate full site/data carrier; no rank16 Fourier fixture
is substituted for it.

The finite-clock correction in (18) is compulsory. If `B>=b_*I>0`,
scalar integration followed by spectral calculus gives

\[
 \frac\alpha2\Delta^2\le\Lambda-\Delta
 \le\frac{\alpha}{2b_*}\Delta^2.
\tag{19}
\]

Indeed `-log(1-x)-x=integral_0^x u/(1-u)du`.
Replacing R by `Tr rho Lambda` would remove the last term, but it would
change the original price. A small mean-energy correction does not
license dropping its full field source, especially before the required
refinement normalization.

Equations (7), (17) and (18) give one exact interpretation of **all three
unchanged terms** in (16): blank-trace pressure, symmetric return-record
pressure, and the prepared Dirac quadratic contribution, or equivalently
the specified relative-entropy expression with its true finite-clock
remainder. A free thermal auxiliary state has not been identified with
physical rho; its fixedRIGHT constraint is retained.

## 5. The variational sign and the amplitude/Born factor are determined

The new representation does not permit a Gibbs minimum to be assigned
the positive Book pressure by changing names. At any finite occupation
cut, refine the pointer readout of (5) by a full orthonormal output and
trace-reference basis. Let the actual nonzero amplitudes be a_eta, their
Born weights `b_eta=|a_eta|^2`, and `Z=sum b_eta`. Set

\[
 s_\eta=-\log_\varphi|a_\eta|
        =-\frac{\log b_\eta}{2\log\varphi},
 \qquad q_\eta^*=b_\eta/Z.
\]

For every distribution q on that fixed support,

\[
 \boxed{\sum_\eta q_\eta s_\eta-
          \frac{H(q)}{2\log\varphi}
 =-\frac{\log Z}{2\log\varphi}
   +\frac{D(q\Vert q^*)}{2\log\varphi}.}
\tag{20}
\]

The actual completed Born law is the unique minimum of this **specified
statistical** functional. This is an application of the already owned
Gibbs algebra to the now explicit coherent native-record weights, not a
new generic Gibbs theorem. Phase information remains in the state (5);
(20) only optimizes this declared readout distribution with those phase
and task data held fixed.

At the convergent occupation limit the optimum is

\[
 -\frac{\log Z_J}{2\log\varphi}
 =-\frac{J}{2\log\varphi}.
\tag{21}
\]

Using probabilities rather than amplitudes as primitive weights removes
the factor2 but retains the **minus** sign. Equivalently J is the maximum
of entropy plus mean log Born weight. The already owned H+J auxiliary
maximum has exactly this sign. Neither formulation is a derivation that
the physical field minimizes +J, or +H+J+R. Changing the sign of an
isolated J preserves its stationary set but reverses its minimum/maximum;
in a sum with H and R it also changes the relative source equations.

The entropy in (20) is the counting entropy of a **specified readout**.
It has not been identified with the original vertex Info in Book03.
The amplitude source itself contains the actual gate and memory data.
Choosing an information table from the desired q* would reverse this
logic and would not derive the original physical continuation.

## 6. Literal original-carrier application and decisive boundary

On an original invariant full-CAR16 Fourier shell, let `A_native^2=aI`,
0<a<1, where `A_native=hD/16`. The actual one-round full128 instrument
has, on this same shell,

\[
 F=fI,\quad f=4p^2a-4p^4a^2,\quad
 r=\Pr(\text{port1})=4p^3a,
\]
\[
 F_t=x(f-r)I+x^2rI,\quad
 C_1(0)=(f+r)I,\quad C_2(0)=(f+3r)I.
\tag{22}
\]

Both `(f-r)` and r are the actual complete exit-port masses; the
blank-label port1 remains included. On the full shell times oldRIGHT,
d=16*128=2048. Thus the exact new symmetric record law is

\[
 Z_J=(1-zf_t)^{-2048},\quad
 \mathbb E C_{\rm tot}=\frac{2048z(f+r)}{1-zf},
\]
\[
 \operatorname{Var}C_{\rm tot}
 =\frac{2048z(f+3r)}{1-zf}
   +\frac{2048z^2(f+r)^2}{(1-zf)^2}.
\tag{23}
\]

The complete unconditioned apparatus instead pays the known mean
`2048 z(1+r)/(1-z)`, and its all-return probability is
`[(1-z)/(1-zf)]^2048`. These use the actual original full128 return,
not an invented two-state model. If a changes through its actual
coframe-scale map with the other
parameters fixed, `df/da=4p^2(1-2p^2a)>0`. Consequently the Book J source
is strictly positive, while the minimized statistical amplitude free-price
in (21) has strictly negative source. This is an exact same-carrier test
that the two proposed variational readings are not interchangeable.
It is not a claim that this one-round shell solves the GR task or that
its 2048-dimensional trace boundary is a physical fixedRIGHT128 pure
preparation. The generic statement (7) applies without a shell restriction.

The interpretation achieved here is constructive: it removes the lack of
an explicit coherent, positive, true-clock partition underlying the
original feedback determinant, and gives its exact cost/source moments.
It identifies H and R without a freely supplied G, including the original
fixedRIGHT entropy and the unavoidable finite-clock correction.

The remaining constitutive premise is now specific. The theory must
identify the actual permitted boundary/occupation task and full absolute
Book Info/work valuation that chooses (16), or an explicitly proved
equivalent source law. Neither local branch counting nor an optimized
archive code supplies those physical operations or their price. The prior
full128 port-regret owner already tests that shortcut and is consumed,
not restated as a new result. The primary all40 geometric reporter remains
available once the **complete** same-execution source and its actual
matter ratio are supplied. This packet does not assert GR closure or
prospective physical minimum attainment.
