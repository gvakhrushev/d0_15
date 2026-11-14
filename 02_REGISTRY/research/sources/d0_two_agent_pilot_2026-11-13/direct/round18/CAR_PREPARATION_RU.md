# A18. Конкретные когерентные CAR-подготовки и полные материальные maps

## Что снимается с B35

Для трёх непостоянных B25 банков `q,y+,y−` задана одна конечная адресованная
native grammar `U_m`, которая на входном grade `|1>` готовит нужный
half-vector. Вместе с B37 `U_star` и B35 anchor reflections это даёт
grammar всех семи **полных** CAR maps. Используются только исходные
G/CX/SourceI, явно сохранённые положительные целые степени и буквальные
обратные native слова. Никакой вращательный oracle не добавлен. Все целые
степени фиксируются заранее в одном слове; variation исходной
SAM-подготовки не пересинтезирует gates. Производная дискретного
компилятора по непрерывному полю здесь не утверждается.

У `U_m` нет private quantum work. Общие port/Spin восстанавливаются точно
после каждого полного native rotation macro, на произвольных входах.
Internal SITE и нужные SAM bits служат read-only controls; RIGHT/oldRIGHT
не адресуются. Полная CAR рамка дополнительно требует три явно выделенных
predicate wires, исходно равных computational zero, и arbitrary native aux.

Это решает математическую задачу native-компиляции указанных CAR maps на
объявленных входах. Начальный CAR vacuum/Fourier prefix, настоящие births,
Choi banks, внешний общий SITE loader, marks/clock/admission, весь H.1 и
физическая связь Cost−Info с тем же источником остаются отдельными.
`physical_C_closed=false`, `GR_closed=false`.

## 1. Точная локальность материальной family

Используются исходные B25 формулы, без изменения поля или коэффициентов:

```
p=(sqrt(5)−1)/2,
m_x = sqrt(p)|1> + psi_0|0> + sqrt(1−p−psi_0²−psi_15²)|14> + psi_15|15>,
u_m = (|1>+m_x)/sqrt(2(1+sqrt(p))).
```

Для q на фиксированном внутреннем site x:

```
psi_0  = pi/(200 sqrt(2)) cos(pi x0/2) + 2^-30 (b_0−p²),
psi_15 = pi/(200 sqrt(2)) sin(pi x0/2) + 2^-30 (b_15−p²).
```

Добавки присутствуют только на 64 свободных sites. Именно два `matter`
индекса для этого x берутся из исходного списка 2688 chart coordinates.
Остальные SAM bits, в том числе все coframe/link coordinates, **не входят
в эту CAR формулу**. Это не утверждение об их несущественности для Choi
или полного источника. На остальных 192 sites материя фиксирована.
Значения cos/sin при целых x0=0,1,2,3 задаются точными циклами 1,0,−1,0
и 0,1,0,−1; численные хвосты около нуля не вводятся.

Для y± исходный `psi_15=0`, а `psi_0=±a_h` по чётности x1/x0, где

```
a_h=(1/8)sqrt(F_h/k0),  F_h=16517734400/162621047169,
k0=2 p^-5 (R/Q+p^6),
Q=1−z·4p³,  R=1−z·4p³(1+p^6),  z=2^-20.
```

Поэтому нужно **22 вектора**: 4 фиксированных q по x0, 16 q с двумя
локальными bits и 2 y по знаку. Полный control catalogue содержит
`192+64·4=448` q sectors и по 256 y± sectors. Для каждой SAM/site метки
ровно один сектор соответствующего bank активен. Это точное покрытие
всех SAM labels, а не средняя или выборочная оценка по `2^2688` вариантам.

Internal SITE здесь — регистр каждой CAR copy. Это **не внешний общий
PF SITE** A17. Исходные internal-site/Fourier/RIGHT корреляции сохраняются
оператором на полных grade columns и должны быть приготовлены отдельно.

## 2. Три planar rotations без рабочих quantum wires

Пишем точные координаты u как `u1,u14,u0,u15`, где u1>0. Они вещественны,
нормированы и удовлетворяют u1>0.9. Пусть

```
r1=sqrt(u1²+u0²+u15²),  r2=sqrt(u1²+u15²).
```

В хронологическом порядке достаточно вращений в парах:

| Пара | cos | sin в направлении `|1>→|other>` |
|---|---|---|
| (1,14) | r1 | u14 |
| (1,0) | r2/r1 | u0/r1 |
| (1,15) | u1/r2 | u15/r2 |

