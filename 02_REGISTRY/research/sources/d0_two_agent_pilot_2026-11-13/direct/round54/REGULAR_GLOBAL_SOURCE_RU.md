# A54. Единый SOURCE для независимо меняющегося поля

## Результат и потребитель

Из A53 и B103 построен один конечный, лениво перечисляемый **G/CX SOURCE**
для каждого точного рационального имени поля `y` с `|y_j|<2^-32`.
Все 2688 исходных координат независимы; Einstein predicate в конструкторе
отсутствует. Один и тот же `FieldCentre` передаётся всем 1440 Choi и 128 CAR
копиям. Сохранены исходные 5376 CODE wires, восемь REPORT, private inputs,
границы, references, SITE, восьмой current bank и original seven-bank SC6.

Удалена конкретная предпосылка следующего применения: вместо условного
«скомпилировать SOURCE при свободном Y» теперь есть действительные
параметризованные providers, единая привязка проводов, uniform error и
uniform componentwise inventory. Это **новое слово**, даже при `y=0`.
Его actual `M(y)` и часы должны вычисляться заново. B105 — отдельный
потребитель, строящий из этого слова actual post и общий оплаченный clock.

Код: [native SOURCE](regular_source_native.py),
[G/CX binding](regular_global_source.py),
[план и оценки](REGULAR_GLOBAL_SOURCE_PLAN.json),
[проверка](check_regular_global_source.py),
[receipt проверки](REGULAR_GLOBAL_SOURCE_CHECK.json).

`physical_C_closed=false`, `GR_closed=false`. Производственное гигантское
слово не исполнено и точное число его **не дополненных** операций не
вычислено. Конечность конструктора не означает практической выполнимости.

## 1. Поле, исходный target и адреса

A53 `FieldCentre` — неизменяемый tuple из 2688 Fractions в исходном порядке
B21: 1024 inverse-coframe, 1536 proper-link и 128 matter. После CODE сдвига

    Y_j(y,b) = Y0_j + y_j + 2^-80 (b_low + 2 b_high − 3p²)

все координаты остаются в старом асимметричном B21 cube. Это следует из
проверенного строгого запаса `2^-32+3·2^-80 < (3/8)·2^-30`.
Конечные рациональные имена не подменяют все вещественные числа. Для
приближения идеального вещественного поля сохраняются A53/B91 ошибки
имени; производная дискретного выбора grid exponent здесь не заявляется.

`Sources(field)` использует:

* A53 coframe для каждого исходного bank и его полного address/CODE
  каталога; current offsets входят только в исходные свободные f/q rows.
* B103 direct Julia32 для всех 256 свободных f-link groups × 4096 CODE
  слов. Каждая группа читает собственные шесть координат в B42 GEN order.
  Группы с одинаковым `xy` не получают общий cached offset.
* Только **fixed** sectors B93 для остальных адресов каждого link bank.
  Старые variable B93 слова не выводятся. Fixed и variable addresses
  попарно различны; обратный обход меняет оба порядка.
* A53 CAR half-preparation для q/y±; прежние фиксированные STAR и
  reflection остаются в той же frame-композиции. Vacuum/Fourier — полное
  выбранное A23 продолжение, не произвольное иное vacuum-продолжение.

Full target proper link остаётся исходным B25:
`U=exp(Θ)U0`, `C=Λ(U)/2`,
`J=[[C,sqrt(I−CCᵀ)],[sqrt(I−CᵀC),−Cᵀ]]`.
Его новое разложение на 496 плоскостей меняет реализацию, не target.
На branch=0 и вне выбранного address/CODE все SELECT targets — identity.
Address 0 не получает изменяемый SELECT; `J_0=I32`, поэтому положительный
anchor overlap `1/sqrt(65568)` A21 остаётся постоянным. Именно это позволяет
сохранить прежний level-nine coherent adapter и его phase correction.

CODE в SOURCE используется только как control. Unit targets/permutations
A53 меняют mode/grade/aux, B103 — пять Julia wires; ни один из них не
записывает CODE. Старые prefix, vacuum, SITE, REPORT, resource frames и SC6
сохраняют свой прежний CODE-spectator contract. A29 replacement использует
старый отдельный helper. Следовательно, полный comparator core имеет
прежнюю block-diagonal по CODE структуру, необходимую actual diagonal
path-sum в B105. Равенство только одного подготовленного вектора для этого
аргумента не используется.

## 2. Полная хронология и literal inverses

Controlled Omega имеет порядок `prefix; coframe; link`. Новый provider
передаётся во все `3^9` вхождений исходного coherent adapter. Choi SOURCE
сохраняет paid PRIVATE_RAW, DATA_RAW, обе joint reflections и оба U.
CAR SOURCE сохраняет paid predicate RAW, vacuum prefix и полный frame.

У каждого метода есть **целочисленная** inverse depth. Для провайдера B103
с Boolean reverse сначала используется `depth mod 2`, затем каждое дерево
обращается ещё `depth − depth mod 2` раз. При depth=2 уже обращённые
положительные native слова не сокращаются бесплатно. При depth=1 меняются
порядок stages, порядок sectors и порядок операций внутри sector.

