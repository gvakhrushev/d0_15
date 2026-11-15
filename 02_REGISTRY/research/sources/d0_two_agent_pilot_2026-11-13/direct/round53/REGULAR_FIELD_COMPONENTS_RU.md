# A53: свободные полевые входы и реальные coframe/CAR компоненты SOURCE

Вместо обращения к сохранённой таблице одного центра теперь можно передать
**2688 независимых точных рациональных смещений центра** и получить новые
native coframe/CAR слова для соответствующего поля. Используется тот же
исходный B21 chart, те же B25 targets, addresses, четыре значения CODE,
канонические входы и retained outputs. Допуск определяется геометрией
старого регулярного chart; уравнение Эйнштейна не проверяется при допуске.

Это реальные параметризованные **компоненты** SOURCE. Proper-link
компонент разрабатывается в B103. Их совместная новая G/CX сборка, actual
post, padding/clock и полный physical source ещё не собраны. Старый A49
clock не присваивается новым словам; `physical_C_closed=false`,
`GR_closed=false`.

## 1. Явная область поля, без замораживания координат

`FieldCentre` принимает в исходном B21 порядке 1024 inverse-coframe,
1536 proper-link и 128 matter coordinates. Пусть y_j — смещения от
прежнего центра Y0. Область нового конструктора:

    |y_j| < 2^-32,  j=0,...,2687.

Boundary sites и исходные reference banks остаются boundary/task data.
Ни один внутренний coframe, link или matter coordinate не связывается
здесь с другим или с Einstein residual. Слово зависит от finite имени
поля; отдельно заданные CODE digits b_j∈{0,1,2,3} дают

    Y_(y,b),j = Y0,j + y_j + σ(b_j−3p²),  σ=2^-80.       (1)

Поскольку `3/8<p²` и `3/8<1−p²`, точная рациональная оценка

    2^-32+3·2^-80 < (3/8)·2^-30

помещает ВСЮ новую область и все CODE assignments строго в прежний
асимметричный B21 cube. Потребляются существующие B91 bounds, включая
regular coframe, CAR slack, positive Julia defects и full SOURCE M1/M2.
Не проводится новый поиск геометрического решения.

Выполнено и прямое интервальное включение на всей коробке: 7168 coframe
templates (2048 current и 5120 reference), все четыре CAR time slices.
Для свободной строки в интервал сразу добавлена вся `±(2^-32+3σ)`;
это не выборка нескольких полей. Все coframe norms <1, выбранные
элиминационные радиусы >0 и ≥ половины нормы; CAR `||ψ||²<1/15` и
slack `1−p−||ψ||²>1/3` сохраняются.

