# A15. Конечное обратимое управление исходным tensor DAG

## Утверждение и место в аргументе

Фаза — native realization. Родительская предпосылка A12: фактический конечный
controller должен выбирать ветви исходного A11 tensor DAG, вести отдельные
Choi/CAR copy offsets и выдавать правильный leaf instruction, не используя
бесплатное классическое вычисление во время квантового исполнения.

Эта предпосылка на уровне **вычисления инструкций** теперь имеет явную
фиксированную схему X/CX/CCX и подстановку конечных G/CX/SourceI слов A14.
Схема включает хронологическое соединение с семью A13 selector attempts и
first-success label circuit для каждого top/internal slot. Никакое решение
о следующей физической операции не принимается внешним классическим агентом.
Все ветвления реализованы как quantum-controlled обратимые таблицы.

Фактический SELECT, исполняющий выданную инструкцию на выбранной копии
квантового банка, **ещё не включён**. Также не включены реальные рождения
всех zero-registers, подготовки семи банков, полный H.1 writer, его все
marked prefixes и Book03 Cost−Info источник. `GR_closed=false`.

Входы: A11 `SOURCE_TENSOR_DAG.json`, `PERIODIC_SOURCE_BINDING.json`; A12
`INTERNAL_SELECTOR_PALETTE.json`; фиксированные A13 reversible selectors;
A14 native macros и их all-column certificate. Все носители, исходные
коэффициенты, `Lambda=2^1525`, `epsilon=2^-1531`, внешний PF SITE и семь
исходных report вызовов сохраняются. Пишем только `direct/round15`.

## 1. Стек и точное размещение тензорных копий

Стек состоит из трёхкомпонентных записей `(node, c, q)`: номер узла —
исходный индекс+1, Choi offset — 7 bits, CAR offset — 2 bits. Пустая запись
равна нулю; исходный нулевой узел не достижим из двух корней. При входе в
узел `n` его tensor operator действует с этих offsets; неиспользованные
копии являются identity. Это соглашение совпадает с правым identity padding
в A11, без физической перестановки копий.

* `add`: выбрать один дочерний узел по A12 palette, сохранив оба offsets.
* `mul`: поместить все дочерние узлы в исходном порядке; смещать Choi и CAR
  отдельно на суммы соответствующих bidegrees предыдущих детей.
* `var`: выдать leaf code и текущие offsets, удалить вершину стека.
* `const`: выдать точный знак в Q(p), удалить вершину. Абсолютная величина
  уже входит в массу A12; второй раз она не применяется.
* dummy, invalid label или abort на add: удалить вершину без детей.

Для пустого стека все следующие переходы — dummy. Готовность проверяется
внешней общей READY процедурой, поэтому abort не переименовывается в успех.
Non-add и dummy slots тоже вызывают A13 palette 0 с теми же семью попытками:
нет бесплатного пропуска после окончания выбранной ветви.

Для каждого узла рекурсии максимума visits и stack depth имеют вид

```
V(leaf)=1; V(add)=1+max V(child); V(mul)=1+sum V(child).
D(leaf)=1; D(add)=max D(child);
D(mul(c0,...,cm-1))=max_i [D(ci)+m-1-i].
```

Дети mul обрабатываются слева направо, поэтому при обработке ребёнка `i`
ещё `m-1-i` соседних детей ожидают в стеке. Другие записи вызывающего
контекста просто добавляются к обеим частям оценки. Индукция доказывает
достаточность глубин **11 для Hf** и **4 для Hq**, и лимитов **455/18**
шагов. При abort число детей только уменьшается.

В каждой допустимой ветви различные листья используют непересекающиеся
копии: mul разводит интервалы, add посещает только одного ребёнка. На
нулевой степени возможны совпадающие формальные offsets, но листа на них
нет. За один десятизнаковый report нужны прежние 2×82+8×2=180 Choi и
8×2=16 CAR копий. Для leaf fair delta можно использовать индекс его
физической копии; дополнительные fair coins контроллеру не нужны.

## 2. Реальные фиксированные схемы

`SOURCE_DISPATCH_TABLES.json` содержит конечные QROM-строки, а не oracle.
`lookup_word` раскрывает каждую строку в A13 multi-literal predicate на
X/CX/CCX, вычисление одного флага, CX нужных константных output bits и
обратный порядок вычисления флага. Результат XOR-записывается в output;
inputs не изменяются даже между операциями. Несовпадающие строки не действуют.

Для переходов non-add строки проверяют 15 node bits; add строки —
15 node+6 choice+1 READY. Эти условия попарно несовместны. Все переходы
начинаются с `push0=1`; строка с `k>0` переключает push0 и pushk. Поэтому
получается ровно один push flag на всех input strings, включая invalid.

Для каждого из четырёх возможных детей offset вычисляется настоящим
обратимым двоичным сложением. При нулевом начальном carry

```
sum_i = a_i xor b_i xor carry_i,
carry_(i+1) = a_i b_i xor a_i carry_i xor b_i carry_i.
```

Carry вычисляются тремя CCX, sum XOR-копируется, carry очищаются обратным
ходом. Сложение modulo 2^7/2^2 определено на всех inputs; на допустимых
историях переполнения нет по tensor-degree инварианту.

