# Конечный перенос стационарного блока через Schur

Модуль `D0.Research.SchurStationaryTransfer` фиксирует тождества конечных вещественных координатных матриц. Для блочного оператора `H = [[A, B], [C, D]]` гипотеза `IsTwoSidedInverse D Dinv` означает `Dinv * D = 1` и `D * Dinv = 1`. Это поставленный двусторонний обратный вспомогательного блока, а не построенный Gibbs-резольвент и не log-det. Обратимость всего `H` не предполагается.

При этой гипотезе редуцированный оператор есть `schurComplement = A - B * Dinv * C`. Ядро этого оператора изоморфно ядру `H` графиком `jointOf`: полевая компонента `x` поднимается как `(x, auxOf)`, где `auxOf = -(Dinv *ᵥ (C *ᵥ x))`. Неоднородный источник `(f, g)` переходит в правую часть `reducedSource = f - B *ᵥ (Dinv *ᵥ g)`. Вспомогательный источник `g` в редукцию входит и не отбрасывается. Восстановление вспомогательной компоненты есть `recoveredAux = Dinv *ᵥ (g - C *ᵥ x)`.

Если `Aᵀ = A`, `Dᵀ = D` и `C = Bᵀ`, тот же обратный даёт конгруэнцию `H = Uᵀ diag(S, D) U` и разложение билинейной формы на форму Шура и сдвинутую форму `D`. Граница `ℓ¹` на `Dinv` — отдельная гипотеза `HasL1Bound`; константа не выводится из log-det. Инерция не формализована.

Нулевой нижний блок седла `shellSaddle = [[Hred, Tstar], [T, 0]]` не объявляется обратимым. Обратный этого нуля не строится.

Это условная конечномерная лемма. Она не утверждает вывод ОТО и не выпускает новый claim.

## Источник и потребитель

Развёртка цены, только чтение: `74e62cdc716e10883accba9d34ccf0e21d58eb65`, файл `02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md`, §§3–5. Совместное ядро, только чтение: `33267713b2e6d3e78af7789547b00f50cdceb43d`. Оттуда взято седло `[[H_red, T*], [T, 0]]` и лёгкое направление критерия: если `Tstar = Tᵀ` и седло убивает `(v, S)`, то `T *ᵥ v = 0` и `w ⬝ᵥ Hred *ᵥ v = 0` для всякого `w` с `T *ᵥ w = 0`.

Потребитель — PR #334: исключение вспомогательного блока при построении совместного эйлерова ядра. Обратимость статистического блока не объявляет совместное ядро пустым. PR #334 не сливается.

Специализация `UnfoldingBlocks` получает только уже объявленные матрицы `Lxx`, `Lxy`, `Lyx`, `Hy` и гипотезу `hyInv`. Скалярные контроли, `β`, `M`, `z`, Gibbs и log-det в модуль не входят.

## Теоремы

В файле нет `sorry`. Узкая сборка напечатала аксиомы. `sorryAx` в печати нет.

- `block_factorization`: `H = [[1, B Dinv], [0, 1]] [[S, 0], [0, D]] [[1, 0], [Dinv C, 1]]`.
- `symmetric_block_congruence`: в симметричном случае `H = Uᵀ diag(S, D) U` и `Sᵀ = S`.
- `symmetric_bilinear_form`: `u ⬝ᵥ H *ᵥ v` распадается на форму `S` по полевым компонентам и форму `D` по сдвинутым вспомогательным компонентам.
- `kernel_aux_eq`: из `H *ᵥ (x, y) = 0` следуют `y = -Dinv *ᵥ (C *ᵥ x)` и `S *ᵥ x = 0`.
- `reduced_joint_kernel`: из `S *ᵥ x = 0` следует `H *ᵥ jointOf = 0`.
- `schurKernelEquiv`: явная биекция `{x // S *ᵥ x = 0} ≃ {v // H *ᵥ v = 0}`.
- `schurKernelEquiv_field`, `schurKernelEquiv_aux`, `schurKernelEquiv_add`, `schurKernelEquiv_smul`: полевая компонента, вспомогательная компонента и ℝ-линейность графика.
- `stationary_transfer` и `stationary_transfer_converse`: неоднородное уравнение и обратное направление. `g` входит в `f - B Dinv g`.
- `aux_reconstruction_l1`, `recovered_aux_l1`, `kernel_aux_l1`: `ℓ¹`-граница реконструкции при поставленной `HasL1Bound Dinv K`.
- `unfolding_reduced_equation`, `unfolding_reduced_equation_converse`: та же передача на `UnfoldingBlocks`.
- `not_twoSidedInverse_of_kernel`: ненулевой вектор ядра запрещает двусторонний обратный.
- `zero_block_not_twoSidedInverse`: при непустом `Y` нулевая матрица не имеет двустороннего обратного.
- `saddle_constraint_without_inverse`: ограничение на строку поля без обратного нулевого блока.

