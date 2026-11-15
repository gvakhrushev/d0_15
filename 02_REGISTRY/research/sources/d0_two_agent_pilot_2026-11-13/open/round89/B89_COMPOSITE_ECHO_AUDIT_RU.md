# B89: независимая проверка composite processor и новой цены A45

**Результат: PASS для математически заданной paid family при закреплённых исходных bounds.** A45 вставляет исходный ten-sign processor и его старый literal inverse на конкретные f-Choi/q-CAR addresses, компилирует их с новой точностью и сохраняет полный WORK/R/failure. Проверены физические привязки, количество операций и новый clock, а также source-prefix и независимые P_f/P_b/Q_f/Q_b budgets. При проверке обнаружен недостающий множитель при нормировании выходного state; A45 исправлен на `3ε_echo`, и независимый пересчёт подтверждает итоговый исходящий bound `<2^-75`. Production history не исполнялась; отдельный восьмой банк и полный original-task/FN admission не установлены. `physical_C_closed=false`, `GR_closed=false`.

## 1. Реальный composite processor и допустимые точки отметок

A45 использует все 180 f-Choi и 16 q-CAR (DATA12+RIGHT7), выбирая 16 физических q-CAR copies по `(T1,…,T8,copy=0,1)`. Инволютивная address map содержит 304 пары f↔q и совпадает со всеми independently recorded B88 физическими адресами. Общий SITE, f sigma и ещё RAW f-private/fair арена, port/aux/helper и исходные границы источников сохраняются. Карта — параметры реально выпущенных адресованных gates, не отдельный бесплатный physical SWAP и не удаление `R_b`.

На общем SOURCE frontier A30 full canonical-input isometry уже имеет bound; B88 отдельно оплачивает существующий обратный RAW frame. A45 использует тот же exact bound

    η_decode = η_common_new+4·29848·2^-7432 <2^-3232.

Для remapped original report-forward prefix с контролируемым replacement и исходным processor error:

    η_Dν ≤η_decode + ε_forward,ν + ε_A17,ν
         ≤η_decode + ε_forward + ε_A17 <2^-3231,
    ε_A17 ≤162754649904·2^-4096 <2^-4058.

Это полная canonical-input prepared-isometry с coherent SAM, old/reference, SITE, source и остальными retained outputs, не только scalar moment. Допускаются только реально соответствующие исходному `D_ν` адреса и полные closed macros; в незавершённом SourceI pair или внутри заменённого CZ прежнюю карту без отдельного transport утверждать нельзя. `observer_blocks(...,include_macro_marks=True)` требует `pending=0`; независимый checker исполнил реальные первые блоки обоих глубин и отверг барьер внутри незаконченной SourceI-пары. Исходное заданное множество обязательных marks ещё должно быть сопоставлено с этим интерфейсом; выдача произвольного marker не превращает его в оригинальное требование.

## 2. Исходный inverse и реально оплаченный новый clock

Старый native-profile `D;D^literal-inverse` равен I на всём carrier. A29 independently переводит обе части в положительные G/CX: их действительное произведение **приближает** I и не объявляется точным inverse. На A38 precision k точные counts совпадают с B88, включая все `C=150392` CZ, (P\) оставшихся пар SourceI и все actual G/CX. Число error units `16P+32C` имеет 4154 бита:

    ||Ê−I|| ≤ ε_echo=(16P+32C)·2^-20000 <2^-15846.

Переназначение source проводов сохраняет tree целой CZ и не касается helper/port; контроль source-I parity идёт независимо для echo и сохраняет состояние исходного A30 transducer. Проверенные ранее B88 реальные remapped Hq templates и структурное покрытие B58 дополняют малые tests; полный гигантский stream не развёрнут.

После добавления (L_{echo}) paid gates, без новых births, `bit_length(L_echo)=24233`, `bit_length(Nbase_new)=25457`, K=`137444`. Сравнения используют один новый layout, а новый полный clock и gain:

    D_new = 2^n(Lbase_new−2+3·2^K)−1,
    Γ_new = 4 z p^K c_ref gs/(1−z+z p^K c₀,new²).

