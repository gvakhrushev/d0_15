# Первый actual matter corrector на меняющемся causal cone

16 октября 2026. Потребитель: §7.1 [causal/source bridge](A4D_NATIVE_CAUSAL_METRIC_SOURCE_BRIDGE.md).
Это продолжение того же Draft #334. Проверяется необходимое уравнение
подготовки в уже определённом exact proper-link stencil, без изменения цены.

**Результат.** В периодическом cone-примере faithful full-shell preparation
не имеет первого stationary amplitude corrector при точном LC sampling
и неизменных первых геометрических jets. Нулевой faithful trace A1 не
позволяет положить rho1=rho2=0 в полной цене или считать matter equation
решённым. Для этой семьи получено точное ненулевое резонансное препятствие.
Другие начальные состояния и корректировки самих полей не исключаются.

## 1. Те же поля, полный carrier и источник

Возьмём тор `(R/2pi Z)^4`, нормированную меру, y=x2,
`theta(y)=y`, `e=s O01(theta)`, `n=e0`, `s>1`. Тогда
`G=s^2 I4`, coordinate torsion0, а g меняет Lorentz cone. Число s
можно увеличить для strict local Julia domain при всех достаточно малых h.
Coordinate transports — именно proper LC transports из исходного owner:

```text
P0=Lambda exp(h M0(y)), P1=Lambda exp(h M1(y)),
P2=Lambda exp(h R01), P3=I,
M0=sin(2y)E02-cos(2y)E12+E21,
M1=-cos(2y)E02-sin(2y)E12-E20,
M2=R01=E01-E10, M3=0.                                    (1)
```

Здесь каждый Mr постоянен вдоль своего r-edge. P2 содержит настоящее
движение endpoint; это не frozen comparison. Native links получают
обратным coordinate intertwiner; (1) не объявляет координатные Mr
Lorentz-матрицами относительно постоянной eta.

После постоянной G-изометрии все16 exterior components сохраняются:
`D0=s^-1 sum_r gamma_r partial_r`, `gamma_r=C_r-I_r`,
`Delta0=-s^-2 sum_r partial_r^2`. Рассматриваем всю первую оболочку
`p=+/-e_r`: восемь momenta ×16 grades, dimension128.
Reference dimension остаётся128. Faithful normalized amplitude —
`C0=I128/sqrt(128)` между этой оболочкой и reference; в реальном
cos/sin basis это также буквальная вещественная матрица. Комплексный
Fourier basis не добавляет состояний и не удаляет conjugate modes.

Для amplitude variation H и J не зависят от C, а actual R даёт

```text
Delta_h C_h=R_h C_h, R_h=Tr C_h*Delta_h C_h/Tr C_h*C_h.       (2)
```

Никакие дополнительный source, выбранная reference column или fitted
материальная поправка не вводятся.

## 2. Exact first jet с настоящим adjoint

Пусть `H_r=Gamma(M_r)=sum_ab (M_r)_ab C_a I_b`.
При s=1 первый coefficient D_h равен

```text
D1=(1/2)sum_r (C_r+I_r)partial_r^2
   +sum_r (C_r H_r-H_r^T I_r)partial_r
   +(1/2)sum_r [C_r H_r^2+(H_r^T)^2 I_r].                 (3)
```

Члена derivative_r H_r в (3) нет именно потому, что он равен0 в
данной семье. Для общего cone его опускать нельзя. (3) также получено
независимо: Taylor raising coefficient `L1=sum C_r nabla_r^2/2`,
затем Fourier matrix adjoint `D1(q,p)=L1(q,p)+L1(p,q)*`.
Совпадают все64 блоков на оболочке. Это сохраняет matrix squares,
transpose boosts и обе противоположные y-моды.

Искомый perturbation `A1={D0,D1}` имеет degree3 в производных.
Сама continuum Cartan cancellation `sum C_r H_r=0` проверена на
полном16, но она не зануляет (3). Масштаб s даёт `A1=s^-2 A1|_(s=1)`.

## 3. Резонансное уравнение не выполняется

Пусть P — полный128-dimensional projector `Delta0=1/s^2`.
Обозначим `A=P A1 P`. Exact Gaussian-rational Fourier assembly даёт

```text
A*=A, Tr128 A=0,
Tr128 A^2=52/s^4.                                        (4)
```

При s=1, p=(-1,0,0,0), mask basis исходного creator owner,
в диагональном momentum block, например,
`A_(mask0,mask5)=i/2` и `A_(mask2,mask4)=1`.
Есть также ненулевой блок между p=-e2 и p=+e2.
Unitary переход всех пар +/-p в real cos/sin basis делает A
вещественной симметричной матрицей с теми же (4).

При `C_h=C0+h C1+o(h)`, `R_h=s^-2+h epsilon1+o(h)`,
первый коэффициент (2) требует

```text
(Delta0-s^-2)C1+(A1-epsilon1)C0=0,
(A-epsilon1 P)C0=0.                                      (5)
```

Проекция первого слагаемого равна0 для ЛЮБОГО C1, включая все
reference directions и off-shell amplitude variations. C0 имеет
полный ранг на P. Следовательно, (5) возможно только если
`A=epsilon1 P`, что противоречит (4). Точный минимальный residual:

```text
min_(epsilon1 real) ||(A-epsilon1 P)C0||_HS^2
 =Tr A^2/128-(Tr A/128)^2=13/(32 s^4)>0.                  (6)
```

У полной нормированной amplitude Euler row `2(Delta-R)C`
квадрат первого residual соответственно `13/(8 s^4)`.
R1 как скаляр равен0, но это не уравнение (5). На единичном торе
с theta=2pi y появляются соответствующие degree3 momentum factors;
число (6) дано в явно указанной period2pi convention, а не выдано
за норму исходного #216 comparator.

## 4. Как результат используется

В §7.1 источника K2 нельзя подставлять unchanged faithful full-shell
rho_h на этой exact-LC cone семье. Перед вычислением actual R2 нужно
либо изменить leading preparation на совместимый eigenblock A,
либо вывести реальные field/link first jets, меняющие резонансный
оператор в (5). Такие jets требуют собственных field Euler equations;
они не назначаются как компенсатор.

Это исключает конкретную stationary preparation continuation, а не все
cone geometries, все оболочки, все joint branches или original
fixed-g/fixed-tau/raw h^-2 terminal. Результат не выбирает native
observer/reference law. Он непосредственно проверяет один из отсутствующих
в предыдущем formal h² expansion actual amplitude coefficients.

Последующий [полный source-balanced test](A4D_CONE_SOURCE_BALANCED_PREPARATION.md)
уже проверяет первую альтернативу: одна смена leading preparation любого
ранга при неизменных first field jets на этом cone не помогает. Metric
balance требует веса1/4 по каждой оси, а actual A1 этому несовместим.
Для faithful полного shell real field-image witness исключает также все
гладкие первые field counterjets. Следующий открытый вариант — неполный
ранг ВМЕСТЕ с выведенными field jets и их полными Euler equations;
ни один из этих результатов не является global GR no-go.

## 5. Проверка

[Узкий helper](sources/d0_cone_matter_corrector_2026-10-16/check_cone_matter_corrector.py)
извлекает AST только frozen creator/order definitions, а не запускает
старые спектры, roots или checker entrypoints. Exact new controls:
полный CAR, Cartan cancellation, independent forward/adjoint assembly,
весь128 block, real preparation chart и (6). Отрицательные проверки
выявляют потерю H_r², замену матрицы её scalar trace и потерю пары
противоположных momenta. Результаты и hashes сохранены рядом с helper.
