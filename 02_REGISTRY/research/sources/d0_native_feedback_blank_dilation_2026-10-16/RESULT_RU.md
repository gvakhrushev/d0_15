# D0 → ОТО: `logdet` как операторная запись полного no-leak event и граница физического допуска

**Дата:** 2026-10-16. **Репозиторий:** `gvakhrushev/d0_15`. **Потребитель:** действующее исследовательское исполнение [Draft #334](https://github.com/gvakhrushev/d0_15/pull/334), `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, узел `MORPH_NATIVE_RETAINED_HISTORY_TO_V8_ACTION`. **Статус:** `RESEARCH / EXACT CONDITIONAL CONSTRUCTION + SCOPED NO-GO`. **Не CORE, не физическая селекция v8, не вывод ОТО.**

Это продолжение [предыдущей проверки селекции](../d0_native_action_selection_2026-10-16/RESULT_RU.md), где установлено событийное тождество цены, но оставлены открытыми физические `P_blank`, коэффициенты повторённых циклов и множитель `M`. Теперь эти *три алгебраических части* сводятся к **одному условному фермионному no-leak readout**. На том же шаге получено точное препятствие: ненулевой рациональный `z=2^-20` нельзя изготовить как конечное *безусловное* событие одного фиксированного золотого reference-инструмента. Утверждения имеют явно ограниченные носители; конечная матричная реализация не выдаётся за native физический прибор.

## 0. Принятые входы, которые не меняются

- BOOK 00 §§00.1/00.8: M1, проверяемость и правила применения reductio. M1 сам по себе не выбирает цену.
- BOOK 03 §§03.3.0/03.3.0a/03.25/03.26: `Cost−Info`, золотой `p+p²=1`, полный finite bootstrap.
- `A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md` §0.1/§0.2: **тот же** selfadjoint Dirac `D`, `Δ=D²`, `B=I−αΔ`, и four-copy coherent completion с signed `S=√α D √(2I−αΔ)`, `B²+S²=I`.
- `A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md` §1: при `L=8`, `N=dim H=16 L⁴=65536`, `n=8192`, `m=2n=16384`, `α=p²/8192`, `z=2^-20`, `M=128`, `K=B^m`, `A=(1−z)I+zK`, `J=−M Tr_H log A`. Retained reference dimension `M`, all16 exterior grades and all4096 momenta остаются.
- `A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md` §3: exact full first source, including matter and moving calibration.
- `A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md`: pathwise `Cost−Info` при **условной** идентификации measured outcomes с history weights.
- `A4D_NATIVE_DYNAMICAL_OWNERSHIP.md`: primitive action fiber. Физического `LAW_SELECT_V8_PROGRAM_AND_PRICE` по этим результатам нет.

`H+J+R` и ни одно из `m,β,z,C,M` не изменяются. Не создаётся новый coupling, `T²`-действие, источник материи либо спектральный cutoff. Ниже строится только условная реализация имеющейся цены через историю реально заданного `B/S`-комплемента.

## 1. Конечный по времени инструмент без eigenbasis oracle

Пусть `H` — конечное Hilbert-пространство размерности `N`, `B=B*`, `S=S*`, `BS=SB`, `B²+S²=I`, `0≤B≤I`. В v8 задано `B=I−αD²`, `S=√α D√(2I−αD²)`; это ровно существующие операторные данные four-copy completion, не новая функция от спектра. Пусть `m=2n` и `0<z<1` — **существующая фиксированная калибровка**, не её новое физическое обоснование.

Выполним следующий условный эксперимент **с полной записью всех исходов**:

1. Контрольная ветвь `0` с амплитудой `√(1−z)` не запускает survival; она фиксируется отдельным label.
2. Контрольная ветвь `1` с амплитудой `√z` запускает ровно `n` проверок signed-complement `B/S`. Её успех после `n` проверок имеет амплитуду `B^n`.
3. Каждый первый провал на попытке `j+1` получает отдельный label `fail_j`, `j=0,...,n−1`, с амплитудой `S B^j`. Ни один провал не нормируется прочь. Полную фиксированную tape можно дополнять явно записанными idle-стадиями, но это не доказывает физического выбора такого stopping protocol.

Набор Kraus-операторов:

\[
L_0=\sqrt{1-z}\,I,\qquad L_1=\sqrt z\,B^n,\qquad
L_{j+2}=\sqrt z\,S B^j\quad(0\le j<n).
\tag{1}
\]

Полнота **на всём H** следует без диагонализации:

\[
\begin{aligned}
\sum_{j=0}^{n+1}L_j^*L_j
&=(1-z)I+zB^{2n}+z\sum_{j=0}^{n-1}B^{2j}S^2\\
&=(1-z)I+zB^{2n}+z(I-B^{2n})=I.
\end{aligned}
\tag{2}
\]

Условие `no-click` означает **обе** помеченные ветви `0` и `1`, а не стирание различия этих ветвей. Его one-particle effect:

\[
E_\varnothing=L_0^*L_0+L_1^*L_1=(1-z)I+z B^{2n}
=A=I-zF,\qquad F=I-K.
\tag{3}
\]

Тем самым реализован **ровно тот же оператор A**, который участвует в исходном `J` (здесь на уровне условного finite instrument). Математически это эффективная композиция уже принадлежащих candidate программных `B,S`, а не физическое доказательство, что D0 действительно подаёт в них coin вероятности `z` и запускает эту control branch.

## 2. Фермионное полное занятие и происхождение одновременно `det`, `M` и `1/j`

Для `N` ортонормальных одночастичных входов `e_1,...,e_N` пусть `V:H→H⊗C^{n+2}` — изометрия, компоненты которой суть Kraus (1); `P_acc` проектирует на две no-click labels `0` и `1`. Тогда `V*P_acc V=A`.

Рассмотрим **математическую** полностью занятую Slater-подготовку

\[
\Omega_{\rm full}=e_1\wedge\dots\wedge e_N\in\wedge^N H.
\]

При внешней степени `∧^N V` вероятность того, что **все N частицы** остаются в подпространстве no-click, равна по тождеству Грама/Cauchy–Binet

\[
\boxed{P^{(N)}_\varnothing=\det(V^*P_{acc}V)=\det A.}
\tag{4}
\]

В доказательстве не выбирается собственный базис `D`, `K`, `F` или `A`: это координатно-инвариантная формула для всех входных базисов.

Теперь используем *уже имеющееся* reference-пространство `H_ref`, `dim H_ref=M=128`, в роли **алгебраического одночастичного spectator**. Если один и тот же оператор действует на `H⊗H_ref` как `A⊗I_M`, то заполненный Slater-сектор на этом расширенном пространстве имеет

\[
\boxed{P^{(NM)}_\varnothing=\det(A\otimes I_M)=(\det A)^M},
\]
\[
\boxed{-\log P^{(NM)}_\varnothing=-M\operatorname{Tr}_H\log A=J_{v8}.}
\tag{5}
\]

Здесь **не** объявляются 128 независимых физически приготовленных вселенных; `M` следует из кратности одного *уже заданного* spectator carrier и тождества тензорного детерминанта. Следует ровно algebraic reader: одна full-occupation quasi-free hypothesis замыкает форму обратной цены и её множитель `M`. Но физический `Λ^{NM}(H⊗H_ref)` **НЕ** есть прежний `H=ℓ²(site)⊗ΛC⁴`, и никакая M1/BOOK теорема пока не устанавливает его внутренний допуск, prepared filled vacuum, выходные labels или полную стоимость ресурса. Запись (5) — typed **candidate extension**, не native owner.

Именно в этой условной модели коэффициент обратимых/повторных циклов **не требует отдельного выбора**:

\[
\frac{d}{dz}[-\log\det(I-zF)]
=\operatorname{Tr}[F(I-zF)^{-1}].
\]

При `||zF||<1`, `J(0)=0` и аналитичности, единственное решение этого дифференциального тождества:

\[
\boxed{J_{v8}=M\sum_{j\ge1}\frac{z^j}{j}\operatorname{Tr}F^j.}
\tag{6}
\]

Итак, **при физическом допуске конкретного fermionic blank readout** и определении действия как отрицательного логарифма этой вероятности `1/j` уже является неизбежным следствием determinant identity, а не дополнительной «скидкой за забытое начало петли». Однако вывод самого физического отрицательного логарифма из `Cost−Info` всё ещё обязателен.

### Полный первый source (включая движущееся z)

Пусть `B(t),z(t)` — допустимые гладкие данные, `n,M` фиксированы. Для произвольного, в частности некоммутирующего `\dot B`,

\[
\dot K=\sum_{a=0}^{2n-1}B^a\dot B B^{2n-1-a},\qquad
\dot A=z\dot K-(I-K)\dot z,
\]
\[
\boxed{\dot J=-M\operatorname{Tr}\left(A^{-1}[z\dot K-(I-K)\dot z]\right).}
\tag{7}
\]

На том же **reference-extended** carrier это тождественно `−Tr_(H⊗ref)[(A^-1⊗I_M)(\dot A⊗I_M)]`. Условия на самосопряжённость и `A>0` заявлены; некоммутативная производная степени и normalizer сохранены. Дополнительные actual calibration derivatives `m,β,C` и moving field-preparation отдельно принадлежат владельцу unfolding; запись (7) их не скрывает.

## 3. Exact obstruction: `z=2^-20` не есть finite unconditioned golden-cylinder event

Золотой reference-код имеет две условно независимые ветви с вероятностями

\[
p=\varphi^{-1}=\frac{\sqrt5-1}{2},\qquad p^2=1-p.
\]

Каждая **конечная безусловная** ветвь с кодовыми словами `0/10` имеет вероятность `p^a(p²)^b=p^{a+2b}`. Любое событие, задаваемое конечным набором непересекающихся остановочных слов, имеет вероятность в кольце `Z[p]`, так как `p` — алгебраическое целое (`p²+p−1=0`). Поскольку `1,p` — рационально линейно независимы,

\[
\boxed{\mathbb Z[p]\cap\mathbb Q=\mathbb Z.}
\tag{8}
\]

Событие имеет вероятность в `[0,1]`. Поэтому **любая рациональная** вероятность такого конечного безусловного события равна `0` или `1`. В частности

\[
\boxed{0<z=2^{-20}<1\quad\Longrightarrow\quad
z\text{ не есть такое golden-event probability}.}
\tag{9}
\]

Это универсальный algebraic-integer аргумент, **не** перебор конечных кодов и **не** запрет всех способов получить `z` из D0. Область узкая и важная: только фиксированная golden reference-мера, конечный deterministic event (union of cylinders) и отсутствие дополнительной conditioning/quantum interference/движущегося preparation law. Предварительно известно, что реальная `q_ρ(ω)` может отличаться от `μ(ω)`; (9) не переносится на произвольное `q_ρ`.

**Прямой условный обход без новой числовой константы.** Два независимых золотых outcomes `01` и `10` имеют **равные** reference-вероятности `p³`. При условии, что получен один из них, получаем честный бит с `P(01 | 01 или 10)=1/2`. Двадцать таких принятых пар дают для 20 конкретных равных битов

\[
\boxed{P(20\text{ нулей}\mid\text{все пары различались})=2^{-20}},
\]

но безусловная вероятность всего принятого слова равна `p^{60}`, а вероятность условий — `(2p³)^{20}`. Значит нужен **явный postselection/условный readout** на 40 золотых outcomes, с удержанными rejected labels и нормировкой. Его стоимость, физическое допущение подготовки и вопрос «почему ровно 20 пар?» ещё не выведены. Если записать z как вероятность без этого условия, меняется истинный source. Для бесконечного повторения до успеха требовался бы дополнительный infinite-stopping/finiteness audit.

## 4. Capacity theorem для архитектуры из конечного числа serial z-coins

Пусть **заявленное дополнительное** ограничение таково: весь `z`-dependence программы проходит через `t` последовательно (или отдельно) вызываемых классических Bernoulli coins, каждый элементарный условный outcome линейно зависит от `z`, все остальные gates/preparations от `z` независимы, нет eigenvalue/determinant oracle и скрытой `z`-прошитой подготовки. Любая вероятность конечного дерева такой программы есть polynomial in z степени не более `t` — по индукции по дереву, даже при адаптивном выборе следующего испытания. Поэтому для **тождественного равенства на открытом интервале z** с (5) необходимо

\[
\boxed{t\ge M\operatorname{rank}F.}\tag{10}
\]

Действительно `det(I−zF)^M` имеет степень `M rank F` и ненулевой старший коэффициент, поскольку ненулевые eigenvalues `F=I−K` положительны. Условие (10) **не** относится к одному фиксированному `z=2^-20`, к gate с глобальным operator-valued z control, к явно построенному расширенному многочастичному Fock-действию или к скрытому/движущемуся generator law.

На homogeneous positive Gram v8 полного `H=ℓ²((Z/L)^4)⊗ΛC⁴` каждый momentum имеет16 exterior states. При `0<B_k<1` на всех `k≠0` и `B_0=1`:

\[
\operatorname{rank}(I-B^{2n})=16(L^4-1).
\]

При унаследованном `M=128` и `n_L=128L²` получаем:

\[
 t\ge128\cdot16(L^4-1),\qquad
 \frac t{n_L}\ge16\Big(L^2-\frac1{L^2}\Big).
\tag{11}
\]

| L | Full one-particle modes | Rank F | Minimal coins for `det(A)^128` (uniform in z) | `n_L` | Minimal average coins per round |
|---:|---:|---:|---:|---:|---:|
| 4 | 4 096 | 4 080 | 522 240 | 2 048 | 255 |
| 8 | 65 536 | 65 520 | 8 386 560 | 8 192 | 1 024 |
| 16 | 1 048 576 | 1 048 560 | 134 215 680 | 32 768 | 4 096 |
| 32 | 16 777 216 | 16 777 200 | 2 147 481 600 | 131 072 | 16 384 |

Следовательно простой **serial single-z-coin-per-record-round** не реализует `J` uniformly in z. Даже bounded-fixed-many z-coins per round рано или поздно не проходит refinement. Но 128 labels и 128 reference dimensions **не** являются по определению 128 coins; из этой таблицы нельзя заключить об impossibility полной D0-программы. Full operator collective gate, многотельный Fock spectator или реально порождённый другой `z`-law лежат за пределами предпосылок (10).

### Размерностная граница именно этого CAR-расширения

Реализация (5) предполагает **внешний CAR на `r=N*M` комплексных one-particle modes**, а не обычный исходный single-site CAR на четырёх ролях. Полная CAR-алгебра `r` мод изоморфна `M_(2^r)(C)`, поэтому её ненулевая/faithful *-репрезентация требует комплексное Hilbert-пространство размерности не меньше `2^r` (не считая вспомогательных outcome labels).

На прежнем `L=8`: `N=65536`, `M=128`, значит `r=8 388 608` и требуемый `log₂ dim ≥ 8 388 608`. Между тем даже **заведомо щедрое** произведение всех явно указанных ресурсов v8 — base `N=2^16`, reference `128=2^7`, workspace `128^8192=2^57344`, плюс отдельно `32` labels, `2` coefficient, `2` golden-port и ещё раз `128` outcomes (последнее, возможно, уже включено в workspace) — имеет

\[
\log_2 \dim H_{\mathrm{listed}}\le16+7+57344+5+1+1+7=\boxed{57381}
\quad\ll\quad\boxed{8\,388\,608}.
\tag{12}
\]

**Следствие:** faithful *полная внешняя CAR-реализация* (5) не помещается в перечисленный существующий v8 tensor budget. Для её физического допуска нужно вывести **новый** источник многомодовой CAR или другой, существенно более сжатый native determinant compiler, не предполагающий весь внешний Fock. Это точное препятствие конкретной предложенной реализации, **не** запрет вычислить determinant меньшей схемой и **не** полная классификация всех ресурсов D0.

## 5. Что изменилось в программе и какой именно следующий потребитель

**Закрыто без физических заявок:** (1)–(3) дают полный finite no-click Kraus instrument *только из supplied B,S,z*, все failures и две accepted labels retained; (4)–(7) дают неиспользующее eigenbasis доказательство `det`, правильных `1/j`, `M=128` как spectator multiplicity и всех заявленных первых jets; (8)–(9) запрещают считать native `z` произвольным конечным безусловным событием золотого **reference**-кода; (10)–(11) дают реальный resource lower bound для **определённого** serial-coin интерфейса.

**Физический выбор всё ещё открыт:** кто из исходных native readout/return primitives порождает `full-occupation wedge` над `H⊗H_ref`, *именно* оба no-click labels, coin z, 20 conditional equal bits (если используется этот маршрут), условную/полную source-normalization, `β`, `C`, `Cost−Info` и сопряжённую настоящую matter/observer/preparation динамику. В частности `reference128` даёт тензорную кратность в кандидатном чтении, но исходная D0-модель не обязана физически заполнять все `NM` single-particle slots.

Минимальное следующее доказательство — **не выбирать коэффициенты циклов заново**. Требуется на existing `LAW_SELECT_V8_PROGRAM_AND_PRICE` предъявить native morphism

```text
  retained golden/record histories + clock + true feedback + reference128
    -> (complete conditional labels, admitted many-body no-click state,
        actual survival readout, full Cost−Info scalar)
    -> same H+J+R with all source jets and finite/refinement budgets.
```

Если такого канонического admitted многочастичного readout нет, нужно исследовать другой owned source реализации `J`, а не считать algebraic probability физической. Доказательство M1 uniqueness приходит только **после** проверки всех primitive/readout diagrams, а не из названия `fermionic`.

## 6. Проверка

Изолированный файл `check_feedback_dilation.py` на точном rational positive **недиагональном** `2×2` B/S исполняет:

- actual `B²+S²=I`, `[B,S]=0`, полный `(n+2)`-outcome instrument, telescoping всех первых failures;
- `Σ(minor of accepted V)^2=det A` в полном occupied-двухфермионном секторе, без eigenbasis;
- `det(A⊗I_M)=det(A)^M` и тот же source после tensor extension;
- действительно некоммутирующий `dB`, moving `dz` и полный first-source с матричной производной `B^{2n}`;
- series `1/j` и Jacobi identity, independent trace-vs-det hostile probe;
- algebraic-integer golden argument с positive 20-pair conditioning countercontrol;
- точный `rank F=16(L⁴−1)`, degree и refinement capacity для однородного carrier v8.

Результат — `RESULT.json`: **39 exact controls**, запуск обычным и `python -O` с побайтно идентичным научным JSON, SHA256, зафиксированный в `RESULT.json` (ordinary/optimized byte-identical). Full Lean, original expensive v8/root, GitHub CI и самостоятельный physical/native admission test **не запускались**. Ни статус задачи, ни claims, ни BOOK не продвигаются.
