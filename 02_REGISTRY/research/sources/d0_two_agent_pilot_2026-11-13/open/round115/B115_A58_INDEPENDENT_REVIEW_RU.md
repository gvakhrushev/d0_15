# B115. Независимая проверка A58 plane-суммы и физического pullback

**Результат: условный PASS.** На том же A57 field-bound graph A58 правильно выражает 2688 raw MG2 rows через полный набор Pf plane contrasts и применяет к ним forward derivative B114. Перенос ошибки в исходную физическую норму имеет вид `α_h·2^-34` с непереопределённой `α_h=||iota_h||_(V_h→ℓ²)`; обратимость общего physical connection→holonomy для этого forward pullback не требуется. Производственные суммы, физический reader и полная Cost−Info связь не исполнены. `physical_C_closed=false`, `GR_closed=false`.

[Независимая проверка](audit_field_source_pullback.py) и [receipt](B115_A58_AUDIT_CHECK.json) закрепляют пять frozen файлов A58, A57 и B114. Существующие сертификаты B112/B113 потребляются по SHA без нового огромного compiler или повторного расчёта production сетки.

## 1. Полная сумма и знаки

Для raw coordinate j локальная цифра кодируется двумя позициями **`j` и `2688+j`**: сначала все low, затем все high. Для каждого набора `s` остальных 5374 битов обозначим через `b_j(s,i)` полный индекс с локальной цифрой `i=0,1,2,3`. Именно все spectators, а не только подготовленная нулевая колонка, входят в identity

    X_j = Σ_s Σ_(i<k) λ_ik E_(b_j(s,i),b_j(s,k)),
    E_ab[a,b]=−1,  E_ab[b,a]=1.

Независимый перебор всех `a<b` для `m=1,…,4` строит поддержку по bit masks, без использования A58 алгоритма вставки, и сверяет **1878** plane terms и их точные коэффициенты/ориентацию. Для всех 2688 production j также независимо проверены физические пары `(2+j,11893771936+j)`; для крайних и среднего j восстановлены разные полные spectator patterns. Проверены 36 настоящих A57 пар signed Pf requests на одном поле.

Поэтому `r_j=Σ_s Σ_(i<k)λ_ik fhat_Pf(E_(b_j(s,i),b_j(s,k)))` использует `6·2^5374` plane rows и `12·2^5374` signed requests на j, всего `32256·2^5374` signed requests на все j. Это точное конечное определение, не оценка практической скорости и не выполненная сумма. A58 generator выдаёт реальные labels; `bounded_raw_row` честно ограничен Q4/рациональными диагностическими rows и не выдаёт трансцендентные `H+J` цены за элементы Q4.

Исходная MG2 identity `[V_j,X_k]χ=δ_jk χ` и `||Σv_jX_j||op≤Σ|v_j|<52||v||₂` дают изометрический B109 lift `||Rraw(v)||raw=||v||₂`. Отсюда непосредственно

    ||r−DIτ(Y)||₂ <2^-34.

Второй множитель числа plane rows не появляется: оценка A57 уже является полной raw-dual оценкой интерполянта. При этом r — **сумма отдельно нормированных finite rows**, а не заявленная цена одного совместно скомпилированного `Σv_jX_j`. В точном трёхмерном Cayley fixture отношение feedback denominators для `X+Y` отличается от произведения соответствующих отношений для X и Y; значит конечная нелинейная price difference вообще не обязана быть аддитивной. Fixture не является производственной ценой.

## 2. Точка поля и forward chain rule

`bound_chart_point` привязывает точку к SHA того же `FieldCentre`: exact outward intervals для u строятся из исходной A53/A48/A20 формулы и coframe offsets, θ равен точным rational link offsets. Для всех 64 узлов и 1024 coframe entries независимо сверены вложение 192-bit intervals в 128-bit и прибавление нужного offset. Отдельная высокоточная численная диагностика всех 1024 компонент воспроизводит исходную B21 формулу; она не заменяет integer/interval proof. Все 1536 link offsets проверены по роли и генератору. Все 128 matter offsets проверены непосредственно в A53 q-provider при одинаковых CODE digits по обе стороны, чтобы sampled shift сократился. Rounded `BRINKMANN_L4_CENTRE.jsonl` не используется как точный field name; sampled digits не подменяют centre offsets.

B114 фиксирует конкретную производную для `δE`, left-trivialized `δU_J U_J⁻¹` и `δψ`. В частности, `u=A E⁻ᵀ`, `A=νη_NS`, `E=Aᵀu⁻ᵀ`, а link блок использует `dexp_Θ⁻¹` и S signs. Это raw current inverse-leg без дополнительного подставленного множителя `sqrt(ρ)`; связь writer `V=s_cal sqrt(ρ) T u` условна на одном и том же descriptor. Динамические PF/frame/collar и иные действительные независимые источники не поглощаются этой fixed-slice картой.

Для действительного `iota_h=Dχ_h` обычное transpose application даёт

    fhat_phys=r iota_h,
    D(Iτ∘χ_h)=DIτ iota_h,
    ||fhat_phys−D(Iτ∘χ_h)||_(V_h*) < α_h·2^-34,
    α_h=||iota_h||_(V_h→ℓ²).

Исходная `V_h` norm сохраняется; ни `α_h=1`, ни h-uniform bound не заданы. Это forward pullback, поэтому он корректен и при ненулевом `ker iota_h`; обратный переход к полному physical source требует отдельно исследовать такие направления. В частности, finite based-link Jacobian не устраняет возможное ядро общего C² connection→holonomy. Реальная калибровка CODE изменения содержит шаг `σ`; physical right lift, если он допущен и нужен, несёт `1/σ`.

Поздний §7fu сохраняет открытой physical C: операторно-статистическая source identity на графе сама не устанавливает полную memory-valued Cost−Info equivalence. Original A23/fine instrument и marked transport, PF/boundary/frame и другие независимые source rows, истинная `V_h` norm/admission и GR refinement остаются отдельными обязательствами.
