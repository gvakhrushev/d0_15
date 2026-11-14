# B38. Независимая проверка A18: материальные CAR-подготовки

## Вывод и область

Проверены исходные target formulas, все SAM/site sectors, 38 конкретных native углов, адресная grammar A18, её literal inverse и композиция семи CAR frames. Для `MATERIAL_PREPARATION_LIBRARY.json` SHA-256 `83592b07988263b453d7ac27fa7f53d7b7d98846a3d8dfd40b3e401fe095e22b` независимая целочисленная оценка даёт наихудшую ошибку одной planar rotation `<2^-4112`, сильнее требуемой `2^-4096`. Повторный запуск владельческого certificate builder не выполнялся.

Отсюда при указанном interface и точных native primitives следует заявленный идеальный all-column target и его условная approximation bound. Vacuum/Fourier prefix, реальная подготовка трёх predicate zeros, physical birth/mark/clock admission, Choi, общий внешний SITE loader и полный H.1 остаются за пределами проверки. `physical_C_closed=false`, `GR_closed=false`.

## 1. B25 binding и вся локальная SAM family

[A18_TARGETS_CHECK.json](A18_TARGETS_CHECK.json) сверяет исходные 2 688 `sam_index`, 256 упорядоченных sites и все control rows с B25:

* `q`: 192 fixed-site rows и `64·4=256` двухбитовых rows, всего 448;
* `y+` и `y−`: по 256 rows; знаки используют исходные паритеты x1 и x0 соответственно;
* 22 half-vector families: четыре fixed q, 16 q с двумя local matter bits и два reference знака.

На каждом свободном site в CAR `psi_0,psi_15` входят только два принадлежащих этому site matter bits. Остальные 2 686 bits не влияют на **этот CAR map**; для Choi и прочих компонентов они могут быть существенны. Это следует из исходной B25 формулы, а не из усреднения по SAM. В восьми дополнительных hostile diagnostic случаях более тысячи остальных bits менялись при фиксированных двух локальных; соответствующие B25 `psi_x` оставались неизменными.

Независимо сверены `p`, `π/(200√2)`, `a_h=(1/8)√(F_h/k0)` и исходные `k0,F_h`. Outward dyadic операции и Machin formula для π проверены как integer bounds; 400-bit mpmath сравнения 22 vectors и 66 rotations — лишь диагностика.

Для каждого нормированного `u_m` исходного CAR half-vector три хронологических planar rotations `(1,14)`, `(1,0)`, `(1,15)` дают `u_m` из grade1. Их знаменатели строго положительны; структурно нулевой sine удаляется только при точном нуле. Общее правило A18 не смешивает внутренний CAR SITE с внешним PF SITE.

## 2. Независимая проверка **всех** сохранённых интервалов

[ALL_MATERIAL_INTERVALS_CHECK.json](ALL_MATERIAL_INTERVALS_CHECK.json) независимо восстанавливает исходные target intervals через dyadic roots и Machin π и считает все 38 actual native powers целочисленным complex-ball методом при 8 448 bits. Все 60 nonzero rotations и шесть exact-zero rotations охвачены; наихудший independently certified L1 error `<2^-4112`. Нет float и нет вызова A18 builder или его `_rotation_intervals`.

Для exact complex powers `|z|=1`: если центры известны с Euclidean radii `r1/S,r2/S`, то после умножения и двух integer roundings новый радиус не превосходит

```
(r1+r2+ceil(r1*r2/S)+2)/S.
```

Это полностью устраняет неконтролируемую зависимость координат при обычном interval squaring. Сумма ошибок cos/sin ограничивает operator norm разности двух planar rotations.

[SAVED_TARGET_INTERVALS_CHECK.json](SAVED_TARGET_INTERVALS_CHECK.json) дополнительно показывает, что **каждый сохранённый** target/half-vector interval содержит независимо рассчитанный более узкий outward interval при 17 408 bits; все 60 integer error numerators пересчитаны. [SAVED_NATIVE_INTERVALS_CHECK.json](SAVED_NATIVE_INTERVALS_CHECK.json) отдельно проверяет, что каждый сохранённый native cos/sin interval содержит независимый 15 744-bit complex ball. Это сильнее простого пересечения интервалов и не повторяет владельческий certificate builder. Шесть структурных нулей проверены отдельно.

## 3. Native namespace, all-column semantics и цена

