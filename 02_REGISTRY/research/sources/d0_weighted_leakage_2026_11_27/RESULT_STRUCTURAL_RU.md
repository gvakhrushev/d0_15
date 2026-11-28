# Структурная проверка weighted CAR на действительном носителе

Этот результат усиливает [предыдущий четырёхточечный пример](RESULT_RU.md),
но не закрывает зарегистрированную общую формулировку NO-GO.
Исходный код — [Structural.lean](Structural.lean), независимый целочисленный
контроль — [check_structural.py](check_structural.py).

## Две общие сдвиговые компоненты

Для произвольного множества `X`, сдвигов `sx, sy : X → X`, рационального
множителя `s` и поля `f` положено `Δr f(x) = f(r x) − f(x)` и
`Q f(x) = s(x) [Δsx(s·Δsy f)(x) − Δsy(s·Δsx f)(x)]`.
Если сдвиги коммутируют в точке `x`, Lean доказывает точную формулу

```text
Q f(x) = s(x) [(s(sx x) − s(sy x)) f(sx(sy x))
              + (s(sy x) − s(x)) f(sy x)
              + (s(x) − s(sx x)) f(sx x)].
```

Для индикатора точки `sx x` она даёт `s(x)(s(x)−s(sx x))`, когда
`sx(sy x) ≠ sx x` и `sy x ≠ sx x`. Теорема
`WeightedLeakageGeneral.weighted_square_ne_zero_of_varying_neighbor`
поэтому доказывает `Q f(x) ≠ 0` при этих условиях, `s(x) ≠ 0` и
`s(x) ≠ s(sx x)`. Это локальный критерий; он не утверждает существование
такой пары сдвигов для произвольного носителя и произвольного веса.

## Четырёхролевой CAR на первом уровне архивного носителя

В Lean используется существующий `ArchiveRolePhasePoint 0`, то есть
`Role → Fin 2`, и существующие целочисленные матрицы создания
`D0.Geometry.carCreateInt` на `ArchiveFockState`. Для каждого `r : Role`
`shiftRole r` меняет соответствующий бит фазовой точки. Множитель
`sqrtWeightInt` равен `1` при `x A = 0` и `2` при `x A = 1`.
Он всюду положителен; Lean отдельно проверяет, что это действительно
неотрицательный квадратный корень веса `weightInt = sqrtWeightInt²`.

На поле `ψ : Site → ArchiveFockState → ℤ` определяется оператор

```text
(Dₛ ψ)(x, bra) = s(x) · Σᵣ Σₖ [ψ(shiftRole r x, k) − ψ(x, k)]
                                      · carCreateInt r bra k.
```

Вход `carFieldProbe` находится в точке `shiftA origin` и вакуумном
состоянии. Выход — точка `origin` и состояние с занятыми `A, B`. Lean
вычисляет точный матричный элемент полного четырёхролевого оператора:

```lean
theorem actual_four_role_car_square :
    weightedExterior (weightedExterior carFieldProbe) origin abOccupied = -1

theorem unweighted_four_role_car_control :
    unweightedExterior (unweightedExterior carFieldProbe) origin abOccupied = 0
```

Отдельно проверены степени Fock-состояний `0` и `2` и знак произведения
двух существующих CAR-операторов. Независимый Python-контроль проверяет
формулу в 1 296 конечных случаях, отрицательный контроль знака
Jordan–Wigner и весь невзвешенный квадрат на этом входе. Скрипт сохраняет
проверки при запуске с `-O`.

## Граница и воспроизведение

Это доказательство утечки для конкретного положительного веса и одного
уровня исходного архивного носителя, а также общий условный критерий для
двух сдвигов. Оно не доказывает утечку для всех непостоянных весов на
всех уровнях, не устанавливает единственность Hodge-модификации и не
является физическим GR-переносом. Отсутствующее исходное имя общего
владельца в реестре этим файлом не подменяется, статус не меняется.

Lean 4.30.0 проверил файл без `sorry`. `#print axioms` для общего критерия
и двух конечных CAR-контролей показывает `propext`, `Classical.choice`,
`Quot.sound`; дополнительных постулатов в файле нет.

```sh
python3 -B -O -W error 02_REGISTRY/research/sources/d0_weighted_leakage_2026_11_27/check_structural.py
cd 03_FORMALIZATION
lake env lean ../02_REGISTRY/research/sources/d0_weighted_leakage_2026_11_27/Structural.lean
```
