# Independent arithmetic, seed and basis review of the exact writer gate

21 October 2026. Existing #334 continuation. Scientific repository input:
`b60a111b`; no repository files changed by this reviewer. This review is
limited to the proposed exact supplied-programme writer and its actual
primary coframe/readout. It does not reject a different transported
weighted-history interface or an independently supplied arithmetic resource.

## 1. Reviewed mathematical statement

Let `p^2+p=1`, `p>0`, `a=sqrt(p)`, and generously enlarge the literal
Golden/Boolean coefficient field to

\[
\mathbb L=\mathbb Q(a,\sqrt2,i).
\]

This includes the literal Q8 phase coefficients and the displayed `sqrt(2)`
constants in the finite AF apparatus frames. Their mathematical existence
does not establish that every AF frame is an independently admitted gate;
enlarging the field only strengthens the arithmetic test.

The tested input contract supplies basis/Golden states, canonical AF trace
seeds, and the actual fixed `L=4` Fourier128 reference. It does not supply an
arbitrary full GNS density, a pre-existing non-`L` boundary programme, or a
continuous amplitude oracle. Every actual primitive Kraus map of the
tested finite writer has entries in `L`; an overall phase may be ignored,
but a branch-dependent scalar of squared modulus outside `L` may not.
This restriction is needed for raw branch probabilities and finite mixed
expectations, not only for projective pure-state ratios. All physical
records, purifiers and unmeasured work remain present.

Under this contract, the exact aggregate programme `Omega(y)` required by
the fixed processor cannot be produced at even one actual primary point.
The obstruction already occurs in one spatial creation block and does not
depend on choosing a transcendental wave profile.

## 2. Independent field proof

Put `F=Q(sqrt(5),sqrt(2))`. The nontrivial `sqrt(5)` automorphism over
`Q(sqrt(2))` sends `p` to `-1/p`; hence

\[
N_{F/\mathbb Q(\sqrt2)}(p)=-1.
\]

In particular `p` is not a square in the totally real field `F`, and every
element of the real field `F(a)` has a unique form `u+a v`, with `u,v in F`.
If its square is a positive rational number `r`, the coefficient of `a`
gives `uv=0`. If `u=0`, taking the displayed relative norm gives

\[
-N(v)^2=r^2,
\]

which is impossible in the real embedding. Thus `sqrt(r)` must lie in
`F`. Its only possible rational squareclasses are `1,2,5,10`, the quadratic
subfields of this biquadratic extension. Adjoining `i` adds no real
elements: `F(a)(i) intersect R=F(a)`.

The original primary count owner gives exactly

\[
\rho_x=\frac{256n_x}{10946}
      =\frac{128n_x}{13\cdot421},\qquad 29\le n_x\le78.
\]

Therefore `v_421(rho_x)=-1`. None of the four squareclasses above has an
odd 421 valuation, so `sqrt(rho_x) notin L`. Multiplication by the genuine
nonzero Golden calibration `s=p^k` cannot change that conclusion.

This argument checks the actual positive field embedding; it does not
confuse an arbitrary quartic conjugate with the physical positive root.

## 3. The forbidden ratio is in the actual orthonormal processor register

The consumed primary dictionary is

\[
V=s\sqrt\rho\,\eta_R(TE_H)^{-T},\qquad
E_H=I+(H/2)E_{10},
\]

where the fixed rational `T` is the identity on spatial coordinates 2,3.
For column `r=2`, independently of `H`,

\[
v_{a2}=-s\sqrt\rho\,\delta_{a2}.
\]

In the actual CAR basis, `c_2^dagger|vac>=|grade-one 2>`. The genuine
full32 Julia matrix also satisfies

\[
J(C_2)|Good,top\rangle=|Bad,top\rangle,
\]

because `C_2|top>=0` and its right defect is exactly the identity on top.
The aggregate Choi programme uses the fixed orthonormal registers
`|address,input-index,output-index>`. The ratio of its coordinate with
input `Good,vac` and output `Good,grade-one 2` to its coordinate with input
`Good,top` and output `Bad,top` is consequently

\[
-s\sqrt{\rho_x}.
\]

The common Choi normalization cancels. Both coordinates belong to the
same address and the full carrier; no discarded grade or postselection
enters. A free interior coframe address suffices. Holding a boundary bank
fixed does not remove this free-address requirement.

## 4. State closure, retained garbage and finite versus unbounded stopping

Finite products, sums, conjugate transposes and computational projections
preserve `L`. For an unnormalized density matrix over `L`, a positive
conditional probability is its trace in `L`; dividing by that trace stays
in `L`. Thus every normalized conditional density of a finite tree has
entries in `L`, as does every finite aggregate of its outcomes.

