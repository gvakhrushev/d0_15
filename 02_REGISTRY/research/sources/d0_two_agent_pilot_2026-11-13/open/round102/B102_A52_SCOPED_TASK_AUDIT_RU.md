# B102. Независимая проверка конечной задачи A52

**Результат: PASS для объявленного конечного fixed-centre packet.** Проверены 26881 обычная метка и их знаки, фиксированный post, порядок слотов и оплаченные заполнения, 8 адресов REPORT/READY и полная математическая positive-response карта. A52 правильно не называет этот packet свободной `Y`-семьёй, зарегистрированным физическим fine instrument или полной Cost−Info. Производственный гигантский word не исполнялся. [Код независимой проверки](audit_scoped_comparison.py) и [receipt с SHA](B102_A52_INDEPENDENT_CHECK.json). `physical_C_closed=false`, `GR_closed=false`.

## 1. Catalogue, независимые slots и точные префиксы

Исчерпаны все 26881 ordinary labels и независимо от их генератора построено ожидаемое множество: один centre, 5376 matched и 21504 конечных сравнений четырёх независимых legs. Каждый packet имеет единственное canonical encode/decode, а лишнее поле `Y`, неподходящие axis/sign/plane, Boolean вместо integer и неканоническое или дублированное поле отвергаются. Для post-probe проверены границы и точная формула числа endpoints `2^5376(2^5376−1)`; такой каталог намеренно не перечислялся.

Для каждого ordinary label независимо сверена настоящая `slot_signs` A49:

| Arm | Знаки фактических `Pf,Qf,Qb,Pb` при `sign=s` |
| --- | --- |
| matched | `(s,−s,s,−s)` |
| Pf | `(s,0,0,0)` |
| Qf | `(0,−s,0,0)` |
| Qb | `(0,0,s,0)` |
| Pb | `(0,0,0,−s)` |
| centre / post-probe | `(0,0,0,0)` |

В post-probe сама проба исполняется после post и является отдельным направлением, не Pb. A52 `word_blocks` делегирует одному `A49.production_blocks`; `actual_post_blocks` и cached `actual_core_target` используют один actual centre core, без пересчёта post на sign/axis/arm. Зависимость этой конструкции от центра остаётся; при будущей передаче Y её source не исчезает автоматически.

Повторены **299** замороженных A52 literal fixture сравнений. Дополнительно построена другая независимая малая grammar с 33 labels, тремя axes, 13 настоящими positions и другими длинами padding: все **429** prefixes буквально совпали с началом `A49.family_blocks`. Для семи форм representative labels дополнительно сверены первые 56 production DAG trees с отдельно собранными actual Pf+SOURCE providers. Это конкретные выборки production, а не развёртывание миллиардов блоков. Для полного структурного переноса используются общие providers и подтверждённое B58/A51 закрытие transducer на границах. Проверена настоящая хронология: pad каждого control оплачен до соответствующего cut; core pad добавляется после всего core, а не перед поздними marks. Отложенные Qb/Pb/post/probe/retention остаются в исходном clock.

A51 `<2^-43` относится только к matched jet на двенадцати **после-Qf** frontiers, не к четырём произвольным independent arms и не к SOURCE_before_Qf. Их A52 предоставляет как корректные отдельные maps, без присвоения им этой оценки.

## 2. Полные outcomes, reference и отсутствие бесплатного измерения

Все 8 физических пар пересчитаны из actual A48 namespace и полей каждого `report`, независимо от A52 `report_labels()`: адреса различны, входят в early births, не являются CODE. Первая пара `(REPORT,READY)=(21216958,21216959)`; полный список в receipt.

Для сохранённой изометрии F на объявленном DATA/SITE input fibre с canonical source-private/factory и для всех четырёх стандартных label projectors

    K_(r,k)=Π_(r,k)F,      E_(r,k)=K_(r,k)†K_(r,k),
    Σ_(r,k) E_(r,k)=F†F=I.