Новый стек — **новый** zero output register. При push=k его запись i
получает child_i для i<k и old_(i+1-k) иначе. Старый стек сохраняется.
Это reversible compute-with-retained-input, а не необратимое стирание
старого стека. Временные transition/child/carry registers очищаются.
Все новые state/palette/instruction registers остаются частью истории.

`walk_events` даёт точный хронологический порядок и глобальные wire maps:

1. Top palette index = `2*SITE+kind`. SITE wires передаются как read-only
   aliases; для каждого Hq отдельный нулевой kind bit получает оплачиваемый X.
2. Семь top selector схем, first-success label. При label0/READY инициализируется
   корень; label2/READY записывает отрицательную identity фазу. Другие случаи
   стартуют с dummy стека.
3. На каждом фиксированном шаге: node→palette QROM; семь настоящих A13
   internal selector схем; first-success в choice/READY текущего шага;
   вычисление нового стека и инструкции.

Все рабочие входы действительно должны быть computational zero. A13
`v→0` компоненты доступны, но их полная аллокация/RAW birth ledger здесь
не объявлена выполненной. Alias не заменяет подготовку zero или fair input.

## 3. Полные leaf addresses

Адресная таблица использует `(external SITE, leaf code)` и содержит все
**256×282=72 192** строки A11. Она возвращает kind и два 22-bit basis labels:

```
Choi: a=0; b=(catalogue_address<<10)|(input<<5)|output.
CAR:  a=(internal_SITE<<4)|mask_a;
      b=(internal_SITE<<4)|mask_b.
```

CAR никогда не подменяется Choi anchor0. Используются именно два cross_masks
исходного leaf template, включая полную grade15. CAR RIGHT и отдельный
unknown oldRIGHT не адресуются. Внешний PF SITE — общий read-only control,
а не CAR internal SITE и не новая независимая PF выборка.

Instruction содержит negative-constant bit, leaf code, оба copy offsets,
kind, a и b. Дальнейший SELECT должен на выбранной копии исполнить B27
signed pair involution с собственным delta и Hadamard control. Условная
фаза константы тоже должна быть применена к нужному control. Просто выдача
правильного classical instruction ещё не исполняет эту квантовую операцию.

## 4. Counts, native lowering и граница ошибки

Точные дополнительные controller counts за один report, включая top kind
bits, но **без повторного счёта прежних A13 selectors**:

| X | CX | CCX |
|---:|---:|---:|
| 144 939 804 | 6 911 538 816 | 9 281 032 152 |

Один геометрический step: X137514, CX6557437, CCX8805648; один материальный
step отличается только CCX8804808. Полные fixed chronological walk layouts
включая A13 label processing имеют 9 092 041 и 378 128 logical wires.
Сохранять все эти registers экономически тяжело; они не объявлены бесплатными.

`native_walk_macros` подставляет в фактическую последовательность gate
операций A14 DAG на отдельно выделенном port, двух Spin wires и arbitrary
auxiliary, с protected oldRIGHT. Слова конечны, но астрономически длинны;
полный native leaf stream не раскрывался и не исполнялся.

Для каждой приблизительной X/CCX all-column ошибка ≤2^-4096. Таким образом
добавка семи controller вызовов строго меньше **2^-4060**. Native forward
и literal raw inverse inventories сохранены целыми числами. Подлинный
обратный проход обращает фактические native листья; повтор приближённой
CCX вместо её adjoint запрещён. Во forward logical compute/uncompute
применяется обычная A14 пооперационная подстановка, поэтому чистота
временного workspace после native исполнения точна только у идеальной
target схемы; actual residual включён в all-column error.

Ошибка суммируется с A14 selector, B31 fair-router и ещё не реализованными
частями. Это не оценка полного writer и не доказательство actual scalar
READY. В частности, малый operator error не доказывает H.1 exact block
structure; остаётся отдельное условие B29.

## 5. Решающие проверки и дальнейший потребитель

`check_source_dispatcher.py` сравнивает 496166 transition cases с отдельной
рекурсивной семантикой, все72192 адреса и76913 достижимых node/copy placements.
Проверены все16400 inputs сумматоров widths2/7 и254 inputs небольших QROM,
600 полных padded walks с abort/top cases и неповторением копий. Все
хронологические stage maps проверены на инъективность и правильное соединение.

Дополнительно по отдельным X/CX/CCX исполнены два **полных фактических**
step streams для mul arity4 и CAR leaf с ненулевым anchor. Это проверяет
полные таблицы, чистый scratch, неизменность inputs и точные gate counts.
Все миллиарды операций десяти полных walks не исполнялись; их корректность
следует из композиции проверенных primitives и указанных инвариантов.

Следующий точный потребитель — controlled SELECT всех инструкций на
реальных disjoint Choi/CAR copies и source-DAG phases, затем полный
H.1 prepare/select/unprepare и same-execution prefixes/clock. Раздельно
остаётся исходная физическая Cost−Info связь. Никакого дополнительного
Info, подогнанного коэффициента или нового действия здесь не введено.
