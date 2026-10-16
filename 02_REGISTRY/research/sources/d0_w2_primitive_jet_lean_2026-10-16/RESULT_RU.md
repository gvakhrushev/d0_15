# Упорядоченная композиция примитивного слова и его первый джет

Модуль `D0.Research.PrimitiveJetComposition` фиксирует одно общее тождество для конечного слова в кольце. Голова списка — левый фактор, так что `List.prod` даёт `V_{a_m} ⋯ V_{a_1}`. Для слова `w` остаток `V_w I - I U_w` равен сумме одношаговых остатков: слева стоит произведение предшествующих `V`, справа — произведение последующих `U`. Пустые произведения равны `1`. Слагаемые сложения коммутируют, порядок букв внутри каждого слагаемого сохраняется и совпадает с формулой (B).

Первый джет — пара `(value, derivative)`. Умножение задано правилом

```text
(x * y).deriv = x.deriv * y.val + x.val * y.deriv.
```

Производная одношагового остатка есть `dV I + V dI - dI U - I dU`. Слагаемое `V dI - dI U` входит в тождество и в оценку. Заморозка `dI` определена отдельно и в отрицательном контроле даёт другой результат.

При `‖V‖ ≤ 1`, `‖U‖ ≤ 1` и поставленных `‖R_a‖ ≤ ε`, `‖dR_a‖ ≤ δ`, `‖dV‖ ≤ M`, `‖dU‖ ≤ M`, `0 ≤ M`, `0 ≤ ε` для слова длины `m` доказаны границы

```text
‖R_w‖ ≤ m ε
‖dR_w‖ ≤ m δ + m (m - 1) M ε.
```

Согласование меток, подготовок и тестов ветвления — отдельная гипотеза. Исчезновение остатка слова не нормализует postselection и не раскладывает сумму помеченных остатков на каждый ярлык. Модуль содержит одну общую теорему, а не каталог программ. Физический допуск примитива v8 остаётся у ведущего и у N10.

Это условная операторная лемма. Она не утверждает вывод ОТО и не выпускает новый claim.

## Источник и уже имеющиеся теоремы

Научный SOURCE, только чтение: `74e62cdc716e10883accba9d34ccf0e21d58eb65`. Формулы (B)–(D) взяты из `02_REGISTRY/research/A4D_FOUNDATION_FORCING_NOT_CATALOGUE_SEARCH.md`, §6 и §6.1. Транспортный вход `A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md`, §0.3, задаёт уже построенные условные v8-отображения; этот модуль их не передоказывает и не допускает.

`D0.Foundation.EmpiricalTheoryFactorization.empiricalProcess_composition` и `process_respects_equivalence` переносят наблюдательную эквивалентность вдоль составного процесса. `D0.Geometry.A4DUnlabelledCenterHolonomyNoGo.chainTransport_telescopes` сворачивает концевой транспорт. Ни одна из этих теорем не раскрывает остаток `V_w I - I U_w`. Они не импортируются: их зависимости тяжелее узкой сборки. Новое утверждение — упорядоченная сумма остатков и её первый джет.

PR #334 не сливается.

## Теоремы

В файле нет `sorry`. Узкая сборка напечатала аксиомы. `sorryAx` в печати нет.

- `wordResidual_eq_orderedSum`: для всякого конечного слова `V_w I - I U_w` равно упорядоченной сумме одношаговых остатков.
- `jet_wordResidual_eq_orderedSum`: то же равенство в кольце джетов, поэтому `dI` сохраняется правилом произведения.
- `stepResidual_deriv`: производная шага есть `dV I + V dI - (dI U + I dU)`.
- `stepResidual_deriv_eq_frozen_add_dI`: замороженная формула `dV I - I dU` отличается от полной производной ровно на `V dI - dI U`.
- `word_intertwining_of_steps`: из `V_a I = I U_a` на каждом шаге слова следует `V_w I = I U_w`.
- `branched_program_requires_agreement`: ветвящееся чтение требует это тождество и отдельно `labelsAgree`, `preparationsAgree`, `testsAgree`.
- `word_residual_does_not_force_branch`: нулевой остаток пустого слова не даёт согласия приборов и не нормализует postselection.
- `exact_step_does_not_normalize_postselection`: точный одношаговый перенос тождества не нормализует postselection.
- `wordResidual_norm_le`: `‖R_w‖ ≤ m ε` при сжатии и одношаговой границе `ε`.
- `jet_wordDeriv_norm_le`: `‖dR_w‖ ≤ m δ + m (m - 1) M ε`.
- `sample_factors_do_not_commute`, `sample_ordered_residual`: некоммутирующие матрицы `2×2` и конкретное значение упорядоченного остатка.
- `reversed_order_fails`: сумма с обратным порядком факторов не равна остатку слова.
- `kept_dI_value`, `frozen_dI_is_zero`, `frozen_dI_fails`: движущийся `dI` сохраняется, замороженный даёт нуль.
- `branch_sum_does_not_give_each_label`: сумма двух противоположных помеченных остатков равна нулю, и ни один ярлык не равен нулю.