[A18_NATIVE_STRUCTURE_CHECK.json](A18_NATIVE_STRUCTURE_CHECK.json) независимо сверяет все 2 880 sector/plane bindings, включая 2 112 потенциальных K=11 и 768 K=13; структурные нули затем не испускаются. При `k_K=2^(13−K)k` оба K дают один exact native exponent `8192k theta`. A18 перечисляет controls в другом порядке, чем B37, но независимая проверка показывает одинаковые control→pattern, grade pair, pivot и ориентацию; побайтное совпадение слов не требуется.

Для настоящих representative K=11 all-zero и K=13 nonzero predicates проверен **каждый** из соответственно 2 050 и 8 194 forward blocks и его literal raw inverse, native resource formulas и то, что SAM/site controls и RIGHT/oldRIGHT не становятся targets. Все остальные строки покрываются теми же аналитическими формулами; полные огромные repeats не исполнялись.

[A18_WALSH_EXACT_CHECK.json](A18_WALSH_EXACT_CHECK.json) исполняет actual `pair_blocks` для K=2,3 в точном `Z[a]`, `a⁴+a²−1=0`, с буквальным native `L_i=diag(J,−J)`: 1 152 полных columns и 1 152 forward→literal inverse, включая zero/mixed/all-one predicates. General K следует из принадлежащей owner parity/Walsh identity. Вне выбранного site/SAM sector полный native block действует точно как identity на arbitrary grade/port/Spin. Поэтому при любых, в том числе запутанных, входах

```
||U_m_native−U_m_target|| <= max_(site,SAM) Σ_(≤3 active planes) δ <= 3δ,
δ=2^-4096.
```

Ошибка не суммируется по 448 взаимоисключённым q sectors; физический gate inventory при этом оплачивает все фактически испущенные sectors. [A18_LIBRARY_INVENTORY_CHECK.json](A18_LIBRARY_INVENTORY_CHECK.json) независимо восстанавливает весь catalogue, 22 именованных specs и все forward/literal-inverse resources: q имеет 1 152 nonidentity rotation occurrences, y± по 512. Source hashes и сохранённый inventory совпадают.

## 4. Семь полных CAR frames

[A18_CAR_FRAME_CHECK.json](A18_CAR_FRAME_CHECK.json) проверяет actual U_star и его literal inverse из B37, actual R_grade1 как `F† Z F` из B35, три distinct clean predicate wires и arbitrary native aux. SAM/internal SITE/RIGHT/oldRIGHT не адресуются как targets или отдельные ресурсы. Хронология

```
U_star† ; R ; U_star ; U_m† ; R ; U_m
```

даёт ideal `R_(u_m) R_(u_star)=O_m O_star^T` на полном grade carrier. Для q/y± hybrid bound на clean predicate inputs составляет `2·3δ+2·δ+2·10δ=28δ`; residual рабочей области отражения включён, reset не предполагается. Для `f,0,x+,x−` используется один и тот же фактический U_star по обе стороны: `R=F†ZF` — точная involution на полном пространстве, так что весь endpoint **точно I даже при arbitrary predicate/aux inputs**. Физические paid stages и их возможные marks при этом не удаляются.

Эта identity дополнительно проверена exact native replay для 64 произвольных grade/predicate/port/Spin/aux/oldRIGHT cases с 3 924 paid small-k calls. [A18_CAR_FRAME_INVENTORY_CHECK.json](A18_CAR_FRAME_INVENTORY_CHECK.json) независимо сверяет forward и literal reverse counts всех семи banks и 112-copy total; q representative K11/K13 frame stage maps проверены полностью на уровне неразвёрнутых blocks. Все три predicate zeros остаются внешней обязанностью, как и исходный vacuum/Fourier.

Консервативно `112·28δ<2^-4084`. Если будущая общая композиция использует совместимые inputs и все ранее учтённые A17 parts действительно присутствуют однократно, известный coefficient `162 754 649 904 + 3 136 = 162 754 653 040 <2^38`, то есть соответствующая сумма ошибок `<2^-4058`. Это условное сложение bounds, не доказательство нового глобального layout, полного error budget или полной `alpha_h`.

## 5. Следующая граница

Подготовка q/y CAR half-vectors и точный CAR-frame grammar устраняют конкретный target-операторный parent при объявленных ресурсах. Не доказаны фактическое создание 112 CAR copies, исходный vacuum/Fourier, Choi banks, общий внешний SITE, RAW predicate births и stage/mark/clock ledger. Исходный physical Cost−Info и путь к ОТО остаются открытыми; никакой новый коэффициент или Info не назначался.
