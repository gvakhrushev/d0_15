# Вещественная оболочка эрмитовых матриц

Статус: кандидат. Скептик не запускался. Ниже описана Lean-теорема в обе стороны, не строка реестра и не физический вывод. Заметка контура: `CANDIDATE_NOTE.md`.

Модуль `D0.Research.MemoryTangentSpan` фиксирует конечномерную алгебраическую лемму. Для эрмитовых матриц одного фиксированного размера условие `Tr(S M) = 0` для всякой допустимой бесследовой источнико-нейтральной матрицы `S` равносильно принадлежности `M` вещественной оболочке `{I, J₁, J₂, J₃}`.

Допустимая `S` эрмитова, `Tr S = 0` и `Tr(S J_r) = 0` для каждого из трёх фиксированных `J_r`. Коэффициенты оболочки лежат в `ℝ`. Линейная независимость четвёрки `{I, J₁, J₂, J₃}` не предполагается, поэтому вырожденная тройка имеет ту же эквивалентность. Спаривание — вещественная часть следа; на паре эрмитовых матриц она совпадает со следом. Для эрмитовой `A` равенство `Tr(A A) = 0` влечёт `A = 0`: след равен сумме квадратов модулей элементов.

`J_r` — данные модуля. В меморандуме это источники `B_r`, не новый оператор и не CAR-представление. Индекс размера фиксирован для всего утверждения. Остаток через обратную матрицу Грама не строится. Лучевое равенство `M χ = λ χ + Σ β_r J_r χ` слабее оболочки и не является доказанной теоремой.

Полевое ядро, кривизна и физический оператор не строятся. Это кандидатная конечная лемма. Она не утверждает вывод ОТО и не выпускает новый claim.

## Источник и потребитель

Чтение через `git show`, pin `ec45c8cc4085e7bce888d97439251be9e578d4ff`, файл `02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md`, §6. Оттуда взято условие (26): `M_v` лежит в `span_ℝ {I₁₆, B₁, B₂, B₃}`. Формула остатка (27) в меморандуме использует невырожденную `G_B`; модуль доказывает принадлежность оболочке без этого предположения. Условие (28) — луч на одном векторе — в модуль входит только как отдельный отрицательный контроль. Пакет на том же pin: `02_REGISTRY/research/sources/d0_memory_rank_continuation_2026-10-16`. Общий источник не изменялся.

Потребитель — PR #334. PR #334 не сливается.

## Теоремы

В файле нет `sorry`. Узкая сборка напечатала аксиомы. `sorryAx` в печати нет.

- `admissible_trace_vanishes_of_memRealSpan`: вещественная комбинация ортогональна всякой допустимой `S`.
- `memRealSpan_of_admissible_trace_vanishes`: обращение. Если эрмитова `M` ортогональна всякой допустимой `S`, то `M` лежит в вещественной оболочке. Четыре формы `S ↦ Re Tr(S · source_i)` порождают форму спаривания с `M` по `mem_span_of_iInf_ker_le_ker`; остаток ортогонален всем эрмитовым матрицам и потому нулевой.
- `trace_vanishes_iff_memRealSpan`: эквивалентность двух направлений при эрмитовых `J₁, J₂, J₃, M`.

## Отрицательные и положительные контроли

Все примеры доказаны в том же модуле на `Fin 2`. Матрицы координатные и не являются полевыми операторами. `pauliX = [[0, 1], [1, 0]]`, `pauliZ = [[1, 0], [0, -1]]`, `halfShift = [[1/2, 0], [0, -1/2]]`, `chi2 = (1, 0)`.

1. Положительный контроль. `pauliZ_isAdmissibleTangent`: `Z` допустима для источников `(X, 0, 0)`. `eye_add_pauliX_memRealSpan`: `I + X` лежит в `span_ℝ {I, X, 0, 0}`. `pauliZ_kills_eye_add_pauliX`: допустимое направление `Z` убивает `I + X`.

2. Бесследовость не даёт допустимости. `pauliX_not_admissible_to_itself`: `Tr(X X) = 2`, поэтому `X` не допустима относительно самой себя.