## Отрицательные и положительные контроли

Все примеры доказаны в том же модуле на `Fin 1`. `eye1 = 1`, `zero1 = 0`, `oneVec = 1`, `shellVec1 = (0, 1)`.

1. Необратимый нижний блок. `every_candidate_inverse_misses_kernel`: для всякого кандидата `Dinv` матрица `zero1` не является двусторонне обратимой. Подъём `jointOf` нулевого поля даёт нуль и пропускает ненулевой вектор ядра `shellVec1` оператора `[[eye1, 0], [0, 0]]`.

2. Ненулевое редуцированное ядро. `nonzero_reduced_kernel`: `D = eye1` обратим, `schurComplement zero1 zero1 zero1 eye1` убивает `oneVec ≠ 0`, совместный вектор `(oneVec, 0)` лежит в ядре `H`, и сам `H` не имеет двустороннего обратного.

3. Знак. `flipped_schur_sign_fails`: при всех блоках `eye1` истинное дополнение `A - B Dinv C` убивает `oneVec`, и график с `y = -Dinv C x` лежит в ядре `H`. Противоположная комбинация `A + B Dinv C` того же вектора не убивает. Подъём со знаком `+Dinv C x` не лежит в ядре `H`.

4. Прямой вспомогательный источник. `direct_auxiliary_source_not_dropped`: уравнение `H *ᵥ (0, oneVec) = (oneVec, oneVec)` редуцируется к нулевой правой части `f - B Dinv g`, и эта правая часть не равна исходному `f`.

5. Нулевой нижний блок седла. `retained_shell_not_eliminated`: у `[[eye1, 0], [0, 0]]` нижний блок есть `0`, он не обратим ни для какого `Dinv`, и `shellVec1` остаётся в ядре. `hred_kernel_is_not_saddle_kernel`: у `[[0, eye1], [eye1, 0]]` нижний блок снова `0` и не обратим, `oneVec` лежит в ядре `Hred`, но `H *ᵥ (oneVec, 0) ≠ 0`. Ядро `Hred` не подменяет ядро седла.

## Печать аксиом

Команда в каталоге `03_FORMALIZATION`:

`~/.elan/bin/lake build D0.Research.SchurStationaryTransfer`

Сборка завершилась успешно. `sorryAx` нет. Для каждой перечисленной теоремы список один и тот же: `propext`, `Classical.choice`, `Quot.sound`.

```
'D0.Research.SchurStationaryTransfer.schurKernelEquiv' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.kernel_aux_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.reduced_joint_kernel' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.stationary_transfer' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.stationary_transfer_converse' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.block_factorization' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.symmetric_block_congruence' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.symmetric_bilinear_form' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.aux_reconstruction_l1' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.unfolding_reduced_equation' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.every_candidate_inverse_misses_kernel' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.nonzero_reduced_kernel' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.flipped_schur_sign_fails' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.direct_auxiliary_source_not_dropped' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.retained_shell_not_eliminated' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.hred_kernel_is_not_saddle_kernel' depends on axioms: [propext, Classical.choice, Quot.sound]
'D0.Research.SchurStationaryTransfer.saddle_constraint_without_inverse' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (1016 jobs).
EXIT:0
```

## Команды

| Команда | Результат |
| --- | --- |
| `~/.elan/bin/lake build D0.Research.SchurStationaryTransfer` в `03_FORMALIZATION` | `Build completed successfully (1016 jobs).` `EXIT:0` |
| `python3 tools/validate_repo.py` | `ERROR orphan Lean modules outside registry/support closure: D0/Research/SchurStationaryTransfer.lean` `FAIL errors=1` |

Цель `D0.All` не собиралась. Каталог `.lake` этого worktree не коммитится.

## Строка formal_support

Строка ниже записана здесь для CONTROL. В `02_REGISTRY/formal_support.csv` она не вставлена. `03_FORMALIZATION/D0/All.lean` не правился.

```
D0.Research.SchurStationaryTransfer,D0/Research/SchurStationaryTransfer.lean,EXPLICIT_SUPPORT,02_REGISTRY/research/sources/d0_w2_schur_lean_2026-10-16/RESULT_RU.md
```

## Блокер

Единственный оставшийся шаг принадлежит CONTROL: внести строку в `formal_support.csv` и пересобрать `All.lean` генератором. До этой регистрации `validate_repo.py` сообщает сиротский модуль, и перевод PR в Ready ломает проверки orphan/closure. PR #340 остаётся Draft, задача остаётся `IN_PROGRESS`. `task_lifecycle.py retire` не запускался. Конечная лемма не даёт физического допуска и не закрывает ОТО.
