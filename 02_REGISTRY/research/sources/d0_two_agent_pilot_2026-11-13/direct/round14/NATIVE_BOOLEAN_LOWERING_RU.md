# A14. X/H/CCX и все A13 decoders через исходные native операции

Фаза — native realization уже заданного H.1 источника. Потреблены A13 реальные обратимые схемы, B27/A13 routed Z/G-inverse и **owned** Walsh/predicate-phase compiler: `sources/d0_native_readiness_amplification_2026-10-24/PHASE_COMPILER.md`, `native_phase.py`; в основном residual owner это (197). Новая подстановка — три конкретных all-column приближения X,H,CCX и их применение к полным конечным схемам A13. Новый gate, полевая angle oracle, measurement/feedforward или закон Info не вводятся.

Для каждого X/H/CCX получен сертификат operator error **≤2^-4096**. Выданная конечная native грамматика содержит только настоящие `G`, `CX`, `SourceI`; каждая положительная степень имеет конкретный integer repeat count. Большое слово не разворачивалось и не исполнялось целиком. Число k имеет4111 бит: это крайне дорогая математическая конструкция, а не практический запуск такого процессора.

## 1. Что именно заимствуется и переносится

Пусть `G=R(theta)`, `R(beta)=exp(beta J)`, `J=[[0,-1],[1,0]]`, cos(theta)=sqrt(p), sin(theta)=p. Для K разных ordinary controls и заданного pattern v owned identity даёт

```
product_S CX_S G_target^[(-1)^(v·S) k] CX_S
 = R_target(2^K k theta P_v).                       (1)
```

На несовпадающем pattern оператор точно identity, на совпадающем — указанное native вращение. Это all-column равенство, включая неизвестный target и коррелированные port/Spin. Старый `phase_word` API требует declared fresh blank target для своей amplifier application. Здесь не подставляется ложный blank: `native_boolean.selective_rotation` потребляет **само all-column доказательство (1)** и валидирует существующий обычный target без требования о его состоянии. Это перенос уже доказанной алгебры на такой интерфейс, а не утверждение, что старый API уже разрешает произвольную физическую подготовку.

Port отделён от всех controls/targets; оба Spin wires и oldRIGHT никогда не адресуются индивидуально. Controls каждой selective rotation остаются read-only на всех native stages. Негативная степень имеет буквальный новый график

```
G_q^-k = SWAP(q,port); SourceI²; G_port^k; SourceI²; SWAP(q,port),
```

то есть k G +4 SourceI +6 CX. Port/Spin точно восстановлены на границе **всей** степени. Старый letterwise inverse имел11k вызовов; его уже исполненные stages не сокращаются задним числом. Здесь строится другой полный forward word, и его марки/цена должны учитывать именно новый график.

## 2. Один общий native power и точные целевые операторы

Выбран один положительный k, для которого k theta близок к π/8 modulo2π. Обозначим `alpha=4k theta`, `R_j=G^j`. Последовательности задаются в matrix order:

```
X_hat=R_(4k) Z,          target X=R(pi/2) Z,
H_hat=R_(2k) Z,          target H=R(pi/4) Z,
CCX_hat=R_t(alpha P_c1c2) R_a(2alpha P_c1c2t).       (2)
```

В последнем случае chronological first block — вращение вспомогательного a на8k theta при трёх controls111; затем target t вращается на4k theta при двух controls11. В идеальном пределе alpha=π/2 первый блок равен Z_t на секторе c1=c2=1, **identity на обоих столбцах a**. Второй равен J_t. Поскольку JZ=X, их произведение — CCX⊗I_a. Вне сектора c1=c2=1 оба блока точно identity. Вспомогательный a может быть произвольным и запутанным: доказательство не предполагает a=0 или отдельного измерения.

Если `e_j=||G^j-R(target_j)||`, то точно

```
||X_hat-X||=e_4k,
||H_hat-H||=e_2k,
||CCX_hat-CCX tensor I_a|| <= e_4k+e_8k <=3 e_4k.    (3)
```

Последняя оценка следует из telescoping двух unitary blocks; `||U²-V²||≤2||U-V||`. В самом сертификате использована прямая более точная сумма отдельно ограниченных e_4k,e_8k. Один и тот же a можно применять в следующих macro, даже если предыдущий оставил небольшую корреляцию: (3) действует на **всех** входах. Общая ошибка суммируется, а не обнуляется утверждением об ideal reset. Actual aux не восстановлен точно; ideal comparison operator содержит I_a.

X_hat и H_hat сами являются точными отражениями, поскольку ZR(beta)Z=R(-beta). Для CCX_hat этого нет. Hostile test обнаруживает, что два применения CCX_hat при k=1 не возвращают вход; нельзя использовать его же как неоплаченный точный inverse.

## 3. Сертификат без доверия к численному поиску угла

