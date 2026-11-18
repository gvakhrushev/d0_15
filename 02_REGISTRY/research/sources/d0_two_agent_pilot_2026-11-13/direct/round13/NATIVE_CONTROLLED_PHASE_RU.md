# Подстановка owned controlled Z с сокращённым маршрутом

Потребитель — оставшаяся логическая `CZ` в B27 controlled signed involution. **Сама phase identity уже принадлежит исходному owner**: `A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md`, §7dk, формула (971), строки89723–89738; она также потреблена в retained-history RP1 около178110. Это не новая теорема о существовании CZ. Изменение здесь — её подстановка в актуальный B27 processor, буквальный проверенный word и сокращение общего маршрута с25 до19 calls. Используется тот же один доступный SourceI port, тот же неизвестный quaternion Spin dimension4 и только разрешённые ordinary CX. Из B27 известны точные `SourceI²=Z_port⊗I_Spin` и routed SourceI через два SWAP.

Обозначим `S_q` оператор, применяющий `L_i` к общему Spin при ordinary bit q=1. Если q не port, это в точности `SWAP(q,port); SourceI; SWAP(q,port)`. Все обычные регистры и неизвестный port восстанавливаются на границе. Имеем `L_i^4=I`, `S_q^-1=S_q^3`. Для двух разных ordinary c,t:

```
S_c S_t CX_(c,t) S_t^-1 CX_(c,t)
 = L_i^(c+t-(c xor t))
 = L_i^(2ct)
 = (-1)^(ct) I_Spin
 = CZ_(c,t) tensor I_Spin.                 (1)
```

Это операторное равенство на **всех** колонках, не только на Spin eigenstate или выбранном READY-секторе. `S_c,S_t` используют один и тот же quaternion action; это существенно для сложения степеней. CX меняет t на `t xor c`, оба CX восстанавливают data. Линейность даёт тот же вывод для произвольной запутанности c,t,port,Spin и остальных факторов.

`compile_native_cz.py` выдаёт реальный chronological word. Если t — физический port, это

```
CX(c,port); SourceI³; CX(c,port); SourceI;
SWAP(c,port); SourceI; SWAP(c,port).
```

Ровно **8 CX +5 SourceI =13 calls**. Если оба c,t отличны от port, добавляются внешние `SWAP(t,port)` и обратный: **14 CX +5 SourceI =19 calls**. При c=port аргументы меняются местами, поскольку CZ симметричен. Spin не адресуется по отдельности, oldRIGHT не используется, дополнительные нулевые или единичные resources отсутствуют. Требуется разрешённый доступ к одному исходному port и указанным CX; все промежуточные вызовы реальны и подлежат оплате/маркировке.

Owner (971) сохранял три отдельно routed S-вызова:20CX+5SourceI=25. Здесь target остаётся на общем port внутри всей middle-операции, поэтому нужно14CX. Это **новый спроектированный порядок выполнения**, не удаление уже оплаченных gates из чужой истории. Равенство конечного CZ не отождествляет прежние и новые промежуточные marks, raw source covectors, clock или цену; их следует вычислить для действительного19-call word.

[NATIVE_CZ_CHECK.json](NATIVE_CZ_CHECK.json) содержит буквальные Execution words. Исходный native domain проверил их допустимость, а точная алгебраическая матрица — все16 или32 колонок в четырёх вариантах положения control/target. Численного tolerance, measurement/feedforward и postselection нет. Теорема (1) доказывает общее действие для любого числа дополнительных spectator factors.

Это прикладное уточнение к B27: его `CZ` больше не является невыпущенным native primitive. `Z` и `CX` также имеют собственные exact реализации. Для целого controlled-V всё ещё остаются native `X`, `CCX`, реальный lookup и Hadamard test; текущий A13 selector не объявляется полным native word. Общая READY, полная отмеченная история/clock и физическая Cost−Info не вычислены. `GR_closed=false`.
