# Hermitian real-span trace test — algebraic iff (DRAFT, pre-skeptic)

**Status:** DRAFT candidate. No registry row edited. Skeptic pass was not run, so this note does not accept the statement. Pre-flight keywords: `MemoryTangentSpan`, `mv_tangent_span`, `traceless source-neutral`, `span_R`. No owning row in `02_REGISTRY/claims.csv` or `02_REGISTRY/formal_support.csv`. `03_FORMALIZATION/D0/All.lean` does not import the module. Skill paths `03_THEORY_MAP/`, `09_LEAN_FORMALIZATION/`, and `05_CERTS/` are absent in this repository; the registry files above were searched instead.

## Claim (DEF-0.2.2 form)

Let `n` be a fixed finite index. Let `J₁, J₂, J₃, M` be Hermitian matrices of that size. Write `S` admissible when `S` is Hermitian, `Tr S = 0`, and `Tr(S J_r) = 0` for each of the three matrices. Then `Tr(S M) = 0` for every admissible `S` if and only if `M` is an `ℝ`-linear combination of `{I, J₁, J₂, J₃}`.

Lean name, both directions: `D0.Research.MemoryTangentSpan.trace_vanishes_iff_memRealSpan`.

Span-implies-trace: `admissible_trace_vanishes_of_memRealSpan`. Trace-implies-span: `memRealSpan_of_admissible_trace_vanishes`. The second direction uses the Hermitian hypotheses. Without them only the first direction is stated.

No physical operator is selected. This note does not claim `matter_source_ward`, does not set `T` equal to `G`, and does not identify a gravitational equation.

## Owned pre-facts (verbatim)

Pin `ec45c8cc4085e7bce888d97439251be9e578d4ff`, file `02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md`.

Lines 242–244:

> Внутри sigma>0 любой Hermitian S с `Tr S=0`, `Tr(S B_r)=0` является допустимой касательной стационарной фибры. Следовательно из (23) необходимо
>
>     M_v in span_R{I16,B1,B2,B3}.                              (26)

Lines 246–251, through the qualifying sentence after (27):

> Не требуется перебрать все252 вариации вручную. Если G_B,rs=Tr(B_rB_s), то полный тест — один остаток
>
>     M_perp=M_v-Tr(M_v)I16/16
>              -sum_r B_r [G_B^-1 (Tr(B_s M_v))_s]_r = 0.      (27)
>
> G_B невырождена по первоначальному source-owner. Это квадратичное условие на полевую скорость v. Оно намного сильнее единственного равенства H_rho(v,v)=0 и дополняет, а не заменяет, H_rho(v,w)=0 для всех w. Условие необходимо даже если размерность/число отрицательных eigenvalues полевого блока изменилось при вариации подготовки.

Lines 255–262:

> На rank8-конце internal sigma=|chi><chi|. Поскольку Gamma>0, три source constraints имеют независимые реальные градиенты в pure-state space около chi. Тогда stationarity по pure stationary memory fibre даёт необходимое условие
>
>     M_v chi=lambda chi+sum_r beta_r B_r chi,
>     lambda,beta_r in R.                                     (28)
>
> Проекция должна быть на **вещественный** tangent/cotangent space. Комплексная линейная оболочка без проверки реальности коэффициентов может пропустить условие.
>
> Различие (26) и (28) существенное. Оператор `M=|chi><chi|-I/16` нарушает (26) (его спаривание с тем же trace/source-neutral S равно15/16), но удовлетворяет (28). Значит, понижение ранга действительно может снять конкретный nonlinear obstruction; оно не только уменьшает число неизвестных. Это algebraic control различия условий, не заявление, что именно такой M_v уже реализован native field velocity.

The paragraph through line 264 continues that (26)–(28) are there to avoid treating the memory coordinate as an external parameter. It does not supply a proof of the span equivalence, and it does not choose a physical operator.

Module statements, `03_FORMALIZATION/D0/Research/MemoryTangentSpan.lean`:

- Lines 54–56: membership is `∃ c : Fin 4 → ℝ`.
- Lines 62–67: admissible means Hermitian, trace zero, and three complex traces `(S * J_r).trace = 0`.
- Lines 202–209: real combination implies `(S * M).trace = 0`, with no Hermitian hypothesis on `J_r` or `M`.
- Lines 212–216: the converse assumes `J₁, J₂, J₃, M` Hermitian.
- Lines 271–276: the iff is exactly those two directions under the Hermitian hypotheses.

## The argument (what the Lean text checks)

The easy direction expands `M = ∑ c_i • source_i` and uses admissibility on each of `I, J₁, J₂, J₃`. Real scaling preserves the zero trace. Linear independence is not used.