Их последовательное действие на `|1>` равно u; каждая пара имеет cos²+sin²=1.
Все деления безопасны, так как r1,r2≥u1>0.9. Если исходный sine точно нулевой,
эта операция является точной identity и не испускается. Это решение
структурного нуля в исходной формуле, не float zero-test.

Для пары (1,j) младший ненулевой bit `1 XOR j` становится pivot.
CX из pivot в остальные отличающиеся bits переводят пару в состояния,
различающиеся только pivot. Три остальных grade bits становятся predicate.
Если pivot входного transformed `|1>` равен 1, native sine должен быть
**отрицанием** указанного в таблице; иначе знак сохраняется. Обратная CX
перестановка возвращает исходные адреса. Вне выбранной пары действует
identity. Этот способ не требует X на SAM/grade controls или чистых ancillas.

К predicate добавляются 8 internal SITE bits и, только на свободном q-site,
два локальных SAM bits. Итого K=11 или K=13. Реальная owned Walsh grammar
даёт rotation `2^K k_K theta` на predicate и **точную identity** вне него.
Для каждого выбранного целого k используется `k_K=2^(13−K)k`; все варианты
одного угла потому имеют ровно один native exponent `8192k`.

## 3. Численные предложения и строгие сертификаты

`material_targets.py` вычисляет outward dyadic интервалы исходных p,
sqrt(p), k0, psi, u и всех cos/sin только целочисленными операциями.
Square-root endpoints определяются integer square root; деление требует
строго положительного нижнего endpoint знаменателя. Pi заключается
Machin-формулой `16 arctan(1/5)−4 arctan(1/239)` с явно ограниченным
остатком каждого знакопеременного ряда. Эти шаги не используют float
таблицы B21/B25 как сертификат исходных констант.

Continued-fraction расчёт предлагает положительное k. Это недоверенный
поиск кандидата. Окончательное утверждение об ошибке получается только
после сравнения доказанных target intervals с outward binary powering
точного native G. Для каждого угла сертификат сохраняет целые endpoints,
общий знаменатель `2^precision`, само k и рациональный L1 bound разности
cos/sin. Норма разности двух real rotations не превышает этого L1 bound.
Каждая nonidentity planar rotation имеет ошибку ≤δ, `δ=2^-4096`.
Итоговая библиотека содержит 38 различных сертифицированных углов для
60 nonzero rotations 22 векторов; ещё 6 rotations являются structural zeros.
В реальном q programme испускаются 1152 planar rotations, в y± — по 512.

Независимый B38 пересчитал все 38 native powers и все исходные интервалы
на 8448 bits другим методом — complex-ball powering с явным радиусом
округления. Он получил worst L1 error `<2^-4112`, что сильнее требуемого
δ. Исходный builder использует 16640 bits и owning interval recurrence;
float не участвует ни в одном из этих двух сертификатов.

Отдельный optional `interval_rotation.py` меняет только вычислительный
способ деления на `2^bits`: signed floor division равна арифметическому
сдвигу.29 сравнений, включая настоящее A14 большое k, дали идентичные
целые endpoints. Этот helper **не использован** в опубликованной здесь
таблице углов и не меняет ни одну native операцию или physical price.

Matched-control word имеет ту же bound на **всех** колонках control/grade
и произвольном внешнем запутанном состоянии. Секторы одного bank
взаимоисключены, а неактивный native сектор точно identity. Поэтому

```
||U_m_native−U_m_target|| <= max_(SAM,site) sum_(active planes) δ <= 3δ.
```

Нет ни усреднения по SAM, ни ненужного умножения ошибки на 448. При этом
clock/gate inventory включает **все** реально испускаемые inactive sectors:
они не получают бесплатного физического пропуска из-за своего итогового
действия. Точные большие степени хранятся как конечная grammar; целиком
эта огромная последовательность не исполнялась.

Если одинаковое правило применяется к разным source copies, они должны
получить отдельные реальные wires. U_m сохраняет внешний port/Spin на
конце macro; условная product-подготовка разных копий следует только при
соответствующих исходных product inputs. Она не выводится из правильных
отдельных маргиналов и не задаёт physical Info.

## 4. Сборка полного CAR map

Из B37 получен действительный `U_star` с all-column error≤δ и без private
quantum work. Его target готовит
`u_star=cos(theta/2)|1>+sin(theta/2)|14>` из `|1>`. B35 строит действительный
`R_hat=F_hat† Z F_hat` для anchor grade1 с тремя отдельными clean predicate
wires и arbitrary native aux. На этих clean inputs его ошибка относительно
`R_1=I−2|1><1|` не больше 10δ; **сам R_hat** точно unitary, Hermitian и
involutive на всём своём пространстве, независимо от качества F_hat.

