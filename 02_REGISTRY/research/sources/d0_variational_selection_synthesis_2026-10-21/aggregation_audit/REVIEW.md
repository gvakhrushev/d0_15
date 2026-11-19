# Independent review of the native aggregation witness repair

21 October 2026. Reviewer: Book binding lane, existing PR #334.

**Disposition: accepted in the stated operator-family scope.** The finite
proof supplies a real nonzero complete-record entropy tangent of the
literal original full128 Fourier instrument. It repairs the earlier
conditional-pair witness without varying the Golden constant, replacing
the POVM, conditioning away outcomes, or changing the fixed input. It does
not establish physical controller admission or two complete D0 models.

## 1. Independently checked source and exact derivation

I read the frozen original `creators()` and `native(theta,nu)` functions,
the full new proof and checker, and the old Book amplitude-binding owner.
The exact row table was independently derived from the repeated raw
Julia words before replaying the checker.

For Walsh label `m=2s`, the creation row is `j=4s`. Duplicate words make
odd `m` vanish. The CAR trace calculation gives

\[
 \frac1{16}\operatorname{Tr}(N_{4s}N_{4s}^*)
 =\frac{\nu^2}{256}\sum_r|\zeta_r-\epsilon_s|^2,
 \qquad \epsilon_s=(-1)^{\operatorname{bit}_1(s)}.
\]

The exact phase sums are 10 and 6, giving eight rows of each kind. The
Julia-defect rows survive only at `j=9,13,29,45,61`:
`N_9=(1+b)I/2`, while the four remaining rows are `(1-b)/8` times Walsh
sums of the four occupation involutions. Their normalized trace pairing
is the identity matrix, which proves the stated small-defect norms.
There are therefore 21 nonzero rows and 43 identically zero rows, with
total normalized squared norm one.

At the declared fixed density `I16/16`, cyclicity of trace and the exact
`A^2=(5nu^2/128)I` prove all128 probability formulas in the proof, including
both special `j=0` outcomes. Exactly 42 labels are positive for `0<nu<1`;
the other86 remain present and identically dark. The compact entropy
formula correctly adds `(2-p)r` for the fixed Golden entropy within every
ordinary pair and does not confuse a pair mass with its conditional law.

Every positive probability except the ordinary blank grows for
`0<nu<sqrt(3)/2`. In particular the only nontrivial derivative sign is

\[
 \frac d{d\nu}\log[\nu^2(1+b)^2]
 =\frac{2(2b-1)}{\nu b}>0.
\]

The independent bound `q_00>(59/64)^2>1/2` makes each logarithm in

\[
 H_\varphi'(\nu)
  =\sum_{i\ne(0,0),q_i>0}q_i'(\nu)
                 \log_\varphi(q_{00}/q_i)
\]

strictly positive. This proves the full open-interval sign analytically;
it does not rely on finite differences or a numerical lower bound.

## 2. The historical error and the repaired aggregation implication

The original ordinary-pair operators obey
`K_(0j)=p L_j`, `K_(1j)=sqrt(p) L_j`. Their conditional law is identically
`(p^2,p)`, so its actual derivative is `(0,0)`. The older proposed
`(-1,+1)` tangent violates `q(0|j)-p q(1|j)=0`; its violation is exactly
`-(1+p)`. The former entropy derivative `-1` and half-source `-1/2` are
correct abstract-simplex calculations, but are not original native pair
derivatives. The new proof explicitly records this error rather than
retaining its physical interpretation.

Under the separately assumed strong complete coherent Book binding,
the old owner already proves

\[
 M=\tfrac12H_\varphi(q)-J,\qquad P=-J,
 \qquad D M-D P=\tfrac12D H_\varphi(q).
\]

The new genuine `nu` family makes the last difference nonzero while all
conditional Golden ratios remain fixed. At `nu=1/2`, numerical evaluation
of the exact formulas gives `H_phi'=0.7671427296247743`, hence
`M'-P'=0.38357136481238713`. These displayed decimals are diagnostics;
the strict sign has the exact proof above. The repaired witness is not
the old `-1/2` witness with a new label.

## 3. Narrow independent replay

I independently ran the new checker once against its default frozen
`../inputs`, with the already supplied scientific Python environment.
All100 checks passed; stdout was byte-identical to `RESULT.json`, and
stderr was empty. The replay retained the literal128 indices and the
16-by128 purification. Maximum literal probability/row-norm discrepancy
across the three fixtures was `4.440892098500626e-16`.

The independent five-point derivative changes the actual constructor's
`nu`, including the Julia roots. It does **not** misuse the constructor's
returned `theta` jet. At `nu=1/2` it gave `0.7671427296275511`, differing
from the exact-formula evaluation by `2.7768898291924415e-12`.
The hostile conditional-pair direction is separately rejected.

No previous receipt, proof, source snapshot, integration manifest, or
scientific suite was changed or replayed for this review.

## 4. Physical and logical boundary

The theorem concerns one supplied native operator family on one Fourier
block, with DATA16, all CAR grades, and a fixed purification using16 active
columns inside oldRIGHT128. It does not assert the primary full spatial
DATA128 preparation, a boundary-compatible all42 geometric variation, or
an admitted same-initial-state physical controller/writer.

The entropy is that of the full history-label Born law. It is not the
coherent archive's von Neumann entropy. Computing this Shannon functional
does not perform a measurement, erase the record, or identify it with the
physical Book `Info`. Its role in the aggregate identity is conditional on
the stated amplitude binding.

In particular, two scalar functionals agreeing on normalized Born data do
not by themselves constitute two physically consistent models of all
Book03. The original book specifies an operator stack and its stationarity;
the relation of either proposed aggregate to that whole stack, its full
cost/Info and its physical tangent family remains to be proved. The new
witness establishes non-equivalence of the **conditional aggregate
candidates on an actual supplied execution family**. It does not prove a
global D0 no-go, a unique Einstein source, or GR closure.

## 5. Reviewed artifact and source pins

| Artifact | SHA-256 |
|---|---|
| `PROOF.md` | `fc1e5d0dadb19bf2af71708cdfd201d057fa98b5347f33fa4be89545ecda76e5` |
| `check_native_entropy_tangent.py` | `2c14d8035da073b19d5ea9642be396840c273542d973aee6cbe0b88a8e187667` |
| `RESULT.json` | `aae295ca4fd45455f2dabbaf69dba2159a91de51c21f1abaae8b55f76849585c` |

| Frozen input | Git blob | SHA-256 |
|---|---|---|
| `native_input.py` at the full path recorded by the checker | `ee8de4635d24c668949ac9a0186616ab7d59f2ed` | `1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9` |
| `A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md` | `df8611c7fa37fa71e883831b3f01f434532d99ce` | `2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79` |

The earlier aggregate identity is consumed from `BOOK_SOURCE_BINDING.md`
§3.1, equation (6), SHA-256
`2b26bf2f4c1b128731ccf14a17437ba654c046e82b5e42e55113a8b6053494ea`.
The later corrected normalized-feedback owner remains in force; the old
scalar-rescaled-feedback example is not used here.

`GR_closed=false`.
