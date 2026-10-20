# Golden recorded refinement and the full Hodge Gibbs state

Parent: existing #310, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input SOURCE: `eb9594d2d06572164c26bd561e60e9faf4f830af`.
Date: 10 October 2026.

The preceding [modular reconstruction](A4D_NATIVE_MODULAR_PREPARATION_BOUNDARY.md)
reduces one proposed preparation route to an actual state/heat identification.
Here that identification is tested against **two existing objects**: the
recorded golden cylinder state and the complete flat counting Hodge heat.
The test allows every positive temperature at every level, every overall
positive heat scale, every unitary identification and any independent
ancillary state. It retains every Hodge site, all sixteen form components
and all thermal zero modes.

**Result.** If the readout state retains an unbounded number of independent
recorded golden factors, its trace distance from this full Hodge Gibbs
state tends to one, uniformly over those choices. It cannot even approach
that state. This is a quantitative obstruction to the named state/heat
identification, not a finite exact-sampling objection. It does not exclude
correlated preparations whose readout spectrum changes, other owned heat
operators, or native paired-price transfer without this Gibbs-state premise.
The common preparation T0, own source and GR remain open.

## 1. The actual inputs and what is being compared

Let p=phi^-1, so p+p^2=1, 3/5<p<2/3, and let g=log(phi)>0.
`DetectorSupportGoldenWeight.cylWeight` assigns p to its true/direct
letter and p^2 to its false/return letter. Its `weightExp` costs these
letters 1 and 2, and `cylWeight_eq_pow` and `cylWeight_refine` prove the
literal powers and refinement consistency. In the operational bit order
0,1 these two weights are the actual marginal

\[
 r=\operatorname{diag}(p,p^2),\qquad
 U|00\rangle=a|00\rangle+p|11\rangle,\quad a^2=p,       \tag{1}
\]

of `GoldenCoherentMemory.fullStep`. Tensoring m copies of that same
declared blank-record experiment gives the full joint pure state and its
word-factor readout r^tensor m. The records are retained in the joint
state; this partial trace is the named readout, not permission to delete
records from the price. Physical admission of arbitrary preparation
resources by M1 is not proved by this tensor identity.

The entire compared state class is

\[
 \rho_m=V_m\bigl(\tau_m\otimes r^{\otimes m}\bigr)V_m^*,       \tag{2}
\]

where tau_m is any density on any finite ancillary carrier and V_m is
any unitary identification with the Hodge carrier. The ancilla need not
be faithful, fixed, or of bounded dimension. Its independence from the
m golden factors before V_m is the essential stated restriction. A more
general joint preparation followed by a different partial trace need
not satisfy (2) and is not excluded.