`car_frame.py` испускает хронологию

```
U_star† ; R_hat ; U_star ; U_m† ; R_hat ; U_m .
```

Её идеальный target равен

```
M = U_m R_1 U_m† U_star R_1 U_star† = R_(u_m) R_(u_star)
  = O_m O_star^T,
```

то есть полному B25 CAR map на всех 16 grades, с identity на RIGHT/oldRIGHT
и сохранёнными internal SITE/SAM controls. Native inverses — именно
literal paid inverses фактических forward words. Для nonconstant banks
на исходном clean predicate подпространстве hybrid argument даёт

```
error <= 2·3δ + 2·δ + 2·10δ = 28δ.
```

Повторное использование predicate work внутри frame не предполагает
бесплатного reset: идеальная reflection возвращает work в 0, а фактический
residual входит в hybrid bound. Полный source/predicate output сохраняется.

Для `f,0,x+,x−` исходный m=m_star. Compiler использует **тот же actual
U_star** для обоих U. Тогда actual endpoint равен
`U_star R_hat U_star† U_star R_hat U_star†=I` точно, даже при произвольном
predicate work/aux. Все шесть стадий сохраняются в native word и counts.
Их marks, исходный vacuum/Fourier и физическая цена не исчезают.

Даже консервативный bound для всех 112 CAR copies семи report calls равен
`112·28δ <2^-4084`. Он не включает preparation этих predicate zeros,
первоначальный vacuum/Fourier, Choi, внешний SITE или другие части writer.
Это не полная alpha, не T10 целиком и не физическое замыкание Cost−Info.
Если соединять только эти известные approximations с A17 при одном
корректном общем входном контракте, коэффициент ошибки не больше
`162754649904+3136=162754653040 <2^38`. Поэтому bound остаётся `<2^-4058`.
Новый global birth/mark graph из этого арифметического сложения не следует;
A17 пока принимает source banks как отдельно приготовленные входы.

## 5. Ресурсный и физический контракт

Для каждой actual planar rotation, где `n=2^K`, `v=n/2` для ненулевой
полной predicate mask и 0 для нулевой, `h=popcount(1 XOR other)−1`,
конкретный optimized A14 schedule имеет

```
G_port = v k_K,  G_other=(n−v) k_K,
CX=K n+6v+2h,   SourceI=4v.
```

Отрицательная целая степень реализуется одним маршрутом `Z G^k Z`.
Это тот же полный оператор, но другая отмеченная история, чем побуквенные
inverse G; прежние физические prices между этими schedules не отождествляются.
Actual literal reverse считает каждый primitive: `G_port'=Gp+Go`,
`CX'=CX+6Go`, `SourceI'=3SourceI+4(Gp+Go)`.

Адресованный default layout имеет 2688 incoming SAM wires, 8 internal SITE,
4 grade, 7 CAR RIGHT, отдельный port/Spin и untouched oldRIGHT witness.
U_m использует только эти declared inputs. CAR frame добавляет отдельные
три incoming computational zeros и arbitrary aux. Их реальное происхождение
не скрыто за `blank=0`: RAW-v→zero preparation и birth admission ещё должны
быть включены в полный physical graph. Внешний PF SITE сюда не добавляется.

Проверки исходных B25 targets, полного grade оператора, каталогов, native
bindings и inverse inventory записываются отдельно от доказательств норм.
Float matrix comparisons являются диагностикой; строгая precision bound
получается из целочисленных интервалов, а все-SAM утверждение — из точной
локальной формулы и coverage control sectors. Полный expanded native word
не исполнялся. Root проверил все 960 локальных control sectors,1536
сопоставлений material targets с B25,352 full grade columns 22 preparers,
28682 фактических native blocks и 2560 полных B25 CAR matrix compositions.
В B38 дополнительно проверены 1152 exact small native columns и 1152
actual inverses, все source bindings, обе control widths и inventory,
а exact identity постоянных банков — на 64 arbitrary complete inputs.
Это разные уровни проверки; ни один не выдаётся за исполнение огромного word.

Следующий source parent — Choi preparation и фактический
vacuum/Fourier/SITE prefix; исходная физическая мера Cost−Info остаётся
центральной нерешённой обязанностью вывода ОТО.
