# Конечный золотой фильтр: скалярные моменты и извлечение коэффициента

Статус: скомпилированный Lean-модуль. Это не выбор действия, не чтение кривизны и не утверждение об ОТО.
Источник, только чтение: `dfaf7c8df509d5abd83fa60a185ad530feadc9b5`,
`02_REGISTRY/research/A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md` и
`02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md`.
Мера: существующий `D0.CondensedAnchor.DetectorSupportGoldenWeight.cylWeight`
(`true` — прямая буква, `false` — возврат). Вторая мера не вводилась.

Модуль: `03_FORMALIZATION/D0/Research/GoldenCurvatureKernel.lean`.
Интеграция для M01: добавить `import D0.Research.GoldenCurvatureKernel` в `03_FORMALIZATION/D0/All.lean` и включить модуль в release closure.

## Что скомпилировано

Четыре слова: `FF = [true, true]`, `FR = [true, false]`, `RF = [false, true]`, `RR = [false, false]`.
Чтение `epsilon`: `FF/RR ↦ 0`, `FR ↦ 1`, `RF ↦ −1`.
`cylinderMoment k` — сумма `cylWeight(word c) * (epsilon c)^k` по этим четырём словам.

- `fourCylinderMass`: сумма четырёх `cylWeight` равна 1.
- `cylinderMoment_odd`: для нечётного `k` момент равен 0. Следствия: `cylinderMoment_one`, `cylinderMoment_three`.
- `cylinderMoment_two`: момент равен `2 * (φ⁻¹) ^ 3`.
- `cylinderMoment_four`: тот же момент `2 * (φ⁻¹) ^ 3`.
- `cylinderExpect_degreeFour_shape`: ожидание `b0 + α ε² t² + γ ε⁴ t⁴` равно `b0 + (α * moment 2) t² + (γ * moment 4) t⁴`.

Полином `degreeFour b a c t = b + a t² + c t⁴`.
Веса при `lam ≠ 0` и `lam² ≠ 1`:

- `coeffC0 lam = -(lam² + 1) / lam²`
- `coeffC1 lam = lam² / (lam² - 1)`
- `coeffC2 lam = -1 / (lam² * (lam² - 1))`

- `coeff_system`: эти веса уничтожают постоянный и степень-четыре члены и нормируют коэффициент при `t²` на 1.
- `coeff_unique`: любое решение той же тройки уравнений совпадает с этими весами.
- `threePointFilter_eq_quadratic`: `c0 F(0) + c1 F(t) + c2 F(lam*t) = a t²`.
- `threePointFilter_of_cylinder_shape`: то же для коэффициентов `α * moment 2` и `γ * moment 4`.
- `joint_spectator_on_samples` и `joint_spectator_blank_preserves_filter`: одно и то же слагаемое на всех трёх точках не меняет чтение.

Золотая специализация, без гипотезы о кривизне:

- `golden_lambda_admissible`: `φ ≠ 0` и `φ² ≠ 1`.
- `goldenContrast t b a c = φ⁴ (F(t) − F(0)) − (F(φ t) − F(0))`.
- `goldenContrast_scale`: контраст равен `a * (φ⁴ − φ²) * t²`.
- `golden_pair_weight_calibration`: `(φ⁻¹)³ * (φ⁴ − φ²) = 1`.
- `golden_specialization`: если квадратичный коэффициент равен `(φ⁻¹)³ * rho`, контраст равен `rho * t²` при любом `c`.
- `golden_specialization_div`: при `t ≠ 0` частное контраста на `t²` равно `rho`.
- `golden_filter_matches_contrast`: общий фильтр при `lam = φ` равен золотому контрасту, делённому на `φ² (φ² − 1)`.
- `joint_spectator_blank_preserves_goldenContrast`: общий сдвиг `b ↦ b + r` на всех масштабах не меняет контраст.

## Печать аксиом

Команда: `python3 tools/lean_task_build.py narrow D0.Research.GoldenCurvatureKernel`.
Успешный прогон: `Build completed successfully (2977 jobs)`, `returncode=0`, `seconds=357.5`.
У всех перечисленных теорем один и тот же набор: `propext`, `Classical.choice`, `Quot.sound`.
`sorryAx` нет. Новых аксиом в утверждениях нет.

```
fourCylinderMass: [propext, Classical.choice, Quot.sound]
cylinderMoment_one: [propext, Classical.choice, Quot.sound]
cylinderMoment_two: [propext, Classical.choice, Quot.sound]
cylinderMoment_three: [propext, Classical.choice, Quot.sound]
cylinderMoment_four: [propext, Classical.choice, Quot.sound]
threePointFilter_eq_quadratic: [propext, Classical.choice, Quot.sound]
coeff_unique: [propext, Classical.choice, Quot.sound]
golden_pair_weight_calibration: [propext, Classical.choice, Quot.sound]
golden_specialization: [propext, Classical.choice, Quot.sound]
golden_specialization_div: [propext, Classical.choice, Quot.sound]
joint_spectator_blank_preserves_goldenContrast: [propext, Classical.choice, Quot.sound]
dropRR_mass_ne_one: [propext, Classical.choice, Quot.sound]
dropRR_renormalized_second_moment_ne: [propext, Classical.choice, Quot.sound]
frozen_blank_fails: [propext, Classical.choice, Quot.sound]
wrong_lambda_coefficient_fails: [propext, Classical.choice, Quot.sound]
wrong_golden_scale_power_fails: [propext, Classical.choice, Quot.sound]
```

