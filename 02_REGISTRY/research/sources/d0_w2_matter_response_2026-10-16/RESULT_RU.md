# Кандидатный интерфейс matter response: shell128 и reference128

Статус: **candidate**. Это реализация уже доказанного off-shell исключения, а не новый вывод. Физическая доступность подготовки не утверждается. Оставшееся совместное field/shell ядро не решается. Предел ОТО не выводится.

Научный владелец, только чтение: `33267713b2e6d3e78af7789547b00f50cdceb43d`, заметка `A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md`. Исторические row-wave и conformal scopes читаются с `74e62cdc716e10883accba9d34ccf0e21d58eb65`. Старый расчёт 8192 рёбер цены не повторяется и не выдаётся за результат.

Потребитель: N07, функция `solve_matter_response`. Файл

`02_REGISTRY/research/sources/d0_w2_matter_response_2026-10-16/matter_response.py`

импортируется по пути, каталог не является Python-пакетом.

## 1. Что вызывается

```text
solve_matter_response(delta_prime, delta_second, parameters)
response_curve_jets(delta(t), epsilon(t), tau(t), V(t), U, W, t)
uniform_shell_complement_bound(delta_norm, epsilon_shift, gap_exceeds_certified=...)
thermal_feedback_source(eigenvalues, diagonal, off_diagonal, calibrations, shell_mask=...)
auxiliary_unfolding(K, A)
off_shell_factors(delta, epsilon, U, W)
```

Входы solver: фактические `Delta'`, `Delta''` и допустимые параметры shell/reference. Выходы: projected compatibility, нормальный matter response, оставшиеся kernel coordinates, вклад в первый и второй source.

`Delta'' is None` не читается как нулевой jet. Носитель `native_dense` отказывается строить вектор из 16 744 448 вещественных Q-координат: `2 (65536 - 128) 128`.

## 2. Уже доказанные тождества, которые только исполняются

На объявленном окне `||Delta - Delta0|| < 1/8`, `|epsilon - epsilon0| < 1/8` и при сертифицированном зазоре `dist(epsilon0, spec(Delta0|Q)) > 1/2`:

```text
Psi = J sqrt(tau) V,
E = J* (Delta - epsilon I) J,
Tr(tau J* J) = 1,
||R_Q|| <= 2,   ||G_Q|| < 4.
```

`||G_Q|| < 4` возвращается только внутри этого открытого окна. На границе `1/8` и без сертифицированного зазора константа 4 не ставится. Более узкий наблюдаемый зазор её не заменяет и не оценивает обратный полный field/shell Hessian. Хвост Неймана — прежняя оценка `||R0|| t^(k+1)/(1-t) < 4 * 2^(-(k+1))` при `t < 1/2`.

Тождество `dE = J* (dDelta) J - G depsilon` исполняется и вне `E = 0`. Второй jet — производная этого тождества. Нормировка — `Tr(tau G)`, а не замороженный `Tr(tau) = 1`.

`P Delta' P = epsilon' P` ставится только при полном Schmidt rank. Для меньшего ранга остаётся поддержка `E tau = 0`. Rank-one подготовка операторного равенства не получает.

`E = 0` и бесследовый shell-остаток `T` удерживаются как уравнения. Нижний нулевой блок седла `[H_red, T*; T, 0]` не обращается. Anti-Hermitian `V` — полярное reference-волокно этой цены, 16384 вещественных направления; traceless Hermitian `S` остаётся свободным множителем. Ни то, ни другое не объявляется gauge.

`sigma_* = K / Tr K` и `X_* = A^{-1}` — вспомогательные профили unfolding. Они не являются `Psi` и не подменяют нормировку `Tr(tau J* J) = 1`.

Прямое ограничение stored-adjoint уже уже полной эрмитовой сферы: `G_rr(x) = G_rr(x+r)`. Оно сообщается отдельно и не превращается в gauge.

## 3. Какие операции matrix-free

Без плотного дополнения и без исключённого вещественного вектора исполняются:

- маска Fourier shell, восемь импульсов `±e_r`;
- modewise применение `R_Q` скаляром `1/(lambda - epsilon)` на Q-моде;
- ряд Неймана для `G_Q` по тем же модам;
- shell Gram по блокам связи, размерности shell, а не дополнения;
- разделённые разности `kappa` и rank-one производная `Z`;
- shell-след `-(2/r) Re Tr(P X_w R_Q X_v P)`.

Плотный native `J` размера `65536 × 128` не собирается.

## 4. Два разных scope

**Row-wave repair.** Хранимая кривая: observer `e0`, тождественные links, нога 2 вращается в плоскости 23 волной `(3,3,0,0)`, фаза не зависит от `x2`. Однородная length acceleration чинит все 128 shell rows: блоки `±e2` были `-gamma I`, остальные нули, после починки все нули. Материальный вклад во второй source есть `-gamma/4`. Нормальный response `Q Psi' = -R_Q X Psi0` ненулевой. Полная тепловая сумма по 4096 модам здесь не пересчитывается и не заменяется shell. Полевое ядро не решено: положительность старого `S''` остаётся у ведущего.

**Nonscalar conformal obstruction.** Коэффициентная кривая `exp(t phi) G_*` нарушает `G_rr(x) = G_rr(x+r)` вдоль роли 0. Внутри занятого Fock-блока `e0`

```text
(E2)_00 - Tr16(E2)/16 = 8 sqrt(2) (d - o) > 0
```

при `d > o > 0`. Скалярная матрица `c I16` это не меняет. Контраст следов `Tr E2_(e0) - Tr E2_(e2)` строго отрицателен на той же области, поэтому предписанная кривая не имеет общего `epsilon''`. Это другой scope: shell equations остаются открытыми.

Сертифицированный прямоугольник v8 только потребляется. Из него следует `d > o > 0`, `d > 1/16` и `epsilon0 > 2`, поэтому нулевая мода не портит уже данный зазор `> 1/2`. Сам зазор заново не оценивается.

## 5. Проверка

```text
python3 02_REGISTRY/research/sources/d0_w2_matter_response_2026-10-16/test_matter_response.py
python3 -O 02_REGISTRY/research/sources/d0_w2_matter_response_2026-10-16/test_matter_response.py
```

Оба режима дают один и тот же JSON, 104 точных проверки, `status = PASS`. Внешний диагональный jet `Delta'`, видимый только вне shell, остаётся в тепловом источнике; обнуление вне shell или rank-one члена `Z` его прячет, и проверка это отвергает. Ложные pure-16 reduction и frozen normalization отвергнуты.

## 6. Куда подставлять и что остаётся

N07 подставляет `T`, нормальный `Q`-response и член `-(2/r) Re Tr(P X R_Q X P)` в блок `[H_red, T*; T, 0]`. Нижний нуль не обращается. Тепло и feedback остаются на полном носителе: `kappa` использует feedback multiplicity, а не reference rank.

Оставшийся blocker: совместное field/shell ядро и нелинейное продолжение не решены. Они остаются у ведущего трека #334.
