# B34. Независимая проверка A16 selected-source consumer

## Результат и точная область

На `source_select.py` SHA-256 `a204f5844abc919a95d1a9103fdf32ba1d415a77f048d1cb676a6cf1f32581f6` независимые проверки логических инструкций, их copy routing, знаковых фаз, очередности walk, структуры native literal inverse, ресурсных counts и ограниченного native binding прошли. Исправленных замечаний к этому коду по проверенной области не осталось. Полный астрономический native walk, его births/marks/clock и общий ten-walk assembler не исполнялись и здесь не сертифицированы.

Таким образом B33 больше не зависит только от абстрактного leaf oracle: при условиях чистого входа, fresh B31 δ, общего SITE и корректной глобальной сборки **идеальный логический consumer текущего A16** исполняет именно потребованный B33 оператор. Это доказательство значения target и конечной грамматики, не утверждение exact компрессии у приближённого native word. В обозначениях A11 `rho_x=256·PF_probability(x)`, а `inverse_PF_once=1/rho_x`; дополнительного множителя 256 вводить не нужно.

## Выбранная физическая копия и фазы

`A16_FULL_DEGREE_CHECK.json` отдельно разворачивает реальные instruction IR обоих корней и исполняет по 128 полных cases. Для `H_f` размер `[82,0]`, 65 479 elementary gates и 82 copy calls; для `H_q` — `[2,2]`, 2 475 gates и 4 copy calls. Проверены выборы начальных, внутренних, последних и несуществующих offsets, фактические A15 адреса, знак и control, непустые посторонние copy banks, `CAR_RIGHT`, отдельные delta и обнуление scratch. `A16_INSTRUCTION_CHECK.json` дополнительно выполняет 800 случаев полного `[2,2]` instruction, включая CAR с ненулевым anchor. Адреса, instruction records, control, delta и `CAR_RIGHT` не являются target ни одного логического gate. Это тесты полных **отдельных инструкций**, не полных walk streams.

Независимое семантическое обоснование: каждый конкретный enable вычисляет `[h=1 ∧ kind=type ∧ offset=i]`; допустимый offset активирует ровно одну copy и её собственный δ. `pair_ir` вычисляет раздельные equality в одно m, очищает их до swap, делает фазу и controlled XOR, затем при неизменном m действительно очищает его. На `x=a,b,complement` получаются точные B27 `V0,V1`; фазу negative constant алгоритм применяет к h отдельно. Недействительный kind или offset не вызывает source копию; `a=b` имеет оговорённое расширение, а для действительных записей A15 `a≠b`. Полное равенство по всем входным колонкам следует из этой семантики и линейности, а не из перебора конечного test sample.

## Истории, порядок и знак

`A16_WALK_WIRING_CHECK.json` проходит actual event grammar целиком. Для f: 455 уникальных 65-bit instruction records и 37 310 copy SELECT; для q: 18 records и 72 copy SELECT. Все controller stages предшествуют `H`, затем идут top identity phase, все fixed instruction phases и выбранные copy SELECT, readout `H` и конвенционный `X`. На восьми выборках крайних slot/copy проверено соединение соответствующих `kind,offset,a,b`, h, δ и нужной copy при неизменных чужих данных, SITE, history и CAR_RIGHT. Отдельно проверены фактические top/constant sign-wire и что `H` затем `X` пишут плюс в bit `1`.

Сохранённые records, all attempts и READY дают предпосылку B33 для суммирования по ортогональным coherent histories. Объединяющая сторона всё ещё должна alias-ить один SITE на все walk и обеспечить отдельные real banks и δ; раздельные функции walk сами не являются доказанной целой глобальной аллокацией. Для одного report условно `Q_pre≈0.740683`, а семь независимых checkpoint дают `Q_pre^7≈0.122300`; это не полная `alpha_h`.

## Native inverse, нулевой контроль и ресурсы

`A16_NATIVE_COUNTS_CHECK.json` независимо сопоставляет 70 716 синтаксических узлов forward/reverse двух actual 12/22-bit native pair DAG. Каждый `G` обращён через оплаченный `Z G Z`, каждый `SourceI` — тремя действительными вызовами, `CX` обращён сам в себя, последовательности идут в обратном порядке; точные forward/reverse inventories совпали. Это сравнение конечной грамматики, не физическое исполнение её огромных повторов.

Условная граница всех известных A13/A15/B31/A16 approximate macros за семь report: `162 611 159 340 · 2^-4096 < 2^-4058`. A16 добавляет 19 067 382 таких macros на один report. Сюда не включены ещё отсутствующие части полной физической схемы и её источника; all-column approximation не устанавливает exact native scalar READY или полную H.1 block structure.

`A16_H0_STRUCTURAL_CHECK.json` покрывает все 86 enable-блоков двух корней и 6 502 gate instances: при чистых SELECT-work и `h=0` каждый enable точно неактивен. Используется установленное A14 exact свойство `CCX_hat` с нулевым **первым** control на произвольных target/aux/port/Spin. Membership может запутывать рабочие провода и aux, но не меняет `h_eff` и phase work; body является exact identity, а фактический literal inverse даёт `M†M=I`. Это относится к SELECT и constant phase, до добавления приближённых H preparation/readout; чистота входных DATA и native aux не предполагается.

`A16_NATIVE_BINDINGS_CHECK.json` сверяет 64 первых блока каждого actual lazy global walk с A15/A14, проверяет шесть конкретных native copy blocks и 174 660 синтаксических native leaves на сохранение instruction/δ и protected oldRIGHT. Остальная полная native последовательность не разворачивалась и не исполнялась.

## Изолированное воспроизведение

`A16_ISOLATED_REPLAY.json`: builder и авторский checker повторены в отдельной временной копии с закреплёнными входами; три output JSON совпали побайтно. Авторский checker сообщает 18 688 малых случаев, 5 136 фактических адресных случаев, 1 600 полных `[2,2]` instructions и 10 проверок Hadamard sign convention. Эти результаты дополняют, но не заменяют вышеперечисленные независимые проверки.

Остаются: действительные рождения и подготовки всех ресурсов, global alias/disjointness, семь source banks, полный physical writer, его marks/clock и полный error budget, H.1 exact block structure и независимое установление физической Cost−Info. `physical_C_closed=false`; `GR_closed=false`.
