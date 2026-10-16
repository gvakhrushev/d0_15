# Конечное координатное отражение источника

Модуль `D0.Research.SourceReflectionKernel` фиксирует тождества конечных вещественных координатных пространств. `Lin X Y` — матрица со строками в кообласти. Действие — `apply L x = L *ᵥ x`. Подъём ковектора — `pullback L e = Lᵀ *ᵥ e`, так что `(L* e)` спаривается как `e (L x)`. Правый обратный — отдельная гипотеза `IsRightInverse L W`, то есть `L * W = 1`. Эта гипотеза остаётся гипотезой: конечная лемма не даёт функционально-аналитического допуска `W` и не даёт физического допуска `W`.

Полный `lake build` цели `D0.All` не запускался. `All.lean`, `ClaimMap` и `02_REGISTRY/formal_support.csv` в этом PR не изменялись.

## Источник и потребитель

Исследовательский снимок, только чтение: `dfaf7c8df509d5abd83fa60a185ad530feadc9b5`. Это не accepted main. Прочитаны

- `02_REGISTRY/research/A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md`
- `02_REGISTRY/research/A4D_NATIVE_GEOMETRIC_READING_INTERFACE.md`
- `02_REGISTRY/research/A4D_COHERENT_COMPILATION_COST_DESCENT.md`

Pull request #310 не сливается.

Потребитель — M05: десять поперечных matching-уравнений и native-source lift, в котором прямые внутренние члены и matter-члены остаются в уравнении.

Координатное чтение заметок, без переноса их физических констант в лемму:

- при `a = L* e + r` и `L ∘ W = id` реконструкция есть `e = W* (a − r)`;
- `ℓ∞`-граница на `W` переходит в `ℓ¹`-границу на `W*`; явная константа `opLInf` — максимум абсолютных строчных сумм; численный множитель `28/s` из записи (21) ценовой заметки в модуль не входит, оценка параметризована произвольным `C ≥ 0`;
- слоты симметричного `4×4`: `(00, 01, 02, 03, 11, 12, 13, 22, 23, 33)`; вес `1` на диагонали и `2` вне диагонали; `packedDual` умножает внедиагональный слот на `2`.

## Теоремы

В файле нет `sorry` и нет новой аксиомы. Узкая сборка напечатала аксиомы перечисленных ниже теорем.

- `pullback_injective_of_rightInverse`: при `IsRightInverse L W` отображение `pullback L` инъективно.
- `reflect_residual`: из `a = pullback L e + r` получается `e = pullback W (a − r)`.
- `reflect_internal_direct`: из `pullback L e + d = 0` получается `e = −pullback W d`.
- `pullback_l1_le_of_lInf_bound`: если `∀ x, lInf (apply W x) ≤ C * lInf x` и `0 ≤ C`, то `l1 (pullback W a) ≤ C * l1 a`.
- `reflect_residual_l1`: реконструкция `reflect_residual` вместе с `l1 e ≤ C * l1 (a − r)`.
- `stationary_internal_l1`: `e = −pullback W d` и `l1 e ≤ C * l1 d`.
- `apply_lInf_le_opLInf`: `lInf (apply W x) ≤ opLInf W * lInf x`.
- `packedPairing_eq_frobenius`: для симметричных `A`, `B` взвешенное спаривание упаковок равно полному `frobenius`.
- `full_contraction_eq_packed_dot`: `frobenius E Q = packedDual E ⬝ᵥ pack Q`.

## Контрольные примеры

Каждый пример доказан в том же модуле.

1. Ранг. `rankOneL` — матрица `2×2` с единицей только в позиции `(0,0)`. Теорема `rank_deficient_neither_sided_inverse`: правого обратного нет, левого обратного нет, `pullback rankOneL axisOne = 0` при `axisOne ≠ 0`.

2. Прямой ковектор. На `Fin 1` взято тождественное отображение, `keptE = 1`, `directD = −1`. Теорема `deleted_direct_covector_does_not_force_zero`: `pullback 1 keptE + directD = 0`, при этом `keptE ≠ 0` и `keptE = −pullback 1 directD`. Нулевая сумма сохраняет ненулевой прямой ковектор.

