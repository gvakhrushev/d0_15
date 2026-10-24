# The actual native copied report, its information source and its preparation row

25 October 2026. Same PR #334, constitutive/native-programme-v1 owner.
This packet consumes the whole native operator/clock construction of
[primary §7w](../../A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md#7w-transfer-the-original-operator-and-finite-heat-through-full-native-words)
and its [operator-holonomy proof](../d0_native_operator_holonomy_2026-10-25/PROOF.md).
It computes a recorded-information component and a genuine upstream
preparation source for that execution. It does not define a replacement
thermal model, select Book03 Info from a desired field equation, or set
an uncomputed Cost/work/preparation source to zero.

## 1. The complete balanced word and the actual seal boundary

Let `h` be the realification/report bit, `A` a NEW copy-bank bit, and
`F` the entire other carrier on which the native word acts. Let `R`
denote original immutable oldRIGHT/reference registers. All actual
work/source-spin modes belong to `F` or to explicitly retained identity
spectators; they are not deleted because an input is blank. The initial
state is

\[
 |0\rangle\langle0|_h\otimes\Omega_{FR}
          \otimes|0\rangle\langle0|_A.
\]

`V` is the actual full-column native word on `hF`, tensor identity on
`R`. Define the real CX `C=CX(h,A)` and the COMPLETE balanced endpoint

\[
 B=C(V\otimes I_A)C,\qquad
 M_b=(\langle b|_h\otimes I_F)V(|0\rangle_h\otimes I_F),
 \quad\sum_{b=0}^1M_b^\dagger M_b=I_F.                 (I1)
\]

The rightmost `C` is identity on the actual initialized column, not on
the unprepared full carrier. Both CX stages belong to the word, its
primitive clock and its full heat. There is no invocation of an
initialized-channel identity in place of an all-column monodromy.
Writing identity factors on `R` implicitly, put

\[
 X_{bc}=M_b\Omega M_c^\dagger,\qquad X_b=X_{bb},\qquad
 p_b=\operatorname{Tr}X_b.
\]

The exact COMPLETE output and its new-bank marginal are

\[
 \Theta=B(|0\rangle\langle0|_h\otimes\Omega
                   \otimes|0\rangle\langle0|_A)B^\dagger
 =\sum_{b,c}|b\rangle\langle c|_h\otimes X_{bc}
                         \otimes|b\rangle\langle c|_A,              (I2)
\]
\[
 \Gamma_{hFR}=\operatorname{Tr}_A\Theta
       =\sum_b|b\rangle\langle b|_h\otimes X_b.                    (I3)
\]

Thus the marginal is CQ at this boundary, with its entire conditional
DATA/work/reference block. The complete state (I2) remains coherent.
In particular neither an environment, a dephasing primitive, a reset,
nor a second independent Shannon outcome has been inserted. This is
the literal binary application of
[paid writer §14.1, (73)–(74)](../../A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#141-actual-recording-including-the-complete-unprepared-space).

Sealing is a PREFIX/SUFFIX interface, rather than an illegal change of
the oldRIGHT mask halfway through one static execution description.
The prefix has a fresh, active bank and includes BOTH copies and every
inverse/preparation stage. At its endpoint retain the SAME correlated
state (I2), transfer the bank's wire identifier to the suffix's immutable
mask, and require all suffix gates to avoid it. The suffix imports this
state; it does not initialize the bank again. The executable grammar's
`old_right`/blank disjointness and no-oldRIGHT-gate rule are unchanged
([native domain](../d0_native_execution_domain_2026-10-24/native_execution.py)).
In particular no subsequent replay of a prefix inverse may touch this
sealed bank. Original oldRIGHT is never a target, control or scratch
register in the prefix or suffix. Historical preparation before an
original reference was first sealed is a separate interface below.

For a suffix word `I_A tensor S` and a terminal effect `I_A tensor E`,
the exact decoder is

\[
 \operatorname{Tr}[\Theta(I_A\otimes S^\dagger E S)]
       =\operatorname{Tr}[\Gamma S^\dagger E S].                    (I4)
\]

The tensor order in (I4) is immaterial. If the declared terminal test
may additionally read the archived bank in its computational basis,
but has no bank-X/coherence read, its effect is instead
`sum_b |b><b|_A tensor E_b`. Its value is exactly

\[
 \sum_b\operatorname{Tr}\big[
  (|b\rangle\langle b|_h\otimes X_b)S^\dagger E_bS\big].          (I5)
\]

Thus the same CQ boundary data decode even the retained archive VALUE.
This read is an explicit terminal-test allowance, not an inferred new
gate acting on immutable oldRIGHT. In the bank-blind case partial
trace is sufficient on every full state; in the bank-Z case the bank
block-diagonal memory is sufficient on every full state, and (I3)
reconstructs that memory on the ACTUAL copied column. Suffix actions
on the active report may create new report coherences, but cannot
recover the bank-off-diagonal terms discarded by these decoders.

These decoder equalities supply the `correct` hypothesis of the OWNED
`FutureExecution.sufficient_memory_reflects_future`
([FutureExecution.lean, lines 111–120](../../../../03_FORMALIZATION/D0/Foundation/FutureExecution.lean))
and hence of `VerificationCore.sufficient_memory_preserves_record`
([VerificationCore.lean, lines 202–211](../../../../03_FORMALIZATION/D0/Foundation/VerificationCore.lean)).
They do not reprove or enlarge the foundational future alphabet. If
an actually allowed terminal comparison contains a joint bank-X
effect, (I4)–(I5) no longer certify that comparison. The explicit old
Q8 access boundary is retained
([retained-work test algebra](../../A4D_Q8_RETAINED_WORK_COHERENCE_TEST_ALGEBRA_2026_10_22.md)).
The generic foundational `Test`/`observe` fields alone do not impose
the bank-blind or bank-Z test policy.

Original `R` has its OWN independent access restriction. In particular
(I3) is a sufficient reference-retaining mathematical memory, not a
proof that all operators on `FR` are physically readable. If suffix
tests also ignore `R`, trace it in the decoder. No claim that the full
CQ algebra is the minimal actual future algebra follows from copying.

## 2. The computed information component and the oldRIGHT distinction

All logarithms and entropies below use natural units;
`h_2(q)=-q log q-(1-q)log(1-q)` denotes binary entropy in those units.

Let `E_A` pinch the copied bank in its actual computational basis and
put `Gamma_tilde=E_A(Theta)`. It has the same nonzero spectrum as
`Gamma` in (I3): the map copying the report label into the bank is an
isometry on the block-diagonal support. Also `S(Theta)=S(Omega)` by
(I1). The OWNED canonical registered-pinching identity therefore gives

\[
 \mathcal I_{\rm ref}:=S(\Gamma_{hFR})-S(\Omega_{FR})
   =D(\Theta\Vert\widetilde\Gamma)
   =H(p)+\sum_b p_bS(X_b/p_b)-S(\Omega).              (I6)
\]

The relative entropy in (I6) is on the SAME full Hilbert space. It is
not `D(Theta || Tr_A Theta)` between different spaces. The bank is not
counted a second time. The consumed result is
[canonical future-register pinching §§1–2, (1)–(5)](../../A4D_FUTURE_ALGEBRA_CANONICAL_PINCHING_OFFNULL_CQ_SOURCE_WELD_2026_10_22.md#1-theorem-a--canonical-operator-valued-future-memory-and-the-unique-lost-coherence-information)
and its actual-word application
[paid writer §14.2, (80)–(81)](../../A4D_PAID_MOMENT_FIELD_WRITER_2026_10_21.md#142-the-actual-known-cost-its-residual-and-the-full-registered-info).
If the COMPLETE initial `Omega_FR` is pure, each nonzero `X_b` is rank
one and `I_ref=H(p)`. A mixed DATA marginal of that pure correlated
state does not invalidate this PURE-GLOBAL statement.

If the actually retained test algebra ignores the original reference,
write `rho_F=Tr_R Omega` and `Gamma_hF=Tr_R Gamma`, and define the
different component

\[
 \mathcal I_{\rm act}:=S(\Gamma_{hF})-S(\rho_F).
\]

The exact already-owned oldRIGHT/Holevo boundary specializes to

\[
 \mathcal I_{\rm ref}-\mathcal I_{\rm act}
 =I(F:R)_\Omega-I(hF:R)_\Gamma\ge0,                  (I7)
\]

because the instrument `F -> hF` is a channel and the `R` marginal is
unchanged. For pure global `Omega`, the conditional `FR` branches are
pure, hence

\[
 \mathcal I_{\rm ref}=h_2(p_1),\qquad
 \mathcal I_{\rm ref}-\mathcal I_{\rm act}
 =S(\rho_F)-\sum_b p_b S(\rho_{F|b}).                 (I8)
\]

This difference need not vanish. General restricted within-sector
tests can forget still more. Equations (I6)–(I8) are valuations of
specified complete/marginal records, not a derivation that compulsory
Book03 Info selects the complete reference-retaining one. See
[stopped quantum price, mixed-DATA convention and oldRIGHT boundary](../../A4D_NATIVE_STOPPED_QUANTUM_PRICE_AND_SOURCE_2026_10_22.md)
and the canonical pinching owner's explicit future-algebra defect.
Book06's typed quotient/entropy principle requires the retained tests
and loss quotient to be declared
([Book06 §§06.5 and 06.24](../../../../01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md));
it does not destroy the coherent archive in (I2).

## 3. All field Fréchet terms and the independent preparation adjoint

First fix the bank/report basis, fixed input support and all other
parameters. On a faithful regular chart let `log X_b` mean the log on
its fixed support. A disappearing branch or changing support must be
handled by the continuous entropy/amplitude extension, not by a log
of zero. For any actual differentiable full-word comparison `V(t)`,
`dot M_b=<b|dot V|0>` and

\[
 \begin{split}
 \dot{\mathcal I}_{\rm ref}
 &=-\sum_b\operatorname{Tr}
  [(\dot M_b\Omega M_b^\dagger+M_b\Omega\dot M_b^\dagger)
                                                   \log X_b]
       +\operatorname{Tr}(\dot\Omega G_\Omega),\\
 G_\Omega&=\log\Omega-
            \sum_b M_b^\dagger(\log X_b)M_b .          (I9)
 \end{split}
\]

The apparent `+I` log derivatives cancel by trace normalization and
`sum M_b†M_b=I`, including its derivative. No preparation term is
discarded. Formula (I9) also applies to `I_act` using its actual reduced
input and branch blocks, rather than replacing them by the pure-global
entropy in (I8). All source-spin/factory/reference factors included in
the true input remain in this formula. Additional initialized work
cannot be silently replaced by an independently varied mixed input.

For the IDEAL full holonomy target of §7w, before its identity auxiliary
factor,

\[
 U_\delta=\exp(\delta J\otimes K),\quad
 J=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
 L_0=\cos(\delta K),\quad L_1=\sin(\delta K).           (I10)
\]

Here `K=K_alpha(D)` is the SAME odd, invertible map consuming the
original finite polynomial heat, not a new exponential substitute.
For fixed `delta`, the complete field derivative uses

\[
 \dot K=DK_\alpha(D)[\dot D],\quad
 \dot L_0=D\cos(\delta K)[\delta\dot K],\quad
 \dot L_1=D\sin(\delta K)[\delta\dot K].                (I11)
\]

In a `K` eigenbasis these are respectively
`cos^[1](delta k_i,delta k_j) delta Kdot_ij` and
`sin^[1](delta k_i,delta k_j) delta Kdot_ij`, with the ordinary
derivatives on equal eigenvalues. This specifies every noncommuting
Fréchet entry; replacing them by `-delta sin(delta K) Kdot` and
`delta cos(delta K) Kdot` is valid only in the commuting case.
Insert these `dot L_b` into (I9). For a pure global fixed input the
same expression reduces, without losing the reference, to

\[
 q=\operatorname{Tr}[\Omega\sin^2(\delta K)],\quad
 \dot q=\operatorname{Tr}\{\Omega D\sin^2(\delta K)
                                      [\delta\dot K]\},\quad
 \dot{\mathcal I}_{\rm ref}
      =\log[(1-q)/q]\,\dot q.                         (I12)
\]

An independently moving input adds
`Tr(dot Omega sin²(delta K))` to `dot q`. For mixed global input the
conditional terms in (I9), not just `q`, are required. The gain and
conditioning of `D -> K`, including the independent density/observer
and material rows, remain those of the consumed holonomy proof.

There is one useful exact zero which must not be overextended. Since
the instrument acts trivially on original `R`, any admitted initial
local-unitary variation there transports `Omega`, `X_b` and `Gamma`
by the SAME `U_R`. Their entropies, and thus (I6), are invariant. In
the real native comparison write `Omega(t)=e^{tT_R}Omega e^{-tT_R}`
with `T_R` real skew; then

\[
 \operatorname{Tr}([T_R,\Omega]G_\Omega)=0.            (I13)
\]

This is an initial-state symmetry reaction, not a physical gate on
immutable oldRIGHT. Arbitrary correlated preparation variations are
not local unitaries and generally have the nonzero (I9) reaction.
Changing the registered basis/cut adds its own moving-expectation term.
Neither (I13) nor the partial trace freezes these independent rows.

## 4. An exact native preparation orbit of the CURRENT-WINDOW Book map

This witness uses the SAME initial state for every compared current
execution and an actual native prefix/inverse. It does not replace
`Omega` by a fitted probability table. Put

\[
 p=(\sqrt5-1)/2,\quad a=\sqrt p,\quad
 G=\begin{pmatrix}a&-p\\p&a\end{pmatrix}
   =e^{\theta J},\quad \cos(2\theta)=p-p^2=p^3.       (I14)
\]

Use DATA `d=0`, report/source-port `h=1`, new bank `A=2`, source-spin
bits `3,4`, and original reference `R=5`. BEFORE the original `R` was
sealed, the literal historical two-stage preparation
`G_d; CX(d,R)` from blanks prepared

\[
 |\psi_0\rangle_{dR}=\sqrt p\,|00\rangle+p|11\rangle,
 \quad\Omega_0=|\psi_0\rangle\langle\psi_0|,
 \quad\rho_{d,0}=\operatorname{diag}(p,p^2).          (I15)
\]

Its actual preparation/storage cost remains in the ledger. It is NOT
an instruction to act on a wire already declared oldRIGHT. Every
current word below avoids bit5. Fixed independent source-spin states
are retained and cancel from this entropy difference; the completed
inverse is identity on source-spin on ALL columns. More general
correlated inputs retain (I9).

For `Q=33`, take the exact chronological native word

\[
 U_Q:\quad G_h^{4Q};\ CX(d,h);\ G_h^{2Q};\ CX(d,h).
                                                               (I16)
\]

Its DATA blocks are `G_h^(6Q)` and `G_h^(2Q)`, respectively. Let `phi`
be the principal angle of `G^(2Q)`. For this `Q`, `0<|phi|<pi/12`;
hence (I16) is LITERALLY (I10) with
`delta K=diag(3phi,phi)`, and

\[
 e_0=\sin^2(3\phi)>e_1=\sin^2\phi>0,\qquad e_0<1/2.                (I17)
\]

These strict signs are exact algebraic questions, not numerical entropy
fits: with `u_0=p³`, `e_1=1-T_33(u_0)^2` and
`e_0=1-T_99(u_0)^2` lie in `Q(p)`. For example
`cos(66theta)=587860948692033799911485385730 p
-363318046950434930074906455681` lies strictly between `9999/10000`
and1 by rational comparisons in the selected positive-square-root
embedding. It is not1, and this bound implies the stated small-angle
condition. The packet checker records exact quadratic-field sign
checks for (I17); floating entropy magnitudes have a separate scope.

Let `A_n=G_d^n`, with positive integer `n`. The CURRENT complete word
is chronological

\[
 B_n:\quad C;\ A_n;\ U_Q;\ A_n^\dagger;\ C,
 \qquad C=CX(h,A).                                   (I18)
\]

Its prepared report Kraus blocks are `A_n† L_b A_n` on the SAME
`Omega_0`, equivalently `L_b` on
`Omega_n=(A_n tensor I_R)Omega_0(A_n† tensor I_R)` followed by the
common output unitary `A_n†`. For `u_n=cos(2n theta)`,

\[
 q_n={e_0+e_1\over2}+{(e_0-e_1)p^3\over2}u_n,
 \quad\mathcal I_{{\rm ref},n}=h_2(q_n).              (I19)
\]

The DATA input is mixed, but the actual DATA+oldR input (I15) is pure.
This is why the second equality in (I19) is the reference-retaining
component. It is NOT a license to set the accessible `I_act` to that
value. Its correct weighted conditional entropies and (I7) remain.

For the mathematical preparation-plane comparison `u=cos2vartheta`
around the native `n=1` point, `u_0=p³`, the exact derivative is

\[
 {d\mathcal I_{\rm ref}\over du}
   ={(e_0-e_1)p^3\over2}\log{1-q(u)\over q(u)}>0.    (I20)
\]

The strict sign follows from (I17) and `0<q(u)<1/2`. The actual pure
preparation lift has
`||d psi/du||²=1/[4(1-u²)]`; at `u=p³` this is finite and nonzero.
Thus this source has a real preparation norm rather than an unpriced
probability-coordinate rescaling. `n=67` and `n=1161` give native
values on opposite sides of `u_1`; their exact quadratic-field
contrasts provide genuine finite-code secants. No continuous native
`G(vartheta)` pulse or continuous selector of finite words is asserted.

Every inverse in (I18) is the source-I all-column inverse of the
existing grammar, NOT a newly admitted `G^-1` atom. The source port
is `h`; routing a DATA inverse uses `1G+6CX+4 SourceI` per factor.
The COMPLETE unpadded inventories are therefore

\[
 g_n=6Q+2n,\quad c_n=4+6n,\quad s_n=4n,\quad
 N_n=g_n+c_n+s_n=6Q+4+12n.                            (I21)
\]

The two `C` stages, dirty-spin intermediate stages and all unprepared
columns are included. The source-spin is returned by each completed
inverse macro, and oldRIGHT is untouched. Pad the COMPLETE words by
the already-owned two/five-CX identity words on active wires `0,1,2`,
before sealing, to a common `N=max(N_n)+4`. For the three stated
`n` values this is `N=14138`. Padding has real CX stages, clock modes
and work; no idle is assigned zero duration.

There is an exact reason the CURRENT-WINDOW whole bare Book `H+J`
misses this row. This window starts from the already supplied (I15);
it does not include that historical preparation in its clock word.
Since `A_n` commutes with `C`,

\[
 B_n=(A_n^\dagger\otimes I)B_0(A_n\otimes I).
                                                               (I22)
\]

The actual input cut fixes `h=A=0` and any declared source blanks,
but not DATA; it commutes with `A_n`. Thus the single-return defect
is conjugated on its FULL cut, and its feedback determinant is exactly
unchanged. The clock's entire heat spectrum is determined by the
full endpoint holonomy and common `N`, so it too is unchanged, not
only its low branch or initialized report probability. Every full
fibre/oldRIGHT/source-spin multiplicity is the SAME across this
comparison. This consumes the original holonomy theorem, rather than
deleting copy modes or replacing `H` by a report entropy. The common
clock parameters and cut are held fixed in this comparison. Hence

\[
 (H+J)(B_n)=(H+J)(B_0),\qquad
 \mathcal I_{{\rm ref},n}\ \hbox{is not constant}.     (I23)
\]

Any additional birth/Rayleigh, actual preparation, work, observer,
stopping or controller term retains its own response. Equation (I23)
is not a no-go for an unchanged complete D0 action, and the elementary
two-scene native witness is not claimed to satisfy the original GR
dictionary or geometric stationary equations. It exhibits the named
independent preparation row inside the same operational domain.

## 5. Put the historical preparation INSIDE the full word and recompute Book

The preceding plateau is a valid current-window statement, not a
calculation of the full birth-to-record Book clock. To price the latter
on the SAME physical preparation, write `P=CX(d,R) G_d` for (I15),
with `P` executed first, and use

\[
 F_n=W_nP,\qquad W_n=B_n\text{ with the actual common padding}.
                                                               (I26)
\]

The full input fixes `d,h,A,R` to0 and leaves the two source-spin bits
protected with arbitrary state/rank up to4. The FULL cut is

\[
 P_{\rm full}=|0000\rangle\langle0000|_{d,h,A,R}
                      \otimes I_{\rm spin},\qquad
 \operatorname{rank}P_{\rm full}=4.                    (I27)
\]

By comparison the current-window cut is `|00><00|_(h,A) tensor
I_(d,R,spin)` and has rank16. The fibre is64 in BOTH cases, with
`2N times64` paired clock modes. A particular input-state rank is not
a thermal dimension. The spin is protected arbitrarily even though
the other four wires are blank.

The full native chronological list is `G_d; CX(d,R); W_n`; its
historical `R` wire is not oldRIGHT until AFTER these first two
stages. The same explicit seal handoff then forbids every subsequent
gate on it. A single static validator description of the WHOLE word
must therefore not falsely mark that wire immutable before `P`.
Its ordinary membership record has it active initially, while the
prefix/suffix seal metadata impose the stronger chronological rule.
The code is finite and every gate support is explicit; no reset or
new oldRIGHT control is used. Source-spin keeps its original protected
typing throughout. Seal the NEW copy bank only after `W_n` and all
its current padding. The total common stage count is

\[
 N_{\rm full}=N+2=14140.                              (I28)
\]

There is no free prefix and no additive thermal-price approximation.
The prior `P` is fixed across `n`, but the heat of the product `W_nP`
is not generally the heat of `W_n` plus a constant cost for `P`.

Here is its complete, small-block exact spectrum. Let
`phi=arg G^(2Q)` as before, and put

\[
 c_n=\cos((1-2n)\theta),\qquad
 \chi_+=\arccos(a\cos\phi),\qquad
 \chi_{-,n}=\arcsin(c_n\sin\phi),\quad a=\sqrt p.       (I29)
\]

Use the principal `arccos` in `[0,pi]` and `arcsin` in
`[-pi/2,pi/2]`. The four representative angles are

\[
 \omega_{1,2}=2\phi\mathbin{\pm}\chi_+,\qquad
 \omega_3=2\phi+\chi_{-,n},\qquad
 \omega_4=2\phi+\pi-\chi_{-,n}.                        (I30)
\]

The FULL64-column spectrum is `exp(±i omega_j)`, each signed entry
with multiplicity8. Degeneracies mean these multiplicities add;
they do not remove modes.

To prove (I30), work first in a computationally unrelated mathematical
X-eigenbasis of the bank and historical `R`. This is spectral analysis,
not a physical X read of a sealed record. If the bank-X eigenvalue is
`eta=±1`, the copy conjugation sends `U_Q` to `U_Q` or `U_Q†`,
respectively. If the `R`-X eigenvalue is `zeta`, `P` reduces to
`G_d` for `zeta=+1` and `Z_d G_d` for `zeta=-1`. Conjugating the
whole block by `A_n` therefore gives

\[
 U_\eta G_d\quad(\zeta=+1),\qquad
 U_\eta G_d^{2n-1}Z_d\quad(\zeta=-1).                 (I31)
\]

Diagonalize `J_h` with eigenvalues `i s`, `s=±1`. Up to the scalar
`exp(2i s eta phi)`, the DATA matrices in (I31) are
`exp(i s eta phi Z)G` and
`exp(i s eta phi Z)G^(2n-1)Z`. The first has determinant1 and trace
`2a cos phi`, giving phases `±chi_+`. The second has determinant−1
and trace `2i s eta c_n sin phi`; its eigenvalues are
`exp(i s eta chi_-)` and `-exp(-i s eta chi_-)`. This gives precisely
the conjugate pairs (I30). Reversing `eta` permutes the same four
phases, giving the bank multiplicity2. The identity source-spin gives
the other factor4. Thus all64 columns have been included.

For the actual paired primitive clock define the even full winding sum

\[
 \mathscr K_{N,\beta_c}(\omega)
 =\sum_{k\bmod N}
  \exp\{-\beta_c[1-\cos((2\pi k+\omega)/N)]\}.
\]

At the fixed common `N=N_full`, with the actual fixed `beta_c`,

\[
 Z_{\rm full}=32\sum_{j=1}^4\mathscr K_{N,\beta_c}(\omega_j),
 \qquad H_{\rm full}=\beta_c^{-1}\log Z_{\rm full}.    (I32)
\]

The factor32 is `2` Hodge grades times `8` multiplicity times `2`
for each `±` pair. At `beta_c=0` the partition is `128N`, exactly the
paired dimension. There is no extra `N` outside the winding sums.
All padding and dirty-spin primitive prefixes remain in this clock;
the owned holonomy theorem accounts for them rather than discarding
them. Using §7w's temperature schedule means substituting its true
`N_full` in that schedule; it does not turn (I32) into the old spatial
heat or restore the current-window plateau.

The complete return block can also be obtained without a spectral
approximation. On returning to `R=0`, only the `sqrt(p)|00>` branch
of (I15) contributes. Returning both the report and copied bank to0
then selects `L_0`. Thus, with `u_n=cos(2n theta)` and

\[
 g_0(u)={\cos3\phi+\cos\phi\over2}
             +{\cos3\phi-\cos\phi\over2}u,
\]

the exact full cut corner, return defect and feedback are as follows,
where `i_full` inserts the four blanks of (I27) and retains source-spin:

\[
 i_{\rm full}^\dagger F_ni_{\rm full}=\sqrt p\,g_0(u_n)I_{\rm spin},
 \quad E_{\rm full}=[1-pg_0(u_n)^2]I_{\rm spin},
\]
\[
 J_{\rm full}=-4\log\{1-z[1-pg_0(u_n)^2]\}.           (I33)
\]

The factor4 is the actual FULL cut rank, not the window rank16 or
the heat fibre64. In particular this is not the window feedback
evaluated with a different input probability. Its preparation
derivative for a smooth comparison-plane parameter `u` is

\[
 {dJ_{\rm full}\over du}
 ={-8pz\,g_0(u)g_0'(u)\over1-z+pz g_0(u)^2}.          (I34)
\]

For (I17), `g_0>0` and `g_0'<0`, so this derivative is strictly
positive. A full preparation source has therefore actually appeared;
it cannot be hidden in a purported constant prefix price.

For completeness the HEAT derivative is equally explicit, including
its relation to the preparation plane. On a branch
`v=sin(2vartheta)=sigma sqrt(1-u²)` set

\[
 c(u)=a u+p\sigma\sqrt{1-u^2},\quad
 \chi_-'(u)={c'(u)\sin\phi\over
                 \sqrt{1-c(u)^2\sin^2\phi}},\quad
 c'(u)=a-{p\sigma u\over\sqrt{1-u^2}}.
\]

Here `chi_+` and all fixed physical parameters stay fixed. Directly
differentiating the FINITE full sum gives

\[
 {dH_{\rm full}\over du}
 ={32\over\beta_c Z_{\rm full}}
  [\mathscr K'(\omega_3)-\mathscr K'(\omega_4)]\chi_-'(u),
\]
\[
 \mathscr K'(\omega)=-{\beta_c\over N}
  \sum_{k\bmod N}\sin((2\pi k+\omega)/N)
       e^{-\beta_c[1-\cos((2\pi k+\omega)/N)]}.       (I35)
\]

This is a comparison-plane covector, not a freely available smooth
native pulse. At `n=1` the branch has `sigma=+1` and
`c'(u_0)=1/(2sqrt(p))`. Finite native alternatives use their exact
values (I32)–(I33) and their actual common duration, not an assumed
derivative of a discrete code selector.

The configured full-Book NONFLATNESS also has a strict finite-code
certificate, separate from non-interval numerical entropy values.
Fix ONLY here `Q=33`, `N=14140`, `beta_c=512N²`, `z=1/4` and the
full cut rank4. Exact `Q(p)` comparisons of (I33) give
`E_67-E_1>1/10^6` and `E_1-E_1161>1/10^6` for their scalar defects.
For this cut and `z`, `J'(E)=1/(1-E/4)>1`. Meanwhile
`cos phi>9999/10000` and `pi²<10` imply `phi²<1/2000<1/1600`:
use `1-cos phi>=2phi²/pi²` on its principal arc. Since
`|omega_3|<=3|phi|`, one retained full-clock mode gives
`H_full>=-9/(3200N²)`. All `128N` modes give
`H_full<=log(128N)/(512N²)<21/(512N²)`, because
`128N<2^21` and `log2<1`. Thus, denoting by `osc H_full` the
range over these three words,

\[
 \operatorname{osc}H_{\rm full}
 <{561\over12800N^2}={561\over2559226880000}<10^{-8},\qquad
 B_{{\rm full},67}-B_{{\rm full},1}>{9\over10^7},\quad
 B_{{\rm full},1}-B_{{\rm full},1161}>{9\over10^7}.     (I42)
\]

This proves actual configured full-Book price differences at the SAME
complete blank input and common paid clock. It makes no universal
nonflatness assertion for other temperatures, `z`, cuts or additional
physical source terms. The bounds are checked in the packet's final
exact-sign/clock checker rather than inferred from plotted values.

The complete prepared output is still obtained from (I15) followed by
(I18). Thus the terminal state, actual report `q_n`, and conditional
blocks are unchanged. The input boundary in an entropy GAIN must,
however, be changed with the clock. The reference-complete candidate
still has `I_ref=h_2(q_n)`: the active `d,h,A,R` input factor and the
window DATA/reference factor (I15) are pure, tensored with the SAME
independent protected-spin state whose entropy cancels. No purity of
that arbitrary rank-up-to4 spin state is assumed. If only active
DATA/report is retained,
the full input DATA is fresh and pure, while the window DATA input
has entropy `h_2(p)`. Consequently

\[
 \mathcal I_{{\rm act},\rm full}
       =\mathcal I_{{\rm act},\rm win}+h_2(p).         (I37)
\]

The DPI/reference-defect equation (I7) applies to the WINDOW where
`R` is already a passive reference throughout the instrument. It
must not be applied to the full word from before `P`, which actually
acts on `R`. In particular it cannot delete the constant in (I37).

There is a concrete intermediate original-reference policy which
uses no forbidden quantum access to oldRIGHT. Declare suffix gates
to avoid both sealed records, allow their terminal computational-Z
values, and retain the full conditional active DATA/work inside each
`(r,b)` block. This is an explicit registered-test contract, not a
deduction that every native future test has this maximal algebra.
The old-reference pointer probabilities are `p_0=p`, `p_1=p²`.
Conditioned on them, the two report probabilities are

\[
 q_0(u)={e_0+e_1\over2}+{e_0-e_1\over2}u,\qquad
 q_1(u)={e_0+e_1\over2}-{e_0-e_1\over2}u,\qquad
 \Pr(r,b)=p_r\operatorname{Bern}_{q_r}(b).            (I38)
\]

This follows by applying `A_n` to the actual conditional DATA inputs
`|0>` and `|1>` in (I15). The conditional DATA output blocks are
pure, including the common `A_n†` return. Pinching BOTH actual sealed
record values therefore gives terminal entropy
`h_2(p)+p h_2(q_0)+p² h_2(q_1)`. At the supplied-input window boundary
the same original-reference restriction already assigns input entropy
`h_2(p)`: its registered input is
`p|00><00|+p²|11><11|`, not the coherent pure reference state. For the
full before-`P` boundary all four bits are genuinely fresh blanks.
The two properly typed registered gains are thus

\[
 \mathcal I_{{\rm reg},\rm win}
      =p h_2(q_0)+p^2h_2(q_1),\qquad
 \mathcal I_{{\rm reg},\rm full}
      =h_2(p)+\mathcal I_{{\rm reg},\rm win}.          (I39)
\]

They are generally neither the coherent-reference `I_ref` nor the
reference-blind `I_act`. This is the existing registered-pinching
owner applied to the ACTUAL input and output algebras, not a fourth
arbitrary entropy table. The fixed initial-prefix entropy `h_2(p)` is
constant on this particular `u` plane but remains in the absolute
full price. Its derivative, with the declared fixed `p`, is

\[
 {d\mathcal I_{\rm reg}\over du}
 ={e_0-e_1\over2}
    \{p\log[(1-q_0)/q_0]-p^2\log[(1-q_1)/q_1]\}.     (I40)
\]

This actual Z-only original-reference contract has an EXACT nonzero
source in the same native example; full quantum oldRIGHT access is
unnecessary. On `1/5<=u<=3/10`, which contains the three stated native
values, the exact quadratic-field bounds for `Q=33` are
`49/50000<e_0<1/1000` and `e_1>1/10000`. They imply
`q_0<1/1000` and
`q_1>(7/20)(49/50000)+(13/20)(1/10000)>1/2500`.
Consequently `h_2'(q_0)>6` and `h_2'(q_1)<8`, since `e^6<999`
and `e^8>2499`. These last strict inequalities follow already from
`8/3<e<3` and rational powers. With `b=(e_0-e_1)/2>0`, (I40) gives

\[
 {d\mathcal I_{\rm reg}\over du}
       >b(6p-8p^2)=b(14p-8)>0.                       (I41)
\]

The algebraic signs and interval inclusion are exact finite-code
comparisons; this bound does not depend on rounding a logarithmic
derivative. It is the REGISTERED component (I39), with its actual
input subtraction, rather than a substitution of `h_2(q)` for it.

Less accessible conditional DATA/work tests can have a further
quotient; a genuinely allowed joint quantum oldRIGHT comparison can
require a different algebra. Neither is silently added here. All
these choices retain the same coherent full state and actual native
word. The read/seal/storage stages and their actual price must be
included if physically executed.

Write `B_full=H_full+J_full` for this computed full-clock bare Book
functional. If a real source equivalence is to have

\[
 DB_{\rm full}=\kappa D(\ell C_{\rm actual}-\mathcal I),
 \qquad\kappa\ne0\ \text{fixed by a derived physical binding},
\]

then its NECESSARY preparation row is

\[
 \ell DC_{\rm actual}
        =D\mathcal I+\kappa^{-1}DB_{\rm full}.        (I36)
\]

Use the physically justified Info component and all its actual
oldRIGHT restrictions in this equation. The coefficient `kappa` is
not chosen to fit this row. If additional genuine Book/Rayleigh/work
terms are part of the proposed source map, their preparation sources
also remain on the relevant side of (I36). This construction does not
prove that the required equality holds; it has now computed the
previously omitted full-clock term rather than setting it to zero.

## 6. What the actual Cost ledger must supply

`C_actual` denotes the actual complete cost of this execution. Its
ledger includes the historical birth preparation and storage, fresh
blank supply, every current forward/inverse/source-I/CX stage, copy
bank, real padding, clock, readout/seal policy and any actual work or
observer operation. Logical stage count, generator description length,
physical Cost and registered Info are separate quantities until their
binding is established. The fixed-length physical report here has
not been assigned the old unequal `0/10` code charges. In particular
no `1+q` cost or zero cost for a fixed output bit is inferred.

For a fixed implemented experiment with a genuinely specified linear
expected-cost effect `C_eff` on the complete input,
`C_actual(Omega)=Tr(Omega C_eff)`. This may contain coherent pullback
terms; a diagonal report tariff is not its general substitute. With
`ell=log(phi_Golden)` and the reference-retaining component (I6), the
preparation part of `ell C_actual-I_ref` is exactly

\[
 \dot\Omega\longmapsto
    \operatorname{Tr}[\dot\Omega\{\ell C_{\rm eff}-G_\Omega\}],
                                                               (I24)
\]

and field/word variations retain `ell dot C_actual` minus the FIRST
term of (I9). A change of the cost effect adds
`ell Tr(Omega dot C_eff)`. The same formula applies with the properly
reduced `G` when the actual Info convention is `I_act` or another
specified future algebra. No cost effect is manufactured by setting
it equal to `G_Omega/ell`.

Consequently a proposed source equivalence between the CURRENT-WINDOW
bare `H+J` and `C_actual-I_ref/ell` on the preparation orbit (I18)
requires the real cost reaction

\[
 D C_{\rm actual}[\text{prep}]
       ={1\over\ell}D\mathcal I_{\rm ref}[\text{prep}].              (I25)
\]

For a full VALUE or divided-difference binding on finite native alternatives,
the corresponding necessary equality is an equality of actual COST
DIFFERENCES and information differences, not a fictitious smooth gate
derivative. An asymptotic covector binding instead retains its actual
endpoint/stencil/lift error budget and does not imply exact finite values.
If the task fixes other
terms with genuine preparation response, those terms belong on the
same source-equivalence equation; (I25) is not obtained by erasing
them. The present native witness is fair to Cost: its actual paid
inventory is explicit, while the numerical physical price of that
inventory is left to its real owner. A constant common duration does
not prove constant Cost, and a nonconstant inventory does not prove
the particular compensating reaction (I25). The zero-Book-source
version (I25) applies only to that supplied-input window, or after a
separate proof that the additional prefix Book source vanishes.
For the full birth-to-record word, (I32)–(I36) replace it. Keeping the
nonzero historical cost `C_init` in a ledger does not by itself account
for that NONADDITIVE global heat/return source.

For the original fields, an actual word `V` always has the exact
blocks (I1), so (I3), (I6), (I9) and its complete cost pullback can be
evaluated without requiring exact equality to the ideal `U_delta`.
The smooth ideal formula (I11) describes a mathematical comparison
lift. Full-column endpoint convergence gives state/entropy VALUE
convergence at fixed finite dimension. It alone gives no `C1` claim
for a discontinuous catalogue of finite native words. To transfer a
finite-difference covector, the genuine endpoint value-error bound
must be divided by the actual stencil separation and preparation/field
lift norm, exactly as in the operator-holonomy proof. Neither a
numerical derivative check nor a large common clock supplies this
missing estimate or a compulsory physical Info valuation.

Book03 §03.3.0a supplies the Cost-minus-distinguishability framework
([Book03, lines 166–172](../../../../01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md)).
It does not by that statement identify the native `Info(v)` with
(I6), (I8), or a selected full-oldRIGHT entropy, choose the suffix test
policy, or price every present apparatus operation. These are native
hardwired configuration comparisons on a common declared quantum input
boundary. A prospective application inside one autonomous decoder needs
its full stored-program carrier, preparation and physical admission;
changing a hardwired word is not an unpriced key variation there. The original
bootstrap and this valuation must still be bound on ONE execution,
with its independent initial-state, cut, clock and controller rows.
What is now explicit is the actual coherent archive/test decoder, its
conditional quantum entropy source, and the nonzero native preparation
reaction which that binding must consume. No additional Action, task
selector, field constraint, root transplantation or GR closure has
been introduced.