Рациональное имя — конечный вход. Оно не выдаётся за точное представление
каждого действительного поля. На этом выпуклом chart для рационального
приближения с `max_j |y_j−y'_j|≤η` B91 непосредственно даёт

    ||B̃(Y)−B̃(Y')|| < 1748·52η <2^17η,
    ||DB̃(Y)−DB̃(Y')|| <3233036·52η <2^28η.              (2)

Это оценки идеального полного SOURCE на его исходном all-DATA / canonical
private fibre; fixed retained processor их не увеличивает. Так конечное
имя может приближать computable regular field с явно оплачиваемой
погрешностью. Производная дискретного compiler index из (2) не выводится.
Полная Book01 finite-section и physical V_h перенос остаются отдельно.

## 2. Coherent coframe и CAR, с прежними input columns

Для current coframe столбца исходная vector formula A20/A48 дополнена
четырьмя выбранными y_j в порядке исходных component indices. Для current
CAR пара `(ψ0,ψ15)` дополнена двумя y_j того же site. Аффинное действие
на параметры проверено точно в interval arithmetic; references и boundary
векторы не меняются. Условные операции по address и CODE остаются
когерентными: поле не измеряется для выбора ветви.

Coherent coframe emitter потребляет исходную A20/A48 факторизацию
creator Julia32 на три mode rotations, их Fock lifts, base Julia rotation
и controlled X с arbitrary aux. Новая программа всегда выводит все три
mode rotations. CAR half-vector всегда использует прежние три planes
`(1,14),(1,0),(1,15)`. Exact-zero oracle для deciding пропуска rotation
не нужен. Последующие fixed vacuum/Fourier и full CAR frame имеют прежние
цели, но здесь их новая общая сборка не объявляется уже выполненной.

Layout и predicates взяты из A48: максимум 24 controls для coframe plane,
25 для phase части X, 15 для CAR. Дополнительных private births нет.
Цель coframe относится ко всем 32 Julia columns, CAR preparation — ко
всем 16 grade columns, с теми же external spectators. Это не новая
гарантия для произвольного dirty SOURCE-private входа всей A22/A24
подготовки; её исходная canonical fibre сохраняется.

## 3. Uniform Golden grid вместо таблицы углов одного центра

`UniformAngles(24)` и `(15)` потребляют уже доказанные B93 grids для
реального orbit `G^(2^K k)`. Код заново сверяет исходный B80 SHA,
`gcd(p_n,q)=1`, полный interval `q·|q2^Kγ−p_n|<1` и `16/q<2^-3460`.
Для каждого требуемого exact unit-circle target берётся outward interval.

Выбирается компонент с сертифицированным модулем больше 3/5; такой
компонент существует, поскольку максимум точных |cos|,|sin| ≥1/√2.
Отношение меньшего к большему после уточнения лежит в (−2,2); один
half-angle переводит его в область собственного A41 atan series. Знак
большего компонента задаёт quadrant, без сравнения угла с точной границей
ячейки. Когда ширина turn interval ≤1/(2q), округляется его середина и
применяется exact modular inverse p_n modulo q. Нулевой k заменяется q,
так что исполняются только положительные Golden powers.

Интервалы целевых формул сходятся; coframe/CAR denominators и выбранные
радиусы имеют доказанный положительный запас на области (1). Поэтому
выбор конечен и при нулевом sine, отрицательном cosine и совпадении с
границей rounding cell. Float guesses в новом selector не участвуют.
Каждая полная controlled rotation имеет uniform operator error
`<2^-3460` относительно её исходной точной цели.

Phase часть X использует удвоенный тот же exponent: её error <2δ,
первая rotation <δ. У controlled X вместе <3δ. Поэтому один coframe
sector имеет error `<(24+1+3)δ=28δ<2^-3455`; одна CAR half-vector
preparation — `<3δ<2^-3458`, где δ=2^-3460. Это all-column estimates.
Разные address/CODE sectors являются ортогональными блоками, и native
Walsh word точно тождественен вне своего predicate в SourceI profile.
Поэтому полная SELECT error — максимум ошибок секторов, не их сумма.

Напротив, **стоимость** включает каждый неактивный сектор. В receipt
даны покомпонентные upper counts всех loops, с k≤q. Они не называются
реальной длиной ещё не исполненного unpadded word. В каждом coframe
sector 27 actual units, часть уже имеет literal inverse depth 1;
счётчик учитывает это. Higher inverse depths не сокращаются по модулю 2:
только порядок обращается по parity, а все настоящие inverse macros
остаются. Проверены depths 0,1,2 и реальное построение DAG leaves.

Профиль этих компонентов всё ещё содержит SourceI. Общая A29 G/CX
замена требует нового суммарного upper и новую фактическую плату.
То, что исходный target при y=0 совпадает со старым, не делает новые
native words или их clocks равными старым A48/A49.

## 4. Проверки и потребление результата

Проверены каноническое кодирование finite field names, отказ float/Boolean
и точной границы открытого chart, вся interval margin-коробка, 27
семантических случаев полевого смещения и 56 **фактических** больших
Golden powers независимо через complex-ball возведение. Последняя
проверка — выборочная; универсальная точность следует из grid theorem.
Дополнительно 30 inverse inventory сравнений и 48 реальных native DAG
деревьев. Полное гигантское SOURCE не исполнялось.

Снятая предпосылка: coframe/CAR не требуют заранее сохранённой lookup
таблицы единственного поля и не исключают regular значения из-за
проверки точного нуля. Это позволяет собирать один off-shell reference
constructor. Для него ещё нужно включить B103 proper links, согласовать
все local-to-global addresses, пересчитать whole SOURCE error/inventory,
повторно построить actual centre post и общий paid clock. Все четыре
independent controls, настоящий initial cut, fine response/suffix,
physical V_h/right lift, полный Cost−Info source и GR refinement остаются
потребителями, а не следствиями одного этого локального compiler.