Они не переименовываются в A43 clock/Γ. Добавленная heat-стоимость учитывается в новом R11 bound; абсолютный heat trace и production post не вычислялись.

## 3. Источники и нормировка

Пусть c₀,c′ — old actual corner и derivative фиксированного logical Y, а c₀,new,c′_new — значения после echo. Все окружающие maps унитарны, `||Y||≤1`, поэтому каждая разность `<ε_echo`. С actual собственной нормой каждой истории

    d(Y)=−c₀ c′/(2c_ref gs),
    |d_new(Y)−d_old(Y)| ≤(3/2) ε_echo/(gs).

Эта формула использует новые и старые реальные знаменатели feedback через соответствующие gains; она не приравнивает численно Γ_new и Γ_old. Независимая рациональная проверка воспроизводит A45 incoming и all-real-skew analytic budgets, finite Q j=2 bound и полный новый heat term:

    |FD_Qb/Γ_new − ½d_Pf,ideal| <2^-75,
    FD_Qb/Γ_new >2^-45,
    FD_Qf/Γ_new =−FD_Qb/Γ_new <−2^-45.

Последнее равенство exact для общего двухслотного paid family: новый echo SAM-disjoint и стоит внутри S, а обе пары сравнивают одинаковые positive native words на разных cuts. Оно не доказывает равенство исходных complete pre-sign maps разных logical p.

Для исходящих plane probes нужна дополнительная осторожность. A42 weighted proof применяет **нормированный** `ξ=Mχ/||Mχ||`. Даже если `||(M_new−M)χ||≤ε_echo`, изменение ξ нельзя в общем ограничить одной ε_echo: пример `Mχ=(3/4,0)`, `M_newχ=(3/4,1/20)` строго нарушает такую оценку. При `r_old=||Mχ||>2/3` и `r_new>0` достаточно

    ||ξ_new−ξ_old|| ≤ 2ε_echo/r_old <3ε_echo.

A45 после этой независимой проверки исправлен и использует

    δ = ε_U + 3ε_echo + μ_probe <2^-14622.

С этим δ полный all-plane finite feedback dual вместе с пересчитанным heat остаётся `<2^-75`. Это результат для указанных математически конечных plane comparisons, а не доказательство, что все они admitted в original descriptor или что построенный production word исполнен. Все source SHA в JSON относятся к уже исправленным A45 py/plan/checker/receipt и финальному отчёту; их содержательная сверка расхождений не выявила.

## 4. Граница reuse и исходного task

`D_ν` исполняется на настоящих source copies и выдаёт полный промежуточный prepared map, но эти же f-Choi/q-CAR остаются source inputs семи последующих REPORT. Поэтому новая история не содержит **одновременно восьмой независимый** genuine bank и не сертифицирует его retention через старые REPORT. Такой результат не следует и из почти identity echo. Возможность отдельного fresh bank или иного физически допустимого encoding остаётся отдельной задачей, со своими births, input maps, marks и новым clock; необходимость именно fresh bank здесь не доказывается.

Не закрыты сопоставление полного оригинального списка marked prefix/processor maps с записанными границами, более сильный same-FN/unsplit descriptor, конкретный old physical input cut, all-plane finite admission, full physical Cost−Info binding и refinement. Соответственно ни finite source A45, ни PASS проверок не являются выводом ОТО.

`check_composite_echo_a45.py` закрепляет SHA исправленного A45 и B88, сравнивает каждую из 16 пар, исходные counts и новый clock, пересчитывает нормировки и bounds, проверяет точный counterexample нормирования, реальные начальные processor templates и отказ незакрытого barrier. Источники B21/B25/B58/B65/A17/A30/A33/A37/A41–A44 потребляются с их заявленной областью; гигантские слова и вся таблица SAM не исполняются.