The converse restricts the real trace pairing to the real vector space of Hermitian matrices. The four forms `S ↦ Re Tr(S · source_i)` have a common kernel contained in the kernel of `S ↦ Re Tr(S · M)`, by the hypothesis that every admissible `S` has `Tr(S M) = 0` and by equality of that trace with its real part on Hermitian arguments. Mathlib's `mem_span_of_iInf_ker_le_ker` (`Mathlib/LinearAlgebra/Dual/Lemmas.lean` at this pin, finite index, not a basis hypothesis) puts the pairing with `M` in the real span of the four forms. The matrix remainder is then orthogonal to every Hermitian matrix, including itself. For Hermitian `R`, `Tr(R R)` is the sum of squared moduli of the entries, so it vanishes only at `R = 0`.

Coefficients are read from that dual membership. They are not built by assuming the matrix decomposition in advance. The Gram inverse in (27) is not constructed. A degenerate triple still falls under the same iff, because independence is not a hypothesis. That is wider than (27), which names `G_B⁻¹`.

## Verification

Independent `Fin 2` arithmetic, not read off the Lean proof terms. `I`, `X = [[0,1],[1,0]]`, `Z = [[1,0],[0,-1]]`, `H = diag(1/2,-1/2)`, `χ = (1,0)`.

- `Tr Z = 0`, `Tr(ZX) = 0`, `Tr(Z(I+X)) = 0`.
- `Tr(XX) = 2`, so traceless `X` is not source-neutral to itself.
- `Tr H = 0`, `Tr(HH) = 1/2`. Against the zero triple, `H` passes the admissible trace tests and fails orthogonality to itself, so it is not in `span_ℝ {I}`.
- `H χ = (1/2) χ`, while the two diagonal entries of `H` differ, so the ray equality does not give span membership.

These controls can fail the conclusion (span membership, or admissibility) rather than only a side lemma.

Rebuild in this worktree, own `.lake` directory, `LAKE_HOME` unset, Mathlib pin `6988106320cbae4bcbd5d142075946f7fe08a7b7`, no merge of main:

`~/.elan/bin/lake build D0.Research.MemoryTangentSpan`

`Build completed successfully (2949 jobs).` The printed axioms of the iff, of each direction, and of the `Fin 2` controls are `propext`, `Classical.choice`, `Quot.sound`. `sorryAx` is absent. The file contains no `sorry`.

## Named risks and pre-registered attack surface

Strongest self-attack: memorandum (26) is a necessity claim inside `sigma>0`, using (23) and (25) and the identification of stationary-fibre tangents with those Hermitian tests. The Lean iff is only the linear-algebra step on an abstract Hermitian triple. It does not prove (26) for `M_v`, does not touch `ker H`, and does not own the memory fibre. Calling the module a proof of (26) is a carrier/programme mismatch.

Second attack: interface text "finite real matrix space" can be read as `Matrix n n ℝ` rather than the real space of Hermitian matrices. The MV brief at lines 242–244 specifies Hermitian `S` and ordinary `Tr`. This note claims the Hermitian statement only. A symmetric-real theorem was not added.

Third attack: (27) is not the iff. It needs the inverse of `G_B`. The module never forms that inverse. A degenerate source triple still has the span iff and does not have (27).

Fourth attack: (28) is strictly weaker. The `Fin 2` ray control separates them. The brief's operator `|chi><chi| - I/16` and the number `15/16` are not re-checked here.

Fifth attack: drop the Hermitian hypotheses and only `admissible_trace_vanishes_of_memRealSpan` remains. That one direction must not be called the equivalence.

Sixth attack: line 260 warns that a complex-linear combination can miss the real tangent condition. Membership in the module is quantified over `ℝ`. There is no separate example whose only coefficients are non-real.

Seventh attack: `n` is generic. The theorem does not instantiate `I₁₆` or the memorandum's `B_r`, and it does not count the 252 variations.

Eighth attack: `Classical.choice` enters through the dual-span lemma. It is not a new axiom and not `sorryAx`. The proof is not claimed to be constructive.

Ninth attack: the `Fin 2` controls are witnesses, not a scan of all matrices. The universal statement is the generic proof. Two examples would not by themselves be an iff.

## What this does not show

It does not show memorandum (26) for a field velocity. It does not show (27) or that (28) implies the span. It does not select an action, a physical operator, or a source Ward. It does not set a stress tensor equal to any geometric tensor. It does not wire `D0.All` and it does not insert `formal_support.csv`. Until a skeptic pass is run, the status remains candidate.