This formulation handles both pure seeds specified projectively over `L`
and canonical mixed AF trace seeds. An accepted pure vector may acquire a
normalizing square root outside `L`, but all its projective ratios and its
density entries remain in `L`; it does not supply a new relative amplitude.

If the reduced programme is the prescribed pure `Omega`, positivity
forces each accepted component of any mixture to have that same rank-one
support. Equivalently, a full pure output has form `Omega tensor eta`.
Fixing any nonzero coordinate of the retained `eta` leaves the forbidden
programme ratio unchanged. Retained unmeasured garbage therefore does not
evade the pure-output obstruction.

The pure-output conclusion also applies to almost-surely finite unbounded
halting: each positive finite successful leaf would already have to give
the same pure programme. A nonzero success event has at least one such
positive leaf. Infinite coherent limits with no finite successful output
are a different interface.

For **bounded-cap or finite-tree** writers there is a stronger immediate
consumer. The fixed Hermitian signed swap of the old creation probe has
entries in `L`; its expectation on a generated conditional density must
lie in `L intersect R`. The desired mean is precisely `-s sqrt(rho_x)`.
Thus even a mixed-state replacement preserving this actual probe mean
fails the finite-tree test. This last mixed-moment claim is not extended
to arbitrary countable halting mixtures: infinite sums of finite-leaf
probabilities need not remain in `L`.

## 5. Existing AF and Fourier inputs do not supply the missing square root

The canonical AF cyclic vector is sometimes displayed as
`sqrt(u) vec(I_d)/sqrt(d)` with `u=d p^(n+1)`. In the actual normalized
matrix-unit basis these factors cancel, leaving each nonzero coordinate
`p^((n+1)/2)`; the other block has `p^((n+2)/2)`. Apparent square roots of
path counts are not independent native amplitudes. The canonical defining
trace density also has entries in `Q(p)`. The much larger full-GNS state
fibre is not a selected preparation; arbitrary points of that fibre would
be additional supplied inputs.

For the actual `L=4` reference, the owner uses

\[
\chi=\frac1{\sqrt{128}}\sqrt{\frac2{256}}
 (\cos(\pi k\cdot x/2),\sin(\pi k\cdot x/2)).
\]

Its entries are exactly `0,+1/128,-1/128`. It supplies no 421 square root.
The actual Fourier pair list is retained, including zero intersite
overlaps; no favourable replacement list is used.

There is a constructive positive seed behind this observation: prepare
eight fair site bits and six fair pair-index bits with the paid factories,
compute the actual pair's `k dot x mod 4`, copy its parity into the seventh
RIGHT bit, apply sign `(-1)^floor((k dot x mod 4)/2)`, then uncompute the
lookup work. The four phase cases are exactly the original cosine/sine
columns. Tensoring the literal Golden CAR state
`a|mask1>+p|mask14>` gives the complete normalized vacuum preparation with
Gram `I128/128`. Every conditional factory-completing branch has that
same output, while failures and all factory costs remain in its full
record. This positive construction does not prepare a moving nonvacuum
field, make the preparation HJR-stationary, or supply the missing programme.

## 6. Weighted coordinates and the fixed-boundary exception

The primary Julia block is written after the specified positive-Hilbert
normalization. Its `sqrt(rho)` is in the local creation coefficient.
A common change of site normalization multiplies both the local input
and local output basis by the same factor and does not remove it. A
grade-dependent nonorthonormal coordinate change can move the factor into
the Gram or other matrices, but a faithful transport also moves the seed,
every gate and the signed-swap observable. It cannot preserve the stated
fixed processor interface while deleting the forbidden physical mean.

Likewise, grouping actual AF leaves into a site gives a classical mass
proportional to its count. The normalized equal-leaf vector inside that
site has its own count-dependent coordinates. Relabelling that vector as
one computational basis state is not a paid coherent compression into the
fixed programme register. Ignoring its retained leaf information is not a
construction of the required pure programme.

A genuinely supplied boundary programme with amplitudes outside `L`
would enlarge the initial resource field. The theorem does not rule out
using that resource, consuming it, or obtaining an additional operation
from it. Its actual common-history preparation is then a separate unpaid
input premise. A boundary pool genuinely prepared from the same declared
seeds and finite palette satisfies the same arithmetic gate. Neither
holding boundary values fixed during variation nor renaming the pool
classical manufactures the missing coherent resource.

This is a rejection of the exact fixed-readout writer from the stated
seeds. A different weighted-history representation with fully transported
seed, gates, observable and price remains a separate possible route.

## 7. Historical source pins

The following were independently read and verified with `git show b60a111b:<path>`.
Paths are relative to the repository root.