Это CP instrument с **полным** выходом: `k=0` failure не отброшен, прочие квантовые провода и external reference сохраняются в post-state. Проверка выполнена также с комплексными операторами и запутанным Bell input/reference; total trace равен 1. Это рассуждение об универсальном допустимом input fibre, а actual Book price A49 остаётся на своём rank-one `H₀=C` и canonical Born input. Из этого не получается формула цены для произвольного old carrier или грязных private.

Вычисленное `Σ KρK†` вообще не равно исходному `FρF†`: фактическая невыборочная запись этих labels привела бы к dephasing. Exact hostile test сохраняет вероятность suffix test 1 без вставки и даёт 1/2 после вставленного считывания. Поэтому A52 корректно рассматривает `(K,E)` как математически доступный test на конкретном frontier и **не** добавляет туда measurement или free readback. K9 всё ещё требует привязать действительно исходный fine instrument, его зарегистрированные labels, failure и реальный suffix; две label variables сами по себе не доказывают, что задан весь original fine record.

## 3. Точный scope цены и faithful-fibre

A52 фиксирует один реально заданный `H+J` Book03 clock с одним birth tree, stage count, rank-one proper cut, обеими Hodge степенями и fixed reference price/gain. При полном same-layout operation tuple и одинаковых обязательных marks owner FN/RAW даёт clock conjugacy и ту же цену на faithful replacements **данного logical label**. Это conditional transport по соответствующей fibre, а не вычисление всей физической Cost−Info, выбор единственной программы или доказательство, что разные labels имеют одинаковые source. Заявленный finite `T` допускается как task datum, но сам по себе не устанавливает physical admission, общий field graph, projection/refinement или все свободные source rows.

В current A52 `round48/two_bit_source_targets.py` и сохранённые angle libraries определяют один центр; `Label` осознанно отвергает свободное Y. Ошибочно было бы записать `E_ref(c,Y)` на открытом chart как уже исполненный constructor только из 26881 меток. Для продолжения требуется один явный эффективный `Y→` SOURCE/marked family, его admissible chart, norm и действительные ценовые/fine-response witnesses; привязка исходного readout может разрабатываться параллельно.

## 4. Проверка возможного следующего post-envelope шага

Идея полного устранения **только post-feedback** уже принадлежит A37 §2–3 и B73. При фиксированном normalized `χ`, действительном `m(Y)=M(Y)χ`, `r=||m||>0`, `ξ=m/r` и `χᵀξ>−1` можно взять одну гладкую локальную формулу

    K=χξᵀ−ξχᵀ,    U*(Y)=I+K+K²/(1+χᵀξ),
    U*(Y)ξ=χ,
    J_red(Y)=−log(d₀+η r(Y)²),   d₀=1−z, η=z p^K.

На отдельном post skew `X`, `d[χᵀ exp(tX)U*m]/dt|₀=r χᵀXχ=0`. Поэтому по любому smooth field path вклад `D_Y U*` в **идеальную J-строку** равен нулю, а исходный член `D_Y m` остаётся. Независимый exact SymPy fixture проверил обе производные на нетривиальном `m(Y)`; A37 уже явно говорит, что при изменении M остаётся `2 Re⟨Mχ,(dM)χ⟩`. Это не требует численной оценки `||D_Y U*||` для самой точной envelope identity. Текущий A52 не реализует такую переменную по Y семью.

Для конечных значений полезна отдельная условная оценка. Если реальный native post `Û(Y)` унитарен и `||Û−U*||≤ε` на обоих endpoint, то при том же m

    0 ≤ J(Û,Y)−J(U*,Y) ≤ η r² ε²/d₀.

Здесь `r²−|χ†Ûm|²≤r²ε²`, а `log(1+x)≤x`. После двух endpoint требуется истинный `2tΓ` нормализатор; если `r≤1`, соответствующий error bound не больше `η ε²/(d₀ |t| Γ)`. Это частичное **conditional** finite-value сравнение: нужна действительная равномерная ε, общий оплаченный layout и реальная положительная Gamma. Если при разных Y пересобираются или дополнительно исполняются post gates, их фактические lengths, clocks и всё изменение H считаются отдельно. Independent пост-направления, physical Cost−Info и source chain полного H+J не исчезают из одной feedback-оптимальности. A37/B73 не устанавливают общий native Y compiler либо полную H+J стационарность.
