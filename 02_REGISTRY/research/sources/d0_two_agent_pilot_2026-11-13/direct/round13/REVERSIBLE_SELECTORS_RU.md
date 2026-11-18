# A13. Исполнимые обратимые схемы всех A12 palettes

Фаза — реализация существующего источника H.1. Вход — три точные A12 prefix palettes, без изменения их весов, `Lambda_h`, вероятности READY или числа исходных coins. Потребитель — исходный source-sign processor и его report. Устранён один конкретный пробел A12: сравнение с thresholds, декодирование Golden prefix и выбор первой успешной **метки** больше не являются нераскрытыми Boolean oracle.

`reversible_selectors.py` выдаёт последовательность только `X`, `CX`, `CCX` с целыми адресами проводов. Все циклы и thresholds зависят от фиксированного файла схемы; Python не ветвится по квантовому входу. Три полные конечные грамматики схем записаны в `*_CIRCUIT.json`; `selector_word(plan)` разворачивает их в элементарные логические gates. Полный плоский поток из миллионов gates не сохранялся и не исполнялся целиком на большом пространстве.

**Это логический gate basis, ещё не полный native word D0.** Для `CX` есть непосредственный primitive, для остальных операций и их полного физического учёта остаются условия. Требуется computational-zero scratch; возможность получить его из RAW births с правильной оплатой проверяется отдельно. `GR_closed=false`.

## 1. Полное обратимое отображение

Для произвольной исходной метки palette j, всех n Golden bits g, r fair bits f и произвольного output y схема даёт

```
|j,g,f,y,0_work> -> |j,g,f,y xor decode(j,g,f),0_work>.
```

Нижние output bits содержат индекс выбранного label, старший — READY. Abort и неиспользуемые бинарные значения j имеют code0. Исходные j,g,f не изменяются **ни на одном gate**, включая реализацию отрицательных контролей; output и work — отдельные адреса. Неиспользованный Golden suffix остаётся на своих исходных wires. Поэтому схема определена на любой суперпозиции и при корреляции этих входов с внешней системой. Она не трассирует retained coins и не утверждает, что их post-READY состояния одинаковы для разных j.

## 2. Отрицательные контроли без изменения входа

Равенство register одному fixed pattern реализовано цепью конъюнкций на чистом scratch и её обратным проходом. Для двух literal controls, например,

```
t xor= (1-a)b:       CX(b,t); CCX(a,b,t),
t xor= (1-a)(1-b):   X(t); CX(a,t); CX(b,t); CCX(a,b,t).
```

Это точные Boolean тождества; gates имеют не более двух контролей. Промежуточные произведения записываются на отдельные work wires; они не зависят от изменяемого target. После его toggle обратная цепь точно очищает work. Никакие multi-controlled gates не объявлены бесплатными primitive.

## 3. Сравнение целого числа с threshold

Регистр x хранится младшими битами вперёд. Для вычитания constant t вводятся scratch borrows `b0=0`. На i-м бите

```
t_i=0: b_(i+1)=(1-x_i)b_i,
t_i=1: b_(i+1)=1-x_i+x_i b_i.
```

Первый случай раскрывается в `CX(b_i,b_(i+1)); CCX(x_i,b_i,b_(i+1))`; второй — в `X`, `CX`, `CCX`. При чистых новых borrow wires это вычисляет обычный unsigned subtraction, следовательно последний borrow равен `[x<t]`. Он копируется XOR на designated target, затем весь borrow pass обращается. Равенства доказаны для обоих значений каждого бита, независимо от ширины; target может быть произвольным. Threshold0 — identity, `2^width` — один X.

В действительных схемах ширина до 1580 bits. Correctness не выводится из перебора `2^1580` колонок: используется эта индукция по borrow, а реальные широкие edge cases дополнительно выполняются элементарным gate interpreter.

## 4. Полный prefix и таблицы интервалов

Для n=0,1,6 перебраны все raw Golden strings. Prefix заканчивается при первом суммарном exponent не меньше n. Его тип k∈{0,1} и lexicographic rank вычисляются read-only truth-table circuit из описанных literal toggles. Все rank/k scratch затем очищаются обратным circuit. Это маленькая полная таблица, а не вероятностное приближение.

