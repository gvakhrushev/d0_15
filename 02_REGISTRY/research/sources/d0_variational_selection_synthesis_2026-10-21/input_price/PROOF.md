# Exact finite all-input price separation on the original full128 Fourier block

Supporting application inside existing PR #334. Input snapshot 441bdef5;
no new task, price, physical information cut, or geometric closure claim.

## 1. Why this changes the input strategy

The newly owned retained-input theorem solves the complete coherent-entropy
input Euler equation, including fixed-RIGHT and free-density domains. Its
field envelope still has the actual term `n d cbar`. A stronger finite
application now shows that on one original native scalar field chart **no
input choice at all** can reverse an exact same-horizon price comparison.
This does not need a numerical Gibbs solve or a stationarity approximation.

## 2. Original chart and exact charge

Use the literal original `native(theta,nu)` definitions, with theta=0 and
the original Fourier phases `(i,i,-1,-i)`. All sixteen CAR grades and all
128 outcomes stay present; the reference may be oldRIGHT128. Let
`p=phi^-1`. The original blank SELECT block is

    A=(nu/16) sum_r [c_r (zeta_r-1)+c_r^* (conj(zeta_r)-1)].

CAR gives `A^2=(10 nu^2/256) I=(5 nu^2/128) I`. Both values nu=1/2 and
nu=3/5 are on the strict original Julia chart. They are actual homogeneous
native creation-column scales; no abstract independent variation of D with
its recycling operator frozen is used. The Julia recycling changes as it
should when nu changes.

The already owned complete port effect is `E1=4p^3 A^2`. Consequently for
every normalized DATA input, every integer horizon n, and every retained
purification,

    C_port,n(nu)=n[1+5p^3 nu^2/32].                    (1)

The proof uses completeness and the scalar effect, so does not enumerate
128^n histories. The checker independently evaluates all128 one-round
Kraus operators and a four-round charge recursion.

## 3. Whole coherent record bound and finite separation

Let E denote all fresh coherent outcomes. The full DATA-RIGHT-E state is
pure. The initial Schmidt rank across DATA16/RIGHT128 is at most16, so the
support of the final DATA-RIGHT state has dimension at most16*16=256.
Equality of Schmidt spectra gives `0<=S_phi(E)<=log_phi256`, independent
of n. No record is erased or measured to obtain this spectral bound.

For the previously declared valuation `F_n^E=C_port,n-S_phi(E)`, equations
(1) and the entropy bound give, for **any** two normalized purifications,

    F_n^E(3/5,C2)-F_n^E(1/2,C1)
        >= n * 11 p^3/640 - log_phi256.                (2)

This includes any common fixed RIGHT Gram, and also arbitrary separate
input minima. At n=4096 the right side is strictly greater than52/25:
`p^3=sqrt5-2>1/5`, while `phi^12=144phi+89>256` implies
`log_phi256<12`. The sharp displayed numerical lower bound is approximately
5.095824892684746; the certified coarse lower bound is52/25. Thus even a
complete input Euler solution cannot make nu=3/5 preferable to every
nu=1/2 input in this specified component price.

The reference-adjoined entropy S(ER)=S(DATA) has the smaller cap log_phi16;
the same conclusion follows with a stronger bound. This does not choose
either information algebra as physical Book03 Info.

**Scope:** the theorem compares two homogeneous original Fourier blocks at
the same integer horizon. It does not furnish a collar-preserving variation
of the spatial all42 Brinkmann family, an admissible common-initial writer,
or a statement about compulsory complete Book03 price. Actual additional
writer/heat/work/label charges and their sources remain untouched. If such
a charge is supplied its genuine difference must be added to (2).

## 4. General long-horizon application of the solved input theorem

On a compact, fixed-dimensional, mixing regular chart, the owned exact
Poisson formula reads

    A_n=n cbar I+Y-(Phi*)^n Y.

Since `(Phi*)^n` is unital positive, `||Y-(Phi*)^nY||<=2||Y||`. The complete
coherent entropy is at most log_phi(d*r), with r the actual Schmidt rank.
Therefore uniformly over all admissible pure input preparations

    |F_n^E/n-cbar| <= [2||Y||+log_phi(d*r)]/n.          (3)

