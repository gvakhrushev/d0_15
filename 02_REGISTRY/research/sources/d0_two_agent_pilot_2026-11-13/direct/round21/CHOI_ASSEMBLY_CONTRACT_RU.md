# A21. Полный Omega и half-vector на одной namespace

Построены конечные native generators полного controlled Omega loader и
когерентного half-vector U. Входы: A19 prefix (commit b3374e74b), A20
coframe SELECT (afbaef2f9), B42 proper-link SELECT (f4deec43d) и B39
fixed-point adapter (562fac0a4). B43 (0f9fd679c) независимо подтвердил
новую A20 библиотеку целиком. Root отдельно воспроизвёл итоговую B42
native-грамматику, полную32-колоночную диагностику и resource receipt.
Следующий потребитель U — исходный B35 full reflection; сам внешний
reflection и полный оригинальный RAW Choi bank в A21 ещё не реализованы.

## Полный controlled Omega loader

Хронология: A19 actual controlled prefix, A20 coframe SELECT, B42
proper-link SELECT. Coframe и link программы точно I вне своих
address/SAM patterns, поэтому их полные endpoints — ортогональные
address blocks. Полный SELECT norm error — max двух bounds, хотя
оплаченные последовательности и ресурсы складываются без сокращений.
Подтверждённый B42 bound `101*2^-3264` даёт всему SELECT `<2^-3257`,
а с prefix `<2^-4091` полный loader удовлетворяет B39 `<=2^-3250`.
`CHOI_LOADER_PLAN.json` хранит точные рациональные числители/знаменатели
суммарных bounds, actual source pins и отдельные native inventories
полных Omega, U и их буквальных обратных ходов для каждого bank.

Branch0 должен быть точно I на всех остальных проводах; branch/SAM
не пишутся примитивами. Address read-only внутри SELECT, но исходный
prefix его подготавливает. Нет private loader work. Arbitrary aux не
переиспользуется как phase rebit или comparator. RAW birth/cost остаётся
отдельным от unitary anchor contract, где DATA на входе равен `0^22`.

## Одна явная namespace

Сохраняется A19 binding:

- SAM 0..2687;
- DATA address 2688..2699, Choi input 2700..2704, Choi output 2705..2709;
- Julia occupation 2705..2708, Julia t=2709;
- branch=2710, port=2711, Spin=2712/2713, arbitrary aux=2714;
- oldRIGHT witness=2715;
- B39 phase rebit=2716, comparator flag=2717, comparator work=2718..2738.

B39 `data` — все 22 DATA, `start_controls` — branch и DATA,
`V_private=[]`. Его private output имеет **24** wires: branch, phase
rebit, flag и 21 comparator work. Они должны возвращаться к 0 с полным
coherent error B39; нормировка хорошей ветви и retained failure входят
в error. SAM/port/Spin/aux/oldRIGHT — произвольные внешние факторы.
Дополнительные SITE/RIGHT, если потребитель их именует, должны быть
явно добавлены как untouched external factors, не как clean private.

## B35 reflection требует отдельного scratch

Для `u_b`-preparation U выходной joint anchor имеет DATA22 + U-private24
=46 контролируемых нулевых проводов. Внешний predicate comparator,
который реализует joint reflection, **не может** использовать B39
private comparator как свой target/work: эти 24 wires входят в сам
проверяемый anchor. Для стандартной clean pattern конструкции K=46
нужны ещё flag+44 work=45 отдельных чистых wires, например 2739..2783.
U/loader обязаны быть тождественны на всех этих дополнительных wires.
Точный bound и inventory reflection потреблять из исходного B35/A13,
не считать приведённое число само по себе доказательством подготовки.

## Исходный вектор и операторная оценка

В идеальном prefix DATA после22 нулей равен
`sum_a|a>/sqrt2049 ⊗ sum_i|i>|i>/sqrt32`, `0<=a<=2048`.
Объединённый исходный SELECT применяет `J_a(b)` к последним пяти битам;
значит output равен именно `Omega_b[a,i,j]=J_a(b)[j,i]/sqrt65568`.
Все J ортогональны на32 колонках, поэтому норма Omega точно1. При a=0
J_0=I32, следовательно `<r,Omega_b>=1/sqrt65568` с одной положительной
фазой для всех b. Padding не добавляет амплитуд в идеальный вектор.

Actual loader приближает весь исходный оператор с ошибкой `<2^-3250`,
поэтому удовлетворяет B39 uniform anchor isometry contract для
произвольных SAM/aux/port/Spin/external factors. Branch0 у actual word
точно I. Loader не адресует отдельные rebit и comparator на всём
пространстве, что необходимо для B39 clean-prefix hybrid и его
anchor-only Lipschitz оценки. В итоге actual U при DATA=r и24private=0
приближает `u_b⊗0^24` с ошибкой `<2^-3230`. Это не полная operator-норма
сравнения U с произвольным unitary extension и не assertion чистого work
после любого входа U. Именно joint-anchor isometry достаточно для
следующего B35 reflection.

## Ленивый интерфейс и буквальные inverse depths

Полные source SELECT содержат слишком много Walsh terms для одного
materialized Python `seq`. Это не позволяет заменить их новым oracle.
Используется конкретный bounded generator каждого actual native block с
прикреплёнными кодом, source-library hashes, диапазонами sector/mask и
точными resources. Адаптация B39 принимает этот конкретный provider,
сохраняя ровно свою хронологию и literal inverse каждого leaf. Нет
неопределённой команды «загрузить Omega»: каждый вызов разворачивается
в те же finite loops и source-specific actual G/CX/SourceI blocks.

Для глубины inversion d: порядок blocks обращается по нечётности d,
а **каждое** native tree обращается буквально d раз. Внутренние depths
coframe/B42 не обнуляются. Цена определяется T^d, где
`T(Gp,Go,CX,S)=(Gp+Go,0,CX+6Go,3S+4(Gp+Go))`.
Нельзя передать XOR вместо количества inversions и затем утверждать
буквальную цену уже выполненной обратной последовательности.

В принятой B42 версии внутренний Fock lift хранит integer depth:
sign-positive F† имеет depth2, а внешний bank reverse — depth3.
Root воспроизвёл финальный nested test и пересчитанные ресурсы; endpoint
matrix comparison сама по себе не доказывала бы эту paid history.

Проверка A21 охватывает все38144 неякорных source sectors семи bank,
294144 coframe units и1781504 proper-link commands с теми же wire
numbers, что в их владельцах. Контракт loader и B39 проверен на одной
namespace. В девяти точных toy replays (levels0/1/2, outerdepth0/1/2)
ленивый provider даёт примитив-за-примитивом тот же word, что исходный
B39 one-DAG interface. Это проверяет новую форму представления; full
огромный level8 word не исполнялся. Структурная индукция по bounded
генераторам и inverse depth распространяет равенство на полные размеры.

После coherent U и B35 full bank всё ещё остаются первоначальные
vacuum/Fourier/SITE, фактическая H1 marked history, alpha, preparation /
oldRIGHT / clock / work и полная исходная Cost−Info. Не подменять их
успехом finite compiler. `physical_C_closed=false`, `GR_closed=false`.