Индекс, сравниваемый с A12 thresholds, равен `rank·2^r+fair`; это простое соединение bit registers, без сложения. Для каждого j,k имеются cumulative boundaries t_i между соседними labels с binary codes c_i. Код abort c_last=0. Output обновляется как

```
output xor= XOR_i ([index<t_i] * (c_i xor c_(i+1))).
```

Если index попал в интервал label ℓ, истинны ровно suffix-предикаты i≥ℓ; XOR телескопируется в c_ℓ. Нулевые длины дают одинаковые boundaries и корректно сокращаются. Read-only equality flag `[j=j0,k=k0]` ограничивает каждую row. Для невыбранной row все выходные toggles выключены, оба вычисления полностью обращаются. Поэтому обход **всех** rows является одним fixed circuit, корректным и при coherent j.

Проверены все 5170 rows (обе prefix kinds для 25+512+2048 partitions). Полное gate исполнение prefix на каждом из 67 raw strings n=0,1,6 и точная сумма retained-suffix масс в Q(p) подтверждают capacity и исходную A12 probability. Следовательно на stated clean-work domain логическая схема сохраняет ранее доказанный scalar READY; этот вывод не включает физические ошибки или дополнительные factories.

## 5. Первая успешная метка

Для cap7 и выходных меток ширины6 (internal) или2 (top) выпущены отдельные схемы. Вначале вычисляются

```
c0=1,
chosen_i=c_i & ready_i,
c_(i+1)=c_i xor chosen_i.
```

Chosen flags взаимоисключающие: первый success имеет1, все позднейшие0. Output label получает XOR от `chosen_i & label_i`, READY — XOR chosen. После этого весь вспомогательный проход обращается. Все семь входных attempts выполняются и сохраняются; ни раннего останова, ни удаления failures нет.

Схема копирует вычислимые basis labels когерентно; это **не копирование неизвестного квантового payload**. Fair-bank resource `|+>` нельзя получить CNOT-копированием его амплитуд на пустой output: так возникла бы корреляция вместо отдельного `|+>`. Его собственная controlled routing/swap процедура остаётся обязательной. Полный source-DAG stack/offset interpreter также пока не выпущен: здесь j предоставлен на входе конкретного decoder.

## 6. Счёт и проверка

| Один fixed decoder | Wires | X | CX | CCX |
|---|---:|---:|---:|---:|
| internal |2768|478828|1089222|1089479|
| top/type×SITE |3185|3478720|19440642|19454976|
| ten-sign report |229|691540|3323278|3398086|

Включены полные прямые и обратные вычисления каждой row и каждого scratch. Для fixed 1054 slots, cap7 и10 top choices суммарный **логический decoder/label-routing** счёт на report: X=3776997052, CX=9400485374, CCX=9403481772. Это консервативная конечная конструкция, а не оценка практической эффективности и не physical Cost. Births, fair preparation, native gate compilation, DAG interpreter, selected involutions, H tests, marks и clock сюда не добавлены.

`check_selector_circuits.py` исполняет primitive gates: все малые equality/comparator inputs с произвольными target/spectator bits, все1024 columns небольшой полной palette-схемы (включая unused j и retained suffix), все действительные Golden prefix columns,500 actual-width row cases,1064 first-success cases. Для огромных схем все строки сверены структурно; счёт gates проверен по раскрытым row blocks. Проверки не являются Lean formalization или полным перечислением квантового пространства. Exact Boolean induction и композиция обратимых maps дают общий вывод при stated inputs.

Воспроизведение из root checkout: `python3 -B -W error .../round13/build_selector_circuits.py`, затем `check_selector_circuits.py`. Это пишет только пакет A13. Перед независимым replay следует использовать отдельную копию A12/A13.

Остаток до actual H.1: compile source-DAG dispatch/copy offsets и quantum payload routing; подставить реальные primitive words и ограничения порта, подготовить нулевой scratch из оплаченных births; получить full READY, all-column/marked-prefix transport и clock, затем связать исходный физический Cost−Info. Текущий результат не меняет `physical_C_closed=false` или `GR_closed=false`.