| Source | SHA256 |
|---|---|
| `02_REGISTRY/research/sources/d0_primary_native_domain_source_2026-10-20/check_primary_domain_source.py` | `c67285c7469db49ff61f3e52597d0bcc6aad991ec1f7af025d6daeb065a43edf` |
| `02_REGISTRY/research/sources/d0_causal_native_weighted_synthesis_2026-10-21/native_source/NATIVE_POLYNOMIAL_FIRST_JET.md` | `4d098d1e6ad8cb7daf477b498f808b7b962d6432f3da78ae573e321dbbcb915d` |
| `02_REGISTRY/research/sources/d0_common_execution_closure_2026-10-21/native_processor/FIXED_PROCESSOR_PROGRAM_SOURCE.md` | `4a879a3bb986aca43f06cec760f882cec4e7c6446efd46d5add8a2f199e9381b` |
| `02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md` | `9c7e4d582d5627bf5b926a6f8ad15743ff473e9bcc22e741c42309dabb854299` |
| `02_REGISTRY/research/A4D_NATIVE_Q8_AF_SPINOR_RECORD_SEED.md` | `bca4dfa9dc26fb0599ce341f1f33ff003add4104c61848374f4a0eddd3707411` |
| `02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py` | `9a016fa4b1a8261a29f626ed7450db7987727957e634799519aede0e3ab587ee` |
| `02_REGISTRY/research/A4D_NATIVE_REFERENCE_MEMORY_PREPARATION.md` | `04d38a6a126830fa857f4f7a06bf74789f21e283ed540d676ba8ea1de50e9184` |

No old geometry, preparation-root, rank, spectrum or factory suite was
rerun for this arithmetic and representation review.

## 8. Frozen writer packet and independent optimized replay

**Analytical review: PASS within the stated input and palette contract.**
The final proof was read in full, including the exact one-particle
`mask4` typing, the raw Kraus-field hypothesis, the fixed-boundary input
exception and the finite-mixture versus almost-surely finite pure-output
distinction. Its positive-support classical entropy estimate in section 7
follows directly from the displayed derivative bound. It is correctly
restricted to the same finite support and pure conditional complete work;
new dark outcomes or mixed conditional work need separate control.

One independent optimized execution was performed:

```text
python3 -O writer_native/check_exact_native_writer_gate.py \
  --repo /workspace/scratch/07af0e1491e7/d0_15 \
  --output /workspace/scratch/07af0e1491e7/writer_preparation/WRITER_INDEPENDENT_RESULT.json
```

It returned PASS and reproduced the author's receipt byte for byte.
The replay verified 15 historical source pins, the actual 256 PF counts,
all actual 256-by-128 integer Fourier entries and their Gram, and the
creation-on-vacuum/top mechanism. The number-field classification and
full-history conclusions were checked analytically; the checker does not
claim to enumerate all native writers.

| Frozen writer item | SHA256 |
|---|---|
| `writer_native/EXACT_NATIVE_WRITER_GATE.md` | `672524e7a56e25675fda6cf295acc258877729f1a4d69bf0a52d4e1425884dcc` |
| `writer_native/check_exact_native_writer_gate.py` | `9db3e6226d1e16b23295e2643931b62650db96c6924bf58ca41e8517b3cf3ac8` |
| `writer_native/WRITER_SOURCE_PINS.json` | `08f1b362bae8d0cf11fa4ff21d02ef349b25139504eac71b4b8a6ce258c38ad7` |
| `writer_preparation/WRITER_INDEPENDENT_RESULT.json` | `5bf9932e0be30cf9ae7e5e474364053685fc183158a9b123b10373e46c5076ca` |

## 9. Independent review of the accompanying Book operator application

**Analytical review: PASS with its stated complete-writer and cut scope.**
I independently read `writer_book/FIXED_PROCESSOR_BOOK_OPERATOR.md` and
its entire exact checker. Equations (1)--(13) are valid with the declared
fixed dimensions, embeddings and retained registers. Their implications
are narrower than an identification of the processor's CQ price with the
original Book action.

### Actual fixed cost schedule

The crucial historical input is not just a state-independent mean cost.
The consumed processor owner, section 6 around its equation (18), says
that each full factory tape `t_F` has a state-independent law, and its
charged cost `c(t_F)` is independent of all address, Bell and report
values. Controlled locations are charged even at zero control. All
attempts execute, and previously read permutation labels survive a later
factory abort. Thus the complete fine block has effect `w_f I`, which
proves

\[
 V_t^*V_t=\sum_f e^{-tc_f}V_f^*V_f
        =\Bigl(\sum_f w_f e^{-tc_f}\Bigr)I.
\]

This proves every cost-moment statement in (3) on the full supplied input
carrier. It does not include an unknown writer price. A conditional
processor acting on a writer success/failure flag inherits this scalar
marked normalizer only if it retains this same charged schedule and
input-independent factory-effect property across those statuses. An
arbitrary fixed isometry with status-dependent skipped costs would not
suffice. The range identity below applies to any genuinely fixed
isometry after that requirement has been met; it does not assert the
marked property for an arbitrary new conditional engine.
The final section 3 now makes this requirement explicit and gives the
correct nonscalar expression
`V_t T (T* N_(V,t) T)^(-1) T* V_t*` when it fails. I read and accepted
that final clarification. At `t=0` any fixed complete isometry suffices.

