# Closed native compilation does not yet select a gravitational law

27 October 2026. Research continuation within `gvakhrushev/d0_15`, existing
Draft PR #334 / `native-programme-v1`.
Pinned remote input: `33bfb4fb3a2d2ceafe529d25941c24e679a0af18`.

## Status and exact consuming step

This note tests the proposed LAST implication in the current synthesis:

> Since the complete comparison is internal, compiled from native gates,
> and has its own full heat and feedback, the system must select the
> constructed Einstein-report programme without another argument.

That implication does not follow from the properties used in the compiler
and reflection-clock proofs. An exact same-palette, same-inventory witness
and a full orbit calculation are supplied below. They do NOT disprove all
D0 models, refute the existing conditional Einstein-sector constructions,
or prohibit a separately derived same-task selection law. They prevent
promoting realizability/universality into selection.

The arithmetic result independently separates exact bounded native
compilation from the source papers' explicit conditional heralded resources.
Those conditional resources remain a valid possible route: they are NOT
refuted by an integrality argument that omits their conditioning.

No change to BOOK, CORE, acceptance, or `GR_closed` is made.

## 0. Inputs actually read

- BOOK_01 §§01.1.2, 01.1.4, 01.1.6: finite code space, canonicalization
  `Can(s)=min_[length,lex] [s]_equiv`, and the actual no-hidden-parameter fork.
- BOOK_03 §03.26.1 and the last local internal-clock packet: actual port
  Golden splitter G, SourceI X, and paid inverse `XXGXX` on every column.
- `A4D_NATIVE_CLOCK_FULL_PRICE_COMPILATION_AND_FINITE_TEST_RECOVERY_2026_10_27.md`,
  commit `33bfb4f`: source-faithful full-register compilation, generated
  clock cut, exact endpoint reflection heat and explicit finite-test scope.
- `A4D_FULL_TWO_BAND_FIXED_TEN_SIGN_CAR_CHOI_SOURCE_2026_10_21.md`, equations
  (1)-(6), fixed report at z=2^-20, and its supplied-resource status.
- `sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_FOUR_COPY_MATTER_RESPONSE.md`,
  §§4,7,8: fair coins and H/Toffoli are logical HERALDED resources, with all
  readiness/abort transcripts retained. They are not a deterministic
  finite Golden word implementing H on its own.

Files inspected from previous local artifacts are listed in MANIFEST.json.
The clocks/real gate literature supplies background, not a physical law:
Caha–Landau–Nagaj, arXiv:1712.07395; Shi, arXiv:quant-ph/0205115.
The finite proofs below are explicit and need no appeal to universality.

## 1. What canonical minimal description does and does not select

Let equivalent codes mean codes with the same declared complete operational
behaviour. A representative map Can has `Can(s) in [s]`. Therefore

    s not equivalent t  ==> Can(s) != Can(t).                 (1)

Proof: equality of representatives would put the same element in both
classes, and equivalence classes are either identical or disjoint.
The length/lex minimization is INSIDE one class, not over different physical
behaviours. It does not turn two distinguishable internal evolutions into
one. A separately defined prospective minimization over admitted programmes
with a compulsory task is another proposition and must be read as such.

This directly matches BOOK_01's no-hidden-parameter fork: a difference which
changes a future record must itself be encoded. An internally encoded
programme is not automatically an external catalogue. No claim that every
finite encoded programme satisfies every other D0 axiom is being made.

## 2. Literal native words, no new parameter or continuous primitive

Put p=phi^-1, t=sqrt(p)>0, so `t^4+t^2-1=0`. On the existing eight-dimensional
port x Q8-spin carrier use

    G = [[t,-p],[p,t]] tensor I4,
    X = diag(I4,L_i),
    L_i = [[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]],
    Z = X^2 = diag(I4,-I4),
    P = diag(I4,0), Q=I-P.

Thus G,X are orthogonal, X^4=I, ZGZ=G^T. The full eight columns are retained.
The spectator oldRIGHT of dimension128 can be tensored without alteration.
This is the original port/spin palette, NOT a claim that this eight-state
block is the entire CAR16 or 42-field gravity apparatus.

Use these two chronological words (leftmost gate is executed first):

    w0 = G X X G X X X X,
    w1 = G X X X X G X X.

Each uses exactly two G and six X, eight actual stages, no inverse primitive
and no idle padding. Direct multiplication gives

    M0 = X^4 G X^2 G = G Z G = Z,
    M1 = X^2 G X^4 G = Z G^2 = G^T Z G.                     (2)

Both complete endpoints are selfadjoint involutions with four +1 and four
-1 eigenvalues. Both are genuinely coherent closed comparison words in the
same class invoked by the preceding thermal theorem.

Their original endpoint feedbacks are

    F0=P M0 Q M0 P=0,
    F1=P M1 Q M1 P=4p^3 P.                                (3)

Golden identity gives `p^6+4p^3=1`, hence `0<4p^3<1`.
No probability has been postselected or assigned by a target equation.

## 3. Same complete clock heat, including every harmonic mode