`certify_boolean_angle.py` использует continued fraction/mpmath только для **предложения** k. Ни π, ни численное значение theta не входят в исполняемую native грамматику или в критерий принятия. Окончательный сертификат `NATIVE_BOOLEAN_ANGLE.json` заново вычисляет рациональные enclosures cos/sin точных `G^(2k)`, `G^(4k)`, `G^(8k)` через owning integer-root и outward dyadic binary powering. Precision16640 bits, k4111 bits. Все numerator endpoints записаны в hex с явным dyadic denominator.

Для target H число1/sqrt2 также ограничено двумя соседними integer-root dyadics. Для target X используются(0,1), для вспомогательного phase —(-1,0). Для любого такого real rotation

```
||R(c,s)-R(c0,s0)|| = sqrt((c-c0)²+(s-s0)²)
                  <= |c-c0|+|s-s0|.
```

Из outward endpoints получены точные rational upper bounds. Их максимум для H, X и суммы CCX не больше2^-4096. Поле всех исполняемых коэффициентов остаётся исходным Q(sqrt(p)); это аппроксимация фиксированной логической операции, не непрерывно регулируемая физическая angle.

## 4. Реальный счёт forward и raw reverse

Для canonical layout target, controls, a отделены от доступного port/Spin. Каждый completed Z_q стоит6CX+2SourceI. Новые графики имеют:

| Macro | Forward primitive calls | Literal paid raw inverse calls |
|---|---:|---:|
| H |2k+8|22k+12|
| X |4k+8|44k+12|
| CCX |12k+92|96k+140|

Forward CCX inventory —12k G,24 SourceI,68 CX. Raw reverse обращает **каждый** реальный исходный primitive: CX сам себе inverse, SourceI^-1=SourceI³, один G^-1 имеет5 calls на port или11 на другом q. Так, reverse большого repeatG содержит тот же repeat count настоящего inverse каждого G. Он не заменяется более дешёвой вновь спроектированной negative-power схемой. В `NATIVE_BOOLEAN_LIBRARY.json` представлены оба явных конечных DAG и их counts.

`check_native_boolean.py` выполнил полные expanded words для k=1,2 в исходном coefficient field, без tolerance:1536 all-input columns для X/H/CCX, включая произвольные port,Spin,aux,protected spectator, и96 raw-inverse случаев. Все primitive адреса дополнительно проверены owning native domain. Эти малые exact проверки связывают реальный emitted syntax с (1)–(2); huge-k correctness даётся той же алгеброй и независимым interval certificate, не утверждением об исполнении гигантской матрицы.

## 5. Подстановка во все фиксированные A13 схемы

`lower_native_selectors.py` задаёт fixed generator: каждый gate настоящего A13 iterator заменяется его native DAG, CX остаётся точным. В JSON закреплены hashes исходных схем и iterator, k и native library, wire map, весь inventory. Включены **три полных decoders и обе cap7 first-success label схемы**. Их native carriers имеют2773,3190,234,76,44 wires соответственно: исходная схема плюс отдельные port/Spin, один общий a и protected oldRIGHT witness. В действительном большом графе эти роли должны быть предоставлены разрешённым аппаратом, не считаться бесплатными wire allocations.

Все macro endpoints сохраняют port/Spin точно; oldRIGHT не затрагивается ни на одном gate. Все исходные read-only j/Golden/fair или ready/label inputs остаются read-only и внутри раскрытых native macro. Aux принадлежит WORK; его допускаемая малая корреляция остаётся в полном operator error. Точные инварианты не выводятся из близости норм, а следуют из адресации и (1).

Для любого fixed logical circuit с N_X,N_H,N_CCX и exact CX имеем

```
||U_native - U_logical tensor I_aux||
 <=(N_X+N_H+N_CCX)·2^-4096.                         (4)
```

На семи A13 decoder/first-success report частях известно ровно92 263 351 768 approximate macro occurrences <2^37. Их суммарная ошибка **<2^-4059**. Это bound для этих частей при предоставленных входах. Остальные source preparation, DAG stack/offset lookup, payload routing, physical births, marks/seal и clock в число не включены. Для полного writer требуется отдельная сумма по всем occurrences, включая actual обратные блоки и marks.

## 6. Физический остаток

Логические X/H/CCX больше не требуют неподтверждённого measurement/feedforward переноса: дан прямой all-column native approximation route с конкретным k, genuine primitive words и error. Это не даёт точную общую READY приближённому writer; его эффект может слабо зависеть от входа. В H.1 target имеет своё ideal α, а actual error переносится через e_B≤2η только после сохранения точной SAM-block/D-identity структуры и использования actual c,w. Conditional lower bound ideal α≥1/2, полный Hessian L, все прочие macro budgets и физическое C ещё нужно установить. B29 выделяет соответствующие условия и ошибку e_B/(g s), не подменяя их component READY.

Native approximation — не доказательство физического выбора этой программы или Einstein source. Полная цель ОТО, её dynamics/refinement и исходная Cost−Info остаются открытыми. `GR_closed=false`.
