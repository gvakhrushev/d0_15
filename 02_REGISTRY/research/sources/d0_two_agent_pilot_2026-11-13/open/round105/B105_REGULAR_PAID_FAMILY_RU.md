# B105. Полевая paid family с post от actual M(Y)

**Статус.** Реализован consumer зафиксированного A54 `GlobalSource(field)` для четырёх независимых control slots, actual path-sum target, field-bound post и нового оплаченного общего clock. Его all-column SOURCE contracts и CODE-support потребляются условно до независимой проверки B106. `physical_C_closed=false`, `GR_closed=false`.

## Равномерная положительность на заявленном chart

При тех же actual/ideal source targets, что в B91/A49, идеальный completed-bank prefix `B_Y` удовлетворяет `||DB_Y||≤M1=1748` на старом B21 cube. Из 2688 смещений `|Y_j|<2^-32` имеем `||Y||₂<52·2^-32`. Общий идеальный comparator — отражённая последовательность `B_Y† S B_Y` с fixed field-independent S. По телескопированию на **всём** retained carrier

    ||M_ideal(Y)−M_ideal(0)|| ≤ 2·1748·52·2^-32.

Это сравнение относится к одному CODE label и одинаковому положению его `σ(d−3p²)`; оно не смешивает разные sampled branches. Из исходного A49 `M_ideal,b(0)>67/100` и требуемого A54 полного canonical compression error `e_M<2^-3421` на этом же all-input contract следует для каждого b и рационального Y

    M_actual,b(Y) > 67/100 − 181792·2^-32 − 2^-3421
                  > 669/1000 > 2/3.                       (P1)

Численно первое выражение около 0.66995767; строгим свидетельством служит точное рациональное неравенство, не округление. Компрессия exact unitary G/CX word имеет `|M_b|≤1`, а её действительная диагональность требует отдельно установленного CODE-control-only support нового A54. B91 bound относится к исходному ideal SOURCE на всём chart; она не является автоматическим следствием совпадения одного output corner. A54 должен доказать именно ту же исходную A23/B25 extension и uniform `e_M`.

Тогда `r(Y)=||M_actual(Y)χ||>669/1000`. Для каждого из конечного числа CODE labels `χ_b≥p^5376>2^-5376` и

    h_b=χ_b[1+M_actual,b(Y)/r(Y)]>χ_b>2^-5376.

В `PositiveTarget.star` исходный положительный `h_0` входит в любой радиус, поэтому промежуточные знаменатели имеют ненулевые реальные bounds и adaptive interval вычисление останавливается. Условием служит конкретный реальный path-sum actual M(Y); таблица A48/M(0) не подставляется вместо него.

## Реальное связывание и четыре slots

[`regular_paid_family.py`](regular_paid_family.py) получает два разных объекта: `api` с pinned uniform A54 namespace/inventory и `api.GlobalSource(field)`, чей actual `core_blocks` формирует `ActualDiagonal` для именно данного immutable FieldCentre. Каждый экземпляр имеет отдельную target cache; замена field внутри source, вложенных sources или components запрещается проверкой до потребления. По actual path-sum конструируется `h`, после чего исполняются те же четыре платных star lists A49, но для нового M(Y). Сравниваемые arms с **одним фиксированным Y** используют один и тот же post; он не пересчитывается в зависимости от slot, sign или axis.

Хронология остаётся исходной:

    Pf ; B(Y) ; Qf† ; middle ; Qb ; return ; Pb† ; U_post(Y) ; post_probe.

`matched=(s,−s,s,−s)`, а четыре независимых arm сохраняют собственные единственные ненулевые occurrence. Post-probe после post не подменяет Pb до post. Входной CODE/birth layout непосредственно сверяется со старым A47 control layout: reuse A47 controls допустим только при фактическом равенстве всех 5376 адресов и исходного birth count.

**Важно:** `U_post(Y)` задаётся одной формулой на поле, но может меняться при переходе между разными Y. Нельзя считать этот post постоянным в полевых сравнениях или подставлять его отдельный минимум без actual source этого выбора. A37/B73 дают exact ideal J-envelope и B102 — conditional finite-value error, но clock/heat и полный Cost−Info этого сами не устраняют. В точке `Y≠0` нуль source или stationary row не утверждается.

## Новый общий padding и цена

Вместо старого A49 inventory consumer получает **одну заранее сертифицированную uniform componentwise upper** `W_G_CX_upper`, сверяет, что она покрывает конкретный A54 источник, и реально исполняет A49 `counted_pad`. Для каждого поля и всех slots берутся одинаковые upper/padded lengths; приближённая длина исходного word не объявляется exact счётом. `postL`, `probeL` и четыре `controlL` вычисляются по исходной одинаковой A49 grammar, `coreL` — по **новому** upper. Настоящий `K` выбирается после нового `Nbase`:

    K=4[bit_length(Nbase)+3208+1700+20+75+1+8064],
    N=Nbase+2K,
    D=2^n(Lbase−2+3·2^K)−1,   n=11893774624.

В зафиксированном A54 `Nbase.bit_length=30833`, `K=175604`, как и прежде по этим двум параметрам; однако exact `coreL`, `Nbase` и `D` отличаются от A49. Это новый clock и новое платное padding, несмотря на совпадающий K. Любые фактически исполненные вычисления field/compiler/post требуют собственной оплаты; конечный математический path-sum сам не объявляется выполненным физическим калькулятором.

Условно на единую uniform upper, A54 source error, CODE support, исходные A49 grid/gain/heat prerequisites и положительность (P1), прямой пересчёт сохраняет вычисленные envelopes `post full-operator <2^-9247`, post-skew dual `<2^-661`, heat-skew dual `<2^-75`. После post точный нижний предел `c₀(Y)>669/1000−2^-9247>2/3` подтверждён рациональной проверкой. Нормировка `Γ_Y` использует реальный `c₀(Y)`, фактический K, исходное `gσ` и фиксируется при каждом сравнении; это `DB/Γ`, не `D(B/Γ)`.

## Проверки и границы

[`check_regular_paid_family.py`](check_regular_paid_family.py) проверяет positivity точными `Fraction`, два разных `FieldCentre` с одинаковым новым общим clock и разными source objects/cache, отказ слишком малого upper/изменённого field, семь representative фактических начала control DAG и независимость четырёх signs. На двух A54 FieldCentre один и тот же coframe sector производит разные сертифицированные native angle powers; на малых **реальных** G/CX словах два источника дают разные точные interval `M_b` и разные выбранные B80 post powers. Вместе с проверкой bound-method это проверяет привязку к новому источнику, а не вычисляет giant production M или post.

Проверены SHA обоих receipts A54 и зафиксированы все шесть файлов. Требуются независимая проверка фактической CODE-only grammar, uniform source/clock certificate и сопоставление той же A23/B25 ideal family; physical fine instrument, `V_h`/full control-source, действительная Cost−Info и refinement остаются отдельными. Это не zero-stationarity proof для нового поля и не полноценная GR closure.