Let A^j_k be the prefix product of word j through its first k gates,
`A^j_0=I`. Define stage gauges

    Q_k=A^1_k G^T (A^0_k)^T, k=0,...,7.

Every edge, including the closing edge, satisfies the exact identity

    U^1_k = Q_(k+1 mod8) U^0_k Q_k^T.                       (4)

It follows on ALL clock/work columns that the two covariant cycle shifts are
orthogonally conjugate. Apply the SAME Q_k at every K(9,11,13) scene vertex;
spatial edges remain identity. Consequently their actual normalized INTERNAL
connection Laplacians have identical spectra.

The product graph contains 33N vertices and 392N edges, N=8, with full fibre
d=8. Its degree0 heat has dimension2112; its degree1 heat has dimension25088,
before the unchanged oldRIGHT factor. The complete graded trace is exactly

    Z01=2 Tr exp(-beta Delta0)+359 N d,
    H01=beta^-1 log[128 Z01].                              (5)

Here `359 N d=22976`; it is not removed or normalized away. Equation (4)
proves equality of these full H01 values for ALL beta>0, not merely a
numerical near-equality. The independent Fourier block evaluation in the
checker is only a value diagnostic, not the proof of equality.

The physical generated active cuts, however, do NOT also map to one another
under (4), because at stage0 `G^T P G != P`. They are the two actual cuts
built from the SAME fixed input and each genuine prefix. Their feedback is
(3) at the return stage and zero at all other stages. This is checked on all
eight stages and every work column. Equal heat is not physical equivalence
of the complete readout.

For the explicitly specified full master `B=H01-logdet(I-zF)` at z=2^-20,

    B(w1)-B(w0) = -512 log(1-2^-20*4p^3)
                = 0.0004610704761577144178754751773162166... >0.  (6)

Any ADDITIONAL price depending only on these gate counts and fixed clock is
also equal. A history-dependent extra price is NOT assumed equal and is
not silently absorbed into H01. Neither word is asserted to satisfy a
separately compulsory curvature-reporting task. Precisely such a task or
another justified constraint would need to exclude one of them; closedness,
native gates, equal gate inventory and the specified master alone do not.

This does not make w0 a countermodel to the entire D0 programme. It is a
counterexample to claiming that those listed realization properties already
select the special nontrivial comparison and therefore Einstein dynamics.

## 4. Complete critical-point classification for the unrestricted reflection orbit

This theorem is a DIAGNOSTIC MATHEMATICAL RELAXATION, not a claim that every
continuous orthogonal variation is a D0 native primitive. The finite words
in §2 do not depend on that relaxation.

Let P be any orthogonal projection of rank r on a finite space. Let M vary
on the full orthogonal/unitary conjugacy orbit of a fixed selfadjoint
involution Z. Keep the same ranks and the isospectral full-clock heat. On PH
put C=PMP and F=P M(I-P) M P. Then

    F=I_PH-C^2,
    J(M)=-Tr_PH log[(1-z)I_PH+z C^2], 0<z<1.               (7)

THEOREM:

    dJ vanishes for every conjugacy tangent [Y,M]
       iff F^2=F.                                         (8)

The global minimum is J=0, attained exactly when F=0, equivalently
`[M,P]=0`. This is NOT the Einstein equation; it is the entire unconstrained
stationarity law of this particular reflection-feedback landscape.

Proof. Write blocks relative to P:

    M=[[C,B],[B^dagger,D]], M^2=I,
    B B^dagger=I-C^2.

The gradient supported in PH is

    K=diag(k(C),0),
    k(C)=-2z C[(1-z)I+z C^2]^-1.

For any skew adjoint Y,
`dJ=Tr(K[Y,M])=Tr([M,K]Y)`. The skew-adjoint trace pairing is nondegenerate,
so full stationarity is equivalent to `[M,K]=0`, which is equivalent to
`k(C)B=0`, hence `CB=0`. Finally

    (CB)(CB)^dagger=C^2-C^4,

so this holds iff the spectrum of C lies in {-1,0,1}, equivalently F is a
projection. Nonnegative eigenvalues of F lie in [0,1], so each contribution
`-log(1-z lambda)` is nonnegative and vanishes only at lambda0. This proves
the minimum statement. The conjugacy orbit contains a reflection commuting
with P by choosing a diagonal arrangement with the original +/- ranks.
No global positivity of a gravitational Hessian has been presumed.

For rank-one active blocks with F=4q(1-q)P, criticality allows only
`q=0,1/2,1`. The existing small nonzero READY probabilities are not in that
list. Their constrained FIELD roots can still be stationary because their
actual field map explores a smaller orbit tangent. The missing premise is
that actual constrained variation domain, not a demand to add externally
arbitrary control variations.

## 5. Exact arithmetic boundary of deterministic finite compilation