3. Допустимость относительно нулевой тройки не даёт оболочку. `halfShift_trace_test_fails`: `halfShift` допустима для `(0, 0, 0)`, и `Tr(halfShift²) = 1/2 ≠ 0`. `halfShift_not_memRealSpan`: `halfShift` не лежит в `span_ℝ {I, 0, 0, 0}`.

4. Луч не заменяет оболочку. `halfShift_mulVec_chi`: `halfShift *ᵥ χ = (1/2) χ`. `ray_member_not_memRealSpan`: при нулевых источниках лучевое равенство выполнено, а принадлежность вещественной оболочке ложна.

## Печать аксиом

Команда в каталоге `03_FORMALIZATION`:

`~/.elan/bin/lake build D0.Research.MemoryTangentSpan`

Сборка завершилась успешно. `sorryAx` нет. Для каждой перечисленной теоремы список один и тот же: `propext`, `Classical.choice`, `Quot.sound`.

```
'D0.Research.MemoryTangentSpan.trace_vanishes_iff_memRealSpan' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.MemoryTangentSpan.admissible_trace_vanishes_of_memRealSpan' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.MemoryTangentSpan.memRealSpan_of_admissible_trace_vanishes' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.MemoryTangentSpan.pauliZ_isAdmissibleTangent' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.MemoryTangentSpan.eye_add_pauliX_memRealSpan' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.MemoryTangentSpan.pauliZ_kills_eye_add_pauliX' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.MemoryTangentSpan.pauliX_not_admissible_to_itself' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.MemoryTangentSpan.halfShift_trace_test_fails' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.MemoryTangentSpan.halfShift_not_memRealSpan' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.MemoryTangentSpan.halfShift_mulVec_chi' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.MemoryTangentSpan.ray_member_not_memRealSpan' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (2949 jobs).
EXIT:0
```

## Команды

| Команда | Результат |
| --- | --- |
| `~/.elan/bin/lake build D0.Research.MemoryTangentSpan` в `03_FORMALIZATION` | `Build completed successfully (2949 jobs).` `EXIT:0` |
| `python3 tools/validate_repo.py` | `ERROR orphan Lean modules outside registry/support closure: D0/Research/MemoryTangentSpan.lean` `FAIL errors=1` |

Цель `D0.All` не собиралась. Каталог `.lake` не удалялся и Mathlib не пересобирался.

## Строка formal_support

Строка ниже записана здесь для CONTROL. В `02_REGISTRY/formal_support.csv` она не вставлена. `03_FORMALIZATION/D0/All.lean` не правился. `ClaimMap` не правился.

```
D0.Research.MemoryTangentSpan,D0/Research/MemoryTangentSpan.lean,EXPLICIT_SUPPORT,02_REGISTRY/research/sources/d0_rank_lean_mv_span_2026-10-16/RESULT_RU.md
```

## Повторная сборка

Повтор в этом worktree, собственный каталог `03_FORMALIZATION/.lake`, переменная `LAKE_HOME` не задана, pin Mathlib `6988106320cbae4bcbd5d142075946f7fe08a7b7`. Main не вливался.

`~/.elan/bin/lake build D0.Research.MemoryTangentSpan`

`Build completed successfully (2949 jobs).` Печать аксиом iff, каждого направления и контролей на `Fin 2` снова равна `propext`, `Classical.choice`, `Quot.sound`. `sorryAx` нет. В файле нет `sorry`.

Оба направления лежат в тексте: `admissible_trace_vanishes_of_memRealSpan` и `memRealSpan_of_admissible_trace_vanishes`. Второе требует эрмитовости `J₁, J₂, J₃, M`. Без неё остаётся только первое направление, и его нельзя называть эквивалентностью. Эквивалентность не заявляет `matter_source_ward` и не отождествляет тензоры источника и геометрии.

## Блокер

Единственный оставшийся шаг принадлежит CONTROL: внести строку в `formal_support.csv` и пересобрать `All.lean` генератором. До этой регистрации `validate_repo.py` сообщает сиротский модуль, и перевод PR в Ready ломает проверки orphan/closure. PR #353 остаётся Draft, задача остаётся `IN_PROGRESS`. `task_lifecycle.py retire` не запускался. `gh pr ready` не запускался. Конечная лемма не даёт физического допуска и не закрывает ОТО.