Optimizing inputs over any nonempty fixed admissible class does not change
this limiting rate. For an actual uniform native creation-column scale
D(s)=sD0, the stationary state Delta^-1/TrDelta^-1 is scale independent
and `cbar(s)=1+s^2 kappa0`. Under the owned uniform C1 mixing/source
hypotheses on a positive s interval and smooth interior input-minimum
branch, the envelope derivative is

    d_s F_n^E = 2n s kappa0 + O(1) > 0

for every sufficiently large n. The recycling and paid Poisson boundary
may vary with s; they belong to the bounded O(1) source. No uniform spatial
refinement gap or earliest finite derivative threshold is inferred.

Equation (2), unlike this local source corollary, needs no mixing estimate,
input regularity, minimum differentiability, or large-n asymptotic.

## 5. The measured archive gives a distinct constructive rate target

For the same instrument define q_n as the law of the **measured complete
pointer**. Starting from stationary DATA makes this a stationary process.
The conditional entropies H(X_n|X_1,...,X_(n-1)) decrease to an entropy rate
h_ptr, and `H(q_n)/n -> h_ptr`. This is a statement about a different
information algebra, not permission to measure or reprice the old record.

Input independence of this rate follows directly from native mixing. If
`delta_k=||Phi^k(rho)-rho_*||_1/2<=C q^k`, discard the first k symbols only
for the entropy calculation. Their conditional entropy is between0 and
k log_phi128. The tails differ in total variation by at most delta_k, so

    |H_n(rho)-H_n(rho_*)|
      <= k log_phi128 + delta_k(n-k)log_phi128+h_phi(delta_k).

Taking k proportional to log n proves O(log n) uniformly over input
densities. Hence the declared measured-pointer price rate, even after
input optimization, is `cbar-h_ptr`. A stationarity claim about its
derivative additionally requires C1 convergence of the entropy rate; it
does not follow from convergence of values.

There is a precise existing full128 split, with no history enumeration.
For every nonblank label the two retained port probabilities are `(p^2,p)`
and the normalized DATA state is the same at both ports. Erasing those
ancillary bits only for the mathematical chain rule gives exactly

    H_full,n = H_red,n +(2-p) E N_nonblank-label.       (4)

On the scalar chart of section2 put `lambda=5nu^2/128`. The actual two
blank-label Kraus operators give

    E_nonblank-label=4p^2 lambda(1-lambda) I,
    h_ptr=h_red+(2-p)4p^2 lambda(1-lambda).             (5)

Consequently, **if** the physical price actually is this measured valuation
with no additional source and its C1 rate limit is established, its
necessary scalar rate-stationarity condition is the single exact equation

    d_nu h_red = (5p^2 nu/16)
                 [p-(2-p)(1-5nu^2/64)].               (6)

No value of h_red or its derivative has been assigned. Physical additional
code/work terms alter (6) by their actual rate derivatives. This is a
concrete surviving information-source target on the existing instrument,
not a proposed replacement action or a proof of an Einstein source.

The difference between measured and coherent entropies is exactly the
relative entropy of coherence of the complete tape:
`H(q_n)-S(rho_E,n)=D(rho_E,n||dephase rho_E,n)/ln(phi)`. Thus an extensive
pointer source cannot be imported into the coherent-input calculation by
renaming the information. Any genuinely selected measurement and its price
must be part of that same physical execution.

## 6. Validation and provenance

Run `PYTHONPATH=/tmp/d0_synthesis_python python3 check_input_obstruction.py
/absolute/path/to/d0_15`. The source bytes are pinned in the script/output.
It checks exact Gaussian-integer CAR, exact Golden inequalities, the
original all128 scalar port and label effects, the complete port ancillary
law, and a bounded paid-cost recurrence. It does not re-solve preparation
minima, enumerate long histories, run Lean or certify lattice/refinement.
All128 numerical residuals are diagnostics; the finite bound (2) is analytic
and its coarse positive lower bound is exact. `GR_closed=false`.
