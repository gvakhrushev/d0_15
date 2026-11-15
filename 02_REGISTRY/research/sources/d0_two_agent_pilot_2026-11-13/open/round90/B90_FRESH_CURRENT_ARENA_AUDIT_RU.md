# B90: независимая genuine current arena и исходный семивызовный comparator

**Результат: PASS для математически заданной оплаченной конструкции A46 при закреплённых исходных bounds.** Добавлен отдельный current SOURCE/REPORT carrier с 180 f-type Choi и 16 q-type CAR, собственными private/fair/READY/sigma и прежним общим SITE. В отличие от A45 composite reuse его SOURCE физически не адресуется семью исходными REPORT и сохраняется на всём их прямом участке. Независимо воспроизведены все 196 source bindings, новые births, полный profile/compiled census, canonical source и scalar errors, новые Q-source bounds и clock. Идеальный новый logical REPORT точно сокращается относительно исходного SC6/sign; actual native word имеет отдельный оплаченный error budget. Это не автоматическое доказательство полного original H.1/FN admission, всех first-jet marks, Cost−Info или ОТО. `physical_C_closed=false`, `GR_closed=false`.

## 1. Новая арена и старый helper — разные адреса

Старые логические namespace и physical binding A30 сохранены. В частности, старый `aux_arbitrary` logical 2 — это physical 1; старый A29 **compiler helper** — другой провод, logical `10407050784`, physical `10407050781`. Fresh logical interval начинается ПОСЛЕ helper, на `10407050785`, а его первый physical wire — прежнее число births `10407050782`. Отображение q↦q−3 для fresh q инъективно и не меняет ни один старый адрес. Для старого префикса длины m обе привязки сдвигаются на m; старое неизвестное состояние не рождается заново и не сбрасывается.

Fresh REPORT-private virtual interval имеет 1 486 716 786 wires; после него идут 180×24 Choi-private и 16×3 CAR-private, всего ещё 4368. Итого новых RAW births 1 486 721 154, всего n=`11893771936`. Из 196 disjoint fresh source copies получаются 3960 Choi DATA и 304 CAR DATA+RIGHT, вместе 4264; они входят в fresh report interval и не пересекаются ни с source-private, ни с семью старыми аренами. JSON фиксирует physical DATA/RIGHT/private starts всех 196 copies. Новые source preparations используют исходные f-Choi и q-CAR providers; неизвестные состояния не копируются.

Проверены соответствие каждого `(kind,walk,copy)` actual A46 namespace и independently reconstructed binding, полный fresh interval, общий SITE, oldRIGHT и точный A29 helper. Предъявлен новый полный RAW resource frame на `29848+4264=34112` DATA/RIGHT wires. Это реальные операции; новые RAW births и обратные frame слова включены в стоимость.

## 2. Сохранение полной подготовленной карты через старые REPORT

В ideal A27 source target условно на SAM label b новый bank содержит полный current `(u_b,U_b,ψ_b)` и свой retained source-private; старые семь банков и общий SITE остаются в некотором полном `R_b`. Для произвольного coherent SAM/old/reference input до REPORT:

    V|b,old> = |b>⊗|current_b>⊗|R_b>⊗|old>.

Старые семь REPORT адресуют свои прежние интервалы, SITE и прежние общие port/aux/helper, но не один fresh SOURCE DATA, RIGHT или source-private wire. Поэтому **полный** оператор их прямого участка имеет форму I_fresh⊗O на соответствующих проводах и

    (I_fresh⊗O)V|b,old>
       = |b>⊗|current_b>⊗O(|R_b>⊗|old>).

Это верно для всего R_b, включая любую запутанность SITE/старых записей/внешней reference; частичный trace, замена R_b постоянным state и отбрасывание failure не используются. Общий SITE может участвовать в O и остаётся внутри сохранённого остатка. Идеальный target factorization потребляет A27 canonical-source contract; для actual prefix в операторной норме прибавляется вся его настоящая ошибка. Последующий **новый** REPORT может менять current DATA и выдаёт требуемые D_ν maps на собственных физических фронтирах; его literal inverse оплаченно возвращает историю обратно. Нельзя называть state «неизменным» во время выполняемого на нём D_ν.

Порядок A46: старый SITE; восемь SIGMA/SOURCE групп; общий RAW frame и его фактический inverse; семь старых REPORT; fresh current REPORT; прежние PORT_ZERO, SC6, central Z; затем literal profile inverse **всей** последовательности. До восьмого REPORT банк действительно отдельный и сохранён через старые семь. Совпадение этого paid graph со всеми конкретными обязательными original marks и разрешением его births — отдельный admission test.

## 3. Почему прежний comparator не получает восьмой коэффициент

SC6 mapping A46 побайтно сохраняет исходные 23 logical addresses: пять selectors, 14 READY/REPORT outputs ровно семи старых вызовов, port, два символических Spin и oldRIGHT witness. Ни fresh READY/REPORT, ни SITE, ни fresh source, ни compiler helper в этот список не добавлены. Поэтому восьмой current REPORT не становится слагаемым/predicate исходного SC6.

Пусть `D_cur` — **идеальный logical target того же полного конечного retained A17 processor**, со всеми его fresh READY/failure и SITE. На полном carrier он действует только на SITE и fresh arena и тождествен на old SC6 inputs и port. Пусть `H=P† SC6† Z SC6 P` с исходным PORT_ZERO P. Из непересечения поддержек следует точно на всех колонках

    [D_cur,H]=0,       D_cur† H D_cur=H.