## Отрицательные и положительные контроли

Все примеры доказаны в том же модуле на `Matrix (Fin 2) (Fin 2) ℝ`.

`e01 = !![0, 1; 0, 0]`, `e10 = !![0, 0; 1, 0]`, `e00 = !![1, 0; 0, 0]`, `sampleI = !![1, 0; 0, 2]`. Слово есть `[⟨e01, e10⟩, ⟨e10, e00⟩]`.

1. Некоммутативность. `sample_factors_do_not_commute`: `e01 * e10 ≠ e10 * e01`. `sample_ordered_residual`: и остаток слова, и упорядоченная сумма равны `!![1, 0; -2, 0]`.

2. Обратный порядок. `reversed_order_fails`: сумма, в которой суффикс `U` стоит слева от остатка, а префикс `V` справа, равна `!![0, 1; 0, 1]` и не равна остатку слова.

3. Замороженный `dI`. Шаг `⟨⟨e10, 0⟩, ⟨e10, 0⟩⟩` и движущийся переплётчик `⟨1, e01⟩`. `kept_dI_value`: производная остатка равна `!![-1, 0; 0, 1]`, то есть `e10 * e01 - e01 * e10`. `frozen_dI_is_zero`: та же формула при `dI = 0` даёт нуль. `frozen_dI_fails`: эти производные различны, замороженное выражение `dV I - I dU` равно нулю, а полная производная равна сохранённому `V dI - dI U`.

## Печать аксиом

Команда в каталоге `03_FORMALIZATION`:

`~/.elan/bin/lake build D0.Research.PrimitiveJetComposition`

Сборка завершилась успешно. `sorryAx` нет. Для каждой перечисленной теоремы список один и тот же или его подмножество: `propext`, `Classical.choice`, `Quot.sound`. Новых аксиом нет.

```
'D0.Research.PrimitiveJetComposition.wordResidual_eq_orderedSum' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.jet_wordResidual_eq_orderedSum' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.stepResidual_deriv' depends on axioms: [propext]
'D0.Research.PrimitiveJetComposition.stepResidual_deriv_eq_frozen_add_dI' depends on axioms: [propext]
'D0.Research.PrimitiveJetComposition.word_intertwining_of_steps' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.branched_program_requires_agreement' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.word_residual_does_not_force_branch' depends on axioms: [propext]
'D0.Research.PrimitiveJetComposition.exact_step_does_not_normalize_postselection' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.wordResidual_norm_le' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.jet_wordDeriv_norm_le' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.sample_factors_do_not_commute' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.sample_ordered_residual' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.reversed_order_fails' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.kept_dI_value' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.frozen_dI_is_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.frozen_dI_fails' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.PrimitiveJetComposition.branch_sum_does_not_give_each_label' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (1475 jobs).
EXIT:0
```

## Команды

| Команда | Результат |
| --- | --- |
| `~/.elan/bin/lake build D0.Research.PrimitiveJetComposition` в `03_FORMALIZATION` | `Build completed successfully (1475 jobs).` `EXIT:0` |
| `python3 tools/validate_repo.py` | `ERROR orphan Lean modules outside registry/support closure: D0/Research/PrimitiveJetComposition.lean` `FAIL errors=1 warnings=0` |

Цель `D0.All` не собиралась. Каталог `.lake` этого worktree не коммитится.

## Строка formal_support

Строка ниже записана здесь для CONTROL. В `02_REGISTRY/formal_support.csv` она не вставлена. `03_FORMALIZATION/D0/All.lean` не правился.

```
D0.Research.PrimitiveJetComposition,D0/Research/PrimitiveJetComposition.lean,EXPLICIT_SUPPORT,02_REGISTRY/research/sources/d0_w2_primitive_jet_lean_2026-10-16/RESULT_RU.md
```

## Блокер

Единственный оставшийся шаг принадлежит CONTROL: внести строку в `formal_support.csv` и пересобрать `All.lean` генератором. До этой регистрации `validate_repo.py` сообщает сиротский модуль, и перевод PR в Ready ломает проверки orphan/closure. PR #342 остаётся Draft, задача остаётся `IN_PROGRESS`. `task_lifecycle.py retire` не запускался. Конечная лемма не даёт физического допуска и не закрывает ОТО.
