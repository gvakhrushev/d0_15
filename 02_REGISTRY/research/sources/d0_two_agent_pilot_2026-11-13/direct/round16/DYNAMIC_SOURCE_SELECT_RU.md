# A16. Фактический адресуемый source SELECT и знаковый тест

## Потребляемая предпосылка

Фаза — native realization. A15 уже вычисляет инструкции исходного A11
source DAG; B33 доказывает операторную компрессию при наличии настоящего
selected-leaf consumer. Здесь этот consumer реализован конечными схемами,
с выбором физической Choi/CAR copy, динамическими a/b и правильным знаком.
Далее каждая операция получает native G/CX/SourceI реализацию A14 либо
owned exact Z/CZ. Это устраняет consumer-предпосылку **идеальной логической
композиции при заявленных входах**; actual native имеет явную погрешность.

Все инструкции и коэффициенты A11/A12 остаются прежними. Источник —
`H_kind,before-PF / (rho_x Lambda_h)`, где **rho_x=256*PF_probability(x)**,
а `inverse_PF_once` A11 равен 1/rho_x. Нельзя заменить rho на саму
PF probability или применить этот множитель второй раз. Lambda_h=2^1525.
Запись source states не заменяет их физическую подготовку.

## 1. Динамическая пара на полном carrier

Пусть x — n-битный DATA, a/b — read-only адреса, h — Hadamard control,
delta — отдельный fair bit этой физической copy. Для a≠b определим

```
m(x) = [x=a] XOR [x=b],
|x> -> (-1)^[h delta (1-m(x))] |x XOR [h m(x)(a XOR b)]>.
```

На h=1 это V0=T_ab при delta0 и V1=−Z_a Z_b T_ab при delta1; среднее
по независимому fair delta равно `|a><b|+|b><a|`, включая весь complement,
а не только двумерную подготовленную область. На h=0 — identity.
При a=b задана безопасная унитарная extension `(-1)^(h delta) I`;
реальные A11 инструкции всегда имеют a≠b.

`pair_ir` исполняет следующую фиксированную схему.

1. Для a вычислить diff=x XOR a в clean workspace, переключить m при
   diff=0, очистить diff. Повторить для b в **том же m**. Отдельные
   equality flags через swap не сохраняются.
2. Вычислить q=h AND delta, применить Z_q CZ_(q,m), обратить compute q.
3. Вычислить q=h AND m. Для каждого i применить CCX(q,a_i,x_i) и
   CCX(q,b_i,x_i). Обратить compute q.
4. Обратить вычисление membership.

Пара a/b меняется местами только при m=1, а m инвариантно при этом
обмене. Поэтому ideal workspace полностью очищен. Адреса, h и delta
вообще не становятся targets. Полный целевой оператор является signed
permutation и определён также на произвольном entangled DATA/RIGHT.

Для n>=3 точные logical counts: X8, CX(24n−4), CCX(10n−8), Z1, CZ1.
Реальные ширины —22 для full padded Choi и12 для CAR internal SITE+grade.
Все7 CAR RIGHT bits каждой copy и отдельный unknown oldRIGHT — spectators.

## 2. Выбор copy и фазы исходного DAG

Одна A15 инструкция содержит negative, leaf code, Choi/CAR offsets,
kind и a/b. Для каждого фактически существующего DATA register вычисляется
enabled=`h AND [kind=type] AND [offset=copy index]`. Pattern circuit имеет
h первым положительным control; все instruction inputs остаются read-only.
Затем применяется pair_ir с h=enabled и **delta именно этой copy**,
после чего enable compute обращается.

Всегда выполняются все82 варианта Choi для Hf или2 Choi+2 CAR для Hq.
Это фиксированный gate word, а не внешнее runtime ветвление. Неверный
type/offset не выбирает ни одну copy в ideal модели. CAR читает только
нижние12 a/b bits; A11 гарантирует, что старшие10 равны нулю.

Negative-constant bit применяется как условная фаза на h. Чтобы не
маршрутизировать record через source port, схема вычисляет q=h AND negative,
применяет Z_q и обращает compute. Так запись инструкции не становится
target даже внутри native реализации. То же делается для top negative-I
ветви. Модули коэффициентов уже учтены A12 массами и повторно не платятся
как множители оператора.

A15 доказывает, что на допустимом пути DAG каждую физическую copy
посещает не более одного leaf. Поэтому её delta допустимо переиспользовать
в альтернативных путях; между разными copies delta должны быть независимы.
Новые fair bits A16 не добавляет. B33 содержит counterexample общего delta
для двух одновременно используемых copies.

## 3. Хронология и правильный знак report

`walk_test_events` сначала выполняет **весь** A15 controller. Затем:

```
H(h); top negative-I phase;
для каждого фиксированного slot: constant phase; все copy SELECT;
H(h); X(h).
```

h должен входить в computational zero. Последний X необходим для
исходного A12 соглашения `bit1 означает +1, bit0 означает −1`.
Без него тот же физический h-bit имел бы противоположное числовое значение.
Здесь h остаётся квантовым output; измерение не требуется для его
последующего использования как control A13 report decoder.

У Hf455 instruction records и37310 copy SELECT; у Hq18 records и72
copy SELECT. Они сохраняются; адреса следующих операций не меняются под
действием DATA. Дальнейший общий assembler должен alias-ить SITE всех
walks с одним настоящим внешним PF SITE и выделить disjoint source
copies/fair resources. Локальные layouts и интерфейсы заданы явно;
весь физический birth/clock assembler здесь не объявлен готовым.