The second input is the actual counting `hodgeCarDirac` square on
`ArchiveCochain N`, L=N+2. Its full Fourier spectrum, already derived in
[the positive Hodge price proof](A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md#4-quantitative-flat-contrast-of-the-literal-bootstrap), is

\[
 \lambda_k=4L^2\sum_{j=1}^4\sin^2(\pi k_j/L),\qquad
 k\in(\mathbb Z/L)^4,\quad L\ge2,                        \tag{3}
\]

each repeated sixteen times. This follows from the actual difference
square and its periodic characters, not the informational pullback kernel.
In particular the constant cochains supply all sixteen zero modes.
For **any** beta>0 put

\[
 \sigma_{L,\beta}=Z_L(\beta)^{-1}e^{-\beta\Delta_L},\qquad
 Z_L(\beta)=16\sum_k e^{-\beta\lambda_k}.                  \tag{4}
\]

Every positive scalar multiplication of Delta is absorbed in beta. An
additive scalar cancels from (4); neither is chosen as a physical law.
The state spaces must have the same dimension:
`dim(tau_m)*2^m=16 L^4`. This class is nonempty at arbitrarily fine
levels. For example L=2^ell, m=4ell and tau=I_16/16 retain the whole
Fock factor. Taking ell>=2 also respects L in 4N. Thus the result is
not a mismatch of dimensions or a discarded-zero-mode argument.

## 2. Golden spectral mass cannot stay in a fixed log-probability window

The eigenvalue attached to a length-m word with k return letters is

\[
                     p^{m+k}.                            \tag{5}
\]

There are binomial(m,k) such words. Under the density's own eigenvalue
mass, K therefore has distribution Binomial(m,q) with q=p^2 and 1-q=p.
Its logarithmic eigenvalue spacing is exactly g. For every real interval
J of length W>=0, define the spectral mass in that window by

\[
 M_\rho(J)=\operatorname{Tr}\bigl(\rho\,
             1_{\{-\log\rho\in J\}}\bigr).              \tag{6}
\]

Zero eigenvalues contribute no mass. For all m>=1 and every state (2),

\[
 \sup_{|J|=W}M_{\rho_m}(J)
 \le {2\over\sqrt m}\left(\left\lfloor{W\over g}\right\rfloor+1\right)
 \le {2\over\sqrt m}\left({W\over g}+1\right).           \tag{7}
\]

Here is an all-m proof, separate from the finite controls. Fourier inversion
of the finite binomial polynomial bounds every atom by

\[
 \begin{split}
 \mathbb P(K=k)
 &\le {1\over2\pi}\int_{-\pi}^{\pi}|1-q+qe^{it}|^m\,dt\\
 &\le {1\over2\pi}\int_{-\pi}^{\pi}
       \exp(-2mq(1-q)t^2/\pi^2)\,dt\\
 &\le {\sqrt\pi\over2\sqrt{2mq(1-q)}} < {2\over\sqrt m}.
 \end{split}                                             \tag{8}
\]

Indeed the squared modulus is `1-4q(1-q) sin^2(t/2)`;
`sin(|t|/2)>=|t|/pi` on this interval, and `1-u<=exp(-u)`.
The last bound extends the Gaussian integral to the real line and uses
q(1-q)=p^3>1/5 and pi<4. A log window contains at most
`floor(W/g)+1` consecutive binomial values, proving (7) for the product.
Each nonzero eigenvalue t_a of tau shifts the window by -log(t_a) and
weights its mass by t_a. Summing over a preserves (7), irrespective of
ancilla size or degeneracies. A unitary does not change spectral mass.

## 3. The full Hodge thermal energy has a uniform second moment

The needed bound is uniform over **both** L and beta; no temperature
scaling is assumed. For j(k)=min(k,L-k), the actual one-axis eigenvalue
mu_k=4L^2 sin^2(pi k/L) satisfies

\[
                   16j(k)^2\le\mu_k\le64j(k)^2.           \tag{9}
\]

The lower inequality is sine concavity and the upper uses sin x<=x and
pi<4. Write S_L(t)=sum_k exp(-t j(k)^2). Group j by floor(j/3).
There are at most six k in each group, the target integer is an available
cycle distance, and `8j^2>=64 floor(j/3)^2`. Consequently, for every t>0,

\[
 S_L(8t)\le6S_L(64t),\qquad
 {Z_L(t/2)\over Z_L(t)}\le6^4.                            \tag{10}
\]

For the second inequality, each one-axis heat at t/2 is bounded above
by S_L(8t), its heat at t is bounded below by S_L(64t), and the four-axis
partition factorizes. The same sixteenfold multiplicity occurs on both
sides; no form degree is selected.

For x>=0 the elementary Taylor bound exp(x/2)>=x^2/8 gives
`x^2 exp(-x)<=8 exp(-x/2)`. Apply it to every beta lambda_k and use (10):

\[
 \operatorname{Tr}\bigl(\sigma_{L,\beta}(\beta\Delta_L)^2\bigr)
 \le8\,{Z_L(\beta/2)\over Z_L(\beta)}
 \le C,\qquad C=8\cdot6^4=10368.                          \tag{11}
\]

These constants are deliberately loose and are not estimated from a mesh
or temperature scan. In particular the spectral projection P onto
`beta Delta_L<=R` obeys

\[
 \operatorname{Tr}(\sigma P)\ge1-C/R^2,\quad
 \operatorname{rank}P\le Ze^R,\quad \|\sigma\|_{op}\le Z^{-1}. \tag{12}
\]

Thus almost all thermal mass lies in a logarithmic eigenvalue window
`[log Z,log Z+R]` of bounded width for any fixed error, at every L,beta.

## 4. A basis-independent separating measurement

This step also covers noncommuting rho and sigma. Fix R,A>0. Let Q_high
be the spectral projection of rho onto eigenvalues greater than e^A/Z.
Since Tr rho=1,

\[
                    \operatorname{rank}Q_{high}\le Ze^{-A}.
\]

Let E project onto `ran(P) intersect ker(Q_high)`. The codimension of
this intersection in ran(P) is at most rank Q_high. Since P-E is a
projection and sigma is bounded by I/Z, (12) gives

\[
             \operatorname{Tr}(\sigma E)\ge1-C/R^2-e^{-A}. \tag{13}
\]

Split rho into its high, middle and low spectral parts, with middle
eigenvalues between e^{-(R+A)}/Z and e^A/Z inclusive. The high part
vanishes on E. The middle part has mass bounded by (7) with width R+2A.
The low part is at most e^{-(R+A)}I/Z, and rank E<=rank P<=Ze^R.
Hence

\[
 \operatorname{Tr}(\rho E)
 \le {2\over\sqrt m}\left({R+2A\over g}+1\right)+e^{-A}.   \tag{14}
\]

For density matrices the trace distance D=(1/2)||rho-sigma||_1 bounds
the difference of the two probabilities of every projection. This follows
directly by splitting the trace-zero self-adjoint rho-sigma into its
positive and negative spectral parts. Combining (13)--(14) proves

\[
 \boxed{D(\rho_m,\sigma_{L,\beta})\ge
 1-{10368\over R^2}-2e^{-A}
 -{2\over\sqrt m}\left({R+2A\over\log\phi}+1\right).}     \tag{15}
\]

No commutation assumption, spectral matching algorithm or selected basis
occurs in this proof. E is a mathematical distinguishing projection; the
theorem does not assert its physical admission as a native detector.

Set R=A=m^(1/6). Uniformly in L,beta,tau,V subject to the dimension match,

\[
 D\ge1-\left(10368+{6\over\log\phi}\right)m^{-1/3}
          -2m^{-1/2}-2e^{-m^{1/6}}\longrightarrow1.       \tag{16}
\]

Trace distance is at most one, so the limit is exactly one. The conclusion
is valid for any compatible sequence with m tending to infinity, including
the explicit cofinal levels in Section 1. Neither temperature tuning nor
a scalar heat calibration can make this trace-norm state identification
convergent, much less O(h). This does not assert that the physical action
contrast requires trace-norm state convergence.

## 5. What the obstruction does and does not close

The independent golden-record state cannot be identified, even
asymptotically in full trace norm, with the complete flat Hodge Gibbs
state through a unitary change of coordinates and a temperature choice.
This closes that explicit proposed preparation arrow on its full stated
class. It retains arbitrary independent ancillary data, all Hodge modes,
level-dependent beta and normalization shifts. The finite fact that one
product has a simple maximal eigenvalue while Hodge has sixteen zero
modes is not the proof: a mixed sixteen-state ancilla already removes
that multiplicity objection, and (15) still applies.

To pursue this Hodge/modular route, an actual preparation must therefore
produce a different readout spectrum through genuinely correlated
preparation/readout, or prove a weaker physically sufficient relation that
does not assert this full-state identification. Neither is supplied or
selected here. A global pure preparation is not itself the thermal state
in (4), and choosing its observable subalgebra remains part of the common
Omega/A/R obligation. A formal log of a supplied density cannot replace it.

This is not a claim about every native state, every coupled heat law,
Lorentzian heat, curved link spectra, or price-covector descent. It does
not prohibit cancellation in full paired-price contrasts, solve source
or Ward, remove response-null directions, or impose Gibbs identification
on the wider native-preparation plan. T0--T3, all 44 dependency nodes and
the original #310/#202/#317 terminals retain their existing scopes.

## 6. Proof status and reproduction

The all-m anti-concentration, all-temperature Hodge bound, projection
argument and uniform trace-distance limit are analytic proofs above.
No new Lean theorem is claimed. The companion exact checker binds the
primary weight/gate/Hodge definitions, reconstructs the recorded states,
all-mode small-lattice heat spectra, exact golden binomial masses, grouping
inequalities and noncommuting projection witnesses. Finite controls are
not extrapolated into (15). The replay has 1418 exact controls, nine executed
mathematical mutants and sixteen false scope/input ledgers; 91 input files
are pinned, including the consumed prior Hodge compilation receipt and its
transitive sources. The mathematical and scope rejections are separate.

Companion stem: `certificates/a4d_native_golden_hodge_state_separation`.
Run its `_check.py` from the repository root. It reads its frozen
`_certificate.json`; it does not choose a state, temperature law or source.