### Range transport and dimensions

With `T:H->K` injective, `Vhat:K->E` isometric and `i:H->E` isometric,
`W=Vhat T` has Gram `T* T`. Therefore

\[
 \Pi_W=\widehat V\Pi_T\widehat V^*,\qquad
 D\Pi_W=\widehat V(D\Pi_T)\widehat V^*.
\]

The raw normalized determinant from
`(1-z) T*T + z (i*W)*(i*W)` divided by `det(T*T)` equals the determinant
of `(1-z)I_H+z i*Pi_W i` by the square-matrix Sylvester identity. This
justifies the range form and its derivative (6); it does not equate the
two unnormalized matrices entry by entry. The inverse exists for
`0<z<1`, and reference multiplicity must be counted only once.

For the rank-one case `H=C`, the normalized writer is `T(1)=C`,
`i(1)` is an actual vector of `E`, and `b=Vhat* i(1)` belongs to `K`.
It may have norm less than one; equation (7) needs no assumption that
it is a normalized state. Right-coordinate variations `DT=T X` leave
the range projector fixed. Mark, hardware, active-cut or writer-range
variations remain separate real terms. In particular scalar `N_t`
does not imply that the marked output range is independent of `t`.

### Retained Bell registers and the normal direction

For the explicitly specified logical Bell block, Pauli completeness gives
`V_S* V_S=I` from `sum_a Tr(S_a* S_a)=A d`. In the initialized-input cut,
the zero new-record overlap forces the old address and both Bell output
registers to zero. Contracting the remaining programme with its own bra
gives exactly

\[
 i_S^*V_S=\frac{|0\rangle\langle0|G_0}{A d^{3/2}},
 \qquad G_0=S_0^*S_0.
\]

Its one possible nonzero squared singular value is
`<0|G_0^2|0>/(A^2 d^3)`, proving (12). On the unitary section `G_0=I`,
every proper-unitary field jet vanishes only after both the operation
and moving-cut derivatives are included. For the compensated normalized
curve at two addresses, `DG_0=|0><0|`, so the derivative (13) is strictly
negative. The sign and the factor two are correct. The proof explicitly
does not carry this logical-block corner through all paid factories,
identify it with the compulsory Book cut, or suppress real heat, matter
and writer contributions. A retained extra programme purifier merely
enlarges the output index of `S_a`; the same contractions still use
`S_a* S_a`.

One optimized replay of `check_writer_book_operator.py --repo ...` passed
all 46 explicit checks, including 8 historical pins. Its exact small
fixtures independently contract the Bell registers, compare raw and range
normalizers and derivatives, retain a nonzero normal source, and show a
varying marked range despite a scalar Gram. Its output in
`writer_preparation/BOOK_INDEPENDENT_RESULT.json` was byte-identical to
the author's receipt before the final section 3 clarification. That
independent receipt is retained unchanged and pins the earlier proof
`e58cb50cbcb7499f149b6243450a811270d09363aaa6698db6f224b5efa7cc25`.
The final author's receipt below differs only in its `proof_sha256` field;
checker, historical pins and all 46 mathematical checks are identical.
The final text was reviewed directly without rerunning the unchanged
checker. The general `d=32` statement rests on the displayed
all-dimensional algebra, not on extrapolating these fixtures.

| Frozen Book item | SHA256 |
|---|---|
| `writer_book/FIXED_PROCESSOR_BOOK_OPERATOR.md` | `cebf19d44d3ea3f8bb6bef1f9f6a2d98d01f7496ba908ba3f38f0b500875fd83` |
| `writer_book/check_writer_book_operator.py` | `bd832ee4599604f2d4099c95b64c1d18051e0e2b64471d88ae3b2643f190a257` |
| `writer_book/SOURCE_PINS.json` | `d4bb28a6c6ab67db2cb4831d2eeeb420d3fc3128b0c3e953d199dc76025a220c` |
| `writer_preparation/BOOK_INDEPENDENT_RESULT.json` | `301ae80999b21022c11606fd7bc688866f82b406278e7ce5e412d762d72a1902` |
| `writer_book/RESULT.json` (final proof metadata) | `87a66e020d5f13e46e7ef7c772aaefbb8a27a7457351ce059e35595fc34f77c4` |

These two reviewed applications neither generate the missing moving
programme/material writer nor remove the already established nonzero
inherited primary HJR preparation row. They provide an exact rejection of
one specified writer and an exact operator consumer for any real complete
writer subsequently supplied. The fixed vacuum-prefix construction is
positive but has precisely the narrower scope stated in section 5.