3. Вес вне диагонали. `offDiag01` симметрична и несёт единицы в `(0,1)` и `(1,0)`. Теорема `wrong_off_diagonal_weight`: `frobenius offDiag01 offDiag01 = 2`, невзвешенное спаривание упаковки равно `1`, взвешенное спаривание равно `2`.

4. Левый обратный на месте правого. `incl : Fin 1 → Fin 2` посылает `t` в `(t, 0)`, `proj : Fin 2 → Fin 1` читает первую координату. `proj * incl = 1` и `incl * proj ≠ 1`. Теорема `left_inverse_reflection_fails`: `pullback incl covectorAxis + 0 = 0`, и `covectorAxis ≠ pullback proj (0 − 0)`.

Дополнительно `rightInverse_hypothesis_is_not_free`: нулевой эндоморфизм `Fin 1` не имеет правого обратного. Существование `W` в леммах выше остаётся посылкой.

## Печать аксиом

`python3 tools/lean_task_build.py narrow D0.Research.SourceReflectionKernel` напечатал для каждой теоремы один и тот же список. `sorryAx` в печати нет.

```
'pullback_injective_of_rightInverse' depends on axioms: [propext, Classical.choice, Quot.sound]
'reflect_residual' depends on axioms: [propext, Classical.choice, Quot.sound]
'reflect_internal_direct' depends on axioms: [propext, Classical.choice, Quot.sound]
'reflect_residual_l1' depends on axioms: [propext, Classical.choice, Quot.sound]
'stationary_internal_l1' depends on axioms: [propext, Classical.choice, Quot.sound]
'apply_lInf_le_opLInf' depends on axioms: [propext, Classical.choice, Quot.sound]
'packedPairing_eq_frobenius' depends on axioms: [propext, Classical.choice, Quot.sound]
'full_contraction_eq_packed_dot' depends on axioms: [propext, Classical.choice, Quot.sound]
'rank_deficient_neither_sided_inverse' depends on axioms: [propext, Classical.choice, Quot.sound]
'deleted_direct_covector_does_not_force_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'wrong_off_diagonal_weight' depends on axioms: [propext, Classical.choice, Quot.sound]
'left_inverse_reflection_fails' depends on axioms: [propext, Classical.choice, Quot.sound]
'rightInverse_hypothesis_is_not_free' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## Команды

| Команда | Результат |
| --- | --- |
| `git status` на старте, HEAD `6641c3399055f8f0179d9c173ff55eca7684b22c` | чисто |
| `python3 tools/task_dispatch.py WRK-A4D-LEAN-SOURCE-REFLECTION` | открытого исполнения не было |
| `python3 tools/task_lifecycle.py start WRK-A4D-LEAN-SOURCE-REFLECTION` | строка `PLANNED` → `IN_PROGRESS` |
| `python3 tools/lean_task_build.py narrow D0.Research.SourceReflectionKernel` | `seconds=115.3 returncode=0` |

Ранние узкие сборки того же файла давали `returncode=1` на целях `sum_fin10`, числовых ветвях `Fin` и лишнем шаге в `left_inverse_reflection_fails`. После правки доказательств повтор дал `returncode=0`. Цель `D0.All` не собиралась.

## Строка formal_support, которая не внесена

```
D0.Research.SourceReflectionKernel,D0/Research/SourceReflectionKernel.lean,EXPLICIT_SUPPORT,02_REGISTRY/research/sources/d0_medium_lean_source_reflection_2026-10-16/RESULT_RU.md
```

## Блокер

Модуль `03_FORMALIZATION/D0/Research/SourceReflectionKernel.lean` остаётся вне замыкания `formal_support`. Пока CONTROL не добавит строку выше, проверка репозитория сообщает orphan. Задача остаётся `IN_PROGRESS`, pull request https://github.com/gvakhrushev/d0_15/pull/333 остаётся draft. Retire и отметка Ready в этом PR не выполняются.