## Карта на формулы источника

Файл `A4D_GOLDEN_CYLINDER_CURVATURE_READOUT.md` на указанном SHA. Номера формул — оттуда. Геометрические имена `R` и `Q4` ниже только как метки источника; в Lean они не используются.

| Источник | Lean |
|---|---|
| Таблица FF/FR/RF/RR, веса `p^2`, `p^3`, `p^3`, `p^4`, `p = φ⁻¹` | `cylWeight_FF`, `cylWeight_FR`, `cylWeight_RF`, `cylWeight_RR` через `cylWeight_eq_pow` |
| Сумма весов равна 1 | `fourCylinderMass` |
| (1) `E ε = E ε³ = 0`, `E ε² = E ε⁴ = 2 p³` | `cylinderMoment_one`, `cylinderMoment_three`, `cylinderMoment_two`, `cylinderMoment_four` |
| Ожидание чётного полинома по `ε` | `cylinderExpect_degreeFour_shape` |
| (7) `c0`, `c1`, `c2` | `coeffC0`, `coeffC1`, `coeffC2`; единственность — `coeff_unique` |
| Отмена `b`, `c` и коэффициент `a` | `threePointFilter_eq_quadratic`: значение фильтра равно `a t²` |
| (8) числитель `φ⁴ (M_t − M_0) − (M_{φ t} − M_0)` | `goldenContrast` |
| `p³ (φ⁴ − φ²) = 1` | `golden_pair_weight_calibration` |
| При квадратичном коэффициенте `p³ * rho` контраст / `t²` равен `rho` | `golden_specialization`, `golden_specialization_div` |
| Общее добавление spectators/blank на всех масштабах | `joint_spectator_blank_preserves_goldenContrast`, `joint_spectator_on_samples` |

Что не переносилось. Многочлен источника `D + p³ t² R + 2 p³ t⁴ Q4` использует ещё тождество `e2(A) = ((tr A)² − tr(A²))/2` и сумму Гаусса. Здесь квадратичный коэффициент ожидания формы `α ε²` равен `α * 2 p³`, а не `p³ R`. Этот множитель 2 и сама кривизна в модуль не входят. Не формализованы определитель `det(I − t ε A)`, унитарное приборное пополнение, подготовка `rho` и ковектор Эйнштейна.

## Контрпримеры

Каждый ниже — отдельная теорема, и её заключение ложно для испорченного чтения.

- Удаление RR: `dropRR_mass_ne_one` — сумма трёх весов без RR не равна 1. `dropRR_renormalized_second_moment_ne` — деление сырого второго момента на эту массу не равно `cylinderMoment 2`. Ненормированная сумма FR+RF по-прежнему равна `cylinderMoment 2` (`dropRR_unnormalized_second_moment`), потому что `epsilon RR = 0`.
- Замороженный blank: `frozen_blank_fails`. Сдвиг только нулевого масштаба на `r = 1` при нулевом полиноме и `t = 1` не равен `goldenContrast`. Сдвиг равен `(1 − φ⁴)` (`frozen_blank_shift`).
- Неверный коэффициент `lam`: `wrong_lambda_coefficient_fails`. При `lam = 2` и `F(t) = t⁴` внешний вес без `lam²` в знаменателе даёт ненулевое значение, тогда как `threePointFilter 2 1 0 0 1 = 0`. Отдельно `wrong_golden_scale_power_fails`: замена `φ⁴` на `φ²` в числителе не уничтожает `t⁴` и не совпадает с `goldenContrast 1 0 0 1`.

## Проверки

| Команда | Результат |
|---|---|
| `python3 tools/lean_task_build.py narrow D0.Research.GoldenCurvatureKernel` | PASS, `returncode=0`, 357.5 s, модуль собран |
| `python3 tools/validate_repo.py` | FAIL, orphan: `D0/Research/GoldenCurvatureKernel.lean` |
| `python3 tools/formalization_debt_audit.py --check` | FAIL, `unreachable-module`: `D0.Research.GoldenCurvatureKernel` |

Полный `lake build D0.All` не запускался: модуль намеренно не добавлен в `All.lean`.

## Блокер

Общий `All.lean` и closure не менялись. Пока M01 не добавит импорт и строку closure, `validate_repo.py` отвергает модуль как orphan, поэтому задача остаётся `IN_PROGRESS` и не переводится в REVIEW.