Это остаётся верным при произвольной entanglement данных факторов: доказательство операторное, не через scalar expectations. Checker строит полную точную матричную модель и отрицательный контроль, где добавление fresh input в comparator разрушает коммутацию. Таким образом логический target для прежних семи source/report остаётся прежним; новый REPORT не подмешивается в SC6.

Actual A17 native processor внутри отдельных macro может использовать shared port, aux и compiler helper. Точную native коммутацию по одному названию D утверждать нельзя. Если `D_raw` отличается от указанного `D_cur` на all-column domain не более чем на `ε_A17`, а два отдельно compiled прохода отклоняются от `D_raw,D_raw†` на `ε_f,ε_b`, то для унитарного actual H гибридная оценка

    ||D̂_b H D̂_f − H|| ≤ ε_b + 2ε_A17 + ε_f

учитывает обе стороны. Аналогично новый f-Choi/q-CAR preparer сравнивается со своей canonical source isometry с удержанием всех остальных факторов. Не требуется и не доказана полная dirty-WORK коммутация его исходного native word с port. Новый actual W сам по себе не объявляется старым W или точным отражателем; ему заново вычисляют scalar target, errors и цену.

## 4. Независимый full census и source bounds

Подсчёт сделан не вызовом A46 inventory: к frozen A30 old-profile W добавлены 180×(f-Choi forward+literal inverse), 16×(q-CAR forward+inverse), свежие sigma и REPORT с их literal inverses и четыре дополнительных RAW-frame occurrences на 4264 wires. При прежнем certified A29 compiler:

    число полных CZ = 16·75196 = 1 203 136,
    bit_length(rotation error units)=4188,
    e_W <2^-3244,   bit_length(G+CX)=11647.

Точные вычисленные G/CX, old-profile и checkpoint counts записаны hex в `B90_FRESH_ARENA_INDEPENDENT_CHECK.json` и совпадают с A46 по каждому числу. На canonical source input независимо проверено

    η_prefix,new <2^-3232,
    e_B,new <2^-3231.

Для второй границы независимая оценка даже включает полный семивызовный A17 known-macro budget сверх старого вместо одного дополнительного REPORT; A46 использует его с точным делением на 7. Оба способа дают тот же заявленный upper bound. Эти оценки потребляют проверенные source/processor targets A17/A22/A24/A27/A30/B58, не являются произвольным all-dirty-column source-preparer доказательством.

Точный production-sized W не развёрнут. Проверены actual A46 source templates Choi и CAR через старый compiler и physical mapping; giant finite specification, адресная инъекция и structural induction B58 остаются частью обоснования.

## 5. Новые Q-prefix bounds и оплаченная семья

Изменение endpoint scalar target не разрешает автоматически перенести старый вставленный Q kernel: fresh SOURCE зависит от SAM, поэтому Q может смешивать labels между его подготовкой и inverse. Exact небольшой controlled-source fixture проверяет, что равенство полного endpoint само по себе не даёт равенства вставок. A46 правильно пересчитывает source distance с 540 coframe Choi copies, 360 link Choi и 32 CAR:

    Λ_coframe <(35/16)s+2·2^-3232 <(9/4)s,
    Λ_link <17s,  Λ_matter <s,
    sup_(b,c)||u_b−u_c|| <1540s.

Прежние coframe/j2 source bounds тем самым сохраняются. Для всех real SAM skew dimension-free A44 expression с δ=`1540s` даёт `<2^-31`; старую численную `<2^-32` после добавления bank автоматически не сохраняем. По исходным B65 gradient/Hessian, e_B и gain для j=2 воспроизводится фактический lower budget A46 `FD_Qb/Γ_new>2^-45`; Q_f даёт противоположный знак в данной общей paid family. Это утверждения условного finite operator-price эксперимента на его заявленных направлениях, не автоматический physical selection.

A46 математически заново задаёт A41 fixed outgoing target из **нового actual M**, а не отождествляет его с прежним `Uhat`. Входные и output/Q сравнения используют один этот target, новый n и новый общий clock:

    Nbase.bit_length=25457, K=137444,
    D=2^n(Lbase−2+3·2^K)−1, n=11893771936.

Actual Γ содержит новый central corner. Target-independent A41 length/accuracy budgets применимы при доказанных прежних type/positivity условиях; сам production post/provider и полный word не материализованы.

## 6. Оставшиеся условия

Физически disjoint fresh source до собственного D устраняет конкретное затруднение A45: теперь genuine bank и старые семь source arenas одновременно существуют и fresh DATA/private не адресуются семью старыми REPORT. Но называть это полным выполнением сильного §7ej/FN до сопоставления **всех фактических** `D_ν`, их адресов и full-vector first jets нельзя. В частности, отдельные marks внутри незавершённого SourceI/CZ не переносятся автоматическим переименованием, а observer/record не объявляется бесплатно исполненным. Открыты фактический old physical cut и разрешение births, same-task four-slot domain, полный независимый Cost−Info source и refinement. `GR_closed=false`.

`check_fresh_arena_independent.py` закрепляет SHA и независимо воспроизводит layout, весь большой счёт через upstream inventory formulas, exact logical commutator и отрицательные controls, retained-source support, глобальную source-оценку и actual A46 namespace/stage/count/bound receipt. Матричные fixtures проверяют операторные формулы, но не являются запуском production history.