Let every primitive matrix entry be an algebraic integer. Start with
computational blank/basis registers; any finite word, with any finite number
of such ancillas, has algebraic-integer entries. Algebraic integers form a
ring and are preserved by complex conjugation. Every complete Born event
probability, a finite sum of unnormalized squared amplitudes, is therefore
an algebraic integer as well. A bounded adaptive tree with all transcript
branches retained has the same property, since every branch is a product
and its full event is a finite sum.

This applies to the literal G/X/CNOT palette above. `t` is a root of the
MONIC integer polynomial `t^4+t^2-1`; Q8 entries and Boolean gates are integers
(or roots of unity in the complex convention). No field parameter is added.
It does NOT apply unchanged to a supplied nonintegral density, a conditioned
success branch, unbounded repeat-until-success, or an independently allowed
nonintegral primitive.

The original two-band report at x=y=0, z=2^-20 has

    L=4p^3,
    r0=1-(1-zL)[1-zL(1+p^6)]
      =(1245203/8589934592)p-3014703/34359738368.             (9)

Because p'=-1-p is the quadratic conjugate,

    Tr_Q(sqrt5)/Q(r0) = -5505109/17179869184,                (10)

which is not an integer. The trace of an algebraic integer in this quadratic
field is an integer. Thus r0 is NOT an algebraic integer, also not in any
larger field's ring of algebraic integers. Consequently:

    r0 cannot be an EXACT unconditional output probability of a bounded
    pure-blank G/X/CNOT programme.                          (11)

This is a concrete exclusion for that precise finite-compilation contract,
not a no-go for continuum GR, arbitrary D0 resources or approximation.
The latest branch's dense full-register compiler only claims approximation
and is not contradicted.

The ten-sign conditional-beta polynomial has average r0 over all 1024
uniform sign words. If all 1024 pure-branch samplers were deterministic
bounded integral-palette programmes, `1024*r0` would be integral. Its
quadratic trace is still noninteger. Thus at least one such conditional
sampler requires a declared resource beyond that deterministic contract.

### The actual heralded escape is retained, not overlooked

Two genuine Golden coins give amplitudes p, p sqrt(p), p sqrt(p), p^2.
Odd parity succeeds with probability `alpha=2p^3`, and the two retained odd
outcomes each have unconditional probability p^3. Given success, either
outcome has probability1/2. There is no contradiction: conditioning divides
by alpha, so the ring argument no longer applies to that conditional law.
The full three-status law is

    (abort,logical0,logical1)=(1-2p^3,p^3,p^3).              (12)

The source's four-copy owner explicitly uses coherent fair resources and
heralded logical H/Toffoli, with readiness and all aborts. It is therefore
incorrect to cite (11) as a refutation of that source-resource construction.
It proves that those resources and their success rates cannot simply be
deleted when moving to an unconditional exact finite-word claim.
As a denominator control only, `(2p^3)^35*r0` lies in Z[p], while powers
0,1,10,34 do not. This does NOT prove an optimal number of heralds or compile
the whole general reporter.

## 6. What an honest complete D0-to-GR theorem still has to prove

The existing results construct a supplied reporter from geometric/matter
moments, a full price, and a controlled smooth source comparison. The latest
finite-test compilation theorem supplies operational witnesses for that
chosen reporter. These are useful and retained.

They are not yet a proof that the closed system itself selects precisely
that task, source preparation, cut and full valuation. In symbols,

    exists native realization whose normalized source tends to Einstein

is different from

    the source of the physically selected complete D0 process is Einstein.

The first statement does not require uniqueness of every microscopic action.
The second DOES require either a proved original process binding or an
actual source-preserving equivalence on its admitted configurations.

Our two words show the selection step is not a consequence of the already
used closed-word conditions alone. The critical theorem identifies exactly
what unconstrained use of their master would select. The integrality
calculation prevents conflating deterministic exact native words with the
separately explicit conditional-resource or approximate interfaces.

A legitimate continuation can derive an internal mandatory comparison task
and prove the same-complete-price constraints from it, or establish a
source-equivalent closed process by its real defining rules. The theorem
must not define that task as "the histories that satisfy Einstein", freeze a
free input after seeing its source, or add an entropy/counterterm fitted to
remove (6). Source-consistent exact roots and their joint continuum limit
retain their own hypotheses; this packet neither constructs nor excludes
those roots.

## 7. Executed evidence

`check_selection.py` proves both literal8-stage words over Q[t]/(t^4+t^2-1),
checks every stage-gauge intertwiner and both generated cuts on all8 columns,
retains the true scene and harmonic count, and checks the critical condition
on exact rational multi-block fixtures. The heat value is an ordinary
floating Fourier-block diagnostic; its equality has an exact matrix proof.

`check_arithmetic.py` reduces the native r0 and its trace over exact rationals,
checks the 1024-branch implication and the positive conditioned-fair escape.
Neither script uses optimization-removable `assert`. Both normal and
`python -O` executions were actually run and give identical JSON bytes.

No original large READY/GR programme was emitted; no all42 root, original
full128 CAR certificate, Lean build, independent review or CI was rerun.
No closure flag is promoted. This is a bounded test of the actual remaining
physical-selection inference, not another geometric solution census.