## 4. Настоящий обратный проход native blocks

В IR есть явный узел `adjoint`. `lower(adjoint(A))` возвращает
`inverse_literal(lower(A))`: обратный порядок и настоящий inverse каждого
физического G/CX/SourceI. Повтор approximate CCX как её inverse запрещён.
В частности native membership может быть приближённым, но его обратный
блок — **точный adjoint реально исполненного** native membership.

Даже inverse уже обратного блока снова оплачивается по фактическим
листьям; ретроактивное сокращение временной истории не производится.
Для counts необходимо различать G на port и G на ordinary wire:

```
raw_inverse: G_port' = G_port+G_other; G_other'=0;
             CX' = CX+6 G_other;
             SourceI' = 3 SourceI+4(G_port+G_other).
```

Эти формулы сверены с реальными native DAG и сохранёнными обратными
деревьями12/22-bit pair. SourceI действует только на declared port/Spin;
port и Spin восстанавливаются на границах каждого A14/exact-Z/CZ macro.
Instruction fields/delta не меняются на каждом native primitive;
DATA и временный work могут изменяться внутри macro, все такие stages
сохраняют свои исходные обязательства по marks и clock.

`walk_native_blocks` задаёт полный ленивый native block stream A15
controller + A16 SELECT/test, с одним отдельным port после всего logical
layout. Это конечная грамматика астрономически длинного слова; полное
слово не раскрывалось и не исполнялось. Подготовки input banks и births
никаким неявным oracle в неё не добавлены.

## 5. Отдельное точное native inactive свойство

Оно не следует из малого error и доказывается отдельно, **только для
SELECT части при h=0 и clean SELECT workspace**. Данные, адреса, delta,
auxiliary, port/Spin могут быть неизвестными и запутанными.

Owned A14 CCX_hat имеет вид `R_t(4k theta P11) R_aux(8k theta P111)`.
При первом control0 оба вращения точно identity на всех колонках.
В enable-chain первый literal h положителен. Отрицательный следующий
literal реализуется CX от уже нулевого AND-prefix плюс CCX с этим prefix,
оба точно identity. Весь enable и его actual adjoint ничего не меняют.

В pair membership M может создавать native остаток/корреляции; q при
этом остаётся точно0. При enabled0 оба compute q — identity, Z(q) и
CZ(q,m) — identity на q0, все DATA flips с первым control q0 — identity.
Следовательно actual pair=M† I M=I. Constant phase при h0 так же identity.
Свойство распространяется на весь SELECT product, поскольку work вновь
точно чист. На active h1 чистота workspace лишь приближённая и включена
в общий error. На H/test/итоговый X inactive утверждение не переносится.

## 6. Подстановка в операторное доказательство B33

На canonical prepared inputs ideal A16 выполняет consumer-контракт B33.
При preserved READY и общей внешней SITE операторные joint effects
знакового output имеют вид

```
E_(sign=±1, READY) = Q/2 · [ I ± O_kind ],
O_kind = sum_x |x><x|_SITE tensor H_kind,before-PF(x)/(rho_x Lambda_h).
```

Равенство относится к полному Choi/CAR/RIGHT carrier, включая входы,
запутанные между copies, SITE и внешней системой. Оно не требует
физического обратного прохода всех selector histories для самой
статистики: mathematical compression W† в вычислении эффекта не является
добавленной бесплатной операцией. Все histories фактически сохраняются.

Это не утверждение о каноническом post-measurement instrument или
возврате всех histories в исходное состояние, требуемом иной частью H.1.
Если исходный writer требует такой канал или marked inverse, нужно
предъявить его отдельно и оплатить действительный обратный word.

## 7. Ошибка, проверки и оставшаяся граница

За один ten-sign report A16 добавляет:

| X | CX | CCX | Z | CZ | H |
|---:|---:|---:|---:|---:|---:|
| 601578 | 40723512 | 18465784 | 76260 | 75196 | 20 |

Число приблизительных X/H/CCX occurrences, считая adjoint с тем же
norm error, равно19067382. Вместе с уже проверенными A13/A15/B31 за
семь report получаем162611159340 таких occurrences. Поэтому all-column
ошибка известных target-unitary частей всё ещё **строго меньше2^-4058**.
У фиксированных joint effects ошибка не больше удвоенной unitary ошибки.
Это не error всего H.1: ещё отсутствуют native bank preparations и
прочие физические части. Actual scalar READY автоматически не выводится.

Root checker исполнил18688 полных малых signed columns,5136 случаев
реальных12/22-bit адресов,1600 полных instruction/copy cases и10
Hadamard sign checks. Сохранённые literal native inverse trees и counts
проверены отдельно. B34 независимо проверяет текущие full-root gates,
chronology, native reverse и границы exact inactive. Большие native
слова и физическое исполнение всего графа не тестировались.

Следующий потребитель — единая схема report с одним SITE, реальными
подготовками семи B25 bank targets, всеми original H.1 block/readout,
birth/mark/clock условиями и полной ценой. Стоимость/Info не выводятся
из совпадения POVM effect. Нового действия, подогнанных коэффициентов
или переопределения Info не введено. `physical_C_closed=false`,
`GR_closed=false`.