Global `A(y); Z; literal_inverse(A(y))` и два source marks используют
старое расписание A48. Все 1568 SOURCE slots привязаны к тому же объекту
поля и к прежнему namespace. Birth map не зависит от значения поля:
`n=11893774624`, CODE pair j — `(2+j,11893771936+j)`.
Дополнительных wires или неучтённых private births не вводится.

## 3. Uniform error на полном объявленном DATA fibre

Положим `δ=2^-3460`, `δ_old=2^-3456`, `ε=2^-4096`.
A53 даёт coframe error `<28δ` и CAR half-preparation `<3δ`.
B103 даёт variable-link Julia error `<498δ` (два target/QR слагаемых и
496 настоящих grid rotations), B93 fixed links — `<102δ`.

Coframe и link действуют на непересекающихся address sectors. Каждый
address/CODE SELECT — прямая сумма с точной identity на остальных blocks,
поэтому controlled SELECT error ограничен максимумом `498δ`, а не числом
sectors. Цена при этом содержит все sectors.

С прежней сертифицированной prefix error `e_pre` имеем

    e_Omega = e_pre + 498δ,
    L = 3^9,
    e_half = 2^-9841 + L e_Omega + [2L + 23(2L−2) + 1] ε,
    e_Choi = 4 e_half + 2δ_old,
    e_CAR = 24δ_old + 43ε,
    e_SITE = 18δ_old,
    e_SOURCE = 1440 e_Choi + 128 e_CAR + e_SITE < 2^-3423.

CAR estimate намеренно сохраняет полную прежнюю оценку обоих preparations,
фиксированного frame, Fourier и H/X; новое `3δ` сильнее старого `3δ_old`.
Оценки проверяются точной рациональной арифметикой.

Как в A48/B91, norm domain — **все SOURCE DATA и SITE columns** с native
RAW исходным состоянием Choi-private24 и CAR-predicate3. CODE, DATA, old
RIGHT и внешняя система могут быть запутаны. Unused private каждой
следующей копии остаётся canonical; гибридная телескопическая оценка
применима. Arbitrary dirty private inputs не объявляются допустимыми.

## 4. Uniform inventory и положительная G/CX реализация

Все выбранные угловые степени имеют фиксированную верхнюю границу q своей
сертифицированной сетки. Поэтому число native calls ограничено одной
целочисленной величиной независимо от поля. Число итераций вычисления
углов конечно, но не считается числом физических G/CX edges.

Для fixed link sector отдельно воспроизведена B93 `bound(0, False)`:
96 Fock pairs с intrinsic inverses, два controlled-X/phase terms и четыре
diagonal terms. Старый variable inventory не добавляется к emitted word.
Для нового variable bank применяется B103 `256·4096·496` upper с q29,
всеми Walsh masks и максимумом восьми CX permutations на плоскость.
Для coframe/CAR используются upper A53 с оплаченными intrinsic inverses.

Native adapter budget сохраняет каждое forward/inverse вхождение. В сумму
входят полные RAW/reflection/vacuum/site слова и все SOURCE copies.
Независимый подсчёт по actual global slot list совпадает с агрегированной
формулой семи банков плюс восьмого f/q bank.

Для forward A добавлены восемь REPORT, REPORT RAW, оба resource frames и
SC6/port inverse. Для core используется `W=A+inv(A)+2 SourceI`.
Исходный A29 compiler сохраняет каждую SourceI pair/closed CZ и старый
helper; число approximate base rotations не больше `8 W_SourceI`.
Следовательно,

    e_replace ≤ 8 W_SourceI · 2^-20000 < 2^-15800.

С теми же восемью REPORT macro errors получены равномерно

    full SOURCE G/CX prefix error < 2^-3423,
    canonical compressed comparator error < 2^-3421.

Новый global G/CX core имеет **верхнюю** оценку числа calls с bit length
24272. Это не точная неоплаченная стоимость и не clocks A49. B105 может
взять эту общую верхнюю границу и вывести настоящее слово с дополнением
identity до общей длины; тогда новая длина и новые часы относятся уже к
действительно дополненному слову.

## 5. Что проверено и что остаётся

Проверены все source slots и depths 0/1/2, соответствие всех link groups
исходным шести coordinates, отсутствие overlap fixed/variable, настоящий
splice обоих провайдеров и literal inverses на noncommuting fixtures,
новая adapter recursion против исходного native DAG на малых уровнях,
полное расписание и оба marks, slot-by-slot inventory, точные error
inequalities. Actual новые coframe/CAR unit trees и все 496 плоскостей
одного общего Julia sector проходят G/CX compiler на global wires с
depths 0/1/2, без записи в CODE/oldRIGHT. Production-sized mask spaces и
всё гигантское слово не развёрнуты.

Это подстановка в **конечную конструкцию представителя**, а не физический
вывод поля. Остаются новый actual M(y)-dependent post и общий clock,
привязка к исходному fine instrument/retained suffix, все независимые
upstream equations, physical V_h/right-lift и действительная same-execution
Cost−Info связь. На `y≠0` нельзя переносить нулевые строки старого центра.
После stationary reduction A37/B73 остаётся настоящий moving-source
член `2 Re<Mχ,(dM)χ>`; никакая точность компилятора его не обнуляет.
